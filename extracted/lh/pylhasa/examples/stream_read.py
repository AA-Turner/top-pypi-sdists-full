from __future__ import annotations

import sys

import pylhasa


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python examples/stream_read.py <archive.lha> <entry_name>")
        return 2
    archive_path = sys.argv[1]
    entry_name = sys.argv[2]

    archive = pylhasa.open(archive_path)
    try:
        entry = next(e for e in archive if e.raw_path == entry_name or e.safe_path == entry_name)
        total = 0
        with entry.open() as stream:
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    break
                total += len(chunk)
        print(f"streamed {total} bytes from {entry_name}")
    finally:
        archive.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
