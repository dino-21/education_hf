from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import urllib.request
from bs4 import BeautifulSoup

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
  "http://localhost:5500",
  "http://127.0.0.1:5500"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/weather")
async def main():
  res = urllib.request.urlopen("http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4161060000")
  bs = BeautifulSoup(res, "xml")
  wname = bs.find("wfKor").string
  print(wname)

  if wname in ["구름많음", "흐림"] :
    img = "cloud.png"
  elif wname == "구름조금":
    img = "cloud_sun.png"
  elif wname == "맑음":  
    img = "sun.png"
  elif wname in ["비", "흐리고 비"]:
    img = "rain.png"
  elif wname == "눈":
    img = "snow.png"
  else:
    img = "etc.png"

  return {"img": img}