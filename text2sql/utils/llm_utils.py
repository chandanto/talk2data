from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import re
from config.settings import groq_api_key

llm = ChatGroq(api_key=groq_api_key, model_name="deepseek-r1-distill-llama-70b", temperature=0.0)

def generate_sql_with_langchain(user_question, schema_info):
    system_prompt = (
        "You are a helpful assistant that converts natural language queries to SQL queries "
        "based on the given database schema. Do not explain anything—just return the SQL query. "
        "If the query is not related to the database schema, return an empty string.\n\n"
        "Schema: \n" + schema_info
    )

    user_prompt = f"Schema: {schema_info}\nQuestion: {user_question}\nSQL:"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    raw_response = response.content.strip()

    cleaned = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL | re.IGNORECASE)
    sql_match = re.search(r"(SELECT|INSERT|UPDATE|DELETE).*", cleaned, re.IGNORECASE | re.DOTALL)

    return sql_match.group(0).strip() if sql_match else "No Valid SQL Statement Found"
