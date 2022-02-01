from time import time

from PyQt5 import QtWidgets
import sys

from PyQt5.QtCore import QTimer, QThread

from lib.Plot.Widgets import FlexPlotWidget
from lib.Plot.TcpClientWorker import TcpClientWorker


class MainWindow(QtWidgets.QMainWindow):
    buffer_size: int
    flex_widget: FlexPlotWidget

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.buffer_size = 2048

        self.setWindowTitle("Live Plotting Sensor Data")
        self.flex_widget = FlexPlotWidget(time_span=5, interval=10)
        self.setCentralWidget(self.flex_widget)

        self.worker = TcpClientWorker()
        self.thread = QThread()
        self.init_thread()

        self.time_init = time()

    def init_thread(self):
        self.worker.new_data_ready.connect(self.on_data_ready)

        # 3 - Move the Worker object to the Thread object
        self.worker.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        self.worker.finished.connect(self.thread.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.worker.update_data)

        # * - Thread finished signal will close the app if you want!
        self.thread.finished.connect(app.exit)

        # 6 - Start the thread
        self.thread.start()

    def on_data_ready(self, data: dict):
        self.flex_widget.add_data(x=time() - self.time_init,
                                  thumb=data["FINGERS"]["thumb"],
                                  index=data["FINGERS"]["index"],
                                  middle=data["FINGERS"]["middle"],
                                  ring=data["FINGERS"]["ring"])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
