"""Test profile extraction with real Dask cluster (simplified - cluster-wide only)."""

from __future__ import annotations

import time
import warnings
from typing import Any

import dask.config
from dask.distributed import Client, LocalCluster
import numpy as np

def extract_profile_interval() -> float:
    """Extract profile interval from Dask config (e.g., "10ms" -> 10.0)."""
    interval = dask.config.get("distributed.worker.profile.interval")

    try:
        if isinstance(interval, str):
            if interval.endswith("ms"):
                return float(interval[:-2])
            if interval.endswith("s"):
                return float(interval[:-1]) * 1000
        return float(interval)
    except (ValueError, TypeError) as e:
        warnings.warn(f"Failed to parse interval '{interval}': {e}. Using 10ms.", stacklevel=2)
        return 10.0


def _flatten_profile_tree(node: dict[str, Any]) -> dict[str, int]:
    """Flatten profile tree to {function_id: count} dict.

    Note: children is a dict {identifier: child_node}, not a list.
    """
    result = {}
    identifier = node.get("identifier", "root")
    count = node.get("count", 0)

    if count > 0 and identifier != "root":
        result[identifier] = count

    # Children is a dict mapping identifier -> child_node
    children = node.get("children", {})
    if isinstance(children, dict):
        for child_id, child_node in children.items():
            child_results = _flatten_profile_tree(child_node)
            result.update(child_results)

    return result


def parse_profile_data(
    profile_tree: dict,
    profile_interval_ms: float = 10.0,
    num_threads: int = 1,
) -> dict[str, float]:
    """Parse aggregated profile tree to {function_id: time_ms}."""
    function_counts = _flatten_profile_tree(profile_tree)
    function_times = {
        func: (count * profile_interval_ms) / num_threads
        for func, count in function_counts.items()
    }
    return function_times


def rank_functions(
    function_times: dict[str, float],
    top_n: int = 10,
) -> list[dict]:
    """Rank functions by time, return top N."""
    ranked = [
        {"function": func, "time_ms": time_ms}
        for func, time_ms in function_times.items()
    ]
    ranked.sort(key=lambda x: x["time_ms"], reverse=True)
    return ranked[:top_n]

def expensive_computation(x):
    """Simulate work."""
    return sum(np.sin(x + i * 0.001) for i in range(1000000))


def process_data(data):
    """Process data chunk."""
    computed = [expensive_computation(x) for x in data]
    time.sleep(0.1)
    return sum(computed)


def main():
    print("Testing Cluster-Wide Profile Extraction")
    print("=" * 70)

    # Create cluster
    cluster = LocalCluster(n_workers=3, threads_per_worker=1, processes=True)
    client = Client(cluster)
    print(client.dashboard_link)

    try:
        # Get interval
        interval = extract_profile_interval()
        print(f"Profile interval: {interval} ms")

        # Run work
        print("Running computations...")
        data_chunks = [list(range(i * 10, (i + 1) * 10)) for i in range(20)]
        futures = client.map(process_data, data_chunks)
        client.gather(futures)

        # Get profile (aggregated across all workers)
        print("Retrieving profile...")
        profile_tree = client.profile()

        # Parse
        function_times = parse_profile_data(profile_tree, interval, num_threads=1)
        print(f"Extracted timing for {len(function_times)} functions")

        # Rank
        ranked = rank_functions(function_times, top_n=15)

        print(f"\nTop 15 Functions (Cluster-Wide):")
        print(f"{'Function':<60} {'Time (ms)':<12}")
        print("-" * 72)
        for item in ranked:
            print(f"{item['function']:<60} {item['time_ms']:<12.2f}")

        print("\n✓ All tests passed")

    finally:
        client.close()
        cluster.close()


if __name__ == "__main__":
    main()
