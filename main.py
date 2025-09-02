from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str

#--------------------------------------Database Setup------------------------------------------

def get_connection():
    return sqlite3.connect("Item_Database.db")

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS item_list (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

def save_to_sqlite(item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR REPLACE INTO item_list (id, name, description) VALUES (?, ?, ?)", (item.id, item.name, item.description))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=404, detail=e)

def update_in_sqlite(item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE item_list SET name = ?, description = ? WHERE id = ?", (item.name, item.description, item.id))
    conn.commit()
    conn.close()

def get_items_from_sqlite():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM item_list")
    rows = cursor.fetchall()
    conn.close()
    return [Item(id=row[0], name=row[1], description=row[2]) for row in rows]

def delete_item_from_sqlite(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM item_list WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def exists_in_sqlite(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM item_list")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        if item_id == row[0]:
            return True
    return False



#------------------------------------REST API Setup---------------------------------------------

@app.get("/")
def root():
    return {"detail": "This is a simple app to keep track of items"}

@app.post("/items")
def add_item(item: Item) -> str:
    if exists_in_sqlite(item.id):
        raise HTTPException(status_code=400, detail="Item id already exist in db")
    save_to_sqlite(item)
    return f"Item {item.id} has been successfully added"

@app.get("/items")
def get_all_items():
    return get_items_from_sqlite()

@app.delete("/items/{item_id}")
def delete_an_item(item_id: int):
    if exists_in_sqlite(item_id):
        delete_item_from_sqlite(item_id)
        return f"Item with item id {item_id} has been deleted"
    raise HTTPException(status_code=404, detail=f"Item id {item_id} not found")

@app.put("/items/{item_id}", response_model=Item)
def update_an_item(item_id: int, item: Item):
    if exists_in_sqlite(item_id):
        update_in_sqlite(item)
        return item
    raise HTTPException(status_code=404, detail=f"Item id {item_id} not found")
