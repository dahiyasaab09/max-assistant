import sys
import os
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from google import genai
from openai import OpenAI
import requests

app = FastAPI(title="MAX 2.0 Quad-AI Neural Grid")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys securely from Render Environment Variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

class CommandRequest(BaseModel):
    command: str

@app.post("/command")
async def process_command(data: CommandRequest):
    # Capture the actual text typed or spoken by you on your phone
    user_input = data.command.strip()
    response_msg = "Command received by MAX core."
    
    try:
        if 'time' in user_input.lower():
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response_msg = f"The current system time is {current_time}."
        else:
            system_prompt = "You are MAX, an elite J.A.R.V.I.S. style artificial intelligence assistant built for your boss, Aadi. Answer concisely, professionally, and intelligently."
            reply = None
            
            # --- TIER 1: GROQ ---
            if groq_client and not reply:
                try:
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.7,
                        max_tokens=300,
                    )
                    reply = completion.choices[0].message.content.strip()
                except Exception as e:
                    print(f"[Failover] Groq bypassed: {e}")

            # --- TIER 2: OPENAI ---
            if openai_client and not reply:
                try:
                    completion = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.7,
                        max_tokens=300,
                    )
                    reply = completion.choices[0].message.content.strip()
                except Exception as e:
                    print(f"[Failover] OpenAI bypassed: {e}")

            # --- TIER 3: GEMINI ---
            if gemini_client and not reply:
                try:
                    full_prompt = f"{system_prompt}\n\nUser Query: {user_input}"
                    ai_response = gemini_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_prompt,
                    )
                    reply = ai_response.text.strip()
                except Exception as e:
                    print(f"[Failover] Gemini bypassed: {e}")

            # Assign the dynamic AI response
            if reply:
                response_msg = reply
            else:
                response_msg = "[CRITICAL] All neural cores failed to process your command."
                
    except Exception as e:
        response_msg = f"Neural grid processing error: {str(e)}"
        
    return {"status": "success", "response": response_msg}

@app.get("/ping")
async def ping_brain():
    return {"status": "active", "brain": "MAX 2.0 Quad-AI Neural Grid Online"}

@app.get("/")
async def root():
    return {"status": "online", "system": "MAX 2.0 Quad-AI Grid Operational"}
