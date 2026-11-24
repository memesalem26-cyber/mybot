import telebot
import requests
from flask import Flask
import threading

TOKEN = "حط التوكن هنا"
GROQ_KEY = "حط الـ Key هنا"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت شغال!"

SYSTEM = """انت مساعد ذكي موسوعة، عندك معلومات في كل مجالات المجتمع البشري: طب، هندسة، دين، تاريخ، جغرافيا، علوم، رياضة، تكنولوجيا، برمجة، اقتصاد، قانون، علم نفس، فلسفة، فن، أدب، لغات، طبخ، زراعة، سياسة، وكل حاجة.
اشرح بالتفصيل خطوة خطوة، بالمصري البسيط، ادي أمثلة من الواقع، وقسم الشرح بعناوين ونقط."""

@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": message.text}],
                "temperature": 0.6,
                "max_tokens": 2000
            },
            timeout=60
        )
        text = r.json()["choices"][0]["message"]["content"]
        for i in range(0, len(text), 4000):
            if i == 0:
                bot.reply_to(message, text[i:i+4000])
            else:
                bot.send_message(message.chat.id, text[i:i+4000])
    except Exception as e:
        print("الغلط هو:", e)
        bot.reply_to(message, "معلش حصل مشكلة، جرب تاني")

threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
print("البوت شغال...")
bot.infinity_polling()