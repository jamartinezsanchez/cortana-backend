import os
from google import genai

# Crear cliente con API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(message: str) -> str:
    response = client.models.generate_content(
        model="gemini-1.0-pro",  # ✅ modelo estable compatible
        contents=message
    )
    return response.text
