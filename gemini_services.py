import os
from google import genai

def ask_gemini(message: str):
    try:
        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message,
        )

        return response.text

    except Exception as e:
        return str(e)
