import unittest

from sys import path
path.append('D:\\University\\Parralel programming\\Course\\src')

from logic.algorithms import sort, sort_multithreaded
from logic.multithreading import get_optimal_threads_number
from logic.utils import get_random_collection
from logic.domain import IllegalArgumentError


class BaseAlgorithmTest:
    def set_up(self):
        self.algorithm = None
        self.algorithm_args = {}
        self.control_algorithm = sorted
        self.control_algorithm_args = {}
        self.minimum_collection_size = 10
        self.maximum_collection_size = 1_000

    def run_algorithm(self, collection):
        return self.algorithm(collection, **self.algorithm_args)

    def run_control_algorithm(self, collection, additional_args={}):
        return self.control_algorithm(collection, **self.control_algorithm_args, **additional_args)

    def test_empty_list(self):
        self.assertEqual(self.run_algorithm([]), [])

    def test_one_element_list(self):
        self.assertEqual(self.run_algorithm([1]), [1])

    def test_regular_list(self):
        collection = get_random_collection(self.minimum_collection_size)
        self.assertEqual(self.run_algorithm(collection), self.run_control_algorithm(collection))

    def test_big_list(self):
        collection = get_random_collection(
            self.maximum_collection_size, 0, self.maximum_collection_size
        )
        self.assertEqual(self.run_algorithm(collection), self.run_control_algorithm(collection))

    def test_sorted_list(self):
        sorted_collection = self.run_control_algorithm(
            get_random_collection(self.minimum_collection_size))
        self.assertEqual(
            self.run_algorithm(sorted_collection), self.run_control_algorithm(sorted_collection)
        )

    def test_list_with_duplicates(self):
        collection = get_random_collection(self.minimum_collection_size)
        collection += collection
        self.assertEqual(self.run_algorithm(collection), self.run_control_algorithm(collection))

    def test_list_with_negative_numbers(self):
        collection = get_random_collection(
            self.minimum_collection_size, -self.minimum_collection_size, 0
        )
        self.assertEqual(self.run_algorithm(collection), self.run_control_algorithm(collection))

    def test_list_with_float_numbers(self):
        collection = get_random_collection(
            self.minimum_collection_size, are_floats=True
        )
        self.assertEqual(self.run_algorithm(collection), self.run_control_algorithm(collection))


class SortAlgorithmTest(BaseAlgorithmTest):
    def set_up(self):
        super().set_up()
        self.algorithm = sort
        self.algorithm_args = {}


class SortAscendingAlgorithmTest(unittest.TestCase, SortAlgorithmTest):
    def setUp(self):
        super().set_up()


class SortDescendingAlgorithmTest(unittest.TestCase, SortAlgorithmTest):
    def setUp(self):
        super().set_up()
        self.algorithm_args['is_reversed'] = True
        self.control_algorithm_args['reverse'] = True


class SortMultithreadAlgorithmTest(BaseAlgorithmTest):
    def set_up(self):
        super().set_up()
        self.algorithm = sort_multithreaded
        self.algorithm_args = { "threads_number": get_optimal_threads_number() }

    def test_threads_number_below_zero(self):
        self.algorithm_args['threads_number'] = -1
        collection = get_random_collection(self.minimum_collection_size)
        with self.assertRaises(IllegalArgumentError):
            self.run_algorithm(collection)


class SortAscendingMultithreadedAlgorithmTest(unittest.TestCase, SortMultithreadAlgorithmTest):
    def setUp(self):
        super().set_up()


class SortDescendingMultithreadedAlgorithmTest(unittest.TestCase, SortMultithreadAlgorithmTest):
    def setUp(self):
        super().set_up()
        self.algorithm_args['is_reversed'] = True
        self.control_algorithm_args['reverse'] = True


if __name__ == '__main__':
    unittest.main()
