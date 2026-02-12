import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_gemini(message: str):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=message
        )

        return response.text

    except Exception as e:
        return f"Error al comunicarse con Gemini: {str(e)}"
