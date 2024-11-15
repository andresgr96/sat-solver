from collections import defaultdict
from typing import List

def jersolow(cnf: List[List[int]]) -> int:
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


def jersolow_sided(cnf: List[List[int]]) -> int:
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

