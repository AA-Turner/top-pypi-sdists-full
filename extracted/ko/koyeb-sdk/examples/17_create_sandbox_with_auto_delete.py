#!/usr/bin/env python3
"""Create sandboxes with auto-delete lifecycle settings and wait for them to be deleted"""

import os
import sys
import random
import string
import time
from collections import defaultdict
from datetime import datetime

from koyeb import Sandbox
from koyeb.sandbox.utils import get_api_clients


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

    def print_recap(self):
        """Print a detailed recap of all timings"""
        print("\n" + "=" * 70)
        print(" TIMING SUMMARY")
        print("=" * 70)

        if not self.operations:
            print("No operations recorded")
            return

        total_time = self.get_total_time()

        print()
        for op in self.operations:
            percentage = (op["duration"] / total_time * 100) if total_time > 0 else 0
            bar_length = int(percentage / 2)
            bar = "█" * bar_length

            print(
                f"  {op['name']:<40} {op['duration']:6.2f}s  {percentage:5.1f}%  {bar}"
            )

        print()
        print("-" * 70)
        print(f"  {'TOTAL':<40} {total_time:6.2f}s  100.0%")
        print("=" * 70)


def get_service_lifecycle(api_token: str, service_id: str):
    """Fetch and return the service lifecycle settings from the API"""
    services_api = get_api_clients(api_token).services
    service_response = services_api.get_service(service_id)
    return service_response.service.life_cycle


def service_exists(api_token: str, service_id: str) -> bool:
    """Check if a service still exists"""
    try:
        services_api = get_api_clients(api_token).services
        services_api.get_service(service_id)
        return True
    except Exception:
        return False


def wait_for_deletion(api_token: str, service_id: str, name: str, timeout: int = 600) -> float:
    """Wait for a service to be deleted. Returns time waited."""
    start = time.time()
    print(f"    Waiting for {name} to be auto-deleted...")

    while time.time() - start < timeout:
        if not service_exists(api_token, service_id):
            duration = time.time() - start
            print(f"    ✓ {name} was auto-deleted after {duration:.1f}s")
            return duration
        time.sleep(5)
        elapsed = time.time() - start
        print(f"      ... still waiting ({elapsed:.0f}s elapsed)")

    print(f"    ✗ Timeout waiting for {name} to be deleted")
    return time.time() - start


