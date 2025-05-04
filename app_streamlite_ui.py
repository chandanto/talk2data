import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData, text
from langchain_groq import ChatGroq # Import the ChatGroq class from the langchain_groq module
from langchain.schema import HumanMessage, AIMessage, SystemMessage 
import re
# from transformers import AutoTokenizer
from pathlib import Path
import base64



# -- Configuration --
groq_api_key = st.secrets["groq_api_key"]
DB_URI = st.secrets["DB_URI"]

# connect to SQLite database
engine = create_engine(DB_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

# Setup Groq LLM
llm = ChatGroq(api_key=groq_api_key, model_name="deepseek-r1-distill-llama-70b", temperature=0.0)
# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# -- Set page Config --
st.set_page_config(page_title="Talk2Data", page_icon="🤖", layout="wide")

# -- Load and encode the Logo image --
def get_base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
logo_path = Path("static/logo/TakePart_In_AI_logo.png")
logo_base64 = get_base64_image(logo_path)

# -- Display logo + title inline at top-left --
st.markdown(
    f"""
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 150px; margin-right: 15px;" />
            <div>
                <h1 style="margin: 0; font-size: 36px; font-weight: bold; color: #1F4E79; letter-spacing: 2px;">Talk2Data</h1>
                <p style="margin: 0; font-size: 16px; color: #6c757d; font-style: italic;">Explore. Learn. Build. TakePart In AI.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -- Streamlit UI --
st.markdown("""
### 💬 How to Ask Questions

Here are some example questions you can try:

- `What is the total sales for each product category with product names?`
- `What is the total sales for each product category in January 2020?`
- `Show total amount spent by each customer.`
- `Show total amount spent by each customer in the year 2020.`
""")  

# User input - Ask a question on UI
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios to your layout preference

with col1:
    user_query = st.text_input("Ask a question about the Customer data:")
# user_query = st.text_input("Ask a question about the Customer data:")

# Generate schema string dynamically based on the tables in the database
def get_schema_info():
    schema_lines = []
    for table in metadata.tables.values():
        columns = [f"{col.name} {col.type}" for col in table.columns]
        schema_lines.append(f"Table '{table.name}': " + ", ".join(columns))
        # print(f"Table '{table.name}': " + ", ".join(columns))
    return "\n".join(schema_lines)

# Validate generated SQL query function
def validate_sql(sql_text):
    try:
        with engine.connect() as conn:
            conn.execute(text(f"EXPLAIN {sql_text}"))
            # st.success("SQL query validation passed: {}".format(sql_text))
        return True
    except Exception as e:
        st.error(f"SQL query validation failed: {e}")
        return False

# Validate multiple SQL statements function
def validate_multiple_sql(sql_text):
    try:

        # split into individual queries
        queries = [q.strip() for q in sql_text.strip().split(";") if q.strip()]

        with engine.begin() as conn:
            for q in queries:

                # For Validation, we just prepare the statement, not neccessarily execute it
                conn.execution_options(no_parameters=True).execute(text(q))
                # conn.execute(text(f"EXPLAIN {sql_statement}"))
        return True
    except Exception as e:
        st.error(f"SQL query validation failed: {e}")
        return False

# Token count function
def count_tokens(messages, tokenizer):
    total_tokens = 0
    for msg in messages:
        if hasattr(msg, 'content'):
            tokens = tokenizer.encode(msg.content, add_special_tokens=False)
            total_tokens += len(tokens)
    return total_tokens
    
# Generate SQL using Lanchain with Groq LLM function
def generate_sql_with_langchain(user_question, schema_info):
    system_prompt = (
        "You are a helful assistant that converts natural language queries to SQL queries."
        "based on the given database schema. Do not explain anything-just return the SQL query."
        "If the query is not related to the database schema, return an empty string."
        "You are given the following schema information: \n" + schema_info
    )
    user_prompt = f"""
Schema: {schema_info}
Question: {user_question}
SQL: """
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    
    # Token usage before sending to LLM
    # input_tokens = count_tokens(messages, tokenizer)

    response = llm.invoke(messages)
    raw_response = response.content.strip()

    # output_tokens = len(tokenizer.encode(raw_response))
    # total_tokens = input_tokens + output_tokens

    # Display or log token usage
    # st.info(f"🧠 Tokens used: Prompt={input_tokens}, Response={output_tokens}, Total={total_tokens}")

    # response = llm.invoke(messages)
    # raw_response = response.content.strip()



    # -- Clean it --
    # 1. Remove <think> tags and anything inside them
    cleaned = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL | re.IGNORECASE)

    # 2. Extract only the first SQL SELECT/INSERT/UPDATE/DELETE statement
    sql_match = re.search(r"(SELECT|INSERT|UPDATE|DELETE).*", cleaned, re.IGNORECASE | re.DOTALL)

    if sql_match:
        return sql_match.group(0).strip()
    else:
        return "No Valid SQL Statement Found" # Return validate information
    

# Main interaction
if st.button("Generate SQL and Query DB") and user_query:
    schema_info = get_schema_info()
    st.write("Schema Info:")
    st.code(schema_info, language="sql")
    # Print schema_info
    # st.write("Schema Info:")
    # st.code(schema_info, language="sql")
    with st.spinner("Generating SQL uing groq LLM..."):
        generated_sql = generate_sql_with_langchain(user_query, schema_info)

        # Display the generated SQL query
        st.code(generated_sql, language="sql")

        if validate_multiple_sql(generated_sql):
            # st.success("SQL query validation passed. Executing query...")
            with engine.connect() as conn:
                    # Execute the Split multiple SQL statements and also if possible execute them one-by-one
                    try:
                        queries = [q.strip() for q in generated_sql.strip().split(";") if q.strip()]
                        for i, sql_statement in enumerate(queries):
                            result = conn.execute(text(sql_statement))
                            df = pd.DataFrame(result.fetchall(), columns=result.keys())
                            st.subheader(f"Result for Query {i+1}")
                            st.dataframe(df)
                    except Exception as err:
                        st.error(f"Error executing SQL query: {err}")
                    # # Execute only one SQL statement
                    # try:
                    #     result = conn.execute(text(generated_sql))
                    #     df = pd.DataFrame(result.fetchall(), columns=result.keys())
                    #     st.dataframe(df)
                    # except Exception as err:
                    #     st.error(f"Error executing SQL query: {err}")



