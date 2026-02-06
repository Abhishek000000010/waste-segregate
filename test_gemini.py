import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDQvjdrkbpOGNvFvwtuZpA7zY0jgEcnpYI"
genai.configure(api_key=GEMINI_API_KEY)

print("Listing models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")

model = genai.GenerativeModel('gemini-1.5-flash')
try:
    response = model.generate_content("Say hello")
    print(f"Flash Response: {response.text}")
except Exception as e:
    print(f"Flash Error: {e}")
