import pickle
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt5.QtNetwork import QTcpSocket


class TcpClientWorker(QObject):
    new_data_ready = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.buffer_size = 2048
        self._socket = QTcpSocket()
        self.connect_tcp_socket()

    def connect_tcp_socket(self):
        self._socket.connectToHost('localhost', 8421)
        self._socket.waitForConnected(3000)
        print("Host connected")
        self._socket.writeData(bytes("receiver", "utf-8"))

    @pyqtSlot()
    def update_data(self):
        sensor_data = dict()
        try:
            while True:
                if self._socket.waitForReadyRead(3000):
                    bytes_buff = self._socket.read(self.buffer_size)

                    if bytes_buff:
                        data = pickle.loads(bytes_buff)
                        self.new_data_ready.emit(data)

        finally:
            self._socket.close()
            self.finished.emit()
