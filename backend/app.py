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

    # PROMPBUIL
    if mode == "pro":

        if fmt == "json":
            instruction = f"""
Convert the idea into a highly detailed structured AI image generation JSON.

Return ONLY valid JSON with this schema:

{{
  "scene": {{
    "title": "...",
    "environment": {{
      "type": "...",
      "location_style": "...",
      "architecture": "...",
      "time_of_day": "...",
      "weather": "...",
      "atmosphere": "...",
      "background_details": [
        "...",
        "..."
      ]
    }},
    "mood": [
      "...",
      "..."
    ],
    "visual_theme": "...",
    "cinematic_style": "..."
  }},

  "subjects": [
    {{
      "type": "...",
      "role": "...",

      "description": {{
        "gender": "...",
        "age": "...",
        "ethnicity": "...",
        "facial_features": "...",
        "expression": "...",
        "pose": "...",
        "body_language": "...",

        "hair": {{
          "style": "...",
          "details": "..."
        }},

        "skin": {{
          "texture": "...",
          "detail_level": "..."
        }}
      }},

      "outfit": {{
        "type": "...",
        "style": "...",

        "primary_colors": [
          "...",
          "..."
        ],

        "materials": [
          "...",
          "..."
        ],

        "details": [
          "...",
          "..."
        ]
      }},

      "accessories": [
        "...",
        "..."
      ],

      "positioning": {{
        "placement": "...",
        "interaction": "...",
        "orientation": "..."
      }}
    }}
  ],

  "cinematography": {{
    "camera": {{
      "body_type": "full_frame_dslr",

      "angle": "...",

      "lens": {{
        "type": "...",
        "focal_length": "...",
        "depth_of_field": "..."
      }},

      "focus": {{
        "primary_subject": "...",
        "sharpness": "..."
      }},

      "movement_style": "..."
    }},

    "composition": {{
      "framing": "...",
      "subject_balance": "...",
      "perspective": "...",
      "negative_space": "...",
      "visual_flow": "..."
    }}
  }},

  "lighting": {{
    "style": "...",
    "source": "...",
    "direction": "...",
    "shadow_style": "...",
    "highlight_behavior": "...",
    "volumetrics": "...",
    "color_temperature": "...",
    "mood_effect": "..."
  }},

  "color_palette": {{
    "primary": [
      "...",
      "..."
    ],

    "secondary": [
      "...",
      "..."
    ],

    "accent": [
      "...",
      "..."
    ]
  }},

  "rendering": {{
    "style": "...",
    "realism_level": "...",
    "texture_quality": "...",
    "detail_level": "...",
    "dynamic_range": "...",
    "color_grading": "...",

    "post_processing": [
      "...",
      "..."
    ]
  }},

  "quality_control": {{
    "resolution": "...",
    "anatomy_accuracy": "...",
    "hand_quality": "...",
    "face_quality": "...",

    "artifact_prevention": [
      "...",
      "..."
    ]
  }},

  "negative_prompt": {{
    "anatomy_errors": [
      "...",
      "..."
    ],

    "render_errors": [
      "...",
      "..."
    ],

    "style_issues": [
      "...",
      "..."
    ]
  }}
}}

Idea: {idea}

Angle: {angle}
Lighting: {lighting}
Lens: {lens}
Style: {style}
Composition: {composition}

If any parameter is 'auto', choose the best cinematic option.

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

    # MODLCALL
    result = llama_prompt(instruction)

    if "choices" not in result:
        result = groq_prompt(instruction)

    # OP
    if "choices" in result:
        text = result["choices"][0]["message"]["content"]

        # JSON
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
