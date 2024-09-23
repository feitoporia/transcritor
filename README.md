# Transcrição de Áudio para Texto com Barra de Progresso

Este projeto é um aplicativo simples que permite ao usuário transcrever áudios para texto e salvar a transcrição como um documento Word. A transcrição do áudio é realizada em partes, e o progresso é mostrado em uma barra de progresso.

## Funcionalidades

- Suporta arquivos de áudio nos formatos: `.mp3`, `.wav`, `.ogg` e `.aac`.
- Transcreve o áudio para texto utilizando a API do Google.
- Exibe uma barra de progresso enquanto o áudio é processado.
- Permite salvar a transcrição em um arquivo `.docx` (Word).
  
## Dependências

Antes de usar o aplicativo, você precisará instalar as seguintes dependências:

- **SpeechRecognition**: Para fazer o reconhecimento de fala.
- **pydub**: Para manipulação de arquivos de áudio (conversão e divisão em chunks).
- **python-docx**: Para salvar a transcrição em um arquivo Word.
- **tkinter**: Para a interface gráfica do aplicativo.

### Instalação das dependências

Você pode instalar as dependências necessárias usando o `pip`. Execute o seguinte comando no terminal:

```bash
pip install SpeechRecognition pydub python-docx
