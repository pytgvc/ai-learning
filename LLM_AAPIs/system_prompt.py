
from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_instruction = """
You are a helpful AI tutor
Answer in exactly 3 points
Use simple English
"""

prompt = "What is Artifical Intelligence ?"


response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
    config={
        "system_instruction": system_instruction
    }
)
#receive the response
answer=response.text
#print the response
print(response.text)
#woh attritubte jisme generated text ans hota=text 
# .=objectkeanadrkisiattritubekoacesskarna