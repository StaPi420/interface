from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QApplication
import json

def order_load():
    with open('order.json', 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return {"first_meal": None, "second_meal": None, "third_meal": None, "dessert": None, "drink": None}

class OrderedWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.order = order_load()
        self.order_list = '\n'.join([f"{key}: {value}" for key, value in self.order.items() if value is not None])
        self.order_label = QLabel("Ваш заказ:\n" + self.order_list, self)
        self.window_height = self.order_label.height() + 30
        self.order_label.move(10, 30)
        
        ##Лейбл
        self.label = QLabel("Заказ оформлен", self)
        self.label.move(10, 10)

        ##Кнопка
        self.btn_ok = QPushButton('OK', self)
        self.btn_ok.setFixedSize(80, 25)
        self.btn_ok.move(10, self.window_height + 20)
        self.btn_ok.clicked.connect(self.close_window)

        self.setFixedSize(300, self.window_height + 70)

    def close_window(self):
        app = QApplication.instance()
        app.closeAllWindows()