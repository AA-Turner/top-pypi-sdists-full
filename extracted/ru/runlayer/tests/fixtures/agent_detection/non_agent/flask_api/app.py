"""A plain Flask CRUD API — not an AI agent (zero-false-positive fixture)."""

import os

from flask import Flask, jsonify, request

app = Flask(__name__)
_ITEMS: dict[int, dict] = {}


@app.route("/health")
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@app.route("/items", methods=["GET", "POST"])
def items():
    if request.method == "POST":
        payload = request.get_json(force=True)
        item_id = len(_ITEMS) + 1
        _ITEMS[item_id] = {"id": item_id, **payload}
        return jsonify(_ITEMS[item_id]), 201
    return jsonify(list(_ITEMS.values())), 200


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
