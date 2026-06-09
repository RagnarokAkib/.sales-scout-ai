import streamlit as st
import google.generativeai as genai
import json
import urllib.parse
from urllib.request import urlopen

st.set_page_config(page_title="Sales Scout AI Pro", layout="wide")
st.title("💼 Sales Scout AI Pro")

# YOUR PRODUCTION KEYS
GOOGLE_API_KEY = "AIzaSyBqL7AJECi7lnkPQERmf2708JkAD1iwgE4"
GOOGLE_CX_ID = "f1b4f2c6ddd784b2e"

# Sidebar
with st.sidebar:
    ai_api_key = st.text_input("Gemini API Key:", type="password")
    if ai_api_key: st.success("Core AI Engine Ready")

target_input = st.text_input("Target Company:")

def search(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote(query)}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX_ID}&num=3"
        with urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())
            return "\n".join([i['snippet'] for i in data.get("items", [])])
    except: return "No web results."

if st.button("🚀 Execute Scan"):
    if not ai_api_key: st.error("Add Gemini Key!")
    else:
        with st.spinner("Processing..."):
            genai.configure(api_key=ai_api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Simple, direct prompt
            context = search(target_input)
            prompt = f"Provide a JSON report for {target_input} using this info: {context}. Keys: official_name, summary, offerings, outreach_pitch."
            
            response = model.generate_content(prompt)
            # Clean response
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            
            try:
                data = json.loads(clean_text)
                st.subheader(data.get("official_name", "Target Profile"))
                st.write(data.get("summary", ""))
                st.write("**Offerings:**", data.get("offerings", ""))
                st.write("**Pitch:**", data.get("outreach_pitch", ""))
            except:
                st.write("Raw AI Output:")
                st.write(clean_text)
