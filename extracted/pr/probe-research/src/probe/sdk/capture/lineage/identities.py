"""a file's identity (sha256, fingerprint, rows) cached per machine, charged against the run's one I/O budget."""

from __future__ import annotations
import hashlib
import os
import sqlite3
import sys
import threading
import time
from typing import Any
FULL_HASH_MAX_BYTES = 1 << 30
#: Row counts from the hashing read (C9, R27): newline-terminated records,
#: a final unterminated line counted; csv/tsv without their header line.
ROW_COUNTED_SUFFIXES = (".jsonl", ".ndjson", ".csv", ".tsv", ".txt")
_HEADED_SUFFIXES = (".csv", ".tsv")
#: `num_rows` read from the footer, only when pyarrow is already imported.
PARQUET_SUFFIX = ".parquet"
RUN_HASH_BUDGET_BYTES = 10 * (1 << 30)
EDGE_BYTES = 4 << 20
_CHUNK = 1 << 20


class _HashCache:
    """Per-machine sha256 cache keyed on (device, inode, size, mtime, ctime).

    Table ``h3`` carries each file's row count beside its hash (F38): a dataset
    hashed once on a machine must still get its ``rows``. An answer only in the
    older ``h2`` table (a release before row counts) is read too
    (:meth:`get_old`); for a file whose rows are countable it is re-hashed once
    inside the budget, then lives in ``h3``.

    ``batch=N`` holds up to N answers and writes them in ONE transaction
    (:meth:`flush`): a close hashing 2,000 small outputs spent 2.8 s of its
    4.4 s committing them one by one (a sync to disk each)."""

    def __init__(self, *, batch: int = 0) -> None:
        self._batch = batch
        self._pending: list[tuple] = []
        self._db: sqlite3.Connection | None = None
        try:
            path = state_dir().parent / "hashcache.sqlite3"
            path.parent.mkdir(parents=True, exist_ok=True)
            with internal():
                self._db = sqlite3.connect(str(path), timeout=5, check_same_thread=False)
                self._db.execute(
                    "CREATE TABLE IF NOT EXISTS h2 (d INTEGER, i INTEGER, s INTEGER, "
                    "m INTEGER, c INTEGER, sha TEXT, fp TEXT, PRIMARY KEY (d, i, s, m, c))"
                )
                self._db.execute(
                    "CREATE TABLE IF NOT EXISTS h3 (d INTEGER, i INTEGER, s INTEGER, "
                    "m INTEGER, c INTEGER, sha TEXT, fp TEXT, rows INTEGER, PRIMARY KEY (d, i, s, m, c))"
                )
        except (OSError, sqlite3.Error):
            self._db = None

    def get(self, ident: tuple) -> tuple[str | None, str | None, int | None] | None:
        """``(sha, fp, rows)`` from ``h3``, else None."""
        if self._db is None:
            return None
        try:
            with internal():
                row = self._db.execute(
                    "SELECT sha, fp, rows FROM h3 WHERE d=? AND i=? AND s=? AND m=? AND c=?", ident
                ).fetchone()
        except sqlite3.Error:
            return None
        return (row[0], row[1], row[2]) if row else None

    def get_old(self, ident: tuple) -> tuple[str | None, str | None] | None:
        """``(sha, fp)`` from ``h2``, the table before row counts, else None."""
        if self._db is None:
            return None
        try:
            with internal():
                row = self._db.execute(
                    "SELECT sha, fp FROM h2 WHERE d=? AND i=? AND s=? AND m=? AND c=?", ident
                ).fetchone()
        except sqlite3.Error:
            return None
        return (row[0], row[1]) if row else None

    def put(self, ident: tuple, sha: str | None, fp: str | None, rows: int | None = None) -> None:
        if self._db is None:
            return
        self._pending.append((*ident, sha, fp, rows))
        if len(self._pending) > self._batch:
            self.flush()

    def flush(self) -> None:
        rows, self._pending = self._pending, []
        if not rows or self._db is None:
            return
        try:
            with internal(), self._db:
                self._db.executemany(
                    "INSERT OR REPLACE INTO h3 (d, i, s, m, c, sha, fp, rows) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    rows,
                )
        except sqlite3.Error:
            pass


def _counted(path: str) -> bool:
    """Rows of this file are counted in its hashing read (line records)."""
    return path.lower().endswith(ROW_COUNTED_SUFFIXES)


