from fastapi import FastAPI, Path, HTTPException
from typing import Annotated


app = FastAPI()

items = {"dooly": "귀여운 아기 공룡"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
      raise HTTPException(status_code=404, detail=f"{item_id} 명의 아이템은 존재하지 않습니다.")
    return {"item": items[item_id]}

@app.get("/items2/{item_id}")
async def read_item2(item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
                    q: str = 'unico'):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
