import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure your Gemini API Key securely via Render environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# In-memory storage for persistent session context (Upgrade 5)
conversation_history = [
    {
        "role": "model",
        "parts": [
            "Hello Aadi, I am MAX, your personal AI assistant. All systems, memory cores, and device telemetry links are active."
        ],
    }
]


@app.route("/process-command", methods=["POST"])
def process_command():
  try:
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
      return jsonify({"response": "Command stream empty."}), 400

    # Append user input to persistent context history
    conversation_history.append({"role": "user", "parts": [user_message]}

    # Start chat session with historical context
    chat = model.start_chat(history=conversation_history[:-1])
    response = chat.send_message(
        f"You are MAX, an advanced Iron Man-style AI assistant built for Aadi. Respond with a futuristic, concise, tactical tone. If the user asks to control a device (like opening apps, taking screenshots on PC, or managing mobile tools), acknowledge it with action codes like [PC_ACTION:NOTEPAD], [PC_ACTION:SCREENSHOT], or [PHONE_ACTION:NAVIGATE]. User command: {user_message}"
    )

    reply_text = response.text

    # Append model reply to history
    conversation_history.append({"role": "model", "parts": [reply_text]})

    # Detect actions for the client apps to execute locally
    action = "NONE"
    if "[PC_ACTION:NOTEPAD]" in reply_text or "open notepad" in user_message.lower():
      action = "OPEN_NOTEPAD"
    elif (
        "[PC_ACTION:SCREENSHOT]" in reply_text
        or "screenshot" in user_message.lower()
    ):
      action = "TAKE_SCREENSHOT"
    elif "[PHONE_ACTION" in reply_text or "phone" in user_message.lower():
      action = "PHONE_TASK"

    return jsonify({"response": reply_text, "action": action})

  except Exception as e:
    return jsonify({"response": f"Telemetry Error: {str(e)}"}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
