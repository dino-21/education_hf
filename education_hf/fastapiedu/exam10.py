from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

@app.post("/items", status_code=201)
async def create_item(item: Item):
  item_dict = item.model_dump()
  print(item_dict)
  if item.tax:
    price_with_tax = item.price + item.tax
    item_dict.update({"price_with_tax": price_with_tax})
  return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
  return {"item_id": item_id, **item.model_dump()}