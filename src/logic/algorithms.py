from typing import List
from concurrent.futures import ThreadPoolExecutor, wait

from .domain import (
    Item,
    Comparer,
    Algorithm,
    MultithreadedAlgorithm,
    IllegalArgumentError,
)
from .utils import (
    is_bigger_or_equal,
    is_smaller_or_equal,
    get_chunks_indexes_pairs,
    are_futures_done,
)
from .multithreading import (
    IndexedFuture,
    get_chunk_size,
    get_optimal_threads_number,
    get_indexed_futures_filter,
    get_scoped_worker,
)


def algorithm(
    collection: List[Item],
    comparer: Comparer[Item],
    start_index: int = 0,
    end_index: int = None,
):
    index = start_index
    current_end_index = end_index if end_index is not None else len(collection) - 1

    while index <= current_end_index:
        if index == 0 or comparer(collection[index], collection[index - 1]):
            index = index + 1
        else:
            collection[index], collection[index - 1] = (
                collection[index - 1],
                collection[index],
            )
            index = index - 1


def get_scoped_algorithm(collection: List[Item], comparer: Comparer[Item]):
    def sorter(start_index: int, end_index: int):
        algorithm(collection, comparer, start_index, end_index)

    return sorter


def gnome_sort(comparer: Comparer[Item]):
    def sorter(initial_collection: List[Item]):
        collection = initial_collection.copy()
        algorithm(collection, comparer)
        return collection

    return sorter


def gnome_sort_multithreaded(comparer: Comparer[Item], minimum_chunk_size: int):
    if minimum_chunk_size <= 1:
        raise IllegalArgumentError("Minimum chunk size must be bigger than 1")

    def sorter(initial_collection: List[Item], threads_number: int):
        if threads_number <= 0:
            raise IllegalArgumentError("Threads number must be positive")

        collection = initial_collection.copy()
        collection_length = len(collection)

        # We include 0 and 1 to avoid slicing empty list
        if collection_length <= 1:
            return collection

        chunk_size = get_chunk_size(
            collection_length, threads_number, minimum_chunk_size
        )
        chunks_indexes_pairs = get_chunks_indexes_pairs(
            collection, chunk_size, right_offset=1
        )
        chunks_number = len(chunks_indexes_pairs)
        executor = ThreadPoolExecutor(chunks_number)
        indexed_futures: List[IndexedFuture] = []
        scoped_algorithm = get_scoped_algorithm(collection, comparer)
        are_any_indexed_futures_with_state = get_indexed_futures_filter(indexed_futures)

        def add_worker(index: int):
            scoped_worker = get_scoped_worker(
                collection,
                chunks_indexes_pairs,
                scoped_algorithm,
                add_worker,
                are_any_indexed_futures_with_state,
            )

            indexed_futures.append(
                (
                    index,
                    executor.submit(
                        scoped_worker,
                        index,
                    ),
                )
            )

        for index in range(chunks_number):
            add_worker(index)

        while not are_futures_done(
            indexed_future[1] for indexed_future in indexed_futures
        ):
            futures = [indexed_future[1] for indexed_future in indexed_futures]
            wait(futures)

        executor.shutdown()

        return collection

    return sorter


sort_ascending: Algorithm = gnome_sort(is_bigger_or_equal)


sort_descending: Algorithm = gnome_sort(is_smaller_or_equal)


def sort(collection: List[Item], is_reversed=False):
    if is_reversed:
        return sort_descending(collection)

    return sort_ascending(collection)


sort_ascending_multithreaded: MultithreadedAlgorithm = gnome_sort_multithreaded(
    is_bigger_or_equal, 2
)


sort_descending_multithreaded: MultithreadedAlgorithm = gnome_sort_multithreaded(
    is_smaller_or_equal, 2
)


def sort_multithreaded(
    collection: List[Item],
    threads_number=get_optimal_threads_number(),
    is_reversed=False,
):
    if is_reversed:
        return sort_descending_multithreaded(collection, threads_number)

    return sort_ascending_multithreaded(collection, threads_number)
