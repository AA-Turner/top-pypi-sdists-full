"""CloseMixin, Run's methods: the close's body: local finalizers, delivery within the deadline, the
preempted machine's direct close, and what will never arrive."""

from __future__ import annotations
import os
import time
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ...session_marker import WIZARD_HINT
from ...artifact.storage_handlers import multipart as _multipart
from ...capture import outputs as _outputs
from ..launch import preempt as _preempt


class CloseMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _close_finalize(self, deadline: float, finalize_ceiling: float | None = None) -> None:
        """The close's local finalizers, before any delivery (see `_close`).

        ``finalize_ceiling`` (defaults to ``deadline``) bounds the LOCAL-only
        waits below (lineage hashing, the hardware collector): never the raw
        ``deadline``, so they cannot spend the reserve `_close_within` keeps
        for the drain and the terminal write (`_close_reserve`)."""
        from ...delivery.transport.deadlines import deadline_scope

        if finalize_ceiling is None:
            finalize_ceiling = deadline

        with deadline_scope(deadline):
            # Plan (f): rows held by `log(commit=False)` go out first, so the
            # drain below delivers them before the close. Never raises. Inside
            # the deadline: under sync writes this is a request, and outside it
            # a hung API held the close for the transport's own timeout (30 s)
            # before the deadline started (review of #2016). One that runs out
            # of time is journaled like any failed sync write, so it stays
            # queued ahead of the close.
            self._flush_pending_rows()
            # Disarm the hard-exit breadcrumb HERE, not in fluent.finish: every
            # close funnels through this method, including Run.__exit__ from the
            # `with probe.init(...) as run:` form the docs advertise. Reaching
            # finish() at all is this process saying it is closing its own run,
            # which is the exact negation of the crumb's claim.
            try:
                from ... import diagnostics

                diagnostics.disarm(self._client, self.id)
            except Exception:  # noqa: BLE001 -- a breadcrumb must never gate a close
                pass
            # Same statement as the disarm above, one layer out: reaching finish()
            # is this process closing its own run, so a watcher on this box has
            # nothing left to explain about it. Left registered, the entry would
            # become a vanished pid the moment the interpreter exits -- and a
            # "process disappeared" note on a run that closed itself cleanly is
            # exactly the false alarm this whole design exists to avoid.
            self._deregister_with_node_agent()
            # The resume guard's final counts (plan 2.4), queued before the drain.
            self._close_resume_span()
            # The files this run read (lineage): collected, hashed and journaled as
            # NON-blocking ops before the drain, so they ride the same flush but can
            # never hold the close.
            try:
                from ...capture import lineage as _inputs

                if _inputs.is_recording(self.id):
                    # Its wait for hashing is local, so no request deadline
                    # bounds it: at most half of what is left of
                    # `finalize_ceiling` -- never the raw deadline, or a short
                    # close (a reinit's 10 s) spent it all on hashing and
                    # queued every write (review of #2016), or under
                    # contention spent it all WAITING and left the drain no
                    # reserve at all (review of the read/write capture flake).
                    _inputs.finalize(
                        self._client,
                        self.id,
                        wait_s=min(
                            _inputs.FINISH_WAIT_S,
                            0.5 * max(0.0, finalize_ceiling - time.monotonic()),
                        ),
                    )
            except Exception:  # noqa: BLE001 -- lineage evidence never gates a close
                pass
            # Stop the hardware collector first: its final windows emit (or drop —
            # best-effort) before the close; it must never block or fail the close.
            # Within at most half of what is left of `finalize_ceiling`, like the
            # hashing wait above: a collector stuck in a hung driver call is
            # abandoned, never waited on past it, and the drain and the
            # terminal write keep time of their own (review of #2016 and of
            # the read/write capture flake).
            monitor = getattr(self, "_hw_monitor", None)
            if monitor is not None:
                try:
                    monitor.finish(timeout=0.5 * max(0.0, finalize_ceiling - time.monotonic()))
                except Exception:  # noqa: BLE001
                    pass
                self._hw_monitor = None

    def _close_within(
        self,
        status: str,
        summary: dict | None,
        *,
        strict: bool,
        timeout: float,
        deadline: float,
        verdict_sent: bool = False,
    ):
        from ...delivery.transport.deadlines import deadline_scope

        # The drain may run to the deadline minus a slice kept for the close
        # itself (the status write, or the deferred-close beacon). Computed
        # FIRST: capture and upload promotion below are local-only work like
        # `_close_finalize`'s, so they are bounded to this same reserve-aware
        # ceiling, never the raw deadline -- else they can spend the drain's
        # own reserve before the drain ever runs (`_close_reserve`).
        drain_deadline = deadline - _close_reserve(timeout)
        # D17's capture queues the run's log and sweeps its folder BEFORE the
        # drain, so the drain tries to deliver them before the terminal status;
        # they are non-blocking, so an outage leaves them queued and the run
        # still closes.
        self._finalize_capture(
            budget=min(_outputs.close_budget(), max(0.0, drain_deadline - time.monotonic()))
        )
        should_warn = status == "completed" and os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0"
        # Uploads still waiting for their credential scan become ops FIRST, on
        # this thread if nobody else is at it -- the terminal status must queue
        # BEHIND this run's uploads, never ahead of them. Local CPU, but inside
        # the deadline like the rest.
        stuck = self._promote_uploads_before_close(
            strict=strict, timeout=max(0.0, drain_deadline - time.monotonic())
        )
        with deadline_scope(drain_deadline):
            pending, dead, delivered, auth_blocked = self._drain_until(
                drain_deadline, strict=strict
            )
        uploading = self._multipart_still_uploading()
        if uploading:
            # Plan (g). Never waited on while a detached worker on durable
            # storage will carry them after this process exits: said, and the
            # worker kicked. When nothing would -- a client that sends its own
            # writes (a token passed in code, drain_interval), an outbox on a
            # disposable disk -- sent now, within the close's budget, and what
            # does not make it is recorded as a reference row before this
            # returns: the run never ends with no record of the file.
            why = _multipart.settle_reason(self._client)
            if why is None:
                _diagnostics.warn(
                    f"probe: run {self.id} closing with {len(uploading)} artifact(s) still "
                    "uploading in the background; the outbox worker finishes them and each "
                    "is live once the server has verified it. See `probe outbox status`.",
                    stacklevel=4,
                )
                try:
                    self._client._after_enqueue()
                except Exception:  # noqa: BLE001 -- a kick never fails a close
                    pass
            else:
                try:
                    with deadline_scope(drain_deadline):
                        recorded = _multipart.settle_for_close(
                            self._client, uploading, drain_deadline, why=why
                        )
                except Exception:  # noqa: BLE001 -- the close goes on
                    recorded = 0
                if recorded:
                    _diagnostics.warn(
                        f"probe: run {self.id}: {recorded} artifact(s) did not finish uploading "
                        f"before the run closed ({why}); each is recorded as a reference to "
                        "its local file.",
                        stacklevel=4,
                    )
        undelivered = len(pending) + len(stuck)
        if dead and strict:
            # Deliberately BEFORE the raise is not where the lock is released:
            # a run that refuses to close is still open, and still has to keep
            # the box claimed against an upgrade.
            raise errors.RosError(
                f"run {self.id} not closed: {len(dead)} outbox op(s) are "
                "dead-lettered — waiting cannot heal a permanent rejection; see "
                "`probe outbox status`, then `probe outbox retry`"
            )
        if undelivered and strict:
            raise errors.RosError(
                f"run {self.id} not closed: {undelivered} outbox op(s) are "
                + (
                    f"undelivered: the server refused the credential ({WIZARD_HINT})"
                    if auth_blocked
                    else f"undelivered after {timeout:g}s"
                )
                + " — see `probe outbox status`, fix or `probe outbox retry`, then finish again"
            )
        # What the record must say about data that will never arrive (plan
        # 0.1/0.2): dead letters (the server refused them) and dropped writes
        # (they never reached the outbox at all).
        # The warnings that say so are printed AFTER the close, and say "marked"
        # only when the close carrying the marker was actually recorded.
        accounting: dict[str, Any] = {}
        if dead:
            accounting["dead_lettered"] = len(dead)
        dropped = max(
            0, int(getattr(self._client, "dropped_writes", 0) or 0) - self._dropped_baseline
        )
        if dropped:
            accounting["dropped_writes"] = dropped
        direct = max(
            0,
            int(getattr(self._client, "direct_sends", 0) or 0)
            - int(getattr(self, "_direct_baseline", 0) or 0),
        )
        if direct:
            accounting["direct_sends"] = direct
        if verdict_sent:
            return self._close_after_verdict(
                accounting, undelivered, delivered, auth_blocked, timeout, dead=dead
            )
        with deadline_scope(deadline):
            lost_with = self._preempted_outbox_goes_with_machine() if undelivered else None
            if lost_with is not None:
                return self._close_preempted_directly(
                    status, summary, undelivered, delivered, accounting, lost_with
                )
            if undelivered:
                # Writes are still pending past the deadline: the terminal
                # status is itself DEFERRED behind them (queued, not written
                # now), so there is no "completed" claim yet for the capture
                # warning to check against -- it applies on whatever later
                # drain actually finishes this run.
                why = (
                    "the server refused this machine's credential (401/403) -- "
                    f"{WIZARD_HINT}; the queued writes deliver once it is fixed"
                    if auth_blocked
                    else f"not delivered within {timeout:g}s; the background worker "
                    "will deliver them"
                )
                _diagnostics.warn(
                    f"probe: run {self.id} closing with {undelivered} write(s) still "
                    f"queued on disk: {why}, then mark the run {status} "
                    "(probe_finish.deferred). See `probe outbox status`.",
                    stacklevel=4,
                )
                report = self._queue_deferred_finish(
                    status, summary, undelivered, accounting=accounting
                )
                report["delivered"] = delivered
                report.update(accounting)
                self._warn_unrecoverable(accounting, recorded=self._close_recorded(report))
                # The writer is exiting by definition of a deferred finish; the
                # run's claim on the box goes with it.
                self._release_run_lock()
                return report
            # AFTER the drain, BEFORE the terminal write: the drain is what
            # makes the just-journaled env_ref PATCH + code-snapshot artifact
            # server-visible, so the check observes the real state rather than
            # a stale one that reads as incomplete.
            if should_warn:
                self._warn_if_capture_incomplete()
            close_summary = summary
            if accounting:
                close_summary = _with_finish_accounting(
                    summary, {**accounting, "session_id": self.session_id}
                )
            # From here an interrupt may land after the server applied this
            # status: `_close` queues this same status then, not another.
            self._terminal_in_flight = status
            dropped_before = int(getattr(self._client, "dropped_writes", 0) or 0)
            result = self.set_status(
                status, ended_at=_now(), summary=close_summary, sync=True, strict=strict
            )
            if result is None:
                settled = self._settle_journaled_finish(
                    strict=strict,
                    deadline=deadline,
                    dropped=int(getattr(self._client, "dropped_writes", 0) or 0) > dropped_before,
                )
                self._warn_unrecoverable(accounting, recorded=self._close_recorded(settled))
                return settled
        self._warn_unrecoverable(accounting, recorded=True)
        # ONLY on success, and deliberately not in a `finally`.
        #
        # If set_status raised, the run is not closed: the caller may catch the
        # error and keep training, and releasing here would hand auto-update a
        # green light over a live process. Holding costs nothing -- an flock is
        # bound to this process and the kernel frees it at exit regardless, so
        # the failure mode of keeping it is "protected slightly too long", while
        # the failure mode of dropping it is an upgrade landing mid-run.
        self._release_run_lock()
        return result

    def _preempted_outbox_goes_with_machine(self) -> str | None:
        """Why this close must not queue behind its undelivered writes: a
        SIGTERM is ending the process and the outbox is on a throwaway disk
        (`ephemeral`), so the queue -- and the worker that would drain it --
        goes with the machine. None otherwise, including when unknown."""
        if _preempt.ending() is None:
            return None
        try:
            from ..launch import ephemeral

            where = ephemeral.describe(str(self._client.journal.dir))
        except Exception:  # noqa: BLE001 -- unknown: queue it, as any close
            return None
        if where.get("durable", True):
            return None
        return str(where.get("reason") or "a disposable disk")

    def _close_preempted_directly(
        self,
        status: str,
        summary: dict | None,
        undelivered: int,
        delivered: int,
        accounting: dict,
        lost_with: str,
    ) -> dict:
        """The close of a SIGTERMed run whose outbox dies with the machine:
        sent NOW, marking what will never arrive, instead of queued behind it
        (`_queue_deferred_finish`) for a worker that dies with the container
        -- or behind a draining lease beat that would keep a dead run live for
        an hour. What is still queued may yet go out before the machine does."""
        accounting = {**accounting, "undelivered": undelivered, "outbox": lost_with}
        close_summary = _with_finish_accounting(
            summary, {**accounting, "session_id": self.session_id}
        )
        preempted = _preempt.ending()
        if preempted is not None and preempted.exit_code is not None:
            # The exit span `finish()` queued sits behind that same data: sent
            # directly too (the same row, so a queued copy landing is harmless).
            from ... import fluent

            fluent._write_exit_span(
                self, -preempted.signum, "signal", status, extra=preempted.facts(), direct=True
            )
        self._terminal_in_flight = status
        result = self.set_status(
            status, ended_at=_now(), summary=close_summary, sync=True, strict=False
        )
        _diagnostics.warn(
            f"probe: run {self.id} closed {status} on SIGTERM with {undelivered} write(s) "
            f"undelivered: the outbox is on {lost_with}, which goes with this machine "
            "(probe_finish.undelivered).",
            stacklevel=5,
        )
        self._warn_unrecoverable(accounting, recorded=getattr(self, "_closed_status", None) is not None)
        self._release_run_lock()
        return {
            "finish_queued": result is None,
            "delivered": delivered,
            "remaining": undelivered,
            **accounting,
        }

    def _warn_unrecoverable(
        self,
        accounting: dict,
        *,
        recorded: bool,
        unmarked_because: str = "its close was not recorded either",
    ) -> None:
        """Say what of this run will never arrive, AFTER the close, and say it
        is marked on the run only when the close carrying the marker landed or
        was queued (review of #2014: a cap-refused close had already printed
        "marked")."""
        where = (
            "the run is marked {key}={n}"
            if recorded
            else f"the run could NOT be marked: {unmarked_because}"
        )
        dead = accounting.get("dead_lettered")
        if dead:
            _diagnostics.warn(
                f"probe: {dead} of run {self.id}'s writes were permanently rejected "
                "by the server (dead-lettered); "
                + where.format(key="probe_finish.dead_lettered", n=dead)
                + ". See `probe outbox status`, then `probe outbox retry`.",
                stacklevel=5,
            )
        dropped = accounting.get("dropped_writes")
        if dropped:
            _diagnostics.warn(
                f"probe: {dropped} write(s) for run {self.id} were dropped before they "
                "reached the outbox (full or unwritable, or logged while probe.init() was "
                "still opening this run -- see the earlier warning; "
                "counted in this process only); "
                + where.format(key="probe_finish.dropped_writes", n=dropped)
                + ". See `probe outbox status`.",
                stacklevel=5,
            )

    def _close_after_verdict(
        self,
        accounting: dict,
        undelivered: int,
        delivered: int,
        auth_blocked: bool,
        timeout: float,
        *,
        dead: list | None = None,
    ):
        """The end of a close whose verdict `set_status` had already sent.

        That verdict stands, so nothing terminal is written or queued here: a
        second terminal PATCH overwrote it with this call's guess (`execute()`
        closed a run `failed` from its child's exit code, and the `finish()`
        after it re-closed it `completed`). The rest of the close has run --
        crumb disarmed, lineage and hardware finalized, capture swept, this
        run's writes drained -- because returning early left the crumb armed,
        and the next `probe.init()` on the host then filed a `hard_exit` on a
        run that had closed cleanly (review of #2016). What could not be
        delivered stays queued for the detached worker, as after any close;
        dead letters and dropped writes are warned about, but cannot be
        marked on a run whose close already went out without them.

        "Sent" is checked, not assumed: a `set_status` that fail-opened into
        the journal only QUEUED its verdict, and the server may then refuse
        it for good. That close was rejected -- the run is still open, and the
        reaper will call it crashed -- and is reported as such, the way a
        `finish()` whose own terminal write was refused reports it
        (`_settle_journaled_finish`), never as a verdict already sent
        (review of #2016).
        """
        terminal = self._latest_terminal_patch()
        verdict = self._closed_status
        if terminal is not None and terminal[0] == "failed":
            # The dead letter IS the close; only the rest is data it lost.
            data_dead = [p for p in (dead or []) if p != terminal[1]]
            if data_dead:
                accounting["dead_lettered"] = len(data_dead)
            else:
                accounting.pop("dead_lettered", None)
            _diagnostics.warn(
                f"probe: run {self.id} not closed: the terminal status was rejected and "
                "dead-lettered — see `probe outbox status`, then `probe outbox retry`. "
                "The server will close the run when it goes quiet.",
                stacklevel=5,
            )
            if undelivered:
                self._client.hand_off_delivery()
            self._warn_unrecoverable(
                accounting, recorded=False, unmarked_because="its close was rejected too"
            )
            # Not released: the run is not closed (as in `_settle_journaled_finish`).
            return {
                "finish_queued": False,
                "delivered": delivered,
                "remaining": undelivered,
                "close_rejected": True,
                **accounting,
            }
        queued = terminal is not None  # still pending: queued, not yet sent
        if undelivered:
            why = (
                f"the server refused this machine's credential (401/403) -- {WIZARD_HINT}"
                if auth_blocked
                else f"not delivered within {timeout:g}s; the background worker will deliver them"
            )
            state = f"closing {verdict} (queued)" if queued else f"already {verdict}"
            _diagnostics.warn(
                f"probe: run {self.id} is {state}; {undelivered} of its write(s) are "
                f"still queued on disk: {why}. See `probe outbox status`.",
                stacklevel=5,
            )
            self._client.hand_off_delivery()
        self._warn_unrecoverable(
            accounting,
            recorded=False,
            unmarked_because=(
                f"its close ({verdict}) was already queued without the marker"
                if queued
                else f"its close ({verdict}) was already sent"
            ),
        )
        self._release_run_lock()
        if undelivered or accounting:
            return {
                "finish_queued": False,
                "delivered": delivered,
                "remaining": undelivered,
                **accounting,
            }
        return self._data
from probe.sdk.run.closing.drain import _close_reserve  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.metrics.values import _now  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.summary import _with_finish_accounting  # noqa: E402 -- pieces need each other; the front door loads this one first
