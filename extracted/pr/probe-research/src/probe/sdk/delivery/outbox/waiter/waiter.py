"""DeliveryWaiter: wait for the outbox workers to deliver one run's writes (R15). Each poll it
reads only the workers' progress records; it counts the folders once before it says "delivered".
It never sends a queued write (D1): it only makes sure a worker runs."""

from __future__ import annotations

import sys
import time
from typing import Any, Callable

from probe.sdk.delivery.outbox.progress import STALL_LIMIT_SECONDS, DeliveryErrorKind
from probe.sdk.delivery.outbox.waiter.marks import mark_waiting, touch_mark
from probe.sdk.delivery.outbox.waiter.outcome import WaitOutcome, WaitResult
from probe.sdk.delivery.outbox.waiter.progress_line import ProgressLine
from probe.sdk.delivery.status_fields import StatusField
from probe.sdk.delivery.outbox.waiter.scan import (
    RunView,
    count_run,
    queues_holding,
    read_records,
    worker_queues,
)

#: How long nothing may answer before the wait gives up (T1: deploys cause no outage, so this is
#: a real one; the worker keeps trying for its 24 h + 50 budget).
OUTAGE_LIMIT_SECONDS = 600.0
POLL_SECONDS = 0.5
PROGRESS_EVERY_SECONDS = 5.0
#: Worker deaths with nothing delivered before the wait gives up.
CRASH_RESTARTS = 3
#: Kicks with no worker ever taking the lease, and no service promising one, before "nothing here can send
#: them".
NO_SENDER_KICKS = 3
_KICK_EVERY_SECONDS = 2.0
#: The full count runs at most this often (only once the records say nothing is left).
_COUNT_EVERY_SECONDS = 5.0
_MARK_EVERY_SECONDS = 30.0
#: Nothing of the run moved this long: the folders are counted (at most every `_COUNT_EVERY_SECONDS`).
_STILL_SECONDS = 15.0
#: A record older than this (or with no worker on its queue) is checked against the folders.
_RECORD_STALE_SECONDS = 2.0
#: The server said this recently that it is storing the run's queued data (I15d): the run is
#: moving, however long that takes (no time cap, the user's decision).
SERVER_STORING_FRESH_SECONDS = 60.0


