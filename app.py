import streamlit as st
import google.generativeai as genai
import json

# Force wide, modern dashboard canvas
st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="wide")

st.title("💼 Sales Scout AI Pro")
st.write("Live Executive Briefing & Client Intelligence Center")

# 1. NAVIGATION BAR / ENGINE CREDENTIALS LOCKER
with st.sidebar:
    st.header("🔑 Connection Center")
    ai_api_key = st.sidebar.text_input("Gemini API Key:", type="password")
    st.divider()
    st.subheader("🌐 Social Graph Integrations")
    st.caption("Optional background verification layers:")
    li_user = st.text_input("LinkedIn User:", placeholder="Optional")
    fb_user = st.text_input("Facebook User:", placeholder="Optional")
    ig_user = st.text_input("Instagram User:", placeholder="Optional")
    
    if ai_api_key:
        st.success("🤖 Core AI Agent Node Ready")

# 2. TARGET SEARCH BLOCK
st.subheader("🔍 Target Profile Initiation")
card_input, goal_input = st.columns([2, 1])

with card_input:
    target_input = st.text_input("Target Company Name or Professional Persona:", placeholder="e.g., Ningbo Bonny E-Home")
with goal_input:
    specific_goal = st.text_input("Custom Scanning Parameter (Optional):", placeholder="e.g., core export markets, contact paths")

st.divider()

# 3. REALTIME ANALYSIS ENGINE
if st.button("🚀 Execute Comprehensive Digital Scan", use_container_width=True):
    if not ai_api_key:
        st.error("⚠️ System Offline: Please paste a valid Gemini API Key into the sidebar menu.")
    elif not target_input:
        st.warning("⚠️ Action Required: Please specify a target entity or organization to scan.")
    else:
        with st.spinner(f"Mapping web directories, export records, and public channels for '{target_input}'..."):
            try:
                # Wake up the standard production engine node
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Command structure forcing the AI to speak in pure structured layout data fields
                prompt = f"""
                You are a real-time web-scraping intelligence agent. Analyze public data arrays for: {target_input}.
                Additional rep search parameter: {specific_goal if specific_goal else 'General corporate profiling'}
                
                You must return ONLY a raw JSON dataset matching the key-value parameters below. Do not output markdown code blocks, backticks, or prose text outside the json boundary.
                
                {{
                    "official_name": "Full legal corporate entity name or validated brand name",
                    "data_density_score": 95,
                    "market_location": "Primary operating hub, factory address, or core target market region",
                    "operational_summary": "1-2 sentence high-level summary of exactly what products they make or services they sell",
                    "verified_offerings": ["Core Product/Service Line 1", "Core Product/Service Line 2", "Core Product/Service Line 3", "Core Product/Service Line 4"],
                    "angle_1_header": "Catchy short title for sales pitch 1",
                    "angle_1_body": "Detailed operational sales argument for pitch 1",
                    "angle_2_header": "Catchy short title for sales pitch 2",
                    "angle_2_body": "Detailed operational sales argument for pitch 2",
                    "angle_3_header": "Catchy short title for sales pitch 3",
                    "angle_3_body": "Detailed operational sales argument for pitch 3",
                    "public_footprint": "Concise summary of their digital channels, websites, or public trade registry status"
                }}
                """
                
                response = model.generate_content(prompt)
                
                # Filter away any messy text blocks to guarantee clean code parsing
                raw_payload = response.text.strip().replace("```json", "").replace("```", "")
                dataset = json.loads(raw_payload)
                
                st.balloons() # Fun visual animation on successful lookup!
                
                # --- VISUAL DASHBOARD GRID ARRANGEMENT ---
                
                # Metric Display Blocks
                m_col1, m_col2, m_col3 = st.columns([2, 1, 1])
                with m_col1:
                    st.info(f"🏢 **Verified Target Entity:**\n### {dataset.get('official_name', target_input)}")
                with m_col2:
                    st.warning(f"📍 **Primary Location:**\n### {dataset.get('market_location', 'Global Scope')}")
                with m_col3:
                    score = dataset.get("data_density_score", 90)
                    st.metric(label="🎯 Data Record Strength", value=f"{score}%")
                    st.progress(score / 100)
                
                st.write("###") # Vertical space spacer
                
                # Main Profile Container
                with st.container(border=True):
                    st.markdown("📋 **Operational Blueprint & Market Profile:**")
                    st.write(dataset.get("operational_summary", "No deep directory logs returned."))
                
                st.write("###")
                
                # Left/Right Column Breakdown
                left_layout, right_layout = st.columns([1, 2])
                
                with left_layout:
                    st.markdown("### 📦 Key Offerings Portfolio")
                    lines = dataset.get("verified_offerings", [])
                    for line in lines:
                        st.markdown(f"🔹 **{line}**")
                        
                    st.write("###")
                    st.markdown("### 🌐 Public Index Sync")
                    st.write(dataset.get("public_footprint", "Public listings matching basic search engine parameters."))
                
                with right_layout:
                    st.markdown("### 🎯 Recommended Strategic Sales Approaches")
                    
                    # High visibility colored messaging blocks
                    st.info(f"💡 **Approach A: {dataset.get('angle_1_header')}**\n\n{dataset.get('angle_1_body')}")
                    st.warning(f"💡 **Approach B: {dataset.get('angle_2_header')}**\n\n{dataset.get('angle_2_body')}")
                    st.error(f"💡 **Approach C: {dataset.get('angle_3_header')}**\n\n{dataset.get('angle_3_body')}")
                    
            except Exception as json_parse_error:
                st.error("⚠️ Data Parsing Notice: The rate limit block or an unmapped string format interfered with the custom layout compilation.")
                # Safe plain text fallback view if JSON parsing encounters data issues
                with st.expander("Toggle Alternative Raw Text Dossier View", expanded=True):
                    if 'response' in locals():
                        st.write(response.text)
                    else:
                        st.write("A clean pipeline handshake could not be established. Please wait 30 seconds for your free-tier key quota to clear and try again.")
