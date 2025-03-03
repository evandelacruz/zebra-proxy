from flask import Flask, request, jsonify
import usb_handler
import json
import os

app = Flask(__name__)

CONFIG_FILE = "config.json"
config = {}

def load_config():
    global config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                if not isinstance(config, dict):  # Ensure valid dict format
                    config = {}
        except (json.JSONDecodeError, IOError):
            config = {}  # Handle corrupted file gracefully
    else:
        config = {}

def save_config():
    temp_file = CONFIG_FILE + ".tmp"
    try:
        with open(temp_file, "w") as f:
            json.dump(config, f, indent=2)
        os.replace(temp_file, CONFIG_FILE)  # Atomic rename ensures valid config
    except IOError as e:
        print(f"Failed to save config: {e}")

# Load config once on startup
load_config()

@app.route("/printers", methods=["GET"])
def list_printers():
    printers = usb_handler.get_printers()
    
    if isinstance(printers, dict) and "error" in printers:
        return jsonify(printers), 500  # Return the error message properly

    return jsonify(printers)

@app.route("/printers/default", methods=["GET", "POST"])
def default_printer():
    if request.method == "POST":
        printer_id = request.json.get("id")
        if printer_id:
            config["default_printer"] = printer_id
            save_config()
    return jsonify({"default_printer": config.get("default_printer", "")})

@app.route("/print", methods=["POST"])
def print_zpl():
    data = request.json
    printer_id = data.get("printer_id") or config.get("default_printer")
    if not printer_id:
        printers = usb_handler.get_printers()
        if printers:
            printer_id = printers[0]["id"]
            config["default_printer"] = printer_id
            save_config()
    if not printer_id:
        return jsonify({"error": "No default printer available"}), 400

    success = usb_handler.send_zpl(printer_id, data["zpl"])
    return jsonify({"status": "sent" if success else "failed"}), (200 if success else 500)

@app.route("/status", methods=["GET"])
def printer_status():
    printer_id = request.args.get("printer_id") or config.get("default_printer")
    if not printer_id:
        return jsonify({"connected": False, "status": "No default printer"}), 400
    return jsonify(usb_handler.get_status(printer_id))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
