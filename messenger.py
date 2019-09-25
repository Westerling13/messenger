import threading
from datetime import datetime
from time import sleep

import requests
from PyQt5 import QtWidgets
from clientui import Ui_MainWindow


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)
        threading.Thread(target=self.refresh).start()

    def send(self):
        text = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()

        try:
            response = requests.post("http://127.0.0.1:5000/login", json={
                "username": username,
                "password": password
            })
            print(response.text)
            response = requests.post("http://127.0.0.1:5000/send", json={
                "username": username,
                "password": password,
                "text": text
            })
            print(response.text)
        except requests.exceptions.ConnectionError:
            print("Server is not available")
            return
        except:
            print("Some error")
            return

        self.lineEdit.setText('')
        self.lineEdit.repaint()

    def refresh(self):
        last_time = 0
        while True:
            try:
                response = requests.get("http://127.0.0.1:5000/messages",
                                        params={"after": last_time})
            except:
                print("Some error has occurred")
                sleep(1)
                continue

            for message in response.json()["messages"]:
                text = message["text"]
                time = message["time"]
                time_mask = "%H:%M:%S - %Y-%m-%d"
                time_formatted = datetime.fromtimestamp(time).strftime(time_mask)
                header = message["username"] + " в " + time_formatted

                self.textBrowser.append(header)
                self.textBrowser.append(text)
                self.textBrowser.append("")

                last_time = message["time"]

            sleep(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
