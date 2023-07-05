from PyQt5.QtWidgets import (
    QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QLabel, QPushButton
)
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QSize, Qt 

class DrawingView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.line_points = []
        self.initUI()

    def initUI(self):
        # scene
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 500, 500)
        self.setScene(self.scene)

    def setup(self):
        self.line_points.clear()
        self.scene.clear()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToScene(event.pos())
            self.line_points.append((pos.x(), pos.y()))

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            pos = self.mapToScene(event.pos())
            self.line_points.append((pos.x(), pos.y()))

            if len(self.line_points) >= 2:
                pen = QPen(Qt.blue)
                pen.setWidth(3)
                self.scene.addLine(*self.line_points[-2], *self.line_points[-1], pen=pen)

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.line_points = []
        self.initUI()

    def initUI(self):
        # scene
        self.drawing_view = DrawingView()
        self.line_points = self.drawing_view.line_points # point to same list

        # widgets
        self.drawing_label = QLabel("Drawing!")
        self.button = QPushButton("Clear", clicked=self.setup)

        # layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.drawing_label)
        self.layout.addWidget(self.drawing_view)
        self.layout.addWidget(self.button)

    def setup(self):
        self.drawing_view.setup()

    def minimumSizeHint(self):
        return QSize(600, 600)
