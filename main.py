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

# Load all 4 API keys securely from Render Environment Variables
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
    command = data.command.lower().strip()
    response_msg = "Command received by MAX core."
    
    try:
        if 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response_msg = f"The current system time is {current_time}."
        else:
            system_prompt = "You are MAX, an elite J.A.R.V.I.S. style artificial intelligence assistant built for your boss, Aadi. Answer concisely, professionally, and intelligently."
            reply = None
            
            # --- TIER 1: GROQ (Llama 3.3 70B - Lightning Fast) ---
            if groq_client and not reply:
                try:
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": command}
                        ],
                        temperature=0.7,
                        max_tokens=300,
                    )
                    reply = completion.choices[0].message.content.strip()
                except Exception as e:
                    print(f"[Failover] Groq bypassed: {e}")

            # --- TIER 2: OPENAI (GPT-4o-mini - High Intelligence) ---
            if openai_client and not reply:
                try:
                    completion = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": command}
                        ],
                        temperature=0.7,
                        max_tokens=300,
                    )
                    reply = completion.choices[0].message.content.strip()
                except Exception as e:
                    print(f"[Failover] OpenAI bypassed: {e}")

            # --- TIER 3: GOOGLE GEMINI (Stable Flash Backup) ---
            if gemini_client and not reply:
                try:
                    full_prompt = f"{system_prompt}\n\nUser Query: {command}"
                    ai_response = gemini_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_prompt,
                    )
                    reply = ai_response.text.strip()
                except Exception as e:
                    print(f"[Failover] Gemini bypassed: {e}")

            # --- TIER 4: HUGGING FACE (Open-Source Fallback) ---
            if HUGGINGFACE_API_KEY and not reply:
                try:
                    hf_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
                    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
                    payload = {"inputs": f"<s>[INST] {system_prompt}\n\n{command} [/INST]"}
                    
                    hf_resp = requests.post(hf_url, headers=headers, json=payload, timeout=10)
                    if hf_resp.status_code == 200:
                        result = hf_resp.json()
                        if isinstance(result, list) and 'generated_text' in result[0]:
                            reply = result[0]['generated_text'].split("[/INST]")[-1].strip()
                except Exception as e:
                    print(f"[Failover] HuggingFace bypassed: {e}")

            if reply:
                response_msg = reply
            else:
                response_msg = "[CRITICAL ALERT] All 4 neural cores failed to respond. Check API keys."
                
    except Exception as e:
        response_msg = f"Neural grid processing error: {str(e)}"
        
    return {"status": "success", "response": response_msg}

@app.get("/ping")
async def ping_brain():
    return {"status": "active", "brain": "MAX 2.0 Quad-AI Neural Grid Online"}

@app.get("/")
async def root():
    return {"status": "online", "system": "MAX 2.0 Quad-AI Grid Operational"}
