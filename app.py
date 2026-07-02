from flask import Flask, jsonify
import os
import psycopg2

from telemetry import configure_comprehend_telemetry

app = Flask(__name__)

configure_comprehend_telemetry("petstore-catalog", app=app)


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=os.environ.get("DB_PORT", "5432"),
    )


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/products")
def products():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, category, price, image_url
        FROM products
        ORDER BY id;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "price": float(row[3]),
            "image_url": row[4]
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)