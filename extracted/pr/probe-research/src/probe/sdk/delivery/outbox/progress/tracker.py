"""ProgressTracker: the worker's per-run memory across passes. Folds each pass's report in,
runs the stall clock (R12), and publishes `progress.json` for a waiting `finish()` (R1)."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from probe.sdk.delivery.outbox.progress.progress import (
    DeliveryErrorKind,
    ProgressRecord,
    RunProgress,
    current_pid,
    load_progress,
    save_progress,
    worker_version,
)
from probe.sdk.delivery.outbox.progress.tally import QueueTally

#: A run whose head write keeps failing with no progress this long is stalled: its stuck write
#: is set aside so the rest of the run lands (T1: 4x the p99 drain of 72.6 s, under the median
#: stalled episode of 1,455 s).
STALL_LIMIT_SECONDS = 300.0
#: The record is rewritten at most this often between passes (a waiter polls about as often).
_PUBLISH_EVERY_SECONDS = 0.5
#: A run with nothing left and no waiter leaves the record this long after it last moved.
_FORGET_AFTER_SECONDS = 600.0
#: The most runs a record keeps: the waited-on ones first, then the deepest backlogs.
MAX_RUNS = 256
_ERROR_CHARS = 300
#: A report the server did not take is tried again after this, doubling, up to the cap (D5).
_REPORT_RETRY_SECONDS, _REPORT_RETRY_CAP_SECONDS = 60.0, 3600.0
#: Causes that last while their writes do (held, refused): later progress does not clear them.
_LASTING_KINDS = frozenset({DeliveryErrorKind.REFUSED, DeliveryErrorKind.STALLED})


@dataclass(frozen=True)
class StalledHead:
    """A run's stuck head write, due to be set aside (R12)."""

    run_ref: str | None
    path: Path
    error: str | None
    #: Its lane in the worker's backoff, retried at once once the write is aside.
    lane: Any = None


