def calculate_trade_levels(entry_price, leverage, position_usdt, risk_usdt, take_profit_percent=1.5, tp1_ratio=0.25, fee_percent=0.1):
    """
    Розрахунок рівнів тейку, стопа, проміжного тейку та б/у.
    Всі розрахунки базуються на відсотковому зростанні ціни, а не фіксованому прибутку.
    """

    # Повний тейк — зростання ціни на take_profit_percent
    take_profit_price = entry_price * (1 + take_profit_percent / 100)

    # Обсяг позиції з урахуванням плеча
    position_value = position_usdt * leverage

    # Стоп — втрати risk_usdt
    stop_percent = risk_usdt / position_value
    stop_price = entry_price * (1 - stop_percent)

    # Тейк №1 — фіксація частини прибутку (наприклад, 25%)
    total_profit = (take_profit_price - entry_price) * position_value / entry_price
    tp1_usdt = total_profit * tp1_ratio
    tp1_percent = tp1_usdt / position_value
    tp1_price = entry_price * (1 + tp1_percent)

    # Стоп у б/у з урахуванням подвійної комісії (на вхід і вихід)
    break_even_price = entry_price * (1 + (fee_percent / 100))

    return {
        "entry_price": round(entry_price, 2),
        "take_profit_price": round(take_profit_price, 2),
        "stop_price": round(stop_price, 2),
        "tp1_price": round(tp1_price, 2),
        "break_even_price": round(break_even_price, 2)
    }


def should_enter_trade(signal_price, actual_price, max_deviation_percent=1.0):
    """
    Перевіряє, чи можна входити в угоду, виходячи з поточної ринкової ціни.
    Повертає True, якщо відхилення не перевищує max_deviation_percent.
    """
    deviation = abs(actual_price - signal_price) / signal_price * 100
    return deviation <= max_deviation_percent
