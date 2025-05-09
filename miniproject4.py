import json
from sys import argv
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QListWidget, QLineEdit, QComboBox\
,QLCDNumber, QTabWidget, QWidget, QCheckBox
from PyQt6 import QtGui

def db_load():
    try:
        with open('db.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}

def db_dump(obj):
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f)

class MWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 550)

        ## combobox
        # self.combobox = QComboBox(self)
        # self.combobox.setFixedSize(300, 30)
        # self.combobox.move(75, 10)
        # self.combobox.currentTextChanged.connect(self.item_changed)

        ## tabwidget
        self.tabs = QTabWidget(self)
        self.tabs.setFixedSize(450, 550)
        self.tabs.currentChanged.connect(self.item_changed)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        if self.tabs.count() > 0:
            self.tabs.setCurrentIndex(0)
        self.item_changed()        

        ## question label
        self.question_label = QLabel(self)
        self.question_label.setFixedSize(350, 30) 
        self.question_label.move(25, 50)

        ## line edit
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedSize(350, 30)
        self.line_edit.move(25, 90)

        ## add button
        self.add_button = QPushButton("ДОБАВИТЬ ВОПРОС", self)
        self.add_button.setFixedSize(150, 30)
        self.add_button.move(25, 130)
        self.add_button.clicked.connect(self.save_question)

        ## delete button
        self.delete_button = QPushButton("УДАЛИТЬ ВОПРОС", self)
        self.delete_button.setFixedSize(150, 30)
        self.delete_button.move(225, 130)
        self.delete_button.clicked.connect(self.delete_question)

        self.update_tabs()


    def handle_btn1_click(self):
        item = self.tabs.tabText(self.tabs.currentIndex())
        db = db_load()
        db[item]['1'].append(self.line_edit.text())
        db_dump(db)
        self.line_edit.clear()
        self.list1_changed()

    def handle_btn2_click(self):
        item = self.tabs.tabText(self.tabs.currentIndex())
        db = db_load()
        db[item]['2'].append(self.line_edit.text())
        db_dump(db)
        self.line_edit.clear()
        self.list2_changed()

    def save_question(self):
        question = self.line_edit.text()
        if question:
            db = db_load()
            db[question] = {'1': [], '2': [], 'is_solved': 0}
            db_dump(db)
            self.line_edit.clear()
            self.update_tabs()
            # self.question_label.setText(question)
            # self.combobox.setCurrentText(question)

    def delete_question(self):
        question = self.tabs.tabText(self.tabs.currentIndex())
        if question:
            db = db_load()
            if question in db:
                del db[question]
            # if len(db) > 0:
            #     last_item = list(db.items())[-1][0]
            #     self.combobox.setCurrentText(last_item)
            #     self.item_changed()
            db_dump(db)
            self.update_tabs()
            self.question_label.setText("")

    def item_changed(self):
        item = self.tabs.tabText(self.tabs.currentIndex())
        if item:
            self.question_label.setText(item)
            self.list1_changed()
            self.list2_changed()
            self.is_solve_update()

    def update_tabs(self):
        db = db_load()
        self.tabs.clear()
        for question in db:
            tab = QWidget()
            ## кнопка "ЗА"
            self.btn1 = QPushButton("ЗА", self)
            self.btn1.setFixedSize(150, 30)
            self.btn1.move(25, 170)
            self.btn1.clicked.connect(self.handle_btn1_click)

            ## Аргументы кнопки "ЗА"
            self.list1 = QListWidget(self)
            self.list1.setFixedSize(150, 200)
            self.list1.move(25, 210)
            self.list1.itemDoubleClicked.connect(self.list1_delete)

            self.up1_btn = QPushButton("Вверх", self)
            self.up1_btn.setFixedSize(60, 30)
            self.up1_btn.move(55, 415)
            self.up1_btn.clicked.connect(self.move_up_list1)

            ## кнопка "ПРОТИВ"
            self.btn2 = QPushButton("ПРОТИВ", self)
            self.btn2.setFixedSize(150, 30)
            self.btn2.move(225, 170)
            self.btn2.clicked.connect(self.handle_btn2_click)

            ## Аргументы кнопки "ПРОТИВ"
            self.list2 = QListWidget(self)
            self.list2.setFixedSize(150, 200)
            self.list2.move(225, 210)
            self.list2.itemDoubleClicked.connect(self.list2_delete)

            self.up2_btn = QPushButton("Вверх", self)
            self.up2_btn.setFixedSize(60, 30)
            self.up2_btn.move(255, 415)
            self.up2_btn.clicked.connect(self.move_up_list2)

            ## LCD для "ЗА"
            self.lcd1 = QLCDNumber(self)
            self.lcd1.setFixedSize(60, 30)
            self.lcd1.move(55, 460)
            self.lcd1.display(0)
            self.lcd1.setStyleSheet('background-color: black;')

            ## LCD для "ПРОТИВ"
            self.lcd2 = QLCDNumber(self)
            self.lcd2.setFixedSize(60, 30)
            self.lcd2.move(255, 460)
            self.lcd2.display(0)
            self.lcd2.setStyleSheet('background-color: black;')

            ## Решённый вопрос
            self.checkbox = QCheckBox(self)
            self.checkbox.setText("Решено")
            self.checkbox.move(25, 490)
            self.checkbox.clicked.connect(self.checkbox_event)

            ## добавление вкладки
            self.tabs.addTab(tab, question)

    def list1_changed(self):
        db = db_load()
        self.list1.clear()
        current_item = self.tabs.tabText(self.tabs.currentIndex())
        count = 0
        if current_item in db and '1' in db[current_item]:
            for argument in db[current_item]['1']:
                self.list1.addItem(argument)
            count = len(db[current_item]['1'])
        self.lcd1.display(count)

    def list2_changed(self):
        db = db_load()
        self.list2.clear()
        item = self.tabs.tabText(self.tabs.currentIndex())
        count = 0
        if item in db and '2' in db[item]:
            for arg in db[item]['2']:
                self.list2.addItem(arg)
            count = len(db[item]['2'])
        self.lcd2.display(count)
            
    def list1_delete(self):
        db = db_load()
        selected_item = self.list1.currentItem()
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        self.list1.takeItem(self.list1.row(selected_item))
        db[current_question]['1'].remove(selected_item.text())
        db_dump(db)

    def list2_delete(self):
        db = db_load()
        selected_item = self.list2.currentItem()
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        self.list2.takeItem(self.list2.row(selected_item))
        db[current_question]['2'].remove(selected_item.text())
        db_dump(db)

    def move_up_list1(self):
        row = self.list1.currentRow()
        if row > 0:
            db = db_load()
            current_question = self.tabs.tabText(self.tabs.currentIndex())
            args = db[current_question]['1']
            args[row - 1], args[row] = args[row], args[row - 1]
            db_dump(db)
            self.list1_changed()
            self.list1.setCurrentRow(row - 1)

    def move_up_list2(self):
        row = self.list2.currentRow()
        if row > 0:
            db = db_load()
            current_question = self.tabs.tabText(self.tabs.currentIndex())
            args = db[current_question]['2']
            args[row - 1], args[row] = args[row], args[row - 1]
            db_dump(db)
            self.list2_changed()
            self.list2.setCurrentRow(row - 1)

    def checkbox_event(self):
        db = db_load()
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        if self.checkbox.isChecked():
            db[current_question]['is_solved'] = 1
        else:
            db[current_question]['is_solved'] = 0
        self.is_solve_update()
        db_dump(db)

    def is_solve_update(self):
        db = db_load()
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        if db[current_question]['is_solved'] == 1:
            self.btn1.setEnabled(False)
            self.btn2.setEnabled(False)
            self.up1_btn.setEnabled(False)
            self.up2_btn.setEnabled(False)
            self.checkbox.setChecked(True)
        else:
            self.btn1.setEnabled(True)
            self.btn2.setEnabled(True)
            self.up1_btn.setEnabled(True)
            self.up2_btn.setEnabled(True)
            self.checkbox.setChecked(False)

app = QApplication(argv)
window = MWindow()
window.show()
app.exec()