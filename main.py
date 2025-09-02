from fastapi import FastAPI, HTTPException

app = FastAPI()

items = []

@app.get("/")
def root():
    return {"detail": "This is a simple app to keep track of items"}

@app.post("/items")
def add_item(item: str) -> str:
    items.append(item)
    return f"Item {item} has been successfully added"

@app.get("/items")
def get_all_items():
    return items

@app.delete("/items/{item_id}")
def delete_an_item(item_id: int):
    if 0 <= item_id < len(items):
        del items[item_id]
        return items
    raise HTTPException(status_code=404, detail=f"Item id {item_id} not found")

@app.put("items/{item_id}")
def update_an_item(item_id: int, item: str):
    if 0 <= item_id < len(items):
        items[item_id] = item
        return items
    raise HTTPException(status_code=404, detail=f"Item id {item_id} not found")
