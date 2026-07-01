#!/usr/bin/env python3
"""Create and manage a sandbox with detailed timing information for debugging (async variant)"""

import argparse
import asyncio
import sys
import os
import sys
import random
import string
import time
from collections import defaultdict
from datetime import datetime

from koyeb import AsyncSandbox


class TimingTracker:
    """Track timing information for operations"""

    def __init__(self):
        self.operations = []
        self.categories = defaultdict(list)

    def record(self, name, duration, category="general"):
        """Record an operation's timing"""
        self.operations.append(
            {
                "name": name,
                "duration": duration,
                "category": category,
                "timestamp": datetime.now(),
            }
        )
        self.categories[category].append(duration)

    def get_total_time(self):
        """Get total time for all operations"""
        return sum(op["duration"] for op in self.operations)

    def get_category_total(self, category):
        """Get total time for a specific category"""
        return sum(self.categories[category])

    def print_recap(self):
        """Print a detailed recap of all timings"""
        print("\n" + "=" * 70)
        print(" TIMING SUMMARY")
        print("=" * 70)

        if not self.operations:
            print("No operations recorded")
            return

        total_time = self.get_total_time()

        # Print individual operations
        print()

        for op in self.operations:
            percentage = (op["duration"] / total_time * 100) if total_time > 0 else 0
            bar_length = int(percentage / 2)  # 50 chars = 100%
            bar = "█" * bar_length

            print(
                f"  {op['name']:<30} {op['duration']:6.2f}s  {percentage:5.1f}%  {bar}"
            )

        print()
        print("-" * 70)
        print(f"  {'TOTAL':<30} {total_time:6.2f}s  100.0%")
        print("=" * 70)


async def main(run_long_tests=False):
    tracker = TimingTracker()

    print("Starting sandbox operations...")

    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        # Create sandbox with timing
        print("  → Creating sandbox...")
        create_start = time.time()
        sandbox = await AsyncSandbox.create(
            image="koyeb/sandbox:slim",
            name=f"example-sandbox-timed-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )
        create_duration = time.time() - create_start
        tracker.record("Sandbox creation", create_duration, "setup")
        print(f"    ✓ took {create_duration:.1f}s")

        # Check health with timing
        print("  → Checking sandbox health...")
        health_start = time.time()
        await sandbox.is_healthy()
        health_duration = time.time() - health_start
        tracker.record("Health check", health_duration, "monitoring")
        print(f"    ✓ took {health_duration:.1f}s")

        # Test command execution with timing
        print("  → Executing initial test command...")
        exec_start = time.time()
        await sandbox.exec("echo 'Sandbox is ready!'")
        exec_duration = time.time() - exec_start
        tracker.record("Initial exec command", exec_duration, "execution")
        print(f"    ✓ took {exec_duration:.1f}s")

        if run_long_tests:
            # Long test 1: Install a package
            print("  → [LONG TEST] Installing a package...")
            install_start = time.time()
            await sandbox.exec("pip install requests")
            install_duration = time.time() - install_start
            tracker.record("Package installation", install_duration, "long_tests")
            print(f"    ✓ took {install_duration:.1f}s")

            # Long test 2: Run a computation
            print("  → [LONG TEST] Running computation...")
            compute_start = time.time()
            await sandbox.exec(
                "python -c 'import time; sum(range(10000000)); time.sleep(2)'"
            )
            compute_duration = time.time() - compute_start
            tracker.record("Heavy computation", compute_duration, "long_tests")
            print(f"    ✓ took {compute_duration:.1f}s")

            # Long test 3: Multiple health checks
            print("  → [LONG TEST] Multiple health checks...")
            multi_check_start = time.time()
            for i in range(5):
                await sandbox.is_healthy()
                await asyncio.sleep(0.5)
            multi_check_duration = time.time() - multi_check_start
            tracker.record(
                "Multiple health checks (5x)", multi_check_duration, "long_tests"
            )
            print(f"    ✓ took {multi_check_duration:.1f}s")

            return 0
    finally:
        if sandbox:
            print("  → Deleting sandbox...")
            delete_start = time.time()
            await sandbox.delete()
            delete_duration = time.time() - delete_start
            tracker.record("Sandbox deletion", delete_duration, "cleanup")
            print(f"    ✓ took {delete_duration:.1f}s")

        print("\n✓ All operations completed")

        # Print detailed recap
        tracker.print_recap()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create and manage a sandbox with detailed timing information"
    )
    parser.add_argument(
        "--long",
        action="store_true",
        help="Run longer tests (package installation, computation, etc.)",
    )

    args = parser.parse_args()
    sys.exit(asyncio.run(main(run_long_tests=args.long)))
