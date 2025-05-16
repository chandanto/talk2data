import sqlite3
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

#DB setup
DB_URI = "chat_history.db"
conn = sqlite3.connect(DB_URI)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
               
''')
conn.commit()

# Initialize Chat Model
llm = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.3)
SESSION_ID = "user_session_sqlite"

# Load previous history - Select tofind previous chat
def get_history(session_id) -> list[BaseMessage]:
    cursor.execute("SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY timestamp", (session_id,))
    rows = cursor.fetchall()
    messages = []
    for role, content in rows:
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "ai":
            messages.append(AIMessage(content=content))
    return messages

# Load chat history and display to user
chat_history = get_history(SESSION_ID)
if chat_history:
    print("\n--- Loaded Previous Chat History ---")
    for msg in chat_history:
        role = "User" if isinstance(msg, HumanMessage) else "AI"
        print(f"{role}: {msg.content}")
    print("-------------------------------------\n")
else:
    print("No previous chat history found.\n")

# Start Chatting
print("Start chatting with the AI. Type 'exit' to quit.")

while True:
    human_input = input("User: ")
    if human_input.lower() == "exit":
        break

    # Add user input to history
    user_msg = HumanMessage(content=human_input)
    chat_history.append(user_msg)

    # Save to DB
    cursor.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)",
                   (SESSION_ID, "user", human_input))
    conn.commit()

    # Get AI response using full history
    ai_response = llm.invoke(chat_history)

    # Add AI response to history
    chat_history.append(AIMessage(content=ai_response.content))

    # Save AI response to DB
    cursor.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)",
                   (SESSION_ID, "ai", ai_response.content))
    conn.commit()

    print(f"AI: {ai_response.content}")
