from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str

items = {}

@app.get("/")
def root():
    return {"detail": "This is a simple app to keep track of items"}

@app.post("/items")
def add_item(item: Item) -> str:
    if items and item.id in items:
        raise HTTPException(status_code=400, detail="Item id already exist")
    items[item.id] = item
    return f"Item {item.id} has been successfully added"

@app.get("/items")
def get_all_items():
    return items

@app.delete("/items/{item_id}")
def delete_an_item(item_id: int):
    if 0 <= item_id < len(items):
        del items[item_id]
        return items
    raise HTTPException(status_code=404, detail=f"Item id {item_id} not found")

@app.put("/items/{item_id}", response_model=Item)
def update_an_item(item_id: int, item: Item):
    if item_id in items:
        delete_an_item(item.id)
        item_id = item.id
        items[item_id] = item
        return items[item_id]
    raise HTTPException(status_code=404, detail=f"Item id {item_id} not found")
