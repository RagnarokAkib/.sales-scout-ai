import streamlit as st
import google.generativeai as genai
import json
import urllib.parse
from urllib.request import urlopen

# Setup page
st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="wide")
st.title("💼 Sales Scout AI Pro")

# Configuration
GOOGLE_API_KEY = "AIzaSyBqL7AJECi7lnkPQERmf2708JkAD1iwgE4"
GOOGLE_CX_ID = "f1b4f2c6ddd784b2e"

# Sidebar
with st.sidebar:
    st.header("🔑 Connection Center")
    ai_api_key = st.text_input("Gemini API Key:", type="password")
    scan_linkedin = st.checkbox("Include LinkedIn", value=True)
    scan_facebook = st.checkbox("Include Facebook/Instagram", value=True)

# Input
target_input = st.text_input("Target Company Name:")

def get_stable_search(target, linkedin, facebook):
    platforms = []
    if linkedin: platforms.append("site:linkedin.com")
    if facebook: platforms.append("site:facebook.com OR site:instagram.com")
    query = f'"{target}" {" OR ".join(platforms)} products contact'
    
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote(query)}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX_ID}&num=3"
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return "\n".join([f"{i['title']}: {i['snippet']}" for i in data.get("items", [])])
    except Exception as e:
        return f"Search error: {str(e)}"

if st.button("🚀 Execute Comprehensive Scan"):
    if not ai_api_key or not target_input:
        st.error("Please provide both Gemini API Key and Target Company.")
    else:
        with st.spinner("Analyzing intelligence..."):
            try:
                # Configure Model
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Fetch Data
                context = get_stable_search(target_input, scan_linkedin, scan_facebook)
                
                # Request
                prompt = f"Analyze: {context}. Provide JSON with keys: official_name, market_hub, summary, offerings (list), pitch_1_title, pitch_1_body, pitch_2_title, pitch_2_body, social_audit."
                response = model.generate_content(prompt)
                
                # Parse
                raw_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_text)
                
                # Display
                st.info(f"🏢 **Entity:** {data.get('official_name')}")
                st.write(f"**Summary:** {data.get('summary')}")
                
                cols = st.columns(2)
                cols[0].write(f"**Offerings:** {', '.join(data.get('offerings', []))}")
                cols[1].write(f"**Social Audit:** {data.get('social_audit')}")
                
                st.divider()
                st.write(f"### {data.get('pitch_1_title')}")
                st.write(data.get('pitch_1_body'))
                
            except Exception as e:
                st.error("Failed to parse JSON structure. Raw output below:")
                if 'response' in locals(): st.write(response.text)
                else: st.write(str(e))
