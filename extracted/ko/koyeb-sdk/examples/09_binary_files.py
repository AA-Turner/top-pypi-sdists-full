#!/usr/bin/env python3
"""Binary file operations"""

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
            name=f"binary-files-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Write binary data (encoding="base64" handles the encoding automatically)
        binary_data = b"Binary data: \x00\x01\x02\x03\xff\xfe\xfd"
        fs.write_file("/tmp/binary.bin", binary_data, encoding="base64")

        # Read binary data (encoding="base64" decodes and returns bytes)
        file_info = fs.read_file("/tmp/binary.bin", encoding="base64")
        print(f"Original: {binary_data}")
        print(f"Read back: {file_info.content}")
        assert binary_data == file_info.content

        return 0

    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
