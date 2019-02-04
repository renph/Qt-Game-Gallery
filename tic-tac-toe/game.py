from PyQt5 import QtGui
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QPalette, QColor, QPainter
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication


class TicTacToeModel:
    def __init__(self):
        self.board = [0 for _ in range(9)]


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
        self.setFixedSize(640, 640 + 30+ 30)
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

if __name__ == '__main__':
    app = QApplication([])
    game = TicTacToeController()
    app.exit(app.exec_())
