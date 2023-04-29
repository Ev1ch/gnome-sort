from typing import TypeVar, List, Tuple
from math import ceil
from os import cpu_count

from .domain import IllegalArgumentError, Item
from .utils import is_last_index, is_first_index


T = TypeVar("T")
IndexedFuture = TypeVar("IndexedFuture")


def get_maximum_chunks_number(collection_length: int, minimum_chunk_size: int) -> int:
    if collection_length < 0:
        raise IllegalArgumentError("Collection length mustn't be negative")

    if minimum_chunk_size <= 0:
        raise IllegalArgumentError("Minimum chunk size must be positive")

    return ceil(collection_length / minimum_chunk_size)


def get_chunk_size(
    collection_length: int, threads_number: int, minimum_chunk_size: int
):
    if collection_length < 0:
        raise IllegalArgumentError("Collection length mustn't be negative")

    if threads_number <= 0:
        raise IllegalArgumentError("Threads number must be positive")

    if minimum_chunk_size <= 0:
        raise IllegalArgumentError("Minimum chunk size must be positive")

    maximum_chunks_number = get_maximum_chunks_number(
        collection_length, minimum_chunk_size
    )

    if threads_number > maximum_chunks_number:
        return minimum_chunk_size

    return ceil(collection_length / threads_number)


def get_optimal_threads_number():
    return max(1, cpu_count())


def get_indexed_futures_filter(indexed_futures: List[IndexedFuture]):
    def _filter(index: int, state: str):
        return list(filter(
            lambda indexed_future: indexed_future[0] == index
            and indexed_future[1]._state == state,
            indexed_futures,
        ))

    return _filter


def worker(
    index: int,
    collection: List[Item],
    chunks_indexes_pairs: List[Tuple[int, int]],
    algorithm,
    add_worker,
    filter_indexed_futures,
):
    chunks_number = len(chunks_indexes_pairs)
    indexes_pair = chunks_indexes_pairs[index]
    is_alone = chunks_number == 1
    is_first = is_first_index(index)
    is_last = is_last_index(index, chunks_number)

    start_index, end_index = indexes_pair
    start_element = collection[start_index]
    end_element = collection[end_index]

    algorithm(start_index, end_index)

    if is_alone:
        return

    are_any_pending_previously_indexed_futures = (
        len(filter_indexed_futures(index - 1, "PENDING")) > 0
    )
    if (
        not is_first
        and start_element != collection[start_index]
        and not are_any_pending_previously_indexed_futures
    ):
        add_worker(index - 1)

    are_any_pending_next_indexed_futures = (
        len(filter_indexed_futures(index + 1, "PENDING")) > 0
    )
    if (
        not is_last
        and end_element != collection[end_index]
        and not are_any_pending_next_indexed_futures
    ):
        add_worker(index + 1)


def get_scoped_worker(
    collection,
    chunks_indexes_pairs,
    algorithm,
    add_worker,
    filter_indexed_futures,
):
    def _worker(index: int):
        worker(
            index,
            collection,
            chunks_indexes_pairs,
            algorithm,
            add_worker,
            filter_indexed_futures,
        )

    return _worker
