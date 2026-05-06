# ESP32 AI Voice Server for Railway

Bu server ESP32-C3 dan yuborilgan WAV audio faylni qabul qiladi, OpenAI Whisper orqali matnga aylantiradi, GPT javob yaratadi va JSON qaytaradi.

## Railway sozlash

1. Railway'da yangi project oching.
2. GitHub repo orqali deploy qiling yoki ZIP ichidagi fayllarni repo'ga joylang.
3. Railway → Variables bo'limida quyidagini qo'shing:

```text
OPENAI_API_KEY=sk-...
```

4. Deploy tugagach, link olinadi:

```text
https://your-project.up.railway.app
```

ESP32 kodida endpoint shunday bo'ladi:

```text
https://your-project.up.railway.app/voice
```

## Test

Brauzerda oching:

```text
https://your-project.up.railway.app/health
```

Natija:

```json
{"status":"ok"}
```

## API

POST `/voice`

Body: WAV audio bytes

Response:

```json
{
  "text": "foydalanuvchi gapi",
  "answer": "AI javobi"
}
```