def main():
    tracker = TimingTracker()

    print("=" * 70)
    print(" AUTO-DELETE SANDBOX DEMO")
    print("=" * 70)
    print()
    print("This example creates two sandboxes with different auto-delete configs:")
    print("  1. delete_after_delay (delete 60s after creation)")
    print("  2. idle_timeout + delete_after_inactivity_delay (sleep after idle, then delete)")
    print()

    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    sandbox1 = None
    sandbox2 = None

    try:
        # =====================================================================
        # Sandbox 1: delete_after_delay (delete after creation)
        # =====================================================================
        print("-" * 70)
        print(" SANDBOX 1: delete_after_delay (delete 60s after creation)")
        print("-" * 70)
        print()

        delete_after_delay_1 = 60  # Delete 60s after creation

        print("  → Creating sandbox 1...")
        print(f"    - delete_after_delay: {delete_after_delay_1}s (delete after creation)")
        print(f"    → Expected deletion: ~{delete_after_delay_1}s after creation")

        create_start = time.time()
        sandbox1 = Sandbox.create(
            image="koyeb/sandbox:slim",
            name="auto-delete-test-1",
            wait_ready=True,
            api_token=api_token,
            delete_after_delay=delete_after_delay_1,
        )
        create_duration = time.time() - create_start
        tracker.record("Sandbox 1 creation", create_duration, "setup")
        print(f"    ✓ Created in {create_duration:.1f}s")
        print(f"    Service ID: {sandbox1.service_id}")

        # Verify lifecycle settings
        lifecycle1 = get_service_lifecycle(api_token, sandbox1.service_id)
        if lifecycle1:
            print(f"    Lifecycle: delete_after_sleep={lifecycle1.delete_after_sleep}s, "
                  f"delete_after_create={lifecycle1.delete_after_create}s")

        # Quick health check
        print("  → Verifying sandbox 1 is healthy...")
        assert sandbox1.is_healthy(), "Sandbox 1 should be healthy"
        result = sandbox1.exec("echo 'Sandbox 1 ready'")
        print(f"    ✓ {result.stdout.strip()}")
        print()

        # =====================================================================
        # Sandbox 2: idle_timeout + delete_after_inactivity_delay
        # =====================================================================
        print("-" * 70)
        print(" SANDBOX 2: idle_timeout + delete_after_inactivity_delay")
        print("-" * 70)
        print()

        idle_timeout_2 = 60  # Sleep after 60s of inactivity
        delete_after_inactivity_2 = 60  # Delete 60s after sleep

        print("  → Creating sandbox 2...")
        print(f"    - idle_timeout: {idle_timeout_2}s (sleep after idle)")
        print(f"    - delete_after_inactivity_delay: {delete_after_inactivity_2}s (delete after sleep)")
        print(f"    → Expected total time to deletion: ~{idle_timeout_2 + delete_after_inactivity_2}s")

        create_start = time.time()
        sandbox2 = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"auto-delete-test-2-{suffix}",
            wait_ready=True,
            api_token=api_token,
            idle_timeout=idle_timeout_2,
            delete_after_inactivity_delay=delete_after_inactivity_2,
        )
        create_duration = time.time() - create_start
        tracker.record("Sandbox 2 creation", create_duration, "setup")
        print(f"    ✓ Created in {create_duration:.1f}s")
        print(f"    Service ID: {sandbox2.service_id}")

        # Verify lifecycle settings
        lifecycle2 = get_service_lifecycle(api_token, sandbox2.service_id)
        if lifecycle2:
            print(f"    Lifecycle: delete_after_sleep={lifecycle2.delete_after_sleep}s, "
                  f"delete_after_create={lifecycle2.delete_after_create}s")

        # Quick health check
        print("  → Verifying sandbox 2 is healthy...")
        assert sandbox2.is_healthy(), "Sandbox 2 should be healthy"
        result = sandbox2.exec("echo 'Sandbox 2 ready'")
        print(f"    ✓ {result.stdout.strip()}")
        print()

        # =====================================================================
        # Wait for auto-deletion
        # =====================================================================
        print("-" * 70)
        print(" WAITING FOR AUTO-DELETION")
        print("-" * 70)
        print()
        print("  Waiting for both sandboxes to be auto-deleted...")
        print(f"  Sandbox 1: should delete ~{delete_after_delay_1}s after creation")
        print(f"  Sandbox 2: should sleep after {idle_timeout_2}s, then delete after {delete_after_inactivity_2}s more")
        print()

        # Track which sandboxes are still alive
        sandbox1_deleted = False
        sandbox2_deleted = False
        sandbox1_delete_time = None
        sandbox2_delete_time = None

        wait_start = time.time()
        max_wait = 600  # 10 minutes max

        while time.time() - wait_start < max_wait:
            elapsed = time.time() - wait_start

            # Check sandbox 1
            if not sandbox1_deleted and not service_exists(api_token, sandbox1.service_id):
                sandbox1_deleted = True
                sandbox1_delete_time = elapsed
                print(f"  ✓ Sandbox 1 auto-deleted at {elapsed:.1f}s")
                tracker.record("Sandbox 1 auto-deletion wait", elapsed, "auto-delete")

            # Check sandbox 2
            if not sandbox2_deleted and not service_exists(api_token, sandbox2.service_id):
                sandbox2_deleted = True
                sandbox2_delete_time = elapsed
                print(f"  ✓ Sandbox 2 auto-deleted at {elapsed:.1f}s")
                tracker.record("Sandbox 2 auto-deletion wait", elapsed, "auto-delete")

            # Both deleted?
            if sandbox1_deleted and sandbox2_deleted:
                print()
                print("  ✓ Both sandboxes have been auto-deleted!")
                break

            # Status update every 30s
            if int(elapsed) % 30 == 0 and int(elapsed) > 0:
                status1 = "deleted" if sandbox1_deleted else "alive"
                status2 = "deleted" if sandbox2_deleted else "alive"
                print(f"    ... {elapsed:.0f}s elapsed (sandbox1: {status1}, sandbox2: {status2})")

            time.sleep(5)
        else:
            print()
            print("  ✗ Timeout waiting for sandboxes to be deleted")
            if not sandbox1_deleted:
                print("    - Sandbox 1 was not deleted")
            if not sandbox2_deleted:
                print("    - Sandbox 2 was not deleted")

        # Clear sandbox references so finally block doesn't try to delete them
        if sandbox1_deleted:
            sandbox1 = None
        if sandbox2_deleted:
            sandbox2 = None

        print()
        print("-" * 70)
        print(" RESULTS")
        print("-" * 70)
        print()
        if sandbox1_delete_time:
            print(f"  Sandbox 1 (delete_after_delay): deleted after {sandbox1_delete_time:.1f}s")
            print(f"    Expected: ~{delete_after_delay_1}s after creation")
        if sandbox2_delete_time:
            print(f"  Sandbox 2 (idle_timeout + delete_after_inactivity): deleted after {sandbox2_delete_time:.1f}s")
            print(f"    Expected: ~{idle_timeout_2 + delete_after_inactivity_2}s (idle + delete delay)")
        return 0

    finally:
        # Clean up any sandboxes that weren't auto-deleted
        if sandbox1:
            print()
            print("  → Manually deleting sandbox 1 (wasn't auto-deleted)...")
            delete_start = time.time()
            sandbox1.delete()
            tracker.record("Sandbox 1 manual deletion", time.time() - delete_start, "cleanup")

        if sandbox2:
            print()
            print("  → Manually deleting sandbox 2 (wasn't auto-deleted)...")
            delete_start = time.time()
            sandbox2.delete()
            tracker.record("Sandbox 2 manual deletion", time.time() - delete_start, "cleanup")

        print()
        print("✓ Demo completed")

        # Print detailed recap
        tracker.print_recap()


if __name__ == "__main__":
    sys.exit(main())
