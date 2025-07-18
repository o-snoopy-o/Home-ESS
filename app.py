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
    default_data = {
        "battery_voltage": 0.0,
        "battery_current": 0.0,
        "battery_power": 0.0,
        "grid_power": 0.0,
        "inverter1_power": 0.0,
        "inverter2_power": 0.0,
        "load_critical": 0.0,
        "load_house": 0.0,
        "load_workshop": 0.0,
        "timestamp": None
    }

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                existing_data = json.load(f)
            # Ensure all required keys are present in case of older files
            for key in default_data:
                existing_data.setdefault(key, default_data[key])
            return jsonify(existing_data)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify(default_data)

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
