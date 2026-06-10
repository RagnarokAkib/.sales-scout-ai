import streamlit as st
import google.generativeai as genai
import json
import urllib.parse
from urllib.request import urlopen

# Wide-view corporate dashboard layout
st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="wide")

st.title("💼 Sales Scout AI Pro")
st.write("Enterprise Digital Intelligence Dashboard")

# PRODUCTION KEYS
GOOGLE_API_KEY = "AIzaSyBqL7AJECi7lnkPQERmf2708JkAD1iwgE4"
GOOGLE_CX_ID = "f1b4f2c6ddd784b2e"

# Sidebar with toggles
with st.sidebar:
    st.header("🔑 Connection Center")
    ai_api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    st.markdown("### 📡 Deep Scan Radar")
    scan_linkedin = st.checkbox("Include LinkedIn", value=True)
    scan_facebook = st.checkbox("Include Facebook/Instagram", value=True)
    
    if ai_api_key:
        st.success("🤖 Core AI Engine Ready")

# TARGET ENTRY
card_input, goal_input = st.columns([2, 1])
with card_input:
    target_input = st.text_input("Target Company Name:")
with goal_input:
    specific_goal = st.text_input("Goal (e.g. contact info):", placeholder="Optional")

st.divider()

# Stable Search Function
def get_stable_data(target, linkedin, facebook):
    platforms = []
    if linkedin: platforms.append("site:linkedin.com")
    if facebook: platforms.append("site:facebook.com OR site:instagram.com")
    platform_query = " OR ".join(platforms)
    
    # Combined Query to prevent quota exhaustion
    query = f'"{target}" {platform_query} products contact'
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote(query)}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX_ID}&num=5"
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return "\n".join([f"{i['title']}: {i['snippet']}" for i in data.get("items", [])])
    except:
        return "Search data currently unavailable."

# 3. RUN PIPELINE
if st.button("🚀 Execute Comprehensive Scan", use_container_width=True):
    if not ai_api_key:
        st.error("Please enter Gemini API Key.")
    elif not target_input:
        st.warning("Please enter a company name.")
    else:
        with st.spinner("Processing intelligence scan..."):
            context = get_stable_data(target_input, scan_linkedin, scan_facebook)
            
            genai.configure(api_key=ai_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""You are a professional sales researcher. Analyze this info for {target_input}: {context}.
            Return ONLY a valid JSON object with these keys: 
            "official_name", "market_hub", "summary", "offerings" (as a list), 
            "pitch_1_title", "pitch_1_body", "pitch_2_title", "pitch_2_body", "social_audit".
            Do not use markdown formatting."""
            
            response = model.generate_content(prompt)
            try:
                data = json.loads(response.text.replace("```json", "").replace("```", "").strip())
                
                # Visual Dashboard
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.info(f"🏢 **Entity:** {data.get('official_name', target_input)}")
                col2.warning(f"📍 **Hub:** {data.get('market_hub', 'N/A')}")
                
                with st.container(border=True):
                    st.markdown("📋 **Summary:**")
                    st.write(data.get("summary", ""))
                
                left, right = st.columns([1, 2])
                with left:
                    st.markdown("### 📦 Offerings")
                    for item in data.get('offerings', []): st.markdown(f"🔹 {item}")
                with right:
                    st.markdown("### 🎯 Outreach Strategy")
                    st.info(f"**{data.get('pitch_1_title')}**\n{data.get('pitch_1_body')}")
                    st.warning(f"**{data.get('pitch_2_title')}**\n{data.get('pitch_2_body')}")
                
                st.markdown("### 📡 Social Audit")
                st.write(data.get("social_audit", ""))
                
            except:
                st.error("Error formatting data. Raw Output:")
                st.write(response.text)
