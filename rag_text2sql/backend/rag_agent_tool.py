from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from utils.ui_helpers import format_documents

def get_tools(sql_db, faiss_db, openai_api_key):
    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.3)
    tools = []

    if sql_db:
        toolkit = SQLDatabaseToolkit(llm=llm, db=sql_db)
        tools.append(Tool(name="SQL Database", func=sql_db.run, description="Query structured sales/inventory data."))
        tools.extend(toolkit.get_tools())

    if faiss_db:
        tools.append(Tool(name="Building Code Search", func=lambda q: format_documents(faiss_db.similarity_search(q, k=3)), description="Search building codes."))

    return tools

def get_agent_response(tools, openai_api_key):
    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.3)
    return initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True)
