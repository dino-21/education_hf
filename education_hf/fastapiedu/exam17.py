from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/files")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
	content = """
					<body>
					<h2>다중 파일 업로드</h2>
					<hr>
					<form action="/files" enctype="multipart/form-data" method="post">
					<input name="files" type="file" multiple>
					<input type="submit">
					</form>
					<hr>
					<form action="/uploadfiles" enctype="multipart/form-data" method="post">
					<input name="files" type="file" multiple>
					<input type="submit">
					</form>
					</body>
					"""
	return HTMLResponse(content=content)