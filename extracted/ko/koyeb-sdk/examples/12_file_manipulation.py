#!/usr/bin/env python3
"""File manipulation operations"""

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
            name=f"file-manip-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )

        fs = sandbox.filesystem

        # Setup
        fs.write_file("/tmp/file1.txt", "Content of file 1")
        fs.write_file("/tmp/file2.txt", "Content of file 2")
        fs.mkdir("/tmp/test_dir")

        # Rename file
        fs.rename_file("/tmp/file1.txt", "/tmp/renamed_file.txt")
        renamed_exists = fs.exists("/tmp/renamed_file.txt")
        print(f"Renamed: {renamed_exists}")
        assert renamed_exists

        # Move file
        fs.move_file("/tmp/file2.txt", "/tmp/test_dir/moved_file.txt")
        moved_exists = fs.exists("/tmp/test_dir/moved_file.txt")
        print(f"Moved: {moved_exists}")
        assert moved_exists

        # Copy file (read + write)
        original_content = fs.read_file("/tmp/renamed_file.txt")
        fs.write_file("/tmp/test_dir/copied_file.txt", original_content.content)
        copied_exists = fs.exists("/tmp/test_dir/copied_file.txt")
        print(f"Copied: {copied_exists}")
        assert copied_exists

        # Delete file
        fs.rm("/tmp/renamed_file.txt")
        deleted = not fs.exists("/tmp/renamed_file.txt")
        print(f"Deleted: {deleted}")
        assert deleted

        # Delete directory
        fs.rm("/tmp/test_dir", recursive=True)
        directory_deleted = not fs.exists("/tmp/test_dir")
        print(f"Directory deleted: {directory_deleted}")
        assert directory_deleted

        return 0

    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
