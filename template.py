from PyQt5 import QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication


class Model:
    def __init__(self):
        pass


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.view.show()
        self.isNewGame = True

    def newGame(self):
        self.model = Model()
        self.isNewGame = True
        self.view.update()


class View(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Game")

        meanBar = self.menuBar()
        startMenu = meanBar.addMenu("Start")
        # startMenu.addAction("New game", self.newGame, "Ctrl+N")
        startMenu.addAction("Quit", self.close, "Ctrl+Q")
        self.setMenuWidget(meanBar)

        self.setFixedSize(640, 640 + 30)
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#B1723C"))
        self.setPalette(palette)

    def paintEvent(self, a0: QtGui.QPaintEvent):
        pass

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        pass

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent):
        pass

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        pass

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        pass

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        pass


if __name__ == '__main__':
    app = QApplication([])
    game = Controller()
    app.exit(app.exec_())
