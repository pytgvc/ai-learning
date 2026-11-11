

from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#write a que(prompt)
prompt = "What is Artifical Intelligence ?"


#send the prompt to the gemini model
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)
#recrive the response
print(response.text)