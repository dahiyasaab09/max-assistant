import os
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Initialize Gemini Client (It automatically looks for the GEMINI_API_KEY environment variable)
client = genai.Client()

class CommandRequest(BaseModel):
    command: str

@app.get("/")
def home():
    return {"status": "MAX 2.0 Gemini-Powered Brain is online and operational."}

@app.post("/process")
def process_command(req: CommandRequest):
    cmd = req.command.lower()
    
    if 'time' in cmd:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The current system time is {current_time}."
    elif 'status' in cmd or 'health' in cmd:
        response_text = "Core cloud systems nominal. Gemini intelligence engine active."
    else:
        try:
            # Send the command/question to Gemini for intelligent generation
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"You are MAX 2.0, an advanced Iron Man style AI assistant created for Aadi. Keep responses sharp, concise, futuristic, and helpful. User input: {req.command}"
            )
            response_text = response.text
        except Exception as e:
            response_text = f"Error processing with Gemini AI engine: {str(e)}"
            
    return {"response": response_text}
