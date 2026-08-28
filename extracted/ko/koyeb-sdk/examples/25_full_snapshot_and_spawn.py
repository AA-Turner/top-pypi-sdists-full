#!/usr/bin/env python3
"""Create a sandbox, take a full snapshot, and spawn a new sandbox from it

This example demonstrates creating a full snapshot (including both filesystem
and process state) as opposed to example 21 which uses filesystem-only snapshots.
"""

import os
import sys
import random
import string

from koyeb import Sandbox
from koyeb.sandbox import SnapshotType
from koyeb.sandbox.utils import SandboxTimeoutError


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
            name=f"full-snapshot-and-spawn-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox created: {sbx.name}")

        # Create some files to verify filesystem preservation
        print("✓ Creating files...")
        sbx.filesystem.mkdir("/workspace")
        sbx.filesystem.write_file("/workspace/requirements.txt", "requests\n")
        print("  ✓ Files created")

        # Install packages
        print("✓ Installing packages...")
        sbx.exec("pip3 install requests")
        print("  ✓ Packages installed")

        # Start daemon http server in the background on port 8000
        print("✓ Running HTTP daemon server on port 8000...")
        try:
            sbx.exec("python3 -m http.server", timeout=2)
        except SandboxTimeoutError:
            pass
        print("  ✓ Started HTTP daemon server on port 8000")

        # Take a FULL snapshot (includes both filesystem and process state)
        print("✓ Creating full snapshot...")
        snapshot = sbx.snapshot(
            name=f"python-full-snapshot-{suffix}",
            snapshot_type=SnapshotType.FULL,
        )
        print(f"  ✓ Full snapshot created: {snapshot.name}")

        # Spawn a new sandbox from the snapshot with a different instance type
        print("✓ Spawning sandbox from full snapshot with different instance type...")
        sbx2 = snapshot.spawn(
            image="python:3.12",
            name=f"test-runner-full-{suffix}",
            instance_type="nano",
            wait_ready=False,
            api_token=api_token,
        )
        print(f"  ✓ Sandbox spawned: {sbx2.name}")

        # Wait for the spawned sandbox to be ready
        print("✓ Waiting for spawned sandbox to be ready...")
        is_ready = sbx2.wait_ready(timeout=300)
        print("  ✓ Sandbox is ready")

        # Verify filesystem is preserved from snapshot
        print("✓ Verifying full snapshot...")

        # Check that packages are pre-installed
        result = sbx2.exec("python3 -c \"import requests; print('OK')\"")
        assert result.stdout.strip() == "OK", f"Package not found: {result.stdout}"
        print("  ✓ Python package installed preserved")

        # Verify processes are preserved
        result = sbx2.exec("curl localhost:8000")
        assert "Directory listing for /" in result.stdout.strip(), "HTTP server launched in original sandbox is not running anymore"
        print("  ✓ Daemon HTTP server launched on initial sandbox is still running")

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
