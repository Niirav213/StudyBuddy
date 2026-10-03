from PyQt6.QtWidgets import QApplication, QWidget, QPushButton , QVBoxLayout
import sys
from PyQt6 import

def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Blank Window")
    window.resize(800, 601)


    layout = QVBoxLayout()
    start_button = QPushButton("Start Focus Session")

    layout.addWidget(start_button)
    window.setLayout(layout)


    window.show()

    sys.exit(app.exec())

if __name__=="__main__":
    main()