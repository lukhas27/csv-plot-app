import json
import os

from lib.PlotDataStrategy.PlotDataStrategy import PlotDataStrategy


class MultiPlotDataStrategy(PlotDataStrategy):
    identifier_list: list
    index_list: list

    def __init__(self, group: str):
        self.group = group

        with open(f'{os.getcwd()}/lib/data_template.json') as f:
            data_template = json.load(f)

        self.identifier_list = list()

        i = 0
        for _group in data_template.keys():
            for j, identifier in enumerate(data_template[_group].keys()):
                if _group == self.group:
                    if j == 0:
                        self.index = i
                    self.identifier_list.append(identifier)
                i += 1

    def get_dp_lists(self, data_objs: list) -> list:
        ret = list()
        for data_obj in data_objs:
            buff_list = list()
            for i, _ in enumerate(self.identifier_list):
                buff_list.append([data_point[self.index + i] for data_point in data_obj])
            ret.append(buff_list)

        return ret

    def get_group(self):
        return self.group

    def get_identifier(self):
        return self.identifier_list
