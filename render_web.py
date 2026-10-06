"""Minimal HTTP server for Render Web Service compatibility.

The Telegram music bot is still the main process. This Flask app only exposes
an HTTP endpoint so Render can route traffic to the service.
"""

import os
from flask import Flask, jsonify

web_app = Flask(__name__)


@web_app.get("/")
def index():
    return "VenomMusic is running."


@web_app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "VenomMusic"}), 200


def run_web_server():
    port = int(os.environ.get("PORT", "10000"))
    # Render requires the web service to bind to 0.0.0.0.
    web_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
