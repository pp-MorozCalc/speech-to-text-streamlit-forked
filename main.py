import os
import whisper
import streamlit as st

# Set page config
st.set_page_config(
    page_title='AI Speech to Text converter',
    page_icon='🎙️',
    layout='centered',
    initial_sidebar_state='auto',
)

# UI
st.title('Расшифруйте аудио или видео в текст ✨')
st.info('Загрузите ваш файл и получите его текстовую расшифровку. Сервис поддерживает все популярные аудио и видео форматы.')
st.divider()

upload_files_directory = 'uploads/'

# Upload audio or video file
def Upload_audio_file():
    # Upload file
    uploaded_object = st.file_uploader(
        type=['opus', 'mp3', 'aac', 'flac', 'wv', 'wav',
              'mp4', 'mov', 'wmv', 'webm', 'avi', 'mkv'],
        label='Выберите аудио или видео для распознавания',
        accept_multiple_files=False,
    )

    # Save uploaded bytes as file
    if uploaded_object is not None:
        with open(os.path.join(upload_files_directory, uploaded_object.name), 'wb') as file:
            file.write(uploaded_object.getbuffer())
        return uploaded_object.name
    else:
        return None

# Transcribe audio
def Trasncribe(audio):
    model = whisper.load_model('base')
    result = model.transcribe(audio)
    st.write(result['text'])

# Getting name of uploading file to put it into model
audio_file = Upload_audio_file()

# Call Trasncribe function
action = st.button('Распознать аудио', type='primary')
if action:
    st.subheader(audio_file)
    st.write(Trasncribe(os.path.join(upload_files_directory, audio_file)))