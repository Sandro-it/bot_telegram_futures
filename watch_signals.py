import os
import re
from dotenv import load_dotenv
from telethon import TelegramClient, events
from signal_handler import process_signal

# 🔐 Завантаження даних з .env
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# 📡 Telegram-клієнт
client = TelegramClient("my_session", api_id, api_hash)

# 👁 Канал, який слухаємо
channel = "https://t.me/trademansi0n"

@client.on(events.NewMessage(chats=channel))
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
