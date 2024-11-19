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

    input_file_name = os.path.basename(input_file)  
    results_dir = os.path.join(os.path.dirname(__file__), "results")  
    os.makedirs(results_dir, exist_ok=True)  
    output_file = os.path.join(results_dir, f"{input_file_name}.out") 

    with open(output_file, "w") as out_file:
        if assignment:
            out_file.write(" ".join(map(str, sorted(assignment, key=abs))) + " 0\n")
        else:
            pass  # File is already created so if we pass it remains empty

    if assignment:
        print(f"SAT. Solution written to {output_file}.")
    else:
        print(f"UNSAT. {output_file} is empty.")
