from fastapi import FastAPI

app = FastAPI(title="Cortana Assistant API")

@app.get("/")
def home():
    return {"message": "Cortana está en línea 🤖"}
