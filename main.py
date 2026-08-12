from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

# Initialize the Gemini client using the environment variable
# (Make sure to install 'google-genai' in your requirements.txt)
client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6Ket9ym_1hgsRVd0wGGRCL8jaiUoEfKsMZWy2DmbLT5ug"))

class CommandRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "Max Brain (Powered by Gemini) is active and online"}

@app.post("/process-command")
async def process_command(request: CommandRequest):
    user_msg = request.message
    
    try:
        # Prompt instructing Gemini to act as JARVIS
        prompt = f"You are M.A.X., an advanced artificial intelligence assistant inspired by JARVIS from Iron Man. Be concise, intelligent, efficient, and address the user respectfully as 'Sir'. User command: {user_msg}"
        
        # Call Gemini model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return {"response": response.text.strip()}
        
    except Exception as e:
        return {"response": f"Max online, but error connecting to Gemini brain: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
