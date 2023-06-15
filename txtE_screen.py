import cv2
import pytesseract
from PyQt5 import QtWidgets, QtGui, QtCore
import text_extraction as txtE

class TextDetectionApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(TextDetectionApp, self).__init__()

        self.setWindowTitle("Text Detection")
        self.setGeometry(0, 0, 375, 600)
        self.setStyleSheet("background-color: #F0F5FA;")
        widget_width = 375
        widget_height = 600
        self.setFixedSize(widget_width, widget_height)

        self.text_box = QtWidgets.QTextEdit(self)
        self.text_box.setGeometry(10, 10, 355, 495)  # Adjusted text box size
        self.text_box.setFont(QtGui.QFont("Arial", 12))
        self.text_box.setStyleSheet("background-color: white; border-radius: 10px;")

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        self.text_box.setGraphicsEffect(shadow)

        self.add_button = QtWidgets.QPushButton("구절 추가하기", self)
        self.add_button.setGeometry(10, 515, 355, 35)  # Adjusted button size
        self.add_button.setStyleSheet("background-color: #6E9EFF; color: white; font-size: 15px; font-weight: bold; border-radius: 10px; font-family: 'Arial';")
        self.add_button.clicked.connect(self.add_text)

        self.complete_button = QtWidgets.QPushButton("완료", self)
        self.complete_button.setGeometry(10, 555, 355, 35)  # Adjusted button size
        self.complete_button.setStyleSheet("background-color: #6E9EFF; color: white; font-size: 15px; font-weight: bold; border-radius: 10px; font-family: 'Arial';")
        self.complete_button.clicked.connect(self.show_text_list)

        self.text_list = []

        self.create_menu()

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        return opening

    def detect_text(self, image_path):
        image = cv2.imread(image_path)
        preprocessed_image = self.preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed_image)
        self.text_box.setPlainText(text)

    def open_image(self):
        file_dialog = QtWidgets.QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if image_path:
            self.detect_text(image_path)

    def add_text(self):
        current_text = self.text_box.toPlainText()
        self.text_list.append(current_text)
        print(f"Added text: {current_text}")
        print(self.text_list)

        self.text_box.clear()  # 텍스트 박스 내용 지우기

    def open_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to open camera.")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def create_menu(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        open_action = QtWidgets.QAction("Open Image", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        camera_menu = main_menu.addMenu("Camera")
        open_camera_action = QtWidgets.QAction("Open Camera", self)
        open_camera_action.triggered.connect(self.show_txtE)
        camera_menu.addAction(open_camera_action)

    def show_txtE(self):
        self.txtE_screen = txtE.text_extraction()
        self.text_box.setPlainText(self.txtE_screen)
        # print(self.txtE_screen)

    def create_gui(self):
        self.show()

    def run(self):
        QtWidgets.QApplication.instance().exec_()

    def show_text_list(self):
        self.complete_window = QtWidgets.QMainWindow()
        self.complete_window.setWindowTitle("M E M O")
        self.complete_window.setGeometry(200, 200, 375, 600)
        self.complete_window.setStyleSheet("background-color: #F0F5FA;")

        main_widget = QtWidgets.QWidget(self.complete_window)
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        main_layout.setAlignment(QtCore.Qt.AlignTop)  # Set vertical alignment to top

        for text in self.text_list:
            label = QtWidgets.QLabel(main_widget)
            label.setFont(QtGui.QFont("Arial", 12))
            label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
            label.setText(text)
            label.setStyleSheet("background-color: #F1EA8B;")
            label.adjustSize()  # Adjust the label size to fit the text content

            main_layout.addWidget(label)

        self.complete_window.setCentralWidget(main_widget)
        self.complete_window.show()




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TextDetectionApp()
    window.create_gui()
    window.run()