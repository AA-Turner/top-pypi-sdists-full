#!/usr/bin/env python3
"""Create sandboxes with custom entrypoint and command"""

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

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # Example 1: Custom command with args
    print("=== Example 1: Custom command ===")
    sandbox = None
    try:
        sandbox = Sandbox.create(
            image="ubuntu",
            name=f"custom-command-{suffix}",
            command="/bin/sh",
            args=["-c", "touch /tmp/command-was-here && sleep infinity"],
            api_token=api_token,
            env={"LOG_LEVEL": "DEBUG"} 
        )
        result = sandbox.exec("cat /tmp/command-was-here && echo 'File exists'")
        print(f"  {result.stdout.strip()}")
        assert result.exit_code == 0, "Expected /tmp/command-was-here to exist"
        print("  OK: custom command created the file")
    finally:
        if sandbox:
            sandbox.delete()

    # Example 2: Custom entrypoint with command
    # Use a custom entrypoint that runs python, proving the entrypoint was used.
    print("=== Example 2: Custom entrypoint ===")
    sandbox = None
    try:
        sandbox = Sandbox.create(
            image="python:3.12-slim",
            name=f"custom-entrypoint-{suffix}",
            entrypoint=["python3", "-c"],
            command="import os; os.makedirs('/tmp', exist_ok=True); open('/tmp/started-by-python', 'w').write('yes'); import time; time.sleep(999999)",
            api_token=api_token,
        )
        # The file was created by python3 (the entrypoint), not bash
        result = sandbox.exec("cat /tmp/started-by-python")
        content = result.stdout.strip()
        print(f"  Marker content: {content}")
        assert content == "yes", f"Expected 'yes', got '{content}'"
        print("  OK: python3 entrypoint created the marker file")
    finally:
        if sandbox:
            sandbox.delete()

    return 0


if __name__ == "__main__":
    sys.exit(main())
