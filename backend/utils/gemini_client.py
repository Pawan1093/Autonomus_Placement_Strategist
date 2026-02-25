from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_gemini(prompt: str) -> str:
    # We renamed to groq but kept function name so all other files still work!
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free and very powerful!
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}  # Forces JSON output!
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"