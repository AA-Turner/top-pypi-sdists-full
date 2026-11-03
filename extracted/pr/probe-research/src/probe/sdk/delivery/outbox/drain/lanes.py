"""order the queue into per-run lanes (round robin, multipart lane) and back off a stalled lane."""

from __future__ import annotations

import os
from pathlib import Path
import time
from typing import Any


def _multipart_pending_count(journal: "Journal") -> int:
    """Multipart ops queued in this journal (names only, no parse)."""
    try:
        return sum(1 for n in os.listdir(journal.dir / "multipart" / "ops") if n.endswith(".json"))
    except OSError:
        return 0


def _multipart_waiting(op: Any) -> bool:
    """A multipart op waiting on the server rather than sending: it does not hold the
    one-upload-at-a-time turn (plan (g))."""
    state = (op.get("multipart") or {}).get("state") if isinstance(op, dict) else None
    return state in ("verifying", "busy")


def _is_waited_for(op: Any, runs: set) -> bool:
    """Whether ``op`` belongs to a run a `finish()` is waiting on (R2)."""
    return isinstance(op, dict) and op.get("run_ref") in runs


def _round_robin(queued: list[tuple[Path, dict]]) -> list[tuple[Path, dict]]:
    """The FIFO list interleaved by run: each run's ops keep their order and the runs take
    turns, one op each, in the order of their oldest op."""
    lanes: dict[Any, list[tuple[Path, dict]]] = {}
    for item in queued:
        op = item[1]
        lanes.setdefault(_lane_of(op), []).append(item)
    if len(lanes) <= 1:
        return queued
    order: list[tuple[Path, dict]] = []
    depth = max(len(ops) for ops in lanes.values())
    for turn in range(depth):
        for ops in lanes.values():
            if turn < len(ops):
                order.append(ops[turn])
    return order


class LaneBackoff:
    """Per-run waits for a loop that drains the whole queue (plan 1.6). A stalled run waits
    out its own backoff (`durable.backoff_delays`, at least the server's ``Retry-After``)
    while every other run keeps delivering; a run that progresses starts over. The detached
    worker and in-process exporter each keep one, passing `skip()` as ``skip_runs``.
    """

    def __init__(self, *, ceiling: float) -> None:
        from .....foundation.durable import durable

        self._durable = durable
        self._ceiling = ceiling
        self._delays: dict[Any, Any] = {}
        self._until: dict[Any, float] = {}
        self._last_wait: dict[Any, float] = {}

    def skip(self, now: float | None = None) -> set:
        now = time.monotonic() if now is None else now
        return {lane for lane, until in self._until.items() if until > now}

    def record(self, report: DrainReport, now: float | None = None) -> None:
        now = time.monotonic() if now is None else now
        # A run that progressed starts over, also when it then stalled in the same pass (review
        # of #2051: a busy run answering `Retry-After: 1` to every other write climbed to the
        # 300 s ceiling while delivering).
        for lane in report.progressed_runs:
            self._forget(lane)
        # A run with nothing queued any more (another drainer, its own `finish()`, delivered it)
        # is forgotten: an expired entry kept `next_wake()` at 0 and the worker re-drained every
        # 0.05 s (review of #2051: 5.4 CPU-s per 10 s).
        if report.queued_runs is not None:
            for lane in list(self._until):
                if lane not in report.queued_runs:
                    self._forget(lane)
        for lane, stall in report.stalled_runs.items():
            delays = self._delays.setdefault(lane, self._durable.backoff_delays(None))
            wait = self._durable.honor_retry_after(
                next(delays), stall.retry_after, ceiling=self._ceiling
            )
            if stall.wake_by is not None:
                # A hold ending at a known time is looked at again then, not a grown backoff later
                # (#2041 round 5: a close held to its cap landed 216 s after it, past the reaper).
                wait = min(wait, max(float(stall.wake_by), 0.05))
            self._until[lane] = now + wait
            self._last_wait[lane] = wait

    def forget(self, lane: Any) -> None:
        """Try ``lane`` again on the next pass (its stuck head was set aside)."""
        self._forget(lane)

    def _forget(self, lane: Any) -> None:
        self._delays.pop(lane, None)
        self._until.pop(lane, None)
        self._last_wait.pop(lane, None)

    def next_wake(self, now: float | None = None) -> float | None:
        """Seconds until the soonest run STILL waiting may be tried again, or None: an entry
        whose wait is over says nothing about when to look next (tried next pass anyway)."""
        now = time.monotonic() if now is None else now
        waiting = [until for until in self._until.values() if until > now]
        if not waiting:
            return None
        return min(waiting) - now

    def at_ceiling(self) -> bool:
        """Whether some run has backed off all the way to the ceiling."""
        return any(wait >= self._ceiling for wait in self._last_wait.values())


