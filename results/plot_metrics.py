import argparse
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any, Optional


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


def aggregate_metrics(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Aggregate metrics from the results.

    Args:
        results (List[Dict[str, Any]]): List of puzzle results.

    Returns:
        Dict[str, float]: Aggregated metrics containing mean values.
    """
    aggregated = {
        "decisions": [],
        "backtracks": [],
        # "conflicts": [],
        "propagations": [],
        # "unit_clauses_resolved": []
    }

    for result in results:
        metrics = result["metrics"]
        for key in aggregated.keys():
            aggregated[key].append(metrics[key])

    mean_metrics = {key: np.mean(values) for key, values in aggregated.items()}
    return mean_metrics


def plot_metrics(metrics: Dict[str, float], title: str, output_dir: str) -> None:
    """
    Plot the mean metrics.

    Args:
        metrics (Dict[str, float]): Mean metrics to plot.
        title (str): Title for the plot.
        output_dir (str): Directory to save the plot.
    """
    os.makedirs(output_dir, exist_ok=True)
    keys = list(metrics.keys())
    values = list(metrics.values())

    plt.figure(figsize=(10, 6))
    plt.bar(keys, values)
    plt.xlabel("Metrics")
    plt.ylabel("Mean Values")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = os.path.join(output_dir, f"{title.replace(' ', '_').lower()}.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Plot saved to {output_path}")


def main() -> None:
    """
    Main function to process and plot SAT solver results.
    """
    parser = argparse.ArgumentParser(description="Process and plot SAT solver results.")
    parser.add_argument(
        "--file1",
        required=True,
        help="Path to the first results JSON file."
    )
    parser.add_argument(
        "--file2",
        default=None,
        help="Path to the second results JSON file for comparison (optional)."
    )
    args = parser.parse_args()

    results1 = load_results(args.file1)
    metrics1 = aggregate_metrics(results1)

    print(f"Metrics for {os.path.basename(args.file1)}:")
    for key, value in metrics1.items():
        print(f"{key}: {value:.2f}")

    plot_metrics(metrics1, f"Metrics for {os.path.basename(args.file1)}", "plots")

    if args.file2:
        results2 = load_results(args.file2)
        metrics2 = aggregate_metrics(results2)

        print(f"\nMetrics for {os.path.basename(args.file2)}:")
        for key, value in metrics2.items():
            print(f"{key}: {value:.2f}")

        plot_metrics(metrics2, f"Metrics for {os.path.basename(args.file2)}", "plots")


if __name__ == "__main__":
    main()
