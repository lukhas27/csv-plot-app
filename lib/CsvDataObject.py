import json
import os

from PyQt5.QtGui import QColor


class CsvDataObject:
    name: str
    path: str
    color: QColor
    checked: bool
    data: list

    def __init__(self, name: str, path: str, color: QColor, checked: bool):
        super().__init__()
        self.name = name
        self.path = path
        self.color = color
        self.checked = checked

        with open(f'{os.getcwd()}/lib/data_template.json') as f:
            data_template = json.load(f)

        buff_list = list()
        for group in data_template.keys():
            try:
                keys = data_template[group].keys()
                for identifier in data_template[group].keys():
                    buff_list.append(list())
            except AttributeError:
                buff_list.append(list())

        self.data = buff_list

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def get_color(self):
        return self.color

    def get_checked(self):
        return self.checked

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
