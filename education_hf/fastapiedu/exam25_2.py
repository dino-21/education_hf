from typing import Union
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse
from transformers import pipeline
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 로컬 경로로 모델 로딩
    ml_model["summarizer"] = pipeline(
        "summarization",
        model="C:/education_hf/model_download/distilbart-cnn-12-6"
    )
    print("✅ 요약 모델 로딩 완료")
    yield
    ml_model.clear()

templates = Jinja2Templates(directory="templates")
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static") 

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("exam25_v1.html", {'request': request})

@app.post("/summarize", response_class=HTMLResponse)
async def summary(request: Request, file: UploadFile):
    content = await file.read()
    content = content.decode("utf-8")
    content = content.replace('\r\n', ' ').replace('\n', ' ')
    
    result = ml_model["summarizer"](content, max_length=130, min_length=30, do_sample=False)
    summary = result[0]['summary_text']

    return templates.TemplateResponse(
        "exam25_v2.html",
        {"request": request, "summary": summary}
    )
