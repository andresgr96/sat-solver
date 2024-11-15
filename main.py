#!/usr/bin/env python3
import sys
import os
import time
import argparse
from solver.utils import *
from solver.solver_class import SatSolver


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
