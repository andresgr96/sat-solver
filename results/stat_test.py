import argparse
import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple
from scipy.stats import ttest_ind


def load_results(file_path: str) -> List[Dict[str, Any]]:
    """
    Load the results from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        List[Dict[str, Any]]: List of puzzle results containing metrics and satisfiability.
    """
    with open(file_path, "r") as f:
        return json.load(f)


def extract_metric_values(results: List[Dict[str, Any]], metric: str) -> List[float]:
    """
    Extract specific metric values from results.

    Args:
        results (List[Dict[str, Any]]): List of puzzle results.
        metric (str): Metric to extract (e.g., "decisions", "backtracks").

    Returns:
        List[float]: List of metric values.
    """
    return [result["metrics"][metric] for result in results]


def perform_statistical_test(
    values1: List[float],
    values2: List[float]
) -> Tuple[float, float]:
    """
    Perform a t-test to compare two sets of values.

    Args:
        values1 (List[float]): First set of values.
        values2 (List[float]): Second set of values.

    Returns:
        Tuple[float, float]: t-statistic and p-value.
    """
    t_stat, p_value = ttest_ind(values1, values2, equal_var=False)
    return t_stat, p_value


def analyze_and_test(
    file1: str,
    file2: str,
    file3: str,
    file4: str
) -> None:
    """
    Analyze metrics from four files and test for significance between the first two and last two.

    Args:
        file1 (str): Path to the first results file.
        file2 (str): Path to the second results file.
        file3 (str): Path to the third results file.
        file4 (str): Path to the fourth results file.
    """
    # Load results
    results1 = load_results(file1)
    results2 = load_results(file2)
    results3 = load_results(file3)
    results4 = load_results(file4)

    # Combine results for the two groups
    group1_results = results1 + results2
    group2_results = results3 + results4

    metrics = ["decisions", "backtracks", "propagations"]

    print("\nStatistical Comparison of Metrics:")
    for metric in metrics:
        group1_values = extract_metric_values(group1_results, metric)
        group2_values = extract_metric_values(group2_results, metric)

        t_stat, p_value = perform_statistical_test(group1_values, group2_values)

        print(f"\nMetric: {metric}")
        print(f"Group 1 Mean: {np.mean(group1_values):.2f}")
        print(f"Group 2 Mean: {np.mean(group2_values):.2f}")
        print(f"T-Statistic: {t_stat:.2f}")
        print(f"P-Value: {p_value:.4f}")


def main() -> None:
    """
    Main function to analyze and test metrics from four files.
    """
    parser = argparse.ArgumentParser(description="Perform statistical tests on SAT solver results.")
    parser.add_argument("--file1", required=True, help="Path to the first results JSON file.")
    parser.add_argument("--file2", required=True, help="Path to the second results JSON file.")
    parser.add_argument("--file3", required=True, help="Path to the third results JSON file.")
    parser.add_argument("--file4", required=True, help="Path to the fourth results JSON file.")
    args = parser.parse_args()

    analyze_and_test(args.file1, args.file2, args.file3, args.file4)


if __name__ == "__main__":
    main()
