from fastapi import FastAPI, Depends
from supabase import create_client
from pydantic import BaseModel
import os
from auth import get_current_user
from uuid import UUID

app = FastAPI(title="Cortana Assistant API")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- MODELOS ----------
class NoteCreate(BaseModel):
    title: str
    content: str

# ---------- ROUTES ----------
@app.get("/")
def home():
    return {"message": "Cortana está en línea 🤖"}

@app.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email
    }

@app.post("/notes")
def create_note(
    note: NoteCreate,
    user=Depends(get_current_user)
):
    response = supabase.table("notes").insert({
        "title": note.title,
        "content": note.content,
        "user_id": user.id
    }).execute()

    return {
        "status": "ok",
        "note": response.data
    }

@app.get("/notes")
def get_notes(user=Depends(get_current_user)):
    response = supabase.table("notes") \
        .select("*") \
        .eq("user_id", user.id) \
        .execute()

    return response.data

@app.delete("/notes/{note_id}")
def delete_note(note_id: UUID, user=Depends(get_current_user)):
    supabase.table("notes") \
        .delete() \
        .eq("id", str(note_id)) \
        .eq("user_id", user.id) \
        .execute()

    return {"status": "deleted"}