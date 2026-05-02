"""Test how profile counts scale with number of workers."""

import time
from dask.distributed import Client, LocalCluster


def expensive_computation(x):
    """Simulate work."""
    import numpy as np
    return sum(np.sin(x + i * 0.001) for i in range(1000000))


def process_data(data):
    """Process data chunk."""
    computed = [expensive_computation(x) for x in data]
    time.sleep(0.1)
    return sum(computed)


def _flatten_profile_tree(node):
    """Flatten profile tree to {function_id: count} dict."""
    result = {}
    identifier = node.get("identifier", "root")
    count = node.get("count", 0)

    if count > 0 and identifier != "root":
        result[identifier] = count

    children = node.get("children", {})
    if isinstance(children, dict):
        for child_id, child_node in children.items():
            child_results = _flatten_profile_tree(child_node)
            result.update(child_results)

    return result


def test_with_n_workers(n_workers):
    """Run test with N workers and return profile counts."""
    cluster = LocalCluster(n_workers=n_workers, threads_per_worker=1, processes=True, silence_logs=True)
    client = Client(cluster)

    try:
        # Run same workload
        data_chunks = [list(range(i * 10, (i + 1) * 10)) for i in range(20)]
        futures = client.map(process_data, data_chunks)
        client.gather(futures)

        # Get profile
        profile_tree = client.profile()

        # Flatten and find expensive_computation
        function_counts = _flatten_profile_tree(profile_tree)
        for func_id, count in function_counts.items():
            if "expensive_computation" in func_id:
                return count

        return 0

    finally:
        client.close()
        cluster.close()


def main():
    print("Testing Profile Count Scaling")
    print("=" * 50)

    results = {}
    for n in [1, 2, 3, 4]:
        print(f"\nTesting with {n} worker(s)...")
        count = test_with_n_workers(n)
        results[n] = count
        print(f"  expensive_computation count: {count}")

    print("\n" + "=" * 50)
    print("Results Summary:")
    print(f"{'Workers':<10} {'Count':<10} {'Count/Worker':<15}")
    print("-" * 35)
    for n, count in results.items():
        per_worker = count / n if n > 0 else 0
        print(f"{n:<10} {count:<10} {per_worker:<15.1f}")

    # Analyze
    print("\nAnalysis:")
    if len(results) >= 2:
        counts = list(results.values())
        if counts[0] == 0:
            print("✗ All counts are zero - function not found in profile")
        elif all(abs(c - counts[0]) / counts[0] < 0.2 for c in counts):
            print("✓ Counts are similar across worker counts")
            print("  → Profile is likely showing PER-WORKER or WALL-CLOCK time")
        else:
            ratio = results[max(results.keys())] / results[min(results.keys())]
            worker_ratio = max(results.keys()) / min(results.keys())
            if abs(ratio - worker_ratio) / worker_ratio < 0.2:
                print("✓ Counts scale linearly with worker count")
                print("  → Profile is aggregating ACROSS ALL WORKERS")
            else:
                print(f"? Counts have ratio {ratio:.2f}x")
                print(f"  Workers have ratio {worker_ratio:.2f}x")


if __name__ == "__main__":
    main()
