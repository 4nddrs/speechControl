import os
from flask import Flask, render_template, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pytz

app = Flask(__name__)

# 🔐 Inicializa Firebase con tus credenciales

# Leer y cargar el JSON desde la variable de entorno
cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
if not cred_json:
    raise ValueError("FIREBASE_CREDENTIALS_JSON no está configurada.")

credentials_dict = json.loads(cred_json)
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

# Inicializar Firestore
db = firestore.Client(credentials=credentials)

# 🌐 Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# 🔸 API para obtener los discursos
@app.route("/api/discursos")
def get_discursos():
    discursos_ref = db.collection("discursos")
    docs = discursos_ref.stream()

    data = []
    for doc in docs:
        d = doc.to_dict()

        # 🔁 Convertir fechas de historial a string legible (opcional)
        if "historial" in d and isinstance(d["historial"], list):
            for h in d["historial"]:
                if isinstance(h.get("fecha"), datetime):
                    h["fecha"] = h["fecha"].astimezone(pytz.UTC).strftime("%Y-%m-%d")

        data.append(d)

    data.sort(key=lambda x: x.get("id", 0))
    return jsonify(data)

# 🔹 API para guardar los discursos modificados
@app.route("/api/guardar", methods=["POST"])
def guardar_discursos():
    data = request.json

    for discurso in data:
        doc_id = str(discurso.get("id"))

        # 🔁 Convertir fecha string a datetime para Firestore
        if "historial" in discurso and isinstance(discurso["historial"], list):
            for h in discurso["historial"]:
                if isinstance(h.get("fecha"), str):
                    try:
                        h["fecha"] = datetime.strptime(h["fecha"], "%Y-%m-%d")
                    except ValueError:
                        continue

        db.collection("discursos").document(doc_id).set(discurso)

    return jsonify({"mensaje": "✅ Datos guardados correctamente en Firestore"})

# 🛠 PWA (opcional)
@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')

if __name__ == '__main__':
    app.run(debug=True)
