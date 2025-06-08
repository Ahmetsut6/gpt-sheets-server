from flask import Flask, request, Response, jsonify
import requests
import os
import json

app = Flask(__name__)

# Ortam değişkeninden API key'i al
GOOGLE_SHEETS_API_KEY = os.environ.get("GOOGLE_API_KEY")

@app.route("/fetch-sheet", methods=["POST"])
def fetch_sheet():
    data = request.json
    sheet_id = data.get("sheet_id")
    range_name = data.get("range", "Sayfa1!A1:Z1000")

    if not sheet_id:
        return jsonify({"error": "Sheet ID eksik"}), 400

    if not GOOGLE_SHEETS_API_KEY:
        return jsonify({"error": "API key tanımlı değil"}), 500

    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?key={GOOGLE_SHEETS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({
            "error": "Veri çekilemedi",
            "details": response.text
        }), 500

    return jsonify(response.json())

@app.route("/openapi.json", methods=["GET"])
def openapi_spec():
    with open("openapi.json", "r") as f:
        content = f.read()
    return Response(content, mimetype="application/json")

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status": "ok",
        "message": "GPT Sheets sunucusu çalışıyor."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
