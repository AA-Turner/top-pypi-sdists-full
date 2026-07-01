#!/usr/bin/env python3
"""Working directory for commands (async variant)"""

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
            name=f"working-dir-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Setup: create directory structure
        await sandbox.exec("mkdir -p /tmp/my_project/src")
        await sandbox.exec("echo 'print(\\\"hello\\\")' > /tmp/my_project/src/main.py")

        # Run command in specific directory
        result = await sandbox.exec("pwd", cwd="/tmp/my_project")
        print(result.stdout.strip())

        # List files in working directory
        result = await sandbox.exec("ls -la", cwd="/tmp/my_project")
        print(result.stdout.strip())

        # Use relative paths
        result = await sandbox.exec("cat src/main.py", cwd="/tmp/my_project")
        print(result.stdout.strip())

        return 0

    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
