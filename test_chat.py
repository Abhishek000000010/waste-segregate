import requests

url = "http://127.0.0.1:8000/chat"
data = {"query": "Tell me about recycling plastic"}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"FULL RESPONSE: {response.text}")
except Exception as e:
    print(f"Error: {e}")
