from flask import Flask, request, jsonify, send_from_directory
import json
import os
import time

app = Flask(__name__)

DATA_FILE = "data.json"

@app.route("/")
def root():
    return send_from_directory(".", "index.html")

@app.route("/data.json")
def data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return jsonify(json.load(f))
    else:
        return jsonify({"solar": 0, "battery": 0, "load": 0, "timestamp": None})

@app.route("/update", methods=["POST"])
def update_data():
    try:
        new_data = request.get_json(force=True)
        new_data["timestamp"] = time.time()
        with open(DATA_FILE, "w") as f:
            json.dump(new_data, f)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
