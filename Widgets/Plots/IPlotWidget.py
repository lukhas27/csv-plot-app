from pyqtgraph import GraphicsLayoutWidget

from lib.PlotDataStrategy import PlotDataStrategy


class IPlotWidget(GraphicsLayoutWidget):
    _plot_data_strategy: PlotDataStrategy
    _data_objs: list
    _data_lists: list

    def __init__(self, plot_data_strategy: PlotDataStrategy, data_objs: list, **kargs):
        super().__init__(**kargs)
        self._plot_data_strategy = plot_data_strategy
        self._data_objs = data_objs

        self.setBackground(None)


    def set_data_objects(self, data_objs: list):
        """
        Give the LivePlot Widget a list of one data point or multiple data points
        each with data from one csv file or multiple csv files.

        :param data_objs: list of data objects.
        """
        self._data_objs = data_objs
        if self._plot_data_strategy:
            self.update_data()

    def update_data(self):
        pass

    def plot_data(self):
        pass
