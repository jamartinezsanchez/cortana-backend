from google import genai
import os

def ask_gemini(message: str):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=message
    )

    return response.text
