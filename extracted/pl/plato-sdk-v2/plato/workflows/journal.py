"""Append-only JSONL journal for workflow resume.

Every ``agent()`` call is journaled to ``<journal_dir>/<workflow_id>/journal.jsonl``
in the world's dedicated ``journal`` workspace (tracked, but NEVER agent-mounted).
Records carry a monotonically increasing ``seq``. Resume replays cache hits keyed on
``sha256(prompt + opts)`` with FIFO occurrence-claim semantics:

* ``load()`` rebuilds the replay pool from the on-disk journal. A truncated
  final line (interrupted append) is tolerated: it is dropped AND the file is
  truncated back to the end of the last parseable line, so the next ``append()``
  starts a fresh line instead of merging into the partial one (a merged line
  would be skipped as corruption on every later load). Returns how many ``ok``
  results are replayable.
* ``claim_replay(key)`` pops the OLDEST unclaimed ``ok`` result for a key, so
  identical ``(prompt, opts)`` calls are interchangeable. Failed/timeout/
  invalid_output records are never replayed; ``call_started`` orphans re-run.
* Cache hits are re-journaled as ``call_result{status:"ok", cached_from, cost_usd:0}``
  as audit/event records. They are EXCLUDED from the replay pool — the original
  ``ok`` record in the same append-only file is the single claimable source, so
  a later occurrence of a key can never claim a duplicate of an earlier
  occurrence's result (chained resumes stay self-consistent).

Durability: appends take an ``asyncio.Lock`` and ``flush() + os.fsync()`` before
returning, so a journal record on disk implies the corresponding work is durable.
"""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel

logger = logging.getLogger(__name__)

__all__ = ["JournalRecord", "Journal"]

RecordType = Literal[
    "workflow_started",
    "call_started",
    "call_result",
    "phase",
    "workflow_result",
]


class JournalRecord(BaseModel):
    seq: int
    type: RecordType
    ts: float
    key: str | None = None
    occurrence: int | None = None
    call_id: str | None = None
    status: str | None = None
    result: Any | None = None
    published_ref: str | None = None
    # Hidden ref where a failed call's git state was salvaged (see backend).
    salvage_ref: str | None = None
    merged: bool | None = None
    attempts: int | None = None
    cost_usd: float | None = None
    phase: str | None = None
    label: str | None = None
    cached_from: str | None = None
    error: str | None = None
    # script_sha256 / args_sha256 / workflow result payload, etc.
    payload: dict[str, Any] | None = None


