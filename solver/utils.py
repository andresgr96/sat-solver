from typing import List

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