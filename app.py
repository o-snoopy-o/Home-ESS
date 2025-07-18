from flask import Flask, send_from_directory, jsonify
import os
import json

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/data.json')
def data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # use 10000 by default or $PORT from environment
    app.run(host='0.0.0.0', port=port)
