from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):

  return templates.TemplateResponse(name="exam8_v.html",   
                    context={"request":request,
                              "id": id, "nextid" : 1 if id == 10 else id+1, "img_name" : f"images/{id}.jpg"})