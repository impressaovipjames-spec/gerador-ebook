#!/usr/bin/env python3
import os
import json
import hashlib
import time
from flask import Flask, jsonify, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEITOR_DIR = os.path.join(BASE_DIR, "app", "leitor")
EXPORTS_DIR = os.path.join(BASE_DIR, "app", "exports")

app = Flask(__name__, static_folder=LEITOR_DIR, static_url_path="")

# === ROTA PRINCIPAL (interface do leitor) ===
@app.route("/")
def home():
    index_path = os.path.join(LEITOR_DIR, "ebook_reader.html")
    if os.path.exists(index_path):
        return send_from_directory(LEITOR_DIR, "ebook_reader.html")
    else:
        return "<h2>Arquivo ebook_reader.html não encontrado.</h2>", 404

# === ARQUIVOS ESTÁTICOS (css, js, imagens) ===
@app.route("/assets/<path:path>")
def assets(path):
    return send_from_directory(os.path.join(LEITOR_DIR, "assets"), path)

# === EXPORTS ===
@app.route("/exports/<path:filename>")
def exports(filename):
    return send_from_directory(EXPORTS_DIR, filename)

# === HEALTH CHECK ===
@app.route("/api/health")
def api_health():
    response = {
        "ok": True,
        "environment": "production",
        "online_mode": True,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "1.0.0"
    }
    return jsonify(response)

# === EXPORTS LIST ===
@app.route("/api/exports")
def api_exports():
    files = []
    if os.path.exists(EXPORTS_DIR):
        for filename in os.listdir(EXPORTS_DIR):
            filepath = os.path.join(EXPORTS_DIR, filename)
            if os.path.isfile(filepath):
                with open(filepath, "rb") as f:
                    sha256 = hashlib.sha256(f.read()).hexdigest()
                files.append({
                    "name": filename,
                    "size": os.path.getsize(filepath),
                    "checksum": sha256,
                    "url": f"/exports/{filename}"
                })
    return jsonify({"count": len(files), "files": files})

# === ADMIN (placeholder) ===
@app.route("/admin")
def admin():
    return "<h1>Painel Administrativo</h1><p>Em breve...</p>"

# === LEITOR (rota direta) ===
@app.route("/leitor")
def leitor():
    return send_from_directory(LEITOR_DIR, "ebook_reader.html")

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
