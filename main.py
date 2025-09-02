from fastapi import FastAPI

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

