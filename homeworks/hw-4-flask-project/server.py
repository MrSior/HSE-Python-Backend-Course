from flask import Flask, jsonify, request
from dotenv import dotenv_values
from controllers import operation

app = Flask(__name__)


@app.route("/")
def server_info():
    return "My server"


@app.route("/author")
def author():
    serverAuthor = {
        "name": "Simon",
        "course": 2,
        "age": 19,
        "favorite food": "lasagna",
    }
    return jsonify(serverAuthor)

@app.route("/sum")
def runner():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    return jsonify({'sum': operation(a, b)})

def get_port() -> int:
    config = dotenv_values(".env")
    if "PORT" in config:
        return config["PORT"]
    return 5000


def is_debug() -> bool:
    config = dotenv_values(".env")
    if "DEBUG" in config:
        return config["DEBUG"]
    return True


if __name__ == "__main__":
    app.run(debug=is_debug(), port=get_port())
