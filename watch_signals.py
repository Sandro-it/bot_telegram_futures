import os
import re
from dotenv import load_dotenv
from telethon import TelegramClient, events
from signal_handler import process_signal

# 🔐 Завантаження даних з .env
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
# channel_username = os.getenv("TELEGRAM_CHANNEL")  # 👈 отримуємо канал

# 📋 Отримання назв каналів з .env
channels = [
    os.getenv("TELEGRAM_CHANNEL_1"),
    os.getenv("TELEGRAM_CHANNEL_2"),
]

# 📡 Telegram-клієнт
client = TelegramClient("my_session", api_id, api_hash)


@client.on(events.NewMessage(chats=channels))
async def handler(event):
    text = event.message.message
    print("\n📩 НОВЕ ПОВІДОМЛЕННЯ:")
    print(text[:300], "...")

    # Передаємо повідомлення у обробник
    process_signal(text)

# ▶️ Запуск бота
print("🕵️‍♂️ Очікую нові сигнали з Telegram...")
client.start()
client.run_until_disconnected()
