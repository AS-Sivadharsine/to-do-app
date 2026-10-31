import json, os, re
from flask import Flask, jsonify, request, send_from_directory, abort

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
os.makedirs(DATA, exist_ok=True)
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024

def user_file(uid):
    if not re.fullmatch(r"[a-z0-9]{6,40}", uid):
        abort(400)
    return os.path.join(DATA, uid + ".json")

@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")

@app.get("/api/lists/<uid>")
def get_lists(uid):
    f = user_file(uid)
    if not os.path.exists(f):
        return jsonify([])
    with open(f, encoding="utf-8") as fh:
        return jsonify(json.load(fh))

@app.put("/api/lists/<uid>")
def put_lists(uid):
    with open(user_file(uid), "w", encoding="utf-8") as fh:
        json.dump(request.get_json(), fh)
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)), debug=True)