"""Tests for tests/smoke/assert.py — the post-install matrix assertion.

This file exists because the smoke assertion silently failed across
v0.1.20 + v0.1.21: it queried the wrong table name (`records` instead
of `provenance_records`) and asserted a `reports/` dir that the
workflow's command sequence (`init` + `scan` only, no `report run`)
never produces. Two release cycles where the entire matrix was red
without anyone noticing — the workflow_run row in `gh run list`
showed "queued" while individual matrix cells failed.

These tests pin down the contract:
- The script accepts a store dir + exits 0 when a real evidence
  record is present in the `provenance_records` table.
- The script exits 1 when the table is empty.
- The script exits 1 when the SQLite DB is missing.
- The script exits 1 when the table name regresses (no fall-through
  to false-positive PASS).
- The script exits 1 when the store dir doesn't exist at all.
- Importantly: the script does NOT assert a `reports/` directory.
  The smoke workflow runs `init` + `scan` (no `report run`), so
  asserting `reports/` is a category error — the reports pipeline
  is exercised by the E2E smoke that runs on every PR. This test
  locks the assertion against accidentally re-introducing a
  reports/ requirement.
"""

from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

ASSERT_SCRIPT = Path(__file__).resolve().parent / "smoke" / "assert.py"


def _make_store(
    store_dir: Path, *, with_evidence: bool, table_name: str = "provenance_records"
) -> Path:
    """Create a `<store_dir>/store.db` matching the prod schema; optionally seed an evidence row."""
    store_dir.mkdir(parents=True, exist_ok=True)
    db_path = store_dir / "store.db"
    conn = sqlite3.connect(db_path)
    conn.execute(f"""
        CREATE TABLE {table_name} (
            record_id    TEXT PRIMARY KEY,
            record_type  TEXT NOT NULL,
            content_ref  TEXT NOT NULL,
            derived_from TEXT NOT NULL,
            primitive    TEXT,
            agent        TEXT,
            model        TEXT,
            prompt_hash  TEXT,
            timestamp    TEXT NOT NULL,
            metadata     TEXT NOT NULL
        )
    """)
    if with_evidence:
        conn.execute(
            f"""INSERT INTO {table_name}
                (record_id, record_type, content_ref, derived_from, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?)""",
            ("rec-1", "evidence", "sha256:abc", "[]", "2026-05-07T00:00:00Z", "{}"),
        )
    conn.commit()
    conn.close()
    return db_path


