import sys
import requests
import barcode_recognition as barR
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class InfoScreen(QWidget):
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    info_screen = InfoScreen()
    info_screen.show()
    sys.exit(app.exec_())
    