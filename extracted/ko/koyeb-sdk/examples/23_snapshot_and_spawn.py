#!/usr/bin/env python3
"""Create a sandbox, take a snapshot, and spawn a new sandbox from it"""

import os
import sys
import random
import string

from koyeb import Sandbox
from koyeb.sandbox import SnapshotType


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    sbx = None
    sbx2 = None
    snapshot = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        print("✓ Creating sandbox...")
        sbx = Sandbox.create(
            image="python:3.12",
            name=f"snapshot-and-spawn-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox created: {sbx.name}")

        # Create some files to verify filesystem preservation
        print("✓ Creating files...")
        sbx.filesystem.mkdir("/workspace")
        sbx.filesystem.write_file("/workspace/test_file.txt", "Hello from snapshot!")
        sbx.filesystem.write_file("/workspace/requirements.txt", "requests\npytest\n")
        print("  ✓ Files created")

        # Install packages
        print("✓ Installing packages...")
        sbx.exec("pip3 install pytest requests")
        print("  ✓ Packages installed")

        # Take a snapshot
        print("✓ Creating snapshot...")
        snapshot = sbx.snapshot(
            name=f"python-with-deps-{suffix}",
            snapshot_type=SnapshotType.FILESYSTEM,
        )
        print(f"  ✓ Snapshot created: {snapshot.name}")

        # Spawn a new sandbox from the snapshot with a different instance type
        print("✓ Spawning sandbox from snapshot with different instance type...")
        sbx2 = snapshot.spawn(
            image="python:3.12",
            name=f"test-runner-{suffix}",
            instance_type="nano",
            env={"SPAWNED_FROM_SNAPSHOT": "true"},
            wait_ready=False,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox spawned: {sbx2.name}")

        # Wait for the spawned sandbox to be ready
        print("✓ Waiting for spawned sandbox to be ready...")
        is_ready = sbx2.wait_ready(timeout=300)
        print("  ✓ Sandbox is ready")

        # Verify filesystem is preserved from snapshot
        print("✓ Verifying filesystem is preserved from snapshot...")
        
        # Check that files exist
        result = sbx2.exec("cat /workspace/test_file.txt")
        assert result.stdout.strip() == "Hello from snapshot!", f"File content mismatch: {result.stdout}"
        print("  ✓ Custom file preserved")
        
        # Check that packages are pre-installed
        result = sbx2.exec("python3 -c \"import requests; print('OK')\"")
        assert result.stdout.strip() == "OK", f"Package not found: {result.stdout}"
        print("  ✓ Packages preserved")
        
        # Verify env var is different from snapshot (new definition)
        result = sbx2.exec("echo $SPAWNED_FROM_SNAPSHOT")
        assert result.stdout.strip() == "true", f"Env var not set: {result.stdout}"
        print("  ✓ New env vars applied (different from snapshot)")

        return 0
    finally:
        if sbx2:
            sbx2.delete()
        if snapshot:
            snapshot.delete()
        if sbx:
            sbx.delete()


if __name__ == "__main__":
    sys.exit(main())
