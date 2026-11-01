"""DrainerMixin, Client's methods: who drains a client's queue (detached worker or in-process
exporter), kicked after an enqueue and at exit."""

from __future__ import annotations
import time


def _at_exit(callback) -> None:
    """`atexit.register`, by a name tests can point elsewhere: a callback that
    outlives pytest runs after every monkeypatch is undone."""
    import atexit

    atexit.register(callback)


class DrainerMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _promote_waiting_at_exit(self, run_ref: str) -> None:
        """Make sure an upload this process queued for a background credential
        scan is promoted even if no worker could be started (a frozen or
        embedded interpreter): at exit, promote what is still waiting for THIS
        process's runs -- not other processes' in a shared journal -- within
        `_EXIT_PROMOTE_SECONDS`, then kick delivery the way `_kick_drainer`
        would. Registered once. Normally a no-op: the worker or `finish()` got
        there first."""
        runs = self.__dict__.setdefault("_waiting_exit_runs", set())
        runs.add(run_ref)
        if len(runs) > 1 or getattr(self, "_waiting_exit_armed", False):
            return
        self._waiting_exit_armed = True
        journal_dir = str(self.journal.dir)
        spawn = self._default_transport and self._auto_drain
        budget = self._EXIT_PROMOTE_SECONDS

        def promote() -> None:
            from .. import outbox as outbox_worker
            from ..journal.journal import Journal

            try:
                journal = Journal(journal_dir)
                deadline = time.monotonic() + budget
                promoted = 0
                for ref in sorted(runs):
                    left = deadline - time.monotonic()
                    if left <= 0:
                        break
                    promoted += journal.promote_waiting(run_ref=ref, timeout=left)
                if spawn and (promoted or journal.waiting()):
                    outbox_worker.maybe_spawn(journal_dir)
            except Exception:  # noqa: BLE001 -- exit must not raise; items stay queued
                pass

        _at_exit(promote)

    def _kick_drainer(self, *, force: bool = False) -> None:
        """Wake the detached outbox worker (parity F1). Throttled: this runs
        on every async write and a training loop logs hundreds of points a
        second; ``maybe_spawn`` is O(1) but not free. Best-effort by design --
        ``finish()``/`probe run end` is the delivery barrier, this is latency.

        ``force`` (deferred finish, F3): skip the mode gate and the throttle
        -- a queued terminal status must not have its one kick swallowed --
        but never the transport gate; a worker cannot replay an injected one.

        The throttle arms ONLY on an actual spawn (prod smoke 2026-08-06): a
        probe that declined because a worker was alive must not suppress the
        next write's probe, or a worker exiting inside the window strands the
        writer's last op if the writer then dies. While a worker lives, every
        write pays one O(1) probe -- a status read and a lock check."""
        if not self._default_transport:
            return
        if not (self._auto_drain or force):
            return
        if not force and (time.monotonic() - self._drainer_kicked_at < self._drainer_kick_interval):
            return
        from .. import outbox as outbox_worker

        try:
            if outbox_worker.maybe_spawn(str(self.journal.dir)) and not force:
                self._drainer_kicked_at = time.monotonic()
        except Exception:  # noqa: BLE001 -- best-effort; run end is the barrier
            pass
