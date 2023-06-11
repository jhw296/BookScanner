import sys
from PyQt5.QtWidgets import *
from main_screen import MainScreen

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.main_screen = None
        self.initUI()

    def initUI(self):
        self.start_button = QPushButton('START', self)
        self.start_button.clicked.connect(self.show_main_screen)
        self.setWindowTitle('Start page')
        
    def show_main_screen(self):
        print('open MainScreen')
        self.main_screen = MainScreen()
        self.main_screen.show()
        # self.hide()