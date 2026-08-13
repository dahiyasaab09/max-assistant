import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

conversation_history = [
    {
        "role": "model",
        "parts": [
            "Hello Aadi, I am MAX, your personal AI assistant. System permissions and telemetry cross-links are standing by."
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

    conversation_history.append({"role": "user", "parts": [user_message]})

    chat = model.start_chat(history=conversation_history[:-1])
    response = chat.send_message(
        f"You are MAX, an advanced Iron Man-style AI assistant built for Aadi. Respond with a tactical, concise tone. Classify the requested task into one of these actions if applicable: [PC_NOTEPAD], [PHONE_BROWSER], [PHONE_SETTINGS], or [NONE]. User command: {user_message}"
    )

    reply_text = response.text
    conversation_history.append({"role": "model", "parts": [reply_text]})

    # Detect action codes
    action = "NONE"
    msg_lower = user_message.lower()
    if "notepad" in msg_lower or "[pc_notepad]" in reply_text:
      action = "OPEN_NOTEPAD"
    elif "browser" in msg_lower or "google" in msg_lower or "search" in msg_lower or "[phone_browser]" in reply_text:
      action = "OPEN_BROWSER"
    elif "settings" in msg_lower or "setting" in msg_lower or "[phone_settings]" in reply_text:
      action = "OPEN_SETTINGS"

    return jsonify({"response": reply_text, "action": action})

  except Exception as e:
    return jsonify({"response": f"Telemetry Error: {str(e)}"}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
