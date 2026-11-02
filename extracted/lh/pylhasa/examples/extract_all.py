from __future__ import annotations

import sys
from pathlib import Path

import pylhasa


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python examples/extract_all.py <archive.lha> <dest_dir>")
        return 2
    archive_path = sys.argv[1]
    dest = Path(sys.argv[2])

    archive = pylhasa.open(archive_path)
    try:
        extracted = archive.extractall(dest, verify_crc=True)
        print(f"extracted {len(extracted)} entries to {dest}")
    finally:
        archive.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
