from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"detail": "This is a simple app to keep track of items"}

