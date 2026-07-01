#!/usr/bin/env python3
"""Directory operations"""

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
            name=f"directory-ops-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Create directory
        fs.mkdir("/tmp/my_project")

        # Create nested directories (API creates parents automatically)
        fs.mkdir("/tmp/my_project/src/utils")

        # List directory
        contents = fs.list_dir("/tmp/my_project")
        print(f"Contents: {contents}")

        # Create project structure
        fs.mkdir("/tmp/my_project/src")
        fs.mkdir("/tmp/my_project/tests")
        fs.write_file("/tmp/my_project/src/main.py", "print('Hello')")
        fs.write_file("/tmp/my_project/README.md", "# My Project")

        # Check if path exists
        exists = fs.exists("/tmp/my_project")
        is_dir = fs.is_dir("/tmp/my_project")
        is_file = fs.is_file("/tmp/my_project/src/main.py")
        print(f"Exists: {exists}, Is dir: {is_dir}, Is file: {is_file}")

        return 0

    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
