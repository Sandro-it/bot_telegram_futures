import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from signal_handler import process_signal

# 🧪 Тестовий сигнал (твх: 1700)
test_signal = """
ETH USDT Long 📈

🧠 Плечо: до 20
Соблюдаем риск менеджмент

💲 Вход: 1700
✅ Тейк: 1725
❌ Стоп: 1691
"""

process_signal(test_signal)
