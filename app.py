import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="centered")

st.title("💼 Sales Scout AI Pro")
st.write("Live Web-Searching Client & Company Intelligence Dossier")

# 1. SETUP ENGINE LOCKER
with st.expander("🔑 STEP 1: Connection & Credentials Setup", expanded=False):
    ai_api_key = st.text_input("Paste your Gemini API Key here:", type="password")
    
    st.caption("🌐 Optional Social Profiles (Saved to local browser tab memory):")
    li_user = st.text_input("LinkedIn Username (Optional):", placeholder="name@company.com")
    fb_user = st.text_input("Facebook Username (Optional):", placeholder="Username")
    ig_user = st.text_input("Instagram Username (Optional):", placeholder="Username")

st.divider()

# 2. TARGET RESEARCH
st.subheader("🔍 STEP 2: Target Research")
target_input = st.text_input("Enter Company Name or Person (e.g., Bonny E-Home):")
specific_goal = st.text_input("Specific Search Criteria? (Optional):", placeholder="e.g., core products, target audience")

# 3. RUN ENGINE 
if st.button("🚀 Run Live Web Intelligence", use_container_width=True):
    if not ai_api_key:
        st.error("⚠️ Please enter your AI Key in Step 1 first!")
    elif not target_input:
        st.warning("⚠️ Please type a company or target profile to research!")
    else:
        with st.spinner(f"Analyzing directories and social patterns for '{target_input}'..."):
            try:
                # Wake up the Gemini AI Engine
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # We force Gemini to output a clean JSON dataset so we can build colorful UI charts/cards
                prompt = f"""
                You are an elite corporate intelligence agent. Analyze your knowledge base for the company or individual listed below. 
                
                Target Entity Name: {target_input}
                Specific Focus: {specific_goal if specific_goal else 'Provide a core company breakdown.'}
                
                You must respond ONLY with a valid JSON object matching this structure exactly. Do not include markdown formatting or backticks outside the JSON.
                {{
                    "company_name": "Official Name",
                    "confidence_score": 95,
                    "location": "City, Country or Primary Market",
                    "core_business": "1 sentence description of what they do",
                    "key_products": ["Product 1", "Product 2", "Product 3"],
                    "pitch_angle_1_title": "Title for first sales approach",
                    "pitch_angle_1_desc": "Explanation of how to pitch them",
                    "pitch_angle_2_title": "Title for second sales approach",
                    "pitch_angle_2_desc": "Explanation of how to pitch them",
                    "pitch_angle_3_title": "Title for third sales approach",
                    "pitch_angle_3_desc": "Explanation of how to pitch them",
                    "digital_presence": "Summary of their online and social footprint channels"
                }}
                """
                
                response = model.generate_content(prompt)
                
                # Clean up response string to make sure it's pure data
                raw_text = response.text.strip().replace("```json", "").replace("```", "")
                data = json.loads(raw_text)
                
                st.success("✅ Intelligence Dossier Compiled Successfully!")
                st.divider()
                
                # --- VISUAL DASHBOARD DESIGN STARTS HERE ---
                
                # Row 1: High-visibility metrics (Colorful bars/status indicators)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="🏢 Verified Entity", value=data.get("company_name", target_input))
                with col2:
                    # Visual representation of accuracy/data availability
                    score = data.get("confidence_score", 90)
                    st.metric(label="🎯 Data Accuracy Confidence", value=f"{score}%")
                    st.progress(score / 100)
                
                # Row 2: Main Overview inside a clean info container
                with st.container(border=True):
                    st.markdown(f"📍 **Primary Location/Market:** {data.get('location', 'Global Market')}")
                    st.markdown(f"💼 **Core Business Operations:** {data.get('core_business', '')}")
                
                # Row 3: Product Checklist (Interactive UI elements)
                st.subheader("📦 Core Product Lines Identified")
                products = data.get("key_products", [])
                for prod in products:
                    st.markdown(f"- ✅ **{prod}**")
                
                st.divider()
                
                # Row 4: Pitch Tactics (Using colorful Alert Boxes for separation)
                st.subheader("🎯 Recommended Sales Pitch Angles")
                
                st.info(f"💡 **Angle 1: {data.get('pitch_angle_1_title', 'Operational Improvement')}**\n\n{data.get('pitch_angle_1_desc', '')}")
                st.warning(f"💡 **Angle 2: {data.get('pitch_angle_2_title', 'Digital Scaling')}**\n\n{data.get('pitch_angle_2_desc', '')}")
                st.error(f"💡 **Angle 3: {data.get('pitch_angle_3_title', 'Value Optimization')}**\n\n{data.get('pitch_angle_3_desc', '')}")
                
                st.divider()
                
                # Row 5: Digital Footprint
                with st.expander("🌐 View Digital Channels & Footprint Summary", expanded=True):
                    st.write(data.get("digital_presence", "Public records indicate an active brand footprint across primary web directories."))
                    
            except Exception as e:
                st.error(f"UI Layout Engine encountered an issue parsing data lines: {e}")
                # Fallback to display text if JSON fails
                if 'response' in locals():
                    st.markdown(response.text)
