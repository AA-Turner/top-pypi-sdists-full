"""
Reconstruct the current state of a LevelDB database and write it to JSON.

Usage:
    python dump_to_json.py <db_dir> [output.json]

If no output path is given, the result is printed to stdout.
"""

import json
import sys

import rleveldb


def dump(db_dir: str) -> dict:
    result = {}
    with rleveldb.RawLevelDb(db_dir) as db:
        records = db.iterate_records_raw()

    # Replay writes in sequence-number order so that later writes win.
    records.sort(key=lambda r: r.seq)

    for rec in records:
        key = rec.user_key.decode("utf-8", errors="replace")

        if rec.state == rleveldb.KeyState.Live:
            raw = rec.value
            try:
                result[key] = json.loads(raw)
            except (json.JSONDecodeError, UnicodeDecodeError):
                result[key] = raw.decode("utf-8", errors="replace")

        elif rec.state == rleveldb.KeyState.Deleted:
            result.pop(key, None)

    return result


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    db_dir = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) >= 3 else None

    data = dump(db_dir)

    text = json.dumps(data, indent=2, ensure_ascii=False)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"{len(data)} keys written to {out_path}")
    else:
        print(text)


if __name__ == "__main__":
    main()
