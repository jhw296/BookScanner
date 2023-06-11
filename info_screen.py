import sys
from PyQt5.QtWidgets import *
import barcode_recognition as barR

class InfoScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title, author = barR.book_info()
        print(title, author)
        self.title_label = QLabel(title, self)
        self.title_label.move(50, 50)
        
        self.author_label = QLabel(author, self)
        self.author_label.move(50, 80)
        
        self.setWindowTitle('info Screen')
        self.author_label.setGeometry(50, 50, 200, 50)