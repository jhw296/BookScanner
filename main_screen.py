import sys
import barcode_recognition as barR
from info_screen import InfoScreen
from PyQt5.QtWidgets import *

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.info_screen = None
        self.initUI()

    def initUI(self):
        btn = QPushButton('barcode', self)
        btn.move(20,20)
        # print(btn.sizeHint())
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.barcode_recognition)

        self.setWindowTitle('Quit Button')
        self.setGeometry(100,100,200,100)

    def barcode_recognition(self):
        self.hide()
        barR.barcorde_recognition()
        self.close()
        self.show_info_screen()
    
    def show_info_screen(self):
        print('Open InfoScreen')
        self.info_screen = InfoScreen()
        self.info_screen.show()
        # self.hide()