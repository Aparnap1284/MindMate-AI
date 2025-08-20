import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Please set it in your .env file")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="MindMate AI",
    page_icon="🧠",
    layout="centered"
)

# App title and description
st.title("🧠 MindMate AI")
st.markdown("### Your friendly mental wellness companion")
st.write("Talk to MindMate about anything that's on your mind - no judgments, just support.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def call_gemini_api(prompt):
    """Call Gemini API and return response"""
    try:
        # Use the latest available model
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
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            return "I've reached my usage limit for now. Please try again later or check your Google Cloud billing settings."
        else:
            return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
# Chat input
if prompt := st.chat_input("How are you feeling today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Call Gemini API
        full_response = call_gemini_api(prompt)
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with additional info
with st.sidebar:
    st.header("About MindMate")
    st.info("""
    MindMate is your confidential AI companion for mental wellness.
    
    Features coming soon:
    - Mood tracking
    - Daily challenges
    - Wellness games
    - Progress dashboard
    """)
    
    # Debug info (optional - remove in production)
    st.divider()
    st.caption("Debug Info")
    st.code(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}" if API_KEY else "No API key found")