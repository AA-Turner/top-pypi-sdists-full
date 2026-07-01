#!/usr/bin/env python3
"""Run all synchronous example scripts in order"""

import argparse
import os
import string
import subprocess
import sys
import time
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Run example flows")
    parser.add_argument(
        "--flows",
        default="all",
        help="Comma-separated flow names to run (e.g., '01_create_sandbox,02_create_sandbox_with_timing'). Prefix with '!' to skip (e.g., '!03_*,!05_*')",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Default timeout per flow in seconds (default: 60)",
    )
    parser.add_argument(
        "--flow-timeout",
        action="append",
        nargs=2,
        metavar=("FLOW", "TIMEOUT"),
        help="Override timeout for specific flow (e.g., --flow-timeout 16_create_sandbox_with_auto_delete_simple.py 180)",
    )
    args = parser.parse_args()

    # Get the examples directory
    examples_dir = Path(__file__).parent

    # Find all Python files, excluding this script and async variants
    all_example_files = sorted(
        [
            f
            for f in examples_dir.glob("*.py")
            if f.name not in ["00_run_all.py", "00_run_all_async.py"]
            and not f.name.endswith("_async.py")
        ]
    )

    # Filter flows based on specification
    example_files = filter_flows(all_example_files, args.flows)

    if not example_files:
        print("No example files match the specified flows")
        return 0

    # Build flow timeout mapping
    flow_timeouts = build_flow_timeouts(args.flow_timeout)

    print(f"Found {len(example_files)} example(s) to run\n")
    print("=" * 70)

    total_start = time.time()
    results = []

    for example_file in example_files:
        example_name = example_file.name
        print(f"\n▶ Running: {example_name}")
        print("-" * 70)

        start_time = time.time()
        timeout = flow_timeouts.get(example_name, args.timeout)

        try:
            print(f"Run example script with timeout: {timeout}s")
            result = subprocess.run(
                [sys.executable, str(example_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            elapsed_time = time.time() - start_time

            # Print output
            if result.stdout:
                print(result.stdout)

            # Check for errors
            if result.returncode != 0:
                print(f"\n❌ ERROR in {example_name}")
                if result.stderr:
                    print("STDERR:")
                    print(result.stderr)

                results.append(
                    {
                        "name": example_name,
                        "status": "FAILED",
                        "time": elapsed_time,
                        "error": result.stderr or "Non-zero exit code",
                    }
                )

                # Break on error
                print("\n" + "=" * 70)
                print("STOPPING: Error encountered")
                print("=" * 70)
                print_summary(results, time.time() - total_start)
                return 1
            else:
                results.append(
                    {"name": example_name, "status": "PASSED", "time": elapsed_time}
                )
                print(f"✓ Completed in {elapsed_time:.2f}s")

        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            print(f"\n❌ TIMEOUT in {example_name} after {elapsed_time:.2f}s")

            results.append(
                {
                    "name": example_name,
                    "status": "TIMEOUT",
                    "time": elapsed_time,
                    "error": "Script exceeded 60 second timeout",
                }
            )

            # Break on timeout
            print("\n" + "=" * 70)
            print("STOPPING: Timeout encountered")
            print("=" * 70)
            print_summary(results, time.time() - total_start)
            return 1

        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"\n❌ EXCEPTION in {example_name}: {e}")

            results.append(
                {
                    "name": example_name,
                    "status": "ERROR",
                    "time": elapsed_time,
                    "error": str(e),
                }
            )

            # Break on exception
            print("\n" + "=" * 70)
            print("STOPPING: Exception encountered")
            print("=" * 70)
            print_summary(results, time.time() - total_start)
            return 1

    total_time = time.time() - total_start

    # Print summary
    print("\n" + "=" * 70)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print_summary(results, total_time)

    return 0

def filter_flows(all_files, flows_spec):
    """
    Filter example files based on flow specification.

    Args:
        all_files: List of all example Path objects
        flows_spec: Comma-separated flow names. Prefix with '!' to skip.
                   Use 'all' to include all flows.

    Returns:
        List of filtered Path objects
    """
    if flows_spec.lower() == "all":
        return all_files

    include_patterns = []
    skip_patterns = []

    if flows_spec.startswith("!"):
        skip_patterns = [p.strip() for p in flows_spec[1:].split(",") if p.strip()]
    else:
        include_patterns = [p.strip() for p in flows_spec.split(",") if p.strip()]

    filtered = []
    for f in all_files:
        name = f.name
        included = True

        if include_patterns:
            included = any(
                name == p or name.startswith(p.rstrip("*"))
                for p in include_patterns
            )

        if skip_patterns:
            skipped = any(
                name == p or name.startswith(p.rstrip("*"))
                for p in skip_patterns
            )
            if skipped:
                included = False

        if included:
            filtered.append(f)

    return filtered


def build_flow_timeouts(flow_timeout_args):
    """
    Build a mapping of flow names to custom timeouts.

    Args:
        flow_timeout_args: List of (flow_name, timeout) tuples from argparse

    Returns:
        Dict mapping flow names to timeout values
    """
    flow_timeouts = {}
    if flow_timeout_args:
        for flow_name, timeout in flow_timeout_args:
            flow_timeouts[flow_name] = int(timeout)
    return flow_timeouts



def print_summary(results, total_time):
    """Print execution summary"""
    print("\n📊 EXECUTION SUMMARY")
    print("-" * 70)

    for result in results:
        status_symbol = {
            "PASSED": "✓",
            "FAILED": "❌",
            "TIMEOUT": "⏱",
            "ERROR": "❌",
        }.get(result["status"], "?")

        print(
            f"{status_symbol} {result['name']:40s} {result['time']:>6.2f}s  {result['status']}"
        )

        if "error" in result:
            error_preview = result["error"].split("\n")[0][:50]
            print(f"   Error: {error_preview}")

    print("-" * 70)
    print(f"Total execution time: {total_time:.2f}s")

    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)
    print(f"Results: {passed}/{total} passed")


if __name__ == "__main__":
    sys.exit(main())
