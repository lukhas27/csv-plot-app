from abc import ABC, abstractmethod


class PlotDataStrategy(ABC):
    group: str

    @abstractmethod
    def get_dp_lists(self, data_obj):
        pass

    @abstractmethod
    def get_group(self):
        pass

    @abstractmethod
    def get_identifier(self):
        pass
