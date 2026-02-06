import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDQvjdrkbpOGNvFvwtuZpA7zY0jgEcnpYI"
genai.configure(api_key=GEMINI_API_KEY)

models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
for model_name in models:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("test")
        print(f"SUCCESS: {model_name}")
    except Exception as e:
        print(f"FAILED: {model_name}")
