from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPalette, QColor, QPainter, QPolygon, QPainterPath


class Connect4View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 700)
        self.boardSize = (70, 100, 560, 480)
        self.setMouseTracking(True)
        p = QPalette(QColor(250, 200, 10, 255))
        self.setPalette(p)
        self.mousePos = -1

    def paintEvent(self, a0: QtGui.QPaintEvent):
        painter = QPainter(self)
        pen = painter.pen()
        pen.setColor(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        board_x, board_y, board_width, board_height = self.boardSize
        for i in range(8):
            lx = board_x + i * 80
            painter.drawLine(lx, board_y, lx, board_y + board_height)
        for j in range(7):
            ly = board_y + j * 80
            painter.drawLine(board_x, ly, board_x + board_width, ly)
        brush = painter.brush()
        brush.setColor(Qt.green)
        painter.setBrush(brush)
        if 0 <= self.mousePos <= 6:
            tr_y = board_y - 20
            tr_x = board_x + self.mousePos * 80 + 40
            painter.drawPolygon(QPoint(tr_x - 20, tr_y - 20), QPoint(tr_x, tr_y), QPoint(tr_x + 20, tr_y - 20))

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        board_x, board_y, board_width, board_height = self.boardSize
        mx = (a0.x() - board_x) // 80
        self.mousePos = mx
        self.update()


if __name__ == '__main__':
    app = QApplication([])
    view = Connect4View()
    view.show()
    app.exit(app.exec_())
