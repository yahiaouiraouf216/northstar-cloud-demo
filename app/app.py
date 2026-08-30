"""
Petite application Flask — 2 pages dynamiques.
Objectif : servir de workload de test pour containerisation (Docker)
et déploiement (AWS EC2 via Terraform), avec CI GitHub Actions plus tard.
"""

import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")

# Compteur de visites en mémoire (remis à zéro à chaque redémarrage du process)
visit_count = 0


@app.route("/")
def index():
    return render_template(
        "index.html",
        hostname=socket.gethostname(),
        version=APP_VERSION,
        now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )


@app.route("/status")
def status():
    global visit_count
    visit_count += 1
    return render_template(
        "status.html",
        hostname=socket.gethostname(),
        visit_count=visit_count,
        now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "hostname": socket.gethostname()}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
