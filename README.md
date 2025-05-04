##  GenAI-Powered Text-to-SQL Application
## Overview
This project enables users to interact with databases using natural language queries, transforming them into executable SQL statements through a Generative AI model. It leverages Groq's LLM (deepseek-r1-distill-llama-70b) for SQL generation, integrated with a backend database and a frontend interface built with Streamlit.

<img src="static/logo/Talk2Data.PNG" alt="Logo" width="370"/>

## Key Features
- Natural Language Interface: Users can input plain English questions.
- SQL Generation: Converts natural language queries into SQL using Groq's LLM.
- SQL Validation: Ensures generated SQL is valid before execution.
- Token Usage Tracking (NOT WORKING): Monitors token usage per query for cost and performance insights.
- Real-Time Execution: Executes validated SQL queries on the connected database.
- Dynamic Schema Awareness: Adapts to the database schema for accurate query generation.

## Technologies Used
- Backend: Python, SQLAlchemy
- Frontend: Streamlit
- Database: SQLite (or any other supported by SQLAlchemy)
- LLM Integration: Groq's ChatGroq class
- Tokenizer: Hugging Face's transformers library for token counting

## Prerequisites
- Python 3.8 or higher
- Streamlit
- SQLAlchemy
- LangChain
- Groq LLM
- Docker (Alpine-based, minimal size)
- make 

## Requirements file
requirements.txt
```
streamlit
sqlalchemy
langchain
groq
pandas
langchain-groq
sqlite3
transformers
```
## Setup Instructions
1. Clone the repository: `git clone https://github.com/chandanto/talk2data.git`

## Install all packages as per requirements.txt
```
pip install -r requirements.txt
```

## Validate the packages 
```
python -c "import importlib; modules = ['streamlit', 'sqlalchemy', 'langchain', 'groq', 'pandas', 'langchain_groq', 'sqlite3', 'transformers']; [print(f'{m}:', importlib.import_module(m).__version__) for m in modules]"
```

## Secrets file
secrets.toml
```
groq_api_key = "your-groq-api-key"
DB_URI = "your-database-uri"
```

## Database schema file init_muliple_tables_db.py
init_muliple_tables_db.py
```python
# Your database schema initialization code here
```

## Execution of database schema - init_muliple_tables_db.py
This will create the database and tables.
```
python init_muliple_tables_db.py
```

## Database schema file schema.sql
shop.sql
```sql
-- Your database schema here
```

## Usage
1. To Run the app: `python -m streamlit run app_streamlite_ui.py`
2. Enter your 'query in text format'.
3. Click the "Generate SQL and Query DB" button.
4. The generated SQL query will be displayed.
5. The results of the SQL query will be displayed.

## Run the app - app_streamlite_ui.py
```
python -m streamlit run app_streamlite_ui.py
```

## 🐳 Docker Usage and Makefile
## 📦 Dockerfile Overview
Multi-stage Alpine build to reduce image size:
- Stage 1: Build + install dependencies
- Stage 2: Minimal runtime with only required libs
- Uses external .streamlit/secrets.toml via volume mount


## 🔧 Build Docker Image
``` 
docker build -t text2data:1.0.0 -t text2data:latest .
```
or

```
make build-debug or make build-prod
```
This tags your image as:
- text2data:1.0.0
- text2data:latest

## Docker Run 🚀 the App
```
docker run -p 8501:8501 -v .\.streamlit\:/app/.streamlit text2data:latest
```
or
```
make run-debug or make run-prod
```
This maps port 8501 on your host to the container and mounts the .streamlit directory for secrets.

<img src="static/logo/TakePart_In_AI_logo.png" alt="Logo" width="120"/>