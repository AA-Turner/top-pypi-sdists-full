#!/usr/bin/env python3
"""Streaming command output (async variant)"""

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
            name=f"streaming-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        # Stream output in real-time
        result = await sandbox.exec(
            '''python3 -u -c "
import time
for i in range(5):
    print(f'Line {i+1}')
    time.sleep(0.5)
"''',
            on_stdout=lambda data: print(data.strip()),
            on_stderr=lambda data: print(f"ERR: {data.strip()}"),
        )
        print(f"\nExit code: {result.exit_code}")

        # Stream a script
        await sandbox.filesystem.write_file(
            "/tmp/counter.py",
            "#!/usr/bin/env python3\nimport time\nfor i in range(1, 6):\n    print(f'Count: {i}')\n    time.sleep(0.3)\nprint('Done!')\n",
        )
        await sandbox.exec("chmod +x /tmp/counter.py")

        result = await sandbox.exec(
            "python3 /tmp/counter.py",
            on_stdout=lambda data: print(data.strip()),
        )

        return 0
    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
