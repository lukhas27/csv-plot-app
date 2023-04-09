from enum import Enum

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QGroupBox


class PlotMode(Enum):
    SINGLE = "single"
    MULTI = "multi"


class PlotModeWidget(QWidget):
    plot_mode: PlotMode
    i: int

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.plot_mode = self.parent.plot_mode
        self.i = 0
        layout = QVBoxLayout()

        self.rb_single_plot_mode = QRadioButton("Single LivePlot")
        self.rb_single_plot_mode.toggled.connect(self.on_rb_changed)
        layout.addWidget(self.rb_single_plot_mode)

        self.rb_multi_plot_mode = QRadioButton("Multi LivePlot")
        self.rb_multi_plot_mode.toggled.connect(self.on_rb_changed)
        layout.addWidget(self.rb_multi_plot_mode)

        if self.plot_mode == PlotMode.SINGLE:
            self.rb_single_plot_mode.setChecked(True)
            self.rb_multi_plot_mode.setChecked(False)

        if self.plot_mode == PlotMode.MULTI:
            self.rb_single_plot_mode.setChecked(False)
            self.rb_multi_plot_mode.setChecked(True)

        self.setLayout(layout)

    def on_rb_changed(self, value):
        # rb callback bug start at beginning, we don't want to update plot_mode on start
        if self.i != 0:
            if self.rb_single_plot_mode.isChecked():
                self.parent.update_plot_mode(PlotMode.SINGLE)
            elif self.rb_multi_plot_mode.isChecked():
                self.parent.update_plot_mode(PlotMode.MULTI)
        self.parent.plot_widget.update_data()
        self.i += 1
