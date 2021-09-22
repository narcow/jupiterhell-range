import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QComboBox, QLabel
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from jh_range import JupiterHellRangeVisualizer

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'Jupiter Hell Range Visualizer'
        self.width = 800
        self.height = 600
        self.jhv = JupiterHellRangeVisualizer()
        self.canvas = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.canvas = PlotCanvas(self, width=8, height=5.5)
        self.canvas.move(0,0)

        lbl_usage = QLabel(self)
        lbl_usage.setText('Minimum / Optimal / Maximum:')
        lbl_usage.adjustSize()
        lbl_usage.move(150,568)

        # minimum range. default: 2
        cb_range_min = QComboBox(self)
        cb_range_min.setToolTip('Minimum Range')
        cb_range_min.move(350,560)
        for i in range(1, 5):
            cb_range_min.addItem(f'{i}', i)
        cb_range_min.setCurrentIndex(cb_range_min.findData(2))
        cb_range_min.currentTextChanged.connect(self._cb_range_min_update)

        # optimal range. default: 3
        cb_range_opt = QComboBox(self)
        cb_range_opt.setToolTip('Optimal Range')
        cb_range_opt.move(450,560)
        for i in range(1, 10):
            cb_range_opt.addItem(f'{i}', i)
        cb_range_opt.setCurrentIndex(cb_range_opt.findData(3))
        cb_range_opt.currentTextChanged.connect(self._cb_range_opt_update)

        # maximum range. default: 6
        cb_range_max = QComboBox(self)
        cb_range_max.setToolTip('Maximum Range')
        cb_range_max.move(550,560)
        for i in range(3, 16):
            cb_range_max.addItem(f'{i}', i)
        cb_range_max.setCurrentIndex(cb_range_max.findData(6))
        cb_range_max.currentTextChanged.connect(self._cb_range_max_update)

        self.show()

    def _cb_range_min_update(self, value):
        try:
            min_range = int(value)
        except ValueError:
            min_range = 0
        self.jhv.gun.update(min_range=min_range)
        self.jhv.visualize(show=False, ax=self.canvas.subplot_ax)
        self.canvas.draw()

    def _cb_range_opt_update(self, value):
        self.jhv.gun.update(optimal_range=int(value))
        self.jhv.visualize(show=False, ax=self.canvas.subplot_ax)
        self.canvas.draw()

    def _cb_range_max_update(self, value):
        self.jhv.gun.update(max_range=int(value))
        self.jhv.visualize(show=False, ax=self.canvas.subplot_ax)
        self.canvas.draw()

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.subplot_ax = self.figure.add_subplot(111)
        parent.jhv.visualize(show=False, ax=self.subplot_ax)
        self.draw()

    def redraw(self):
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
