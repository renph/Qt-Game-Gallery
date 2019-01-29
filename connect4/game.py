from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPalette, QColor, QPainter


class Connect4GameModel:
    def __init__(self):
        # empty: -1, red: 0, blue: 1
        self.board = [[-1 for _ in range(7)] for __ in range(6)]
        self.nMoves = 0
        self.lastMove = None, None, 1

    def get(self, row, col):
        if 0 <= row <= 5 and 0 <= col <= 6:
            return self.board[row][col]

    def __getitem__(self, item):
        return self.board[item]

    def isGameOver(self):
        r, c, p = self.lastMove
        if r is None:
            return
        # count number of consecutive chess in 4 directions
        dirCnt = [1 for _ in range(4)]
        consecutive = [[True, True] for _ in range(4)]
        for i in range(1, 4):  # i from 1 to 4
            dirPos = [(r - i, c, r + i, c), (r, c - i, r, c + i),
                      (r - i, c - i, r + i, c + i), (r - i, c + i, r + i, c - i)]
            for d in range(4):  # check 4 directions
                r1, c1, r2, c2 = dirPos[d]
                if consecutive[d][0]:
                    if self.get(r1, c1) == p:
                        dirCnt[d] += 1
                    else:
                        consecutive[d][0] = False
                if consecutive[d][1]:
                    if self.get(r2, c2) == p:
                        dirCnt[d] += 1
                    else:
                        consecutive[d][1] = False
                if dirCnt[d] >= 4:
                    return True
        return False

    def move(self, col):
        if 0 <= col <= 6:
            for row in range(5, -1, -1):
                if self.board[row][col] == -1:
                    self.board[row][col] = self.nMoves % 2
                    self.lastMove = row, col, self.nMoves % 2
                    self.nMoves += 1
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
                winner = ['red','blue'][self.gameModel.lastMove[-1]]
                print('Game over, {} wins'.format(winner))

    def newGame(self):
        self.isNewGame = True
        self.gameModel = Connect4GameModel()
        self.view.update()


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

        menubar = self.menuBar()
        startMenu = menubar.addMenu('start')
        startMenu.addAction('New Game', self.controller.newGame, 'ctrl+N')
        startMenu.addAction('Quit', self.close, 'ctrl+Q')

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
