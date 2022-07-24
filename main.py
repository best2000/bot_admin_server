from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
#uvicorn main:app --reload
#api docs => http://127.0.0.1:8000/docs

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: int=None):
    return {"item_id": item_id, "q": q}
