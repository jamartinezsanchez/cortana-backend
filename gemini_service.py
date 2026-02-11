import google.generativeai as genai
import os
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def process_command(user_message: str, memories: list = []):
    memory_text = "\n".join([m["content"] for m in memories]) if memories else ""

    prompt = f"""
Eres un asistente inteligente tipo Cortana.
Responde SOLO en formato JSON válido.

Devuelve:
- intent (string)
- app (string o null)
- query (string o null)
- response (string para responder al usuario)

Memoria del usuario:
{memory_text}

Mensaje del usuario:
{user_message}
"""

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except:
        return {
            "intent": "UNKNOWN",
            "app": None,
            "query": None,
            "response": response.text
        }
