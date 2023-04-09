from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import *

from lib.Widgets.Plots.MultiPlotWidget import MultiPlotWidget
from lib.CsvFilesReader import CsvFilesReader
from lib.PlotDataStrategy.MultiPlotDataStrategy import *
from lib.PlotDataStrategy.SinglePlotDataStrategy import *
from lib.Widgets.CSVFilesWidget import CSVFilesWidget
from lib.Widgets.PlotDataWidget import PlotDataWidget
from lib.Widgets.PlotModeWidget import *
from lib.Widgets.Plots.SinglePlotWidget import SinglePlotWidget

with open(f'{os.getcwd()}/lib/data_template.json') as f:
    data_template = json.load(f)

    for _group in data_template.keys():
        INIT_GROUP = _group
        for _identifier in data_template[_group]:
            INIT_IDENTIFIER = _identifier
            break
        break

css_file_path = 'lib/Widgets/stylesheet.css'
file = QFile(css_file_path)
file.open(QFile.ReadOnly | QFile.Text)
GLOBAL_STYLES = QTextStream(file).readAll()

HEADER_MAX_HEIGHT = 150


class MainWindow(QMainWindow):
    data_objs: list
    plot_mode: PlotMode
    single_plot_data_strategy: SinglePlotDataStrategy
    multi_plot_data_strategy: MultiPlotDataStrategy

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.data_objs = list()
        self.plot_mode = PlotMode.SINGLE
        self.single_plot_data_strategy = SinglePlotDataStrategy(INIT_GROUP, INIT_IDENTIFIER)
        self.multi_plot_data_strategy = MultiPlotDataStrategy(INIT_GROUP)

        self.setWindowTitle("Plot Sensor Data of CSV Files")
        self.resize(1200, 800)
        self.setStyleSheet(GLOBAL_STYLES)

        self.layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        layout_csv = QHBoxLayout()
        csv_widget = QWidget()
        csv_widget.setObjectName("CsvWidget")
        csv_widget.setMaximumHeight(HEADER_MAX_HEIGHT)
        # gb_csv_files.setStyleSheet("border: 1px solid gray; border-radius: 13px")
        self.csv_files_widget = CSVFilesWidget(self)
        layout_csv.addWidget(self.csv_files_widget)
        csv_widget.setLayout(layout_csv)
        header_layout.addWidget(csv_widget)

        layout_mode_data = QHBoxLayout()
        mode_data_widget = QWidget()
        mode_data_widget.setObjectName("ModeDataWidget")
        mode_data_widget.setMaximumHeight(HEADER_MAX_HEIGHT)
        self.plot_mode_widget = PlotModeWidget(self)
        layout_mode_data.addWidget(self.plot_mode_widget)

        self.plot_data_widget = PlotDataWidget(self)
        layout_mode_data.addWidget(self.plot_data_widget)
        mode_data_widget.setLayout(layout_mode_data)
        header_layout.addWidget(mode_data_widget)
        self.layout.addLayout(header_layout)

        self.plot_widget = SinglePlotWidget(self.single_plot_data_strategy, self.data_objs)
        self.layout.addWidget(self.plot_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def update_plot_data_strategy(self, group: str, identifier: str = None):
        if self.plot_mode == PlotMode.SINGLE:
            self.set_single_plot_data_strategy(SinglePlotDataStrategy(group, identifier))
            self.plot_widget.set_plot_data_strategy(self.single_plot_data_strategy)
        else:
            self.set_multi_plot_data_strategy(MultiPlotDataStrategy(group))
            self.plot_widget.set_plot_data_strategy(self.multi_plot_data_strategy)

    def update_data_objs(self, data_objs: list):
        csv_reader = CsvFilesReader([item.get_path() for item in data_objs])
        all_files = csv_reader.get_data_of_csv_files()
        for i, data_obj in enumerate(data_objs):
            data_obj.set_data(all_files[i])
        self.set_data_objs(data_objs)
        self.plot_data_widget.update_plot_data_strategy()
        self.plot_widget.set_data_objects(data_objs)

    def update_plot_mode(self, plot_mode: PlotMode):
        self.set_plot_mode(plot_mode)
        group, identifier = self.plot_data_widget.get_cbs()
        self.plot_widget.setVisible(False)
        self.layout.removeWidget(self.plot_widget)
        if self.plot_mode == PlotMode.SINGLE:
            self.plot_widget = SinglePlotWidget(SinglePlotDataStrategy(group, identifier), self.data_objs)
        elif self.plot_mode == PlotMode.MULTI:
            self.plot_widget = MultiPlotWidget(MultiPlotDataStrategy(group), self.data_objs)
        self.layout.addWidget(self.plot_widget)
        self.plot_widget.setVisible(True)
        self.plot_data_widget.update_plot_data_strategy()
        self.plot_data_widget.update_cbs()

    def set_data_objs(self, data_objs: list):
        self.data_objs = data_objs

    def set_plot_mode(self, plot_mode: PlotMode):
        self.plot_mode = plot_mode

    def set_single_plot_data_strategy(self, plot_data_strategy: SinglePlotDataStrategy):
        self.single_plot_data_strategy = plot_data_strategy

    def set_multi_plot_data_strategy(self, plot_data_strategy: MultiPlotDataStrategy):
        self.multi_plot_data_strategy = plot_data_strategy

    def get_plot_mode(self) -> PlotMode:
        return self.plot_mode
