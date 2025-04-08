import re

# 🧪 Сюди вставляй тестовий сигнал з Telegram
text = """
KAVA USDT Long 📈

🧠 Плечо: до 25
Соблюдаем риск менеджмент

💲 Точка входа: 0,4104 - 0,3780
✅ Тейк: 0,4433
❌ Стоп: 0,3730 (смотря откуда вы заходили)
"""

print("\n📩 ТЕСТОВЕ ПОВІДОМЛЕННЯ:")
print(text.strip())

match_pair = re.search(r"([A-Z]{2,10})\s*\/?\s*(USDT|BTC)\s+(Long|Short)", text, re.IGNORECASE)
match_leverage = re.search(r"Плечо\s*[:\-]?\s*до?\s*(\d+)", text, re.IGNORECASE)
match_entry = re.search(r"Точка входа\s*[:\-]?\s*([\d\.,]+)", text, re.IGNORECASE)

if match_pair:
    pair = f"{match_pair.group(1).upper()}/{match_pair.group(2).upper()}"
    direction = match_pair.group(3).capitalize()
    leverage = f"x{match_leverage.group(1)}" if match_leverage else "???"
    entry = match_entry.group(1).replace(",", ".") if match_entry else "???"

    print("\n✅ Імітація відкриття ордера:")
    print(f"➡ Пара: {pair}")
    print(f"➡ Напрям: {direction}")
    print(f"➡ Плече: {leverage}")
    print(f"➡ Точка входу: {entry}")
    print("🚧 (Тут буде реальний запит на OKX API)")
else:
    print("⚠️ Сигнал не розпізнано.")
