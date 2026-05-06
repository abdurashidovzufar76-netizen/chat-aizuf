import os
import tempfile
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "ESP32 Voice AI Server is working!"

@app.route("/voice", methods=["POST"])
def voice():
    try:
        audio_bytes = request.get_data()
        if not audio_bytes:
            return jsonify({"error": "No audio data received"}), 400

        # ESP32 sends WAV bytes. Save as temporary WAV file for Whisper.

        audio_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_bytes)
                audio_path = tmp.name

            with open(audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="uz"
                )

            user_text = transcript.text.strip()
            if not user_text:
                user_text = "Foydalanuvchi ovozi tushunilmadi."

            chat = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "Sen ESP32 TFT ekranida ishlaydigan qisqa, aniq va o'zbekcha javob beradigan AI assistentsan. Javobni 2-4 qatorda, juda uzun qilma."
                    },
                    {"role": "user", "content": user_text}
                ],
                max_tokens=180
            )

            answer = chat.choices[0].message.content.strip()
            return jsonify({"text": user_text, "answer": answer})
        finally:
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception:
                    pass

    except Exception as e:
        return jsonify({"error": "Ichki server xatosi yuz berdi."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
