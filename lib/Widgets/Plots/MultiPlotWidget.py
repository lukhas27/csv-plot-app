import json
import os

from pyqtgraph import PlotItem, mkPen

from lib.Widgets.Plots.IPlotWidget import IPlotWidget
from lib.PlotDataStrategy.MultiPlotDataStrategy import MultiPlotDataStrategy


class MultiPlotWidget(IPlotWidget):
    plot_items: list

    def __init__(self, plot_data_strategy: MultiPlotDataStrategy = None, data_objs: list = None):
        super().__init__(plot_data_strategy, data_objs)
        self.plot_items = list()
        self.set_plot_data_strategy(plot_data_strategy)
        self.__update_plot_items()

    def update_data(self):
        self.__clear_plot_items()
        if self._data_objs:
            data = self._plot_data_strategy.get_dp_lists(self._data_objs)
            self.plot_data(data)

    def plot_data(self, data):
        """
        LivePlot Data of one sensor group with the amount of plots like the identifiers.
        """
        if data and self._plot_data_strategy:
            for i in range(len(data)):
                for j, plot_item in enumerate(self.plot_items):
                    if self._data_objs[i].get_checked():
                        plot_item.plot(x=data[i][len(data[i])-1], y=data[i][j], pen=mkPen(color=self._data_objs[i].get_color(), width=3))
                    else:
                        plot_item.plot(x=data[i][len(data[i])-1], y=data[i][j], pen=mkPen(color=self._data_objs[i].get_color(), width=1))

    def get_plot_data_strategy(self) -> MultiPlotDataStrategy:
        return self._plot_data_strategy

    def set_plot_data_strategy(self, plot_data_strategy: MultiPlotDataStrategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """
        self._plot_data_strategy = plot_data_strategy
        self.__update_plot_items()
        self.update_data()

    def __update_plot_items(self):
        """
        Update the plot items with the set group and identifiers and add it to
        the list of plot items.
        """
        for plot_item in self.plot_items:
            self.removeItem(plot_item)
        self.plot_items.clear()

        group = self._plot_data_strategy.get_group()
        identifiers = self._plot_data_strategy.get_identifier()

        for i, identifier in enumerate(identifiers):
            plot_item = PlotItem()
            plot_item.setLabel(axis='left', text=f'{group}[{identifier}]')
            if i == len(identifiers) - 1:
                plot_item.setLabel(axis='bottom', text='time [sec]')

            self.addItem(plot_item)
            self.nextRow()
            self.plot_items.append(plot_item)

    def __clear_plot_items(self):
        for plot_item in self.plot_items:
            plot_item.clear()
