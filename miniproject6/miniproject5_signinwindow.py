import re
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt6.QtGui import QFont
from miniproject5 import MWindow
import funcs
import hashlib


class SignInWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Вход")
        self.main_window = main_window
        self.main_window.close()
        self.login = None

        ## Заголовок
        self.name_label = QLabel('Вход', self)
        self.name_label.move(140, 20)
        self.name_label.setFixedSize(250, 30)
        self.font1 = QFont('Arial', 16)
        self.font1.setBold(True)
        self.name_label.setFont(self.font1)

        ## Логин
        self.login_label = QLabel('Введите логин:', self)
        self.login_label.move(50, 70)
        self.login_label.setFixedSize(300, 30)
        self.font2 = QFont('Arial', 12)
        self.login_label.setFont(self.font2)

        self.login_line = QLineEdit(self)
        self.login_line.move(50, 100)
        self.login_line.setFixedSize(300, 30)

        ## Пароль
        self.pass_label = QLabel('Введите пароль:', self)
        self.pass_label.move(50, 140)
        self.pass_label.setFixedSize(300, 30)
        self.pass_label.setFont(self.font2)

        self.pass_line = QLineEdit(self)
        self.pass_line.move(50, 170)
        self.pass_line.setFixedSize(300, 30)
        self.pass_line.setEchoMode(QLineEdit.EchoMode.Password)

        ## Кнопка входа
        self.sign_in_btn = QPushButton('Войти', self)
        self.sign_in_btn.setFixedSize(150, 40)
        self.sign_in_btn.move(125, 220)
        self.sign_in_btn.clicked.connect(self.sign_in_event)

    def sign_in_event(self):
        self.login = self.login_line.text()
        password = self.pass_line.text()
        obj = funcs.db_load()
        if self.login == '':
                self.account_window = MWindow('ravil')
                self.account_window.show()
                self.close() 
                return
        if self.login in obj:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if obj[self.login]['password'] == hashed_password:
                QMessageBox.information(self, 'Успех', 'Вы успешно вошли в систему!')
                self.account_window = MWindow(self.login)
                self.account_window.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный пароль.')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Логин не найден.')

##admin1488
##Admin1488!