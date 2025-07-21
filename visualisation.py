#import chess, chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QColor, QPalette, QPixmap
#from PyQt5.QtSvg import QSvgWidget

nr_queens = 12

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class Queen(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap('images/queen.svg')
        self.setPixmap(pixmap)

def createhorisontal():
    layout = QGridLayout()
    layout.setHorizontalSpacing(0)
    layout.setVerticalSpacing(0)
    x = 0
    for i in range(0, nr_queens):
        if i % 2 == 0:
            first = "#23461a"
            second = "#9fc797"
        else:
            first = "#9fc797"
            second = "#23461a"
        for _ in range(0, int(nr_queens/2)):
            layout.addWidget(Color(first), i, x)
            layout.addWidget(Queen(), i, x)
            x = x+1
            print(x)
            layout.addWidget(Color(second), i, x)
            x = x+1
            if x >= nr_queens:
                x = 0
    return layout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 550, 550)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        self.setPalette(palette)

        layout = createhorisontal()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()