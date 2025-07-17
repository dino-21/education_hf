from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id):
  return {"item_id": item_id}

@app.get("/friend/{name}/{age}")
async def read_item(name : str, age : int):
  return {"이름": name, "나이" : age}