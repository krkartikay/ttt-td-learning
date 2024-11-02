from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("dashboard.html")  # Create a template with Plotly graphs


@app.route("/metrics")
def get_metrics():
    try:
        with open("metrics.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return {}


if __name__ == "__main__":
    app.run(debug=True)
