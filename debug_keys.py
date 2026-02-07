
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
RAW_KEYS = os.getenv("GEMINI_API_KEY", "").split(",")
for i, key in enumerate(RAW_KEYS):
    k = key.strip()
    print(f"--- Key #{i+1} ({k[:5]}...) ---")
    try:
        genai.configure(api_key=k)
        models = genai.list_models()
        print("  Models found:")
        for m in models:
            print(f"    - {m.name}")
    except Exception as e:
        print(f"  FAIL: {e}")
