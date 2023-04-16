from typing import Callable, TypeVar, List


Item = TypeVar("Item", int, float, complex)
Comparer = Callable[[Item, Item], bool]
Flatter = Callable[[List[List[Item]]], List[Item]]
Algorithm = Callable[[List[Item]], List[Item]]
MultithreadedAlgorithm = Callable[[List[Item], int], List[Item]]


class IllegalArgumentError(ValueError):
    pass
