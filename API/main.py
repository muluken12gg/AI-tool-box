from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

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

class Friendly(BaseModel):
    question: str

class Request(BaseModel):
    topic: str
    question: str

class Summarizer(BaseModel):
    text: str

class Generator(BaseModel):
    prompt: str

@app.post("/topic")
def ask_qustion(req: Request):
    response = client.chat.completions.create(
        model = "moonshotai/kimi-k2-instruct-0905",
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
        model = "moonshotai/kimi-k2-instruct-0905",
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
        model = "moonshotai/kimi-k2-instruct-0905",
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
        model = "moonshotai/kimi-k2-instruct-0905",
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