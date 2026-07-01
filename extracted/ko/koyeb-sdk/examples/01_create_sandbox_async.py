#!/usr/bin/env python3
"""Create and manage a sandbox (async variant)"""

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

    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        sandbox = await AsyncSandbox.create(
            image="koyeb/sandbox:slim",
            name=f"example-sandbox-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Check health
        is_healthy = await sandbox.is_healthy()
        print(f"Healthy: {is_healthy}")

        # Test command
        result = await sandbox.exec("echo 'Sandbox is ready!'")
        print(result.stdout.strip())

        return 0
    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
