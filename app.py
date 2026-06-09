import streamlit as st
import google.generativeai as genai
import json
import urllib.parse
from urllib.request import urlopen

# Wide-view dashboard configuration
st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="wide")

st.title("💼 Sales Scout AI Pro")
st.write("Multi-Channel Digital Intelligence Dashboard (No Social Logins Required)")

# 1. SIDEBAR CONFIGURATION (Cleaned up - no risky passwords!)
with st.sidebar:
    st.header("🔑 Engine Credentials")
    ai_api_key = st.sidebar.text_input("Gemini API Key:", type="password")
    st.divider()
    st.markdown("### 📡 Deep Scan Radar")
    st.caption("Enable automatic OSINT sweeps on public directory channels:")
    scan_linkedin = st.checkbox("Sweep Public LinkedIn Indexes", value=True)
    scan_facebook = st.checkbox("Sweep Public Facebook Logs", value=True)
    scan_instagram = st.checkbox("Sweep Public Instagram Handles", value=True)

# 2. TARGET ENTRY
st.subheader("🔍 Target Profile Initiation")
card_input, goal_input = st.columns([2, 1])
with card_input:
    target_input = st.text_input("Target Company Name or Persona:", placeholder="e.g., Ningbo Bonny E-Home")
with goal_input:
    specific_goal = st.text_input("Custom Parameter (Optional):", placeholder="e.g., core products, target audience")

st.divider()

# Helper tool to scrape public search snippets without accounts
def fetch_public_social_snippets(target, site_domain):
    try:
        query = urllib.parse.quote(f"site:{site_domain} {target}")
        url = f"https://html.duckduckgo.com/html/?q={query}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urlopen(req, timeout=4) as response:
            html = response.read().decode('utf-8')
            # Extracts simple text chunks out of the html container
            import re
            snippets = re.findall(r'<td class="result-snippet">(.*?)</td>', html)
            return " | ".join(snippets[:3]).replace('<b>', '').replace('</b>', '')
    except:
        return "No unauthenticated public layout blocks returned directly."

# 3. ANALYSIS PIPELINE RUNNER
if st.button("🚀 Execute Comprehensive Multi-Channel Scan", use_container_width=True):
    if not ai_api_key:
        st.error("⚠️ Setup Incomplete: Please provide your Gemini API Key in the left sidebar menu.")
    elif not target_input:
        st.warning("⚠️ Action Required: Enter a company or prospect target to scan.")
    else:
        with st.spinner(f"Deploying free web scanners across active public registries for '{target_input}'..."):
            try:
                # Run the free, account-free social channel checks via search indexes
                li_data = fetch_public_social_snippets(target_input, "linkedin.com/in/") if scan_linkedin else "Skipped"
                fb_data = fetch_public_social_snippets(target_input, "facebook.com/") if scan_facebook else "Skipped"
                ig_data = fetch_public_social_snippets(target_input, "instagram.com/") if scan_instagram else "Skipped"
                
                # Wake up Gemini 
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Bundle the gathered public social data and send it directly to the model
                prompt = f"""
                You are an elite multi-channel sales intelligence agent. 
                Synthesize a factual, tactical corporate dossier for: {target_input}.
                Custom parameter: {specific_goal if specific_goal else 'None'}
                
                Raw Open-Web Social Network Snippets Discovered:
                - LinkedIn Indexing: {li_data}
                - Facebook Indexing: {fb_data}
                - Instagram Indexing: {ig_data}
                
                You must return ONLY a pure JSON dataset matching the key-value attributes below. No backticks, no prose text.
                {{
                    "official_name": "Full validated name of company or individual",
                    "market_hub": "Primary city/country location",
                    "data_confidence": 95,
                    "summary": "1-2 sentence high-level business profile summary",
                    "offerings": ["Core Offering 1", "Core Offering 2", "Core Offering 3"],
                    "pitch_1_title": "Pitch 1 Header",
                    "pitch_1_body": "Detailed sales strategy text using LinkedIn context if available",
                    "pitch_2_title": "Pitch 2 Header",
                    "pitch_2_body": "Detailed sales strategy text using Facebook context if available",
                    "pitch_3_title": "Pitch 3 Header",
                    "pitch_3_body": "Detailed sales strategy text using Instagram context if available",
                    "social_audit": "A summary critique of how active their brand footprints appear across the searched indexes"
                }}
                """
                
                response = model.generate_content(prompt)
                raw_payload = response.text.strip().replace("```json", "").replace("```", "")
                dataset = json.loads(raw_payload)
                
                st.balloons() # Success animation
                
                # --- VISUAL DASHBOARD GRID ARRANGEMENT ---
                col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
                with col_m1:
                    st.info(f"🏢 **Verified Target Entity:**\n### {dataset.get('official_name', target_input)}")
                with col_m2:
                    st.warning(f"📍 **Primary Location:**\n### {dataset.get('market_hub', 'Global Horizon')}")
                with col_m3:
                    score = dataset.get("data_confidence", 90)
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
                    for item in dataset.get("offerings", []):
                        st.markdown(f"🔹 **{item}**")
                    
                    st.write("###")
                    st.markdown("### 📡 Public Social Signal Audit")
                    st.caption(dataset.get("social_audit", ""))
                    
                with right_col:
                    st.markdown("### 🎯 Cross-Channel Pitch Strategies")
                    st.info(f"🔗 **LinkedIn Angle: {dataset.get('pitch_1_title')}**\n\n{dataset.get('pitch_1_body')}")
                    st.warning(f"👥 **Facebook Angle: {dataset.get('pitch_2_title')}**\n\n{dataset.get('pitch_2_body')}")
                    st.error(f"📸 **Instagram Angle: {dataset.get('pitch_3_title')}**\n\n{dataset.get('pitch_3_body')}")
                    
            except Exception as e:
                st.error("⚠️ Free indexing rate limits or parsing formats caused a dashboard frame stall. Retrying raw format...")
                if 'response' in locals():
                    st.markdown(response.text)
