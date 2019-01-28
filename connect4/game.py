from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPalette, QColor, QPainter, QPolygon, QPainterPath


class Connect4GameModel:
    def __init__(self):
        # empty: -1, red: 0, blue: 1
        self.board = [[-1 for _ in range(7)] for __ in range(6)]
        self.nMoves = 0
        self.lastMove = None

    def __getitem__(self, item):
        return self.board[item]

    def isGameOver(self):
        directions = [(0, 1), (-1, 1), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
        for d in range(7):
            print()
        return True

    def move(self, col):
        if 0 <= col <= 6:
            for i in range(-1, -7, -1):
                if self.board[i][col] == -1:
                    self.board[i][col] = self.nMoves % 2
                    self.nMoves += 1
                    self.lastMove = col
                    return True


class Connect4GameController:
    def __init__(self):
        self.view = Connect4View(self)
        self.view.show()
        self.isNewGame = True
        self.gameModel = Connect4GameModel()

    def move(self, col):
        if self.isNewGame and 0 <= col <= 6 and self.gameModel[0][col] == -1:
            print("move to {}".format(col))
            self.gameModel.move(col)
            self.view.update()
            if self.gameModel.isGameOver():
                self.isNewGame = False

    def newGame(self):
        self.isNewGame = True


class Connect4View(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.setFixedSize(700, 700)
        self.boardSize = (70, 100, 560, 480)
        self.setMouseTracking(True)
        p = QPalette(QColor(255, 250, 205, 255))
        self.setPalette(p)
        self.mousePos = -1

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == Qt.LeftButton:
            if self.mousePos != -1:
                self.controller.move(self.mousePos)

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
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        if 0 <= self.mousePos <= 6:
            tr_y = board_y - 20
            tr_x = board_x + self.mousePos * 80 + 40
            painter.drawPolygon(QPoint(tr_x - 20, tr_y - 20), QPoint(tr_x, tr_y), QPoint(tr_x + 20, tr_y - 20))

        for col in range(7):
            for row in range(5, -1, -1):
                piece = self.controller.gameModel[row][col]
                if piece == -1:
                    break
                if piece == 0:
                    brush.setColor(QColor("#db0000"))
                else:
                    brush.setColor(QColor("#00468b"))
                painter.setBrush(brush)
                painter.drawEllipse(QPoint(board_x + col * 80 + 40, board_y + row * 80 + 40), 35, 35)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        board_x, board_y, board_width, board_height = self.boardSize
        mx = (a0.x() - board_x) // 80
        self.mousePos = mx
        self.update()


if __name__ == '__main__':
    app = QApplication([])
    game = Connect4GameController()
    app.exit(app.exec_())
