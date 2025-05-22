from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("CAPITAL_API_KEY")
BASE_URL = "https://api-capital.backend-capital.com"

HEADERS = {
    "X-CAP-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def place_market_order(symbol, direction, size):
    url = f"{BASE_URL}/positions"
    payload = {
        "market": symbol,
        "direction": direction.upper(),
        "size": size,
        "orderType": "MARKET",
        "currencyCode": "USD",
        "forceOpen": True
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook empfangen:", data)
    
    symbol = data.get("symbol")
    action = data.get("action")
    size = data.get("size", 1)
    
    if not symbol or not action:
        return jsonify({"error": "symbol und action sind erforderlich"}), 400

    result = place_market_order(symbol, action, size)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

