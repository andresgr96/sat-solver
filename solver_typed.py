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


def jersolow_wang_method(cnf: List[List[int]]) -> int:
    """
    Apply the Jersolow-Wang heuristic to select the next variable to assign.

    Args:
        cnf (List[List[int]]): The CNF formula represented as a list of clauses.

    Returns:
        int: The literal to assign based on the heuristic.
    """
    literal_weight = defaultdict(int)
    for clause in cnf:
        for literal in clause:
            literal_weight[literal] += 2 ** -len(clause)
    return max(literal_weight, key=literal_weight.get)


def jersolow_wang_2_sided_method(cnf: List[List[int]]) -> int:
    """
    Apply the two-sided Jersolow-Wang heuristic to select the next variable to assign.
    This considers only the absolute value of literals.

    Args:
        cnf (List[List[int]]): The CNF formula represented as a list of clauses.

    Returns:
        int: The literal to assign based on the heuristic.
    """
    literal_weight = defaultdict(int)
    for clause in cnf:
        for literal in clause:
            literal_weight[abs(literal)] += 2 ** -len(clause)
    return max(literal_weight, key=literal_weight.get)


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


def backtrack(cnf: List[List[int]], assignments: List[int]) -> List[int]:
    """
    Perform the DPLL backtracking algorithm to solve the SAT problem.

    Args:
        cnf (List[List[int]]): The CNF formula represented as a list of clauses.
        assignments (List[int]): The current list of variable assignments.

    Returns:
        List[int]: A satisfying assignment if the formula is SAT, otherwise an empty list.
    """
    cnf, unit_assignments = assign_unit(cnf)
    assignments += unit_assignments
    if cnf == -1:
        return []
    if not cnf:
        return assignments
    selected_literal = jersolow_wang_2_sided_method(cnf)
    result = backtrack(bcp(cnf, selected_literal), assignments + [selected_literal])
    if not result:
        result = backtrack(bcp(cnf, -selected_literal), assignments + [-selected_literal])
    return result


def run_benchmarks(output_file: str) -> None:
    """
    Run the SAT solver on all benchmarks in the "benchmarks" directory.

    Args:
        output_file (str): Path to the output file where results will be saved.
    """
    print('Running on benchmarks...')
    start_time = time.time()
    with open(output_file, 'w') as out_file:
        for filename in os.listdir("benchmarks"):
            clauses = parse_dimacs(os.path.join("benchmarks", filename))
            assignment = backtrack(clauses, [])
            if assignment:
                out_file.write('SAT\n')
            else:
                out_file.write('UNSAT\n')
    end_time = time.time()
    print(f'Execution time: {end_time - start_time:.2f} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A SAT solver using the DPLL algorithm with heuristics.")
    parser.add_argument('--run_benchmarks', action='store_true',
                        help='Run the SAT solver on all files in the benchmarks folder.')
    parser.add_argument('--input_file', default=None,
                        help='Input file in DIMACS format (ignored if --run_benchmarks is set).')
    args = parser.parse_args()

    if args.run_benchmarks:
        run_benchmarks('benchmarks-results.log')
    elif args.input_file is not None:
        input_file = args.input_file
        assert os.path.exists(input_file), f'{input_file} does not exist.'
        clauses = parse_dimacs(input_file)
        assignment = backtrack(clauses, [])
        if assignment:
            print('SAT')
            assignment.sort(key=abs)
            print(assignment)
        else:
            print('UNSAT')
    else:
        print('Please provide an input file or specify --run_benchmarks. Use --help for details.')
