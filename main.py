from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'side' not in data:
        return 'Missing or invalid data', 400

    side = data['side']
    print(f"Received signal: {side.upper()}")

    # Hier kannst du später deine Trading-Logik einfügen

    return jsonify({"status": "ok", "received": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

