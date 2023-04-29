from timeit import default_timer as timer
from datetime import timedelta
from tabulate import tabulate

from files.utils import get_list_from_file
from logic.utils import get_lists_from_dictionary
from constants import ALL_ALGORITHMS, MULTITHREADED_ALGORITHMS, DATA


COLLECTION_SIZES = [
    20_000,
]
THREADS_NUMBERS = [
    16,
]
TIMES_TO_RUN = 1
OUTPUT_FILE_PATH = "G:\\My Drive\\Course\\Результати.txt"


def get_time_delta(start: float, end: float):
    return timedelta(seconds=end - start)


def get_list_by_size(collection_size: int):
    return get_list_from_file(DATA[collection_size])


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
        [collection_size for collection_size in COLLECTION_SIZES] * TIMES_TO_RUN
    ]
    results = dict()

    for _ in range(TIMES_TO_RUN):
        for size in COLLECTION_SIZES:
            collection = get_list_by_size(size)

            for algorithm_name, algorithm in ALL_ALGORITHMS:
                is_multithreaded = algorithm_name in [
                    item[0] for item in MULTITHREADED_ALGORITHMS
                ]

                if is_multithreaded:
                    if len(THREADS_NUMBERS) > 0:
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
                                get_time_delta(start, end)
                            )
                        else:
                            results[algorithm_name] = [
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

    results_lists = get_lists_from_dictionary(results)
    table += results_lists
    format_table(table)
    tabulated_table = tabulate(table, headers="firstrow")

    results_file = open(OUTPUT_FILE_PATH, "w")
    results_file.write(tabulated_table)
    results_file.close()

    print(tabulated_table)
