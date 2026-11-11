from google import genai
import os
import json

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Write a prompt
prompt = "What is Artificial Intelligence?"


# System instruction
system_instruction = """
Return ONLY valid JSON.

Use these fixed keys:
- topic: Main topic of the question.
- difficulty: Beginner, Intermediate, or Advanced.
- Select the most appropriate level for the topic

If any information is missing, use null.
Do not make up information.
"""

# Send prompt to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
    config={
        "system_instruction": system_instruction,
        "response_mime_type": "application/json" #responsekisformatmaichahiye
    }
)

# Receive and print response
print(response.text)

# Convert JSON string into Python dictionary
data = json.loads(response.text)

# Access individual values
print("Topic:", data["topic"])
print("Difficulty:", data["difficulty"])
