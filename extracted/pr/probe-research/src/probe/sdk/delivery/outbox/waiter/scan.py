"""The waiter's views of one run across every queue of the outbox: the workers' progress
records (each poll) and one full count of the folders (before it says "delivered", R10)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from probe.sdk.delivery.outbox.progress import QueueTally, load_progress
from probe.sdk.delivery.status_fields import StatusField


@dataclass
class RunView:
    """One run summed over the outbox's queues."""

    pending: int = 0
    pending_bytes: int = 0
    held: int = 0
    failed: int = 0
    discarded: int = 0
    #: Writes the server refused for good, dead letters or in discarded/ (counted from the folders only).
    set_aside: int = 0
    #: Best-effort writes still in line: waited for, never a reason to raise.
    best_effort: int = 0
    delivered_total: int = 0
    last_progress_at: float | None = None
    unreachable_since: float | None = None
    retry_after_until: float | None = None
    error_kinds: set = field(default_factory=set)
    last_error: str | None = None
    #: Writes of other runs the workers send before this run's ("N writes ahead of yours").
    ahead: int = 0
    #: Queue dir -> the record's worker pid, and whether that worker said it exited.
    workers: dict = field(default_factory=dict)
    #: When the newest record was written (epoch seconds), None with no record.
    updated_at: float | None = None
    #: I15d: the server holds the run's close until its queued data is stored: the points it
    #: last said were pending, and when (epoch seconds).
    server_pending_points: int | None = None
    server_storing_at: float | None = None


def worker_queues(journal: Any) -> list:
    """Every queue of ``journal``'s outbox that has a worker of its own: the root and each
    credential queue (a receipt namespace rides its parent's worker)."""
    from probe.sdk.delivery.journal.journal import Journal

    root = Journal(journal.outbox_root, context=journal.context, attribution=journal.attribution)
    return [queue for queue in root.namespaces() if not queue.receipt_enabled]


def read_records(queues: list, run_ref: str) -> RunView:
    """This run as the workers' progress records last said (nothing else is read)."""
    view = RunView()
    for queue in queues:
        record = load_progress(queue.dir)
        if record is None:
            continue
        view.workers[str(queue.dir)] = (record.pid, record.exited)
        view.updated_at = _latest(view.updated_at, record.updated_at)
        run = record.run(run_ref)
        if run is None:
            continue
        view.pending += run.pending
        view.pending_bytes += run.pending_bytes
        view.held += run.held
        view.failed += run.failed
        view.discarded += run.discarded
        view.best_effort += run.best_effort
        view.delivered_total += run.delivered_total
        view.last_progress_at = _latest(view.last_progress_at, run.last_progress_at)
        if run.pending and run.unreachable_since is not None:
            view.unreachable_since = _earliest(view.unreachable_since, run.unreachable_since)
        view.retry_after_until = _latest(view.retry_after_until, run.retry_after_until)
        if run.last_error_kind:
            view.error_kinds.add(run.last_error_kind)
            view.last_error = run.last_error or view.last_error
        view.ahead += _writes_ahead(record, run_ref, run.pending)
        if run.server_storing_at is not None and (view.server_storing_at or 0.0) < run.server_storing_at:
            view.server_storing_at, view.server_pending_points = run.server_storing_at, run.server_pending_points
    return view


def count_run(
    queues: list, run_ref: str, tallies: dict | None = None, *, min_epoch: int | None = None
) -> RunView:
    """This run counted from the folders themselves: the one full check (R10). Each queue under
    its append lock, the lock `outbox/held` moves writes under, so a write let out of held/
    between two listings is never read as gone. ``tallies``: kept across counts (each file parsed
    once). ``min_epoch``: leave out an older attempt's writes (the server refuses them)."""
    from probe.foundation.durable.durable import file_lock

    view = RunView()
    tallies = {} if tallies is None else tallies
    for queue in queues:
        tally = tallies.setdefault(str(queue.dir), QueueTally(queue))
        with file_lock(queue.append_lock):
            counts, _ = tally.count({run_ref: min_epoch} if min_epoch is not None else None)
        run = counts.get(run_ref)
        if run is None:
            continue
        view.pending += run.pending
        view.pending_bytes += run.pending_bytes
        view.held += run.held
        view.failed += run.failed
        view.discarded += run.discarded
        view.set_aside += run.set_aside
        view.best_effort += run.best_effort
    return view


def queues_holding(queues: list, run_ref: str, *, min_epoch: int | None = None) -> list:
    """The queues with writes of this run still to send (a full count, at the start)."""
    holding = []
    for queue in queues:
        counts, _ = QueueTally(queue).count({run_ref: min_epoch} if min_epoch is not None else None)
        run = counts.get(run_ref)
        if run is not None and (run.pending or run.best_effort):
            holding.append(queue)
    return holding


def _writes_ahead(record: Any, run_ref: str, mine: int) -> int:
    if run_ref in record.priority:
        before = record.priority[: record.priority.index(run_ref)]
        return sum((record.run(ref).pending if record.run(ref) else 0) for ref in before)
    return max(0, record.queue_pending - mine)


def _latest(a: float | None, b: float | None) -> float | None:
    return b if a is None else a if b is None else max(a, b)


def _earliest(a: float | None, b: float | None) -> float | None:
    return b if a is None else a if b is None else min(a, b)


#: The server's bound on every age it takes in a beat body (10 years, in seconds).
_AGE_CAP_SECONDS = 315_360_000.0
#: When a run shows several error kinds, the one a person must act on first names it.
_KIND_ORDER = ("login_refused", "refused", "stalled", "unreachable", "transient", "held_elsewhere")


def delivery_summary(journal: Any, run_ref: str) -> dict | None:
    """The beat's ``delivery`` body (R13): this run's backlog as the workers' records last said,
    or None when no worker of this release has a record here. Ages are seconds, finite, capped."""
    import math
    import time

    queues = worker_queues(journal)
    view = read_records(queues, run_ref)
    if not view.workers:
        return None
    now = time.time()
    kinds = [kind for kind in _KIND_ORDER if kind in view.error_kinds]
    body: dict = {
        "pending": view.pending,
        "pending_bytes": view.pending_bytes,
        "held": view.held,
        "failed": view.failed,
        "worker_alive": any(queue.worker_alive() for queue in queues),
        "last_error_kind": kinds[0] if kinds else None,
    }
    oldest = _oldest_pending_at(queues) if view.pending else None
    for key, since in (("oldest_pending_age_s", oldest), ("last_progress_age_s", view.last_progress_at)):
        if since is not None and math.isfinite(now - since):
            body[key] = round(min(max(now - since, 0.0), _AGE_CAP_SECONDS), 3)
    return body


def _oldest_pending_at(queues: list) -> float | None:
    """Epoch seconds of the oldest write still queued in these queues (status.json's banner)."""
    from datetime import datetime

    from probe.sdk.delivery.journal.journal import Journal

    stamps = []
    for queue in queues:
        status = Journal.read_status(queue.dir, include_receipts=False, credential_queues=False) or {}
        try:
            stamps.append(datetime.fromisoformat(str(status[StatusField.OLDEST_PENDING])).timestamp())
        except (KeyError, TypeError, ValueError):
            continue
    return min(stamps) if stamps else None
