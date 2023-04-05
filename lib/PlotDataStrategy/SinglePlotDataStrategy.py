import json
import os

from lib.PlotDataStrategy.PlotDataStrategy import PlotDataStrategy


class SinglePlotDataStrategy(PlotDataStrategy):
    identifier: str
    index: int

    def __init__(self, group: str, identifier):
        self.group = group
        self.identifier = identifier

        with open(f'{os.getcwd()}/lib/data_template.json') as f:
            data_template = json.load(f)

        self.index = 0

        i = 0
        for _group in data_template.keys():
            for _identifier in data_template[_group].keys():
                if _group == group and _identifier == identifier:
                    self.index = i
                    return
                i += 1

    def get_dp_lists(self, data_objs: list) -> list:
        ret = list()
        for data_obj in data_objs:
            ret.append([data_point[self.index] for data_point in data_obj.get_data()])

        return ret

    def get_group(self):
        return self.group

    def get_identifier(self):
        return self.identifier
