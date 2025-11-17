import os
from groq import Groq
from datetime import datetime

def get_client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("❌ GROQ_API_KEY is missing! Set it in .env")
    return Groq(api_key=key)

def generate_diary_text(plant_name: str, disease: str) -> str:
    client = get_client()

    timestamp = datetime.now().strftime("%d-%m-%Y, %A, %I:%M %p")

    prompt = f"""
You are {plant_name}. Speak like a friendly plant writing a diary.
Disease = {disease}
Time = {timestamp}

Rules:
- Simple Hinglish
- 2–3 lines
- If healthy → thank farmer
- If disease → give 1–2 cure tips
- If unknown → ask farmer to check leaves properly
"""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content
