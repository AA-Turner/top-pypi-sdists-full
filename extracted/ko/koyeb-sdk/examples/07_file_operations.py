#!/usr/bin/env python3
"""Basic file operations"""

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
            name=f"file-ops-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Write file
        content = "Hello, Koyeb Sandbox!\nThis is a test file."
        fs.write_file("/tmp/hello.txt", content)

        # Read file
        file_info = fs.read_file("/tmp/hello.txt")
        print(file_info.content)

        # Write Python script
        python_code = "#!/usr/bin/env python3\nprint('Hello from Python!')\n"
        fs.write_file("/tmp/script.py", python_code)
        sandbox.exec("chmod +x /tmp/script.py")
        result = sandbox.exec("/tmp/script.py")
        print(result.stdout.strip())

        return 0

    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
