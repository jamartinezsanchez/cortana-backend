import os
from google import genai

def ask_gemini(message: str):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=message
    )

    # Forma segura de extraer el texto
    if response.candidates:
        return response.candidates[0].content.parts[0].text
    
    return "No se recibió respuesta de Gemini."
