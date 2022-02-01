from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QVBoxLayout, QListView

from Widgets.PlotModeWidget import PlotMode
from lib.PlotDataStrategy.SinglePlotDataStrategy import *


class PlotDataWidget(QWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        layout = QHBoxLayout()

        self.cb_layout = QVBoxLayout()
        self.cb_group = GroupCB()
        lv_group = QListView()
        self.cb_group.setView(lv_group)
        self.cb_group.currentTextChanged.connect(self.on_cb_group_changed)
        self.cb_layout.addWidget(self.cb_group)


        self.cb_identifier = IdentifierCB(self.cb_group.currentText())
        lv_identifier = QListView()
        self.cb_identifier.setView(lv_identifier)
        self.cb_identifier.currentTextChanged.connect(self.on_cb_identifier_changed)
        self.cb_layout.addWidget(self.cb_identifier)
        layout.addLayout(self.cb_layout)

        self.setLayout(layout)

    """
    Callbacks
    """

    def on_cb_identifier_changed(self):
        self.__update_plot_data_strategy()

    def on_cb_group_changed(self):
        self.cb_layout.removeWidget(self.cb_identifier)
        self.__init_identifier_cb()
        self.__update_plot_data_strategy()

    def get_cbs(self) -> tuple:
        return self.cb_group.currentText(), self.cb_identifier.currentText()

    def update_cbs(self):
        self.cb_layout.removeWidget(self.cb_group)
        self.cb_layout.removeWidget(self.cb_identifier)

        self.cb_layout.addWidget(self.cb_group)
        self.__init_identifier_cb()

        # if self.parent.get_plot_mode() == PlotMode.SINGLE:
        #     pass
        # else:
        #     self.cb_identifier.setVisible(False)

    """
    Private Methods
    """

    def __update_plot_data_strategy(self):
        group = self.cb_group.currentText()
        if self.parent.get_plot_mode() == PlotMode.SINGLE:
            identifier = self.cb_identifier.currentText()
            self.parent.update_plot_data_strategy(group, identifier)
        else:
            self.parent.update_plot_data_strategy(group)

    def __init_identifier_cb(self):
        self.cb_identifier = IdentifierCB(self.cb_group.currentText())
        self.cb_identifier.currentTextChanged.connect(self.on_cb_identifier_changed)
        if self.parent.get_plot_mode() == PlotMode.SINGLE:
            self.cb_layout.addWidget(self.cb_identifier)
            self.cb_identifier.setVisible(True)

        else:
            self.cb_identifier.setVisible(False)


class GroupCB(QComboBox):
    def __init__(self):
        super().__init__()

        with open(f'{os.getcwd()}/lib/data_template.json') as f:
            data_template = json.load(f)

            for group in data_template.keys():
                self.addItem(group)


class IdentifierCB(QComboBox):
    def __init__(self, group: str):
        super().__init__()

        with open(f'{os.getcwd()}/lib/data_template.json') as f:
                data_template = json.load(f)

                for _group in data_template.keys():
                    if _group == group:
                        for identifier in data_template[group].keys():
                            self.addItem(identifier)


