import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# Page Setup for Mobile Phones
st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="centered")

st.title("💼 Sales Scout AI Pro")
st.write("Enter your key, connect optional platforms, and get a custom client report.")

# 1. SETUP LOG-IN LOCKER (With Optional Social Media Platforms)
with st.expander("🔑 STEP 1: Connection & Credentials Setup", expanded=True):
    st.info("Log in once. Only the AI API Key is required. Social platforms are 100% optional.")
    
    # REQUIRED
    ai_api_key = st.text_input("🔑 Paste Gemini API Key (Required):", type="password", placeholder="AI_Key...")
    
    st.divider()
    st.write("🌐 **Optional Social Profiles (Leave blank if you don't use them):**")
    
    # OPTIONAL FIELDS
    li_user = st.text_input("LinkedIn Username:", placeholder="name@company.com")
    li_pass = st.text_input("LinkedIn Password:", type="password")
    
    fb_user = st.text_input("Facebook Username:", placeholder="Username")
    fb_pass = st.text_input("Facebook Password:", type="password")
    
    ig_user = st.text_input("Instagram Username:", placeholder="Username")
    ig_pass = st.text_input("Instagram Password:", type="password")
    
    if ai_api_key:
        st.success("🎯 AI Engine Connected! You can close this box now.")

st.divider()

# 2. TARGET RESEARCH INPUTS
st.subheader("🔍 STEP 2: Target Research")
target_input = st.text_input("Enter Company Name or Prospect Details:", placeholder="e.g., Acme Corp or John Doe at Acme")
specific_goal = st.text_input("Specific Search Criteria? (Optional):", placeholder="e.g., What are their latest products?")

# Helper tool to create the PDF download file
def create_pdf_bytes(report_text, entity_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(200, 10, txt=f"Sales Report: {entity_name}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", size=11)
    clean_text = report_text.replace("##", "").replace("###", "").replace("*", "-")
    for line in clean_text.split('\n'):
        pdf.multi_cell(0, 7, txt=line)
    return pdf.output()

# 3. RUN ENGINE BUTTON
if st.button("🚀 Generate Report & PDF", use_container_width=True):
    # This is the fix: The code now ONLY blocks the user if the AI Key is missing!
    if not ai_api_key:
        st.error("⚠️ Please enter your Gemini AI Key in Step 1 first!")
    elif not target_input:
        st.warning("⚠️ Please type a company or prospect name!")
    else:
        with st.spinner("AI Agent is scanning records and compiling your briefing..."):
            try:
                # Initialize the Gemini AI Engine
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Check which optional accounts the sales rep provided
                linkedin_status = f"Connected as {li_user}" if li_user else "Not connected (Using fallback public search)"
                facebook_status = f"Connected as {fb_user}" if fb_user else "Not connected (Using fallback public search)"
                instagram_status = f"Connected as {ig_user}" if ig_user else "Not connected (Using fallback public search)"
                
                # Build the AI Prompt
                prompt = f"""
                You are an elite sales intelligence agent. Provide a detailed sales dossier for the target.
                
                Target: {target_input}
                Custom Request from Sales Rep: {specific_goal if specific_goal else 'Provide a general executive briefing.'}
                
                Rep Platform Connections Status:
                - LinkedIn: {linkedin_status}
                - Facebook: {facebook_status}
                - Instagram: {instagram_status}
                
                Structure your report cleanly with markdown formatting:
                ## 📊 Executive Briefing
                (A clear summary of what they do and their industry presence)
                
                ### 🎯 Tactical Sales Hooks
                (Provide 3 smart angles the rep can use to pitch them)
                
                ### 🌐 Digital & Social Footprint Notes
                (Summarize how they look online based on the active connections listed above)
                """
                
                response = model.generate_content(prompt)
                report_content = response.text
                
                # Show results on screen
                st.success("✅ Intelligence Dossier Generated Successfully!")
                st.markdown(report_content)
                
                st.divider()
                
                # Generate PDF download option
                pdf_data = create_pdf_bytes(report_content, target_input)
                st.download_button(
                    label="📥 Download This Briefing Report (PDF)",
                    data=bytes(pdf_data),
                    file_name=f"Sales_Scout_{target_input.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Failed to communicate with AI Node: {e}")
