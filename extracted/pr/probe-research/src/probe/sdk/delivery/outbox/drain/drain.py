"""Drain: one drain pass over a queue and its namespaces, FIFO within each run, settling each op."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TYPE_CHECKING

from .....foundation.os_backend import os_backend as oscompat
from .....foundation.compose.compose import fold_parts
from .....foundation.durable.durable import (
    file_lock,
    now_iso)
from probe.sdk.delivery.status_fields import StatusField


def drain(
    journal: Journal,
    *,
    run_ref: str | None = None,
    client_factory: Callable[[dict | None], Any] | None = None,
    wait_for_lock: bool = True,
    lock_timeout: float | None = None,
    promote_timeout: float | None = None,
    on_error: Callable[[Exception], None] | None = None,
    on_delivered: Callable[[str | None], None] | None = None,
    skip_runs: "set | frozenset | None" = None,
    credential_queues: bool = True,
    long_ops: bool = True,
    only_ops: "set | frozenset | None" = None,
    window: "CollectWindow | None" = None,
    priority_runs: "set | frozenset | None" = None,
    set_best_effort_aside: bool = False,
    senders: "SenderClients | None" = None,
    _include_receipts: bool = True,
) -> DrainReport:
    """Deliver queued ops, FIFO within each run and runs round-robin (plan 1.6); one pass per
    namespace. Foreground and background drains share it; the worker wraps it in backoff.

    ``run_ref``: a run's barrier, only its ops (no multipart). ``only_ops``: those op ids only.
    ``skip_runs``: runs the caller is backing off. ``lock_timeout`` / ``promote_timeout``: bounded
    waits (None: ``wait_for_lock`` decides / no bound). ``long_ops=False``: no multipart slice.
    ``window`` (a drainer's `CollectWindow`, plan T2): hold a run's telemetry until its
    `send_after`; other callers pass none and send what is queued now.
    ``priority_runs``: runs a `finish()` is waiting on (R2): their lanes go first.
    ``set_best_effort_aside``: the worker's passes only (it lets held writes out again): a failing
    best-effort write leaves its run's line at once instead of holding it (`outbox/held`).
    ``senders``: the worker's `SenderClients`, kept across passes (I13); without one a pass builds
    its own and closes them at its end. ``client_factory``: tests. ``on_error`` may raise to keep
    the op as it was; ``on_delivered`` runs after a delivery is durable and cannot fail it.
    DESIGN.md has the full contract."""
    if _include_receipts and not journal.receipt_enabled:
        namespaces = journal.namespaces()
        if len(namespaces) > 1:
            return _drain_namespaces(
                namespaces,
                run_ref=run_ref,
                client_factory=client_factory,
                wait_for_lock=wait_for_lock,
                lock_timeout=lock_timeout,
                promote_timeout=promote_timeout,
                on_error=on_error,
                on_delivered=on_delivered,
                skip_runs=skip_runs,
                credential_queues=credential_queues,
                long_ops=long_ops,
                only_ops=only_ops,
                window=window,
                priority_runs=priority_runs,
                set_best_effort_aside=set_best_effort_aside,
                senders=senders,
            )
    options = DrainOptions(
        run_ref=run_ref,
        client_factory=client_factory,
        wait_for_lock=wait_for_lock,
        lock_timeout=lock_timeout,
        promote_timeout=promote_timeout,
        on_error=on_error,
        on_delivered=on_delivered,
        skip_runs=skip_runs,
        long_ops=long_ops,
        only_ops=only_ops,
        window=window,
        priority_runs=priority_runs,
        set_best_effort_aside=set_best_effort_aside,
        senders=senders,
    )
    return DrainPass(journal, options).run()


def _drain_namespaces(
    namespaces: list,
    *,
    run_ref,
    client_factory,
    wait_for_lock,
    lock_timeout,
    promote_timeout,
    on_error,
    on_delivered,
    skip_runs,
    credential_queues,
    long_ops,
    only_ops,
    window,
    priority_runs=None,
    set_best_effort_aside=False,
    senders=None,
) -> DrainReport:
    """One pass per namespace (the root queue and its credential queues), reports summed."""
    combined = DrainReport()
    for queue in namespaces:
        if queue.dir.parent.parent.name == CREDENTIAL_NAMESPACE or (
            queue.dir.parent.name == CREDENTIAL_NAMESPACE
        ):
            if not credential_queues:
                # The root's detached worker: each credential queue has its own,
                # started by a writer holding that credential (#2041 round 3). This one
                # could only hold their writes, and keep its lease doing it.
                continue
        if queue.dir.parent.name == CREDENTIAL_NAMESPACE and _queue_is_empty(queue.dir):
            # An idle credential queue: nothing to lock, scan or rewrite status for
            # (#2041 round 3: hundreds of them made every pass slow).
            continue
        part = drain(
            queue,
            run_ref=run_ref,
            client_factory=client_factory,
            wait_for_lock=wait_for_lock,
            lock_timeout=lock_timeout,
            promote_timeout=promote_timeout,
            on_error=on_error,
            on_delivered=on_delivered,
            skip_runs=skip_runs,
            long_ops=long_ops,
            only_ops=only_ops,
            window=window,
            priority_runs=priority_runs,
            set_best_effort_aside=set_best_effort_aside,
            senders=senders,
            _include_receipts=False,
        )
        _add_part_report(combined, part)
    return combined


def _add_part_report(combined: DrainReport, part: DrainReport) -> None:
    """Fold one namespace's report into the pass total."""
    combined.delivered += part.delivered
    combined.dead_lettered += part.dead_lettered
    combined.remaining += part.remaining
    if part.auth_blocked and not combined.auth_blocked:
        combined.auth_status = part.auth_status
        combined.auth_message = part.auth_message
        combined.auth_context = part.auth_context
    combined.auth_blocked |= part.auth_blocked
    combined.queue_auth_stopped |= part.queue_auth_stopped
    combined.credential_refused += part.credential_refused
    combined.close_held += part.close_held
    combined.permanently_held += part.permanently_held
    combined.auth_refusals.extend(part.auth_refusals)
    combined.held_reasons.extend(
        r for r in part.held_reasons if r not in combined.held_reasons
    )
    combined.stopped_transient |= part.stopped_transient
    combined.held_back += part.held_back
    combined.credential_held += part.credential_held
    combined.errors.extend(part.errors)
    combined.deadline_reached |= part.deadline_reached
    combined.lock_busy |= part.lock_busy
    combined.unreachable |= part.unreachable
    if part.queued_runs is not None:
        combined.queued_runs = (combined.queued_runs or set()) | part.queued_runs
    combined.unknown_kinds += part.unknown_kinds
    combined.in_progress += part.in_progress
    combined.coalesced += part.coalesced
    combined.skipped += part.skipped
    combined.dead_letter_records.extend(part.dead_letter_records)
    combined.progressed_runs |= part.progressed_runs
    combined.busy_runs |= part.busy_runs
    combined.superseded.merge(part.superseded)
    for lane, stall in part.stalled_runs.items():
        combined.stalled_runs.setdefault(lane, stall)
    if part.retry_after is not None:
        combined.retry_after = max(combined.retry_after or 0.0, part.retry_after)
    combined.deferred += part.deferred
    if part.send_in is not None:
        combined.send_in = (
            part.send_in if combined.send_in is None else min(combined.send_in, part.send_in)
        )
    combined.deferred_loads.update(part.deferred_loads)
    for ref, count in part.delivered_by_run.items():
        combined.delivered_by_run[ref] = combined.delivered_by_run.get(ref, 0) + count
    combined.progressed_refs |= part.progressed_refs
    combined.lane_refs.update(part.lane_refs)
    combined.held_again += part.held_again
    combined.lane_held += part.lane_held
    combined.answered_servers |= part.answered_servers
    combined.failing_servers |= part.failing_servers
    combined.server_storing.update(part.server_storing)


@dataclass(frozen=True)
class DrainOptions:
    """What the caller asked of one pass (see `drain`)."""

    run_ref: str | None = None
    client_factory: Callable[[dict | None], Any] | None = None
    wait_for_lock: bool = True
    lock_timeout: float | None = None
    promote_timeout: float | None = None
    on_error: Callable[[Exception], None] | None = None
    on_delivered: Callable[[str | None], None] | None = None
    skip_runs: "set | frozenset | None" = None
    long_ops: bool = True
    only_ops: "set | frozenset | None" = None
    window: "CollectWindow | None" = None
    priority_runs: "set | frozenset | None" = None
    set_best_effort_aside: bool = False
    senders: "SenderClients | None" = None


if TYPE_CHECKING:
    from probe.sdk.delivery.outbox.drain.window import CollectWindow
    from probe.sdk.delivery.outbox.drain.settle import DrainSettleMixin
    from probe.sdk.delivery.outbox.drain.senders import DrainSendersMixin
    from probe.sdk.delivery.outbox.drain.lanes import DrainLanesMixin

    class _DrainPassParts(
        DrainSettleMixin,
        DrainSendersMixin,
        DrainLanesMixin,
    ):
        """DrainPass's parts as bases, for editors and type checkers; at runtime fold_parts() copies them in."""
else:
    _DrainPassParts = object


class DrainPass(_DrainPassParts):
    """One drain pass over one queue: its state, and the stages `drain` runs in order."""

    def __init__(self, journal: Journal, options: DrainOptions):
        self.journal = journal
        self.options = options
        self.report = DrainReport()
        # Whether an upload LEFT the queue this pass (delivered or dead-lettered): only then can a
        # blob have lost its last reference. `gc_blobs` re-reads the whole queue under the append
        # lock; after a pass that merely TRIED an upload (head of the queue during an outage, every
        # pass) it blocked `log()` ~1 s per pass at 20k ops (review of #2038).
        self.settled_upload = False
        # Petname -> uuid, for this drain only. See _resolved_run_id.
        self.run_ids: dict[str, str] = {}
        # What the closing status recount may reuse instead of re-parsing under the append lock
        # (plan 1.9); filled by the one scan below.
        self.known: dict[str, tuple[int, str | None]] = {}
        self.held_note: str | None = None
        # Per run: queued-at of each blocking op in the outbox's OTHER queues. Read once, only
        # when this pass meets a run's close.
        self.elsewhere: dict | None = None

    def run(self) -> DrainReport:
        """Prepare the queue, take the drain lock, deliver, then settle the status file."""
        if not self._prepare_queue():
            return self.report
        self._start_senders()
        if not self._take_lock():
            return self.report
        try:
            self._deliver_queue()
        finally:
            self._finish_pass()
        return self.report

    # -- before the lock ----------------------------------------------------------------------
    def _prepare_queue(self) -> bool:
        """Layout, stale temps and waiting uploads; False when the outbox is paused."""
        journal = self.journal
        journal._ensure()
        if journal.receipt_enabled:
            journal._receipt_dirs()
        try:
            journal.sweep_stale_temps()
        except Exception:  # noqa: BLE001 -- hygiene is best-effort
            pass
        if journal.paused:
            self.report.remaining = journal._count_dir(journal.ops_dir)[0]
            return False
        if not journal.receipt_enabled:
            # Uploads queued before their credential scan become ops first: every new-version drain
            # (worker, barrier, `probe outbox drain`) is a promoter. An item another process holds
            # is left to it.
            try:
                # The lease says "someone is promoting", so a kick meanwhile forks no promote-only
                # worker; items have their own locks, so this promotes with or without the lease.
                with _try_lock(journal.promote_lease):
                    journal.promote_waiting(run_ref=self.options.run_ref, timeout=self.options.promote_timeout)
            except Exception:  # noqa: BLE001 -- items stay waiting; the next pass retries
                pass
        return True

    def _take_lock(self) -> bool:
        """The drain lock, or a `lock_busy` report when another drain keeps it past the wait."""
        journal = self.journal
        self.lock_handle = journal.drain_lock.open("a+")
        # A run's close (its barrier, or the uploads it must see through) says it is waiting, so a
        # pass holding the lock gives it up at its next op (#3618).
        urgent = self.options.run_ref is not None or self.options.only_ops is not None
        if not _take_drain_lock(
            self.lock_handle,
            wait_for_lock=self.options.wait_for_lock,
            timeout=self.options.lock_timeout,
            want=journal.drain_want if urgent and not journal.receipt_enabled else None,
        ):
            self.lock_handle.close()
            self.report.remaining = journal._count_dir(journal.ops_dir)[0]
            self.report.lock_busy = True
            self.report.errors.append("another drain holds the lock")
            return False
        self.drain_hold = _DrainHold(journal, self.lock_handle, urgent=urgent)
        return True

    # -- the queue ------------------------------------------------------------------------------
    def _deliver_queue(self) -> None:
        """Every op of the queue, in lane order, until the pass ends."""
        journal = self.journal
        if journal.receipt_enabled:
            journal.recover_intents()
        # 2.3: a close a dead relaunch held aside goes back in the queue, so this pass delivers
        # it (a stat when nothing is held).
        try:
            restore_abandoned_holds(journal)
        except Exception:  # noqa: BLE001 -- a hold left in place is the old behaviour
            pass
        self._read_queue()
        for position, (path, op) in enumerate(self.queued):
            if not self._handle_op(position, path, op):
                break

    def _handle_op(self, position: int, path: Path, op: dict) -> bool:
        """One queued op: pass over it, hold it, or send it (alone, or with the metric and step
        ops queued behind it: `_partition`). False ends the pass."""
        if path in self.consumed:
            return True  # delivered inside an earlier op's batch
        if self.parallel and path not in self.prefetched and self.cursor <= position:
            if not self._send_upload_window(position):
                return False
        if self._is_not_for_this_pass(path, op):
            return True
        lane = _lane_of(op)
        if self._is_held_for_its_run(path, lane) or self._is_in_collect_window(path, lane):
            return True
        # Between two ops: a close waiting for the drain lock gets it now
        # (#3618). Whatever another drain did meanwhile is on disk.
        try:
            self.drain_hold.between_ops()
        except _LockNotBack:
            self.report.deadline_reached = True
            return False
        if not self.drain_hold.fresh(path, op):
            self.consumed.add(path)
            return True  # another drain sent it, or set it aside, while this pass was away
        if self.drain_hold.busy(lane):
            self.mark_run_busy(lane)
            return True
        if (
            self._needs_newer_sdk(op, lane)
            or self._is_close_held(op, lane)
            or self._is_close_behind_an_upload(op, lane)
        ):
            return True
        self.journal._scan_forget(path.name)  # attempted: read it fresh next pass
        metric_ops, step_ops = (
            ([], [])
            if self.journal.receipt_enabled
            else _partition(
                self.lanes.get(lane) or [],
                self.lane_index.get(path, 0),
                self.held_back.get(lane),
                still_queued=self.is_still_queued if self.drain_hold.let_go else self.is_unsent,
            )
        )
        batch = [*metric_ops, *step_ops]
        for item_path, _ in batch:
            self.journal._scan_forget(item_path.name)

        if batch:
            return self._send_batch(path, op, lane, metric_ops, step_ops)
        return self._send_one(path, op, lane)

    # -- after the pass -------------------------------------------------------------------------
    def _finish_pass(self) -> None:
        """Close what the pass opened, gc blobs, write status.json, release the drain lock."""
        journal = self.journal
        report = self.report
        if self.should_close_senders:  # the worker's own outlive the pass (I13)
            self.sender_clients.close()
        if self.settled_upload:  # no upload left the queue: no blob can be unreferenced
            try:
                journal.gc_blobs()
            except Exception:  # noqa: BLE001
                pass
        self._write_status()
        if not journal.receipt_enabled:
            # Plan (g): an upload still in its own queue is still work, so a worker does not
            # exit with one half-sent (status.json's count, which older releases read, stays
            # the shared queue's).
            report.remaining += _multipart_pending_count(journal)
        self.drain_hold.close()
        oscompat.flock(self.lock_handle.fileno(), oscompat.LOCK_UN)
        self.lock_handle.close()
        if report.superseded.writes:
            # Set aside, not lost by us: a newer attempt owns those runs (T24). Every drain
            # says so (a `finish()`'s, a flush's, the worker's), as a dead letter used to reach
            # `probe outbox status`.
            try:
                from ..... import analytics as _telemetry

                # A worker's surface in a worker; `sdk` in a script's or a command's own drain.
                _telemetry.emit_outbox_discarded(
                    report.superseded, reason=_telemetry.DiscardReason.SUPERSEDED,
                    surface=_telemetry.get_worker_surface(),
                )
            except Exception:  # noqa: BLE001 -- telemetry never stops delivery
                pass

    def _write_status(self) -> None:
        """status.json, recounted under the append lock and merged with what is on disk now."""
        journal = self.journal
        report = self.report
        # Counted from the recount itself: names under the lock, parsing only what this pass's
        # scan did not see (plan 1.9).
        journal._ensure()
        with file_lock(journal.append_lock):
            # Merged with what is on disk NOW, under the append lock: a `probe login` during
            # this pass cleared the list (clear_auth_block) and writing back the one read at
            # the start undid it (#2041 re-review).
            previous = Journal.read_status(journal.dir, include_receipts=False, keep_idle_refusals=True) or {}
            on_disk = previous.get(StatusField.REFUSED_FINGERPRINTS) or {}
            if not isinstance(on_disk, dict):
                on_disk = {}
            # A held run the caller backs off is skipped next pass; not recounting its holds
            # wrote `held: 0` while they still waited and the stuck signal flickered. The last
            # count stands for the ops this pass did not look at.
            carried = min(_status_count(previous.get(StatusField.HELD)), report.skipped)
            carried_close = min(_status_count(previous.get(StatusField.CLOSE_HELD)), carried)
            cleared = set(self.cooling) - set(on_disk)
            report.remaining = journal._write_status_locked(
                known=self.known,
                auth_blocked_since=(now_iso() if report.queue_auth_stopped else None),
                held=report.credential_held + report.credential_refused + report.close_held + carried,
                close_held=report.close_held + carried_close,
                held_at=now_iso(),
                refused_fingerprints={
                    **{fp: at for fp, at in on_disk.items() if fp not in self.delivered_fps},
                    **{fp: at for fp, at in self.refused_now.items() if fp not in cleared},
                },
                last_error=(report.errors[-1] if report.errors else self.held_note),
                new_dead_letters=report.dead_letter_records,
            )
from probe.sdk.delivery.journal.item_locks import _try_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.paths import _queue_is_empty  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.status_file import _status_count  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CREDENTIAL_NAMESPACE,
    _lane_of,
)
from probe.sdk.delivery.outbox.drain.coalesce import _partition  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.holds import restore_abandoned_holds  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lanes import _multipart_pending_count  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lock import _DrainHold, _LockNotBack, _take_drain_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import DrainReport  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.settle import DrainSettleMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.senders import DrainSendersMixin, SenderClients  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lanes import DrainLanesMixin  # noqa: E402 -- pieces need each other; the front door loads this one first

# DrainPass's parts read it back at import time, so they load after it and are folded in here.
fold_parts(DrainPass, DrainSettleMixin, DrainSendersMixin, DrainLanesMixin)
