from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Deine Capital.com Zugangsdaten
CAPITAL_API_KEY      = "elvswWKiE4RmZ4Mt"
CAPITAL_API_PASSWORD = "Daisy1234!"

BASE_URL = "https://api-capital.backend-capital.com"

HEADERS = {
    "X-CAP-API-KEY": CAPITAL_API_KEY,
    "Content-Type": "application/json"
}

def place_market_order(symbol, side, size):
    url = f"{BASE_URL}/positions"
    payload = {
        "market": symbol,
        "direction": side.upper(),  # "BUY" oder "SELL"
        "size": size,
        "orderType": "MARKET",
        "currencyCode": "USD",
        "forceOpen": True
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    return resp.json()

@app.route('/', methods=['GET'])
def home():
    return 'Capital.com Webhook Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'side' not in data or 'symbol' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    side   = data['side']
    symbol = data['symbol']
    size   = data.get('size', 1)

    if side.lower() not in ['buy', 'sell']:
        return jsonify({'error': 'Invalid side, must be buy or sell'}), 400

    result = place_market_order(symbol, side, size)
    print("Order response:", result)
    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

