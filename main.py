from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

class CommandRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "Max Brain (Powered by Gemini) is active and online"}

@app.post("/process-command")
async def process_command(request: CommandRequest):
    user_msg = request.message
    
    # Retrieve the API key inside the function to catch configuration issues cleanly
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"response": "Error: GEMINI_API_KEY environment variable is missing on Render."}
    
    try:
        # Initialize client with the key
        client = genai.Client(api_key=api_key)
        
        prompt = f"You are M.A.X., an advanced artificial intelligence assistant inspired by JARVIS from Iron Man. Be concise, intelligent, efficient, and address the user respectfully as 'Sir'. User command: {user_msg}"
        
        # Call Gemini model using the stable gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return {"response": response.text.strip()}
        
    except Exception as e:
        # Return the error message safely as JSON so Flutter won't throw a FormatException
        return {"response": f"Max AI Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
