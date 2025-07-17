from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from transformers import pipeline
from contextlib import asynccontextmanager
from PIL import Image
from io import BytesIO

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 로컬 모델 경로로 불러오기
    ml_model["imagetotext"] = pipeline(
        "image-to-text",
        model="C:/education_hf/model_download/blip-image-captioning-large"
    )
    print("✅ 이미지 캡셔닝 모델 로딩 완료 (로컬)")
    yield
    ml_model.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/imagetotext", response_class=HTMLResponse)
async def imagetotext(file: UploadFile):
    content = await file.read()
    img_content = Image.open(BytesIO(content))
    result = ml_model["imagetotext"](img_content)
    caption = result[0]['generated_text']

    return HTMLResponse(content=f"""
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
            <h2>🖼️ 이미지에 대한 설명 결과</h2>
            <hr>
            <p><strong>설명:</strong> {caption}</p>
            <a href="/">🔙 다시 업로드</a>
        </body>
        </html>
    """)

@app.get("/")
async def main():
    content = """
    <html>
    <head><meta charset="UTF-8"></head>
    <body>
        <h2>🖼️ 이미지에 대한 설명글을 작성하려는 이미지 파일을 업로드하세요</h2>
        <hr>
        <form action="/imagetotext" enctype="multipart/form-data" method="post">
            <input name="file" type="file" required>
            <input type="submit" value="설명 생성">
        </form>       
    </body>
    </html>
    """
    return HTMLResponse(content=content)
