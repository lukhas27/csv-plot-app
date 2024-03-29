import csv
import tkinter as tk
from os import listdir

import numpy as np

from lib.CsvDataObject import CsvDataObject


def find_csv_filenames(directory_path, suffix=".csv"):
    """
    :param directory_path: path to search for csv files
    :param suffix: suffix of the desired files
    :return: list of all names of the csv files from the desired directory.
    """
    filenames = listdir(directory_path)
    return [directory_path + '/' + filename for filename in filenames if filename.endswith(suffix)]


class CsvFilesReader:
    csv_files_list: list

    def __init__(self, csv_files_list: list):
        """
        Read Data out of a list of paths from csv files

        :param csv_files_list: list of file path strings of csv files that want to be plotted
        """
        self.csv_files_list = csv_files_list

    def get_data_of_csv_files(self) -> list:
        """
        Get all data of the csv files in the asked directory in List of data objects.

        :return: list of data objects.
        """
        data_objects = list()
        for file in self.csv_files_list:
            with open(file, 'r') as f:
                reader = csv.reader(f)

                data_object = list()

                for i, row in enumerate(reader):
                    if i != 0:
                        data_object.append([float(val) for val in row])

            data_objects.append(data_object)

        return data_objects