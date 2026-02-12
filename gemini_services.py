import os
import google.generativeai as genai

# Configurar API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Crear modelo
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt: str) -> str:
    """Envía prompt a Gemini y devuelve respuesta"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al comunicarse con Gemini: {str(e)}"
