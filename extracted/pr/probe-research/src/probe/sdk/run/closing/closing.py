"""ClosingMixin, Run's methods: run.finish and the context manager -- close once, settle, choose
the interrupted status."""

from __future__ import annotations
import threading
import time
from typing import TYPE_CHECKING, Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ..launch import preempt as _preempt

if TYPE_CHECKING:  # Run only in annotations: importing it here would loop back into run.py
    from ..run import Run

#: `Run._finish_result` while a close is running (see `Run.finish`).
_FINISHING: Any = object()


class ClosingMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _close_on_interrupt(self, status: str, summary: dict | None, *, strict: bool) -> None:
        """Ctrl-C landed inside the close. Whatever of this run is on disk
        stays there; make sure the run still gets its verdict and something
        delivers it, then let the interrupt propagate.

        Only local work: journal the terminal status behind the queued data (no
        beacon -- that is a network round trip the person just asked to skip)
        and hand the journal to the detached worker. A strict close queues no
        verdict (it promises not to close over undelivered data), but still
        hands off the data. Never raises: the caller re-raises the interrupt.
        """
        try:
            if getattr(self, "_closed_status", None) is None and not strict:
                pending = len(self._client.journal.run_ops(self.id).pending())
                report = self._queue_deferred_finish(status, summary, pending, beacon=False)
                self._finish_result = report
                self._release_run_lock()
            else:
                self._client.hand_off_delivery()
        except BaseException:  # noqa: BLE001 -- the interrupt is what must propagate
            pass

    def finish(
        self,
        status: str = "completed",
        *,
        summary_metrics: dict | None = None,
        summary: dict | None = None,
        flush_timeout: float | None = None,
        strict: bool | None = None,
        wait: bool = True,
    ):
        """Close the run, and (``wait``, the default) wait for the background worker to deliver
        everything of it (D1, D2): the run row once it all landed; `DeliveryIncomplete`
        (`probe.sdk.delivery.outbox`) when some of it cannot be (refused, login refused, set
        aside after a stall, server unreachable for 10 minutes, no worker can run). Slowness
        never raises: while writes move it prints a progress line every ~5 s, and Ctrl-C stops
        waiting (the worker keeps sending). ``wait=False`` queues the close behind the data and
        returns at once. ``flush_timeout`` (or ``PROBE_FINISH_TIMEOUT_SEC``) caps the wait; past
        it the close stays queued, as with ``wait=False``. ``strict`` is accepted and no longer
        needed: loss always raises. A `with probe.init()` block that is already raising is never
        masked (`Run.__exit__`). This path is a client on the default transport; one with an
        injected transport (hosted MCP, tests) cannot hand its writes to the worker and closes as
        described below.

        Injected transport. Outside ``strict`` it NEVER raises over delivery.

        This run's journaled writes are drained, retried with backoff, to ONE
        deadline -- ``flush_timeout``, else ``PROBE_FINISH_TIMEOUT_SEC``, else
        600 s (`FINISH_TIMEOUT_DEFAULT_SECONDS`) -- that bounds everything the
        close does: upload promotion, the drain-lock wait, each request, the
        final status write (plan 0.2/0.6). Then:

        * everything delivered: the terminal status is written and the run
          row returned -- as before;
        * writes still undelivered at the deadline: they stay durable on disk,
          the terminal status is journaled BEHIND them
          (``_queue_deferred_finish``, stamped ``probe_finish.deferred``), a
          warning names the count, and a report ``{finish_queued, delivered,
          remaining}`` is returned instead of the row. FIFO is the correctness
          guarantee: the run can never read terminal ahead of its own data;
        * writes the server permanently rejected (dead letters): a warning, and
          the run closes with ``probe_finish.dead_lettered = N`` on it, so a
          ``completed`` run with missing data says so on the RECORD, not only
          on a terminal that has scrolled away;
        * writes this client DROPPED before they reached the outbox (full, or
          unwritable -- `Client.dropped_writes`): a warning, and
          ``probe_finish.dropped_writes = N`` on the run the same way (plan 0.1).

        So a run with undelivered or dead-lettered data never reads
        ``completed`` without ``probe_finish.deferred`` or
        ``probe_finish.dead_lettered``. Red team's original finding -- finish()
        "used to discard the drain outcome and close 'completed' over silently
        missing data" -- is answered by the marker, not by refusing to close:
        refusing broke the standing rule that nothing may block a run
        (maintainer decision 2026-08-06, `_warn_if_capture_incomplete`; argued
        in design PR #1680), and live it failed 4 of 6 ten-step runs on one
        503 from a colliding write.

        ``strict`` (default: the client's ``not fail_open``) keeps the old
        barrier for a caller who wants delivery or an exception: dead letters
        raise at once, anything still undelivered at the deadline raises, and
        the run is NOT closed. `probe run end` is the CLI's barrier.

        A completion WARNING (never a gate) fires when ``status == "completed"``
        and capture was not opted out (``PROBE_AUTO_SNAPSHOT`` != ``"0"``). A
        run finishing "failed" (the body already raised, or the caller is
        being honest about a bad outcome) never warns -- there is no claim of
        completeness to caveat, and ``Run.__exit__`` depends on this so a
        body's real exception is never masked by a capture warning on the way
        out.

        The warning's ``check_run`` reads the run BUNDLE -- a plain GET,
        never the journal -- so under ``async_writes`` the env_ref PATCH and
        code-snapshot artifact ``snapshot()`` just journaled are not yet
        server-visible. The check must observe the very capture this finish()
        is about to claim, so it runs AFTER the drain (below), never before:
        checking first would make a spurious warning fire on data that is
        durable on disk and about to be delivered, not actually missing.
        """
        # IDEMPOTENT (#2011): a repeat returns the first close's answer; a close running in another thread
        # is waited for; the same thread re-entering gets ``{"finish_in_progress": True}`` (DESIGN.md).
        lock = self.__dict__.setdefault("_finish_lock", threading.Lock())
        # A SIGTERM (`preempt`): whoever closes, the run ends `failed`, marked preempted, in its budget.
        preempted = _preempt.ending()
        with lock:
            previous = getattr(self, "_finish_result", _UNSET)
            if previous is _UNSET:
                if preempted is not None:
                    status = "failed"
                    flush_timeout = preempted.close_timeout(
                        self._resolve_finish_timeout(flush_timeout)
                    )
                timeout = self._resolve_finish_timeout(flush_timeout)
                # Only a limit someone set caps the wait on the worker (D2): an argument, the
                # env, a SIGTERM's grace. The 600 s default bounds the close's local work only.
                limit = self._resolve_finish_timeout(flush_timeout, default=None)
                wait_limit = None if limit is None else time.monotonic() + limit
                self._finish_result = _FINISHING
                self._finish_done = threading.Event()
                self._finish_thread = threading.get_ident()
                self._finish_deadline = time.monotonic() + timeout
        if previous is _FINISHING:
            done = getattr(self, "_finish_done", None)
            if done is not None and getattr(self, "_finish_thread", None) != threading.get_ident():
                left = max(0.0, (self._finish_deadline or 0.0) - time.monotonic())
                done.wait(left + _CLOSE_RESERVE_SECONDS)
            result = self._finish_result
            return {"finish_in_progress": True} if result is _FINISHING else result
        if previous is not _UNSET:
            return previous
        close_summary = _one_summary(summary_metrics, summary)
        if preempted is not None:
            close_summary = _with_finish_accounting(close_summary, preempted.facts())
            if preempted.exit_code is not None:
                # The exit code as the crash email reads it: negative means died on that signal (DESIGN.md).
                from ... import fluent

                fluent._write_exit_span(
                    self, -preempted.signum, "signal", status, extra=preempted.facts()
                )
        try:
            result = self._close(
                status,
                summary=close_summary,
                flush_timeout=timeout,
                strict=strict,
                wait=wait,
                wait_limit=wait_limit,
            )
        except BaseException:
            if self._finish_result is _FINISHING:
                # Nothing was closed or queued: a later finish() may try again.
                # Otherwise the verdict went out; a repeat returns None.
                self._finish_result = (
                    _UNSET if getattr(self, "_closed_status", None) is None else None
                )
            self._finish_done.set()
            if self._finish_result is not _UNSET:
                self._settled()
            raise
        self._finish_result = result
        self._finish_done.set()
        # Delivery trouble held back by the notices' 5-minute limit, said once
        # at the close (plan 1.7). Never raises.
        notices = getattr(self._client, "_notices", None)
        if notices is not None:
            notices.summary()
        # And the process's delivery counts, to our telemetry (plan 1.12).
        report = getattr(self._client, "_report_delivery", None)
        if report is not None:
            report(final=True)
        # Last: it may close this run's client (a `create_new` run's).
        self._settled()
        return result

    def _settled(self) -> None:
        """This handle's close is over: run the one `_after_finish` callback."""
        from ..launch import open_runs as _open_runs

        # One run fewer open here: workers may be bound to the one left (F5).
        _open_runs.closed(self)
        callback, self._after_finish = getattr(self, "_after_finish", None), None
        if callback is not None:
            try:
                callback()
            except Exception:  # noqa: BLE001 -- bookkeeping after a close never raises
                pass

    def _close(
        self,
        status: str,
        *,
        summary: dict | None,
        flush_timeout: float | None,
        strict: bool | None,
        wait: bool = True,
        wait_limit: float | None = None,
    ):
        """`finish()`'s body, run at most once per handle (see `finish`)."""
        # ONE deadline, taken FIRST, for everything the close does (plan 0.6):
        # the lineage and hardware finalizers below, capture, promotion, the
        # drain, and the terminal write.
        timeout = self._resolve_finish_timeout(flush_timeout)
        strict = (not self._client.fail_open) if strict is None else bool(strict)
        close_started = time.monotonic()
        deadline = close_started + timeout
        # `set_status` already sent this run's verdict (`execute()`'s finalize,
        # `probe run end`, a caller's own call): the close below still runs --
        # crumb, lineage, hardware, capture, drain -- and only the terminal
        # write is skipped (`_close_within`).
        verdict_sent = getattr(self, "_closed_status", None) is not None
        # `_close_within` keeps `_close_reserve(timeout)` back for the drain
        # and the terminal write: `_close_finalize`'s own local-only work must
        # never spend it (see `_close_reserve`).
        finalize_ceiling = deadline - _close_reserve(timeout)
        try:
            self._close_finalize(deadline, finalize_ceiling)
        except (KeyboardInterrupt, SystemExit) as interrupt:
            # A Ctrl-C (or a SystemExit) BEFORE the drain started: the
            # finalizers can take seconds (hashing the files the run read,
            # joining the hardware collector), and an interrupt there
            # left no status queued at all, so the run sat `running` until the
            # reaper called it crashed (lane E, building on #2011). Nothing was
            # delivered and the lineage/hardware tail was cut short, so the
            # verdict is the interrupt's own -- `canceled` for Ctrl-C, a
            # SystemExit's code otherwise -- queued behind the data and handed
            # to the worker like the later window below.
            self._close_on_interrupt(
                self._interrupted_status(interrupt, status), summary, strict=strict
            )
            # Cut short before it stopped the hardware collector (read capture
            # hashing comes first): it must not go on sampling a closed run.
            monitor = getattr(self, "_hw_monitor", None)
            if monitor is not None:
                try:
                    monitor.request_stop()
                except BaseException:  # noqa: BLE001 -- the interrupt must propagate
                    pass
            raise
        # A Ctrl-C during the close (it may wait up to the deadline) must not
        # leave the run with no terminal status queued and nothing handed to
        # the worker: the reaper would call it `crashed` (review of #2011).
        # SystemExit too: Lightning turns SIGTERM into a code-less SystemExit,
        # and a preempted job must still queue its verdict (re-review of #2011).
        try:
            return self._close_within(
                status,
                summary,
                strict=strict,
                timeout=timeout,
                deadline=deadline,
                verdict_sent=verdict_sent,
                wait=wait,
                wait_limit=wait_limit,
            )
        except (KeyboardInterrupt, SystemExit):
            # Once the terminal write is on its way the server may already have
            # applied it, and the response is what the interrupt cut off. The
            # status queued then is THAT one again -- an idempotent replay (the
            # server acts on a status only when it changes) -- never a
            # different one: a reinit's `canceled` queued there landed later
            # and overwrote the `completed` already applied (review of #2016).
            sent = getattr(self, "_terminal_in_flight", None)
            self._close_on_interrupt(
                sent or getattr(self, "_status_on_interrupt", None) or status,
                summary,
                strict=strict,
            )
            raise

    def _interrupted_status(self, interrupt: BaseException, requested: str) -> str:
        """The verdict for a close interrupted before it delivered anything:
        read the way `Run.__exit__` reads an ending. Ctrl-C is ``canceled``;
        a SystemExit is its code, and a clean one (Lightning's code-less
        SIGTERM) takes what `note_exit` recorded, else the status asked for.
        A close its caller did not choose (a reinit closing the previous run)
        sets `_status_on_interrupt`, which wins in both windows."""
        override = getattr(self, "_status_on_interrupt", None)
        if override:
            return override
        if isinstance(interrupt, KeyboardInterrupt):
            return "canceled"
        verdict, _ = _status_for_system_exit(
            getattr(interrupt, "code", None), interrupt.__context__
        )
        if verdict != "completed":
            return verdict
        noted = getattr(self, "_noted_exit", None)
        return noted[0] if noted else requested

    # -- context manager ----------------------------------------------------
    def __enter__(self) -> "Run":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Close the run, but never let closing it displace the body's failure.

        This block is the whole reason the campaign's workers died: `finish()`
        runs inside an exception handler, so anything it raises REPLACES the
        traceback the researcher actually needs. Making `set_status` fail-open
        fixed the transport case and then the dead-letter raise reopened it from
        a different direction -- a permanently rejected terminal PATCH (a 422,
        not a blip) turned `1/0` into "the terminal status was dead-lettered".

        So the rule lives here, once, where it cannot be reopened again: when
        the body already failed, a close failure is downgraded to a warning and
        the original exception propagates. An explicit `run.finish()` still
        raises -- there is no other error to protect, and a caller who asked to
        close deserves to hear that it did not happen.

        BaseException, not Exception. `finish()` sleeps and does blocking
        network I/O on an unbounded drain, so a Ctrl-C landing in it is not
        exotic -- it is the likely case: the body fails, finish() hangs on a
        dead API, the researcher interrupts, and the real error is gone. The
        warning itself goes through the non-raising channel, because the
        previous version of this handler used `warnings.warn` and reopened the
        bug a third time under `-W error`.
        """
        # The same reading of the ending as `fluent`'s process hooks, which
        # now stand down for a run this block closed: a SystemExit is its code
        # (`sys.exit(0)` is not a failure) and Ctrl-C is `canceled`, both when
        # it escapes the block and when it is in flight behind a SystemExit.
        cause: BaseException | None = None
        exit_code = 0
        if exc is None:
            status = "completed"
        elif (
            isinstance(exc, SystemExit)
            and exc.code is None
            and getattr(self, "_noted_exit", None) is not None
        ):
            # Lightning on SIGTERM: on_exception -> note_exit("failed", exc),
            # then a SystemExit with no code, which alone reads as success.
            status, noted = self._noted_exit
            if status == "failed":
                cause = noted
        elif isinstance(exc, SystemExit):
            status, exit_code = _status_for_system_exit(exc.code, exc.__context__)
            # Hydra's shape: the traceback it swallowed is the crash report,
            # never the SystemExit itself.
            if status == "failed" and isinstance(exc.__context__, Exception):
                cause = exc.__context__
        elif isinstance(exc, KeyboardInterrupt):
            status = "canceled"
        else:
            status, cause = "failed", exc
        if getattr(self, "_closed_status", None) is not None or self._finish_called():
            # The run was closed inside the block -- a second probe.init()
            # replaced it (reinit), or `run.finish()` / `set_status` ran. Its
            # verdict stands, and what ended the block after that is not its
            # ending: no exit code or crash report is filed on it (the
            # exception still propagates). finish() below returns the first
            # close's answer, or finishes the cleanup a bare set_status left.
            exit_code, cause = 0, None
        if exit_code:
            try:
                from ... import fluent

                fluent._write_exit_span(self, exit_code, "SystemExit", status)
            except BaseException:  # noqa: BLE001 -- evidence is best effort
                pass
        if cause is not None:
            try:
                from ... import diagnostics

                diagnostics.report_exception(self, cause)
            except BaseException:  # noqa: BLE001 -- even an interrupted report is best effort
                pass
        try:
            self.finish(status)
        except BaseException as close_error:  # noqa: BLE001
            if exc_type is None:
                raise
            _diagnostics.warn(
                f"run {self.id} did not close cleanly "
                f"({_diagnostics.describe(close_error)}); re-raising the "
                "original error from the with-block instead. See "
                "`probe outbox status`."
            )
from probe.sdk.run.closing.drain import _CLOSE_RESERVE_SECONDS, _close_reserve  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.closing.status import _status_for_system_exit  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.handle import _UNSET  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.summary import _one_summary, _with_finish_accounting  # noqa: E402 -- pieces need each other; the front door loads this one first
