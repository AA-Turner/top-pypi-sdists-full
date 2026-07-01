#!/usr/bin/env python3
"""Basic command execution"""

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
            name=f"basic-commands-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Simple command
        result = sandbox.exec("echo 'Hello World'")
        print(result.stdout.strip())

        # Python command
        result = sandbox.exec("python3 -c 'print(2 + 2)'")
        print(result.stdout.strip())

        # Multi-line Python script
        result = sandbox.exec(
            '''python3 -c "
import sys
print(f'Python version: {sys.version.split()[0]}')
print(f'Platform: {sys.platform}')
"'''
        )
        print(result.stdout.strip())

        # Failing command returns non-zero exit code
        result = sandbox.exec("ls /nonexistent")
        print(f"Exit code: {result.exit_code}")
        assert result.exit_code != 0, "Expected non-zero exit code"

        return 0
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
