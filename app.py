import os
import requests
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app) # Compliant

PROXMOX_HOST = os.environ.get("PROXMOX_HOST", "localhost")
PROXMOX_NODE = os.environ.get("PROXMOX_NODE", "pve")
PROXMOX_PORT = os.environ.get("PROXMOX_PORT", 8006)
VMID = os.environ.get("PROXMOX_VMID")
API_TOKEN_ID = os.environ.get("PROXMOX_TOKEN_ID")
API_TOKEN_SECRET = os.environ.get("PROXMOX_TOKEN_SECRET")

BASE = f"https://{PROXMOX_HOST}:8006/api2/json"

HEADERS = {
    "Authorization": f"PVEAPIToken={API_TOKEN_ID}={API_TOKEN_SECRET}"
}


def proxmox_get(path):
    r = requests.get(
        f"{BASE}{path}",
        headers=HEADERS,
    )
    r.raise_for_status()
    return r.json()["data"]


def proxmox_post(path):
    r = requests.post(
        f"{BASE}{path}",
        headers=HEADERS,
        timeout=5
    )
    r.raise_for_status()
    return r.json()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/status", methods=["GET"])
def status():
    data = proxmox_get(f"/nodes/{PROXMOX_NODE}/qemu/{VMID}/status/current")
    return jsonify({"status": data["status"]})


@app.route("/start", methods=["POST"])
def start():
    proxmox_post(f"/nodes/{PROXMOX_NODE}/qemu/{VMID}/status/start")
    return jsonify({"ok": True})


@app.route("/stop", methods=["POST"])
def stop():
    proxmox_post(f"/nodes/{PROXMOX_NODE}/qemu/{VMID}/status/stop")
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
