import sys
import os
import os.path
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6.QtGui import QPixmap

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 350)

        ##Изображение
        self.images = os.listdir("python_progs/interface/image")
        self.images.sort()
        print(self.images)
        self.current_image_index = 0
        self.current_image = self.images[self.current_image_index]  # Начальное изображение
        self.image = QPixmap(os.path.join("python_progs/interface/image", self.current_image))
        self.image.scaled(400, 250)

        #Лейбл для изображения
        self.label = QLabel(self)
        self.label.setPixmap(self.image)
        self.label.setScaledContents(True)
        self.label.setFixedSize(400, 250)
        self.label.move(100, 20)

        ##Кнопка вперёд
        self.btn_next = QPushButton('ВПЕРЁД', self)
        self.btn_next.setFixedSize(80, 25)
        self.btn_next.move(510, 120)
        self.btn_next.clicked.connect(self.next_image)

        ##Кнопка назад
        self.btn_last = QPushButton('НАЗАД', self)
        self.btn_last.setFixedSize(80, 25)
        self.btn_last.move(10, 120)
        self.btn_last.clicked.connect(self.prev_image)
        self.btn_last.setEnabled(False)  

        ##Первое изображение
        self.btn_first = QPushButton('ПЕРВОЕ', self)
        self.btn_first.setFixedSize(80, 25)
        self.btn_first.move(10, 150)
        self.btn_first.clicked.connect(self.first_image)
        self.btn_first.setEnabled(False)

        ##Последнее изображение
        self.btn_last_image = QPushButton('ПОСЛЕДНЕЕ', self)
        self.btn_last_image.setFixedSize(80, 25)
        self.btn_last_image.move(510, 150)
        self.btn_last_image.clicked.connect(self.last_image)
    
    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.image_update()
        self.btn_set_enabed()

    
    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.image_update()     
        self.btn_set_enabed()

    def image_update(self):
        self.image = QPixmap(os.path.join("python_progs/interface/image", self.images[self.current_image_index]))
        self.image.scaled(400, 250)
        self.label.setPixmap(self.image)

    def first_image(self):
        self.current_image_index = 0
        self.image_update()
        self.btn_set_enabed()

    
    def last_image(self):
        self.current_image_index = len(self.images) - 1
        self.image_update()
        self.btn_set_enabed()

    def btn_set_enabed(self):
        if self.current_image_index == 0:
            self.btn_last.setEnabled(False)
            self.btn_first.setEnabled(False)
        if self.current_image_index == len(self.images) - 1:
            self.btn_next.setEnabled(False)
            self.btn_last_image.setEnabled(False)
        if self.current_image_index > 0:
            self.btn_last.setEnabled(True)
            self.btn_first.setEnabled(True)
        if self.current_image_index < len(self.images) - 1:
            self.btn_next.setEnabled(True)
            self.btn_last_image.setEnabled(True)
    
    
    

app = QApplication(sys.argv)
ex = MyWindow()
ex.show()
sys.exit(app.exec())