from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def preguntar_gemini(mensaje):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=mensaje
        )

        return response.text

    except Exception as e:
        return f"Error al comunicarse con Gemini: {str(e)}"
