from fastapi import FastAPI

app = FastAPI()

@app.get("/test1")
async def root1():
  return {"name": "둘리"}

@app.get("/test2")
async def root2():
  return ["둘리", "또치", "도우너"]

@app.get("/test3")
async def root3():
  return "<h1>안녕?</h1>"

@app.get("/test4")
async def root4():
  return 1000