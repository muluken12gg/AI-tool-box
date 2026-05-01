from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import sqlite3

def get_db():
    conn = sqlite3.connect("chat.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor  = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

load_dotenv()

client = Groq(api_key = os.getenv("GROK_API_KEY"))

def save_message(user_id, role, content):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO messages (user_id, role, content)
    VALUES (?, ?, ?)
    """, (user_id, role, content))

    conn.commit()
    conn.close()

def get_conversation(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role, content FROM messages
    WHERE user_id = ?
    ORDER BY timestamp ASC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{"role": row["role"], "content": row["content"]} for row in rows]

class Friendly(BaseModel):
    question: str

class Request(BaseModel):
    topic: str
    question: str

class Summarizer(BaseModel):
    text: str

class Generator(BaseModel):
    prompt: str

class Text_Generator(BaseModel):
    prompt: str

@app.on_event("startup")
def startup():
    init_db()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    # 1. Save user message
    save_message(req.user_id, "user", req.message)

    # 2. Get full conversation
    messages = [
        {
            "role": "system",
            "content": "You are a human-like, context-aware conversational assistant. Remember previous messages, respond naturally, and keep the tone warm and personal. Use earlier conversation details to continue the dialogue like a real person, and avoid sounding robotic."
        }
    ] + get_conversation(req.user_id)

    # 3. Send to AI
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.8,
        max_tokens=500
    )

    reply = response.choices[0].message.content

    # 4. Save AI reply
    save_message(req.user_id, "assistant", reply)

    return {"reply": reply}

@app.get("/chat/{user_id}")
def chat_history(user_id: str):
    messages = get_conversation(user_id)
    return {"messages": messages}

@app.post("/topic")
def ask_qustion(req: Request):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
            "role" : "system",
            "content" : "Answer only answers related to provided topic. If the question is not in the topic ask him to focus on his topic."
            },
            {
            "role": "user",
            "content" : f"Context : {req.topic}\nQuestion : {req.question}"
            }
        ]
    )

    return {"answer" :
            response.choices[0].message.content}

@app.post("/friendly")
def ask_friendly_ai(req: Friendly):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "system",
                "content" : "Don't ever talk seriously. Talk casually, use friendly words. You can insult friendly. Don't respond formally when someone chats. Just use friendly, casual, and funny words always."
            },
            {
                "role" : "user",
                "content" : req.question
            }
        ]
    )

    return{"answer" :
           response.choices[0].message.content}

@app.post("/summarize")
def summarize(req: Summarizer):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "system",
                "content" : "Summarize the given text to short sentences or words."
            },
            {
                "role" : "user",
                "content" : req.text
            }
        ]
    )

    return {"answer" : response.choices[0].message.content}

@app.post("/generator")
def generator(req: Generator):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "system",
                "content" : "Generate code that you are asked. only generate codes, no talking."
            },
            {
                "role" : "user",
                "content" : req.prompt
            }
        ]
    )

    return {"answer" : response.choices[0].message.content}

@app.post("/text_generator")
def text_generator(req: Text_Generator):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "system",
                "content" : "Generate clear, helpful responses to the user's prompt. Keep the output concise and relevant."
            },
            {
                "role" : "user",
                "content" : req.prompt
            }
        ]
    )

    return {"answer" : response.choices[0].message.content}