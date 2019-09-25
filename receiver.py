from time import sleep

import requests

response = requests.get("http://127.0.0.1:5000/status")
print(response.json())

last_time = 0

while True:
    response = requests.get("http://127.0.0.1:5000/messages",
                            params={"after": last_time})

    for message in response.json()["messages"]:
        print(message)
        last_time = message["time"]

    sleep(1)