class DrainLanesMixin:
    """Part of DrainPass: its methods run with `self` the DrainPass; fold_parts() copies them into DrainPass."""

    def _read_queue(self) -> None:
        """The pass's work list: one parse of the queue, in lanes, multipart last."""
        journal = self.journal
        options = self.options
        multipart_queue = self._read_multipart_queue()
        # A run's ops queued after an upload still being scanned wait for it: its close must not
        # reach the server first (see `promote_waiting`). Read BEFORE the queue: an upload
        # promoted in between is then both "waiting" and queued, holding successors back one
        # pass; the other order would miss it in both and let its close go first.
        self.held_back = {} if journal.receipt_enabled else journal.waiting_positions()
        # Runs whose lane is held after a stall (`outbox/held`): none of their writes goes this pass.
        self.held_lanes = set() if journal.receipt_enabled else held_lanes(journal.dir)
        # ONE parse of the queue, outside the append lock (plan 1.9): this pass's work list,
        # quarantine list and the recount's cache.
        queued, corrupt = journal._scan_ops(stamps=self.drain_hold.stamps)
        self.known = op_meta(queued)
        self.report.queued_runs = {
            _lane_of(op) for _, op in [*queued, *multipart_queue] if isinstance(op, dict)
        }
        # Each run's ops in queue order, for coalescing (plan 1.2): a metric op rides in one
        # POST with the ones queued right behind it in its run.
        self.lanes: dict[Any, list[tuple[Path, dict]]] = {}
        for item in queued:
            self.lanes.setdefault(_lane_of(item[1]), []).append(item)
        self.lane_index = {item[0]: n for ops in self.lanes.values() for n, item in enumerate(ops)}
        self.consumed: set[Path] = set()
        priority = set(options.priority_runs or ())
        if options.run_ref is None:
            queued = _round_robin(queued)
            if priority:
                # R2: the runs a `finish()` waits on go first, each keeping its order.
                queued = sorted(queued, key=lambda item: not _is_waited_for(item[1], priority))
                multipart_queue = sorted(
                    multipart_queue, key=lambda item: not _is_waited_for(item[1], priority)
                )
        else:
            # A run's own pass (its close, a takeover): the run's lane first, then what rides a
            # lane of its own (the open's archive, queued at open), so a store that never answers
            # cannot spend the pass's budget before the run's data (and only once that lane is
            # through: `_waits_for_own_lane`). Each lane keeps its order.
            queued = sorted(queued, key=lambda item: _lane_of(item[1]) != options.run_ref)
        # Plan (g): a multipart upload spends up to a slice of seconds per visit, so every other
        # lane goes first each pass (a metric behind a 10 GB checkpoint is delivered before its
        # next slice). ONE upload at a time sends or hashes (the oldest not waiting on the
        # server); the next starts only when it is verifying, so an earlier checkpoint finishes
        # and releases its staged bytes before a later one pins more.
        self.queued = [*queued, *multipart_queue]
        self.report.lane_refs = {
            _lane_of(op): op.get("run_ref")
            for _, op in self.queued
            if isinstance(op, dict) and (op.get("run_ref") is None or isinstance(op.get("run_ref"), str))
        }
        self.multipart_turn = next(
            (p for p, o in multipart_queue if not _multipart_waiting(o)), None
        )
        self.skip = set(options.skip_runs or ())
        self.stalled = self.report.stalled_runs
        # Runs parked for the pass behind an op this drainer must not send.
        self.held_runs: set = set()
        # Of those, the runs held for a credential (#2035): their later ops count as kept too.
        self.credential_lanes: dict = {}
        self.held_paths: set = set()
        for _path, queued_op in self.queued:
            queued_stamp = (queued_op.get("context") or {}).get("principal")
            queued_as = stamp_identity(queued_stamp) if isinstance(queued_stamp, dict) else None
            if queued_as is not None:
                self.accounts.setdefault(str(queued_stamp.get("fingerprint")), queued_as)
        try:
            journal.quarantine_paths(corrupt, known=self.known)
        except Exception:  # noqa: BLE001 -- quarantine is best-effort hygiene
            pass
        self.workers = _upload_workers()
        self.parallel = self.workers > 1
        self.prefetched: dict = {}
        # The window REFILLS as the serial loop advances. A single fetch took the first
        # `workers * FACTOR` operations and every one after went back to being uploaded alone:
        # a hundred-thousand-file import parallelised sixteen files and serialised the rest,
        # the latency this exists to remove, hidden behind a test that never staged over eight.
        self.cursor = 0
        self.lost_responses = 0
        # The collect window (plan T2): each run's lane is judged once, at its first op this
        # pass. A close waiting for the drain lock sends every lane now, and so does a volume
        # under the free-space floor: a writer there sends around an EMPTY queue only (C6).
        self.window_judged: set = set()
        self.window_off = (
            self.options.window is None or self.drain_hold._wanted() or is_short_of_disk(self.journal)
        )

    def _read_multipart_queue(self) -> list:
        """Multipart uploads still to run, for a pass that may run them."""
        journal = self.journal
        options = self.options
        # Plan (g): multipart uploads live in a queue of their own (`<outbox>/multipart/ops/`)
        # that no earlier release reads, so an older worker holding this outbox never meets one.
        # Only a pass that may run them (not a run's barrier, not a closing exporter) reads it.
        multipart_queue: list = []
        if (
            not journal.receipt_enabled
            and options.run_ref is None
            and (options.only_ops is not None or options.long_ops)
        ):
            try:
                _multipart = multipart_storage()

                # A staged copy nothing will read again (op finished or dead-lettered, a copy
                # cut short by a kill) goes first.
                _multipart.gc_staging(journal)
                multipart_queue = _multipart.pending(journal)
            except Exception:  # noqa: BLE001 -- multipart waits for the next pass
                multipart_queue = []
        return multipart_queue

    def _is_not_for_this_pass(self, path: Path, op: dict) -> bool:
        """Outside what the caller asked for (``only_ops``, ``run_ref``), or a multipart upload
        whose turn it is not."""
        only_ops = self.options.only_ops
        if only_ops is not None and op.get("op_id") not in only_ops:
            return True
        if self.options.run_ref is not None and op.get("run_ref") != self.options.run_ref:
            return True
        if self._waits_for_own_lane(op):
            return True
        if _is_multipart(op) and path != self.multipart_turn and not _multipart_waiting(op):
            return True  # not its turn: one upload at a time (plan (g))
        return False

    def _waits_for_own_lane(self, op: dict) -> bool:
        """A run's own pass (its close, a takeover): an op on a lane of its own (the open's archive)
        goes only once the run's lane is through. One 503 left that lane for the next pass and the
        archive's hung PUT spent what was left of the close's deadline; a window taking it beside
        the run's first upload waited for it the same way."""
        run_ref = self.options.run_ref
        if run_ref is None or _lane_of(op) == run_ref:
            return False
        return any(path.exists() for path, _ in self.lanes.get(run_ref) or [])

    def _is_held_for_its_run(self, path: Path, lane: Any) -> bool:
        """Its run waits this pass (held, backed off, stalled, or behind a waiting upload); counted."""
        report = self.report
        if lane in self.credential_lanes and path not in self.held_paths:
            # A later op of a run held for its credential (or a close held behind another
            # queue): kept too and counted, so "N kept" says how many writes wait, not how
            # many runs (#2041 round 4), and how many `discard --held` would drop (round 5).
            report.credential_held += 1
            if self.credential_lanes[lane]:
                report.permanently_held += 1
            return True
        if lane in self.held_lanes:
            report.lane_held += 1
            return True  # held after a stall: nothing of its run passes its stuck write
        if lane in self.skip:
            report.skipped += 1
            return True  # backed off: its run waits; the other runs do not
        if lane in self.stalled or lane in self.held_runs:
            return True  # its run waits; the other runs do not
        if path.name > self.held_back.get(lane, path.name):
            report.held_back += 1
            return True
        return False

    def _is_in_collect_window(self, path: Path, lane: Any) -> bool:
        """Its run's collect window is open (plan T2): the run's telemetry goes in one POST later.
        Each lane is judged once, at its first op this pass; counted."""
        report = self.report
        if not self.window_off and lane not in self.window_judged:
            self.window_judged.add(lane)
            held = self.options.window.hold(
                (self.lanes.get(lane) or [])[self.lane_index.get(path, 0):], sizes=self.drain_hold.stamps
            )
            if held is not None:
                report.deferred_loads[lane] = held.load
                report.send_in = held.wait if report.send_in is None else min(report.send_in, held.wait)
        if lane in report.deferred_loads:
            report.deferred += 1
            return True
        return False

    def _needs_newer_sdk(self, op: dict, lane: Any) -> bool:
        """An op kind this SDK does not know: left in order for a newer worker."""
        report = self.report
        kind = op.get("kind")
        if isinstance(kind, str) and kind not in OP_KINDS:
            # A newer SDK's op. Not attempted: no attempt charged, the 24 h budget never
            # starts; it waits, in its run's order, for a worker that can deliver it (plan
            # 1.11). A kind that is not even a string is not a newer SDK's: `_execute`
            # refuses it (dead letter), as always (review of #2052: a list here raised
            # TypeError and failed every pass machine-wide).
            reason = f"op kind {kind!r} needs a newer probe-research to deliver it"
            report.unknown_kinds += 1
            if reason not in report.errors:
                report.errors.append(reason)
            if lane is not None:
                self.stalled[lane] = LaneStall(reason)
            # An op naming no run holds only itself: the run-less lane has no order to keep
            # and stalling it would hold every other run-less write behind a newer SDK's op.
            return True
        return False

    def _is_close_held(self, op: dict, lane: Any) -> bool:
        """A run's close waiting for its writes queued under another credential."""
        report = self.report
        if lane is not None and _is_run_close(op) and not _close_hold_expired(op):
            waiting = self.count_writes_elsewhere(lane, op.get("enqueued_at"), _write_epoch_of(op))
            if waiting:
                # The close must not land before its data: writes of this run queued earlier
                # under another credential are in another queue, which this queue's order
                # cannot see (#2041 round 3). Held, at most CLOSE_HOLD_MAX_SECONDS.
                reason = (
                    f"the close of run {lane} waits for {waiting} of its write(s) queued "
                    "under another credential"
                )
                self.stalled[lane] = LaneStall(reason, held=True, wake_by=_close_hold_left(op))
                report.close_held += 1
                if reason not in report.held_reasons:
                    report.held_reasons.append(reason)
                return True
        return False

    def _is_close_behind_an_upload(self, op: dict, lane: Any) -> bool:
        """A run's close while an upload of that run is still being sent from a multipart queue
        (its own lane: the run's order cannot see it), in this queue or another of the outbox:
        sent now, the server would close the run before the checkpoint lands. Held, no time
        cap: a stuck upload is set aside by the stall rule (`outbox/held`), then the close goes."""
        if lane is None or not _is_run_close(op):
            return False
        uploading = self.count_uploads_of(lane)
        if not uploading:
            return False
        reason = f"the close of run {lane} waits for {uploading} of its upload(s) still sending"
        self.stalled[lane] = LaneStall(reason, held=True, wake_by=_UPLOAD_RECHECK_SECONDS)
        if reason not in self.report.held_reasons:
            self.report.held_reasons.append(reason)
        return True

    def count_uploads_of(self, run: str) -> int:
        """Multipart uploads of ``run`` still queued (not set aside) in any queue of the outbox.
        Read once per pass, only when the pass meets a close."""
        if getattr(self, "uploads", None) is None:
            self.uploads = {}
            for queue in self.journal.outbox_queues():
                if queue.receipt_enabled:
                    continue
                for _path, upload in Journal._read_dir(queue.dir / "multipart" / "ops"):
                    ref = upload.get("run_ref") if isinstance(upload, dict) else None
                    if isinstance(ref, str):
                        self.uploads[ref] = self.uploads.get(ref, 0) + 1
        return self.uploads.get(run, 0)

    def count_writes_elsewhere(self, run: str, before: str | None, epoch: Any = None) -> int:
        """How many blocking writes of ``run`` queued no later than ``before`` sit in the
        outbox's other queues. A write stamped with an OLDER write epoch than the close's is
        left out: the server refuses it as stale, so holding the close for it only delays the
        close (#2041 round 5: a takeover's close sat behind the dead attempt's writes)."""
        if self.elsewhere is None:
            self.elsewhere = {}
            for queue in self.journal.other_queues():
                for _other_path, other in Journal._read_dir(queue.ops_dir):
                    if isinstance(other, dict) and other.get("run_ref") and other.get("blocking", True):
                        self.elsewhere.setdefault(other["run_ref"], []).append(
                            (str(other.get("enqueued_at") or ""), _write_epoch_of(other))
                        )
                if not queue.receipt_enabled:
                    # Uploads still waiting for their credential scan count too: they become
                    # ops of that queue shortly (#2041 round 4).
                    for _position, _op_id, ref, readable, blocking in queue._waiting_items():
                        if readable and blocking and ref:
                            self.elsewhere.setdefault(ref, []).append(("", None))
        return sum(
            1
            for at, their_epoch in self.elsewhere.get(run, ())
            if (not before or at <= before)
            and not (epoch is not None and their_epoch is not None and their_epoch < epoch)
        )

    def should_skip_in_window(self, path: Path, op: dict) -> bool:
        """What the serial pass would not attempt now, for `_run_window`: such an op
        ends its run's parallel window."""
        lane = _lane_of(op)
        only_ops = self.options.only_ops
        return (
            (only_ops is not None and op.get("op_id") not in only_ops)
            or self._waits_for_own_lane(op)
            or lane in self.skip
            or lane in self.held_lanes
            or lane in self.stalled
            or lane in self.held_runs
            or lane in self.credential_lanes
            or path.name > self.held_back.get(lane, path.name)
            or self.drain_hold.busy(lane)
        )

    def is_unsent(self, item_path: Path, item_op: dict) -> bool:
        """For `_partition`: an op an earlier batch of this pass sent (or holds) does not ride
        again; one a batch stopped before is still to go (`ALONE_MAX`)."""
        return item_path not in self.consumed

    def is_still_queued(self, item_path: Path, item_op: dict) -> bool:
        """For `_partition` once this pass let go of the drain lock: an op another drain sent
        meanwhile does not ride again (#3618)."""
        if item_path in self.consumed:
            return False
        if self.drain_hold.fresh(item_path, item_op):
            return True
        self.consumed.add(item_path)
        return False

#: How soon a close held behind its run's upload looks again (an upload sends a slice per pass).
_UPLOAD_RECHECK_SECONDS = 5.0

from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _lane_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import DrainReport  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import LaneStall  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import OP_KINDS  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.holds import _close_hold_expired  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.holds import _close_hold_left  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _is_multipart  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _is_run_close  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.upload_windows import _upload_workers  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _write_epoch_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import multipart_storage  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import op_meta  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import stamp_identity  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.window import is_short_of_disk  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.held import held_lanes  # noqa: E402 -- pieces need each other; the front door loads this one first
