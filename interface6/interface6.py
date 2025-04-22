from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtGui import QFont
import sys
from interface6_sign_up_window import SignUpWindow
from interface6_sign_in import SignInWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)

        ##лейбл
        self.label = QLabel('Добро пожаловать!', self)
        self.label.move(25, 10)
        self.label.setFixedSize(150, 20)
        self.label.setFont(QFont('Arial', 12))

        ##Кнопка "Зарегистрироваться"
        self.sign_up_btn = QPushButton('ЗАРЕГИСТРИРОВАТЬСЯ', self)
        self.sign_up_btn.setFixedSize(180, 50)
        self.sign_up_btn.move(10, 40)
        self.sign_up_btn.clicked.connect(self.sign_up_window_open)

        ##Кнопка войти
        self.sign_in_btn = QPushButton('Войти', self)
        self.sign_in_btn.setFixedSize(180, 50)
        self.sign_in_btn.move(10, 120)
        self.sign_in_btn.clicked.connect(self.sign_in_window_open)

    def sign_up_window_open(self):
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.show()
        self.close()
    
    def sign_in_window_open(self):
        self.sign_in_window = SignInWindow(self)
        self.sign_in_window.show()
        #self.close()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())