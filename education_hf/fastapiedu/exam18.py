from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from typing import List
import os
from contextlib import asynccontextmanager
import signal

@asynccontextmanager
async def my_lifespan(app: FastAPI):
    print("서버 기동시 실행")
    if not os.path.isdir("static/files"):
      os.mkdir("static/files")
    yield

app = FastAPI(lifespan=my_lifespan) 

@app.get("/kill") 
async def lll() :
  os.kill(os.getpid(), signal.SIGTERM)

@app.post("/singleuploadfile")
async def create_upload_file(file: UploadFile):
  path = f"static/files/{file.filename}"
  content = await file.read()
  with open(path, 'w+b') as fp:
    fp.write(content)

  return {
      'file': file.filename,
      'content': file.content_type, 
      'path': path,
  }

@app.post("/multiuploadfiles")
async def create_upload_files(files: List[UploadFile]):
  result = []
  for file in files:
    path = f"static/files/{file.filename}"
    content = await file.read()
    with open(path, 'w+b') as fp:
      fp.write(content) 

    result.append({
      'file': file.filename,
      'content': file.content_type,
      'path': path,
    })
  return result


@app.get("/")
async def main():
  content = """
      <body>
        <h2>파일 업로드하여 서버에 저장하기</h2>
        <hr>
        <form action="/singleuploadfile" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit" value="싱글파일 업로드">
        </form>
        <hr>
        <form action="/multiuploadfiles" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit" value="다중파일 업로드">
        </form>
      </body>
    """
  return HTMLResponse(content=content)