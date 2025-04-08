import os
import time
import base64
import hmac
import hashlib
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Авторизація
API_KEY = os.getenv("OKX_API_KEY")
API_SECRET = os.getenv("OKX_SECRET_KEY")
API_PASSPHRASE = os.getenv("OKX_PASSPHRASE")

BASE_URL = "https://www.okx.com"

# 🧾 Підпис запиту OKX API
def generate_signature(timestamp, method, request_path, body=""):
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    mac = hmac.new(
        API_SECRET.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256,
    )
    d = mac.digest()
    return base64.b64encode(d).decode("utf-8")

# 🌐 Заголовки запиту
def get_headers(method, path, body=""):
    timestamp = str(time.time())
    sign = generate_signature(timestamp, method, path, body)
    return {
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": sign,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json",
    }

# 📊 Поточна ринкова ціна
def get_current_price(symbol: str) -> float:
    try:
        url = f"{BASE_URL}/api/v5/market/ticker?instId={symbol}"
        response = requests.get(url)
        data = response.json()
        last_price = float(data["data"][0]["last"])
        print(f"📊 Поточна ціна {symbol}: {last_price}")
        return last_price
    except Exception as e:
        print(f"❌ Помилка при отриманні ціни {symbol}: {e}")
        return 0.0

# ✅ Перевірка допустимого відхилення
def is_entry_price_valid(signal_price: float, market_price: float, max_diff_percent: float = 1.0) -> bool:
    diff = abs(signal_price - market_price)
    diff_percent = (diff / signal_price) * 100
    print(f"📏 Відхилення: {diff_percent:.2f}% (макс. {max_diff_percent}%)")
    return diff_percent <= max_diff_percent

# 💰 Реальне відкриття ринкової позиції
def open_market_position(symbol: str, side: str, margin: float, leverage: int):
    try:
        # 🔧 Встановити плече
        leverage_url = "/api/v5/account/set-leverage"
        leverage_body = json.dumps({
            "instId": symbol,
            "lever": str(leverage),
            "mgnMode": "isolated"
        })
        leverage_headers = get_headers("POST", leverage_url, leverage_body)
        res_lev = requests.post(BASE_URL + leverage_url, headers=leverage_headers, data=leverage_body)
        print("📐 Плече встановлено:", res_lev.json())

        # 📤 Відкрити позицію
        order_url = "/api/v5/trade/order"
        order_body = json.dumps({
            "instId": symbol,
            "tdMode": "isolated",
            "side": side,
            "ordType": "market",
            "sz": str(margin)
        })
        order_headers = get_headers("POST", order_url, order_body)
        res_order = requests.post(BASE_URL + order_url, headers=order_headers, data=order_body)
        print("✅ Позиція відкрита:", res_order.json())
        return res_order.json()
    except Exception as e:
        print(f"❌ Помилка відкриття позиції: {e}")
        return None

# 🎯 Заглушка — TP/SL поки що не реалізована
def set_tp_sl(symbol: str, tp_price: float, sl_price: float, side: str):
    print(f"🎯 Імітація встановлення TP/SL для {symbol} | TP: {tp_price} | SL: {sl_price} | Сторона: {side}")


# =================================================================================================================================

# import os
# import time
# import hmac
# import hashlib
# import base64
# import json
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("OKX_API_KEY")
# API_SECRET = os.getenv("OKX_SECRET_KEY")
# API_PASSPHRASE = os.getenv("OKX_PASSPHRASE")
# BASE_URL = "https://www.okx.com"

# # 🧾 Генерація підпису HMAC SHA256
# def generate_signature(timestamp, method, request_path, body=""):
#     message = f"{timestamp}{method.upper()}{request_path}{body}"
#     mac = hmac.new(
#         API_SECRET.encode("utf-8"),
#         msg=message.encode("utf-8"),
#         digestmod=hashlib.sha256
#     )
#     return base64.b64encode(mac.digest()).decode()

# # 🏷️ Заголовки з підписом
# def get_headers(method, request_path, body=""):
#     timestamp = str(time.time())
#     sign = generate_signature(timestamp, method, request_path, body)
#     return {
#         "OK-ACCESS-KEY": API_KEY,
#         "OK-ACCESS-SIGN": sign,
#         "OK-ACCESS-TIMESTAMP": timestamp,
#         "OK-ACCESS-PASSPHRASE": API_PASSPHRASE,
#         "Content-Type": "application/json"
#     }

# # 📊 Поточна ринкова ціна
# def get_current_price(symbol: str) -> float:
#     try:
#         url = f"{BASE_URL}/api/v5/market/ticker?instId={symbol}"
#         response = requests.get(url)
#         data = response.json()
#         last_price = float(data["data"][0]["last"])
#         print(f"📊 Поточна ціна {symbol}: {last_price}")
#         return last_price
#     except Exception as e:
#         print(f"❌ Помилка при отриманні ціни {symbol}: {e}")
#         return 0.0

# # 📏 Перевірка допустимого відхилення
# def is_entry_price_valid(signal_price: float, market_price: float, max_diff_percent: float = 1.0) -> bool:
#     diff = abs(signal_price - market_price)
#     diff_percent = (diff / signal_price) * 100
#     print(f"📏 Відхилення: {diff_percent:.2f}% (макс. {max_diff_percent}%)")
#     return diff_percent <= max_diff_percent

# # 💰 Відкриття позиції
# def open_market_position(symbol: str, side: str, margin: float, leverage: int):
#     try:
#         # 1. Встановити плече
#         leverage_body = json.dumps({
#             "instId": symbol,
#             "lever": str(leverage),
#             "mgnMode": "isolated"
#         })
#         leverage_headers = get_headers("POST", "/api/v5/account/set-leverage", leverage_body)
#         leverage_response = requests.post(
#             f"{BASE_URL}/api/v5/account/set-leverage",
#             headers=leverage_headers,
#             data=leverage_body
#         )
#         print("🔧 Встановлення плеча:", leverage_response.json())

#         # 2. Відкрити ринкову позицію
#         order_body = json.dumps({
#             "instId": symbol,
#             "tdMode": "isolated",
#             "side": side,  # buy / sell
#             "ordType": "market",
#             "sz": str(margin)
#         })
#         order_headers = get_headers("POST", "/api/v5/trade/order", order_body)
#         order_response = requests.post(
#             f"{BASE_URL}/api/v5/trade/order",
#             headers=order_headers,
#             data=order_body
#         )
#         print("📥 Відповідь на відкриття позиції:", order_response.json())
#         return order_response.json()
#     except Exception as e:
#         print(f"❌ Помилка відкриття позиції: {e}")
#         return None

# # 🎯 TP/SL (поки залишимо як імітацію або додамо пізніше)
# def set_tp_sl(symbol: str, tp_price: float, sl_price: float, side: str):
#     print(f"🎯 Імітація TP/SL | TP: {tp_price} | SL: {sl_price} | Side: {side}")

