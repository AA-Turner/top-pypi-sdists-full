#!/usr/bin/env python3
"""File manipulation operations (async variant)"""

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
            name=f"file-manip-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Setup
        await fs.write_file("/tmp/file1.txt", "Content of file 1")
        await fs.write_file("/tmp/file2.txt", "Content of file 2")
        await fs.mkdir("/tmp/test_dir")

        # Rename file
        await fs.rename_file("/tmp/file1.txt", "/tmp/renamed_file.txt")
        renamed_exists = await fs.exists("/tmp/renamed_file.txt")
        print(f"Renamed: {renamed_exists}")

        # Move file
        await fs.move_file("/tmp/file2.txt", "/tmp/test_dir/moved_file.txt")
        moved_exists = await fs.exists("/tmp/test_dir/moved_file.txt")
        print(f"Moved: {moved_exists}")

        # Copy file (read + write)
        original_content = await fs.read_file("/tmp/renamed_file.txt")
        await fs.write_file("/tmp/test_dir/copied_file.txt", original_content.content)
        copied_exists = await fs.exists("/tmp/test_dir/copied_file.txt")
        print(f"Copied: {copied_exists}")

        # Delete file
        await fs.rm("/tmp/renamed_file.txt")
        deleted_check = not await fs.exists("/tmp/renamed_file.txt")
        print(f"Deleted: {deleted_check}")

        # Delete directory
        await fs.rm("/tmp/test_dir", recursive=True)
        dir_deleted_check = not await fs.exists("/tmp/test_dir")
        print(f"Directory deleted: {dir_deleted_check}")

        return 0

    finally:
        if sandbox:
            await sandbox.delete()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
