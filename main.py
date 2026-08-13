import sys
import os
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

app = FastAPI(title="MAX 2.0 Cloud Brain")

# Enable CORS for cross-platform app requests (iPhone, iPad, Samsung, PC)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq Client securely using Render's Environment Variable
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
            system_prompt = "You are MAX, an elite J.A.R.V.I.S. style artificial intelligence assistant built for your boss, Aadi. Answer the following query concisely, professionally, and intelligently."
            
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ],
                temperature=0.7,
                max_tokens=300,
            )
            response_msg = completion.choices[0].message.content.strip()
            
    except Exception as e:
        response_msg = f"Neural processing error: {str(e)}"
        
    return {"status": "success", "response": response_msg}

@app.get("/ping")
async def ping_brain():
    return {"status": "active", "brain": "MAX 2.0 Groq FastAPI cloud core online"}
