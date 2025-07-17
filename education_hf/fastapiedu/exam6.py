from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
  item = {"item_id": item_id}
  if q:
    item.update({"q": q})
  if not short:
    item.update(
      {"description": "유용하고 잘 만들어진 상품"}
    )
  return item

@app.get("/items2/{item_id}")
async def read_user_item(item_id: str, needy: str):
  item = {"item_id": item_id, "needy": needy}
  return item