# app_streamlite_rag_ui.py
import streamlit as st
import pandas as pd
import tempfile
import os
from sqlalchemy import create_engine, MetaData, text
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import re
import base64
from pathlib import Path
# from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

# -- Configuration --
groq_api_key = st.secrets["groq_api_key"]
DB_URI = st.secrets["DB_URI"]

# Initialize components
engine = create_engine(DB_URI)
metadata = MetaData()
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=st.secrets["hf_api_key"],
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
llm = ChatGroq(api_key=groq_api_key, model_name="mixtral-8x7b-32768", temperature=0.3)

# -- Session State --
if 'faiss_db' not in st.session_state:
    st.session_state.faiss_db = None
if 'sql_db' not in st.session_state:
    st.session_state.sql_db = SQLDatabase(engine)

# -- Helper functions --
def get_base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def process_pdf(uploaded_file):
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        # Load and split the PDF into pages
        loader = PyPDFLoader(tmp_path)
        pages = loader.load_and_split()

        # Add metadata to each page (e.g., filename, page number)
        for i, page in enumerate(pages):
            page.metadata['source'] = uploaded_file.name
            page.metadata['page_number'] = i + 1

        # Split pages into smaller text chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Adjust based on your use case
            chunk_overlap=200  # Helps preserve context between chunks
        )
        texts = text_splitter.split_documents(pages)   # Returns list of Document objects

        # Create a FAISS vector database from chunks
        db = FAISS.from_documents(texts, embeddings) # Assumes `embeddings` is predefined
        os.remove(tmp_path) # Clean up the temporary file
        return db
    except Exception as e:
        raise RuntimeError(f"PDF processing failed: {str(e)}")

def process_csv(uploaded_file):
    # Create a temporary file    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Sanitize table name
    table_name = os.path.splitext(uploaded_file.name)[0].lower()
    # table_name = re.sub(r'\W+', '_', table_name)  # Clean invalid characters
    
    try:
        # Read CSV
        df = pd.read_csv(tmp_path)

        # Validate DataFrame (example: ensure columns are safe)
        # df.columns = [re.sub(r'\W+', '_', col) for col in df.columns]

        # Write to SQL
        df.to_sql(table_name, engine, if_exists='replace', index=False) 

        os.remove(tmp_path)
        metadata.reflect(bind=engine)
        return SQLDatabase.from_uri(DB_URI) # Creating a new connection with from_uri 
    
    # except pd.errors.ParserError as e:
    #     raise ValueError(f"CSV parsing failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"SQL write failed: {str(e)}")


def get_schema_info():
    metadata.reflect(bind=engine)
    schema_lines = []
    for table in metadata.tables.values():
        columns = [f"{col.name} ({str(col.type)})" for col in table.columns]
        schema_lines.append(f"Table '{table.name}': {', '.join(columns)}")
    return "\n".join(schema_lines)

def validate_sql(sql_text):
    try:
        with engine.connect() as conn:
            conn.execute(text(f"EXPLAIN {sql_text}"))
        return True
    except Exception as e:
        st.error(f"SQL validation failed: {e}")
        return False

def format_documents(docs):
    if not docs:
        return "No relevant documents found."
    result = ""
    for doc in docs:
        meta = doc.metadata
        source = meta.get("source", "Unknown")
        page = meta.get("page_number", "N/A")
        result += f"\n**Source:** {source} (Page {page})\n```\n{doc.page_content.strip()}\n```\n"
    return result.strip()

# -- Streamlit UI --
logo_path = Path("static/logo/TakePart_In_AI_logo.png")
logo_base64 = get_base64_image(logo_path)
st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 150px; margin-right: 15px;" />
            <div>
                <h1 style="margin: 0; font-size: 36px; font-weight: bold; color: #1F4E79; letter-spacing: 2px;">RAG Construction Assistant</h1>
                <p style="margin: 0; font-size: 16px; color: #6c757d; font-style: italic;">Ask about building codes or sales data</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# -- Streamlit UI --
st.markdown("""
### 💬 How to Ask Questions

Here are some example questions you can try:

- `Show materials with density over 2000 kg/m³`
- `List structural materials with tensile strength above 300 MPa`
- `Compare costs of fire-rated materials`
- `What's the most thermally conductive material under $2/kg?`
- `What's the fire safety requirement for steel structures?"  # Uses PDF`
- `Show total sales of materials with density > 2400 kg/m³"  # Combines CSV+SQL`
- `What's the minimum concrete strength required?`
- `Compare sales of Category A and B materials`
""")  

# User input - Ask a question on UI
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios to your layout preference

# File upload section
with st.sidebar:
    st.header("Upload Documents")
    pdf_file = st.file_uploader("Upload PDF (Building Codes)", type="pdf")
    csv_file = st.file_uploader("Upload CSV (Material Specs)", type="csv")

    if pdf_file:
        st.session_state.faiss_db = process_pdf(pdf_file)
        st.success("PDF processed and added to FAISS.")
    if csv_file:
        st.session_state.sql_db = process_csv(csv_file)
        st.success("CSV loaded into SQL database.")

# Tool initialization logic -  ReAct prompting (Reason + Act) 
tools = []

# SQL database tool - initialization
if st.session_state.sql_db:
    toolkit = SQLDatabaseToolkit(llm=llm, db=st.session_state.sql_db)
    tools.append(
        Tool(
            name="SQL Database",
            func=st.session_state.sql_db.run,
            description="Use for structured data queries about sales, customers, or materials"
        )
    )
    tools.extend(toolkit.get_tools())

# Semantic Seach on Vector database tool - initialization
if st.session_state.faiss_db:
    tools.append(
        Tool(
            name="Building Code Search",
            func=lambda q: format_documents(st.session_state.faiss_db.similarity_search(q, k=3)),
            description="Use for building code and construction regulation questions"
        )
    )

# Tool Structure - LangChain agent
agent = None
if tools:
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

# Query interface
user_query = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if not user_query:
        st.warning("Please enter a question")
    elif not agent:
        st.error("Please upload documents or CSV to enable the assistant.")
    else:
        with st.spinner("Thinking..."):
            try:
                schema_info = get_schema_info()
                prompt = f"""You are an assistant combining structured data (sales, inventory, materials) and unstructured building code documents.
Schema Information:
{schema_info}

User Question: {user_query}

Provide a detailed answer that cites documents if relevant.
"""
                response = agent.run(prompt)
                st.markdown(f"### Answer:\n{response}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Show schema
if st.checkbox("Show Database Schema"):
    st.code(get_schema_info(), language="sql")