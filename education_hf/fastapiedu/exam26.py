from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

app = FastAPI(docs_url="/documentation", redoc_url=None)

templates = Jinja2Templates(directory="templates") 

translator = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    translator["translation"] = pipeline("translation", model="Helsinki-NLP/opus-mt-ko-en")
    yield
    # Clean up the ML models and release the resources
    translator.clear()

app = FastAPI(lifespan=lifespan)

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
    return templates.TemplateResponse("exam26_v.html",{"request":request})

