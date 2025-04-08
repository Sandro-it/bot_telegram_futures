import os
import pprint
from dotenv import load_dotenv
from okx import Trade  # <- ОНОВЛЕНО

# Завантаження змінних з .env
load_dotenv()

api_key = os.getenv("OKX_API_KEY")
secret_key = os.getenv("OKX_SECRET_KEY")
passphrase = os.getenv("OKX_PASSPHRASE")
flag = os.getenv("OKX_USE_DEMO", "1")  # 1 = demo, 0 = реальне

# Створення підключення
trade_api = Trade(api_key, secret_key, passphrase, flag=flag)

# Отримання списку відкритих ордерів
response = trade_api.get_order_list(instType="FUTURES", state="live")

pprint.pprint(response)
