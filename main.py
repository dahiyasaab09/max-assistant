import os
from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI(title="Max Personal Assistant", version="1.0")

# Setup OpenAI client (or fallback if key isn't provided yet)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy-key"))

class CommandRequest(BaseModel):
    device_id: str
    command: str

@app.post("/process-command")
async def process_command(req: CommandRequest):
    print(f"[{req.device_id}] Received command: {req.command}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Max, an advanced, highly intelligent personal AI assistant inspired by JARVIS. Be concise, efficient, and precise."},
                {"role": "user", "content": req.command}
            ]
        )
        max_reply = response.choices[0].message.content
    except Exception as e:
        max_reply = f"Systems operational. Cloud API key missing or invalid, but Max received your command: '{req.command}'"

    return {
        "status": "success",
        "response": max_reply
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
