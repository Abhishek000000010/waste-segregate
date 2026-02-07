
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
RAW_KEYS = os.getenv("GEMINI_API_KEY", "").split(",")
for i, key in enumerate(RAW_KEYS):
    k = key.strip()
    print(f"--- Key #{i+1} ---")
    try:
        genai.configure(api_key=k, transport='rest')
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content("test")
        print(f"OK: {response.text[:10]}")
    except Exception as e:
        print(f"FAIL: {str(e)}")
