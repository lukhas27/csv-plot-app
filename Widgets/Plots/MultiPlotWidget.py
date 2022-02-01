import json
import os

from pyqtgraph import PlotItem, mkPen

from Widgets.Plots.IPlotWidget import IPlotWidget
from lib.PlotDataStrategy.MultiPlotDataStrategy import MultiPlotDataStrategy


class MultiPlotWidget(IPlotWidget):
    plot_items: list

    def __init__(self, plot_data_strategy: MultiPlotDataStrategy = None, data_objs: list = None):
        super().__init__(plot_data_strategy, data_objs)
        self.plot_items = list()

        with open(f'{os.getcwd()}/lib/data_template.json') as f:
            self.data_template = json.load(f)

        self.set_plot_data_strategy(plot_data_strategy)

    def update_data(self):
        self.__clear_plot_items()
        if self._data_objs:
            self._data_lists = self._plot_data_strategy.get_dp_lists([item.get_data() for item in self._data_objs])
            self.plot_data()

    def plot_data(self):
        """
        LivePlot Data of one sensor group with the amount of plots like the identifiers.
        """
        if self._data_lists and self._plot_data_strategy:
            for i, data_list in enumerate(self._data_lists):
                for j, plot_item in enumerate(self.plot_items):
                    if self._data_objs[i].get_checked():
                        plot_item.plot(data_list[j], pen=mkPen(color=self._data_objs[i].get_color(), width=3))
                    else:
                        plot_item.plot(data_list[j], pen=mkPen(color=self._data_objs[i].get_color(), width=1))

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

        for identifier in identifiers:
            plot_item = PlotItem()
            plot_item.setLabel(axis='left', text=f'{group}[{identifier}]')

            self.addItem(plot_item)
            self.nextRow()
            self.plot_items.append(plot_item)

    def __clear_plot_items(self):
        for plot_item in self.plot_items:
            plot_item.clear()
