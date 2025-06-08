from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_SHEETS_API_KEY = "AIzaSyBx533BlZzo54lAcyh31nJW6UNeoXHaWfw"

@app.route("/fetch-sheet", methods=["POST"])
def fetch_sheet():
    data = request.json
    sheet_id = data.get("sheet_id")
    range_name = data.get("range", "Sayfa1!A1:Z1000")

    if not sheet_id:
        return jsonify({"error": "Sheet ID eksik"}), 400

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
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "GPT Sheets API",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "https://gpt-sheets-server-uq7w.onrender.com"
            }
        ],
        "paths": {
            "/fetch-sheet": {
                "post": {
                    "summary": "Google Sheets verisini getir",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "sheet_id": {
                                            "type": "string"
                                        },
                                        "range": {
                                            "type": "string"
                                        }
                                    },
                                    "required": ["sheet_id"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Başarılı yanıt"
                        }
                    }
                }
            }
        }
    })

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status": "ok",
        "message": "GPT Sheets sunucusu aktif."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
