from sqlalchemy import create_engine, MetaData, text
import streamlit as st

from config.settings import DB_URI

engine = create_engine(DB_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

def get_schema_info():
    schema_lines = []
    for table in metadata.tables.values():
        columns = [f"{col.name} {col.type}" for col in table.columns]
        schema_lines.append(f"Table '{table.name}': " + ", ".join(columns))
    return "\n".join(schema_lines)

def validate_multiple_sql(sql_text):
    try:
        queries = [q.strip() for q in sql_text.strip().split(";") if q.strip()]
        with engine.begin() as conn:
            for q in queries:
                conn.execution_options(no_parameters=True).execute(text(q))
        return True
    except Exception as e:
        st.error(f"SQL query validation failed: {e}")
        return False
