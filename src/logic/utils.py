from typing import List, TypeVar, Dict
from random import sample, uniform

from .domain import IllegalArgumentError


T = TypeVar("T")
K = TypeVar("K")
L = TypeVar("L", int, float)


def get_chunks(collection: List[T], chunk_size: int):
    if chunk_size <= 0:
        raise IllegalArgumentError("Chunk size must be positive")

    return [collection[i:i+chunk_size]
            for i in range(0, len(collection), chunk_size)]


def flatten(lst: List[List[T]]):
    return [item for sublist in lst for item in sublist]


def is_bigger(a: T, b: T) -> bool:
    return a > b


def is_smaller(a: T, b: T) -> bool:
    return a < b


def is_bigger_or_equal(a: T, b: T) -> bool:
    return a >= b


def is_smaller_or_equal(a: T, b: T) -> bool:
    return a <= b


def get_random_collection(length: int, minimum=0, maximum=100, are_floats=False):
    if length <= 0:
        raise IllegalArgumentError("Length must be positive")

    if are_floats:
        return [uniform(minimum, maximum) for _ in range(length)]

    return sample(range(minimum, maximum), length)


def get_lists_from_dictionary(dictionary: Dict[T, K]):
    return [[key] + [value for value in dictionary[key]] for key in dictionary]


def get_merged_list_by(step: int):
    if step <= 0:
        raise IllegalArgumentError("Step must be positive")

    def merge(lst: List[List[T]]):
        merged_list: List[T] = []
        common_length = min([len(current_list) for current_list in lst])

        for i in range(0, common_length, step):
            for current_list in lst:
                merged_list += current_list[i:i+step]

        return merged_list

    return merge


get_merged_list_by_one = get_merged_list_by(1)


def get_average(lst: List[L]):
    return sum(lst) / len(lst)
