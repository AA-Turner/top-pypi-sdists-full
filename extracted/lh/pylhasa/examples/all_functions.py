from __future__ import annotations

from pathlib import Path

import pylhasa


def main() -> int:
    path = Path("example.lha")
    if not path.exists():
        print("Place an archive named example.lha in the current directory to run this example.")
        return 2

    # open(path)
    archive = pylhasa.open(path)
    try:
        # Iterate entries
        entries = list(archive)
        print(f"entries: {len(entries)}")
        if not entries:
            return 0

        entry = entries[0]
        print(f"first entry: {entry.raw_path} method={entry.method}")
        print(f"normalized time: {entry.datetime_utc()}")

        # read(name_or_entry)
        data = entry.read()
        print(f"read bytes: {len(data)}")

        # extract(name_or_entry)
        out_dir = Path("out")
        out_path = archive.extract(entry, out_dir, verify_crc=True)
        print(f"extracted to: {out_path}")

        # extractall
        archive.extractall(out_dir, verify_crc=True)

    finally:
        archive.close()

    # open_bytes / from_bytes
    data = path.read_bytes()
    with pylhasa.open_bytes(data) as archive2:
        print(f"open_bytes entries: {len(list(archive2))}")

    with pylhasa.from_bytes(data) as archive3:
        print(f"from_bytes entries: {len(list(archive3))}")

    # open_fileobj
    with path.open("rb") as fp:
        archive4 = pylhasa.open_fileobj(fp)
        try:
            print(f"open_fileobj entries: {len(list(archive4))}")
        finally:
            archive4.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
