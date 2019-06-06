import math
from typing import List, Tuple

from prettytable import PrettyTable


class SimplexType:
    MAXIMIZE = "MAXIMIZE"
    MINIMIZE = "MINIMIZE"


class Simplex:
    """
    Assume Y = c1 * x1 + c2 * x2 + .. + cn * xn
    Y is the function to optimize
    c1, c2, ... cn are the coefficients of x1, x2, ..., xn from the function

    Each restriction has the following format:
    c11 * x1 + c12 * x2 + .. + c1n * xn <INEQUALITY_TYPE> = C1
    c21 * x1 + c22 * x2 + .. + c2n * x2 <INEQUALITY_TYPE> = C2
    ...
    cn1 * x1 + cn2 * x2 + .. + cnn * xn <INEQUALITY_TYPE> = CN

    Where:
        cij = coefficient of xj from inequality i
        x1, x2, x3 are variables from each inequality
        <INEQUALITY_TYPE> can be "<=" ">=" or "=="
        C1, C2 .. CN is right side member
    """

    # TABLE: coefficients .. helper_variables .. Y ..  constants

    def __init__(self, function: List[float], restrictions: List[Tuple[List, str, float]], simplex_type: SimplexType):
        self.__original_function = function
        self.__table = []

        self.__optimized_values = []
        self.__maximum = None

        # rewrite objective function depending on the SimplexType
        self.__function = function if simplex_type == SimplexType.MINIMIZE else list(map(lambda x: x * -1, function))

        self.__restrictions = restrictions

        for ((coefficients, inequality_type, total), line_number) in zip(restrictions, range(len(restrictions))):
            self.__table.append(
                coefficients
                +
                [(1 if inequality_type == "<=" else -1 if inequality_type == ">=" else 0)
                 if i == line_number else 0 for i in range(len(restrictions))]
                +
                [0]
                +
                [total]
            )
        # rewrite the function
        self.__function += ([0] * len(self.__restrictions)) + [1, 0]

    def print_system(self):
        # table header

        headers = [f"x{i}" for i in range(len(self.__restrictions))] + \
                  [f"v{i}" for i in range(len(self.__restrictions))] + \
                  ["Y", "C"]

        data = [[f"{c}" for c in line] for line in self.__table] + [[f"{c}" for c in self.__function]]

        table = PrettyTable()
        table.field_names = headers
        table._rows = data

        print(table)

    def get_optimized_values(self):
        if self.__maximum is None:
            self.optimize()

        return self.__optimized_values, self.__maximum

    def optimize(self):
        while any(map(lambda x: x < 0, self.__function)):
            # Select pivot line and pivot row
            pivot_row = self.__function.index(min(self.__function))

            pivot_line, _ = min(filter(lambda x: x[1] > 0,
                                       zip(range(len(self.__table)),
                                           [self.__table[line][-1] / self.__table[line][pivot_row]
                                            if self.__table[line][pivot_row] != 0 else math.inf
                                            for line in range(len(self.__table))
                                            ])),
                                key=lambda x: x[1])

            # Select the pivot value and divide each element from pivot line with the pivot value
            pivot_value = self.__table[pivot_line][pivot_row]

            self.__table[pivot_line] = [c / pivot_value for c in self.__table[pivot_line]]

            pivot_value = self.__table[pivot_line][pivot_row]

            # Get the line's number that need to be changed
            line_numbers_to_change = list(range(len(self.__table)))
            line_numbers_to_change.remove(pivot_line)

            # Subtract each line with pivot line * multiplier
            for line_number in line_numbers_to_change:
                multiplier = self.__table[line_number][pivot_row] / pivot_value
                self.__table[line_number] = [self.__table[line_number][i] - multiplier * self.__table[pivot_line][i]
                                             for i in range(len(self.__table[line_number]))]

            # Subtract from function the pivot line * multiplier
            multiplier = self.__function[pivot_row] / pivot_value
            self.__function = [self.__function[i] - multiplier * self.__table[pivot_line][i]

                               for i in range(len(self.__function))]

        self.__optimized_values = [
            self.__table[var_number][-1] if sum([self.__table[l][var_number] for l in range(len(self.__table))]) == 1
            else 0
            for var_number in range(len(self.__table))

        ]

        self.__maximum = self.__function[-1]