def _parquet_rows(path: str) -> int | None:
    """``num_rows`` from a Parquet file's footer, ONLY when pyarrow is already
    imported (never an import: R27), else None. A small extra read."""
    if not path.lower().endswith(PARQUET_SUFFIX) or "pyarrow" not in sys.modules:
        return None
    try:
        import pyarrow.parquet as pq  # already loaded with pyarrow, or cheap beside it

        with internal():
            rows = pq.read_metadata(path).num_rows
    except Exception:  # noqa: BLE001 -- a count is a bonus, never a failure
        return None
    return rows if isinstance(rows, int) and not isinstance(rows, bool) and rows >= 0 else None


def _rows_of(path: str, newlines: int, last: bytes, size: int) -> int | None:
    """A counted file's rows from its full read: newline-terminated records,
    a final unterminated line too, and for csv/tsv without the header line."""
    if not _counted(path):
        return None
    rows = newlines + (1 if size > 0 and last != b"\n" else 0)
    if path.lower().endswith(_HEADED_SUFFIXES):
        rows = max(rows - 1, 0)
    return rows


def hash_file(
    path: str,
    ident: tuple,
    *,
    cache: _HashCache | None,
    budget: list[int],
    deadline: float | None = None,
    fingerprint: bool = True,
) -> tuple[str | None, str | None, int | None] | None:
    """``(sha256, fingerprint, rows)`` for a file, ``(None, None, None)`` when it
    is no longer the one observed (unstable) or cannot be read, or None when it
    was NOT HASHED: the I/O ``budget`` cannot pay even for a fingerprint, or
    ``deadline`` (a ``time.monotonic()`` instant) has passed.

    ``rows`` is counted in the SAME read as the hash (no second pass, R27) for
    `ROW_COUNTED_SUFFIXES`; a Parquet file's comes from its footer when pyarrow
    is already imported; anything fingerprinted (over 1 GiB, or for budget) has
    none but a Parquet footer's.

    Every byte read is charged to ``budget`` -- a one-element list, shared by
    everything one run hashes: a full hash its size, a fingerprint the edges
    it reads (at most 2 x EDGE_BYTES). A full hash that runs into the deadline
    stops mid-file, is charged what it read, and is None. ``fingerprint=False``
    asks for a full hash or nothing (a reference's ``content_hash``)."""
    with internal():
        if deadline is not None and time.monotonic() >= deadline:
            return None
        try:
            before = _ident(os.stat(path))
        except OSError:
            return (None, None, None)
        if before != ident:
            return (None, None, None)
        old: tuple[str | None, str | None] | None = None
        if cache is not None:
            hit = cache.get(ident)
            if hit is not None and (fingerprint or hit[0] is not None):
                if hit[2] is None:
                    rows = _parquet_rows(path)
                    if rows is not None:
                        cache.put(ident, hit[0], hit[1], rows)
                        return (hit[0], hit[1], rows)
                return hit
            old = cache.get_old(ident)
            if old is not None and (fingerprint or old[0] is not None):
                if old[0] is None or not _counted(path):
                    # Nothing a re-read would add: moved to h3 as it is.
                    answer = (old[0], old[1], _parquet_rows(path))
                    cache.put(ident, *answer)
                    return answer
                # Hashed before row counts existed: re-hashed ONCE, inside the
                # budget, for its rows (F38); the old answer when it cannot pay.
        size = ident[2]
        sha: str | None = None
        fp: str | None = None
        rows: int | None = None
        full = size <= FULL_HASH_MAX_BYTES and _take(budget, size)
        if not full and old is not None:
            return (old[0], old[1], None)
        if not full and not (fingerprint and _take(budget, min(size, 2 * EDGE_BYTES))):
            return None
        try:
            if full:
                digest = hashlib.sha256()
                done = 0
                newlines = 0
                last = b""
                count = _counted(path)
                with open(path, "rb") as handle:
                    for chunk in iter(lambda: handle.read(_CHUNK), b""):
                        digest.update(chunk)
                        if count:
                            newlines += chunk.count(b"\n")
                            last = chunk[-1:]
                        done += len(chunk)
                        if done < size and deadline is not None and time.monotonic() >= deadline:
                            _give_back(budget, size - done)
                            # Re-reading an h2 answer for its rows: the hash it
                            # holds still stands (review of #2791).
                            return (old[0], old[1], None) if old is not None else None
                sha = digest.hexdigest()
                rows = _rows_of(path, newlines, last, done) if count else _parquet_rows(path)
            else:
                digest = hashlib.sha256()
                with open(path, "rb") as handle:
                    digest.update(handle.read(EDGE_BYTES))
                    if size > 2 * EDGE_BYTES:
                        handle.seek(size - EDGE_BYTES)
                    digest.update(handle.read(EDGE_BYTES))
                fp = f"{size}:{ident[3]}:{digest.hexdigest()}"
                rows = _parquet_rows(path)
            after = _ident(os.stat(path))
        except OSError:
            return (None, None, None)
        if after != ident:
            return (None, None, None)
        # A fingerprint taken only because THIS run's budget ran out is not
        # the file's answer: cached, it would stand in for the full hash a
        # later run has the budget for.
        if cache is not None and (sha is not None or size > FULL_HASH_MAX_BYTES):
            cache.put(ident, sha, fp, rows)
        return (sha, fp, rows)


