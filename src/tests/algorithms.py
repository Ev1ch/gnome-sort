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
        self.algorithm_args = ()
        self.minimum_collection_size = 10
        self.maximum_collection_size = 1_000

    def run_algorithm(self, collection):
        return self.algorithm(collection, *self.algorithm_args)

    def test_empty_list(self):
        self.assertEqual(self.run_algorithm([]), [])

    def test_one_element_list(self):
        self.assertEqual(self.run_algorithm([1]), [1])

    def test_regular_list(self):
        collection = get_random_collection(self.minimum_collection_size)
        self.assertEqual(self.run_algorithm(collection), sorted(collection))

    def test_big_list(self):
        collection = get_random_collection(
            self.maximum_collection_size, 0, self.maximum_collection_size)
        self.assertEqual(self.run_algorithm(collection), sorted(collection))

    def test_sorted_list(self):
        sorted_collection = sorted(
            get_random_collection(self.minimum_collection_size))
        self.assertEqual(self.run_algorithm(
            sorted_collection), sorted(sorted_collection))

    def test_reversed_list(self):
        reversed_collection = sorted(get_random_collection(
            self.minimum_collection_size), reverse=True)
        self.assertEqual(self.run_algorithm(
            reversed_collection), sorted(reversed_collection))

    def test_list_with_duplicates(self):
        collection = get_random_collection(self.minimum_collection_size)
        collection += collection
        self.assertEqual(self.run_algorithm(collection), sorted(collection))

    def test_list_with_negative_numbers(self):
        collection = get_random_collection(
            self.minimum_collection_size, -self.minimum_collection_size, 0)
        self.assertEqual(self.run_algorithm(collection), sorted(collection))

    def test_list_with_float_numbers(self):
        collection = get_random_collection(
            self.minimum_collection_size, are_floats=True)
        self.assertEqual(self.run_algorithm(collection), sorted(collection))


class TestAlgorithm(unittest.TestCase, BaseAlgorithmTest):
    def setUp(self):
        super().set_up()
        self.algorithm = sort


class TestMultithreadAlgorithm(unittest.TestCase, BaseAlgorithmTest):
    def setUp(self):
        super().set_up()
        self.algorithm = sort_multithreaded
        self.algorithm_args = get_optimal_threads_number(),

    def test_threads_number_below_zero(self):
        self.algorithm_args = -1,
        collection = get_random_collection(self.minimum_collection_size)
        with self.assertRaises(IllegalArgumentError):
            self.run_algorithm(collection)


if __name__ == '__main__':
    unittest.main()
