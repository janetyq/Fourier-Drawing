import sys
from fourier_drawing_app import FourierDrawingApp
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FourierDrawingApp()
    window.show()
    sys.exit(app.exec())
    