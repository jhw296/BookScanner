import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
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

        # Start 버튼 생성 및 스타일 설정
        button_width = 200
        button_height = 60
        button_x = (widget_width - button_width) // 2
        button_y = (widget_height - button_height) // 2 + 127

        self.start_button = QPushButton('S T A R T', self)
        self.start_button.setGeometry(button_x, button_y, button_width, button_height)
        self.start_button.setStyleSheet("background-color: #6E9EFF; color: white; border-radius: 25px; font-size: 25px; font-weight: bold;")


        # startpg_book.png 이미지 추가
        image_label = QLabel(self)
        image_path = "./img/startpg_book.png"
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(button_width)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setGeometry(button_x, button_y - pixmap.height() - 50, pixmap.width(), pixmap.height())

        self.start_button.clicked.connect(self.show_main_screen)

        self.setWindowTitle('BOOKSCANER')

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
