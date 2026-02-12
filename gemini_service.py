import os
import google.generativeai as genai

# Inicializar API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(prompt: str) -> str:
    """Envía prompt a Gemini y devuelve la respuesta de texto"""
    try:
        response = genai.text.generate(
            model="models/text-bison-001",
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=512
        )
        return response.text
    except Exception as e:
        return f"Error al comunicarse con Gemini: {str(e)}"
