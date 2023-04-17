from typing import List, Tuple

from logic.domain import Algorithm, MultithreadedAlgorithm, Flatter
from logic.algorithms import sort, sort_multithreaded


AlgorithmVariant = Tuple[str, Algorithm | MultithreadedAlgorithm]
FlatterVariant = Tuple[str, Flatter]


SIMPLE_ALGORITHMS: List[AlgorithmVariant] = [
    ("sort", sort),
]

MULTITHREADED_ALGORITHMS: List[AlgorithmVariant] = [
    ("sort_multithreaded", sort_multithreaded),
]

ALL_ALGORITHMS: List[AlgorithmVariant] = [
    ("sort", sort),
    ("sort_multithreaded", sort_multithreaded),
]

DATA_ROOT_PATH = "D:\\University\\Parralel programming\\Course\\src\\data"

DATA = {
    1_000: DATA_ROOT_PATH + "\\1000.csv",
    2_000: DATA_ROOT_PATH + "\\2000.csv",
    3_000: DATA_ROOT_PATH + "\\3000.csv",
    5_000: DATA_ROOT_PATH + "\\5000.csv",
    8_000: DATA_ROOT_PATH + "\\8000.csv",
    10_000: DATA_ROOT_PATH + "\\10000.csv",
}