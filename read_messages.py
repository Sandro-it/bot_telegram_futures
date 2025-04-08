import os
import re
from dotenv import load_dotenv
from telethon import TelegramClient


# Завантаження змінних з .env
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    channel = 'https://t.me/trademansi0n'
    async for message in client.iter_messages(channel, limit=20):
        if not message.text:
            continue

        text = message.text
        print("\n📩 НОВЕ ПОВІДОМЛЕННЯ:")
        print(text[:200], "...")

        match_pair = re.search(r"([A-Z]{2,10})\s?\/?\s?(USDT|BTC)\s+(Long|Short)", text, re.IGNORECASE)
        if match_pair:
            print(f"🔸 Пара: {match_pair.group(1).upper()} / {match_pair.group(2).upper()}")
            print(f"🔸 Напрям: {match_pair.group(3).capitalize()}")

        match_leverage = re.search(r"Плечо\s*[:\-]?\s*до?\s*(\d+)", text, re.IGNORECASE)
        if match_leverage:
            print(f"🔸 Плече: x{match_leverage.group(1)}")

        match_entry = re.search(r"Точка входа\s*[:\-]?\s*([\d\.,]+)", text, re.IGNORECASE)
        if match_entry:
            print(f"🔸 Вхід: {match_entry.group(1).replace(',', '.')}")

with client:
    client.loop.run_until_complete(main())
