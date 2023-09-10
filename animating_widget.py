import sys
from math import pi
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QGraphicsScene, QGraphicsView, QPushButton, 
    QVBoxLayout, QLabel, QSlider, QGraphicsEllipseItem
)
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import Qt, QSize, QTimer 
from fourier_decomp import calculate_intermediate_points, dft, normalize_points, xy_to_complex

class AnimatingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.num_circles = 4 # default 4 circles
        self.N = 0
        self.n = 0
        self.offset = 0
        self.dft_coeffs = []
        self.circles = []
        self.lines = []
        self.drawn_points = []
        self.drawn_lines = []
        
        self.initUI()

    def initUI(self):
        # scene
        self.scene = QGraphicsScene()
        self.scene.addText("Animation!")
        self.scene.setSceneRect(0, 0, 500, 500)
        self.view = QGraphicsView(self.scene)

        # widgets
        self.num_circles_slider = QSlider(Qt.Horizontal)
        self.num_circles_slider.setMinimum(1)
        self.num_circles_slider.setMaximum(50)
        self.num_circles_slider.setValue(self.num_circles)
        self.num_circles_slider.valueChanged.connect(self.update_num_circles)
        self.label = QLabel(f" # of circles = {self.num_circles}")
        self.animating_label = QLabel("Animating!")

        # layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.animating_label)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.num_circles_slider)
        self.layout.addWidget(self.label)
        
        # animation updating
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(20)

        # pens
        self.target_drawing_pen = QPen(Qt.blue)
        self.target_drawing_pen.setWidth(2)
        self.animating_pen = QPen(Qt.red)
        self.animating_pen.setWidth(3)
        self.circle_pen = QPen(Qt.lightGray)
        self.circle_pen.setWidth(1)
        self.line_pen = QPen(Qt.black)
        self.line_pen.setWidth(1)

        
    def setup(self, line_points):
        self.clear_scene()
        if len(line_points) < 2: # default drawing
            line_points = [[250+120*np.cos(theta), 250 + 120 * np.sin(theta)] for theta in np.linspace(0, 2*pi, 5, endpoint=False)]
        line_points = normalize_points(line_points)
        self.dft_coeffs = dft(xy_to_complex(line_points))
        self.N = len(line_points)

        # draw target drawing as a whole loop
        for i in range(self.N):
            self.scene.addLine(*line_points[i-1], *line_points[i], pen=self.target_drawing_pen)
        
        # add K circles and lines
        for i in range(self.num_circles):
            circle = self.scene.addEllipse(0, 0, 0, 0, pen=self.circle_pen)
            line = self.scene.addLine(0, 0, 0, 0, pen=self.line_pen)
            self.circles.append(circle)
            self.lines.append(line)
        self.update_animation()

    def minimumSizeHint(self):
        return QSize(600, 600)

    def clear_scene(self):
        self.scene.clear()
        self.circles.clear()
        self.lines.clear()
        self.drawn_lines.clear()
        self.drawn_points.clear()
        self.offset = 0
        self.n = 0   

    def update_animation(self):
        if self.N != 0:
            intermediate_points = calculate_intermediate_points(self.dft_coeffs, self.offset + self.n, self.num_circles, self.N)
            for i in range(self.num_circles):
                curr_pos = intermediate_points[i].real, intermediate_points[i].imag
                next_pos = intermediate_points[i+1].real, intermediate_points[i+1].imag
                radius = abs(intermediate_points[i+1] - intermediate_points[i])
                self.circles[i].setRect(curr_pos[0] - radius, curr_pos[1] - radius, 2*radius, 2*radius)
                self.lines[i].setLine(*curr_pos, *next_pos)
            self.drawn_points.append(next_pos)
            if len(self.drawn_points) > 1:
                self.drawn_lines.append(self.scene.addLine(*self.drawn_points[-2], *self.drawn_points[-1], pen=self.animating_pen))
            self.n += 1
            if self.n >= self.N:
                self.reset_drawn_line()
    
    def update_num_circles(self):
        new_num_circles = self.num_circles_slider.value()
        if new_num_circles < self.num_circles:
            for i in range(new_num_circles, self.num_circles):
                self.scene.removeItem(self.circles[i])
                self.scene.removeItem(self.lines[i])
            self.circles = self.circles[:new_num_circles]
            self.lines = self.lines[:new_num_circles]
        elif new_num_circles > self.num_circles:
            for i in range(self.num_circles, new_num_circles):
                circle = self.scene.addEllipse(0, 0, 0, 0, pen=self.circle_pen)
                line = self.scene.addLine(0, 0, 0, 0, pen=self.line_pen)
                self.circles.append(circle)
                self.lines.append(line)
        self.num_circles = new_num_circles
        self.label.setText(f" # of circles = {self.num_circles}")
        self.reset_drawn_line()
        self.update_animation()

    def reset_drawn_line(self):
        self.offset = (self.offset + self.n) % self.N
        self.n = 0
        for line in self.drawn_lines:
            self.scene.removeItem(line)
        self.drawn_points.clear()
        self.drawn_lines.clear()
