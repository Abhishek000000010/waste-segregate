
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"Testing key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    response = model.generate_content("Say 'Key is working'")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
