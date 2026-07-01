#!/usr/bin/env python3
"""Basic file operations (async variant)"""

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
            name=f"file-ops-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Write file
        content = "Hello, Koyeb Sandbox!\nThis is a test file."
        await fs.write_file("/tmp/hello.txt", content)

        # Read file
        file_info = await fs.read_file("/tmp/hello.txt")
        print(file_info.content)

        # Write Python script
        python_code = "#!/usr/bin/env python3\nprint('Hello from Python!')\n"
        await fs.write_file("/tmp/script.py", python_code)
        await sandbox.exec("chmod +x /tmp/script.py")
        result = await sandbox.exec("/tmp/script.py")
        print(result.stdout.strip())

        return 0

    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
