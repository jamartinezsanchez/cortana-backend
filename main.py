from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI(title="Cortana Assistant API")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"message": "Cortana está en línea 🤖"}

@app.post("/notes")
def create_note(title: str, content: str):
    response = supabase.table("notes").insert({
        "title": title,
        "content": content
    }).execute()

    return {
        "status": "ok",
        "note": response.data
    }
