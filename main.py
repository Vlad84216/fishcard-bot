# фиктивный коммит для перезапуска деплоя
import asyncio

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
