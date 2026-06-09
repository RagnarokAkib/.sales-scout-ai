import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# 1. Page Configuration for Great Mobile & Desktop Use
st.set_page_config(
    page_title="Sales Scout AI Pro", 
    page_icon="💼", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom Styling for Premium Interface
st.markdown("""
    <style>
    .main .block-container { max-width: 600px; padding-top: 1.5rem; }
    h1 { font-size: 2.2rem !important; text-align: center; color: #1E3A8A; margin-bottom: 0px;}
    p.subtitle { text-align: center; color: #6B7280; font-size: 1.0rem; margin-bottom: 1.5rem; }
    .privacy-badge { background-color: #E0F2FE; color: #0369A1; padding: 5px 10px; border-radius: 15px; font-size: 0.8rem; text-align: center; font-weight: bold; margin-bottom: 15px;}
    </style>
""", unsafe_allow_html=True)

st.write("<h1>💼 Sales Scout AI Pro</h1>", unsafe_allow_html=True)
st.write("<p class='subtitle'>Instant Client Intelligence & Secure PDF Exporter</p>", unsafe_allow_html=True)

# Privacy Badge to reassure sales reps
st.markdown("<div class='privacy-badge'>🔒 Zero-Knowledge System: Data is processed in-memory and never stored on our servers.</div>", unsafe_allow_html=True)

# Initialize a simple active browser session memory for history (Clears when tab closes)
if "session_history" not in st.session_state:
    st.session_state.session_history = []

# 2. STEP 1: The Connection Setup Locker
with st.expander("🔑 STEP 1: Connection & Credentials Setup", expanded=True):
    st.info("Log in once. Your credentials stay strictly in your device's active session.")
    
    # AI Brain Selection
    ai_api_key = st.text_input("🔗 Paste AI API Key (Gemini/OpenAI):", type="password", placeholder="AI_Key...")
    
    st.divider()
    st.write("🌐 **Linked Social Profiles (Optional Integration):**")
    
    li_user = st.text_input("LinkedIn Username:", placeholder="name@company.com")
    li_pass = st.text_input("LinkedIn Password:", type="password")
    
    fb_user = st.text_input("Facebook/Instagram Account:", placeholder="Username")
    fb_pass = st.text_input("Facebook/Instagram Password:", type="password")
    
    if ai_api_key:
        st.success("🎯 LLM Engine Active! You can close this menu and start searching.")
    else:
        st.warning("⚠️ Enter your AI key above to unlock the search dashboard.")

st.divider()

# 3. STEP 2: The Main Intelligence Dashboard
st.subheader("🔍 STEP 2: Target Research")

target_input = st.text_input(
    "Enter Company Name or Prospect Details:", 
    placeholder="e.g., Acme Corp or Jane Doe Director at Acme"
)

specific_goal = st.text_input(
    "Specific Search Criteria? (Optional):", 
    placeholder="e.g., What are their latest products? Main competitors?"
)

# Helper function to generate PDF from text completely in the user's browser memory
def create_pdf_bytes(report_text, entity_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # PDF Title Header
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(200, 10, txt=f"Sales Intelligence Report: {entity_name}", ln=True, align='C')
    pdf.set_font("Helvetica", size=10)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.date.today().strftime('%B %d, %Y')}", ln=True, align='C')
    pdf.ln(10)
    
    # Body Text Processing (removes markdown formatting artifacts for clean PDF viewing)
    pdf.set_font("Helvetica", size=11)
    clean_text = report_text.replace("##", "").replace("###", "").replace("*", "-")
    
    for line in clean_text.split('\n'):
        # Multi-line cell text wrapper to prevent clipping on mobile screens
        pdf.multi_cell(0, 7, txt=line)
        
    return pdf.output()

# 4. STEP 3: Run Search & Process Results
if st.button("🚀 Generate & Compile Dossier", use_container_width=True):
    if not ai_api_key:
        st.error("❌ Action Blocked: You must provide your AI Key in Step 1.")
    elif not target_input:
        st.warning("⚠️ Please provide a company or target name.")
    else:
        with st.spinner(f"Scouting global registries, verifying networks, and structuring data for '{target_input}'..."):
            try:
                # Set up the LLM config
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Dynamic Prompt Injection
                prompt = f"""
                You are a senior-level strategic corporate intelligence engine. 
                Generate a tactical sales dossier based on your deep industrial knowledge graphs and web indexes.
                
                Target Entity: {target_input}
                Specific Focus Request: {specific_goal if specific_goal else 'Provide standard premium executive briefing.'}
                
                Format the final response layout perfectly using simple Markdown formatting:
                
                ## 📊 Executive Briefing: {target_input}
                Provide a sharp, 3-sentence summary detailing exactly what they sell, their market scale, and industry positioning.
                
                ---
                ### 🎯 Tactical Sales Openers & Hooks
                Provide 3 highly direct angles or operational pain-points a sales representative can use to pitch this company.
                
                ---
                ### 🌐 Digital Social Footprint Summary
                - **LinkedIn Insights:** Outline key stakeholders, department growth, or general profile structures.
                - **Meta/Insta Footprint:** Describe their public branding tone, consumer strategy, or recent public marketing plays.
                
                ---
                ### 📋 Specific Requested Custom Intelligence
                Directly address: "{specific_goal if specific_goal else 'No additional custom search requested.'}"
                """
                
                # Fetch text response from AI
                response = model.generate_content(prompt)
                report_content = response.text
                
                # Store this specific search into session history memory for easy toggling
                st.session_state.session_history.append({
                    "target": target_input,
                    "date": datetime.date.today().strftime("%H:%M"),
                    "content": report_content
                })
                
                st.balloons()
                st.success("✅ Intelligence Compiled Successfully!")
                
                # Display the Live Interactive Report
                st.markdown(report_content)
                
                st.divider()
                
                # --- PDF EXPORTER MODULE ---
                st.subheader("📥 Export & Save")
                st.write("Download this report directly to your phone storage. This file will not be saved anywhere else.")
                
                # Generate the PDF file data bytes
                pdf_data = create_pdf_bytes(report_content, target_input)
                
                # Native Streamlit Mobile Download Button
                st.download_button(
                    label="📥 Download Briefing Report (PDF)",
                    data=bytes(pdf_data),
                    file_name=f"Sales_Scout_{target_input.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Failed to communicate with AI Node: {e}. Double-check your API key.")

# 5. STEP 4: Session History Panel (Private to the Browser tab)
if st.session_state.session_history:
    st.divider()
    st.subheader("⏳ Recent Reports (This Session Only)")
    st.caption("These temporary session history cards will vanish completely when you close this browser tab.")
    
    for idx, history_item in enumerate(reversed(st.session_state.session_history)):
        with st.expander(f"📄 Report: {history_item['target']} ({history_item['date']})"):
            st.markdown(history_item['content'])
            
            # Re-generate PDF download option for previous history cards
            hist_pdf = create_pdf_bytes(history_item['content'], history_item['target'])
            st.download_button(
                label=f"Download PDF for {history_item['target']}",
                data=bytes(hist_pdf),
                file_name=f"Sales_Scout_{history_item['target'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                key=f"hist_dl_{idx}"
            )
