#!/usr/bin/env python3
"""Create a sandbox and then retrieve it by service ID (async)"""

import asyncio
import sys
import os
import sys


import random
import string
from koyeb import AsyncSandbox


async def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    original_sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    retrieved_sandbox = None

    try:
        # Step 1: Create a new sandbox
        print("Creating a new sandbox...")
        original_sandbox = await AsyncSandbox.create(
            image="koyeb/sandbox:slim",
            name="example-sandbox",
            wait_ready=True,
            api_token=api_token,
        )

        print(f"✓ Created sandbox: {original_sandbox.name}")
        print(f"  Service ID: {original_sandbox.service_id}")
        print(f"  App ID: {original_sandbox.app_id}")

        # Execute a command with the original sandbox
        result = await original_sandbox.exec("echo 'Hello from original sandbox!'")
        print(f"  Original sandbox output: {result.stdout.strip()}")

        # Step 2: Retrieve the same sandbox using its service ID
        print("\nRetrieving sandbox by service ID...")
        retrieved_sandbox = await AsyncSandbox.get_from_id(
            id=original_sandbox.id,
            api_token=api_token,
        )

        print(f"✓ Retrieved sandbox: {retrieved_sandbox.name}")
        print(f"  Service ID: {retrieved_sandbox.service_id}")
        print(f"  App ID: {retrieved_sandbox.app_id}")

        # Verify it's the same sandbox
        assert original_sandbox.id == retrieved_sandbox.id, "Sandbox IDs should match!"
        print("  ✓ Confirmed: Same sandbox retrieved")

        # Check health
        is_healthy = await retrieved_sandbox.is_healthy()
        print(f"  Healthy: {is_healthy}")

        # Execute a command with the retrieved sandbox
        if is_healthy:
            result = await retrieved_sandbox.exec(
                "echo 'Hello from retrieved sandbox!'"
            )
            print(f"  Retrieved sandbox output: {result.stdout.strip()}")

        return 0

    finally:
        # Cleanup: delete the sandbox (works from either instance)
        if original_sandbox:
            print("\nCleaning up...")
            await original_sandbox.delete()
            print("✓ Sandbox deleted")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
