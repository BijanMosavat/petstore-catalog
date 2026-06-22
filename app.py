from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/products")
def products():
    return jsonify([
        {
            "id": 1,
            "name": "Dog Food",
            "price": 19.99
        },
        {
            "id": 2,
            "name": "Cat Toy",
            "price": 9.99
        }
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)