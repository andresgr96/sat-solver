import os
import argparse
from typing import List


def read_sudoku_rules(sudoku_rules: str) -> List[str]:
    """
    Read the file with the sudoku rules.

    Args:
        sudoku_rules (str): Path to the file containing sudoku rules.

    Returns:
        List[str]: List of lines from the sudoku rules file.
    """
    with open(sudoku_rules, 'r') as file:
        return file.readlines()


def convert_to_DIMACS(puzzle: str, board_size: int) -> List[str]:
    """
    Convert a sudoku puzzle to DIMACS format clauses.

    Args:
        puzzle (str): Sudoku puzzle as a single string.
        board_size (int): Size of the sudoku board (e.g., 9 for 9x9).

    Returns:
        List[str]: List of clauses in DIMACS format.
    """
    rows = [puzzle[i * board_size:(i + 1) * board_size] for i in range(board_size)]
    DIMACS_lines = []  # Clauses
    grid_base = 17 if board_size == 16 else 10  # Use 17 for 16x16 grid, otherwise 10
    char_map = {char: index + 1 for index, char in enumerate("123456789ABCDEF")}  # Map characters to 1 to 16
    char_map.update({char: index + 11 for index, char in enumerate("GHIJKLMNOP")})  # Map characters to 11 to 26

    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            if value != '.':  # Skip empty cells
                variable = grid_base**2 * (row_index + 1) + grid_base * (column_index + 1) + char_map[value]
                DIMACS_lines.append(f"{variable} 0\n")
    return DIMACS_lines


def generate_DIMACS(sudoku_puzzle: str, sudoku_rules: str, result_directory: str, board_size: int) -> None:
    """
    Generate DIMACS files for each sudoku puzzle using the provided rules.

    Args:
        sudoku_puzzle (str): Path to the file containing sudoku puzzles.
        sudoku_rules (str): Path to the file containing sudoku rules.
        result_directory (str): Directory to save the generated DIMACS files.
        board_size (int): Size of the sudoku board (e.g., 9 for 9x9).
    """
    rules = read_sudoku_rules(sudoku_rules)
    with open(sudoku_puzzle, 'r') as file:
        puzzles = [line.strip() for line in file if line.strip()]  # Extract non-empty lines from input

    # Verify that puzzles have the expected length
    total_cells = board_size ** 2
    for index, puzzle in enumerate(puzzles):
        if len(puzzle) != total_cells:
            raise ValueError(f"Puzzle {index + 1} has invalid length {len(puzzle)}. Expected {total_cells}.")

    os.makedirs(result_directory, exist_ok=True)

    for index, puzzle in enumerate(puzzles):
        puzzle_clauses = convert_to_DIMACS(puzzle, board_size)
        DIMACS_lines = rules[1:] + puzzle_clauses  

        header = f"p cnf {board_size ** 3} {len(DIMACS_lines)}\n"
        result_file = os.path.join(result_directory, f"puzzle_{index + 1}.cnf")
        with open(result_file, 'w') as f:
            f.write(header)
            f.writelines(DIMACS_lines)


def main() -> None:
    """
    Main function to handle command-line arguments and generate DIMACS files.
    """
    parser = argparse.ArgumentParser(description="Encode Sudoku puzzles in DIMACS format.")
    parser.add_argument(
        "--sudoku_puzzle",
        default='./data/test_sets/1000 sudokus.txt',
        help="Path to the file containing sudoku puzzles (default: './data/test_sets/1000 sudokus.txt')."
    )
    parser.add_argument(
        "--sudoku_rules",
        default='./data/rules/sudoku-rules-9x9.txt',
        help="Path to the file containing sudoku rules (default: './data/rules/sudoku-rules-9x9.txt')."
    )
    parser.add_argument(
        "--board_size",
        type=int,
        default=9,
        choices=[4, 9, 16],
        help="Size of the sudoku board (e.g., 4 for 4x4, 9 for 9x9, 16 for 16x16; default: 9)."
    )
    args = parser.parse_args()

    result_directory = os.path.join(
        "./data/sets_encoded",
        os.path.basename(args.sudoku_puzzle).split(".")[0]
    )

    generate_DIMACS(args.sudoku_puzzle, args.sudoku_rules, result_directory, args.board_size)


if __name__ == "__main__":
    main()
