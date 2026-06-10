import streamlit as st
import google.generativeai as genai
import json
import urllib.parse
from urllib.request import urlopen

st.set_page_config(page_title="Sales Scout AI Pro", layout="wide")
st.title("💼 Sales Scout AI Pro")

GOOGLE_API_KEY = "AIzaSyBqL7AJECi7lnkPQERmf2708JkAD1iwgE4"
GOOGLE_CX_ID = "f1b4f2c6ddd784b2e"

with st.sidebar:
    ai_api_key = st.text_input("Gemini API Key:", type="password")

target = st.text_input("Target Company:")

if st.button("🚀 Execute Scan"):
    if not ai_api_key or not target:
        st.error("Missing API Key or Target.")
    else:
        with st.spinner("Analyzing..."):
            try:
                # 1. Search
                query = f'"{target}" (site:linkedin.com OR site:facebook.com OR site:instagram.com)'
                url = f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote(query)}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX_ID}&num=3"
                with urlopen(url, timeout=10) as r:
                    search_context = r.read().decode()

                # 2. AI (Switched to 'gemini-pro' which is universally available)
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"Analyze: {search_context}. Provide a professional profile for {target}. Keep it short."
                response = model.generate_content(prompt)
                
                # 3. Output (No complex JSON parsing)
                st.markdown("### Intelligence Report")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
