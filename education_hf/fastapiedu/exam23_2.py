from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from transformers import pipeline
from contextlib import asynccontextmanager

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 로컬 경로에 저장된 summarization 모델 로딩
    ml_model["summarizer"] = pipeline("summarization", model="C:/education_hf/model_download/distilbart-cnn-12-6")
    print("✅ 로컬 요약 모델 로딩 완료")
    yield
    ml_model.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/summarize", response_class=HTMLResponse)
async def summary(file: UploadFile):
    content = await file.read()
    content = content.decode("utf-8")
    content = content.replace('\r\n', ' ').replace('\n', ' ')
    
    # 허깅페이스 summarizer는 길이 제한이 있음 (기본 max 1024 tokens)
    result = ml_model["summarizer"](content, max_length=130, min_length=30, do_sample=False)

    return HTMLResponse(content=f"""
        <html>
            <body>
                <h2>📄 요약 결과</h2>
                <hr>
                <p><strong>요약된 내용:</strong></p>
                <p>{result[0]['summary_text']}</p>
                <br><a href="/">🔙 다시 업로드</a>
            </body>
        </html>
    """)

@app.get("/")
async def main():
    content = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>텍스트 요약기</title>
        </head>
        <body>
            <h2>📄 요약하려는 텍스트 파일을 업로드하세요</h2>
            <hr>
            <form action="/summarize" enctype="multipart/form-data" method="post">
                <input name="file" type="file" required>
                <input type="submit" value="요약 요청">
            </form>       
        </body>
    </html>
    """
    return HTMLResponse(content=content)
