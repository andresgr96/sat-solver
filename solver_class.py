#!/usr/bin/env python3

import sys
from collections import defaultdict
from typing import List, Dict, Tuple, Union
import os
import time
import argparse


def parse_dimacs(filename: str) -> List[List[int]]:
    """
    Parse a DIMACS CNF file into a list of clauses.

    Args:
        filename (str): Path to the DIMACS CNF file.

    Returns:
        List[List[int]]: A list of clauses, where each clause is a list of integers representing literals.
    """
    clauses = []
    with open(filename, 'r') as input_file:
        for line in input_file:
            if line[0] in ['c', 'p']:
                continue
            literals = list(map(int, line.split()))
            assert literals[-1] == 0
            literals = literals[:-1]
            clauses.append(literals)
    return clauses


def bcp(cnf: List[List[int]], unit: int) -> Union[List[List[int]], int]:
    """
    Perform Boolean Constraint Propagation (BCP) on the CNF formula.

    Args:
        cnf (List[List[int]]): The CNF formula represented as a list of clauses.
        unit (int): The literal to propagate.

    Returns:
        Union[List[List[int]], int]: The updated CNF formula after propagation,
        or -1 if a conflict is detected.
    """
    new_cnf = []
    for clause in cnf:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [literal for literal in clause if literal != -unit]
            if not new_clause:  # Empty clause found
                return -1
            new_cnf.append(new_clause)
        else:
            new_cnf.append(clause)
    return new_cnf


def assign_unit(cnf: List[List[int]]) -> Tuple[Union[List[List[int]], int], List[int]]:
    """
    Assign unit clauses iteratively and propagate their effects using BCP.

    Args:
        cnf (List[List[int]]): The CNF formula represented as a list of clauses.

    Returns:
        Tuple[Union[List[List[int]], int], List[int]]:
            The updated CNF formula and the list of assignments.
    """
    assignments = []
    unit_clauses = [clause for clause in cnf if len(clause) == 1]
    while unit_clauses:
        unit = unit_clauses[0][0]
        cnf = bcp(cnf, unit)
        assignments.append(unit)
        if cnf == -1:
            return -1, []
        if not cnf:
            return cnf, assignments
        unit_clauses = [clause for clause in cnf if len(clause) == 1]
    return cnf, assignments


class SatSolver:
    """
    A class for solving SAT problems using DPLL with different heuristics.
    """

    def __init__(self, strategy: int) -> None:
        """
        Initialize the SAT solver with the given strategy.

        Args:
            strategy (int): The strategy number (1: Basic DPLL, 2: DPLL with Jersolow-Wang,
                            3: DPLL with Jersolow-Wang 2-sided).
        """
        assert strategy in [1, 2, 3], "Invalid strategy. Must be 1, 2, or 3."
        self.strategy = strategy

    def select_literal(self, cnf: List[List[int]]) -> int:
        """
        Select the next literal to assign based on the chosen strategy.

        Args:
            cnf (List[List[int]]): The CNF formula.

        Returns:
            int: The literal to assign.
        """
        if self.strategy == 1:
            # Basic DPLL: Select the first literal in the first clause
            return cnf[0][0]
        elif self.strategy == 2:
            return self.jersolow_wang_method(cnf)
        elif self.strategy == 3:
            return self.jersolow_wang_2_sided_method(cnf)

    @staticmethod
    def jersolow_wang_method(cnf: List[List[int]]) -> int:
        """
        Apply the Jersolow-Wang heuristic to select the next variable to assign.

        Args:
            cnf (List[List[int]]): The CNF formula.

        Returns:
            int: The literal to assign.
        """
        literal_weight = defaultdict(int)
        for clause in cnf:
            for literal in clause:
                literal_weight[literal] += 2 ** -len(clause)
        return max(literal_weight, key=literal_weight.get)

    @staticmethod
    def jersolow_wang_2_sided_method(cnf: List[List[int]]) -> int:
        """
        Apply the two-sided Jersolow-Wang heuristic to select the next variable to assign.

        Args:
            cnf (List[List[int]]): The CNF formula.

        Returns:
            int: The literal to assign.
        """
        literal_weight = defaultdict(int)
        for clause in cnf:
            for literal in clause:
                literal_weight[abs(literal)] += 2 ** -len(clause)
        return max(literal_weight, key=literal_weight.get)

    def solve(self, cnf: List[List[int]], assignments: List[int] = []) -> List[int]:
        """
        Solve the SAT problem using the DPLL algorithm.

        Args:
            cnf (List[List[int]]): The CNF formula.
            assignments (List[int], optional): Current variable assignments. Defaults to [].

        Returns:
            List[int]: A satisfying assignment if SAT, otherwise an empty list.
        """
        cnf, unit_assignments = assign_unit(cnf)
        assignments += unit_assignments
        if cnf == -1:
            return []
        if not cnf:
            return assignments
        selected_literal = self.select_literal(cnf)
        result = self.solve(bcp(cnf, selected_literal), assignments + [selected_literal])
        if not result:
            result = self.solve(bcp(cnf, -selected_literal), assignments + [-selected_literal])
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A SAT solver using the DPLL algorithm with heuristics.")
    parser.add_argument('--s', type=int, required=True,
                        help='Strategy number (1: Basic DPLL, 2: DPLL with Jersolow-Wang, 3: DPLL with Jersolow-Wang 2-sided)')
    parser.add_argument('--input_file', help='Input file in DIMACS format')
    args = parser.parse_args()

    input_file = args.input_file
    assert os.path.exists(input_file), f'{input_file} does not exist.'
    clauses = parse_dimacs(input_file)

    solver = SatSolver(strategy=args.s)
    assignment = solver.solve(clauses)

    if assignment:
        print('SAT')
        assignment.sort(key=abs)
        print(assignment)
    else:
        print('UNSAT')
