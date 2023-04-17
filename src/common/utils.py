from typing import List, TypeVar


T = TypeVar("T")


def flatten(lst: List[List[T]]):
    return [item for sublist in lst for item in sublist]