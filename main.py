import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure your Gemini API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Persistent Memory Bank
conversation_history = [{
    "role": "model",
    "parts": ["Hello Aadi, I am MAX. All systems, telemetry, and cross-device execution protocols are active."],
}]

@app.route("/process-command", methods=["POST"])
def process_command():
  try:
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
      return jsonify({"response": "Command stream empty."}), 400

    # Add user message to memory
    conversation_history.append({"role": "user", "parts": [user_message]})
    
    # Generate AI response
    chat = model.start_chat(history=conversation_history[:-1])
    response = chat.send_message(
        f"You are MAX, a highly advanced Iron Man-style AI assistant built for Aadi. Respond with a concise, tactical, and loyal tone. If the user asks to open Instagram, include [ACTION:INSTAGRAM]. For WhatsApp, include [ACTION:WHATSAPP]. For Notepad, include [ACTION:NOTEPAD]. User command: {user_message}"
    )

    reply_text = response.text
    conversation_history.append({"role": "model", "parts": [reply_text]})

    # Action Router
    action = "NONE"
    msg_lower = user_message.lower()
    if "instagram" in msg_lower or "[ACTION:INSTAGRAM]" in reply_text:
      action = "OPEN_INSTAGRAM"
    elif "whatsapp" in msg_lower or "[ACTION:WHATSAPP]" in reply_text:
      action = "OPEN_WHATSAPP"
    elif "notepad" in msg_lower or "[ACTION:NOTEPAD]" in reply_text:
      action = "OPEN_NOTEPAD"

    return jsonify({"response": reply_text, "action": action})
    
  except Exception as e:
    return jsonify({"response": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
