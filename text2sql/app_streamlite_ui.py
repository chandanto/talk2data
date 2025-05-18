import streamlit as st
import pandas as pd
from config.settings import DB_URI, groq_api_key
from utils.db_utils import get_schema_info, validate_multiple_sql, engine
from utils.llm_utils import generate_sql_with_langchain
from utils.ui_components import display_logo, display_instructions
from sqlalchemy import create_engine, MetaData, text
# Page setup
st.set_page_config(page_title="Talk2Data", page_icon="🤖", layout="wide")
display_logo()
display_instructions()

# UI input
col1, _, _ = st.columns([1, 2, 1])
with col1:
    user_query = st.text_input("Ask a question about the Customer data:")

# Main interaction
if st.button("Generate SQL and Query DB") and user_query:
    schema_info = get_schema_info()
    st.write("Schema Info:")
    st.code(schema_info, language="sql")

    with st.spinner("Generating SQL using Groq LLM..."):
        generated_sql = generate_sql_with_langchain(user_query, schema_info)
        st.code(generated_sql, language="sql")

        if validate_multiple_sql(generated_sql):
            try:
                with engine.connect() as conn:
                    queries = [q.strip() for q in generated_sql.strip().split(";") if q.strip()]
                    for i, sql_statement in enumerate(queries):
                        result = conn.execute(text(sql_statement))
                        df = pd.DataFrame(result.fetchall(), columns=result.keys())
                        st.subheader(f"Result for Query {i+1}")
                        st.dataframe(df)
            except Exception as err:
                st.error(f"Error executing SQL query: {err}")