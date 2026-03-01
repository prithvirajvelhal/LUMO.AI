import requests
import json
import time
import os

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free"
]

SYSTEM_PROMPT = "You are Lumo, an AI that converts short ideas into high-quality AI image prompts."

def llama_prompt(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    for model_name in MODELS:
        for attempt in range(4):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=60
                )

                result = response.json()

                if "choices" in result:
                    return result

            except Exception as e:
                print("Error:", e)

            time.sleep(2)

    return {"error": "All models busy"}