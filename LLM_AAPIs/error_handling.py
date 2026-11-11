
from google import genai
import os
import json

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

prompt = """
What is  Artificial Intelligence ?

Return data ONLY in JSON format.
Use these keys:
- topic
- difficulty
"""

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json"
    }
)
# 6. Try parsing
try:
    data = json.loads(response.text)

    print("JSON extracted successfully!")
    print("Topic:", data["topic"])
    print("Difficulty:", data["difficulty"])

except json.JSONDecodeError:

    print("Invalid JSON! Retrying...")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    # 7. Try parsing again
    try:
        data = json.loads(response.text)

        print("JSON extracted successfully on retry!")
        print("Topic:", data["topic"])
        print("Difficulty:", data["difficulty"])

    except json.JSONDecodeError: #jab response valid jsondecoderror
        print("Error: Gemini returned invalid JSON again.")           