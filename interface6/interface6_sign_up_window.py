from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QLineEdit
from PyQt6.QtGui import QFont
from interface6_sign_in import SignInWindow
import funcs
import re
import hashlib

obj = funcs.db_load()

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 700)
        self.name_label = QLabel('Регистрация', self)
        self.name_label.move(140, 20)
        self.name_label.setFixedSize(250, 30)
        self.font1 = QFont('Arial', 16)
        self.font1.setBold(True)
        self.name_label.setFont(self.font1)

        ##Шрифты
        self.font2 = QFont('Arial', 12)
        self.font2.setBold(True)
        self.font3 = QFont('Arial', 8)

        ##флаги
        self.login_flag = False
        self.pass_flag = False
        self.repeat_pass_flag = False
        self.email_flag = False
        self.phone_flag = False


        ##Кнопка закрыть
        self.close_btn = QPushButton('ЗАКРЫТЬ', self)
        self.close_btn.setFixedSize(100, 50)
        self.close_btn.move(250, 640)
        self.close_btn.clicked.connect(self.close_event)

        ##Логин
        self.login_label = QLabel('Введите логин (обязательно):', self)
        self.login_label.move(50, 70)
        self.login_label.setFixedSize(300, 30)
        self.login_label.setFont(self.font2)

        self.login_line = QLineEdit(self)
        self.login_line.move(50, 100)
        self.login_line.setFixedSize(300, 30)
        self.login_line.textEdited.connect(self.login_event)

        self.login_correct_label = QLabel('Логин состоит не менее чем из 5 символов из набора\n \
латинских букв и цифр.', self)
        self.login_correct_label.setFont(self.font3)
        self.login_correct_label.move(50, 140)
        self.login_correct_label.setFixedSize(300, 40)

        ## Пароль
        self.pass_label = QLabel('Введите пароль (обязательно):', self)
        self.pass_label.move(50, 170)
        self.pass_label.setFixedSize(300, 30)
        self.pass_label.setFont(self.font2)

        self.pass_line = QLineEdit(self)
        self.pass_line.move(50, 200)
        self.pass_line.setFixedSize(300, 30)
        self.pass_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_line.textEdited.connect(self.pas_event)

        self.pass_correct_label = QLabel(
            'Пароль должен состоять не менее чем из 8 символов,\n'
            'содержать как минимум одну строчную и одну прописную букву,\n'
            'хотя бы одну цифру и хотя бы один специальный символ.', self)
        self.pass_correct_label.setFont(self.font3)
        self.pass_correct_label.move(50, 230)

        ## Повтор пароля
        self.repeat_pass_label = QLabel('Повторите пароль (обязательно):', self)
        self.repeat_pass_label.move(50, 270)
        self.repeat_pass_label.setFixedSize(300, 30)
        self.repeat_pass_label.setFont(self.font2)

        self.repeat_pass_line = QLineEdit(self)
        self.repeat_pass_line.move(50, 300)
        self.repeat_pass_line.setFixedSize(300, 30)
        self.repeat_pass_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.repeat_pass_line.textEdited.connect(self.repeat_pas_event)

        self.repeat_pass_correct_label = QLabel(
            'Повтор пароля обязан совпадать с паролем.\n'
            'Если повтор не совпадает, пароль вводится заново.', self)
        self.repeat_pass_correct_label.setFont(self.font3)
        self.repeat_pass_correct_label.move(50, 330)

        ## Электронная почта
        self.email_label = QLabel('Введите электронную почту \n'
        '(обязательно):', self)
        self.email_label.move(50, 370)
        self.email_label.setFixedSize(300, 60)
        self.email_label.setFont(self.font2)

        self.email_line = QLineEdit(self)
        self.email_line.move(50, 430)
        self.email_line.setFixedSize(300, 30)
        self.email_line.textEdited.connect(self.email_event)

        self.email_correct_label = QLabel(
            'Адрес электронной почты должен содержать ровно один символ @,\n'
            'но не начинаться с него и не заканчиваться им.', self)
        self.email_correct_label.setFont(self.font3)
        self.email_correct_label.move(50, 460)

        ## Номер телефона
        self.phone_label = QLabel('Введите номер телефона\n'
        '(обязательно):', self)
        self.phone_label.move(50, 500)
        self.phone_label.setFixedSize(300, 60)
        self.phone_label.setFont(self.font2)

        self.phone_line = QLineEdit(self)
        self.phone_line.move(50, 560)
        self.phone_line.setFixedSize(300, 30)
        self.phone_line.textEdited.connect(self.phone_event)

        self.phone_correct_label = QLabel(
            'Телефон вводится в следующем формате:\n'
            'сначала идёт +7 или 8, а затем 10 цифр с любым количеством\n'
            'пробелов между ними и без каких-либо иных символов.', self)
        self.phone_correct_label.setFont(self.font3)
        self.phone_correct_label.move(50, 590)

        ##Кнопка регистрации
        self.sign_up_btn = QPushButton('Зарегистрироваться', self)
        self.sign_up_btn.setFixedSize(150 ,50)
        self.sign_up_btn.move(50, 640)
        self.sign_up_btn.setEnabled(False)
        self.sign_up_btn.clicked.connect(self.sign_up_event)

    def close_event(self):
        app = QApplication.instance()
        app.closeAllWindows()

    def login_event(self):
        if self.login_line.text() in obj:
            self.login_correct_label.setText('Такой логин уже существует')
            self.login_correct_label.setStyleSheet('color: #D60026')
            self.login_flag = False
            self.sign_up_enabled()
        else:
            response = ''.join(funcs.login_check(self.login_line.text()))
            self.login_correct_label.setText(response)
            if response == '':
                self.login_flag = True
            else:
                self.login_flag = False
            self.login_correct_label.setStyleSheet('color: #D60026')
            self.sign_up_enabled()

    def pas_event(self):
        for i in obj:
            if obj[i]['password'] == hashlib.sha256(self.pass_line.text().encode()).hexdigest():
                self.pass_correct_label.setText('Такой пароль уже существует')
                self.pass_correct_label.setStyleSheet('color: #D60026')
                self.pass_flag = False
                self.sign_up_enabled()
                return
        response = ''.join(funcs.pass_check(self.pass_line.text()))
        self.pass_correct_label.setText(response)
        if response == '':
            self.pass_flag = True
        else:
            self.pass_flag = False
        self.pass_correct_label.setStyleSheet('color: #D60026')
        self.sign_up_enabled()

    def repeat_pas_event(self):
        if self.pass_line.text() != self.repeat_pass_line.text():
            self.repeat_pass_correct_label.setText('Пароли должны совпадать')
            self.repeat_pass_correct_label.setStyleSheet('color: #D60026')
            self.repeat_pass_flag = False
        else:
            self.repeat_pass_correct_label.setText('')
            self.repeat_pass_flag = True
        self.sign_up_enabled()

    def email_event(self):
        for i in obj:
            if obj[i]['email'] == self.email_line.text():
                self.email_correct_label.setText('Такой адрес электронной почты уже существует')
                self.email_correct_label.setStyleSheet('color: #D60026')
                self.email_flag = False
                self.sign_up_enabled()
                return
        if re.fullmatch(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', self.email_line.text()) is None:
            self.email_correct_label.setText('Адрес электронной почты должен содержать ровно один символ @,\n'
            'но не начинаться с него и не заканчиваться им.')
            self.email_correct_label.setStyleSheet('color: #D60026')
            self.email_flag = False
        else:
            self.email_correct_label.setText('')
            self.email_flag = True
        self.sign_up_enabled()
        
    

    def phone_event(self):
        for i in obj:
            if obj[i]['phone'] == self.phone_line.text():
                self.phone_correct_label.setText('Такой номер телефона уже существует')
                self.phone_correct_label.setStyleSheet('color: #D60026')
                self.phone_flag = False
                self.sign_up_enabled()
                return
        if re.fullmatch(r'(?:\+7|8)(?:\d{10})', self.phone_line.text()) is None:
            self.phone_correct_label.setStyleSheet('color: #D60026')
            self.phone_correct_label.setText('Телефон вводится в следующем формате:\n'
            'сначала идёт +7 или 8, а затем 10 цифр с любым количеством\n'
            'пробелов между ними и без каких-либо иных символов.')
            self.phone_flag = False
        else:
            self.phone_correct_label.setText('')
            self.phone_flag = True
        self.sign_up_enabled()

    def sign_up_enabled(self):
        if self.login_flag and self.pass_flag and self.repeat_pass_flag and self.email_flag and self.phone_flag:
            self.sign_up_btn.setEnabled(True)
        else:
            self.sign_up_btn.setEnabled(False)
    
    def sign_up_event(self):
        obj.update({self.login_line.text(): {'password': hashlib.sha256(self.pass_line.text().encode()).hexdigest(),
        'email': self.email_line.text(), 'phone': self.phone_line.text()}})
        funcs.db_dump(obj)
        self.new_window = SignInWindow()
        self.new_window.show()
        

##14881488Tt@