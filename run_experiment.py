import os
import argparse
import json
from solver.solver_class import SatSolver
from solver.utils import parse_dimacs

def run_experiment(puzzles_path: str, strategies: dict, results_folder: str) -> None:
    """
    Run the experimental loop for specified heuristics on Sudoku puzzles.

    Args:
        puzzles_path (str): Path to the folder containing Sudoku puzzles in DIMACS format.
        strategies (dict): Dictionary of strategy names and their corresponding numbers.
        results_folder (str): Path to the folder to save results.
    """
    os.makedirs(results_folder, exist_ok=True)  # Ensure results folder exists

    for strategy_name, strategy_number in strategies.items():
        output_file = os.path.join(results_folder, f"{strategy_name}.json")
        results = []

        print(f"Running experiments for {strategy_name} heuristic...")
        for puzzle_file in os.listdir(puzzles_path):
            puzzle_path = os.path.join(puzzles_path, puzzle_file)

            if not puzzle_path.endswith(".cnf"):
                continue  # Skip non-CNF files

            clauses = parse_dimacs(puzzle_path)
            solver = SatSolver(strategy=strategy_number)
            assignment, metrics = solver.solve(clauses)

            results.append({
                "puzzle": puzzle_file,
                "metrics": metrics,
                "satisfiable": bool(assignment)
            })

        # Save to JSON 
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)

        print(f"Results for {strategy_name} saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run experiments on Sudoku puzzles using different SAT solver heuristics.")
    parser.add_argument("--puzzles_path", required=True, help="Path to the folder containing Sudoku puzzles in DIMACS format.")
    args = parser.parse_args()

    strategies = {
        "JW_2_Sided": 3,  # Literal-oriented
        "DLIS": 5,        # Literal-oriented
        "MOMS": 4,        # Clause-oriented
        "BOHMS": 6        # Clause-oriented
    }

    results_folder = os.path.join(os.path.dirname(__file__), "results")
    run_experiment(args.puzzles_path, strategies, results_folder)
