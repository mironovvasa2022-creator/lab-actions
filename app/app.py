import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


@app.route("/health")
def health():
    return "OK"


@app.route("/api/data")
def data():
    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT id, name FROM items ORDER BY id")
        return jsonify([{"id": r[0], "name": r[1]} for r in cur.fetchall()])


@app.route("/api/items/count")
def count():
    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM items")
        return str(cur.fetchone()[0])


@app.route("/")
def index():
    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT name FROM items ORDER BY id")
        rows = "".join(f"<li>{r[0]}</li>" for r in cur.fetchall())
    return f"<meta charset='utf-8'><h1>Items</h1><ul>{rows}</ul>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("APP_PORT", 3000)))
