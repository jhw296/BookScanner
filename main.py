import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLable
from PyQt5.QtWidgets import *
from start_screen import StartScreen
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_screen = StartScreen()

    start_screen.show()

    sys.exit(app.exec_())