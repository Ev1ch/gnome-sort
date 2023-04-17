from typing import List
from concurrent.futures import ThreadPoolExecutor

from .domain import Item, Comparer, Flatter, Algorithm, MultithreadedAlgorithm, IllegalArgumentError
from .utils import is_bigger_or_equal, is_smaller_or_equal, get_chunks, flatten, get_merged_list_by_one
from .multithreading import get_chunk_size


def gnome_sort(comparer: Comparer[Item]):
    def sorter(initial_collection: List[Item]):
        index = 0
        collection = initial_collection.copy()
        collection_length = len(collection)

        while index < collection_length:
            if index == 0 or comparer(collection[index], collection[index - 1]):
                index = index + 1
            else:
                collection[index], collection[index -
                                              1] = collection[index-1], collection[index]
                index = index - 1

        return collection

    return sorter


def gnome_sort_multithreaded(comparer: Comparer[Item], flatter: Flatter[Item]):
    def sorter(collection: List[Item],  threads_number: int):
        if threads_number <= 0:
            raise IllegalArgumentError("Threads number must be positive")

        collection_length = len(collection)

        # We include 0 and 1 to avoid slicing empty list
        if collection_length <= 1:
            return collection.copy()

        chunk_size = get_chunk_size(collection_length, threads_number)
        chunks = get_chunks(collection, chunk_size)
        chunks_number = len(chunks)
        executor = ThreadPoolExecutor(chunks_number)
        sorted_chunks = [
            sorted_chunk for sorted_chunk in executor.map(
                gnome_sort(comparer), chunks
            )
        ]

        return gnome_sort(comparer)(flatter(sorted_chunks))

    return sorter


sort_ascending: Algorithm = gnome_sort(is_bigger_or_equal)


sort_descending: Algorithm = gnome_sort(is_smaller_or_equal)


sort_ascending_multithreaded_flatten: MultithreadedAlgorithm = gnome_sort_multithreaded(
    is_bigger_or_equal, flatten
)


sort_descending_multithreaded_flatten: MultithreadedAlgorithm = gnome_sort_multithreaded(
    is_smaller_or_equal, flatten
)


sort_ascending_multithreaded_by_one: MultithreadedAlgorithm = gnome_sort_multithreaded(
    is_bigger_or_equal, get_merged_list_by_one
)


sort_descending_multithreaded_by_one: MultithreadedAlgorithm = gnome_sort_multithreaded(
    is_bigger_or_equal, get_merged_list_by_one
)
