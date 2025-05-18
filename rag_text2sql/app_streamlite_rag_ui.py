import streamlit as st
from pathlib import Path
from backend.rag_agent_tool import get_agent_response, get_tools
from database.database_ai import get_schema_info, process_csv
from utils.file_processing import process_pdf
from utils.ui_helpers import get_base64_image


# Load secrets
groq_api_key = st.secrets["groq_api_key"]
openai_api_key = st.secrets["openai_api_key"]
DB_URI = st.secrets["DB_URI"]

# UI Logo
logo_path = Path("static/logo/TakePart_In_AI_logo.png")
logo_base64 = get_base64_image(logo_path)
st.markdown(f"""<div style="display: flex;"><img src="data:image/png;base64,{logo_base64}" style="width: 150px;" /><div><h1>RAG Construction Assistant</h1></div></div>""", unsafe_allow_html=True)

# Instructions
st.markdown("""
    ### 💬 Example Questions\n
    - `What’s the fire safety requirement for steel structures?`
    - `Compare costs of fire-rated materials`
    - `Show total sales of materials with density > 2400 kg/m³`
    - `Show materials with density over 2000 kg/m³`
    - `List structural materials with tensile strength above 300 MPa`
    - `What's the most thermally conductive material under $2/kg?`
    - `What's the minimum concrete strength required?`
    - `Compare sales of Category A and B materials`
    """)

# File Uploads
with st.sidebar:
    st.header("Upload Documents")
    pdf_file = st.file_uploader("Upload PDF", type="pdf")
    csv_file = st.file_uploader("Upload CSV", type="csv")
    
    if pdf_file:
        st.session_state.faiss_db = process_pdf(pdf_file, openai_api_key)
        st.success("PDF processed.")

    if csv_file:
        st.session_state.sql_db = process_csv(csv_file, DB_URI)
        st.success("CSV loaded to SQL database.")

# Setup tools and agent
tools = get_tools(st.session_state.get("sql_db"), st.session_state.get("faiss_db"), openai_api_key)
agent = get_agent_response(tools, openai_api_key) if tools else None

# Query box
user_query = st.text_input("Ask your question:")
if st.button("Get Answer") and user_query:
    if not agent:
        st.warning("Upload PDF/CSV to activate assistant.")
    else:
        with st.spinner("Thinking..."):
            response = agent.run(user_query)
            st.markdown(f"### Answer:\n{response}")

# Schema view
if st.checkbox("Show Database Schema"):
    st.code(get_schema_info(DB_URI), language="sql")