import json
from math import log
from sys import argv
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QListWidget, QLineEdit, QComboBox\
,QLCDNumber, QTabWidget, QWidget, QCheckBox, QMessageBox
from PyQt6 import QtGui

def db_load():
    try:
        with open('D:\\vscode101\\python_progs\\interface\\miniproject5\\db.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}

def db_dump(obj):
    with open('D:\\vscode101\\python_progs\\interface\\miniproject5\\db.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f)

class MWindow(QMainWindow):
    def __init__(self, login):
        super().__init__()
        self.setFixedSize(450, 550)
        self.login = login

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
        db[self.login][item]['1'].append(self.line_edit.text())
        db_dump(db)
        self.line_edit.clear()
        self.list1_changed()

    def handle_btn2_click(self):
        item = self.tabs.tabText(self.tabs.currentIndex())
        db = db_load()
        db[self.login][item]['2'].append(self.line_edit.text())
        db_dump(db)
        self.line_edit.clear()
        self.list2_changed()

    def save_question(self):
        dlg = QMessageBox(self)
        dlg.setText("Вы действительно хотите добавить вопрос?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if dlg.exec() == QMessageBox.StandardButton.Yes:
            question = self.line_edit.text()
            if question:
                db = db_load()
                print(db)
                if self.login not in db:
                    db[self.login] = {}
                db[self.login][question] = {'1': [], '2': [], 'is_solved': 0}
                db_dump(db)
                self.line_edit.clear()
                self.update_tabs()
                # self.question_label.setText(question)
                # self.combobox.setCurrentText(question)

    def delete_question(self):
        dlg = QMessageBox(self)
        dlg.setText("Вы действительно хотите удалить вопрос?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        question = self.tabs.tabText(self.tabs.currentIndex())
        if dlg.exec() == QMessageBox.StandardButton.Yes:
            if question:
                db = db_load()
                if question in db[self.login]:
                    del db[self.login][question]
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
        db = db[self.login]
        self.tabs.clear()
        self.tab_widgets = {}  # Для хранения виджетов каждой вкладки
        for question in db:
            tab = QWidget()
            # кнопка "ЗА"
            btn1 = QPushButton("ЗА", tab)
            btn1.setFixedSize(150, 30)
            btn1.move(25, 170)
            btn1.clicked.connect(self.handle_btn1_click)

            # Аргументы кнопки "ЗА"
            list1 = QListWidget(tab)
            list1.setFixedSize(150, 200)
            list1.move(25, 210)
            list1.itemDoubleClicked.connect(self.list1_delete)

            up1_btn = QPushButton("Вверх", tab)
            up1_btn.setFixedSize(60, 30)
            up1_btn.move(55, 415)
            up1_btn.clicked.connect(self.move_up_list1)

            # кнопка "ПРОТИВ"
            btn2 = QPushButton("ПРОТИВ", tab)
            btn2.setFixedSize(150, 30)
            btn2.move(225, 170)
            btn2.clicked.connect(self.handle_btn2_click)

            # Аргументы кнопки "ПРОТИВ"
            list2 = QListWidget(tab)
            list2.setFixedSize(150, 200)
            list2.move(225, 210)
            list2.itemDoubleClicked.connect(self.list2_delete)

            up2_btn = QPushButton("Вверх", tab)
            up2_btn.setFixedSize(60, 30)
            up2_btn.move(255, 415)
            up2_btn.clicked.connect(self.move_up_list2)

            # LCD для "ЗА"
            lcd1 = QLCDNumber(tab)
            lcd1.setFixedSize(60, 30)
            lcd1.move(55, 460)
            lcd1.display(0)
            lcd1.setStyleSheet('background-color: black;')

            # LCD для "ПРОТИВ"
            lcd2 = QLCDNumber(tab)
            lcd2.setFixedSize(60, 30)
            lcd2.move(255, 460)
            lcd2.display(0)
            lcd2.setStyleSheet('background-color: black;')

            # Решённый вопрос
            checkbox = QCheckBox(tab)
            checkbox.setText("Решено")
            checkbox.move(25, 490)
            checkbox.clicked.connect(self.checkbox_event)

            # Сохраняем виджеты для доступа из других методов
            self.tab_widgets[question] = {
                'btn1': btn1,
                'list1': list1,
                'up1_btn': up1_btn,
                'btn2': btn2,
                'list2': list2,
                'up2_btn': up2_btn,
                'lcd1': lcd1,
                'lcd2': lcd2,
                'checkbox': checkbox
            }

            self.tabs.addTab(tab, question)

    def list1_changed(self):
        db = db_load()
        db = db[self.login]
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        widgets['list1'].clear()
        count = 0
        if current_question in db and '1' in db[current_question]:
            for argument in db[current_question]['1']:
                widgets['list1'].addItem(argument)
            count = len(db[current_question]['1'])
        widgets['lcd1'].display(count)

    def list2_changed(self):
        db = db_load()
        db = db[self.login]
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        widgets['list2'].clear()
        count = 0
        if current_question in db and '2' in db[current_question]:
            for arg in db[current_question]['2']:
                widgets['list2'].addItem(arg)
            count = len(db[current_question]['2'])
        widgets['lcd2'].display(count)
            
    def list1_delete(self):
        db = db_load()
        db = db[self.login]
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        selected_item = widgets['list1'].currentItem()
        widgets['list1'].takeItem(widgets['list1'].row(selected_item))
        db[current_question]['1'].remove(selected_item.text())
        db_dump({**db_load(), self.login: db})

    def list2_delete(self):
        db = db_load()
        db = db[self.login]
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        selected_item = widgets['list2'].currentItem()
        widgets['list2'].takeItem(widgets['list2'].row(selected_item))
        db[current_question]['2'].remove(selected_item.text())
        db_dump({**db_load(), self.login: db})

    def move_up_list1(self):
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        row = widgets['list1'].currentRow()
        if row > 0:
            db = db_load()
            db = db[self.login]
            args = db[current_question]['1']
            args[row - 1], args[row] = args[row], args[row - 1]
            db_dump({**db_load(), self.login: db})
            self.list1_changed()
            widgets['list1'].setCurrentRow(row - 1)

    def move_up_list2(self):
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        row = widgets['list2'].currentRow()
        if row > 0:
            db = db_load()
            db = db[self.login]
            args = db[current_question]['2']
            args[row - 1], args[row] = args[row], args[row - 1]
            db_dump({**db_load(), self.login: db})
            self.list2_changed()
            widgets['list2'].setCurrentRow(row - 1)

    def checkbox_event(self):
        db = db_load()
        db = db[self.login]
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        if widgets['checkbox'].isChecked():
            db[current_question]['is_solved'] = 1
        else:
            db[current_question]['is_solved'] = 0
        self.is_solve_update()
        db_dump({**db_load(), self.login: db})

    def is_solve_update(self):
        db = db_load()
        db = db[self.login]
        current_question = self.tabs.tabText(self.tabs.currentIndex())
        widgets = self.tab_widgets[current_question]
        if db[current_question]['is_solved'] == 1:
            widgets['btn1'].setEnabled(False)
            widgets['btn2'].setEnabled(False)
            widgets['up1_btn'].setEnabled(False)
            widgets['up2_btn'].setEnabled(False)
            widgets['checkbox'].setChecked(True)
        else:
            widgets['btn1'].setEnabled(True)
            widgets['btn2'].setEnabled(True)
            widgets['up1_btn'].setEnabled(True)
            widgets['up2_btn'].setEnabled(True)
            widgets['checkbox'].setChecked(False)

