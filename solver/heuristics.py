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


def moms_heuristic(cnf: List[List[int]]) -> int:
    """
    Apply MOM's Heuristic (Maximum Occurrences in clauses of Minimum Size).

    Args:
        cnf (List[List[int]]): The CNF formula.

    Returns:
        int: The literal to assign.
    """
    min_size = float('inf')
    literal_counts = defaultdict(int)

    for clause in cnf:
        if len(clause) < min_size:
            min_size = len(clause)
            literal_counts = defaultdict(int)  
        if len(clause) == min_size:
            for literal in clause:
                literal_counts[literal] += 1

    return max(literal_counts, key=literal_counts.get)


def dlis(cnf: List[List[int]]) -> int:
    """
    Apply the DLIS heuristic (Dynamic Largest Individual Sum).

    Args:
        cnf (List[List[int]]): The CNF formula.

    Returns:
        int: The literal to assign.
    """
    positive_counts = defaultdict(int)
    negative_counts = defaultdict(int)

    for clause in cnf:
        for literal in clause:
            if literal > 0:
                positive_counts[literal] += 1
            else:
                negative_counts[-literal] += 1

    max_literal = max(
        list(positive_counts.keys()) + list(negative_counts.keys()),
        key=lambda l: positive_counts.get(l, 0) + negative_counts.get(l, 0)
    )

    return max_literal if positive_counts.get(max_literal, 0) >= negative_counts.get(max_literal, 0) else -max_literal

def bohm_heuristic(cnf: List[List[int]]) -> int:
    """
    Apply BOHM's heuristic to select the next literal.

    Args:
        cnf (List[List[int]]): The CNF formula.

    Returns:
        int: The literal to assign.
    """
    weights = {1: 10, 2: 5, 3: 1}  # Weights for clause sizes
    literal_scores = defaultdict(int)

    for clause in cnf:
        clause_size = len(clause)
        weight = weights.get(clause_size, 0)  # Default weight for larger clauses is 0
        for literal in clause:
            literal_scores[literal] += weight

    return max(literal_scores, key=literal_scores.get)

