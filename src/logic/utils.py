from typing import List, TypeVar, Dict
from random import sample, uniform
from concurrent.futures import Future

from .domain import IllegalArgumentError


T = TypeVar("T")
K = TypeVar("K")
L = TypeVar("L", int, float)


def get_chunks_indexes_pairs(
    collection: List[T], chunk_size: int, left_offset=0, right_offset=0
):
    if chunk_size <= 0:
        raise IllegalArgumentError("Chunk size must be positive")

    start_index = 0
    end_index = len(collection) - 1
    return [
        (
            max(start_index, i - left_offset),
            min(end_index, i + chunk_size - 1 + right_offset),
        )
        for i in range(0, len(collection), chunk_size)
    ]


def is_bigger(a: T, b: T) -> bool:
    return a > b


def is_smaller(a: T, b: T) -> bool:
    return a < b


def is_bigger_or_equal(a: T, b: T) -> bool:
    return a >= b


def is_smaller_or_equal(a: T, b: T) -> bool:
    return a <= b


def is_sorted(collection: List[T], comparer):
    return all(
        comparer(collection[i + 1], collection[i]) for i in range(len(collection) - 1)
    )


def get_random_collection(length: int, minimum: int, maximum: int, are_floats=False):
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
                merged_list += current_list[i : i + step]

        return merged_list

    return merge


get_merged_list_by_one = get_merged_list_by(1)


def get_average(lst: List[L]):
    return sum(lst) / len(lst)


def is_last_index(index: int, collection_length: int):
    return index == collection_length - 1


def is_first_index(index: int):
    return index == 0


def is_middle_index(index: int, collection_length: int):
    return (
        not is_first_index(index)
        and not is_last_index(index, collection_length)
        and collection_length > 2
    )


def are_futures_done(futures: List[Future]):
    return all(future.done() for future in futures)
