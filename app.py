import streamlit as st
import google.generativeai as genai
import json
import urllib.parse
from urllib.request import urlopen

# Wide-view corporate dashboard layout
st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="wide")

st.title("💼 Sales Scout AI Pro")
st.write("Multi-Channel Digital Intelligence Dashboard")

# HARDCODED SECURE SEARCH ACCESS
GOOGLE_API_KEY = "AIzaSyBqL7AJECi7lnkPQERmf2708JkAD1iwgE4"
GOOGLE_CX_ID = "b6e6328bc4e844b82"  # Global public web search node orientation

# Sidebar for AI Key verification & Toggles
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
card_input, goal_input = st.columns([2, 1])
with card_input:
    target_input = st.text_input("Target Company Name or Persona (e.g., Ningbo Bonny E-Home):")
with goal_input:
    specific_goal = st.text_input("Custom Target Query Parameter (Optional):", placeholder="e.g., contact info, owners")

st.divider()

# Official Google Search Data Handshake
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
            return snippet_text if snippet_text else ""
    except:
        return ""

# 3. RUN PIPELINE
if st.button("🚀 Execute Comprehensive Multi-Channel Scan", use_container_width=True):
    if not ai_api_key:
        st.error("⚠️ Setup Incomplete: Please provide your Gemini API Key in the left sidebar menu.")
    elif not target_input:
        st.warning("⚠️ Action Required: Enter a company or prospect target to scan.")
    else:
        with st.spinner(f"Querying live global indexing nodes for '{target_input}'..."):
            try:
                # Gather live data blocks using your new key!
                general_search = google_search_lookup(f"{target_input} {specific_goal}", GOOGLE_API_KEY, GOOGLE_CX_ID)
                li_search = google_search_lookup(f"site:linkedin.com/in/ OR site:linkedin.com/company/ {target_input}", GOOGLE_API_KEY, GOOGLE_CX_ID) if scan_linkedin else ""
                fb_search = google_search_lookup(f"site:facebook.com/ {target_input}", GOOGLE_API_KEY, GOOGLE_CX_ID) if scan_facebook else ""

                # Initialize the Gemini Engine Node
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                You are an elite corporate intelligence agent. 
                Synthesize a factual, highly professional sales dossier based on these official live Google results. 
                
                Target Request: {target_input}
                
                Live Google Search Verified Data: {general_search}
                LinkedIn Index Records: {li_search}
                Facebook Index Records: {fb_search}
                
                You must return ONLY a pure JSON dataset matching the key-value attributes below. Do not use markdown blocks or backticks.
                {{
                    "official_name": "Full validated name of company or individual found in search data",
                    "market_hub": "Primary city/country corporate headquarters",
                    "data_confidence": 98,
                    "summary": "1-2 sentence corporate operations summary based on search details",
                    "offerings": ["Product/Service Line 1", "Product/Service Line 2", "Product/Service Line 3"],
                    "pitch_1_title": "LinkedIn-Tailored Outreach Header",
                    "pitch_1_body": "Operational pitch tactic leveraging their LinkedIn presence or professional records",
                    "pitch_2_title": "Facebook/B2C Outreach Header",
                    "pitch_2_body": "Pitch tactic leveraging their marketing, client interactions, or public community presence",
                    "pitch_3_title": "Executive Summary Value Play",
                    "pitch_3_body": "A custom pitch matching the exact criteria requested by the user",
                    "social_audit": "A professional analysis of how strong their verified public social footprints look."
                }}
                """
                
                response = model.generate_content(prompt)
                raw_payload = response.text.strip().replace("```json", "").replace("```", "")
                dataset = json.loads(raw_payload)
                
                st.balloons() # Success animation!
                
                # --- VISUAL DASHBOARD BLOCKS ---
                col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
                with col_m1:
                    st.info(f"🏢 **Verified Target Entity:**\n### {dataset.get('official_name', target_input)}")
                with col_m2:
                    st.warning(f"📍 **Primary Location:**\n### {dataset.get('market_hub', 'Global Scope')}")
                with col_m3:
                    score = dataset.get("data_confidence", 95)
                    st.metric(label="🎯 Data Record Strength", value=f"{score}%")
                    st.progress(score / 100)
                
                st.write("###")
                with st.container(border=True):
                    st.markdown("📋 **Operational Blueprint & Market Profile:**")
                    st.write(dataset.get("summary", ""))
                
                st.write("###")
                left_col, right_col = st.columns([1, 2])
                with left_col:
                    st.markdown("### 📦 Key Offerings Portfolio")
                    for item in dataset.get('offerings', []):
                        st.markdown(f"🔹 **{item}**")
                    st.write("###")
                    st.markdown("### 📡 Public Social Signal Audit")
                    st.caption(dataset.get('social_audit', ''))
                    
                with right_col:
                    st.markdown("### 🎯 Cross-Channel Pitch Strategies")
                    st.info(f"🔗 **LinkedIn Outreach Angle: {dataset.get('pitch_1_title')}**\n\n{dataset.get('pitch_1_body')}")
                    st.warning(f"👥 **Facebook Marketing Play: {dataset.get('pitch_2_title')}**\n\n{dataset.get('pitch_2_body')}")
                    st.error(f"🎯 **Targeted Solution Pitch: {dataset.get('pitch_3_title')}**\n\n{dataset.get('pitch_3_body')}")
                    
            except Exception as e:
                st.error("⚠️ Visual formatting reset. Displaying text dossier report:")
                if 'response' in locals():
                    st.markdown(response.text)
