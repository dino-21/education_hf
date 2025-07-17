from typing import Dict, Annotated
from fastapi import FastAPI, Form
from transformers import pipeline
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse

classifier = None
@asynccontextmanager
async def startup(app: FastAPI):
  global classifier 
  classifier = pipeline("sentiment-analysis")
  print(classifier)
  yield

app = FastAPI(lifespan=startup)

@app.post("/predict", response_model = Dict)
def predict(content: Annotated[str, Form()]):
  result = classifier(content)
  return result[0]

@app.get("/")
async def main():
  content = """
      <!DOCTYPE html> 
      <html>
        <head>
        <meta charset="UTF-8">
        <title>FastAPI+HuggingFace</title>
      </head>
      <body>
        <h1>허깅페이스 모델을 활용한 sentiment-analysis 테스트</h1><hr>
        <form action="/predict" method="post">
        <input name="content" type="text" size="50" placeholder="분석을 원하는 글을 입력하세요"><br>
        <input type="submit" value="요청">
        </form>
      </body>
    """
  return HTMLResponse(content=content)
