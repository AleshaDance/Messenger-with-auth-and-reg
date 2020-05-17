import time  # +
from flask import Flask, request

app = Flask(__name__)

messages = [  # список сообщений
    {'username': 'Alesha', 'time': time.time(), 'text': 'Qq'},
    {'username': 'Masha', 'time': time.time(), 'text': 'Hi'},
]

users = {  # словарь пользователей
    "Alesha": "qwerty",
    "Masha": "12345",
}


@app.route("/reg", methods=['POST'])
def registration():
    username = request.json["username"]
    password = request.json["password"]
    users[username] = password


@app.route("/messages")  # метод получения списка сообщений
def messages_view():
    after = float(request.args['after'])
    filtered_messages = []

    for message in messages:
        if message['time'] > after:
            filtered_messages.append(message)

    return {'messages': filtered_messages}


# метод отправки сообщений
@app.route("/send", methods=['POST'])  # принимаем только пост запросы
def send_view():
    username = request.json["username"]
    password = request.json["password"]
    text = request.json["text"]

    if username in users and users[username] == password and text != '':
        messages.append({'username': username, 'time': time.time(), 'text': text})
    elif username not in users or users[username] != password:
        messages.append({'username': "Jesus", 'time': time.time(), 'text': "Authorisation ERROR!"})


if __name__ == '__main__':
    app.run()

