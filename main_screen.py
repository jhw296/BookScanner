import sys
import requests
import barcode_recognition as barR
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.info_screen = None
        self.initUI()

    def initUI(self):
        # 위젯 사이즈 설정
        widget_width = 375
        widget_height = 600
        self.setFixedSize(widget_width, widget_height)

        # 버튼 생성 및 스타일 설정
        button_size = 100
        button_x = 20
        button_y = widget_height - button_size - 20

        btn = QPushButton('barcode', self)
        btn.setGeometry(button_x, button_y, button_size, button_size)
        btn.setStyleSheet("background-color: #f0f0f0; border-radius: 50%; font-size: 18px;")

        btn.clicked.connect(self.barcode_recognition)

        self.setWindowTitle('Quit Button')

    def barcode_recognition(self):
        self.hide()
        barR.barcorde_recognition()
        # self.close()
        self.show_info_screen()
    
    def show_info_screen(self):
        print('Open InfoScreen')
        self.info_screen = InfoScreen()
        self.info_screen.closed.connect(self.show_main_screen)
        self.info_screen.show()

    def show_main_screen(self):
        self.show()
        self.info_screen = None

class InfoScreen(QWidget):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Book information from barcode recognition
        title, author, isbn, publisher, pubdata, discount, description, image_url = barR.book_info()
        # print(title, author)

        # Layout
        layout = QVBoxLayout()

        # Load and display image
        image_data = requests.get(image_url).content
        image = QPixmap()
        image.loadFromData(image_data)
        image = image.scaledToWidth(image.width() // 3)
        
        # Display image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(image)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Display title
        self.title_label = QLabel(title, self)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Display author
        self.author_label = QLabel(author, self)
        self.author_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.author_label)
        
        # Display isbn
        self.isbn_label = QLabel(isbn, self)
        self.isbn_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.isbn_label)
        
        # Display publisher
        self.publisher_label = QLabel(publisher, self)
        self.publisher_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.publisher_label)
        
        # Display pubdata
        self.pubdata_label = QLabel(pubdata, self)
        self.pubdata_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pubdata_label)

        # Display discount
        self.discount_label = QLabel(discount, self)
        self.discount_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.discount_label)
        
        # Display description
        self.description_scroll_area = QScrollArea()
        self.description_scroll_area.setWidgetResizable(True)
        self.description_label = QLabel(description, self)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_scroll_area.setWidget(self.description_label)
        layout.addWidget(self.description_scroll_area)
        
        
        self.setLayout(layout)
        self.setWindowTitle('Info Screen')
        self.setStyleSheet("background-color: white;")

    def closeEvent(self, event):
        self.closed.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_screen = MainScreen()
    main_screen.show()
    sys.exit(app.exec_())
