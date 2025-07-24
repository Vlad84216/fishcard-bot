import os
import openai
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка API-ключа
openai.api_key = os.environ["OPENAI_API_KEY"]

# ✅ Прокси OpenAI (добавлено)
openai.proxy = {
    "http": "http://ddemoipl:zkv01bcgs6pz@23.95.150.145:6114",
    "https": "http://ddemoipl:zkv01bcgs6pz@23.95.150.145:6114"
}

BOT_TOKEN = os.environ["BOT_TOKEN"]

async def estimate_fish_parameters(photo_path):
    with open(photo_path, "rb") as image_file:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Ты эксперт по рыбалке. На основе фото оцени вес и длину рыбы. Формат строго: Вес: ... кг\nДлина: ... см"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Оцени по фото примерный вес и длину рыбы. Ответ строго:\nВес: ... кг\nДлина: ... см"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=100
    )

    return response.choices[0].message.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне фото своей рыбы 🎣")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    await file.download_to_drive("fish.jpg")
    await update.message.reply_text("Фото получено! Анализирую...")

    try:
        gpt_reply = await estimate_fish_parameters("fish.jpg")
        await update.message.reply_text(f"🧠 GPT предполагает:\n{gpt_reply}\n\nХочешь изменить?")
    except Exception as e:
        await update.message.reply_text(f"Ошибка анализа фото: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == '__main__':
    main()
