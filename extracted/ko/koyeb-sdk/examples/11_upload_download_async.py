#!/usr/bin/env python3
"""Upload and download files (async variant)"""

import asyncio
import sys
import os
import sys
import tempfile


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
            name=f"upload-download-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Upload local file to sandbox
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("This is a local file\n")
            f.write("Uploaded to Koyeb Sandbox!")
            local_file = f.name

        try:
            await fs.upload_file(local_file, "/tmp/uploaded_file.txt")
            uploaded_info = await fs.read_file("/tmp/uploaded_file.txt")
            print(uploaded_info.content)
        finally:
            os.unlink(local_file)

        # Download file from sandbox
        await fs.write_file(
            "/tmp/download_source.txt", "Download test content\nMultiple lines"
        )

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix="_downloaded.txt") as f:
            download_path = f.name

        try:
            await fs.download_file("/tmp/download_source.txt", download_path)
            with open(download_path, "r") as f:
                print(f.read())
        finally:
            os.unlink(download_path)

        return 0

    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
