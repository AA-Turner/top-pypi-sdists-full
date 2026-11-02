"""stop, restart onto newer code (a successor), shut down; react when an action, desktop change or update cycle ends."""

from __future__ import annotations

import asyncio
import contextlib
import os
import sys
import time

from ...foundation.service_api import paths
from ..jobs.background.background import FLUSH_S as BACKGROUND_FLUSH_S
from ...foundation.service_api.vocabularies import (
    Action,
    StopReason,
    Topic)
from ..watch.settings import UPDATE_FAILED_STREAK
from ..watch.incident import Family
from ..watch.bounds import log_traceback
from probe.service.server.policy import log
#: Created while the service stops, so a new instance that finds the lock still
#: held waits for it instead of exiting (the old one is about to let go).
STOPPING_NAME = "service.stopping"
#: How long the next service's starter waits for a restarting one to exit
#: (`Service._start_successor`): its recorders pause for at most PAUSE_JOIN_S.
SUCCESSOR_WAIT_S = 30.0
STOPPING_WAIT_S = 3.0


class LifecycleMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    def _changed(self) -> None:
        """An action started or ended: what holds the service, and what
        `probe status` would say, may have changed."""
        self.status_cache.invalidate()
        if self._restart_pending and not self.actions.pending():
            self.stop(StopReason.UPDATE)
            return
        self.reevaluate()

    def _management_changed(self) -> None:
        """A desktop change's child exited: what holds the service (and the
        mutating slot) may have changed."""
        self.status_cache.invalidate()
        self.actions.drain()
        self.reevaluate()

    def _cycle_changed(self) -> None:
        """An update cycle started, let go of the mutating slot or ended: what
        holds the service may have changed (the actions queued behind it run
        now), and so may every version `probe status` reports."""
        self.status_cache.invalidate()
        self.actions.drain()
        self._note_update_cycles()
        self.reevaluate()

    def _note_update_cycles(self) -> None:
        """UPDATE_FAILED_STREAK cycles in a row ended `ok: false`
        (`updater` keeps the count): one `update_failed` per such cycle (plan B2)."""
        if self.updater.in_progress():
            return
        streak = self.updater.state.get("failed_in_a_row")
        last = self.updater.state.get("last_result")
        if isinstance(streak, int) and streak >= UPDATE_FAILED_STREAK and isinstance(last, dict):
            self.watch.note(
                Family.UPDATE_FAILED, "failed_in_a_row", facts={"in_a_row": streak, "last_result": last},
                once=f"update_failed:{last.get('cycle_id')}",
            )

    def _loop_exception(self, loop: asyncio.AbstractEventLoop, context: dict) -> None:
        """`loop.set_exception_handler`: a callback's exception, a task's never
        retrieved. Logged with its traceback (each line with the service's
        prefix), and one event of `service_error`. Never raises."""
        try:
            exc = context.get("exception")
            message = str(context.get("message") or "unhandled exception in the event loop")
            text = ""
            if isinstance(exc, BaseException):
                import traceback

                text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            log_traceback(log, f"loop: {message}", text, gate=self._tracebacks,
                          key=("loop", type(exc).__name__ if exc is not None else message[:60]))
            self.watch.note(Family.SERVICE_ERROR, "loop_exception", facts={
                "message": message[:300], "type": type(exc).__name__ if exc is not None else None, "traceback": text,
            })
        except Exception:  # noqa: BLE001
            pass

    def _action_finished(self, action: str) -> None:
        if action == Action.UPDATE:
            self.updater.after_update_action()

    def _restart_for_update(self, reason: str) -> None:
        """An update cycle installed a new CLI: this service is old code. Not
        under a running action, though, whose child would lose the rest of its
        events and read as stopped with the service: the action holds the one
        mutating slot meanwhile, and the stop follows the moment it ends. Nor
        before the actions queued behind the update have run (on the new CLI:
        their child is `runtime.json`'s interpreter)."""
        if self.actions.pending():
            if not self._restart_pending:
                log("a new CLI is installed: restarting once the running and queued actions end")
            self._restart_pending = True
            return
        self.stop(reason)

    def stop(self, reason: str) -> None:
        if self.stop_reason is not None or self._done is None:
            return
        self.stop_reason = reason
        # No queued action starts under a stopping service (the cycle's
        # cancellation below says the slot is free): the next one reads it as stopped.
        self.actions.stop_starting()
        with contextlib.suppress(OSError):
            (paths.service_dir() / STOPPING_NAME).touch()
        log(f"stopping ({reason})")
        # No daemon worker starts from here on: one would outlive this process unowned.
        with contextlib.suppress(Exception):
            self.workers.close()
            if self._host_pool is not None:
                self._host_pool.shutdown(wait=False, cancel_futures=True)  # a proxy's wait never holds the exit
        self._emit(Topic.SERVICE_STOPPING, {"reason": reason})
        guarded = bool(getattr(self.updater, "guard_pending", None))
        with contextlib.suppress(Exception):
            self.statepost.stopped(reason, uptime_s=time.time() - self.started_at)
        with contextlib.suppress(Exception):
            self.updater.before_exit(reason)
        with contextlib.suppress(Exception):
            from .. import guard

            guard.record_stop(reason, self.version)
        if reason in (StopReason.UPDATE, StopReason.TAP_UPDATE) and not guarded:
            with contextlib.suppress(Exception):
                if self.recorders.alive():
                    self._start_successor()
        if reason in (StopReason.UPDATE, StopReason.TAP_UPDATE, StopReason.IDLE, StopReason.STOP):
            # A stop on purpose is no start for `ensure` to back off from: only
            # a service that dies is (three a minute). An idle exit or a
            # `probe service stop` counted too, and a session starting right
            # after two quick idle exits found no service for most of a minute
            # (live test I, 2026-10-24). What a miss would start again after an
            # idle exit, the hooks' dispatcher leaves alone for a while instead
            # (`dispatch.idle_recently`, reading `guard.record_stop` above).
            with contextlib.suppress(Exception):
                from ...foundation import service_api as client

                # Its parent too: on Windows a venv's python is a launcher's child.
                client.forget_start(os.getpid(), os.getppid())
        self.updater.close()
        if not self._done.done():
            self._done.set_result(reason)

    def _start_successor(self) -> None:
        """This service restarts onto newer code or a newer tap while it records
        sessions: the next one starts the moment this one is gone (a detached
        `ensure` that waits for this pid), not at whatever asks next. Its
        recorders pause about a second and resume there from their saved
        progress. A switch's guard (D5) starts it itself. Never raises."""
        import subprocess

        from ...foundation import service_api as client

        # Gone, or a zombie its parent has not reaped yet: its lock and socket
        # went with its last file descriptor (`client._pid_runs`).
        code = (
            "import sys, time\n"
            "from probe.service import client\n"
            "pid, until = int(sys.argv[1]), time.monotonic() + float(sys.argv[2])\n"
            "while client._pid_runs(pid) and time.monotonic() < until:\n"
            "    time.sleep(0.1)\n"
            "client.ensure()\n"
        )
        try:
            subprocess.Popen(  # noqa: S603 -- the CLI's own interpreter, our own module
                [client.runtime_python() or sys.executable, "-I", "-c", code, str(os.getpid()), str(SUCCESSOR_WAIT_S)],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                cwd=str(paths.service_dir()), env=client._clean_env(), close_fds=True, **client._DETACHED,
            )
            log("the next service starts once this one has exited")
        except OSError as exc:
            log(f"could not start the next service: {exc}")

    async def _shutdown(self) -> None:
        # First: the recorders pausing below moves every session's capture,
        # and a status-line refresh following it would write "not started"
        # from a service on its way out (`statusline.py`).
        with contextlib.suppress(Exception):
            self.statusline.close()
        for handle in (self._discovery_handle, self._grace_handle, self._expiry_handle, self._outbox_task):
            if handle is not None:
                handle.cancel()
        if self._server is not None:
            self._server.close()
        if self.legacy is not None:
            self.legacy.close()
        for conn in list(self.connections):
            with contextlib.suppress(Exception):
                await asyncio.wait_for(conn.writer.drain(), 0.2)
            with contextlib.suppress(Exception):
                conn.writer.close()
        if self.watcher is not None:
            self.watcher.close()
        self.mailwatch.close()
        self.mailhost.close()
        self.alerts.close()
        self.hints.close()
        self.hookhosts.close()
        self.hook_queue.close()
        # Its children go on delivering: the outbox on disk is theirs. The
        # telemetry it took gets the SDK sender's bounded flush, on a thread,
        # while the recorders pause below.
        flushing = asyncio.ensure_future(asyncio.to_thread(self.background.close, BACKGROUND_FLUSH_S))
        for pool in (self._hook_runs, self._host_starts, self._queue_stores, self._background_starts):
            if pool is not None:
                pool.shutdown(wait=False, cancel_futures=True)
        # No worker starts from here on; the running ones are asked to hand over
        # to the next service's (`recorders.close`), never stopped.
        with contextlib.suppress(Exception):
            self.workers.close()
            if self._host_pool is not None:
                self._host_pool.shutdown(wait=False, cancel_futures=True)  # a proxy's wait never holds the exit
        self.watch.close()
        self.statepost.close()
        self.codex_trust.close()
        # Every recorder pauses (after the connections closed: a recorder's link
        # cannot end its session in the registry saved below).
        with contextlib.suppress(Exception):
            await self.recorders.close()
        with contextlib.suppress(Exception):
            await flushing
        self.actions.close()
        for part in (self.notes, self.imports):
            with contextlib.suppress(Exception):
                part.close()
        self.registry.save()


def _keep() -> None:
    with contextlib.suppress(Exception):
        from .. import keeper

        # The lifeboat first (`lifeboat.install`), then the units that run it;
        # env.json with the login shell's index settings (never this clean env's).
        login = None
        if keeper.wanted():
            from ..updater import lifeboat

            login = lifeboat.login_env()
        outcome = keeper.install(login)
        if outcome not in ("current", "not wanted"):
            log(f"keeper: {outcome}")


def _lifeboat_after(result: dict) -> None:
    with contextlib.suppress(Exception):
        from ..updater import lifeboat

        if lifeboat.after_cycle(result):
            log("lifeboat: current/ proved itself and is the known-good copy now")
