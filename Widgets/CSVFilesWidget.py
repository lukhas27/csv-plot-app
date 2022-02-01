import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QDialogButtonBox, \
    QVBoxLayout, QApplication, QListWidget, QAbstractItemView, QListWidgetItem

from lib.CsvDataObject import CsvDataObject
from termcolor import colored

STEPS_LOOP_COLOR = 5  # steps for color loop when color should start iterating from beginning


class CSVFilesWidget(QWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        layout = QHBoxLayout()

        button_layout = QVBoxLayout()
        self.add_button = QPushButton("+")
        self.add_button.setObjectName("AddButton")
        self.add_button.clicked.connect(self.on_add_button_click)
        button_layout.addWidget(self.add_button, alignment=Qt.AlignTop)

        self.delete_button = QPushButton("-")
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.clicked.connect(self.delete_selected)
        button_layout.addWidget(self.delete_button, alignment=Qt.AlignBottom)

        layout.addLayout(button_layout)

        self.csv_list_widget = CsvFilesListWidget(self)
        layout.addWidget(self.csv_list_widget)

        self.setLayout(layout)

    def get_csv_files(self) -> list:
        fltr = "CSV (*.csv)"
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.AnyFile)
        names, _ = file_name.getOpenFileNames(self, "Open files", os.getcwd() + '/TestData', fltr)

        return names

    def on_add_button_click(self) -> None:
        csv_paths = self.get_csv_files()
        i = self.csv_list_widget.count()
        j = 0
        for csv_path in csv_paths:
            if csv_path.endswith('.csv'):
                self.csv_list_widget.add_list_item(i + j, csv_path)
                j += 1
        self.csv_list_widget.update_color()
        self.update_data_objs()

    def delete_selected(self):
        for item in self.csv_list_widget.selectedItems():
            self.csv_list_widget.takeItem(self.csv_list_widget.row(item))

        self.update_data_objs()

    def update_data_objs(self):
        buff = list()
        for i in range(self.csv_list_widget.count()):
            buff.append(CsvDataObject(self.csv_list_widget.item(i).data(Qt.DisplayRole),
                                      self.csv_list_widget.item(i).data(Qt.UserRole),
                                      self.csv_list_widget.item(i).data(Qt.BackgroundRole),
                                      self.csv_list_widget.item(i).data(Qt.CheckStateRole)))

        self.parent.update_data_objs(buff)


class CsvFilesListWidget(QListWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setObjectName("CsvFilesList")
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""background-color: gray""")
        self.itemSelectionChanged.connect(self.selection_changed)

    def selection_changed(self):
        for i in range(self.count()):
            if self.item(i) in self.selectedItems():
                self.item(i).setData(Qt.CheckStateRole, True)
            else:
                self.item(i).setData(Qt.CheckStateRole, False)

        self.parent.update_data_objs()

    def update_color(self):
        num = self.count()
        c_list = iterate_colors(num, STEPS_LOOP_COLOR)

        for i in range(num):
            self.item(i).setData(Qt.BackgroundRole, c_list[i])

    def add_list_item(self, i: int, path: str):
        item = QListWidgetItem()
        item.setData(Qt.DisplayRole, decorate_url_to_text(path, i))
        item.setData(Qt.UserRole, path)
        item.setData(Qt.CheckStateRole, False)
        item.setTextAlignment(Qt.AlignCenter)
        self.addItem(item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            return super().dragEnterEvent(event)  # return to the original event state

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            return super().dragMoveEvent(event)  # return to the original event state

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            i = self.count()
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    if url.toString().endswith('.csv'):
                        self.add_list_item(i, str(url.toLocalFile()))
                        i += 1

            self.update_color()
            self.parent.update_data_objs()

        else:
            return super().dropEvent(event)  # return to the original event state


def iterate_colors(num_colors: int, steps_loop: int):
    h_values = [int(360 / num_colors * i) for i in range(num_colors)]
    sorted_h = list()

    ret = list()
    if steps_loop + 1 < num_colors:
        for i in range(num_colors // steps_loop + 1):
            for k in range(i, num_colors, 2):
                color = QColor()
                color.setHsv(h_values[k], 255, 255, 180)
                ret.append(color)
                sorted_h.append(h_values[k])
        if num_colors % (num_colors // steps_loop + 1) == 0:
            ret.pop()
    else:
        for i in range(num_colors):
            color = QColor()
            color.setHsv(h_values[i], 255, 255, 200)
            ret.append(color)

    return ret


def decorate_url_to_text(s: str, i: int) -> str:
    strings = s.split('/')
    strings = strings[len(strings) - 2:]

    test_person, test_time = strings[1].split('_')
    test_time = test_time.replace("-", ".", 6)
    test_time = test_time.replace(".", ":", 5)
    test_time = test_time.replace(":", " ", 3)
    test_time = test_time.replace(" ", "-", 2)

    return f'[TEST {i + 1}]    Gesture: {strings[0]}    Person: {test_person}    Time: {test_time[0:19]}'
