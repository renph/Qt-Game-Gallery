from PyQt5 import QtGui
from PyQt5.QtCore import QThread, Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QPainter
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication


class TicTacToeModel:
    def __init__(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.nextMove = 1
        self.lastMove = (0, 0, 0)
        self.nMove = 0

    def __getitem__(self, item):
        return self.board[item]

    def get(self, row, col):
        if 0 <= row <= 2 and 0 <= col <= 2:
            return self.board[row][col]

    def move(self, row, col):
        # print('move to',row,col)
        self.board[row][col] = self.nextMove
        self.lastMove = row, col, self.nextMove
        self.nextMove = 0 - self.nextMove
        self.nMove += 1

    def isGameOver(self):
        r, c, p = self.lastMove
        if p == 0:
            return False
        if self.nMove > 8:
            return True
        # count number of consecutive chess in 4 directions
        dirCnt = [1 for _ in range(4)]
        consecutive = [[True, True] for _ in range(4)]
        for i in range(1, 3):  # i from 1 to 2
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
                if dirCnt[d] >= 3:
                    return True
        return False


class TicTacToeController:
    def __init__(self):
        self.model = TicTacToeModel()
        self.view = TicTacToeView(self)
        self.view.show()

        self.isNewGame = True

    def newGame(self):
        self.model = TicTacToeModel()
        self.isNewGame = True
        self.view.update()

    def move(self, row, col):
        if self.isNewGame:
            if 0 <= row <= 2 and 0 <= col <= 2 and self.model[row][col] == 0:
                self.model.move(row, col)
                self.view.update()
                if self.model.isGameOver():
                    self.isNewGame = False
                    print("Game over")


class TicTacToeView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Tic Tac Toe")

        meanBar = self.menuBar()
        startMenu = meanBar.addMenu("Start")
        # startMenu.addAction("New game", self.newGame, "Ctrl+N")
        startMenu.addAction("Quit", self.close, "Ctrl+Q")
        self.setMenuWidget(meanBar)

        # self.resize(QSize(640, 640))
        self.setFixedSize(640, 640 + 30 + 30)
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#B1723C"))
        self.setPalette(palette)

        self.boardSize = 20, 20 + 30, 600, 600

    def paintEvent(self, a0: QtGui.QPaintEvent):
        puzzleSize = 3
        painter = QPainter(self)
        pen = painter.pen()
        pen.setColor(QColor("#8D5822"))
        pen.setWidth(7)
        painter.setPen(pen)

        brush = painter.brush()
        brush.setColor(QColor("#EEC085"))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        font = painter.font()
        font.setFamily("consolas")
        font.setBold(True)
        font.setPointSize(180 // puzzleSize)  # 60-3 45-4
        painter.setFont(font)

        board_x, board_y, board_width, board_height = self.boardSize
        painter.drawRect(board_x, board_y, board_width, board_height)
        board_div = 600 // puzzleSize
        for i in range(puzzleSize - 1):
            painter.drawLine(board_div * (i + 1) + board_x, board_y, board_div * (i + 1) + board_x,
                             board_y + board_height)
            painter.drawLine(board_x, board_div * (i + 1) + board_y, board_x + board_width,
                             board_div * (i + 1) + board_y)

        for i in range(3):
            for j in range(3):
                p = self.controller.model.get(j, i)
                if p == 0:
                    continue
                if p == 1:
                    pen.setColor(QColor("#db0000"))
                    painter.setPen(pen)
                    painter.drawLine(board_x + board_div * i + 50, board_y + board_div * j + 50,
                                     board_x + board_div * i + 150, board_y + board_div * j + 150)
                    painter.drawLine(board_x + board_div * i + 50, board_y + board_div * j + 150,
                                     board_x + board_div * i + 150, board_y + board_div * j + 50)
                elif p == -1:
                    pen.setColor(QColor("#00468b"))
                    painter.setPen(pen)
                    painter.drawEllipse(QPoint(board_x + board_div * i + 100,
                                               board_y + board_div * j + 100),
                                        60, 60)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        board_x, board_y, board_width, board_height = self.boardSize
        my = (a0.x() - board_x) // 200
        mx = (a0.y() - board_y) // 200
        self.controller.move(mx, my)


if __name__ == '__main__':
    app = QApplication([])
    game = TicTacToeController()
    app.exit(app.exec_())
