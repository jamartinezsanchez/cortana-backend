from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from supabase import create_client
from pydantic import BaseModel
from uuid import UUID
import os
from auth import get_current_user
from gemini_services import ask_gemini

# ------------------ APP ------------------
app = FastAPI(title="Cortana Assistant API")

# CORS para frontend local y backend deploy
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Frontend local
        "https://cortana-backend-3k7q.onrender.com"  # Render deploy
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ SUPABASE ------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------ MODELOS ------------------
class NoteCreate(BaseModel):
    title: str
    content: str

class MemoryCreate(BaseModel):
    content: str
    type: str  # preference | reminder | fact | context

class ChatRequest(BaseModel):
    message: str

# ------------------ ROUTES ------------------
@app.get("/")
def home():
    return {"message": "Cortana está en línea 🤖"}

@app.get("/me")
def me(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email}

# ---------- NOTES ----------
@app.post("/notes")
def create_note(note: NoteCreate, user=Depends(get_current_user)):
    response = supabase.table("notes").insert({
        "title": note.title,
        "content": note.content,
        "user_id": user.id
    }).execute()
    return {"status": "ok", "note": response.data}

@app.get("/notes")
def get_notes(user=Depends(get_current_user)):
    response = supabase.table("notes").select("*").eq("user_id", user.id).execute()
    return response.data

@app.put("/notes/{note_id}")
def update_note(note_id: str, note: NoteCreate, user=Depends(get_current_user)):
    response = supabase.table("notes").update({
        "title": note.title,
        "content": note.content
    }).eq("id", note_id).eq("user_id", user.id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Nota no encontrada o no autorizada")
    return {"status": "updated", "note": response.data}

@app.delete("/notes/{note_id}")
def delete_note(note_id: UUID, user=Depends(get_current_user)):
    supabase.table("notes").delete().eq("id", str(note_id)).eq("user_id", user.id).execute()
    return {"status": "deleted"}

# ---------- MEMORIES ----------
@app.post("/memories")
def create_memory(memory: MemoryCreate, user=Depends(get_current_user)):
    response = supabase.table("memories").insert({
        "content": memory.content,
        "type": memory.type,
        "user_id": user.id
    }).execute()
    return {"status": "ok", "memory": response.data}

@app.get("/memories")
def get_memories(user=Depends(get_current_user)):
    response = supabase.table("memories").select("*").eq("user_id", user.id).execute()
    return response.data

# ---------- CHAT (Gemini) ----------
@app.post("/chat")
def chat(data: ChatRequest, user=Depends(get_current_user)):
    respuesta = ask_gemini(data.message)
    return {"response": respuesta}
