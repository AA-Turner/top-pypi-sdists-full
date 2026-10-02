"""THE RUN LEASE — the one primitive every scheduled handler inherits.

Two numbers govern how long a claimed run may live, and they mean different
things (the same split Temporal draws between ``heartbeat_timeout`` and
``start_to_close_timeout``, and Sidekiq between its process heartbeat and a
job's own limit):

* **The lease** (``configure(lease_seconds=...)``) is the HEARTBEAT TIMEOUT: how
  long ``sch_run.claim_expires_at`` may sit un-renewed before the scanner's
  expiry sweep decides the worker is dead. The runner renews it automatically
  while the handler coroutine is alive, so a live run never "expires" and a dead
  process is noticed within one lease, not one run ceiling.
* **The run ceiling** (``sch_agent_task.max_runtime_seconds`` — the "Max runtime"
  field on the schedule) is the HARD DEADLINE: the runner stops heartbeating
  and cancels the handler when it is reached, so a genuinely hung handler still
  dies, and it dies with whatever progress it had reported preserved.

Before 2026-09-13 there was only one number: the claim was written once for
``max(lease, max_runtime + 60)`` and nothing ever renewed it. When the sweep
marked such a run ``failed / lease expired`` it did NOT stop the handler — the
handler kept running as a zombie, spending real money, and its final report was
thrown away at the end because its claim token was gone. Live: the approved
keyword facet backfill classified 638 keywords in 31 minutes, was stamped
``failed`` with ``result_metadata=NULL``, and then carried on for hours with
nobody able to see it. The repeat guard, which judges "never succeeded" by
``result_metadata.units_done``, was blind to every one of those keywords.

What a handler gets
-------------------
``current_run_lease()`` returns the lease of the run this coroutine is executing
under (or an unbounded ``NoLease`` outside the scheduler — a user-triggered
command has its own lifetime). A multi-pass handler uses exactly two calls:

    lease = current_run_lease()
    for unit in work:
        if (stop := lease.stop_reason()) is not None:   # cannot finish another
            break                                        # unit before the deadline
        do(unit)
        await lease.progress(units_done=total_so_far, metadata={...})

``progress`` writes the running ``units_done`` and metadata onto the ledger row
UNDER THE CLAIM TOKEN, so an expiry, a cancel, or a crash after pass 3 leaves
pass 1–3 on the row; and it renews the lease, so a slow unit that reports is a
live unit. ``stop_reason`` answers "can I afford one more unit" from the
measured duration of the last one — the handler stops CLEANLY with a named
reason instead of being killed mid-unit with claims left hanging.
"""

from __future__ import annotations

import asyncio
import contextvars
import logging
import time
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from typing import Any

from .models import RUN_STOPPED_EARLY_KEY, RUN_UNITS_DONE_KEY

log = logging.getLogger("matrx_scheduler.lease")

#: ``result_metadata`` key carrying the wall-clock of the last progress write.
RUN_PROGRESS_AT_KEY = "progress_at"

#: Safety factor applied to the last unit's measured duration when a handler
#: asks whether it can afford another one. Units are not perfectly uniform (a
#: classifier batch varies with phrase length); 1.5× is the margin between
#: "stopped cleanly with 4 minutes to spare" and "killed mid-batch".
UNIT_SAFETY_FACTOR = 1.5

#: The heartbeat renews at a third of the lease, never faster than this.
#: KNOB MIRROR of platform.feature_knob "scheduler.lease" "min_heartbeat_interval_seconds"
#: (platform-locked, overridable_by []). Read at import inside a package that may
#: not touch the host's DB, so the registry row is the declared value and this
#: constant mirrors it; change the row AND this line together.
MIN_HEARTBEAT_INTERVAL_SECONDS = 5.0

_current: contextvars.ContextVar[RunLease | None] = contextvars.ContextVar(
    "matrx_scheduler_run_lease", default=None
)


