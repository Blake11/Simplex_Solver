from unittest import TestCase

from simplex_solver import Simplex, SimplexType


class TestSimplex(TestCase):
    def test_optimize_example(self):
        function = [2, 3, 4]
        restrictions = [
            ([1, 1, 1], "<=", 30),
            ([2, 1, 3], ">=", 60),
            ([1, -1, 2], "<=", 20)
        ]
        expected_output = ([0, 40/3, 50/3], 320/3)

        simplex = Simplex(function, restrictions, simplex_type=SimplexType.MAXIMIZE)
        simplex.optimize()

        self.assertEqual(simplex.get_optimized_values(), expected_output)

    def test_optimize_example_o(self):
        function = [6, 5, 4]
        restrictions = [
            ([2, 1, 1], "<=", 180),
            ([1, 3, 2], "<=", 300),
            ([2, 1, 2], "<=", 240)
        ]
        expected_output = ([48.0, 84.0, 0], 708.0)

        simplex = Simplex(function, restrictions, simplex_type=SimplexType.MAXIMIZE)
        simplex.optimize()

        self.assertEqual(simplex.get_optimized_values(), expected_output)

    def test_optimize_first(self):
        function = [2, 3, -1]
        restrictions = [
            ([3, 6, 0], "<=", 30),
            ([4, 2, 1], "<=", 20),
            ([0, 1, 1], "<=", 10)
        ]
        expected_output = ([3.333333333333333, 3.3333333333333335, 0], 50/3)

        simplex = Simplex(function, restrictions, simplex_type=SimplexType.MAXIMIZE)
        simplex.optimize()

        self.assertEqual(simplex.get_optimized_values(), expected_output)
