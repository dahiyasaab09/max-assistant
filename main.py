from fastapi import FastAPI
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

class CommandRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "MAX Brain (Powered by Gemini) is active and online"}

@app.post("/process-command")
async def process_command(request: CommandRequest):
    user_msg = request.message
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"response": "Error: GEMINI_API_KEY is missing on Render dashboard."}
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Immediate match for startup or introductory text
        if "hello" in user_msg.lower() or "who are you" in user_msg.lower() or "start" in user_msg.lower():
            return {"response": "Hello, I am MAX, a personal assistant of Aadi."}

        prompt = f"You are M.A.X., an advanced artificial intelligence assistant. Be concise, intelligent, efficient, and address the user respectfully as 'Aadi'. User command: {user_msg}"
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        return {"response": response.text.strip()}
        
    except Exception as e:
        return {"response": f"MAX AI Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
