#!/usr/bin/env python3
"""Create a single sandbox with auto-delete lifecycle setting and wait for it to be deleted"""

import os
import sys
import time


import random
import string
from koyeb import Sandbox
from koyeb.sandbox.utils import get_api_clients


def service_exists(api_token: str, service_id: str) -> bool:
    """Check if a service still exists"""
    try:
        services_api = get_api_clients(api_token).services
        services_api.get_service(service_id)
        return True
    except Exception:
        return False


def main():
    print("=" * 70)
    print(" SIMPLE AUTO-DELETE SANDBOX DEMO")
    print("=" * 70)
    print()
    print("This example creates a single sandbox with auto-delete after creation.")
    print()

    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    try:
        delete_after_delay = 60  # Delete 60s after creation

        print("→ Creating sandbox with auto-delete...")
        print(f"  - delete_after_delay: {delete_after_delay}s (delete after creation)")
        print(f"  → Expected deletion: ~{delete_after_delay}s after creation")
        print()

        create_start = time.time()
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"auto-delete-test-simple-{suffix}",
            wait_ready=True,
            api_token=api_token,
            delete_after_delay=delete_after_delay,
        )
        create_duration = time.time() - create_start
        print(f"✓ Created in {create_duration:.1f}s")
        print(f"  Service ID: {sandbox.service_id}")

        # Quick health check
        print()
        print("→ Verifying sandbox is healthy...")
        assert sandbox.is_healthy(), "Sandbox should be healthy"
        result = sandbox.exec("echo 'Sandbox ready'")
        print(f"  ✓ {result.stdout.strip()}")
        print()

        # Wait for auto-deletion
        print("→ Waiting for sandbox to be auto-deleted...")
        start = time.time()
        timeout = 300

        while time.time() - start < timeout:
            if not service_exists(api_token, sandbox.service_id):
                duration = time.time() - start
                print(f"✓ Sandbox was auto-deleted after {duration:.1f}s")
                sandbox = None
                break
            time.sleep(5)
            elapsed = time.time() - start
            print(f"  ... still waiting ({elapsed:.0f}s elapsed)")
        else:
            print(f"✗ Timeout waiting for sandbox to be deleted")

        return 0

    finally:
        if sandbox:
            print()
            print("→ Manually deleting sandbox (wasn't auto-deleted)...")
            sandbox.delete()

        print()
        print("✓ Demo completed")


if __name__ == "__main__":
    sys.exit(main())
