#!/usr/bin/env python3
"""Use the fluent builder API to create a reusable snapshot and spawn sandboxes from it"""

import os
import sys
import random
import string

from koyeb import Sandbox


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    snapshot = None
    runner1 = None
    runner2 = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        # Build a reusable snapshot declaratively
        print("✓ Building declarative snapshot...")
        snapshot = (
            Sandbox.template(
                f"ci-environment-{suffix}",
                image="python:3.12",
                workdir="/workspace",
                api_token=api_token,
            )
            .file("requirements.txt", "requests")
            .run("pip install -r requirements.txt")
            .build(snapshot_name=f"python-ci-env-{suffix}")
        )
        
        # Print operations performed during build
        if snapshot.operations:
            for op in snapshot.operations:
                print(f"    - {op}")
        print(f"  ✓ Snapshot built: {snapshot.name}")

        # Spawn multiple sandboxes from the same snapshot in parallel
        print("✓ Spawning sandboxes from snapshot...")
        print("  - Spawning runner1...")
        print("  - Spawning runner2...")
        runner1 = snapshot.spawn(
            image="python:3.12",
            name=f"test-suite-1-{suffix}",
            wait_ready=False,
            api_token=api_token,
        )
        runner2 = snapshot.spawn(
            image="python:3.12",
            name=f"test-suite-2-{suffix}",
            wait_ready=False,
            api_token=api_token,
        )
        print(f"  ✓ Runner1 spawned: {runner1.name}")
        print(f"  ✓ Runner2 spawned: {runner2.name}")
        
        # Wait for both sandboxes to be ready
        print("✓ Waiting for sandboxes to be ready...")
        for runner in [runner1, runner2]:
            runner.wait_ready(timeout=300)
        print("  ✓ All sandboxes are ready")

        # Verify the environment is pre-configured from snapshot filesystem
        print("✓ Verifying runner1 has pre-installed packages from snapshot filesystem...")
        result = runner1.exec("python3 -c \"import requests; print('All packages installed')\"")
        print(f"  stdout: '{result.stdout}', stderr: '{result.stderr}', exit_code: {result.exit_code}")
        assert "All packages installed" in result.stdout, f"Expected packages to be installed, got stdout: '{result.stdout}', stderr: '{result.stderr}'"
        print(f"  ✓ Result: {result.stdout.strip()}")

        print("✓ Verifying runner2 has pre-installed packages from snapshot filesystem...")
        result = runner2.exec("python3 -c \"import requests; print('All packages installed')\"")
        print(f"  stdout: '{result.stdout}', stderr: '{result.stderr}', exit_code: {result.exit_code}")
        assert "All packages installed" in result.stdout, f"Expected packages to be installed, got stdout: '{result.stdout}', stderr: '{result.stderr}'"
        print(f"  ✓ Result: {result.stdout.strip()}")

        return 0
    finally:
        if runner2:
            runner2.delete()
        if runner1:
            runner1.delete()
        if snapshot:
            snapshot.delete()


if __name__ == "__main__":
    sys.exit(main())
