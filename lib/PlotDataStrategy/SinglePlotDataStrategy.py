import json
import os

import numpy as np

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
            if data_template[_group]:
                for _identifier in data_template[_group].keys():
                    if _group == group and _identifier == identifier:
                        self.index = i
                        return
                    i += 1
            self.index = i

    def get_dp_lists(self, data_objs: list):
        ret = list()
        ref_time = 0
        for data_obj in data_objs:
            buff = list()
            for i, data_point in enumerate(data_obj.get_data()):
                if i == 0:
                    ref_time = data_point[len(data_point) - 1]
                # append data value and time in sec
                buff.append([data_point[self.index], (data_point[len(data_point) - 1] - ref_time)/1000])
            ret.append(np.array(buff).transpose())

        return ret

    def get_group(self):
        return self.group

    def get_identifier(self):
        return self.identifier
