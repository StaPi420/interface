from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont
import funcs


class AccountWidget(QWidget):
    def __init__(self, login, main_window):
        super().__init__()
        self.obj = funcs.db_load()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Информация об аккаунте")
        self.main_window = main_window

        # Шрифт для заголовков
        font_header = QFont('Arial', 14)
        font_header.setBold(True)

        # Шрифт для текста
        font_text = QFont('Arial', 12)

        # Заголовок
        self.title_label = QLabel("Информация об аккаунте", self)
        self.title_label.setFont(font_header)

        # Логин
        self.login_label = QLabel(f"Логин: {self.main_window.login}", self)
        self.login_label.setFont(font_text)

        # Электронная почта
        self.email_label = QLabel(f"Электронная почта: {self.obj[login].get('email', 'Не указана')}", self)
        self.email_label.setFont(font_text)

        # Номер телефона
        self.phone_label = QLabel(f"Номер телефона: {self.obj[login].get('phone', 'Не указан')}", self)
        self.phone_label.setFont(font_text)

        # Кнопка возврата
        self.back_button = QPushButton("Назад", self)
        self.back_button.setFixedSize(100, 40)
        self.back_button.clicked.connect(self.go_back)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.login_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def go_back(self):
        """Возврат в главное окно."""
        self.main_window.show()
        self.close()