import requests
import os
import json

GROQ_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

def groq_prompt(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are Lumo, an AI that converts short ideas into high-quality AI image prompts."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        r = requests.post(URL, headers=headers, json=body, timeout=30)
        data = r.json()
        if "choices" in data:
            return data
    except:
        pass

    return {"error": "groq_failed"}