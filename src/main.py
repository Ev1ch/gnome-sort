from timeit import default_timer as timer
from datetime import timedelta
from tabulate import tabulate

from logic.utils import get_random_collection, get_lists_from_dictionary, get_average, flatten
from logic.multithreading import get_optimal_threads_number
from constants import ALL_ALGORITHMS, MULTITHREADED_ALGORITHMS


COLLECTION_SIZES = [5_000, 10_000, 20_000]
THREADS_NUMBERS = [get_optimal_threads_number(), 10, 20]
TIMES_TO_RUN = 3


def get_time_delta(start: float, end: float):
    return timedelta(seconds=end - start).microseconds


def get_formatted_time_delta(start: float, end: float):
    return f"{get_time_delta(start, end):,}ms"


def format_row(row):
    for index, item in enumerate(row):
        if type(item) is int or type(item) is float:
            row[index] = f"{item:,}"


def format_table(table):
    for row in table:
        format_row(row)


if __name__ == "__main__":
    table = [
        ["Algorithm"] +
        flatten([[collection_size] * TIMES_TO_RUN for collection_size in COLLECTION_SIZES]) +
        ["Average"]
    ]
    results = dict()

    for size in COLLECTION_SIZES:
        for _ in range(TIMES_TO_RUN):
            collection = get_random_collection(size, 0, size)

            for algorithm_name, algorithm in ALL_ALGORITHMS:
                is_multithreaded = algorithm_name in [
                    item[0] for item in MULTITHREADED_ALGORITHMS
                ]

                if is_multithreaded:
                    for threads_number in THREADS_NUMBERS:
                        start = timer()
                        algorithm(collection, threads_number)
                        end = timer()
                        result_algorithm_name = f"{algorithm_name}_{threads_number}"

                        if result_algorithm_name in results:
                            results[result_algorithm_name].append(
                                get_time_delta(start, end)
                            )
                        else:
                            results[result_algorithm_name] = [
                                get_time_delta(start, end)
                            ]
                else:
                    start = timer()
                    algorithm(collection)
                    end = timer()

                    if algorithm_name in results:
                        results[algorithm_name].append(
                            get_time_delta(start, end))
                    else:
                        results[algorithm_name] = [
                            get_time_delta(start, end)]

    results_lists = [
        [*lst, round(get_average(lst[1:]))]
        for lst in get_lists_from_dictionary(results)
    ]
    table += results_lists
    format_table(table)

    print(tabulate(table, headers="firstrow", ))
