from flask import Flask, request, jsonify, send_from_directory
import os
import json
import time

app = Flask(__name__, static_folder='.')

DATA_FILE = 'data.json'

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({
            "solar": 0,
            "battery": 0,
            "load": 0,
            "timestamp": time.time()
        }, f)

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/data.json", methods=["GET"])
def get_data():
    with open(DATA_FILE, 'r') as f:
        return jsonify(json.load(f))

@app.route("/update", methods=["POST"])
def update_data():
    try:
        new_data = request.get_json(force=True)
        new_data["timestamp"] = time.time()
        with open(DATA_FILE, 'w') as f:
            json.dump(new_data, f)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