class ProgressTracker:
    """Per-run state of one worker's queues (the root's, or one credential queue's)."""

    def __init__(self, journal: Any, *, clock: Callable[[], float] = time.time) -> None:
        self.journal = journal
        self.clock = clock
        self.tally = QueueTally(journal)
        previous = load_progress(journal.dir)
        #: Carried from the last worker: totals and what was already reported.
        self.runs: dict[str | None, RunProgress] = {}
        if previous is not None:
            for ref, progress in previous.runs.items():
                self.runs[ref] = RunProgress(
                    delivered_total=progress.delivered_total,
                    last_progress_at=progress.last_progress_at,
                    reported=list(progress.reported),
                )
        self.unreachable_since: float | None = None
        self.priority: list[str] = []
        #: run_ref -> (its failing head's file, its lane).
        self._failing_paths: dict[str | None, tuple[Path, Any]] = {}
        self._published_at = float("-inf")
        #: (run_ref, cause) -> first error, for reports not yet taken by the server (D5).
        self._unsent: dict[tuple[str, str], str | None] = {}
        self._report_retry: dict[tuple[str, str], tuple[float, float]] = {}

    # -- one pass ---------------------------------------------------------------------------
    def record(self, report: Any, *, priority: list[str] | None = None) -> None:
        """Fold one pass's `DrainReport` in."""
        now = self.clock()
        self.priority = list(priority or ())
        if getattr(report, "unreachable", False):
            self.unreachable_since = self.unreachable_since or now
            # An outage is not a poison write: nothing was tried, so no stall clock runs on.
            for run in self.runs.values():
                run.failing_since = None
            self._failing_paths.clear()
        elif report.delivered or report.dead_lettered or getattr(report, "in_progress", 0):
            self.unreachable_since = None
        for ref, count in getattr(report, "delivered_by_run", {}).items():
            self._run(ref).delivered_total += int(count)
        for ref in getattr(report, "progressed_refs", set()):
            run = self._run(ref)
            run.last_progress_at = now
            run.failing_since = None
            self._failing_paths.pop(ref, None)
            if run.last_error_kind not in _LASTING_KINDS:
                run.last_error_kind = run.last_error = None
        lane_refs = getattr(report, "lane_refs", {})
        for lane, stall in report.stalled_runs.items():
            ref = lane_refs.get(lane, lane if isinstance(lane, str) else None)
            self._note_stall(ref, lane, stall, now, report)
        for record in report.dead_letter_records:
            ref = record.get("run_ref") if isinstance(record.get("run_ref"), str) else None
            run = self._run(ref)
            run.last_error_kind = DeliveryErrorKind.REFUSED
            run.last_error = str(record.get("error") or "")[:_ERROR_CHARS]

    def _note_stall(self, ref: str | None, lane: Any, stall: Any, now: float, report: Any) -> None:
        run = self._run(ref)
        run.last_error = str(stall.error or "")[:_ERROR_CHARS] or None
        run.last_error_kind = _kind_of(stall)
        if stall.retry_after:
            run.retry_after_until = now + float(stall.retry_after)
        if getattr(stall, "failing", False) and ref not in getattr(report, "progressed_refs", ()):
            # R11: a Retry-After sets the timing only; the clock runs on regardless.
            run.failing_since = run.failing_since or now
            if getattr(stall, "path", None) is not None:
                self._failing_paths[ref] = (Path(stall.path), lane)

    def _run(self, ref: str | None) -> RunProgress:
        return self.runs.setdefault(ref, RunProgress())

    # -- the stall rule (R12) ---------------------------------------------------------------
    def due_stalls(self) -> list[StalledHead]:
        """Runs whose head kept failing with no progress for `STALL_LIMIT_SECONDS`: their stuck
        write, to set aside. A write in a receipt queue (an import's) is never set aside: its
        importer owns the retry (`flush(on_error=...)`)."""
        now = self.clock()
        due = []
        for ref, run in self.runs.items():
            failing = self._failing_paths.get(ref)
            if run.failing_since is None or failing is None:
                continue
            path, lane = failing
            if now - run.failing_since < STALL_LIMIT_SECONDS:
                continue
            if path.parent.parent.name == "delivery-v1" or not path.exists():
                continue
            due.append(StalledHead(ref, path, run.last_error, lane))
        return due

    def note_set_aside(self, head: StalledHead) -> None:
        """Its stuck write went to held/: the clock starts over for what comes after it."""
        run = self._run(head.run_ref)
        run.failing_since = None
        run.last_error_kind = DeliveryErrorKind.STALLED
        self._failing_paths.pop(head.run_ref, None)

    def seconds_to_next_stall(self) -> float | None:
        """How long until the soonest running stall clock runs out, so the worker looks then."""
        now = self.clock()
        left = [
            STALL_LIMIT_SECONDS - (now - run.failing_since)
            for ref, run in self.runs.items()
            if run.failing_since is not None and ref in self._failing_paths
        ]
        return max(0.05, min(left)) if left else None

    # -- reports to the server (D5) ----------------------------------------------------------
    def queue_report(self, ref: str | None, cause: str, error: str | None) -> None:
        """Owe the server one report of ``cause`` for ``ref``, unless it already took one."""
        if ref is None or cause in self._run(ref).reported:
            return
        self._unsent.setdefault((ref, str(cause)), error)

    def due_reports(self) -> list[tuple[str, str, str | None]]:
        """Owed reports whose retry time has come: (run_ref, cause, first error)."""
        now = time.monotonic()
        return [
            (ref, cause, error)
            for (ref, cause), error in self._unsent.items()
            if self._report_retry.get((ref, cause), (0.0, 0.0))[0] <= now
        ]

    def note_report_result(self, ref: str, cause: str, *, taken: bool, final: bool = False) -> None:
        """``taken``: the server took it, or cannot (an older one): sent for good, kept in the
        record across workers. ``final``: no retry would help (a refused credential refuses the
        report too). Otherwise tried again later, waiting longer each time."""
        key = (ref, str(cause))
        if taken or final:
            self._unsent.pop(key, None)
            self._report_retry.pop(key, None)
            if str(cause) not in self._run(ref).reported:
                self._run(ref).reported.append(str(cause))
            return
        _, wait = self._report_retry.get(key, (0.0, _REPORT_RETRY_SECONDS / 2))
        wait = min(wait * 2, _REPORT_RETRY_CAP_SECONDS)
        self._report_retry[key] = (time.monotonic() + wait, wait)

    # -- the record -------------------------------------------------------------------------
    def publish(self, *, force: bool = False, exiting: bool = False) -> ProgressRecord | None:
        """Count the queues and write the record, at most every `_PUBLISH_EVERY_SECONDS` unless
        ``force``. ``exiting``: the worker's last word (a clean exit). Never raises."""
        monotonic = time.monotonic()
        if not (force or exiting) and monotonic - self._published_at < _PUBLISH_EVERY_SECONDS:
            return None
        self._published_at = monotonic
        try:
            return self._publish(exiting=exiting)
        except Exception:  # noqa: BLE001 -- a waiter falls back to scanning the queue
            return None

    def _publish(self, *, exiting: bool = False) -> ProgressRecord:
        now = self.clock()
        counts, queued = self.tally.count()
        for ref, count in counts.items():
            run = self._run(ref)
            run.pending, run.pending_bytes = count.pending, count.pending_bytes
            run.held, run.failed, run.discarded = count.held, count.failed, count.discarded
            run.best_effort = count.best_effort
        for ref, run in self.runs.items():
            if ref not in counts:
                run.pending = run.pending_bytes = run.held = run.failed = run.discarded = 0
                run.best_effort = 0
            if not run.pending:
                run.failing_since = None
                self._failing_paths.pop(ref, None)
            if (run.last_error_kind == DeliveryErrorKind.STALLED and not run.held) or (
                run.last_error_kind == DeliveryErrorKind.REFUSED and not run.failed
            ):
                run.last_error_kind = run.last_error = None
            run.unreachable_since = self.unreachable_since if run.pending else None
        self._forget_idle(now)
        record = ProgressRecord(
            pid=current_pid(),
            version=worker_version(),
            updated_at=now,
            unreachable_since=self.unreachable_since,
            paused=bool(getattr(self.journal, "paused", False)),
            priority=self.priority,
            runs={ref: run for ref, run in self.runs.items() if ref is not None},
            queue_pending=queued,
            exited=exiting,
        )
        save_progress(self.journal.dir, record)
        return record

    def _forget_idle(self, now: float) -> None:
        """Keep the record bounded: runs with writes left or a waiter, then recent movers."""
        waited = set(self.priority)

        owed = {ref for ref, _cause in self._unsent}

        def is_live(ref: str | None, run: RunProgress) -> bool:
            if ref in waited or ref in owed or run.pending or run.held or run.failed or run.best_effort:
                return True
            return run.last_progress_at is not None and now - run.last_progress_at < _FORGET_AFTER_SECONDS

        for ref in [ref for ref, run in self.runs.items() if not is_live(ref, run)]:
            del self.runs[ref]
        if len(self.runs) > MAX_RUNS:
            ranked = sorted(
                self.runs, key=lambda ref: (ref not in waited, -(self.runs[ref].pending or 0))
            )
            for ref in ranked[MAX_RUNS:]:
                del self.runs[ref]

    def context_of(self, ref: str | None) -> dict | None:
        """The pinned context of the run's writes (which server, which credential)."""
        return self.tally.contexts.get(ref) if ref is not None else None


def _kind_of(stall: Any) -> str | None:
    """A lane stall as a `DeliveryErrorKind` (None: waiting on the server, not an error)."""
    status = getattr(stall, "status", None)
    if getattr(stall, "held", False):
        return DeliveryErrorKind.HELD_ELSEWHERE
    if status in (401, 403):
        return DeliveryErrorKind.LOGIN_REFUSED
    if getattr(stall, "failing", False):
        return DeliveryErrorKind.TRANSIENT
    return None
