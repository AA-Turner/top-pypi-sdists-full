from __future__ import annotations

import sys

import pylhasa


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python examples/list_entries.py <archive.lha>")
        return 2
    path = sys.argv[1]
    archive = pylhasa.open(path)
    try:
        for entry in archive:
            print(
                f"{entry.raw_path} method={entry.method} size={entry.size} "
                f"compressed={entry.compressed_size} dir={entry.is_dir} symlink={entry.is_symlink} "
                f"header_level={entry.header_level} time={entry.datetime_utc()}"
            )
    finally:
        archive.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
