import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QLineEdit, QMainWindow, QMessageBox, QWidget
from PyQt6.QtCore import Qt

class DragButton(QPushButton):

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.MouseButton.RightButton:
            self.__mousePressPos = event.pos()
            self.__mouseMovePos = event.pos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.RightButton:
            # adjust offset from clicked point to origin of widget
            currPosX = self.pos().x()
            currPosY = self.pos().y()
            newPosX = event.pos().x() - self.__mouseMovePos.x() + currPosX
            newPosY = event.pos().y() - self.__mouseMovePos.y() + currPosY
            self.move(newPosX, newPosY)

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(DragButton, self).mouseReleaseEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 300)

        self.line = QLineEdit(self)
        self.line.setFixedSize(300, 30)
        self.line.move(10, 10)


    def mouseDoubleClickEvent(self, event):
        self.new_window = EnterLetterWindow(self, event.pos().x(), event.pos().y())
        self.new_window.show()
        # self.new_button = DragButton(self)
        # self.new_button.setFixedSize(80, 40)
        # self.new_button.move(int(event.pos().x()), int(event.pos().y()))
        # self.new_button.clicked.connect(lambda: self.letter_event(self.new_button.text()))

    def letter_event(self, letter):
        self.line.setText(self.line.text() + letter)

    


class EnterLetterWindow(QWidget):
    def __init__(self, parent_window, posx, posy):
        super().__init__(parent_window)
        self.setFixedSize(200, 100)
        self.setWindowFlag(Qt.WindowType.Window)
        self.posx = posx
        self.posy = posy

        self.input_field = QLineEdit(self)
        self.input_field.setFixedSize(180, 30)
        self.input_field.move(10, 10)

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setFixedSize(80, 30)
        self.submit_button.move(10, 50)
        self.submit_button.clicked.connect(self.submit_letter)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.setFixedSize(80, 30)
        self.cancel_button.move(110, 50)
        self.cancel_button.clicked.connect(self.close)

    def submit_letter(self):
        letter = self.input_field.text()
        parent_window = self.parent()
        parent_window.new_button = DragButton(letter, parent_window)
        parent_window.new_button.setFixedSize(80, 40)
        parent_window.new_button.move(int(self.posx), int(self.posy))
        parent_window.new_button.clicked.connect(lambda: parent_window.line.setText(parent_window.line.text() + letter))
        parent_window.new_button.show()
        self.close()

    def close(self):
        super().close()
    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())