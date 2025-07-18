from flask import Flask, request, jsonify
import time

app = Flask(__name__)

power_data = {
    "solar": 0,
    "battery": 0,
    "load": 0,
    "timestamp": time.time()
}

@app.route("/data.json", methods=["GET"])
def get_data():
    return jsonify(power_data)

@app.route("/update", methods=["POST"])
def update_data():
    global power_data
    try:
        new_data = request.get_json(force=True)
        power_data = {**new_data, "timestamp": time.time()}
        return jsonify({"status": "ok", "received": power_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def root():
    return "✅ ESS Power Flow Server is running"
