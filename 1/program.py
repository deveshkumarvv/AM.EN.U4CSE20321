from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except requests.exceptions.RequestException:
        pass
    return []

@app.route("/numbers", methods=["GET"])
def get_numbers():
    urls = request.args.getlist("url")
    merged_numbers = []

    for url in urls:
        numbers = fetch_numbers(url)
        merged_numbers.extend(numbers)

    merged_numbers = list(set(merged_numbers))  # Deduplicate
    merged_numbers.sort()  # Sort in ascending order

    return jsonify({"numbers": merged_numbers})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008)
