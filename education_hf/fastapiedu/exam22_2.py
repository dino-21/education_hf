from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Form
from transformers import pipeline
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from typing import Annotated

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 로컬 모델 경로 설정
    ml_model["translation"] = pipeline("translation", model="C:/education_hf/model_download/opus-mt-ko-en")
    ml_model["classifier"] = pipeline("sentiment-analysis")  # 사전 내장 모델 사용
    print("✅ 로컬 모델 로딩 완료")
    yield
    ml_model.clear()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/predict", response_class=HTMLResponse)
def predict(content: Annotated[str, Form()]):
    print(f"[입력] {content}")
    
    translated = ml_model["translation"](content)
    eng_content = translated[0]['translation_text']
    print(f"[번역] {eng_content}")

    result = ml_model["classifier"](eng_content)
    label = result[0]['label']
    score = result[0]['score']

    result_text = f"{score:.3f}% 정확도로 {'긍정' if label == 'POSITIVE' else '부정'}입니다."

    return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>결과</title>
        </head>
        <body>
            <h1>Hugging Face AI Model 활용</h1>
            <img src="static/images/hf1.png" width="100">
            <hr>
            <h3>입력한 문장: {content}</h3>
            <h3>영문 번역: {eng_content}</h3>
            <h3>결과: {result_text}</h3>
            <a href="/">🔙 돌아가기</a>
        </body>
        </html>
    """

@app.get("/")
async def main():
    content = """
    <!DOCTYPE html> 
    <html>
        <head>
            <meta charset="UTF-8">
            <title>HTML학습</title>
        </head>
        <body>
            <h1>Hugging Face AI Model 활용</h1>
            <img src="static/images/hf1.png" width="100">
            <hr>
            <h3>긍정&부정을 채크하려는 문장을 한국어로 입력하세요.</h3>
            <form action="/predict" method="post">
                <textarea name="content" rows="5" cols="50"></textarea><br>
                <input type="submit" value="요청">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=content)
