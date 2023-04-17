from sys import path
path.append('D:\\University\\Parralel programming\\Course\\src')

from common.utils import flatten


def get_table_from_csv_file(path: str):
    with open(path, "r") as file:
        return [line.split(',') for line in file]


def get_list_from_file(path: str):
    return [float(item) for item in flatten(get_table_from_csv_file(path))]