class DeliveryWaiter:
    """One wait on one run. ``own_queue`` is the queue its client writes to; ``kick_own`` starts
    that queue's worker with the client's credential (a token passed in code rides it, R5)."""

    def __init__(
        self,
        journal: Any,
        run_ref: str,
        *,
        kick_own: Callable[[], None] | None = None,
        deadline: float | None = None,
        on_progress: Callable[[str], None] | None = None,
        clock: Callable[[], float] = time.monotonic,
        wall: Callable[[], float] = time.time,
        sleep: Callable[[float], None] = time.sleep,
        outage_limit: float = OUTAGE_LIMIT_SECONDS,
        stall_limit: float = STALL_LIMIT_SECONDS,
        min_epoch: int | None = None,
    ) -> None:
        self.journal = journal
        self.run_ref = run_ref
        self.kick_own = kick_own
        self.deadline = deadline
        self.on_progress = on_progress or _print_progress
        self.clock, self.wall, self.sleep = clock, wall, sleep
        self.outage_limit, self.stall_limit = outage_limit, stall_limit
        #: This attempt's write epoch: an older attempt's writes are refused, never waited for.
        self.min_epoch = min_epoch
        self.queues = worker_queues(journal)
        self.line = ProgressLine(run_ref, clock=clock)
        self._view = RunView()
        self._kicks: dict[str, int] = {}
        self._kicked_at: dict[str, float] = {}
        self._seen_alive: dict[str, bool] = {}
        self._deaths = 0
        #: The run's delivered total when its worker first died: a crash loop delivers nothing.
        self._delivered_at_death: int | None = None
        self._old_since: dict[str, float] = {}
        self._holder: str | None = None
        #: The full count's tallies, kept across counts so each op file is parsed once.
        self._tallies: dict = {}

    # -- the wait ----------------------------------------------------------------------------
    def wait(self) -> WaitResult:
        """Wait until the run's writes are delivered or a stop rule fires (the outcomes table)."""
        self.started = self.clock()
        root = self.journal.outbox_root
        with mark_waiting(root, self.run_ref):
            try:
                return self._loop(root)
            except KeyboardInterrupt:
                self._kick_holding()
                return self._result(WaitOutcome.STOPPED_WAITING, self._view)

    def _loop(self, root) -> WaitResult:
        self.holding = queues_holding(self.queues, self.run_ref, min_epoch=self.min_epoch)
        if not self.holding:
            return self._settle(self._count())
        self._delivered_at_start: int | None = None
        moved_at = said_at = marked_at = self.clock()
        counted_at: float | None = None
        last_seen = (None, None)
        while True:
            now = self.clock()
            view = self._view = read_records(self.queues, self.run_ref)
            if self._delivered_at_start is None and view.workers:
                self._delivered_at_start = view.delivered_total
            seen = (view.delivered_total, view.pending + view.best_effort + view.held + view.failed)
            if seen != last_seen or self._moved_recently(view, now):
                moved_at, last_seen = now, seen
            in_line = view.pending + view.best_effort
            # The records count every write (an older attempt's too): the folders are counted when
            # they say nothing is left, when they may be behind, and when nothing moved for a while.
            doubt = in_line == 0 or self._is_stale(view) or now - moved_at >= _STILL_SECONDS
            if doubt and (counted_at is None or now - counted_at >= _COUNT_EVERY_SECONDS):
                counted_at = now
                full = self._count()
                if full.pending + full.best_effort == 0:
                    return self._settle(full)
            ended = self._stop_rule(view, now, moved_at)
            if ended is not None:
                # A failure is said only once the folders agree something is still in line: a
                # worker can die between its last delivery and its last record.
                full = self._count()
                if full.pending + full.best_effort == 0:
                    return self._settle(full)
                # No worker ever wrote a record (no sender at all): only the folders count them.
                return self._result(ended, view if view.updated_at is not None else full)
            if now - self.started >= PROGRESS_EVERY_SECONDS and now - said_at >= PROGRESS_EVERY_SECONDS:
                said_at = now
                self.on_progress(self.line.render(view, is_server_storing=self._is_server_storing(view)))
            if now - marked_at >= _MARK_EVERY_SECONDS:
                marked_at = now
                touch_mark(root, self.run_ref)
            self.sleep(POLL_SECONDS)

    def _count(self) -> RunView:
        return count_run(self.queues, self.run_ref, self._tallies, min_epoch=self.min_epoch)

    def _is_stale(self, view: RunView) -> bool:
        """The records may be behind the folders: none yet, none newer than a few polls (a
        worker publishes before every sleep), or no worker holds any queue of the run."""
        from probe.sdk.delivery.outbox.lease import _lease_is_free

        if view.updated_at is None or self.wall() - view.updated_at > _RECORD_STALE_SECONDS:
            return True
        return all(_lease_is_free(queue) for queue in self.holding)

    def _moved_recently(self, view: RunView, now: float) -> bool:
        """The record says the run moved since the last poll (a multipart slice is progress too)."""
        last = view.last_progress_at
        if last is not None and self.wall() - last < POLL_SECONDS * 2:
            return True
        return self._is_server_storing(view)

    def _is_server_storing(self, view: RunView) -> bool:
        """The server holds the run's close until its queued data is stored, and said so lately."""
        said = view.server_storing_at
        return said is not None and self.wall() - said < SERVER_STORING_FRESH_SECONDS

    def _stop_rule(self, view: RunView, now: float, moved_at: float) -> WaitOutcome | None:
        """The first rule of the outcomes table that fires, or None to keep waiting."""
        if self.deadline is not None and now >= self.deadline:
            return WaitOutcome.OUT_OF_TIME
        blocked = self._blocked(view)
        if blocked is not None:
            return blocked
        tended = self._tend_workers(view, now, moved_at)
        if tended is not None:
            return tended
        if view.unreachable_since is not None and self.wall() - view.unreachable_since >= self.outage_limit:
            return WaitOutcome.UNREACHABLE
        if view.unreachable_since is None and now - moved_at >= 2 * self.stall_limit:
            return WaitOutcome.STALLED
        return None

    def _blocked(self, view: RunView) -> WaitOutcome | None:
        """Paused, or the credential refused: only a person changes that, so raise now."""
        from probe.sdk.delivery.journal.journal import Journal

        for queue in self.holding:
            if queue.paused:
                return WaitOutcome.PAUSED
            status = Journal.read_status(queue.dir, credential_queues=False) or {}
            if status.get(StatusField.AUTH_BLOCKED_SINCE):
                return WaitOutcome.LOGIN_REFUSED
        if DeliveryErrorKind.LOGIN_REFUSED in view.error_kinds:
            return WaitOutcome.LOGIN_REFUSED
        if DeliveryErrorKind.NEEDS_NEWER in view.error_kinds:
            return WaitOutcome.NEEDS_NEWER_SERVICE
        return None

    # -- keeping a worker on each queue that holds the run ----------------------------------
    def _tend_workers(self, view: RunView, now: float, moved_at: float) -> WaitOutcome | None:
        from probe.sdk.delivery.outbox.drainers.detached import is_drain_promised
        from probe.sdk.delivery.outbox.lease import (
            PROGRESS_FEATURE,
            _lease_is_free,
            ask_worker_to_step_aside,
            live_worker_has,
            worker_holder,
        )

        for queue in self.holding:
            key = str(queue.dir)
            if not _lease_is_free(queue):
                if live_worker_has(PROGRESS_FEATURE, key) is False:
                    # R3: an older release publishes no record; ask it to step aside.
                    ask_worker_to_step_aside(PROGRESS_FEATURE, key)
                    since = self._old_since.setdefault(key, now)
                    if now - since >= self.stall_limit:
                        holder = worker_holder(queue)
                        self._holder = f"pid {holder[0]}, {holder[1] or 'unknown release'}" if holder else None
                        return WaitOutcome.OLD_WORKER
                else:
                    self._old_since.pop(key, None)
                self._seen_alive[key] = True
                continue
            if self._seen_alive.pop(key, False) and not view.workers.get(key, (None, True))[1]:
                # Its lease is free and its record never said it exited: it died.
                if self._delivered_at_death is None or view.delivered_total > self._delivered_at_death:
                    self._deaths, self._delivered_at_death = 0, view.delivered_total
                self._deaths += 1
                if self._deaths >= CRASH_RESTARTS:
                    return WaitOutcome.WORKER_CRASH_LOOP
            if now - self._kicked_at.get(key, float("-inf")) >= _KICK_EVERY_SECONDS:
                self._kicked_at[key] = now
                self._kick(queue)
                self._kicks[key] = self._kicks.get(key, 0) + 1
                if (self._kicks[key] > NO_SENDER_KICKS and not any(self._seen_alive.values()) and not view.workers
                        and not is_drain_promised(queue.dir)):
                    return WaitOutcome.NO_SENDER
        return None

    def _kick(self, queue: Any) -> None:
        """Start the queue's worker: its own with this client's credential, others plainly."""
        try:
            if self.kick_own is not None and queue.dir == self.journal.dir:
                self.kick_own()
            else:
                from probe.sdk.delivery.outbox.drainers.detached import maybe_spawn

                maybe_spawn(str(queue.dir))
        except Exception:  # noqa: BLE001 -- the next poll kicks again
            pass

    def _kick_holding(self) -> None:
        for queue in getattr(self, "holding", None) or self.queues:
            self._kick(queue)

    # -- the result --------------------------------------------------------------------------
    def _settle(self, full: RunView) -> WaitResult:
        """Nothing of the run is queued any more: delivered, or what stayed behind and why."""
        if full.failed:
            outcome = WaitOutcome.REFUSED
        elif full.set_aside:
            # Refused for good (the run in the trash, or a newer attempt owns it): not delivered.
            outcome = WaitOutcome.SET_ASIDE
        elif full.held:
            outcome = WaitOutcome.STALLED
        else:
            outcome = WaitOutcome.DELIVERED
        full.delivered_total = self._view.delivered_total
        full.last_error = self._view.last_error
        return self._result(outcome, full)

    def _result(self, outcome: WaitOutcome, view: RunView) -> WaitResult:
        start = getattr(self, "_delivered_at_start", None)
        return WaitResult(
            outcome=outcome,
            run_ref=self.run_ref,
            pending=view.pending,
            pending_bytes=view.pending_bytes,
            held=view.held,
            failed=view.failed,
            discarded=view.discarded,
            set_aside=view.set_aside,
            delivered=max(0, view.delivered_total - (start or 0)) if start is not None else 0,
            first_error=view.last_error,
            waited_seconds=self.clock() - getattr(self, "started", self.clock()),
            holder=self._holder,
            service_version=_get_service_version() if outcome == WaitOutcome.NEEDS_NEWER_SERVICE else None,
        )


def _get_service_version() -> str | None:
    from probe.foundation.service_api import handoff

    return handoff.hello_answer().get("service_version")


def _print_progress(line: str) -> None:
    try:
        print(line, file=sys.stderr, flush=True)
    except Exception:  # noqa: BLE001 -- a closed stderr never stops the wait
        pass
