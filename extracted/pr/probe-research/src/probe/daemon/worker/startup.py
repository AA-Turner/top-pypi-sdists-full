"""`probe daemon worker`: parse arguments, take the session lock, run the worker to an exit code."""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import contextvars
import logging
import os
import signal
import sys
import threading
from dataclasses import dataclass
from probe import analytics as telemetry
from pathlib import Path
from typing import Callable
from probe.daemon.host import lease
from probe.shared import mailbox
from probe.daemon.worker import alerts
from probe.daemon.trace import shipper as shipper_mod
from probe.daemon.trace import trace as trace_mod
from probe.sdk.session_marker import WIZARD_HINT
from probe.daemon.store.device import LANE_WRITE
from probe.daemon.store.store import StoreVersionError
#: "1": the supervisor started this worker outside its session's folder (the
#: service starts it from its state folder: a hung project mount must not stall
#: the service), so it moves into `--cwd` itself, HOME if it cannot -- where
#: the tap's spawn would have started it.
ENTER_CWD_ENV = "PROBE_DAEMON_ENTER_CWD"


# ---------------------------------------------------------------------------
# Entry point.
# ---------------------------------------------------------------------------


@dataclass
class RunHooks:
    """How a run of the worker meets what started it: its own process
    (`main`, a per-process worker) or the daemon host (`probe.daemon.host.host`), which
    runs every session's worker as a thread of one process. The steps, their
    order and the exit codes are the same either way (`run_session`)."""

    #: One line for the session's `<sid>.log` (the process's stderr, per process).
    say: Callable[[str], None]
    #: Has the run's supervisor gone (`parent_gone` per process; the owner's
    #: connection, hosted)?
    supervisor_gone: Callable[[], bool]
    #: Called where the per-process worker configures logging (after the
    #: barrier and inline checks, before the AI libraries load).
    configure_logging: Callable[[], None] = lambda: None
    #: Called where the per-process worker installs its signal handlers (just
    #: before it takes the session lock).
    ready: Callable[[], None] = lambda: None
    #: Runs the worker's loop (`asyncio.run` per process; the host's own loop).
    run: Callable[..., int] = asyncio.run
    #: Per process: the worker's parent at start and its supervisor's identity
    #: (`supervisor_identity`), kept on the Worker as before.
    parent_pid: int | None = None
    supervisor: tuple[int, str | None] | None = None
    #: Hosted: the Worker reads `supervisor_gone` itself instead of its parent.
    hosted: bool = False
    #: Called with the Worker once it exists, before its loop starts (the host
    #: sets its heartbeat and a moved run's finish deadline).
    on_worker: Callable[[Worker], None] = lambda worker: None