def _run_assert(store_dir: Path) -> tuple[int, str]:
    proc = subprocess.run(  # nosemgrep
        [sys.executable, str(ASSERT_SCRIPT), str(store_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout + proc.stderr


def test_assert_passes_with_seeded_evidence(tmp_path: Path) -> None:
    """Happy path: a store with one evidence record satisfies the assertion."""
    store = tmp_path / "store"
    _make_store(store, with_evidence=True)
    code, out = _run_assert(store)
    assert code == 0, f"expected exit 0; got {code}. Output:\n{out}"
    assert "PASS" in out
    assert "evidence_records=1" in out


def test_assert_fails_when_db_missing(tmp_path: Path) -> None:
    store = tmp_path / "store"
    store.mkdir()
    # No store.db file.
    code, out = _run_assert(store)
    assert code == 1
    assert "SQLite DB missing" in out


def test_assert_fails_when_store_dir_missing(tmp_path: Path) -> None:
    code, out = _run_assert(tmp_path / "does-not-exist")
    assert code == 1
    assert "store dir" in out and "does not exist" in out


def test_assert_fails_when_table_present_but_empty(tmp_path: Path) -> None:
    """Store exists, schema correct, but no evidence rows → fail.
    Locks the no-evidence-records path that pre-v0.1.22 was masked
    by the wrong-table-name bug."""
    store = tmp_path / "store"
    _make_store(store, with_evidence=False)
    code, out = _run_assert(store)
    assert code == 1
    assert "no evidence records in provenance_records" in out


def test_assert_does_not_require_reports_dir(tmp_path: Path) -> None:
    """The smoke workflow runs `init` + `scan` (no `report run`). The
    assertion must NOT require a `reports/` dir — that requirement
    silently failed every matrix cell across v0.1.20 + v0.1.21.

    This test locks the contract: with a valid store and no reports/
    dir at all, the assertion passes."""
    store = tmp_path / "store"
    _make_store(store, with_evidence=True)
    assert not (store / "reports").exists()
    code, out = _run_assert(store)
    assert code == 0, f"reports/ should not be required; got exit {code}:\n{out}"


def test_assert_queries_provenance_records_not_records(tmp_path: Path) -> None:
    """If a future schema rename creates a `records` table without
    `provenance_records`, the smoke assertion must fail (not silently
    pass against the wrong table).

    Lock: when only a `records` table exists and `provenance_records`
    does not, the assertion fails with a clear sqlite error.
    """
    store = tmp_path / "store"
    _make_store(store, with_evidence=True, table_name="records")
    code, out = _run_assert(store)
    assert code == 1
    assert "sqlite error" in out and "provenance_records" in out


def test_assert_usage_message_on_wrong_argc() -> None:
    proc = subprocess.run(  # nosemgrep
        [sys.executable, str(ASSERT_SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "Usage:" in proc.stderr


def test_assert_script_is_executable_and_locatable() -> None:
    """Sanity: the script lives at its documented path."""
    assert ASSERT_SCRIPT.is_file(), f"smoke assertion script missing at {ASSERT_SCRIPT}"
    body = ASSERT_SCRIPT.read_text(encoding="utf-8")
    # Pin the corrected query string so a careless edit reverting the
    # table name immediately breaks this test.
    assert "FROM provenance_records" in body
    assert "FROM records WHERE" not in body


def test_assert_passes_against_readonly_db(tmp_path: Path) -> None:
    """Lock for the docker-ghcr matrix cells: the container writes the
    SQLite store as root, the host's python (runner user) can't open
    it read-write. v0.1.22's fix surfaced this as a follow-on failure
    ("attempt to write a readonly database"); v0.1.23 fixed it by
    opening the DB in URI read-only mode.

    Test: chmod the DB file to read-only and verify the assertion
    still passes. This catches a regression where someone changes the
    `?mode=ro&immutable=1` URI back to a default read-write open.
    """
    import os
    import stat

    store = tmp_path / "store"
    db_path = _make_store(store, with_evidence=True)
    # Make the DB strictly read-only (matches root-owned-on-host case
    # without needing to actually run as root). chmod 0o444 = r--r--r--.
    os.chmod(db_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    try:
        code, out = _run_assert(store)
        assert code == 0, f"expected exit 0 against read-only DB; got {code}:\n{out}"
        assert "evidence_records=1" in out
    finally:
        # Restore writable so pytest's tmp_path cleanup can remove it.
        os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)


def test_assert_passes_against_wal_mode_readonly_dir(tmp_path: Path) -> None:
    """Stronger lock: reproduce the actual prod failure mode.

    The Efterlev provenance store enables WAL via
    `PRAGMA journal_mode=WAL` (src/efterlev/provenance/store.py:87).
    SQLite by default still tries to open a writable journal file in
    the same directory as the DB — even on SELECT, even with
    `?mode=ro` — to handle hot-journal recovery. If the directory
    itself is read-only (matches prod docker-ghcr: container writes
    the store as root, host can't write into the dir), SQLite raises
    "attempt to write a readonly database" during the SELECT.

    `?mode=ro` alone is NOT enough for this case. `&immutable=1`
    tells SQLite the DB is on read-only media and skips ALL write-
    path operations including journal opens. v0.1.23 shipped with
    only `?mode=ro` and the docker-ghcr cells STILL failed; v0.1.24
    adds `&immutable=1`.

    This test reproduces the prod scenario: WAL-mode store + chmod
    on the DIRECTORY (not just the file) to read-only. Without
    `immutable=1` this test fails with the exact prod error message.
    Verified by A/B test before commit.
    """
    import os
    import stat

    store = tmp_path / "store"
    store.mkdir(parents=True, exist_ok=True)
    db_path = store / "store.db"

    # Create the DB with WAL mode enabled (matches prod store schema).
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE provenance_records (
            record_id    TEXT PRIMARY KEY,
            record_type  TEXT NOT NULL,
            content_ref  TEXT NOT NULL,
            derived_from TEXT NOT NULL,
            primitive    TEXT,
            agent        TEXT,
            model        TEXT,
            prompt_hash  TEXT,
            timestamp    TEXT NOT NULL,
            metadata     TEXT NOT NULL
        )
    """)
    conn.execute(
        """INSERT INTO provenance_records
           (record_id, record_type, content_ref, derived_from, timestamp, metadata)
           VALUES (?, ?, ?, ?, ?, ?)""",
        ("rec-1", "evidence", "sha256:wal", "[]", "2026-05-07T00:00:00Z", "{}"),
    )
    conn.commit()
    conn.close()

    # Make BOTH the DB and the parent directory read-only — matches
    # the docker-ghcr prod case where the host runner can't write
    # into a root-owned mounted volume. r-x for the dir so we can
    # still list it; r-- for the file. SQLite under `?mode=ro` alone
    # would attempt a journal-file open in the read-only directory
    # and fail with "attempt to write a readonly database".
    os.chmod(db_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    os.chmod(store, stat.S_IRUSR | stat.S_IXUSR)
    try:
        code, out = _run_assert(store)
        assert code == 0, (
            f"WAL + readonly dir should pass with immutable=1 URI; "
            f"got exit {code}. The fix is `?mode=ro&immutable=1`, NOT "
            f"`?mode=ro` alone. Output:\n{out}"
        )
        assert "evidence_records=1" in out
    finally:
        os.chmod(store, stat.S_IRWXU)
        os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)


def test_assert_uri_includes_immutable_flag(tmp_path: Path) -> None:
    """Hard-pin the v0.1.24 fix shape against accidental reversion.

    A future edit reverting `?mode=ro&immutable=1` back to `?mode=ro`
    alone would re-break docker-ghcr cells (WAL mode + readonly file).
    Pin both the mode + immutable params at the source level."""
    body = ASSERT_SCRIPT.read_text(encoding="utf-8")
    assert "mode=ro" in body, "URI mode=ro flag missing from assert.py"
    assert "immutable=1" in body, (
        "URI immutable=1 flag missing from assert.py; without it, WAL-mode "
        "stores with read-only files (docker-ghcr cells) fail with "
        "'attempt to write a readonly database'."
    )


@pytest.mark.parametrize("evidence_count", [1, 2, 5])
def test_assert_passes_with_multiple_records(tmp_path: Path, evidence_count: int) -> None:
    """Realistic scans produce many evidence records; lock the count path."""
    store = tmp_path / "store"
    db_path = _make_store(store, with_evidence=False)
    conn = sqlite3.connect(db_path)
    for i in range(evidence_count):
        conn.execute(
            """INSERT INTO provenance_records
               (record_id, record_type, content_ref, derived_from, timestamp, metadata)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (f"rec-{i}", "evidence", f"sha256:{i:064x}", "[]", "2026-05-07T00:00:00Z", "{}"),
        )
    conn.commit()
    conn.close()
    code, out = _run_assert(store)
    assert code == 0, f"expected exit 0; got {code}:\n{out}"
    assert f"evidence_records={evidence_count}" in out
