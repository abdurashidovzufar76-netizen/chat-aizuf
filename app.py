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
    return "ESP32 AI Voice Server is running"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/voice", methods=["POST"])
def voice():
    audio_data = request.data

    if not audio_data:
        return jsonify({"error": "No audio data received"}), 400

    audio_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_file:
            audio_file.write(audio_data)
            audio_path = audio_file.name

        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        user_text = transcript.text.strip()

        if not user_text:
            return jsonify({
                "text": "",
                "answer": "Ovoz tushunilmadi. Iltimos, qayta gapiring."
            })

        chat_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sen ESP32 TFT ekrani uchun qisqa, aniq va o'zbekcha javob beradigan AI assistantsan. Javoblarni 2-4 qatordan oshirma."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        answer = chat_response.choices[0].message.content.strip()

        return jsonify({
            "text": user_text,
            "answer": answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if audio_path:
            try:
                os.remove(audio_path)
            except Exception:
                pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
