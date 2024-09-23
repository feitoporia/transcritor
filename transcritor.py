import os
from tkinter import Tk, filedialog, messagebox, Text, Button, Label, END
from tkinter.ttk import Progressbar
import speech_recognition as sr
from pydub import AudioSegment
from docx import Document

def convert_audio_to_wav(input_file):
    file_extension = os.path.splitext(input_file)[1].lower()
    if file_extension in [".mp3", ".ogg", ".aac"]:
        try:
            audio = AudioSegment.from_file(input_file, format=file_extension.replace(".", ""))
            wav_output = os.path.splitext(input_file)[0] + ".wav"
            audio.export(wav_output, format="wav")
            return wav_output
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter o arquivo de áudio: {e}")
            return None
    elif file_extension == ".wav":
        return input_file
    else:
        messagebox.showerror("Erro", "Formato de arquivo não suportado. Use MP3, OGG, AAC ou WAV.")
        return None

def transcribe_audio_in_chunks(file_path, chunk_size=60000):
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_wav(file_path)
        duration = len(audio)
        transcription = ""
        
        progress_bar["maximum"] = duration
        progress_bar["value"] = 0

        for start in range(0, duration, chunk_size):
            end = min(start + chunk_size, duration)
            chunk = audio[start:end]

            chunk_wav_path = "temp_chunk.wav"
            chunk.export(chunk_wav_path, format="wav")

            try:
                with sr.AudioFile(chunk_wav_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="pt-BR")
                    transcription += text + " "
            except sr.UnknownValueError:
                transcription += "[Inaudível] "
            except sr.RequestError as e:
                transcription += f"[Erro de solicitação: {e}] "

            # Atualiza a barra de progresso
            progress_bar["value"] = end
            root.update_idletasks()

        return transcription.strip()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo de áudio: {e}")
        return None

def save_to_word(transcription):
    save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Documento Word", "*.docx")])
    if save_path:
        doc = Document()
        doc.add_paragraph(transcription)
        doc.save(save_path)
        messagebox.showinfo("Sucesso", f"Transcrição salva com sucesso em {save_path}")

def select_audio_file():
    input_file = filedialog.askopenfilename(
        title="Selecione o arquivo de áudio",
        filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.ogg *.aac")]
    )
    return input_file

def transcribe_audio():
    input_file = select_audio_file()
    if not input_file:
        return

    wav_file = convert_audio_to_wav(input_file)
    if not wav_file:
        return

    transcription = transcribe_audio_in_chunks(wav_file)
    if transcription:
        transcription_box.delete(1.0, END)
        transcription_box.insert(END, transcription)
    else:
        messagebox.showwarning("Aviso", "Nenhuma transcrição disponível.")

def save_transcription():
    transcription = transcription_box.get(1.0, END).strip()
    if transcription:
        save_to_word(transcription)
    else:
        messagebox.showwarning("Aviso", "Nenhuma transcrição para salvar.")

def create_gui():
    global root, transcription_box, progress_bar
    root = Tk()
    root.title("Transcrição de Áudio para Texto")

    Label(root, text="Transcrição de Áudio", font=("Arial", 14)).pack(pady=10)

    transcription_box = Text(root, wrap="word", width=80, height=20, font=("Arial", 12))
    transcription_box.pack(padx=10, pady=10)

    Button(root, text="Selecionar e Transcrever Áudio", command=transcribe_audio, font=("Arial", 12), width=25).pack(pady=5)
    Button(root, text="Salvar Transcrição em Word", command=save_transcription, font=("Arial", 12), width=25).pack(pady=5)

    # Barra de progresso
    progress_bar = Progressbar(root, orient="horizontal", length=500, mode="determinate")
    progress_bar.pack(pady=10)

    root.geometry("700x600")
    root.mainloop()

if __name__ == "__main__":
    create_gui()
