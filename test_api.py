import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}" if API_KEY else "No API key found")

# Test the API key with a simple list models request
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ API key is valid!")
        models = response.json()
        print("Available models:", [model['name'] for model in models.get('models', [])])
    else:
        print("❌ API key validation failed")
        print("Response:", response.text)
except Exception as e:
    print(f"Error: {e}")