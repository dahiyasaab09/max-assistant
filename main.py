import os
import re
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="Max Personal Assistant", version="1.2")

# Set GEMINI_API_KEY as an environment variable on Render (Settings -> Environment).
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Whitelist of device actions the Flutter app knows how to execute.
# Keep this in sync with _executeDeviceAction() in main.dart.
VALID_ACTIONS = {
    "OPEN_NOTEPAD",
    "OPEN_CALCULATOR",
    "OPEN_PAINT",
    "OPEN_INSTAGRAM",
    "OPEN_WHATSAPP",
    "OPEN_MAPS",
    "OPEN_YOUTUBE",
    "VOLUME_UP",
    "VOLUME_DOWN",
    "SCREENSHOT",
}

ACTION_TAG_RE = re.compile(r"\[ACTION:([A-Z_]+)\]")

SYSTEM_PROMPT = (
    "You are MAX, an advanced, highly intelligent personal AI assistant inspired by JARVIS, "
    "speaking to your creator Aadi. Be concise, efficient, and precise. "
    "If — and only if — the user's request clearly means one of the following device actions, "
    "end your reply with exactly one tag on its own, chosen from: "
    f"{', '.join(sorted(VALID_ACTIONS))}. "
    "Format the tag like [ACTION:OPEN_NOTEPAD]. "
    "If no device action applies, do not include any tag at all."
)


class HistoryTurn(BaseModel):
    role: str  # "user" or "assistant"
    text: str


class CommandRequest(BaseModel):
    message: str
    history: Optional[List[HistoryTurn]] = None
    device_id: Optional[str] = None  # unused for now, kept for future multi-device support


@app.post("/process-command")
async def process_command(req: CommandRequest):
    print(f"[{req.device_id or 'unknown-device'}] Received command: {req.message}")

    action = "NONE"

    if client is None:
        clean_reply = (
            f"Systems operational, Aadi. Gemini API key isn't configured on the server yet, "
            f"but MAX received your command: '{req.message}'"
        )
        return {"status": "success", "response": clean_reply, "action": action}

    # Gemini expects roles "user" and "model" (not "assistant").
    contents: List[types.Content] = []
    for turn in (req.history or []):
        role = "model" if turn.role == "assistant" else "user"
        contents.append(types.Content(role=role, parts=[types.Part(text=turn.text)]))
    contents.append(types.Content(role="user", parts=[types.Part(text=req.message)]))

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        raw_reply = response.text or "Systems nominal."

        match = ACTION_TAG_RE.search(raw_reply)
        if match and match.group(1) in VALID_ACTIONS:
            action = match.group(1)

        clean_reply = ACTION_TAG_RE.sub("", raw_reply).strip()
    except Exception:
        clean_reply = (
            f"Systems operational, Aadi. Gemini API error, "
            f"but MAX received your command: '{req.message}'"
        )

    return {
        "status": "success",
        "response": clean_reply,
        "action": action,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
