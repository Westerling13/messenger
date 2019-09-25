import time
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)
messages = [
    # {"username": "Jack", "time":  time.time(), "text": "Hello"},
    # {"username": "Mary", "time":  time.time(), "text": "Hi, Jack"}
]
users = {
    # username: password
    "Jack": "Black",
    "Mary": "12345"
}


@app.route("/")
def hello():
    return "Hello"


@app.route("/status")
def status():
    return {
        "status": True,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages_count": len(messages),
        "users_count": len(users)
    }


@app.route("/messages")
def messages_view():
    """
    :input: ?after=float
    :return: [{"username": str, "time": float, "text': str}, ...]
    """
    # print(request.args)
    after = float(request.args["after"])

    filtered_messages = []
    for message in messages:
        if message["time"] > after:
            filtered_messages.append(message)

    return {"messages": filtered_messages}


@app.route("/send", methods=["POST"])
def send_view():
    """
    Отправить сообщение всем
    :input: {"username": str, "password": str, "text": str}
    :return: {"ok": bool}
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]
    text = request.json["text"]

    if username not in users or users[username] != password:
        return {"ok": False}

    messages.append({"username": username, "time":  time.time(), "text": text})
    return {"ok": True}


@app.route("/login", methods=["POST"])
def login_view():
    """
    Отправить сообщение всем
    input: {"username": str, "password": str}
    :return: {"ok": bool}
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]

    if username not in users:
        users[username] = password
        return {"ok": True}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}


if __name__ == "__main__":
    app.run()
