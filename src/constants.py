from typing import List, Tuple

from logic.domain import Algorithm, MultithreadedAlgorithm, Flatter
from logic.algorithms import (
    sort_ascending,
    sort_descending,
    sort_ascending_multithreaded_flatten,
    sort_descending_multithreaded_flatten,
    sort_ascending_multithreaded_by_one,
    sort_descending_multithreaded_by_one,
)
from logic.utils import flatten, get_merged_list_by_one


AlgorithmVariant = Tuple[str, Algorithm | MultithreadedAlgorithm]
FlatterVariant = Tuple[str, Flatter]


SIMPLE_ALGORITHMS: List[AlgorithmVariant] = [
    ("sort_ascending", sort_ascending),
    # ('sort_descending', sort_descending)
]

MULTITHREADED_ALGORITHMS: List[AlgorithmVariant] = [
    ("sort_ascending_multithreaded_flatten", sort_ascending_multithreaded_flatten),
    # ('sort_ascending_multithreaded_by_one', sort_ascending_multithreaded_by_one),
    # ('sort_descending_multithreaded_flatten',
    #  sort_descending_multithreaded_flatten),
    # ('sort_descending_multithreaded_by_one', sort_descending_multithreaded_by_one)
]

ALL_ALGORITHMS: List[AlgorithmVariant] = [
    ("sort_ascending", sort_ascending),
    ("sort_ascending_multithreaded_flatten", sort_ascending_multithreaded_flatten),
    # ('sort_ascending_multithreaded_by_one', sort_ascending_multithreaded_by_one),
    # ("sort_descending", sort_descending),
    # ("sort_descending_multithreaded_flatten", sort_descending_multithreaded_flatten),
    # ("sort_descending_multithreaded_by_one", sort_descending_multithreaded_by_one),
]

FLATTERS: List[FlatterVariant] = [
    ("flatten", flatten),
    # ("get_merged_list_by_one", get_merged_list_by_one),
]
