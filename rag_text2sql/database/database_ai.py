from sqlalchemy import create_engine, MetaData, text
from langchain_community.utilities import SQLDatabase

def process_csv(uploaded_file, db_uri):
    import pandas as pd
    import tempfile, os
    table_name = uploaded_file.name.split(".")[0].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    df = pd.read_csv(tmp_path)
    engine = create_engine(db_uri)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    os.remove(tmp_path)
    return SQLDatabase(engine)

def get_schema_info(db_uri):
    engine = create_engine(db_uri)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    schema_lines = []
    for table in metadata.tables.values():
        cols = ", ".join([f"{col.name} ({str(col.type)})" for col in table.columns])
        schema_lines.append(f"Table '{table.name}': {cols}")
    return "\n".join(schema_lines)

def validate_sql(sql_text, db_uri):
    engine = create_engine(db_uri)
    try:
        with engine.connect() as conn:
            conn.execute(text(f"EXPLAIN {sql_text}"))
        return True
    except:
        return False
