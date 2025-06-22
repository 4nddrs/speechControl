from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path

app = Flask(__name__)
JSON_PATH = Path("static/discursos.json")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

@app.route("/api/discursos")
def get_discursos():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/api/guardar", methods=["POST"])
def guardar_discursos():
    data = request.json
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return jsonify({"mensaje": "Datos guardados correctamente"})

if __name__ == '__main__':
    app.run(debug=True)

