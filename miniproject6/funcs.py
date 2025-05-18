import json
import string
from PyQt6.QtWidgets import QListWidget, QMessageBox, QMenu, QInputDialog
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

def db_load():
    with open('D:\\vscode101\\python_progs\\interface\\miniproject6\\accounts.json', 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

def db_dump(obj):
    with open('D:\\vscode101\\python_progs\\interface\\miniproject6\\accounts.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f)

def login_check(log):
    response = ['', '']
    if len(log) < 5:
        response[1] = 'Логин должен быть длиннее 5 символов.\n'
    else:
        response[1] = ''
    symbols = set(string.ascii_letters + string.digits)
    for i in log:
        if i not in symbols:
            response[0] = 'Логин должен содержать только символы \n\
латиницы и цифры.\n'
            break   
    else:
        response[0] = ''
    return response

def pass_check(pas):
    response = ['', '', '', '', '']
    if len(pas) < 8:
        response[0] = "Пароль должен состоять не менее чем из 8 символов\n"
    else:
        response[0] = ''
    if any(x.isupper() for x in pas):
        response[1] = ''
    else:
        response[1] = 'Пароль должен содержать хотя бы заглавный символ\n'
    if any(x.islower() for x in pas):
        response[2] = ''
    else:
        response[2] = 'Пароль должен содержать хотя бы один строчной символ\n'
    if any(x in string.digits for x in pas):
        response[3] = ''
    else:
        response[3] = 'Пароль должен содержать хотя бы одну цифру\n' 
    if any(x in {'!', '@', '#', '$','%', '%'} for x in pas):
        response[4] = ''
    else:
        response[4] = 'Пароль должен содержать хотя бы один специальный символ\n'
    return response

class DraggableListWidget(QListWidget):
    def __init__(self, parent=None, grandparent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.parent = parent
        self.grandparent = grandparent

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            item = self.itemAt(e.pos())
            if item:
                drag = QtGui.QDrag(self)
                mime_data = QtCore.QMimeData()
                mime_data.setText(item.text())
                drag.setMimeData(mime_data)
                drag.exec(Qt.DropAction.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Подтверждение")
        dlg.setText("Вы уверены, что хотите переместить элемент?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if dlg.exec() == QMessageBox.StandardButton.Yes:
            if event.mimeData().hasText():
                text = event.mimeData().text()
                # Удаляем элемент из исходного списка, если перенос между списками
                source = event.source()
                items = source.findItems(text, Qt.MatchFlag.MatchExactly)
                for item in items:
                    source.takeItem(source.row(item))
                self.addItem(text)
                event.accept()
                self.grandparent.db_update()
            else:
                event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            item = self.itemAt(event.pos())
            if item is None:
                return
            menu = QMenu(self)
            delete_action = QAction("Удалить", self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)
            edit_action = QAction("Редактировать", self)
            edit_action.triggered.connect(lambda: self.editItem(item))
            menu.addAction(edit_action)
            menu.exec(self.mapToGlobal(event.pos()))

    def delete_item(self, item):
        self.takeItem(self.row(item))
        self.grandparent.db_update()

    def editItem(self, item):
        text, ok = QInputDialog.getText(self, "Редактировать элемент", "Новое значение:", text=item.text())
        if ok and text:
            item.setText(text)
            self.grandparent.db_update()