class RunLease:
    """The lease of ONE claimed run, as the handler and the runner both see it."""

    def __init__(
        self,
        *,
        run_id: str,
        task_id: str,
        claim_token: str,
        lease_seconds: int,
        max_runtime_seconds: int,
        claimed_at: datetime | None = None,
        renew: Callable[[str, str, int], Awaitable[bool]] | None = None,
        record_progress: Callable[[str, str, dict[str, Any]], Awaitable[bool]] | None = None,
    ) -> None:
        self.run_id = run_id
        self.task_id = task_id
        self.claim_token = claim_token
        self.lease_seconds = max(1, int(lease_seconds))
        self.max_runtime_seconds = max(1, int(max_runtime_seconds))
        started = claimed_at or datetime.now(UTC)
        self.started_at = started
        #: THE HARD DEADLINE — the schedule's "Max runtime".
        self.deadline = started + timedelta(seconds=self.max_runtime_seconds)
        self.expires_at: datetime = started + timedelta(seconds=self.lease_seconds)
        self.lost: bool = False
        self.lost_reason: str | None = None
        self.units_done: int = 0
        self.progress_metadata: dict[str, Any] = {}
        self.renewals: int = 0
        self.progress_writes: int = 0
        self._renew = renew
        self._record_progress = record_progress
        self._last_unit_started = time.monotonic()
        self.last_unit_seconds: float = 0.0
        self.longest_unit_seconds: float = 0.0

    # ── What the handler asks ──────────────────────────────────────────────

    @property
    def bounded(self) -> bool:
        return True

    def remaining_seconds(self, now: datetime | None = None) -> float:
        """Seconds until the hard deadline; 0 once the lease is lost."""
        if self.lost:
            return 0.0
        now = now or datetime.now(UTC)
        return max(0.0, (self.deadline - now).total_seconds())

    def stop_reason(
        self, estimated_seconds: float | None = None, *, now: datetime | None = None
    ) -> str | None:
        """Why the handler must stop NOW, or None when it may start another unit.

        ``estimated_seconds`` is how long the next unit will take; when omitted
        the longest unit seen so far (as measured between ``progress`` calls)
        stands in, scaled by ``UNIT_SAFETY_FACTOR``. A handler that has not
        reported any unit yet and gives no estimate is allowed to start — the
        deadline still bounds it, via the runner.
        """
        if self.lost:
            return f"lease lost: {self.lost_reason or 'another worker owns this run'}"
        remaining = self.remaining_seconds(now)
        need = (
            float(estimated_seconds)
            if estimated_seconds is not None
            else self.longest_unit_seconds * UNIT_SAFETY_FACTOR
        )
        if remaining <= 0.0:
            return (
                f"run ceiling reached: max_runtime_seconds={self.max_runtime_seconds} "
                f"elapsed with {self.units_done} unit(s) committed"
            )
        if need > 0.0 and need > remaining:
            return (
                f"run ceiling: {remaining:.0f}s left of max_runtime_seconds="
                f"{self.max_runtime_seconds}, the last unit took "
                f"{self.last_unit_seconds:.0f}s ({need:.0f}s needed with margin); "
                f"stopped cleanly after {self.units_done} unit(s) — raise the "
                "schedule's Max runtime if the approved budget needs more time"
            )
        return None

    async def progress(
        self, *, units_done: int, metadata: dict[str, Any] | None = None
    ) -> bool:
        """Report committed work so far. Writes it onto the ledger row under the
        claim token and renews the lease. Returns False when the lease is lost —
        the handler should stop; anything it commits after that point belongs to
        a run the ledger no longer credits to it."""
        now_mono = time.monotonic()
        self.last_unit_seconds = max(0.0, now_mono - self._last_unit_started)
        self.longest_unit_seconds = max(self.longest_unit_seconds, self.last_unit_seconds)
        self._last_unit_started = now_mono
        self.units_done = max(0, int(units_done))
        if metadata:
            self.progress_metadata = dict(metadata)
        self.progress_writes += 1
        if self._record_progress is None:
            return not self.lost
        try:
            ok = await self._record_progress(
                self.run_id, self.claim_token, self.snapshot_metadata()
            )
        except Exception:  # noqa: BLE001 — a progress write failing never breaks the work
            log.exception(
                "run %s: progress write failed; the ledger lags the work by one unit",
                self.run_id,
            )
            return not self.lost
        if not ok:
            self.mark_lost("the ledger row no longer carries this claim token")
            return False
        self.expires_at = datetime.now(UTC) + timedelta(seconds=self.lease_seconds)
        return True

    # ── What the runner drives ─────────────────────────────────────────────

    def mark_lost(self, reason: str) -> None:
        if not self.lost:
            self.lost = True
            self.lost_reason = reason

    def snapshot_metadata(self, stopped_early: str | None = None) -> dict[str, Any]:
        """The ledger-shaped view of everything reported so far. The reserved
        keys are stamped LAST so a handler's own metadata can never shadow
        them — the repeat guard reads exactly these keys back."""
        meta = dict(self.progress_metadata)
        meta[RUN_UNITS_DONE_KEY] = self.units_done
        meta[RUN_STOPPED_EARLY_KEY] = stopped_early
        meta[RUN_PROGRESS_AT_KEY] = datetime.now(UTC).isoformat()
        return meta

    async def renew(self) -> bool:
        """One heartbeat: push ``claim_expires_at`` out by one lease. Returns
        False (and marks the lease lost) when the row no longer carries our
        claim token — the sweep expired it, or another claimer took it."""
        if self._renew is None:
            return not self.lost
        ok = await self._renew(self.run_id, self.claim_token, self.lease_seconds)
        if not ok:
            self.mark_lost("the ledger row no longer carries this claim token")
            return False
        self.renewals += 1
        self.expires_at = datetime.now(UTC) + timedelta(seconds=self.lease_seconds)
        return True

    def heartbeat_interval_seconds(self) -> float:
        return max(self.lease_seconds / 3.0, MIN_HEARTBEAT_INTERVAL_SECONDS)


