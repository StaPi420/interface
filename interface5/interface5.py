import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QCheckBox, QRadioButton, QButtonGroup, QListWidget, QPushButton
from PyQt6.QtGui import QFont
from interface5_new_window import OrderedWindow
import json

def order_dump(order):
    with open('order.json', 'w', encoding='utf-8') as f:
        json.dump(order, f)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(420, 350)

        self.layout = QGridLayout()

        ##
        self.btn_clicked = 0
        self.order = {'Первое блюдо': None, 'Второе блюдо': None, 'Салат': None, 'Десерт': None, 'Напиток': None}


        ##Первое блюдо
        self.first_meal = QCheckBox("Первое блюдо", self)
        self.first_meal.setFont(QFont("Arial", 12))
        self.first_meal.move(10, 20)
        self.first_meal.setFixedSize(200, 20)
        self.first_meal.setEnabled(False)

        
        ##Варианты первого блюда
        self.first_meal_option1 = QRadioButton("Суп", self)
        self.first_meal_option1.setFont(QFont("Arial", 10))
        self.first_meal_option1.move(25, 50)

        self.first_meal_option2 = QRadioButton("Борщ", self)
        self.first_meal_option2.setFont(QFont("Arial", 10))
        self.first_meal_option2.move(25, 80)

        self.first_meal_option3 = QRadioButton("Щи", self)
        self.first_meal_option3.setFont(QFont("Arial", 10))
        self.first_meal_option3.move(25, 110)

        self.first_meal_group = QButtonGroup(self)
        self.first_meal_group.addButton(self.first_meal_option1)
        self.first_meal_group.addButton(self.first_meal_option2)
        self.first_meal_group.addButton(self.first_meal_option3)
        self.first_meal_group.buttonClicked.connect(lambda: (self.first_meal.setEnabled(True)))

        ##Второе блюда
        self.second_meal = QCheckBox("Второе блюдо", self)
        self.second_meal.setFont(QFont("Arial", 12))
        self.second_meal.move(10, 150)
        self.second_meal.setFixedSize(200, 20)
        self.second_meal.setEnabled(False)

        ##Варианты второго блюда
        self.second_meal_option1 = QRadioButton("Котлета", self)
        self.second_meal_option1.setFont(QFont("Arial", 10))
        self.second_meal_option1.move(25, 170)

        self.second_meal_option2 = QRadioButton("Рыба", self)
        self.second_meal_option2.setFont(QFont("Arial", 10))
        self.second_meal_option2.move(25, 200)

        self.second_meal_option3 = QRadioButton("Курица", self)
        self.second_meal_option3.setFont(QFont("Arial", 10))
        self.second_meal_option3.move(25, 230)

        self.second_meal_group = QButtonGroup(self)
        self.second_meal_group.addButton(self.second_meal_option1)
        self.second_meal_group.addButton(self.second_meal_option2)
        self.second_meal_group.addButton(self.second_meal_option3)
        self.second_meal_group.buttonClicked.connect(lambda: (self.second_meal.setEnabled(True)))


        ##Салат
        self.third_meal = QCheckBox("Салат", self)
        self.third_meal.setFont(QFont("Arial", 12))
        self.third_meal.move(160, 20)
        self.third_meal.setFixedSize(200, 20)
        self.third_meal.setEnabled(False)


        ##Варианты салата
        self.third_meal_option1 = QRadioButton("Оливье", self)
        self.third_meal_option1.setFont(QFont("Arial", 10))
        self.third_meal_option1.move(170, 50)

        self.third_meal_option2 = QRadioButton("Цезарь", self)
        self.third_meal_option2.setFont(QFont("Arial", 10))
        self.third_meal_option2.move(170, 80)

        self.third_meal_option3 = QRadioButton("Винегрет", self)
        self.third_meal_option3.setFont(QFont("Arial", 10))
        self.third_meal_option3.move(170, 110)

        self.third_meal_group = QButtonGroup(self)
        self.third_meal_group.addButton(self.third_meal_option1)
        self.third_meal_group.addButton(self.third_meal_option2)
        self.third_meal_group.addButton(self.third_meal_option3)
        self.third_meal_group.buttonClicked.connect(lambda: (self.third_meal.setEnabled(True)))


        ##Десерт
        self.dessert = QCheckBox("Десерт", self)
        self.dessert.setFont(QFont("Arial", 12))
        self.dessert.move(160, 150)
        self.dessert.setFixedSize(200, 20)
        self.dessert.setEnabled(False)

        ##Варианты десерта
        self.dessert_option1 = QRadioButton("Мороженое", self)
        self.dessert_option1.setFont(QFont("Arial", 10))
        self.dessert_option1.move(170, 170)

        self.dessert_option2 = QRadioButton("Торт", self)
        self.dessert_option2.setFont(QFont("Arial", 10))
        self.dessert_option2.move(170, 200)

        self.dessert_option3 = QRadioButton("Пирожное", self)
        self.dessert_option3.setFont(QFont("Arial", 10))
        self.dessert_option3.move(170, 230)

        self.dessert_group = QButtonGroup(self)
        self.dessert_group.addButton(self.dessert_option1)
        self.dessert_group.addButton(self.dessert_option2)
        self.dessert_group.addButton(self.dessert_option3)
        self.dessert_group.buttonClicked.connect(lambda: (self.dessert.setEnabled(True)))

        ##Напиток
        self.drink = QCheckBox("Напиток", self)
        self.drink.setFont(QFont("Arial", 12))
        self.drink.move(300, 20)
        self.drink.setFixedSize(200, 20)
        self.drink.setEnabled(False)

        ##Выбор напитка
        self.drink_option1 = QRadioButton("Чай", self)
        self.drink_option1.setFont(QFont("Arial", 10))
        self.drink_option1.move(320, 50)

        self.drink_option2 = QRadioButton("Кофе", self)
        self.drink_option2.setFont(QFont("Arial", 10))
        self.drink_option2.move(320, 80)

        self.drink_option3 = QRadioButton("Сок", self)
        self.drink_option3.setFont(QFont("Arial", 10))
        self.drink_option3.move(320, 110)

        self.drink_group = QButtonGroup(self)
        self.drink_group.addButton(self.drink_option1)
        self.drink_group.addButton(self.drink_option2)
        self.drink_group.addButton(self.drink_option3)        
        self.drink_group.buttonClicked.connect(lambda: (self.drink.setEnabled(True)))

        
        ##Кнопка заказать
        self.order_btn = QPushButton("ЗАКАЗАТЬ", self)
        self.order_btn.setFixedSize(100, 40)
        self.order_btn.move(10, 270)
        self.order_btn.setFont(QFont("Arial", 10))
        self.order_btn.setEnabled(False)

        ##Подключения
        self.first_meal.clicked.connect(lambda: (self.btn_click(), self.order.update({'Первое блюдо': self.first_meal_group.checkedButton().text()\
                                      if not self.first_meal_group.checkedButton() is None else None})) if self.first_meal.isChecked() else (self.btn_release(), 
                                      self.order.update({'Первое блюдо': None})))
        self.second_meal.clicked.connect(lambda: (self.btn_click(), self.order.update({'Второе блюдо': self.second_meal_group.checkedButton().text()\
                                      if not self.second_meal_group.checkedButton() is None else None})) if self.second_meal.isChecked() else (self.btn_release(), 
                                      self.order.update({'Второе блюдо': None})))
        self.third_meal.clicked.connect(lambda: (self.btn_click(), self.order.update({'Салат': self.third_meal_group.checkedButton().text()\
                                      if not self.third_meal_group.checkedButton() is None else None})) if self.third_meal.isChecked() else (self.btn_release(), 
                                      self.order.update({'Салат': None})))
        self.dessert.clicked.connect(lambda: (self.btn_click(), self.order.update({'Десерт': self.dessert_group.checkedButton().text()\
                                      if not self.dessert_group.checkedButton() is None else None})) if self.dessert.isChecked() else (self.btn_release(), 
                                      self.order.update({'Десерт': None})))
        self.drink.clicked.connect(lambda: (self.btn_click(), self.order.update({'Напиток': self.drink_group.checkedButton().text()\
                                      if not self.drink_group.checkedButton() is None else None})) if self.drink.isChecked() else (self.btn_release(), 
                                      self.order.update({'Напиток': None})))
        self.order_btn.clicked.connect(self.ordered)


    def btn_click(self):
        self.btn_clicked += 1
        if self.btn_clicked >= 2:
            self.order_btn.setEnabled(True)
    
    def btn_release(self):
        self.btn_clicked -= 1
        if self.btn_clicked < 2:
            self.order_btn.setEnabled(False)

    def ordered(self):
        order_dump(self.order)
        self.order_window = OrderedWindow()
        self.order_window.show()
        print(self.order)


    


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
