"""The SDK local spool for fail-open writes: a data write must never block or crash
the training loop (ingestion doc). On failure with fail-open we append the raw request
to an on-disk JSONL queue; `flush` replays it in order (at `run end` or `probe flush`).
Deliberately dumb: append-only, replay-in-order, stop-on-first-failure. A safety net,
not a high-throughput buffer.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from ...foundation.durable.durable import file_lock, fsync_directory, write_text_atomic
from ...foundation.durable import homedir


def default_dir() -> Path:
    configured = os.environ.get("PROBE_SPOOL_DIR")
    if configured:
        return Path(configured).expanduser()
    base = os.environ.get("XDG_STATE_HOME")
    root = Path(base) if base else homedir.home() / ".local" / "state"
    return root / "probe" / "spool"


@dataclass
class SpoolRecord:
    method: str
    path: str
    json_body: dict | None


class Spool:
    def __init__(self, directory: Path | None = None):
        self.dir = directory or default_dir()
        self.file = self.dir / "pending.jsonl"
        self.inflight_file = self.dir / "inflight.jsonl"
        self.lock_file = self.dir / ".pending.lock"
        self.flush_lock_file = self.dir / ".flush.lock"

    def _locked(self):
        return file_lock(self.lock_file)

    def _flush_locked(self):
        return file_lock(self.flush_lock_file)

    def append(self, method: str, path: str, json_body: dict | None) -> None:
        line = json.dumps({"method": method, "path": path, "json": json_body})
        with self._locked():
            created = not self.file.exists()
            with self.file.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            if created:
                fsync_directory(self.dir)

    def pending(self) -> list[SpoolRecord]:
        with self._locked():
            # inflight is immutable during replay. Count it so a diagnostic never reads an
            # empty queue while flush is active (or the process died after pending->inflight).
            return self._read_records(self.inflight_file) + self._read_records(self.file)

    @staticmethod
    def _read_records(path: Path) -> list[SpoolRecord]:
        if not path.exists():
            return []
        out: list[SpoolRecord] = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            out.append(SpoolRecord(rec["method"], rec["path"], rec.get("json")))
        return out

    def _write_records_atomic(self, records: list[SpoolRecord]) -> None:
        text = "".join(
            json.dumps(
                {"method": record.method, "path": record.path, "json": record.json_body}
            )
            + "\n"
            for record in records
        )
        write_text_atomic(self.file, text)

    def flush(self, transport) -> int:
        """Replay pending records in order; returns the count sent. Stops at the first
        failure and rewrites the queue with the remainder (no reorder, no drop)."""
        # Serialize flushers, but never hold the append lock over network I/O:
        # a failing training-loop write must still enqueue during a slow replay.
        with self._flush_locked():
            with self._locked():
                # At-least-once crash recovery: a process may die after moving the queue
                # out of append's way; prepend that immutable batch on restart.
                recovered = self._read_records(self.inflight_file)
                queued = self._read_records(self.file)
                if recovered:
                    self._write_records_atomic(recovered + queued)
                    self.inflight_file.unlink(missing_ok=True)
                    fsync_directory(self.dir)
                if not self.file.exists():
                    return 0
                os.replace(self.file, self.inflight_file)
                fsync_directory(self.dir)
                records = self._read_records(self.inflight_file)

            sent = 0
            remaining: list[SpoolRecord] = []
            failed = False
            for rec in records:
                if failed:
                    remaining.append(rec)
                    continue
                try:
                    transport.request(rec.method, rec.path, json_body=rec.json_body)
                    sent += 1
                except Exception:  # noqa: BLE001 - keep the rest queued on any failure
                    failed = True
                    remaining.append(rec)
            with self._locked():
                # Appends made during replay are newer than the inflight batch: the
                # failed remainder stays in front.
                appended = self._read_records(self.file)
                combined = remaining + appended
                if combined:
                    self._write_records_atomic(combined)
                else:
                    self.file.unlink(missing_ok=True)
                self.inflight_file.unlink(missing_ok=True)
                fsync_directory(self.dir)
            return sent
