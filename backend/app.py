from groq_llm import groq_prompt
from flask import Flask, request, jsonify
from flask_cors import CORS
from llama import llama_prompt

app = Flask(__name__)
CORS(app)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    idea = data.get("prompt", "")
    mode = data.get("mode", "beginner")
    fmt = data.get("format", "text")

    angle = data.get("angle", "auto")
    lighting = data.get("lighting", "auto")
    lens = data.get("lens", "auto")
    style = data.get("style", "auto")
    composition = data.get("composition", "auto")

    # ---------- PROMPT BUILD ----------
    if mode == "pro":

        if fmt == "json":
            instruction = f"""
Convert the idea into a structured AI image generation JSON.

Return ONLY valid JSON with this schema:

{{
  "scene": "...",
  "subjects": [
    {{
      "type": "...",
      "description": "...",
      "position": "..."
    }}
  ],
  "style": "...",
  "lighting": "...",
  "color_palette": ["...", "..."],
  "camera": {{
    "angle": "...",
    "lens": "...",
    "composition": "..."
  }},
  "mood": "..."
}}

Idea: {idea}

Angle: {angle}
Lighting: {lighting}
Lens: {lens}
Style: {style}
Composition: {composition}

If any parameter is 'auto', choose the best.
Output ONLY JSON.
"""
        else:
            instruction = f"""
Create a highly detailed cinematic AI image prompt.

Idea: {idea}

Angle: {angle}
Lighting: {lighting}
Lens: {lens}
Style: {style}
Composition: {composition}

If any parameter is 'auto', choose the most cinematic choice.

Write one long richly descriptive prompt in natural English.
No JSON. No lists. Only the final prompt.
"""

    else:
        instruction = f"""
Create a detailed cinematic AI image prompt from:
{idea}

Return concise English prompt.
"""

    # ---------- MODEL CALL ----------
    result = llama_prompt(instruction)

    if "choices" not in result:
        result = groq_prompt(instruction)

    # ---------- OUTPUT ----------
    if "choices" in result:
        text = result["choices"][0]["message"]["content"]

        # pretty JSON if requested
        if mode == "pro" and fmt == "json":
            import json as pyjson
            try:
                text = pyjson.dumps(pyjson.loads(text), indent=2)
            except:
                pass
    else:
        text = "Model busy — click Generate again"

    return jsonify({"output": text})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
