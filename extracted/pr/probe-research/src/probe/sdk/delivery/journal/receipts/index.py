"""the sqlite receipt index: commit receipt identities in one transaction and compact it in bounded batches."""

from __future__ import annotations

from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import time

from probe.foundation.durable.durable import fsync_directory
RECEIPT_INDEX_VERSION = 1
RECEIPT_COMPACTION_BATCH = 256


class ReceiptIndexMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    @staticmethod
    def _commit_receipt_index(conn) -> None:
        """The terminal durability boundary; operation removal happens later."""
        conn.commit()

    def _index_receipts(self, receipts: list[dict], *, timeout: float = 5.0) -> None:
        """Commit immutable identities in one indexed, FULL-synchronous transaction."""
        self._receipt_dirs()
        # Reserve a private inode before sqlite opens it (its default mode is 644).
        descriptor = os.open(self.receipt_index, os.O_CREAT | os.O_RDWR, 0o600)
        os.close(descriptor)
        with closing(sqlite3.connect(self.receipt_index, timeout=timeout)) as conn, conn:
            conn.execute("PRAGMA synchronous=FULL")
            conn.execute("BEGIN IMMEDIATE")
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, RECEIPT_INDEX_VERSION):
                raise ValueError("unsupported terminal receipt index version")
            conn.execute("CREATE TABLE IF NOT EXISTS receipts (key TEXT PRIMARY KEY, "
                         "payload TEXT NOT NULL, cleanup INTEGER NOT NULL DEFAULT 1) WITHOUT ROWID")
            conn.execute("CREATE INDEX IF NOT EXISTS receipt_cleanup ON receipts(cleanup) WHERE cleanup=1")
            conn.execute(f"PRAGMA user_version={RECEIPT_INDEX_VERSION}")
            for receipt in receipts:
                if (receipt.get("schema") != DELIVERY_SCHEMA or receipt.get("state") != "delivered"
                        or receipt.get("status") != "complete" or not receipt.get("artifact_id")
                        or not receipt.get("request_digest")):
                    raise ValueError("cannot compact an unverified terminal receipt")
                key = self._correlation_key(receipt["correlation"])
                payload = json.dumps(receipt, separators=(",", ":"), sort_keys=True)
                previous = conn.execute("SELECT payload FROM receipts WHERE key=?", (key,)).fetchone()
                if previous and json.loads(previous[0]) != receipt:
                    raise ValueError("terminal receipt identity is immutable")
                conn.execute("INSERT OR IGNORE INTO receipts(key,payload) VALUES (?,?)", (key, payload))
                conn.execute("UPDATE receipts SET cleanup=1 WHERE key=?", (key,))
            self._commit_receipt_index(conn)
        fsync_directory(self.dir)

    def compact_receipts(self, *, max_records: int = RECEIPT_COMPACTION_BATCH,
                         max_seconds: float = 1.0) -> dict:
        """Bounded explicit checkpoint; preserves all terminal identities forever. Imports legacy
        JSON into the index before deleting any copy. Cleanup is indexed, so a crash after the
        index commit or JSON unlink resumes without scanning historical identities. Does not
        VACUUM or erase receipts. One filesystem operation/SQLite commit may overrun the time
        budget; lock waits are nonblocking and DB admission uses that budget.
        """
        if not self.receipt_enabled:
            return self.for_receipts(self.dir).compact_receipts(max_records=max_records, max_seconds=max_seconds)
        if not 1 <= max_records <= 4096 or not 0 < max_seconds <= 10:
            raise ValueError("receipt compaction requires 1..4096 records and 0 < seconds <= 10")
        deadline = time.monotonic() + max_seconds
        report = {"indexed": 0, "json_removed": 0, "locks_removed": 0,
                  "compacted": 0, "deferred": 0, "remaining": False}
        receipts = []
        if self.receipts_dir.exists():
            with os.scandir(self.receipts_dir) as entries:
                for entry in entries:
                    if len(receipts) >= max_records or time.monotonic() >= deadline:
                        break
                    if entry.name.endswith(".json") and entry.is_file(follow_symlinks=False):
                        receipt = self._read_record(Path(entry.path))
                        if receipt is not None:
                            if entry.name != self._correlation_key(receipt["correlation"]) + ".json":
                                raise ValueError("legacy receipt name differs from correlation")
                            receipts.append(receipt)
        if receipts:
            self._index_receipts(receipts, timeout=max(0.001, deadline - time.monotonic()))
            report["indexed"] = len(receipts)
        if not self.receipt_index.exists():
            return report
        with closing(sqlite3.connect(self.receipt_index, timeout=max(0.001, deadline - time.monotonic()))) as conn:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version == 0 and not conn.execute("SELECT 1 FROM sqlite_master LIMIT 1").fetchone():
                return report
            if version != RECEIPT_INDEX_VERSION:
                raise ValueError("unsupported terminal receipt index version")
            keys = conn.execute("SELECT key FROM receipts WHERE cleanup=1 LIMIT ?", (max_records,)).fetchall()
            cleaned = []
            for (key,) in keys:
                if time.monotonic() >= deadline:
                    break
                try:
                    with self._correlation_lock(key, blocking=False):
                        for directory, suffix, field in (
                            (self.receipts_dir, ".json", "json_removed"),
                            (self.dir / "correlations", ".lock", "locks_removed"),
                        ):
                            path = directory / f"{key}{suffix}"
                            if path.exists():
                                path.unlink()
                                fsync_directory(directory)
                                report[field] += 1
                        cleaned.append((key,))
                except BlockingIOError:
                    report["deferred"] += 1
            if cleaned:
                conn.executemany("UPDATE receipts SET cleanup=0 WHERE key=?", cleaned)
                conn.commit()
            report["compacted"] = len(cleaned)
            report["remaining"] = bool(conn.execute("SELECT 1 FROM receipts WHERE cleanup=1 LIMIT 1").fetchone())
        if self.receipts_dir.exists():
            with os.scandir(self.receipts_dir) as entries:
                report["remaining"] |= next(entries, None) is not None
        return report
from probe.sdk.delivery.ops.ops import DELIVERY_SCHEMA  # noqa: E402 -- pieces need each other; the front door loads this one first
