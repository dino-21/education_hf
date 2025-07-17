from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

templates = Jinja2Templates(directory="templates") 

translator = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 로컬 경로로 모델 로딩
    translator["translation"] = pipeline(
        "translation",
        model="C:/education_hf/model_download/opus-mt-ko-en"
    )
    print("✅ 번역 모델 로딩 완료")
    yield
    translator.clear()

# ✅ lifespan 적용
app = FastAPI(lifespan=lifespan, docs_url="/documentation", redoc_url=None)

# ✅ CORS 설정 필요 시
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translation_text: str

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    translated_text = translator["translation"](request.text)
    return {"translation_text": translated_text[0]['translation_text']}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("exam26_v.html", {"request": request})
