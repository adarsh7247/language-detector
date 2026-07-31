from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("my_own_language_model.joblib")

# Script pattern for languages
script_map = {
    "Hindi": r'[\u0900-\u097F]',
    "Arabic": r'[\u0600-\u06FF]',
    "Urdu": r'[\u0600-\u06FF]',
    "Korean": r'[\uAC00-\uD7AF]',
    "Tamil": r'[\u0B80-\u0BFF]',
    "Thai": r'[\u0E00-\u0E7F]'
}

def detect_script(text):
    for lang, pat in script_map.items():
        if re.search(pat, text):
            return lang
    return None


# Greeting whitelist (corrects short-text errors)
greet_map = {
    "hello": "English",
    "helloo": "English",
    "helo": "English",
    "hi": "English",
    "hii": "English",
    "hey": "English",

    "ok": "English",
    "okay": "English",
    "yes": "English",
    "no": "English",

    "name": "English",
    "myname": "English",
    "yourname": "English",

    "hola": "Spanish",
    "namaste": "Hindi",
    "salam": "Arabic",
}


# Final detection function
def detect_language(text):
    t = text.strip()

    # 1. Script-based detection
    lang = detect_script(t)
    if lang:
        return lang

    # 2. Greeting/short words override
    norm = re.sub(r'[^A-Za-z]', '', t.lower())
    if norm in greet_map:
        return greet_map[norm]

    # 3. Short-word fallback
    if len(t) <= 3:
        return "English"

    # 4. ML model prediction
    return model.predict([t])[0]


# API endpoint
@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = detect_language(text)

    return jsonify({"language": result})


@app.route("/", methods=["GET"])
def home():
    return "Language Detection API Running ✅"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5800, debug=True)
