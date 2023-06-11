import sys
from PyQt5.QtWidgets import *
from main_screen import MainScreen

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.main_screen = None
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")

        # 위젯 사이즈 설정
        widget_width = 375
        widget_height = 600
        self.setFixedSize(widget_width, widget_height)

        # 버튼 생성 및 스타일 설정
        button_width = 200
        button_height = 60
        button_x = (widget_width - button_width) // 2
        button_y = (widget_height - button_height) // 2 + 200

        self.start_button = QPushButton('START', self)
        self.start_button.setGeometry(button_x, button_y, button_width, button_height)
        self.start_button.setStyleSheet("background-color: #f0f0f0; border-radius: 30px; font-size: 18px;")

        self.start_button.clicked.connect(self.show_main_screen)

        self.setWindowTitle('Start Page')

    def show_main_screen(self):
        print('open MainScreen')
        self.main_screen = MainScreen()
        self.main_screen.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_screen = StartScreen()
    start_screen.show()
    sys.exit(app.exec_())