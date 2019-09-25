import requests

response = requests.get("http://127.0.0.1:5000/status")
print(response.json())

username = input("Say your name: ")
password = input("Password, please: ")

login_data = {"username": username, "password": password}

print(response.json())

while True:
    text = input()
    data = {"username": username, "password": password, "text": text}
    requests.post("http://127.0.0.1:5000/login", json=login_data)
    response = requests.post("http://127.0.0.1:5000/send", json=data)
    print(response.json())