class NoLease(RunLease):
    """The lease a handler sees OUTSIDE a scheduled run — a user-triggered
    command, a test, an admin one-off. Unbounded and never lost: ``stop_reason``
    is always None and ``progress`` only records locally. Its existence is what
    lets a handler call ``current_run_lease()`` unconditionally."""

    def __init__(self) -> None:
        super().__init__(
            run_id="",
            task_id="",
            claim_token="",
            lease_seconds=1,
            max_runtime_seconds=1,
        )

    @property
    def bounded(self) -> bool:
        return False

    def remaining_seconds(self, now: datetime | None = None) -> float:
        return float("inf")

    def stop_reason(
        self, estimated_seconds: float | None = None, *, now: datetime | None = None
    ) -> str | None:
        return None

    async def renew(self) -> bool:
        return True


def current_run_lease() -> RunLease:
    """The lease of the scheduled run this coroutine executes under, or a
    ``NoLease`` when there is none. Never raises, never None."""
    lease = _current.get()
    return lease if lease is not None else NoLease()


def bind_run_lease(lease: RunLease | None) -> contextvars.Token[RunLease | None]:
    """Runner-side: make ``lease`` the current one for this task and its
    children (asyncio tasks copy the context at creation)."""
    return _current.set(lease)


def unbind_run_lease(token: contextvars.Token[RunLease | None]) -> None:
    _current.reset(token)


async def heartbeat_until_stopped(lease: RunLease) -> str:
    """The runner's liveness heartbeat. Renews the lease every third of it
    while the handler is alive; returns the reason it stopped:

    * ``"deadline"`` — the run ceiling (``max_runtime_seconds``) is reached; the
      runner cancels the handler and finalizes with progress preserved.
    * ``"lost"`` — a renewal found the row no longer ours (the sweep expired it
      or another claimer took over); the runner cancels the handler so it does
      not zombie on, spending money on a run the ledger has already closed.

    EVERY RENEWAL IS BOUNDED. A renewal gets one heartbeat interval to answer;
    one that errors or hangs is retried after a quarter of an interval, so three
    or four attempts fit inside a single lease. Until 2026-09-14 the renewal was
    awaited with no bound: one call stuck on a pooled connection that never
    answered froze the heartbeat forever — no retry, no log — while the handler
    kept working, and the sweep expired a LIVE run
    (``tests/test_run_lease.py::test_a_renewal_that_hangs_does_not_let_a_live_run_expire``).
    """
    interval = lease.heartbeat_interval_seconds()
    retry_after = max(MIN_HEARTBEAT_INTERVAL_SECONDS, interval / 4.0)
    wait = interval
    while True:
        remaining = lease.remaining_seconds()
        if remaining <= 0.0:
            return "deadline"
        await asyncio.sleep(min(wait, remaining))
        if lease.remaining_seconds() <= 0.0:
            return "deadline"
        try:
            renewed = await asyncio.wait_for(lease.renew(), timeout=interval)
        except asyncio.CancelledError:
            raise
        except TimeoutError:
            log.error(
                "[scheduler-lease-renewal-failed] run %s: a lease renewal did not answer "
                "within %.1fs; retrying in %.1fs (the lease lapses at %s if none lands)",
                lease.run_id,
                interval,
                retry_after,
                lease.expires_at.isoformat(),
            )
            wait = retry_after
            continue
        except Exception:  # noqa: BLE001 — retried below; a lapse is the safe direction
            log.exception(
                "[scheduler-lease-renewal-failed] run %s: lease renewal raised; retrying in "
                "%.1fs (the lease lapses at %s if none lands)",
                lease.run_id,
                retry_after,
                lease.expires_at.isoformat(),
            )
            wait = retry_after
            continue
        if not renewed:
            return "lost"
        wait = interval


__all__ = [
    "MIN_HEARTBEAT_INTERVAL_SECONDS",
    "RUN_PROGRESS_AT_KEY",
    "UNIT_SAFETY_FACTOR",
    "NoLease",
    "RunLease",
    "bind_run_lease",
    "current_run_lease",
    "heartbeat_until_stopped",
    "unbind_run_lease",
]
