import streamlit as st
import google.generativeai as genai
import requests

# Load API Key and Search Engine ID from Streamlit Secrets
GOOGLE_SEARCH_API_KEY = st.secrets["GOOGLE_SEARCH_API_KEY"]
SEARCH_ENGINE_ID = st.secrets["SEARCH_ENGINE_ID"]

# Initialize Gemini AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
Gemini = genai.GenerativeModel(model_name="gemini-1.5-flash")

# System Prompt
sys_prompt = """You are an AI that provides code reviews and real-time answers.
For coding:
- Review for correctness, efficiency, readability, and security.
- Suggest improvements and best practices.

For real-time information:
- Use Google Search API when necessary.
- Summarize the latest and most relevant information.
"""

# Streamlit UI
st.title("NOVA-AI")

# User Input
user_input = st.text_area(label="", placeholder="Ask Me Something...")

# Function to fetch real-time data from Google Search API
def fetch_real_time_data(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("items", [])
        if results:
            return results[0]["snippet"]  # Return the top search result snippet
        else:
            return "No relevant real-time data found."
    return "Error fetching real-time information."

# Submit Button
if st.button("Submit"):
    if user_input.strip():
        # Check if the question requires real-time data
        real_time_keywords = ["news", "weather", "stock", "latest", "live", "real-time"]
        if any(keyword in user_input.lower() for keyword in real_time_keywords):
            real_time_response = fetch_real_time_data(user_input)
            st.subheader("Real-Time Data:")
            st.write(real_time_response)
        else:
            response = Gemini.generate_content(user_input)
            if response and response.text:
                st.subheader("AI Response:")
                st.write(response.text)
            else:
                st.warning("No response generated. Please try again.")
    else:
        st.error("Please enter a question or code before submitting.")

