import os
import whisper
import streamlit as st

st.set_page_config(
    page_title="Whisper based ASR",
    page_icon="musical_note",
    layout="wide",
    initial_sidebar_state="auto",
)

upload_files_directory = 'uploads/'

# Загружаем аудиофайл
def Upload_audio_file():
    # Uploadind file
    uploaded_object = st.file_uploader(
        type=['opus', 'mp3', 'aac', 'flac', 'wv', 'wav',
              'mp4', 'mov', 'wmv', 'webm', 'avi', 'mkv'],
        label='Выберите аудио или видео для распознавания',
        accept_multiple_files=False,
    )
    if uploaded_object is not None:
        with open(os.path.join(upload_files_directory, uploaded_object.name), 'wb') as file:
            file.write(uploaded_object.getbuffer())
        return uploaded_object.name
    else:
        return None

# Транскрибируем аудио
def Trasncribe(audio):
    # Транскрибация аудио в текст
    model = whisper.load_model('base')
    result = model.transcribe(audio)
    st.write(result['text'])

# UI заголовок
st.title('Транскрибация аудио')

# Передача Bytes в аудиофайл
audio_file = Upload_audio_file()

# Вызов функции Trasncribe
action = st.button('Распознать аудио')
if action:
    st.title('Транскрипция')
    st.subheader(audio_file + ':')
    st.write(Trasncribe(os.path.join(upload_files_directory, audio_file)))