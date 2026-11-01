"""CloseDrainMixin, Run's methods: drain this run's queued ops within the close deadline, promoting
its waiting uploads first."""

from __future__ import annotations
import os
import time
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from probe.sdk.run.handle import _UNSET


#: How long `finish()` waits for another process (the worker) to finish scanning
#: this run's queued uploads. Scanning is local and takes seconds; this only
#: bounds a promoter that hung while holding an item.
WAITING_PROMOTE_TIMEOUT = 300.0

#: The DEFAULT deadline for `finish()` (plan 0.2, decision D1), in seconds;
#: ``flush_timeout=`` or ``PROBE_FINISH_TIMEOUT_SEC`` overrides it.
#:
#: The default close used to be a hard barrier that made ONE delivery attempt
#: and raised (PR #1679 gave it a 15 s retry, and it still raised after). A
#: close that raises over telemetry breaks the maintainer rule written in
#: `_warn_if_capture_incomplete` -- "nothing, opt-in or otherwise, may block a
#: run" (2026-08-06, argued in design PR #1680) -- and live it raised on 4 of 6
#: ten-step runs whenever the hardware rail's write collided with the drain
#: (a 503 "concurrent telemetry write"). Now every close retries to this
#: deadline, then queues its terminal status BEHIND whatever is still
#: undelivered (`_queue_deferred_finish`) and returns. 600 s outlasts a deploy
#: or an ingress restart and stays under the server's 900 s silence reaper,
#: which the heartbeat keeps at bay while the close waits.
FINISH_TIMEOUT_DEFAULT_SECONDS = 600.0

#: The close loop's waits (first, ceiling), fed to `durable.backoff_delays`
#: like every other durable retry loop (plan 0.6). Short on purpose: someone is
#: waiting on this one, and the first retry of a blip should land in half a
#: second, while the 4 s ceiling keeps a long deadline from hammering a sick
#: server (PR #1679's numbers).
_FINISH_BACKOFF = (0.5, 4.0)

#: The part of the deadline kept back from the drain for the close ITSELF --
#: the final status write, or the deferred-close beacon -- so a drain that runs
#: to the deadline does not leave the terminal write no time at all. At most a
#: quarter of a short deadline.
_CLOSE_RESERVE_SECONDS = 5.0


def _close_reserve(timeout: float) -> float:
    """The slice of the close's budget that must reach the drain and the
    terminal write untouched: every LOCAL-only step before the drain
    (lineage hashing, the hardware collector, capture, upload promotion) is
    bounded to ``deadline - this``, never the raw deadline, so a close whose
    local finalizers spend their whole individual allowance under contention
    still leaves this reserve for delivery. Without it, a SIGTERM close with
    read/write capture on could spend the ENTIRE budget hashing and stopping
    the hardware collector -- both individually bounded to "half of what's
    left" -- and die with nothing sent at all: the run stayed `running`
    (review of the read/write capture flake, #2124 on #2119's budget)."""
    return min(_CLOSE_RESERVE_SECONDS, 0.25 * timeout)


#: Longest single wait for the drain lock before looking again at what of this
#: run is still queued: the lock's holder (the detached worker, mid-pass) may be
#: delivering exactly those ops.
_FINISH_LOCK_POLL_SECONDS = 1.0


class CloseDrainMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _queued_ops(self, rows) -> list[dict]:
        """This run's ops that are allowed to hold its close.

        ``blocking=False`` ops are excluded: they are best-effort by contract
        (diagnostics), and letting one dead-letter into this set would keep a
        run `running` for the reaper instead of closing it `failed`.
        """
        return [op for _, op in rows if op.get("run_ref") == self.id and op.get("blocking", True)]

    @staticmethod
    def _resolve_finish_timeout(flush_timeout: float | None, *, default: Any = _UNSET) -> float | None:
        """The close's deadline in seconds: ``flush_timeout``, else
        ``PROBE_FINISH_TIMEOUT_SEC``, else ``default`` -- by default
        `FINISH_TIMEOUT_DEFAULT_SECONDS` (600), read at call time; `execute()`
        passes None to keep its one-pass delivery of captured outputs. Read
        ONCE per close, so a mid-close env change cannot extend it. Negative
        means zero: queue everything, wait for nothing."""
        if default is _UNSET:
            default = FINISH_TIMEOUT_DEFAULT_SECONDS
        if flush_timeout is not None:
            return max(float(flush_timeout), 0.0)
        raw = os.environ.get("PROBE_FINISH_TIMEOUT_SEC")
        if raw:
            try:
                return max(float(raw), 0.0)
            except ValueError:
                # Read inside a close: a plain warnings.warn raises under -W error.
                _diagnostics.warn(
                    f"ignoring malformed PROBE_FINISH_TIMEOUT_SEC={raw!r}; "
                    "expected seconds as a float",
                    stacklevel=3,
                )
        return default

    def _drain_until(
        self, drain_deadline: float, *, strict: bool
    ) -> tuple[list, list, int, bool]:
        """Deliver THIS run's ops until none is left or ``drain_deadline``.

        Returns ``(pending, dead, delivered, auth_blocked)``: this run's
        blocking ops still queued, its dead letters, how many ops the loop
        delivered, and whether it stopped on a refused credential.

        Grown from PR #1679's ``_barrier_drain_with_retry`` (Mahit), which gave
        the old one-attempt hard barrier a bounded retry: a two-second blip --
        a pod rolling, a DNS hiccup, a 502 that recovers at once -- must not
        decide a run whose data is durable on disk. What holds it to its
        deadline now (plan 0.6):

          * the caller wraps it in `transport.deadline_scope`, so every request
            -- each attempt's timeout and every transport-level retry -- ends by
            ``drain_deadline``, not merely each PASS;
          * the drain lock is polled, at most `_FINISH_LOCK_POLL_SECONDS` at a
            time, never blocked on: a detached worker mid-pass cannot hold the
            close past its deadline, and between polls the loop looks at what
            of this run is still queued, since that worker may be delivering it;
          * while it polls, the close says it is waiting (`Journal.drain_want`),
            and a pass gives the lock up at its next op; a pass also lets go of
            it while an upload of its is on the network, keeping only that
            run's lock (#3618). So the close sends its own run's writes in
            seconds behind a 10k-op backlog or a 30 MiB upload of another run,
            where it used to wait out whole passes (~400 s in the swarm);
          * the waits come from `durable.backoff_delays` (`_FINISH_BACKOFF`),
            at least the server's ``Retry-After`` when it named one, and never
            past the deadline.

        Counts only THIS run's ops (`Journal.run_ops`): each op file is parsed
        once, not the whole machine-wide queue after every pass.

        ``strict`` returns at the first dead letter: a strict close refuses on
        it, and waiting cannot heal a permanent rejection (#1679's rule). A
        default close keeps delivering the rest and reports the dead letters on
        the run instead.

        A refused credential (401/403) on THIS run's pass returns at once: only
        a login fixes it, so waiting out the deadline was dead time (review of
        #2011: a 401 held the close 300 s where main raised in 0.01 s). The
        signal is the run-scoped pass's own `auth_blocked`, never the
        machine-wide `auth_blocked_since` in status.json, which a NEIGHBOUR
        run's expired token could have written (#1679).
        """
        from ....foundation.durable import durable

        mine = self._client.journal.run_ops(self.id)
        # Writes of this run queued under ANOTHER credential (#2035) sit in
        # their own queue, where this process cannot deliver them and this
        # queue's order cannot see them. Counted, never waited on: a close is
        # then deferred, and the drain keeps a queued close behind them
        # (#2041 round 3: the close landed first, 5 of 5).
        elsewhere = self._client.journal.run_ops_elsewhere(self.id, min_epoch=self.write_epoch)
        delays = durable.backoff_delays(None, _FINISH_BACKOFF)
        delivered = 0
        while True:
            report = None
            left = drain_deadline - time.monotonic()
            try:
                report = self._client._drain_for_close(
                    self.id, lock_timeout=max(0.0, min(left, _FINISH_LOCK_POLL_SECONDS))
                )
                delivered += report.delivered
            except Exception:  # noqa: BLE001 -- drain records last_error itself
                pass
            pending = mine.pending()
            dead = mine.failed()
            auth_blocked = report is not None and report.auth_blocked
            if not pending:
                return elsewhere.pending(), dead, delivered, auth_blocked
            if (strict and dead) or auth_blocked:
                return pending, dead, delivered, auth_blocked
            left = drain_deadline - time.monotonic()
            if left <= 0:
                return pending, dead, delivered, False
            if report is not None and report.lock_busy:
                # Already waited on the lock; its holder may be delivering ours.
                continue
            if report is not None and report.delivered:
                delays = durable.backoff_delays(None, _FINISH_BACKOFF)  # progress: stay prompt
            time.sleep(
                durable.honor_retry_after(
                    next(delays),
                    None if report is None else report.retry_after,
                    ceiling=left,
                )
            )

    def _has_queued_tag_write(self) -> bool:
        """Whether this run has a PATCH carrying `tags` still in the queue.

        `set_tags` replaces the WHOLE list, so a queued one and a server read
        disagree by construction, and FIFO makes the queued write land first.
        Anything derived from the server's current tags is therefore stale the
        moment one is pending.
        """
        try:
            for op in self._queued_ops(self._client.journal.pending()):
                if op.get("method") == "PATCH" and "tags" in (op.get("body") or {}):
                    return True
        except Exception:  # noqa: BLE001 -- a probe may never break a close
            return True  # unknown means assume conflict; skipping the beacon is cheap
        return False

    def _promote_uploads_before_close(self, *, strict: bool, timeout: float | None = None) -> list[str]:
        """Turn this run's waiting uploads into queued ops (see
        `Journal.promote_waiting`) within ``timeout``; returns the ones still
        waiting that hold the close. ``strict`` raises when one cannot be
        prepared; otherwise the close stays fail-open, as `set_status` promises
        -- a close must never replace the traceback of a run that is failing --
        and the caller counts them as undelivered: a close queued behind them
        waits for them (the drain holds a run's later ops behind its waiting
        uploads)."""
        if timeout is None:
            # Inside a close's `deadline_scope` (the terminal `set_status` that
            # finish() makes), what is left of that deadline bounds this too.
            from ...delivery.transport.deadlines import deadline_remaining

            timeout = deadline_remaining(WAITING_PROMOTE_TIMEOUT)
        stuck = self._client.journal.promote_for_close(
            self.id, timeout=max(0.0, min(WAITING_PROMOTE_TIMEOUT, timeout))
        )
        if stuck and strict:
            raise errors.RosError(
                f"run {self.id} not closed: {len(stuck)} queued upload(s) could not be "
                "prepared for delivery (credential scan) — see `probe outbox status`, "
                "then close again"
            )
        return stuck

    def _queued_ops_any(self, rows) -> bool:
        """Any op of this run still queued, blocking or not."""
        return any(op.get("run_ref") == self.id for _, op in rows)
