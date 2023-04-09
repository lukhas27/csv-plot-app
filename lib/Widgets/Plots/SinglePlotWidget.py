from pyqtgraph import PlotItem, mkPen

from lib.Widgets.Plots.IPlotWidget import IPlotWidget
from lib.PlotDataStrategy.SinglePlotDataStrategy import SinglePlotDataStrategy


class SinglePlotWidget(IPlotWidget):
    def __init__(self, plot_data_strategy: SinglePlotDataStrategy = None, data_objs: list = None):
        super().__init__(plot_data_strategy, data_objs)
        self.plot_item = PlotItem()
        self.__update_labels()
        self.addItem(self.plot_item)

    def update_data(self):
        self.plot_item.clear()
        if self._data_objs:
            data = self._plot_data_strategy.get_dp_lists(self._data_objs)
            self.plot_data(data)

    def plot_data(self, data):
        """
        LivePlot Data with different colors
        """
        if data and self._plot_data_strategy:
            for i in range(len(self._data_objs)):
                if self._data_objs[i].get_checked():
                    self.plot_item.plot(x=data[i][1], y=data[i][0],
                                        pen=mkPen(color=self._data_objs[i].get_color(), width=3))
                else:
                    self.plot_item.plot(x=data[i][1], y=data[i][0],
                                        pen=mkPen(color=self._data_objs[i].get_color(), width=1))

    def set_plot_data_strategy(self, plot_data_strategy: SinglePlotDataStrategy) -> None:
        self._plot_data_strategy = plot_data_strategy
        self.__update_labels()

    def __update_labels(self):
        group = self._plot_data_strategy.get_group()
        identifier = self._plot_data_strategy.get_identifier()
        self.plot_item.setTitle(f'LivePlot values of {group}[{identifier}]')  # set Title of Widget
        self.plot_item.setLabel(axis='left', text=f'{group}[{identifier}]')
        self.plot_item.setLabel(axis='bottom', text='data-points')
