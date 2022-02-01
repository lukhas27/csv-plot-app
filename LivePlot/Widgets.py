from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from pyqtgraph import PlotWidget, PlotCurveItem, PlotDataItem, mkPen, AxisItem


# class for one Finger with label name and the live plot of the values
class FlexSensor:
    name: str
    time_span: float
    color: tuple
    x: list
    y: list

    def __init__(self, name: str, time_span: float, color: tuple):
        self.name = name
        self.time_span = time_span
        self.color = color
        self.x = list()
        self.y = list()

    def add_datapoint(self, x: float, y: int):
        self.add_x(x)
        self.add_y(y, x)

    def add_x(self, value: float):
        # if length of list is greater than the number of shown data points remove first item in list
        if value > self.time_span:
            self.x = self.x[1:]

        self.x.append(value)  # Add a new value 1 higher than the last.

    def add_y(self, value: int, last_x: float):
        # if length of list is greater than the number of shown data points remove first item in list
        if last_x > self.time_span:
            self.y = self.y[1:]
        self.y.append(value)  # Add a new value 1 higher than the last.

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_data(self):
        return self.x, self.y


class FlexPlotWidget(PlotWidget):
    time_span: float

    def __init__(self, time_span: float = 5, interval: int = 50):
        """
        :param time_span: time span in seconds which should be shown by plot
        :param interval: time interval in which th plot should be updated
        """
        super().__init__()
        self.time_span = time_span

        self.getPlotItem().setTitle("Flex Sensor Data")  # set Title of Widget
        self.setRange(xRange=(0, self.time_span), yRange=(0, 110))  # set x range to 0 ... 500
        self.setBackground('black')

        self.getPlotItem().setLabel(axis='left', text='value of flexsensor')
        self.getPlotItem().setLabel(axis='bottom', text='time (s)')

        self.flex_thumb = FlexSensor("thumb", self.time_span, (255, 0, 0))
        self.flex_index = FlexSensor("index", self.time_span, (255, 255, 0))
        self.flex_middle = FlexSensor("middle", self.time_span, (0, 255, 0))
        self.flex_ring = FlexSensor("ring", self.time_span, (0, 0, 255))

        # create LivePlot Curve Items
        self.curve_thumb = PlotDataItem(pen=mkPen(color=self.flex_thumb.get_color()))
        self.curve_index = PlotCurveItem(pen=mkPen(color=self.flex_index.get_color()))
        self.curve_middle = PlotCurveItem(pen=mkPen(color=self.flex_middle.get_color()))
        self.curve_ring = PlotCurveItem(pen=mkPen(color=self.flex_ring.get_color()))

        self.add_plot_items()  # add items to PlotItem
        self.legend = self.getPlotItem().addLegend(offset=(0, 10), colCount=4)
        self.init_legend()  # initialize Legend

        self.timer = QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        x, y = self.flex_thumb.get_data()
        self.curve_thumb.setData(x, y)
        self.curve_index.setData(*self.flex_index.get_data())
        self.curve_middle.setData(*self.flex_middle.get_data())
        self.curve_ring.setData(*self.flex_ring.get_data())

        if x:
            if x[-1] > self.time_span:
                self.setXRange(x[-1] - self.time_span, x[-1])

    def add_data(self, x: float, thumb: int, index: int, middle: int, ring: int):
        self.flex_thumb.add_datapoint(x, thumb)
        self.flex_index.add_datapoint(x, index)
        self.flex_middle.add_datapoint(x, middle)
        self.flex_ring.add_datapoint(x, ring)

    def add_plot_items(self):
        self.getPlotItem().addItem(self.curve_thumb)
        self.getPlotItem().addItem(self.curve_index)
        self.getPlotItem().addItem(self.curve_middle)
        self.getPlotItem().addItem(self.curve_ring)

    def init_legend(self):
        self.legend.addItem(self.curve_thumb, self.flex_thumb.get_name())
        self.legend.addItem(self.curve_index, self.flex_index.get_name())
        self.legend.addItem(self.curve_middle, self.flex_middle.get_name())
        self.legend.addItem(self.curve_ring, self.flex_ring.get_name())