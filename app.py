import os
import streamlit as st
from agent import run_research

st.set_page_config(page_title="AI Research Agent", page_icon="🔎")
st.title("🔎 AI Research Agent")
st.caption("CrewAI + Groq + DuckDuckGo")

api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

topic = st.text_input("Research topic", placeholder="e.g. Future of quantum computing")

if st.button("Generate Report", type="primary"):
    if not api_key:
        st.error("GROQ_API_KEY missing hai. Secrets me add karo.")
    elif not topic.strip():
        st.warning("Pehle topic likho.")
    else:
        with st.spinner("Agent research kar raha hai..."):
            try:
                report = run_research(topic.strip(), api_key)
                st.markdown(report)
                st.download_button("Download report (.md)", report, file_name="report.md")
            except Exception as e:
                st.error(f"Error: {e}")