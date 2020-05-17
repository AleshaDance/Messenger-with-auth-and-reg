import threading
from datetime import datetime
from time import sleep

import requests
from PyQt5 import QtWidgets  # class widgets
from Qt import Ui_MainWindow  # импортирует Ui_MainWindow


class OurApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)      # нажатие -> def send
        self.pushButton_2.clicked.connect(self.login)   # нажатие -> def login
        self.pushButton_3.clicked.connect(self.reg)     # нажатие -> def reg
        threading.Thread(target=self.receive).start()

    # ФУНКЦИЯ АВТОРИЗАЦИИ
    def login(self):    # считывает с line edit`ов -> def send
        return self.lineEdit_2.text(), self.lineEdit_3.text()

    # ФУНКЦИЯ РЕГИСТРАЦИИ
    def reg(self):      # считывает с line edit`ов
        username, password = self.lineEdit_2.text(), self.lineEdit_3.text()
        if self.lineEdit_2.text() != '' and self.lineEdit_3.text() != '':
            try:
                response = requests.post('http://127.0.0.1:5000/reg',json={
                    'username': username,
                    'password': password
                })
            except:
                print('Какая-то ошибка произошла')
                return

    # ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЙ
    def send(self):
        text = self.lineEdit.text()
        username, password = self.login()   # авторазационные данные с line edit`ов
        if username != '' and password != '':   # if поля пустые: не работает кнопка
            try:    # отправляем на ../send адрес "пакет с данными"
                response = requests.post('http://127.0.0.1:5000/send', json={
                    'username': username,
                    'password': password,
                    'text': text
                })
                print(response.text)
            except requests.exceptions.ConnectionError:     # если не приходит ответ с сервера
                print('Сервер недоступен')
                return
            except:
                print('Какая-то ошибка произошла')          # неизвестная ошибка
                return
            self.lineEdit.setText('')       # текст в send исчезает
        self.lineEdit.repaint()     # перерисовывает и очищает поле

    # ПОЛУЧЕНИЕ СООБЩЕНИЙ
    def receive(self):
        last_time = 0   # для мониторинга за сообщениями
        while True:     # загружаем все сообщения из ../messages
            try:
                response = requests.get('http://127.0.0.1:5000/messages',
                                        params={'after': last_time})
            except:
                sleep(1)
                continue

            # СООБЩЕНИЯ ПОСЛЕ ОПРЕДЕЛЕННОЙ МЕТКИ (ОБНОВЛ-ЯЯ)
            for message in response.json()['messages']:  # выводит все сообщения
                time_format = datetime.fromtimestamp(message['time'])
                time_format = time_format.strftime('%Y-%m-%d %H:%M:%S')
                head = message['username'] + ' в ' + time_format
                text = message['text']

                # ДОБАВЛЯЕМ В txtBrowser ПРИНЯТЫЕ СООБЩЕНИЯ
                self.textBrowser.append(head)
                self.textBrowser.append(text)
                self.textBrowser.append('')

                last_time = message['time']
            sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = OurApp()
    window.show()
    app.exec_()