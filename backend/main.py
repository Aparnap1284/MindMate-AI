import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("No API key found. Please set GEMINI_API_KEY environment variable.")

# Use gemini-1.5-flash (recommended) or gemini-1.5-pro-latest
MODEL_NAME = "gemini-1.5-flash"  # Faster and more available
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

def call_gemini_api(prompt):
    """Call Gemini API and return response"""
    try:
        # Use the working model
        MODEL_NAME = "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        return f"Sorry, I'm having trouble connecting right now. Error: {str(e)}"
# Test the API
if __name__ == "__main__":
    test_message = "Hello! I'm feeling a bit stressed today. Can you help?"
    print("Testing Gemini API with:", MODEL_NAME)
    
    response = call_gemini_api(test_message)
    print("User:", test_message)
    print("AI Response:", response)