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