def file_identity(
    path: str,
    *,
    budget: list[int],
    cache: _HashCache | None = None,
    deadline: float | None = None,
    hash_level: bool = False,
) -> dict | None:
    """A file's identity with the recorder's own hasher (F39: one hasher):
    ``{"content_hash", "fingerprint", "size_bytes", "rows"}``, or None when
    ``path`` is not a regular file or cannot be read.

    ``content_hash`` is the sha256 when the file is at most 1 GiB and the
    ``budget`` pays for it; past either, ``fingerprint`` (size, mtime, first
    and last 4 MiB) when the budget pays for that; neither when it cannot (or
    ``deadline`` passed). ``rows`` as :func:`hash_file`. ``hash_level=True``
    (a `.probe.config` `hash` path) applies `HASH_LEVEL_MIN_BYTES`: below it,
    path and size only (F30). Never raises."""
    try:
        with internal():
            st = os.stat(path)
        if not _stat_is_file(st):
            return None
        ident = _ident(st)
        out: dict = {"content_hash": None, "fingerprint": None, "size_bytes": st.st_size, "rows": None}
        if hash_level and st.st_size < HASH_LEVEL_MIN_BYTES:
            return out
        result = hash_file(path, ident, cache=cache, budget=budget, deadline=deadline)
        if result is None:
            return out
        sha, fp, rows = result
        if sha is None and fp is None:
            return None  # it moved while it was read, or cannot be read
        out.update(content_hash=sha, fingerprint=fp, rows=rows)
        return out
    except Exception:  # noqa: BLE001 -- an identity is evidence, never a failure
        return None


def reference_hash(
    path: str, *, budget: list[int], deadline: float, size: int | None = None, mtime_ns: int | None = None
) -> str | None:
    """sha256 of a file output capture records as a REFERENCE (F3: 64 MB to
    1 GiB, not uploaded), so a later read of those bytes can match it -- paid
    from ``budget``, never past ``deadline``. Everything that touches the file,
    its stat included, runs on a daemon thread the caller waits for only until
    then: a stalled mount costs the hash, never the close. None when the file
    is over 1 GiB, changed from the ``size``/``mtime_ns`` capture listed, or
    the budget or the time ran out. The machine's hash cache answers for a
    file this run's write list already hashed."""
    if time.monotonic() >= deadline:
        return None
    box: dict[str, Any] = {}

    def work() -> None:
        _local.internal = 1
        try:
            st = os.stat(path)
            if not _stat_is_file(st) or st.st_size > FULL_HASH_MAX_BYTES:
                return
            if (size is not None and st.st_size != size) or (
                mtime_ns is not None and st.st_mtime_ns != mtime_ns
            ):
                return
            box["result"] = hash_file(
                path, _ident(st), cache=_HashCache(), budget=budget, deadline=deadline, fingerprint=False
            )
        except Exception:  # noqa: BLE001 -- a hash failure costs the reference its hash
            pass

    worker = threading.Thread(target=work, name="probe-reference-hash", daemon=True)
    worker.start()
    worker.join(max(deadline - time.monotonic(), 0.0))
    result = box.get("result")
    sha = result[0] if isinstance(result, tuple) else None
    return sha if isinstance(sha, str) and _HEX64.fullmatch(sha) else None
from probe.sdk.capture.lineage.exclusions import HASH_LEVEL_MIN_BYTES  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.lineage import _give_back, _take  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.rows import _HEX64  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.spool.spool import _ident, _local, _stat_is_file, internal, state_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
