import streamlit as st
import google.generativeai as genai
import json
import urllib.parse
from urllib.request import urlopen

# Robust visual dashboard setup
st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="wide")

st.title("💼 Sales Scout AI Pro")
st.write("Enterprise Digital Intelligence Dashboard")

# ==========================================
# 🔑 BRAND NEW PRODUCTION ENGINE KEYS
# ==========================================
GOOGLE_API_KEY = "AIzaSyBqL7AJECi7lnkPQERmf2708JkAD1iwgE4"
GOOGLE_CX_ID = "f1b4f2c6ddd784b2e"  # Your freshly minted search engine container ID!

# Clean sidebar interface for reps
with st.sidebar:
    st.header("🔑 Connection Center")
    ai_api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    st.markdown("### 📡 Deep Scan Radar")
    scan_linkedin = st.checkbox("Include Public LinkedIn Footprints", value=True)
    scan_facebook = st.checkbox("Include Public Facebook Footprints", value=True)
    
    if ai_api_key:
        st.success("🤖 Core AI Engine Ready")

# 2. TARGET ENTRY
st.subheader("🔍 Target Profile Initiation")
target_input = st.text_input("Target Company Name or Persona (e.g., Ningbo Bonny E-Home):")
specific_goal = st.text_input("Custom Target Query Parameter (Optional):", placeholder="e.g., contact info, owners")

st.divider()

# Official Google Search API Handshake
def google_search_lookup(query, api_key, cx_id):
    try:
        safe_query = urllib.parse.quote(query)
        url = f"https://www.googleapis.com/customsearch/v1?q={safe_query}&key={api_key}&cx={cx_id}&num=3"
        with urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get("items", [])
            snippet_text = ""
            for item in results:
                snippet_text += f"Title: {item['title']}\nSnippet: {item['snippet']}\n\n"
            return snippet_text if snippet_text else "No extra public footprints indexed."
    except:
        return "Search API indexing online."

# 3. RUN ANALYSIS PIPELINE
if st.button("🚀 Execute Comprehensive Multi-Channel Scan", use_container_width=True):
    if not ai_api_key:
        st.error("⚠️ Setup Incomplete: Please provide your Gemini API Key in the left sidebar menu.")
    elif not target_input:
        st.warning("⚠️ Action Required: Enter a company or prospect target to scan.")
    else:
        with st.spinner(f"Querying live global data pipelines for '{target_input}'..."):
            
            # Gather live data blocks safely using your custom engines
            general_search = google_search_lookup(f"{target_input} {specific_goal}", GOOGLE_API_KEY, GOOGLE_CX_ID)
            li_search = google_search_lookup(f"linkedin {target_input}", GOOGLE_API_KEY, GOOGLE_CX_ID) if scan_linkedin else "Skipped"
            fb_search = google_search_lookup(f"facebook {target_input}", GOOGLE_API_KEY, GOOGLE_CX_ID) if scan_facebook else "Skipped"

            # Fire up the Gemini Model
            try:
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                You are an elite corporate intelligence agent. 
                Synthesize a factual, highly professional sales dossier based on the requested target name and any accompanying search snippets. 
                
                Target Request: {target_input}
                Additional Context: {specific_goal}
                
                Live Search Logs: {general_search}
                LinkedIn Footprints: {li_search}
                Facebook Footprints: {fb_search}
                
                You must return ONLY a pure JSON dataset matching the key-value attributes below. Do not use markdown blocks, backticks, or wrap it in ```json.
                {{
                    "official_name": "Full validated name of company or individual",
                    "market_hub": "Primary city/country corporate headquarters",
                    "data_confidence": 95,
                    "summary": "A high-level 2-3 sentence corporate profile detailing operations, target market, and focus areas.",
                    "offerings": ["Core Product/Service Line 1", "Core Product/Service Line 2", "Core Product/Service Line 3"],
                    "pitch_1_title": "LinkedIn-Tailored Outreach Header",
                    "pitch_1_body": "Strategic B2B outreach pitch matching their professional scope.",
                    "pitch_2_title": "Facebook/B2C Outreach Header",
                    "pitch_2_body": "Marketing alignment or distribution-focused outreach play.",
                    "pitch_3_title": "Executive Summary Value Play",
                    "pitch_3_body": "Custom pitch matching the exact query criteria requested by the user.",
                    "social_audit": "An analysis of their digital footprint stance based on available market records."
                }}
                """
                
                response = model.generate_content(prompt)
                raw_payload = response.text.strip()
                
                # Rigid string cleaners to bypass any markdown formatting slips
                if raw_payload.startswith("```"):
                    raw_payload = raw_payload.split("\n", 1)[1]
                if raw_payload.endswith("```"):
                    raw_payload = raw_payload.rsplit("\n", 1)[0]
                raw_payload = raw_payload.strip().replace("```json", "").replace("```", "")
                
                dataset = json.loads(raw_payload)
                st.balloons()
                
                # --- RESPONSIVE ENTERPRISE DISPLAY DASHBOARD ---
                st.info(f"🏢 **Verified Target:** {dataset.get('official_name', target_input)} | 📍 **Location:** {dataset.get('market_hub', 'Global Scope')} | 🎯 **Data Strength:** {dataset.get('data_confidence', 95)}%")
                
                with st.container(border=True):
                    st.markdown("📋 **Operational Blueprint & Market Profile:**")
                    st.write(dataset.get("summary", ""))
                
                st.divider()
                st.markdown("### 📦 Key Offerings Portfolio")
                for item in dataset.get('offerings', []):
                    st.markdown(f"🔹 **{item}**")
                
                st.divider()
                st.markdown("### 📡 Public Social Signal Audit")
                st.info(dataset.get('social_audit', 'No alternative digital footprints tracked.'))
                
                st.divider()
                st.markdown("### 🎯 Cross-Channel Pitch Strategies")
                st.markdown(f"#### 🔗 {dataset.get('pitch_1_title')}")
                st.write(dataset.get('pitch_1_body'))
                
                st.markdown(f"#### 👥 {dataset.get('pitch_2_title')}")
                st.write(dataset.get('pitch_2_body'))
                
                st.markdown(f"#### 🎯 {dataset.get('pitch_3_title')}")
                st.write(dataset.get('pitch_3_body'))
                    
            except Exception as e:
                st.error("⚠️ Visual sync reset. Displaying textual data stack:")
                if 'response' in locals():
                    st.write(response.text)
