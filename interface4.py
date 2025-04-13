import sys
import os
import os.path
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTimeEdit
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import QTimer

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 350)

        ##Изображение
        self.images = os.listdir("python_progs/interface/image")
        self.images.sort()
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

        ##Задание времени для таймера
        self.time_edit = QTimeEdit(self)
        self.time_edit.setFixedSize(80, 25)
        self.time_edit.move(10, 300)
        self.time_edit.setDisplayFormat("mm:ss")

        ##Таймер
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)

        ##Кнопка слайд шоу
        self.btn_slideshow = QPushButton('СЛАЙД ШОУ', self)
        self.btn_slideshow.setFixedSize(80, 25)
        self.btn_slideshow.move(100, 300)
        self.btn_slideshow.clicked.connect(self.slideshow)

        ##Поворот Изображения
        self.btn_rotate = QPushButton('ПОВОРОТ', self)
        self.btn_rotate.setFixedSize(80, 25)
        self.btn_rotate.move(250, 300)
        self.btn_rotate.clicked.connect(self.rotate_image)

        ##Кнопка удалить
        self.btn_delete = QPushButton('УДАЛИТЬ', self)
        self.btn_delete.setFixedSize(80, 25)
        self.btn_delete.move(400, 300)
        self.btn_delete.clicked.connect(self.delete_image)

    
    ##Кнопка Вперед
    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.image_update()
        self.btn_set_enabed()

    ##Кнопка Назад
    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.image_update()     
        self.btn_set_enabed()

    ##Обновление изображения
    def image_update(self):
        self.image = QPixmap(os.path.join("python_progs/interface/image", self.images[self.current_image_index]))
        self.image.scaled(400, 250)
        self.label.setPixmap(self.image)

    ##Кнопка Первое изображение
    def first_image(self):
        self.current_image_index = 0
        self.image_update()
        self.btn_set_enabed()

    ##Кнопка Последнее изображение
    def last_image(self):
        self.current_image_index = len(self.images) - 1
        self.image_update()
        self.btn_set_enabed()

    ##Проверка состояния кнопок
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
    

    ##Слайд шоу
    def slideshow(self):
        self.time_slideshow = (self.time_edit.time().minute() * 60 + self.time_edit.time().second()) * 1000
        if self.timer.isActive():
            self.timer.stop()
            self.btn_slideshow.setText('СЛАЙД ШОУ')
        else:
            self.timer.start(self.time_slideshow)
            self.btn_slideshow.setText('СТОП')

    ##Поворот изображения
    def rotate_image(self):
        transform = QTransform().rotate(90)
        self.image = self.image.transformed(transform)
        self.image.save(os.path.join("python_progs/interface/image", self.images[self.current_image_index]))
        self.image_update()

    ##Удаление изображения
    def delete_image(self):
        if os.path.exists(os.path.join("python_progs/interface/image", self.images[self.current_image_index])):
            os.remove(os.path.join("python_progs/interface/image", self.images[self.current_image_index]))
            del self.images[self.current_image_index]
            self.image_update()
            self.btn_set_enabed()
    

app = QApplication(sys.argv)
ex = MyWindow()
ex.show()
sys.exit(app.exec())
