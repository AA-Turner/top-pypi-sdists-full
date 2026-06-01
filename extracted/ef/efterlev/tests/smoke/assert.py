#!/usr/bin/env python3
"""Smoke-test assertion: verify `efterlev scan` produced a valid store.

Called by .github/workflows/release-smoke.yml after the scan step in
every matrix cell. Checks that the install produced a real, valid
Efterlev state, not just "exit 0 from somewhere."

Usage:
    python3 tests/smoke/assert.py <store-dir>

Exits 0 on success, 1 on any failure. Prints a short human-readable
summary on both paths.

Two bugs in v0.1.20-v0.1.21's version of this script silently failed
the entire matrix on every release; the workflow stayed "queued" in
`gh run list` so the failures went unnoticed for two release cycles.
v0.1.22 fixes both and lands a unit test (`tests/test_smoke_assert.py`)
+ a T7 in `scripts/triage.sh` that surfaces matrix conclusion on the
release page so silent matrix failures cannot recur.

Bugs fixed in v0.1.22:
- `FROM records` → `FROM provenance_records`. The actual table is
  `provenance_records` (see `src/efterlev/provenance/store.py:32`).
  The wrong name raised `OperationalError: no such table: records`,
  caught by the bare `sqlite3.Error` handler, surfaced as
  "sqlite error querying store: no such table: records".
- The script asserted `<store>/reports/` exists; but the workflow
  runs `efterlev init` + `efterlev scan` only, not `efterlev report
  run`. `scan` writes to the SQLite store; `report run` is what
  generates HTML. The reports/ assertion was always wrong against
  the workflow's actual command sequence — we just hadn't observed
  the false-positive PASS on a working release because the SQLite
  bug above was masking it. v0.1.22 drops the reports/ check from
  the smoke assertion. The reports pipeline is exercised by the
  full E2E smoke (Anthropic, Sonnet 4.6) on every PR — that's the
  right place for it.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <store-dir>", file=sys.stderr)
        return 1

    store_dir = Path(sys.argv[1])
    failures: list[str] = []
    evidence_count = 0

    if not store_dir.is_dir():
        failures.append(f"store dir {store_dir} does not exist")

    db_path = store_dir / "store.db"
    if not db_path.is_file():
        failures.append(f"SQLite DB missing at {db_path}")

    if db_path.is_file():
        try:
            # Open the DB in immutable read-only mode via SQLite URI.
            #
            # The smoke workflow's docker-ghcr cells run `efterlev` inside a
            # container that writes the SQLite store as root onto the mounted
            # host volume, leaving the file root-owned. The host-side
            # `python3` (running as the runner user) can read but not write
            # to that file. The default `sqlite3.connect()` mode is read-
            # write, so the open + first journal-create attempt raises
            # "attempt to write a readonly database".
            #
            # `?mode=ro` alone is NOT enough for our schema, because the
            # store enables WAL via `PRAGMA journal_mode=WAL`
            # (src/efterlev/provenance/store.py:87). WAL mode requires
            # writable `.wal` and `.shm` files even for reads. v0.1.23's
            # initial fix used `mode=ro` only and still hit the readonly
            # error in docker-ghcr cells — caught by v0.1.23's first
            # release-smoke run.
            #
            # `&immutable=1` tells SQLite the database is on read-only
            # media and won't change. SQLite skips WAL/SHM operations
            # entirely. That's the correct mode for a frozen post-scan
            # store the smoke assertion is just counting rows in. v0.1.24
            # closes the docker-ghcr cell failure for real.
            conn = sqlite3.connect(f"file:{db_path}?mode=ro&immutable=1", uri=True)
            cur = conn.execute(
                "SELECT COUNT(*) FROM provenance_records WHERE record_type = 'evidence'"
            )
            (evidence_count,) = cur.fetchone()
            if evidence_count == 0:
                failures.append("no evidence records in provenance_records table")
        except sqlite3.Error as e:
            failures.append(f"sqlite error querying store: {e}")

    print(
        f"Smoke assertion state: "
        f"store_dir={store_dir.is_dir()}, "
        f"db={db_path.is_file()}, "
        f"evidence_records={evidence_count}"
    )

    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
