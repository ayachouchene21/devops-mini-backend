from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DevOps Mini Backend")

items = []

class Item(BaseModel):
    name: str


@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def add_item(item: Item):
    items.append(item)
    return {"message": "Item added", "item": item}
