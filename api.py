from fastapi import FastAPI, UploadFile, File
from starlette.requests import Request
import os
import whisper

# Создаем экземпляр FastAPI
app = FastAPI()

# Определяем директорию для хранения загруженных файлов
upload_files_directory = "uploads/"


# Создаем маршрут для загрузки файла
@app.post("/uploadfile/")
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    try:
        # Открываем файл в режиме записи байтов
        with open(os.path.join(upload_files_directory, file.filename), "wb") as buffer:
            # Читаем содержимое файла и записываем его в буфер
            contents = await file.read()
            buffer.write(contents)
        # Возвращаем имя загруженного файла
        return {"filename": file.filename}
    except Exception as e:
        # Возвращаем сообщение об ошибке в случае исключения
        return {"error": str(e)}


# Создаем маршрут для транскрибирования аудио
@app.get("/transcribe/{filename}")
async def transcribe_audio(filename: str):
    # Загружаем модель whisper
    model = whisper.load_model("base")
    # Транскрибируем аудиофайл
    result = model.transcribe(os.path.join(upload_files_directory, filename))
    # Возвращаем результат транскрибирования
    return {"text": result["text"]}


# Эта функция возвращает список всех загруженных файлов.
# Она просто читает все файлы в директории upload_files_directory и возвращает их имена.
@app.get("/listfiles")
async def list_files():
    files = os.listdir(upload_files_directory)
    return {"files": files}


# Эта функция удаляет указанный файл.
# Она принимает имя файла в качестве параметра, проверяет, существует ли такой файл,
# и если файл существует, удаляет его и возвращает сообщение об успешном удалении.
# Если файла не существует, возвращается сообщение об ошибке.
@app.delete("/deletefile/{filename}")
async def delete_file(filename: str):
    file_path = os.path.join(upload_files_directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"{filename} deleted successfully"}
    else:
        return {"error": f"{filename} does not exist"}