class Stopper:
    """A stop asked of a run: SIGTERM or SIGINT per process (the handler runs on
    the run's own thread), the host's `stop` hosted (from another thread: the
    worker's `begin_stopping` is then called on its loop). A stop before the
    worker exists begins as soon as it does (`bind`); one after its loop ended
    has nothing left to begin and never raises."""

    def __init__(self) -> None:
        self.asked = False
        self.worker: Worker | None = None
        self.loop: asyncio.AbstractEventLoop | None = None
        self._thread: int | None = None
        #: The run's context as its loop started: a stop from another thread
        #: begins inside it (the run's environment and state folder).
        self._context: contextvars.Context | None = None
        # Re-entrant: per process `request` runs in the signal handler, on the
        # very thread that may be inside `bind` (a plain lock would hang it there).
        self._lock = threading.RLock()

    def request(self) -> None:
        with self._lock:
            self.asked = True
            worker, loop, thread, context = self.worker, self.loop, self._thread, self._context
        if worker is None:
            return  # `bind` begins stopping once the worker exists
        if loop is None:
            if thread == threading.get_ident():
                worker.begin_stopping()  # the run's own thread, before its loop: at once, as before
            return  # another thread's: `bind` takes it as the run's loop starts
        try:
            running = asyncio.get_running_loop()
        except RuntimeError:
            running = None
        if running is loop:
            worker.begin_stopping()  # the finish budget starts now, not at the next round
            return
        try:
            loop.call_soon_threadsafe(worker.begin_stopping, context=context)
        except RuntimeError:
            pass  # its loop closed meanwhile: the run is over

    def bind(self, worker: Worker, loop: asyncio.AbstractEventLoop | None = None) -> None:
        """The run's worker (as it is built), then its loop (as the loop starts)."""
        with self._lock:
            self.worker, self.loop, self._thread = worker, loop, threading.get_ident()
            self._context = contextvars.copy_context() if loop is not None else None
            asked = self.asked
        if asked:
            worker.begin_stopping()

    def unbind(self) -> None:
        """The run's loop has ended: a later stop has nothing to begin."""
        with self._lock:
            self.worker, self.loop = None, None


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="probe daemon worker")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--source", default="claude_code")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    # Pydantic AI prints a welcome banner on its first run; it would land in the
    # daemon's log on every start.
    os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")
    args = _parse_args(argv)
    # First, before anything slow: its supervisor may be gone by the time the
    # libraries are loaded (`_parent_gone`).
    parent = os.getppid()
    supervisor = supervisor_identity(args.session_id)
    if os.environ.get(ENTER_CWD_ENV) == "1":
        # Started from a local folder by the service: into the session's own
        # here, on this worker's time (a hung mount stalls this session alone).
        try:
            os.chdir(args.cwd)
        except OSError:
            with contextlib.suppress(OSError):
                os.chdir(Path.home())
    stopper = Stopper()

    def _configure_logging() -> None:
        # Into the session's folder beside its trace (`trace.py`); warnings on stderr too.
        logging.basicConfig(level=os.environ.get("PROBE_DAEMON_LOG", "INFO"),
                            format="%(asctime)s %(levelname)s %(name)s %(message)s",
                            handlers=trace_mod.log_handlers(args.session_id))
        trace_mod.quiet_noisy_loggers()
        # The harness warns through `warnings` (a collapsed prompt cache, T3): into the log.
        logging.captureWarnings(True)

    def _stop(_sig, _frame):
        stopper.request()

    def _ready() -> None:
        signal.signal(signal.SIGTERM, _stop)
        signal.signal(signal.SIGINT, _stop)

    hooks = RunHooks(say=lambda text: print(text, file=sys.stderr),
                     supervisor_gone=lambda: parent_gone(supervisor, parent),
                     configure_logging=_configure_logging, ready=_ready, parent_pid=parent, supervisor=supervisor)
    return run_session(Session(args.session_id, Path(args.transcript), Path(args.cwd), args.source), hooks, stopper)


