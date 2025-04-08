import os
import time
import hmac
import base64
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

API_KEY = os.getenv("OKX_API_KEY")
SECRET_KEY = os.getenv("OKX_SECRET_KEY")
PASSPHRASE = os.getenv("OKX_PASSPHRASE")

BASE_URL = "https://www.okx.com"  # Замінимо на demo нижче
USE_DEMO = os.getenv("OKX_USE_DEMO") == "1"
if USE_DEMO:
    BASE_URL = "https://www.okx.com"  # demo API теж працює тут, важливий тільки demo account

def get_timestamp():
     return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def sign(message, secret):
    return base64.b64encode(
        hmac.new(secret.encode(), message.encode(), digestmod='sha256').digest()
    ).decode()

def get_headers():
    timestamp = get_timestamp()
    message = timestamp + 'GET' + '/api/v5/account/balance'
    signature = sign(message, SECRET_KEY)
    return {
        'OK-ACCESS-KEY': API_KEY,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': PASSPHRASE,
        'Content-Type': 'application/json'
    }

def get_balance():
    url = f"{BASE_URL}/api/v5/account/balance"
    response = requests.get(url, headers=get_headers())
    return response.json()

if __name__ == "__main__":
    result = get_balance()
    print(result)
