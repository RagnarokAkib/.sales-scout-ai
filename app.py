import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from duckduckgo_search import DDGS
import datetime

st.set_page_config(page_title="Sales Scout AI Pro", page_icon="💼", layout="centered")

st.title("💼 Sales Scout AI Pro")
st.write("Live Web-Searching Client & Company Intelligence Dossier")

# 1. SETUP ENGINE LOCKER
with st.expander("🔑 STEP 1: Enter Your Gemini AI API Key", expanded=True):
    ai_api_key = st.text_input("Paste your Gemini API Key here:", type="password")
    
    st.caption("🌐 Optional Social Profiles (Saved to local browser tab memory):")
    li_user = st.text_input("LinkedIn Username (Optional):", placeholder="name@company.com")
    fb_user = st.text_input("Facebook Username (Optional):", placeholder="Username")
    ig_user = st.text_input("Instagram Username (Optional):", placeholder="Username")

st.divider()

# 2. TARGET RESEARCH
st.subheader("🔍 STEP 2: Target Research")
target_input = st.text_input("Enter Company Name or Person (e.g., Bonny E-Home, Akib):")
specific_goal = st.text_input("Specific Search Criteria? (Optional):", placeholder="e.g., core products, target contact info")

# Safe PDF generator that wraps text beautifully and drops non-standard characters
def create_pdf_bytes(report_text, entity_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, txt=f"Sales Report: {entity_name}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", size=11)
    
    clean_text = report_text.replace("##", "").replace("###", "").replace("*", "-")
    
    for line in clean_text.split('\n'):
        # Clean out emojis or unusual symbols
        clean_line = line.encode('latin-1', 'ignore').decode('latin-1')
        # multi_cell automatically wraps text to the next line so it never crashes width limits!
        pdf.multi_cell(0, 6, txt=clean_line)
    return pdf.output()

# 3. RUN ENGINE WITH LIVE WEB SEARCH
if st.button("🚀 Run Live Web Intelligence", use_container_width=True):
    if not ai_api_key:
        st.error("⚠️ Please enter your AI Key in Step 1 first!")
    elif not target_input:
        st.warning("⚠️ Please type a company or target profile to research!")
    else:
        with st.spinner(f"Actively crawling web directories and social patterns for '{target_input}'..."):
            try:
                # Execution: Gather live search snippets from the open web
                search_query = f"{target_input} {specific_goal if specific_goal else ''}"
                raw_context = ""
                
                with DDGS() as ddgs:
                    results = ddgs.text(search_query, max_results=5)
                    for r in results:
                        raw_context += f"Source Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}\n\n"
                
                # Check if we found web data
                if not raw_context:
                    raw_context = "No public search engine text snippets returned. Relying on default background index layers."

                # Wake up the AI Node
                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Feed the live web research straight into the AI prompt layout
                prompt = f"""
                You are an elite, real-time corporate intelligence agent. 
                Synthesize a factual, tactical sales dossier based on these live web search results. Do not make up facts.
                
                Target Entity Request: {target_input}
                Additional Context: {specific_goal if specific_goal else 'None'}
                
                Live Web Search Results Collected:
                {raw_context}
                
                Provide your intelligence report using this clean Markdown structure (Do not use emojis):
                
                ## Executive Briefing
                Summarize exactly what this company/person does, their real-world presence, and active footprints based on the live data.
                
                ## Key Sales Insights & Hooks
                Provide 3 smart operational hooks a sales rep can use to strike up a business conversation with them.
                
                ## Public Information Sources Located
                Reference the key findings from the search results above.
                """
                
                response = model.generate_content(prompt)
                report_content = response.text
                
                # Print results on dashboard screen
                st.success("✅ Live Intelligence Report Generated!")
                st.markdown(report_content)
                
                st.divider()
                
                # Offer safe PDF download
                pdf_data = create_pdf_bytes(report_content, target_input)
                st.download_button(
                    label="📥 Download Report as PDF",
                    data=bytes(pdf_data),
                    file_name=f"Live_Scout_{target_input.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"System Error running lookup pipeline: {e}")