class Journal:
    """Append-only JSONL journal with FIFO replay-claim resume semantics."""

    def __init__(self, journal_dir: Path, workflow_id: str) -> None:
        self._path = Path(journal_dir) / workflow_id / "journal.jsonl"
        self._journal_dir = Path(journal_dir)
        self._workflow_id = workflow_id
        self._lock = asyncio.Lock()
        self._next_seq = 0
        # Monotonic append/checkpoint counters: `dirty` compares them, and
        # mark_checkpointed(upto=) clears only what a checkpoint actually
        # covered — a bare boolean lost records appended DURING a checkpoint.
        self._append_count = 0
        self._checkpointed_count = 0
        # key -> FIFO list of replayable ``ok`` call_result records (file order).
        self._replay: dict[str, list[JournalRecord]] = {}

    @property
    def workflow_id(self) -> str:
        """The workflow this journal belongs to (namespaces call artifacts)."""
        return self._workflow_id

    @property
    def path(self) -> Path:
        """Path of the on-disk ``journal.jsonl`` (may not exist yet)."""
        return self._path

    # -- resume ------------------------------------------------------------

    def load(self) -> int:
        """Rebuild replay state from the on-disk journal.

        Tolerates a truncated final line (an append interrupted before its
        ``flush()+fsync()`` completed): the partial line is dropped and the file
        is truncated back to the end of the last parseable line so the next
        ``append()`` starts a fresh line instead of writing onto the partial one.
        ``cached_from`` re-journal records are audit-only and excluded from the
        replay pool (the original ``ok`` record is the claimable source).
        Returns the number of replayable ``ok`` ``call_result`` records. A
        freshly-loaded journal is NOT dirty — its records were already
        checkpointed into the restored workspace.
        """
        self._replay = {}
        self._next_seq = 0
        self._append_count = 0
        self._checkpointed_count = 0

        if not self._path.exists():
            return 0

        data = self._path.read_bytes()
        if not data:
            return 0

        lines = data.split(b"\n")
        terminated = lines[-1] == b""  # the file ends with a newline
        if terminated:
            lines.pop()

        max_seq = -1
        replayable = 0
        offset = 0
        good_end = 0  # byte offset just past the last parseable (or blank) line
        last_idx = len(lines) - 1
        for idx, raw_line in enumerate(lines):
            has_newline = idx != last_idx or terminated
            line_end = offset + len(raw_line) + (1 if has_newline else 0)
            offset = line_end

            if not raw_line.strip():
                if has_newline:
                    good_end = line_end  # harmless blank padding
                continue
            if not has_newline:
                # No trailing newline: this append never completed its
                # write+fsync, so the record is not durable — drop it (and
                # truncate it below so the next append starts a fresh line).
                logger.warning("Dropping truncated final journal line in %s", self._path)
                continue
            try:
                record = JournalRecord.model_validate_json(raw_line)
            except ValueError:
                # A parse failure on the LAST line is an interrupted write —
                # tolerate it. Anywhere else it is real corruption; skip loudly.
                if idx == last_idx:
                    logger.warning("Dropping truncated final journal line in %s", self._path)
                else:
                    logger.warning("Skipping unparseable journal line %d in %s", idx, self._path)
                continue

            good_end = line_end
            if record.seq > max_seq:
                max_seq = record.seq

            if (
                record.type == "call_result"
                and record.status == "ok"
                and record.key is not None
                and record.cached_from is None
            ):
                self._replay.setdefault(record.key, []).append(record)
                replayable += 1

        if good_end < len(data):
            # Unparseable tail (truncated final append or trailing corruption):
            # cut it so the next append cannot merge into it — a merged line
            # would be silently skipped as corruption on every later load.
            try:
                os.truncate(self._path, good_end)
            except OSError:
                logger.warning("Failed to truncate corrupt journal tail in %s", self._path, exc_info=True)

        self._next_seq = max_seq + 1
        return replayable

    def claim_replay(self, key: str) -> JournalRecord | None:
        """Pop the oldest unclaimed ``ok`` result for ``key`` (FIFO), or None."""
        pool = self._replay.get(key)
        if not pool:
            return None
        return pool.pop(0)

    # -- append ------------------------------------------------------------

    def next_seq(self) -> int:
        """Return the next sequence number and advance the counter."""
        seq = self._next_seq
        self._next_seq += 1
        return seq

    async def append(self, record: JournalRecord) -> None:
        """Append a record durably (lock + open + write + fsync + close).

        The file is reopened for every append ON PURPOSE. The journal lives on
        a tracked workspace directory, which is a FUSE overlay: a long-lived
        ``O_APPEND`` handle there writes at a cached offset that goes stale
        when the workspace commit machinery touches the file between writes —
        observed on live VMs as a NUL-filled hole in the read view exactly one
        record long. Reopening per append re-resolves the current file state
        through the overlay; the append rate (dozens per workflow) makes the
        open/close cost irrelevant.
        """
        line = record.model_dump_json() + "\n"
        async with self._lock:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._path, "a", encoding="utf-8") as fh:
                fh.write(line)
                fh.flush()
                os.fsync(fh.fileno())
            self._append_count += 1

    # -- checkpoint bookkeeping -------------------------------------------

    @property
    def dirty(self) -> bool:
        """True when records were appended since the last covered checkpoint."""
        return self._append_count > self._checkpointed_count

    @property
    def append_count(self) -> int:
        """Monotonic count of appends — snapshot BEFORE a checkpoint and pass to
        :meth:`mark_checkpointed` so records appended DURING the checkpoint keep
        their dirty status (a bare boolean clear silently dropped them from the
        next periodic commit, widening the crash-loss window)."""
        return self._append_count

    def mark_checkpointed(self, upto: int | None = None) -> None:
        """Record that appends up to ``upto`` (default: all current) are durable."""
        self._checkpointed_count = self._append_count if upto is None else upto

    def close(self) -> None:
        """No-op: appends open/close per record (see ``append``). Kept for callers."""