def run_session(session: Session, hooks: RunHooks, stopper: Stopper) -> int:
    """One run of a session's worker, start to exit code: the per-process
    worker's whole life (`main`), or one run in the daemon host."""
    from probe.service.updater.quiet import barrier

    sid = session.session_id
    if barrier.workers_held() or not barrier.wait():
        # The Probe service is replacing the CLI's env (plan X1), or stopping
        # the running workers first (D7): `probe`'s own entry looked already;
        # this covers a worker started another way.
        hooks.say(f"probe daemon worker: {barrier.MESSAGE}")
        return EXIT_RESPAWN_LATER
    if lease.inline(sid):
        # Started while manual or confirmed-quota inline is active (an older tap wants a
        # worker there): leave before loading anything.
        return inline_exit_code(sid)
    hooks.configure_logging()
    if not ai_libraries_importable():
        if _libs_missing_log_due(sid):
            _device_error(f"daemon mode needs the AI libraries: Enter on Who records in the Probe wizard "
                          f"installs them ({WIZARD_HINT})")
        hooks.say(f"the daemon's AI libraries are not installed: Enter on Who records in the Probe wizard "
                  f"installs them ({WIZARD_HINT})")
        return libs_missing_exit_code()
    from probe.daemon.agent.model import model as model_mod

    try:
        ep = model_mod.endpoint()
    except model_mod.NoKey as exc:
        _device_error(str(exc))
        return EXIT_DO_NOT_RESPAWN
    alerts.configure(ep.base_url)
    # Before anything is recorded: whose traces these are (`shipper.bind`). A
    # folder recorded under another account or server stays local, unshipped.
    shipper_mod.bind(sid, ep.base_url, ep.key)
    # Whose hint marker the reader's prompt wake and every chat request read.
    model_mod.bind_hints(sid)
    # The watched session, named on every `/v1/companion/*` call (its spend).
    model_mod.bind_session(session.source, sid)
    worker: Worker | None = None
    hooks.ready()
    held = session_lock(sid, should_stop=lambda: stopper.asked or hooks.supervisor_gone())
    if isinstance(held, int):
        return held
    if not barrier.wait():
        # Raised while this worker loaded its libraries, after the check above:
        # the service's second look (plan X1) may have found no lock of ours
        # then. Holding it now, wait for the update to finish, else come back.
        hooks.say(f"probe daemon worker: {barrier.MESSAGE}")
        held.close()
        return EXIT_RESPAWN_LATER
    # We hold the lock, so no other worker of this session runs: a `.finishing`
    # left by one that crashed is stale.
    mailbox.finishing_path(sid).unlink(missing_ok=True)
    try:
        # At once, not after the folder baseline: `probe ask --writer` refuses a
        # live worker without it as one from before requests.
        mailbox.keep_folders()
        mailbox.mark_worker_accepts(sid)
    except OSError as exc:
        log.warning("could not say this worker takes requests: %s", exc)
    try:
        try:
            worker = Worker(session)
        except (LookupError, StoreVersionError) as exc:
            _device_error(str(exc))
            return EXIT_DO_NOT_RESPAWN
        stopper.bind(worker)  # a stop asked by now begins before the sweeps, as before
        worker.marks_requests = True
        if hooks.hosted:
            worker.supervisor_gone = hooks.supervisor_gone
        else:
            worker.parent_pid, worker.supervisor = hooks.parent_pid, hooks.supervisor
        hooks.on_worker(worker)
        try:
            sweep_stale(sid)
            mailbox.sweep_stale_sessions(sid)
        except Exception as exc:  # noqa: BLE001 -- housekeeping never stops recording
            log.warning("sweeping old daemon files failed: %s", exc)

        async def _loop() -> int:
            stopper.bind(worker, asyncio.get_running_loop())
            try:
                return await worker.loop()
            finally:
                stopper.unbind()

        return hooks.run(_loop())
    except Exception as exc:  # noqa: BLE001 -- a bug hands writing back and waits, never a hot crash loop
        if install_replaced():
            # Not a bug: the CLI was reinstalled under this worker (2026-10-12, CLI
            # 0.233.1: FileNotFoundError on record_session.md, pinged as a crash).
            # Exit 0 and the supervisor starts the new install now, which takes the
            # session over; no crash backoff, no ping.
            log.warning("the probe CLI was reinstalled under this worker (%s: %s); exiting for the new install",
                        type(exc).__name__, exc)
            _device_error(f"session {sid}: the probe CLI was reinstalled; the daemon restarts on the new install")
            try:
                lease.release(sid, lease.REASON_STOPPED)
            except Exception:  # noqa: BLE001
                pass
            return 0
        if alerts.disk_full(exc):
            # Not a bug: the machine's disk is full (new-workspace 2026-10-24: the
            # store's COMMIT, pinged as "Daemon crashed"). Said where the
            # researcher looks, no ping; its supervisor waits as after a crash.
            log.error("the daemon worker stopped: the disk is full (%s)", _crash_detail(exc))
            try:
                _device_error(f"session {sid}: the daemon stopped: the disk is full ({_crash_detail(exc)}; "
                              f"its state folder: {_state_base()}); it starts again once there is space")
            except OSError:
                pass  # the disk that is full may be this log's too
            try:
                lease.release(sid, lease.REASON_DISK_FULL)
            except Exception:  # noqa: BLE001
                pass
            return EXIT_DISK_FULL
        log.exception("the daemon worker crashed")
        _device_error(f"session {sid}: the daemon crashed ({_crash_detail(exc)}); "
                      "the agent records until capture starts it again")
        try:
            lease.release(sid, lease.REASON_ERROR)
        except Exception:  # noqa: BLE001
            pass
        # After the lease: the agent records again before the up to 3.5 s flush below.
        alerts.report(alerts.Kind.CRASHED, session_id=sid, lane=LANE_WRITE, exc=exc)
        # The stack (Probe's own frames, no message) as a `$exception`; it flushes both before exit.
        telemetry.report_crash(exc, surface="daemon", base_url=ep.base_url)
        return EXIT_CRASHED
    finally:
        mailbox.finishing_path(sid).unlink(missing_ok=True)
        try:
            mailbox.clear_worker_accepts(sid)  # before the lock goes: the next worker writes its own
        except OSError:
            pass
        held.close()
from probe.daemon.worker.env import Session  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.error_log import _crash_detail, _device_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.files import _state_base, session_lock, sweep_stale  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.install import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _libs_missing_log_due,
    ai_libraries_importable,
    install_replaced,
    libs_missing_exit_code,
)
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.supervisor import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    EXIT_CRASHED,
    EXIT_DISK_FULL,
    EXIT_DO_NOT_RESPAWN,
    EXIT_RESPAWN_LATER,
    inline_exit_code,
    parent_gone,
    supervisor_identity,
)
from probe.daemon.worker.worker import Worker  # noqa: E402 -- pieces need each other; the front door loads this one first


if __name__ == "__main__":
    raise SystemExit(main())
