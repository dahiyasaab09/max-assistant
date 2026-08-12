from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

class CommandRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "Max Brain is active and online"}

@app.post("/process-command")
async def process_command(request: CommandRequest):
    user_msg = request.message
    # JARVIS core response logic
    return {"response": f"Hello Sir. Max online. You said: {user_msg}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
