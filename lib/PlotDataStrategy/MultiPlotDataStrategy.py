import json
import os

import numpy as np

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
            if data_template[_group]:
                for j, identifier in enumerate(data_template[_group].keys()):
                    if _group == self.group:
                        if j == 0:
                            self.index = i
                        self.identifier_list.append(identifier)
                    i += 1

    def get_dp_lists(self, data_objs: list):
        ret = list()
        for data_obj in data_objs:
            buff = list()
            time_buff = list()
            for i, _ in enumerate(self.identifier_list):
                index_buff = list()
                for j, data_point in enumerate(data_obj.get_data()):

                    index_buff.append(data_point[self.index + i])
                    if i == len(self.identifier_list) - 1:
                        # time in sec
                        time_buff.append((data_point[len(data_point) - 1]) / 1000)
                buff.append(index_buff)
            buff.append(time_buff)
            ret.append(np.array(buff))

        return ret

    def get_group(self):
        return self.group

    def get_identifier(self):
        return self.identifier_list
