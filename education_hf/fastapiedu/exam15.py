from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/insert")
async def login(username: Annotated[str, Form()], emailaddress: Annotated[str, Form()]):
  print(username, emailaddress)  
  return {"username" : username, "emailaddress" : emailaddress}

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
        <h1>개인 정보 작성</h1><hr>
        <form action="/insert/" method="post">
        <input name="username" type="text" placeholder="계정을 입력하세요"><br>
        <input name="emailaddress" type="email" placeholder="메일주소를 입력하세요"><br>
        <input type="submit" value="요청">
        </form>
      </body>
    """
  return HTMLResponse(content=content)