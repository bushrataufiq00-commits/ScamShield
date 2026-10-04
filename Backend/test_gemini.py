from google import genai
import os


api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain in one sentence what a phishing message is."
)


print(response.text)