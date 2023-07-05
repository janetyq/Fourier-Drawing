from drawing_widget import DrawingWidget
from animating_widget import AnimatingWidget
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

DRAW_MODE = 0
ANIMATE_MODE = 1

class FourierDrawingApp(QMainWindow):
    def __init__(self):
        super(FourierDrawingApp, self).__init__()
        self.mode = DRAW_MODE
        self.initUI()

    def initUI(self):
        # main
        self.setWindowTitle("Fourier Drawing")
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
    
        # widgets
        self.drawing_widget = DrawingWidget()
        self.animating_widget = AnimatingWidget()
        self.switch = QPushButton("Draw/Animate")
        self.switch.clicked.connect(self.switch_mode)

        # layout
        self.layout.addWidget(self.switch)
        self.layout.addWidget(self.drawing_widget)
        self.layout.addWidget(self.animating_widget)
        self.animating_widget.hide()
        self.mode = DRAW_MODE

        self.show()

    def switch_mode(self):
        if self.mode == DRAW_MODE:
            self.mode = ANIMATE_MODE
            self.drawing_widget.hide()
            self.animating_widget.show()
            self.animating_widget.setup(self.drawing_widget.line_points)
        else:
            self.mode = DRAW_MODE
            self.animating_widget.hide()
            self.drawing_widget.show()
            self.drawing_widget.setup()
            