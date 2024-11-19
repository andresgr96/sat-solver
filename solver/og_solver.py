from typing import List, Tuple, Union
from .utils import *
from .heuristics import *

class SatSolver:
    """
    A class for solving SAT problems using DPLL with different heuristics.
    """

    def __init__(self, strategy: int) -> None:
        """
        Initialize the SAT solver with the given strategy.

        Args:
            strategy (int): The strategy number (1: Basic DPLL, 2: DPLL with Jersolow-Wang,
                            3: DPLL with Jersolow-Wang 2-sided, 4: MOM's Heuristic, 5: DLIS).
        """
        assert strategy in [1, 2, 3, 4, 5], "Invalid strategy. Must be 1, 2, 3, 4, or 5."
        self.strategy = strategy
        self.metrics = {
            "decisions": 0,
            "backtracks": 0,
            "conflicts": 0,
            "propagations": 0,
            "unit_clauses_resolved": 0
        }

    @staticmethod
    def propagate_unit(cnf: List[List[int]], unit: int) -> Union[List[List[int]], int]:
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

    def get_unit_clauses(self, cnf: List[List[int]]) -> Tuple[Union[List[List[int]], int], List[int]]:
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
            cnf = self.propagate_unit(cnf, unit)
            self.metrics["unit_clauses_resolved"] += 1
            self.metrics["propagations"] += 1  # Each propagation is part of resolving a unit clause
            assignments.append(unit)

            if cnf == -1:
                return -1, []
            if not cnf:
                return cnf, assignments
            unit_clauses = [clause for clause in cnf if len(clause) == 1]

        return cnf, assignments

    def select_literal(self, cnf: List[List[int]]) -> int:
        """
        Select the next literal to assign based on the chosen strategy.

        Args:
            cnf (List[List[int]]): The CNF formula.

        Returns:
            int: The literal to assign.
        """
        if self.strategy == 1:
            return cnf[0][0]  # Basic DPLL
        elif self.strategy == 2:
            return jersolow(cnf)
        elif self.strategy == 3:
            return jersolow_sided(cnf)
        elif self.strategy == 4:
            return moms_heuristic(cnf)
        elif self.strategy == 5:
            return dlis(cnf)

    def solve(self, cnf: List[List[int]], assignments: List[int] = []) -> Tuple[List[int], dict]:
        """
        Solve the SAT problem using the DPLL algorithm.

        Args:
            cnf (List[List[int]]): The CNF formula.
            assignments (List[int], optional): Current variable assignments. Defaults to [].

        Returns:
            Tuple[List[int], dict]: A tuple containing the satisfying assignment (if SAT)
            and a dictionary of metrics.
        """
        cnf, unit_assignments = self.get_unit_clauses(cnf)
        assignments += unit_assignments

        if cnf == -1:
            self.metrics["conflicts"] += 1
            return [], self.metrics
        if not cnf:
            return assignments, self.metrics

        self.metrics["decisions"] += 1  # A decision is made when selecting a literal
        selected_literal = self.select_literal(cnf)

        result, _ = self.solve(self.propagate_unit(cnf, selected_literal), assignments + [selected_literal])
        if not result:
            self.metrics["backtracks"] += 1  # A backtrack occurs when the first branch fails
            result, _ = self.solve(self.propagate_unit(cnf, -selected_literal), assignments + [-selected_literal])

        return result, self.metrics