#!/usr/bin/env python3
"""Create and manage a sandbox"""

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

    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"example-sandbox-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Check health
        is_healthy = sandbox.is_healthy()
        print(f"Healthy: {is_healthy}")

        # Test command
        result = sandbox.exec("echo 'Sandbox is ready!'")
        print(result.stdout.strip())

        return 0
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
