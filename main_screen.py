import cv2
import sys
import requests
import numpy as np
import barcode_recognition as barR
import text_extraction as txtE
import txtE_screen
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal

class MainScreen(QWidget):    
    def __init__(self):
        super().__init__()
        self.image_paths = []
        self.text_list = []
        self.info_screen = None
        self.initUI()

    def initUI(self):
        # 위젯 사이즈 설정
        self.widget_width = 375
        self.widget_height = 600
        self.setFixedSize(self.widget_width, self.widget_height)

        background_image_path = "./img/bookself.png"
        self.background_image = QPixmap(background_image_path)
        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.widget_width, self.widget_height)
        
        # 책 각 위치에 출력하는 부분
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(50, 10, 10, 10)
        self.grid_layout.setSpacing(0)

        self.create_search_btn()
        
    def create_search_btn(self):
        # 버튼 생성 및 스타일 설정
        button_size = 50
        button_x = 20
        button_y = self.widget_height - button_size - 20

        btn = QPushButton(self)
        btn.setGeometry(button_x, button_y, button_size, button_size)
        btn.setStyleSheet(" border-radius: 50%;")
        btn_image_path = "./img/search_icon.png"
        
        btn_image = QPixmap(btn_image_path)
        btn_image = btn_image.scaled(button_size, button_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        icon = QIcon(btn_image)
        btn.setIcon(icon)
        btn.setIconSize(btn.size())

        btn.clicked.connect(self.barcode_recognition)
        self.setWindowTitle('mainscreen')
        
    def barcode_recognition(self):
        self.hide()
        barR.barcorde_recognition()
        self.close()
        self.show_info_screen()
    
    def show_info_screen(self):
        print('Open InfoScreen')
        self.info_screen = InfoScreen(self.image_paths)
        self.info_screen.closed.connect(self.update_image_paths)
        self.info_screen.closed.connect(self.show_main_screen)
        self.info_screen.show()

    def update_image_paths(self):
        self.image_paths = self.info_screen.image_paths
                
    def show_main_screen(self):
        # Clear grid layout
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.create_search_btn()

        for row in range(4):
            self.grid_layout.setRowMinimumHeight(row, self.widget_height // 4) 
            for col in range(3):
                self.grid_layout.setColumnMinimumWidth(col, self.widget_width // 3)
                index = row * 3 + col
                if index < len(self.image_paths):
                    if self.image_paths[row * 3 + col]:
                        image_path = self.image_paths[row * 3 + col]
                        self.create_bookimg_button(image_path, row, col)
                else:
                    continue
               
        self.show()
        
    def create_bookimg_button(self, image_path, row, col):
        self.bookimg_btn = QPushButton(self)
        self.bookimg_btn.setFixedSize(70, 100)
        pixmap = QPixmap(image_path).scaled(self.bookimg_btn.size())
        self.bookimg_btn.setIcon(QIcon(pixmap))
        self.bookimg_btn.setIconSize(self.bookimg_btn.size())
        self.bookimg_btn.clicked.connect(self.show_custom)
        self.grid_layout.addWidget(self.bookimg_btn, row, col)
        
    def show_custom(self):
        print('open MainScreen')
        # self.main_screen = pdf.CustomWidget()
        # self.main_screen = txtE.text_extraction()
        self.txtE_screen = txtE_screen.TextDetectionApp()
        self.txtE_screen.show()
        # self.hide()


class InfoScreen(QWidget):
    closed = pyqtSignal()

    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.initUI()

    def initUI(self):
        # Book information from barcode recognition
        title, author, isbn, publisher, pubdata, discount, description, image_url = barR.book_info()

        # Layout
        layout = QVBoxLayout()

        # Load and display image
        image_data = requests.get(image_url).content
        image = QPixmap()
        image.loadFromData(image_data)
        image = image.scaledToWidth(image.width() // 3)
        
        # Save image
        cap_cnt = len(self.image_paths) + 1
        image_array = np.frombuffer(image_data, np.uint8)
        save_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        save_image_path = f"./img/books/image{cap_cnt}.jpg"
        cv2.imwrite(save_image_path, save_image)
        self.image_paths.append(save_image_path)
        print(self.image_paths)
        
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
        self.emit_closed_signal()
        
    def emit_closed_signal(self):
        self.closed.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_screen = MainScreen()
    main_screen.show()
    sys.exit(app.exec_())
