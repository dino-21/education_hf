from typing import Any, List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
  name: str
  description: Union[str, None] = None
  price: Union[float, None] = None
  tax: Union[float, None] = None
  tags: List[str] = []

@app.post("/items1", response_model=Item)
async def proc1(item: Item) :
  return item

@app.get("/items2", response_model=List[Item])
async def proc2() :
  return [
    {"name": "둘리", "price": 42.0},
    {"name": "또치", "price": 32.0},
    {"name": "도우너", "price": 32.0},
  ]

my_items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items3", response_model=List[Item])
async def proc3():
    return my_items

@app.get("/items4", response_model=dict[str, float])
async def proc4():
  return {"foo": 2.3, "bar": 3.4}
