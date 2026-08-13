import os
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Automatically pulls your secure GEMINI_API_KEY from Render Environment Variables
client = genai.Client()

class CommandRequest(BaseModel):
    command: str

@app.get("/")
def home():
    return {"status": "MAX 2.0 Gemini-3.6 Cloud Brain is online and operational."}

@app.post("/process")
def process_command(req: CommandRequest):
    cmd = req.command.lower()
    
    if 'time' in cmd:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The current system time is {current_time}."
    elif 'status' in cmd or 'health' in cmd:
        response_text = "Core cloud systems nominal. Gemini-3.6 intelligence engine active."
    else:
        try:
            # Using Gemini 3.6 Flash for advanced agentic performance
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=f"You are MAX 2.0, an advanced Iron Man style AI assistant created for Aadi. Keep responses sharp, futuristic, and helpful. User input: {req.command}"
            )
            response_text = response.text
        except Exception as e:
            response_text = f"Error processing with Gemini AI engine: {str(e)}"
            
    return {"response": response_text}
