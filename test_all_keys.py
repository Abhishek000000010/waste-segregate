
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
RAW_KEYS = os.getenv("GEMINI_API_KEY", "").split(",")
GEMINI_KEYS = [k.strip() for k in RAW_KEYS if k.strip()]

for i, key in enumerate(GEMINI_KEYS):
    print(f"Testing Key #{i+1}: {key[:10]}...")
    try:
        genai.configure(api_key=key, transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hi")
        print(f"  ✅ Key #{i+1} is WORKING. Response: {response.text[:20]}")
    except Exception as e:
        print(f"  ❌ Key #{i+1} FAILED: {e}")
