from typing import List, Tuple

from logic.domain import Algorithm, MultithreadedAlgorithm
from logic.algorithms import sort, sort_multithreaded


SIMPLE_ALGORITHMS: List[Tuple[str, Algorithm]] = [
    ("sort", sort),
]

MULTITHREADED_ALGORITHMS: List[Tuple[str, MultithreadedAlgorithm]] = [
    ("sort_multithreaded", sort_multithreaded),
]

ALL_ALGORITHMS = SIMPLE_ALGORITHMS + MULTITHREADED_ALGORITHMS

DATA_ROOT_PATH = "D:\\University\\Parralel programming\\Course\\src\\data"

DATA = {
    1_000: DATA_ROOT_PATH + "\\1000.csv",
    2_000: DATA_ROOT_PATH + "\\2000.csv",
    3_000: DATA_ROOT_PATH + "\\3000.csv",
    5_000: DATA_ROOT_PATH + "\\5000.csv",
    8_000: DATA_ROOT_PATH + "\\8000.csv",
    10_000: DATA_ROOT_PATH + "\\10000.csv",
    20_000: DATA_ROOT_PATH + "\\20000.csv",
    30_000: DATA_ROOT_PATH + "\\30000.csv",
    50_000: DATA_ROOT_PATH + "\\50000.csv",
    80_000: DATA_ROOT_PATH + "\\80000.csv",
    100_000: DATA_ROOT_PATH + "\\100000.csv",
}