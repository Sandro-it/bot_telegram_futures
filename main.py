import os
from dotenv import load_dotenv
from telethon import TelegramClient


# Завантаження змінних з .env
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# 📁 створення сесії, збережеться у файлі my_session.session
client = TelegramClient('my_session', api_id, api_hash)

async def main():
    await client.start()
    print("✅ Акаунт успішно авторизовано")

# 🚀 Запуск
with client:
    client.loop.run_until_complete(main())
