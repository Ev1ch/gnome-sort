from os import cpu_count
from math import ceil

from .domain import IllegalArgumentError


def get_maximum_chunks_number(collection_length: int, minimum_chunk_size=2):
    if collection_length < 0:
        raise IllegalArgumentError("Collection length mustn't be negative")

    if minimum_chunk_size <= 0:
        raise IllegalArgumentError("Minimum chunk size must be positive")

    return ceil(collection_length / minimum_chunk_size)


def get_chunk_size(collection_length: int, threads_number: int, minimum_chunk_size=2):
    if collection_length < 0:
        raise IllegalArgumentError("Collection length mustn't be negative")
    
    if threads_number <= 0:
        raise IllegalArgumentError("Threads number must be positive")

    if minimum_chunk_size <= 0:
        raise IllegalArgumentError("Minimum chunk size must be positive")

    maximum_chunks_number = get_maximum_chunks_number(collection_length, minimum_chunk_size)

    if threads_number > maximum_chunks_number:
        return maximum_chunks_number

    return ceil(collection_length / threads_number)


def get_optimal_threads_number():
    return max(1, cpu_count() // 2)
