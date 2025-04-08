import re
from trade_utils import calculate_trade_levels, should_enter_trade
from okx_trader import (
    get_current_price,
    open_market_position,
    set_tp_sl,
)

def process_signal(signal_text):
    try:
        print(f"🔍 Сигнал:\n{signal_text}")

        # 📌 Парсинг тексту
        pair_match = re.search(r'([A-Z]+)[-/ ]?USDT', signal_text, re.IGNORECASE)
        direction = 'SHORT' if 'SHORT' in signal_text.upper() else 'LONG'
        entry_match = re.search(r'(точка входа|вход)[:\s]*([\d.]+)', signal_text, re.IGNORECASE)

        if not pair_match or not entry_match:
            print("⚠️ Не вдалося витягнути інформацію із сигналу.")
            return

        pair = pair_match.group(1).upper()
        entry_price = float(entry_match.group(2))
        symbol = f"{pair}-USDT-SWAP"

        print(f"📈 Пара: {symbol} | Напрям: {direction} | ТВХ: {entry_price}")

        # 🔍 Поточна ціна
        current_price = get_current_price(symbol)
        if not should_enter_trade(entry_price, current_price):
            print("⛔ Ціна змінилась більше ніж на 1% — не входимо в угоду.")
            return

        # 🔢 Розрахунок рівнів
        levels = calculate_trade_levels(
            entry_price=entry_price,
            leverage=20,
            position_usdt=30,
            risk_usdt=3
        )

        print("📊 Рівні розраховані:")
        print(f"Стоп: {levels['stop_price']}")
        print(f"TP1 (25%): {levels['tp1_price']}")
        print(f"TP повний: {levels['take_profit_price']}")
        print(f"Б/у з комісією: {levels['break_even_price']}")

        # 💰 Відкриття позиції
        side = "buy" if direction == "LONG" else "sell"
        margin = round(30 / entry_price, 3)

        open_market_position(symbol, side=side, margin=margin, leverage=20)

        # 🎯 Встановлення тейку і стопу
        set_tp_sl(symbol, tp_price=levels["take_profit_price"], sl_price=levels["stop_price"], side=side)

        print("✅ Угода повністю оброблена")

    except Exception as e:
        print(f"❌ Помилка при обробці сигналу: {e}")
