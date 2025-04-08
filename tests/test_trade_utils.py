from trade_utils import calculate_trade_levels, should_enter_trade

# Дані для тесту
entry_price = 1700         # Ціна входу
leverage = 20              # Плече
position_usdt = 30         # Сума входу
risk_usdt = 3              # Ризик 3 USDT (1% від депо)

# Розрахунок рівнів
levels = calculate_trade_levels(entry_price, leverage, position_usdt, risk_usdt)

print("📊 Результати розрахунку рівнів:")
print(f"Вхід: {levels['entry_price']} USDT")
print(f"Стоп: {levels['stop_price']} USDT")
print(f"Тейк №1 (25% прибутку): {levels['tp1_price']} USDT")
print(f"Тейк повний (+1.5% ціни): {levels['take_profit_price']} USDT")
print(f"Б/у з комісією: {levels['break_even_price']} USDT")

# Перевірка допуску до угоди
signal_price = 1700
actual_price_good = 1710     # +0.59% — в межах
actual_price_bad = 1725      # +1.47% — за межами

print("\n🎯 Перевірка допуску за відхиленням:")
print(f"1710 vs 1700 ➡ {should_enter_trade(signal_price, actual_price_good)}")  # True
print(f"1725 vs 1700 ➡ {should_enter_trade(signal_price, actual_price_bad)}")   # False
