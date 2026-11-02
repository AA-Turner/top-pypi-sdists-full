"""The Probe service: one light process per user per machine, alive only while used.

    first agent session ──ensure──> python -m probe.service
                                      │ service.lock (flock, held for life)
                                      │ service.sock (unix stream, 0600, JSON-RPC 2.0 lines)
                                      │ discovering (15 s) -> running <-> grace (5 s) -> exit
                                      │
            tap watch / pi ──register/heartbeat──> registry ──pid watch──> owner exit
            desktop app    ──hello keepalive────> held alive while connected (D1)

            app / CLI      ──action.run─────────> actions.py ──> python -m probe.core.run <action>
                           ──status.get─────────> statuscache.py (a child, cached 30 s)
            CLI            ──manifest.refresh───> manifest.py (a child refreshes the CLI's cache)
            app            ──desktop.request────> management.py (a child answers `probe desktop request`'s request)
            app / CLI      ──session.list───────> registry.py + receipts.py (each session's journal: D29)
                           ──run.hold/release───> runholds.py (a `probe exec`'s run: the quiet check)
                           ──recorders.finish───> recorders.py (`probe capture off` for one agent)
            a recorder's tap ──controls.workers───> workers.py (its session's daemon worker)
            daemon worker  ──mailbox.post───────> mailhost.py (messages, run alerts, held questions:
            hooks, app     ──mailbox.claim/answer> the service owns delivery; the files stay the store, Q2)
            Stop waiter    ──events.subscribe───> mailwatch.py (the reads mailbox and held
                                                  questions of the sessions waited on, Q2)
            (daemon sessions) ──────────────────> alertpoll.py (their run alerts, once a machine)
            (recorded sessions) ────────────────> hints.py (the team's nearest records, posted to
                                                  each session's mailbox; Probe hints T3)
            SDK            ──outbox.drain───────> background.py: the drainer, a child (caller's python)
                           ──box.watch──────────> background.py: the box watcher, a child
                           ──telemetry.send─────> background.py: one sender thread
                           ──import.start───────> imports.py (an approved import's worker, watched)
            hooks          ──statusline.refresh─> statusline.py (one fetch child per plugin folder)
                           ──notes.sync─────────> notesync.py (the team note's sync, debounced)
            (schedule, check_now) ──────────────> updater.py: CLI + plugins, app, self
            (each minute, Codex's cache) ───────> codextrust.py: Probe's hooks approved again
                                                  once Codex rewrote its copies of them, in a child (#3617)

Nothing here runs on a timer while idle: owners are watched by the kernel
(pidfd on Linux, kqueue on macOS; a 2 s poll only where neither works), and the
only timers are the discovery end, the grace, a heartbeat-only owner's TTL,
the 6-hourly update check, the state post's and the Codex healer's minute (a
digest, a stat walk), and two that run only while they have work (plan
Q2): the mailbox watch's look every 0.25 s while a subscriber waits on a
session, and the run-alert round every 30 s while a daemon session is live
(one GET per session whose worker asked, on a kept connection). No model calls
and no CLI import in this process: heavy work stays in the per-session
workers, and every action, status read and update runs in a `probe.core.run`
child (plan R9, X7; `children.py`). Uploads run here in two places only: the
recorders (plan A2, D3: the owner moved capture into the service on
2026-10-22) and a training process's outbox drain (plan Q5), which runs as a
CHILD on the caller's interpreter, never in this process, and never holds the
service alive (D1); client telemetry batches the SDK built are POSTed from
one thread.

Stdlib only on the start path (plan S1, Q3; `tests/test_service_import_budget.py`).
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import contextlib
import itertools
import os
import signal
import socket
import threading
import time
from collections.abc import Callable

from ...foundation.service_api import paths
from .. import updater as updater_mod
from ..actions.actions import ActionManager
from ..watch.alertpoll import AlertPoller
from ..hooks.codex_trust import CodexTrust
from ..jobs.background.background import BackgroundHost
from ..hints.hints import HintLane
from ..hooks.hooks import HookHosts
from ..hooks.queue import HookQueue
from ..jobs.imports import IMPORTS_NAME, ImportWorkers
from ..mail.mail import MailHost
from ..mail.watch import MailWatch
from ..actions.management import Management
from ..updater.manifest import ManifestRefresher
from ..jobs.notesync import NoteSync
from ..sessions.receipts import ReceiptCache
from ..sessions.recorders.recorders import RecorderHost
from ..sessions.runholds import RUNS_NAME, RunHolds
from ..jobs.statusline import StatuslineRefresher
from ...foundation.service_api.wire import (
    API_VERSION,
    MAX_LINE_BYTES)
from ...foundation.service_api.vocabularies import (
    State,
    StopReason,
    Topic)
from ..sessions.sessions import Registry
from ..watch.statepost import StatePost
from ..actions.statuscache import StatusCache
from ..updater.updater import Updater
from ..watch.bounds import TracebackGate
from ..watch.watch import Watch
from ..sessions.workers import WorkerHost
from ...foundation.compose.compose import compose
from probe.service.server.connections.connections import Connection, ConnectionsMixin
from probe.service.server.connections.pid_waiter import PidWatcher
from probe.service.server.handlers.background import BackgroundHandlersMixin, MAX_PENDING_BACKGROUND
from probe.service.server.handlers.jobs import JobHandlersMixin
from probe.service.server.handlers.callers import CallerChecksMixin
from probe.service.server.handlers.hooks import HookHandlersMixin, MAX_PENDING_HOOK_RUNS, MAX_PENDING_HOST_STARTS
from probe.service.server.handlers.mailbox import MailboxHandlersMixin
from probe.service.server.handlers.runs import RunHandlersMixin
from probe.service.server.handlers.session import SessionHandlersMixin
from probe.service.server.legacy_door import LegacyDoor
from probe.service.server.lifecycle import LifecycleMixin, _keep
from probe.service.server.outbox import OutboxMixin
from probe.service.server.policy import _version, log
from probe.service.server.tracking import SessionsMixin
from probe.service.server.update_followup import UpdateFollowupMixin

#: Seconds without a live session (or keep-alive client) before the service exits.
GRACE_S = 5.0
#: Seconds after start in which the service never idles out: registrants of a
#: restarted service re-send within this window (plan X6).
DISCOVERY_S = 15.0
#: `hooks.queue` stores (a file write each) on one thread of their own, at
#: most this many taken in at once: past it a dispatcher runs its routes itself.
MAX_PENDING_QUEUE_STORES = 8


@compose
class Service(
    LifecycleMixin,
    UpdateFollowupMixin,
    SessionsMixin,
    ConnectionsMixin,
    SessionHandlersMixin,
    CallerChecksMixin,
    HookHandlersMixin,
    RunHandlersMixin,
    MailboxHandlersMixin,
    BackgroundHandlersMixin,
    JobHandlersMixin,
    OutboxMixin,
):
    def __init__(
        self,
        *,
        registry: Registry,
        grace_s: float = GRACE_S,
        discovery_s: float = DISCOVERY_S,
        expected_uid: int | None = None,
        legacy: LegacyDoor | None = None,
    ) -> None:
        self.registry = registry
        #: The pre-machine-key socket, for clients from before the key (plan D8).
        self.legacy = legacy
        self.grace_s = grace_s
        self.discovery_s = discovery_s
        self.expected_uid = (os.getuid() if hasattr(os, "getuid") else None) if expected_uid is None else expected_uid
        self.version = _version()
        #: The env this service's code came from, resolved at its start (a
        #: rebuild of the same version is another folder, `<v>+g<N>`).
        self.env = str(updater_mod.STARTED_ENV)
        self.pid = os.getpid()
        self.started_at = time.time()
        self.state = State.DISCOVERING
        self.connections: set[Connection] = set()
        self._serials = itertools.count(1)
        self.stop_reason: str | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._done: asyncio.Future | None = None
        self._server: asyncio.AbstractServer | None = None
        self._discovering_until = 0.0  # monotonic
        self._discovery_handle: asyncio.TimerHandle | None = None
        self._grace_handle: asyncio.TimerHandle | None = None
        #: `_keep_outbox`.
        self._outbox_task: asyncio.Task | None = None
        self._expiry_handle: asyncio.TimerHandle | None = None
        self.watcher: PidWatcher | None = None
        self.status_cache = StatusCache()
        #: What fails here, sent to the Probe team as automatic diagnostic
        #: reports (crash-report plan B2): the parts below note their failures
        #: to it (`incident=`), and it decides what is reported, with whose consent.
        self.watch = Watch(
            log=log, loop_getter=lambda: self._loop, updating=self._updating, barrier_up=_barrier_up,
            discovering=lambda: self.discovering, sessions=self._live_sessions, voters=self._voters,
            hosted_env=self._hosted_env, supervised=lambda sid: self.workers.supervised(sid),
            recorders=self._recorder_beats, receipts=self._watch_receipts,
        )
        #: The service's own state in PostHog (`statepost`): started, hourly and
        #: on a change, stopped; counts and enums only, with the machine's consent.
        self.statepost = StatePost(
            log=log, status=lambda: self._status(None, {}), consent=self.watch.machine_consent,
            voters=self._voters, login_env=self.watch.last_login_env, login_reader=self.watch._login_env,
            keys=self.watch.key_answers,
        )
        #: `service_error`'s tracebacks in service.log: a few per site and type (`watch.TracebackGate`).
        self._tracebacks = TracebackGate()
        #: Warm hook hosts, one per plugin folder sessions use (plan A0).
        self.hookhosts = HookHosts(log, incident=self.watch.note)
        #: `hooks.run`'s threads (plan D38), started on the first, and its slots.
        self._hook_runs = None
        self._hook_slots = threading.BoundedSemaphore(MAX_PENDING_HOOK_RUNS)
        #: Host starts' threads and slots: a folder check and a process start
        #: block, so neither runs on this loop.
        self._host_starts = None
        self._host_slots = threading.BoundedSemaphore(MAX_PENDING_HOST_STARTS)
        #: A training process's background work (plan Q5): drainer and box
        #: watcher children, client telemetry; their starts' threads and slots.
        self.background = BackgroundHost(log=log, incident=self.watch.note)
        self._background_starts = None
        self._background_slots = threading.BoundedSemaphore(MAX_PENDING_BACKGROUND)
        #: Warm-ups under way (asyncio keeps only a weak reference to a task).
        self._warming: set = set()
        #: plugin folder -> when `hooks.run` last started its host (monotonic).
        self._warmed: dict = {}
        #: Hook events' record-keeping routes, queued to run once (plan D36):
        #: stored on `_queue_stores`' thread, run on the queue's own.
        self.hook_queue = HookQueue(
            log, version=self.version, warm=self._warm_soon, changed=self._queue_changed, incident=self.watch.note
        )
        self._queue_stores = None
        self._queue_slots = threading.BoundedSemaphore(MAX_PENDING_QUEUE_STORES)
        #: `daemon.host`'s threads (`_daemon_host`): never the loop's shared executor.
        self._host_pool: concurrent.futures.ThreadPoolExecutor | None = None
        #: The daemon workers of the sessions recorded here whose tap hands them over (plan Q3).
        from ..sessions.daemon_host import DaemonHost

        self.workers = WorkerHost(log=log, incident=self.watch.note,
                                  daemon_host=DaemonHost(log=log, incident=self.watch.note))
        #: Sessions this service records itself, one thread each (plan A2).
        self.recorders = RecorderHost(
            log=log, loop_getter=lambda: self._loop, changed=self._recorders_changed, workers=self.workers,
            incident=self.watch.note, claimed=self._recorder_claimed, held=self._recorder_held,
        )
        # A registration this service made is held while it records the session
        # (`Registry._vacant`): a `tap watch` that took it back may take it up.
        self.registry.service_records = self.recorders.recording
        #: (method, sid, caller pid) -> when its refusal was last logged (`_log_unbound`).
        self._refusals_logged: dict = {}
        #: The runs a `probe exec` wraps here (`run.hold`), beside the registry.
        self.runs = RunHolds(registry.path.parent / RUNS_NAME)
        #: The CLI's release-manifest refreshes (`manifest.refresh`).
        self.manifest = ManifestRefresher(changed=self.reevaluate)
        #: Each registered session's delivery receipts (`session.list`, D29).
        self.receipts = ReceiptCache()
        #: The desktop app's management requests (`desktop.request`).
        self.management = Management(log=log, changed=self._management_changed)
        #: The status line's server reads, one child per plugin folder (`statusline.refresh`).
        self.statusline = StatuslineRefresher(log=log, changed=self.reevaluate, readings=self._statusline_readings)
        #: Claude Code config folders whose `refreshInterval` was looked at (`_refresh_interval`).
        self._interval_folders: set = set()
        self._interval_lock = threading.Lock()
        #: The team note's sync, once per machine (`notes.sync`); none starts
        #: while an in-place update replaces the CLI's files.
        self.notes = NoteSync(log=log, changed=self.reevaluate, held=lambda: self.updater.applying)
        #: Approved imports' workers this service started or watches (`import.start`).
        self.imports = ImportWorkers(
            registry.path.parent / IMPORTS_NAME, log=log, changed=self._imports_changed,
            held=lambda: self.updater.applying,
        )
        self._import_count = 0
        #: An update installed a new CLI while an action ran or waited: stop once they end.
        self._restart_pending = False
        self.actions = ActionManager(
            emit=self._emit, changed=self._changed, holder=self.mutating_holder, finished=self._action_finished
        )
        self.updater = Updater(
            version=self.version,
            emit=self._updater_emit,
            changed=self._cycle_changed,
            stop=self._restart_for_update,
            # A desktop request's change imports from the CLI's env like an action.
            action_running=lambda: self.actions.running is not None or self.management.running > 0,
            discovering=lambda: self.discovering,
            daemon_session=self.registry.daemon_unseen,
            state_dirs=self.registry.state_dirs,
            # An import worker imports from the CLI's env as a wrapped run does.
            run_held=lambda: self.runs.live() or self.imports.live(),
            app_connected=lambda: len(self._app_connections()),
            app_listeners=lambda: len(self._app_listeners()),
            app_target=self._app_target,
            send_app_check=self._send_app_check,
            app_alive=lambda serial: any(c.serial == serial for c in self._app_connections()),
            followup=self._update_followup,
            stop_hosted=self.workers.stop_hosted,
        )
        updater_mod.set_hosted(self.recorders.live, self.workers.hosted_draining)
        #: The reads mailboxes and approvals boards somebody waits on (plan Q2).
        self.mailwatch = MailWatch(
            loop_getter=lambda: self._loop,
            emit=self._emit,
            targets=self._watch_targets,
            log=log,
            boards=lambda: any(Topic.APPROVALS_CHANGED in c.topics for c in self.connections),
        )
        #: The reads mailbox and approvals board's writes and claims (plan Q2).
        self.mailhost = MailHost(log=log)
        #: The daemon sessions' run alerts, asked for once for the machine (plan Q2).
        self.alerts = AlertPoller(
            loop_getter=lambda: self._loop, sessions=self._daemon_sessions, log=log, version=self.version
        )
        #: The team's nearest records for each session recorded here, looked up
        #: once for the machine and posted to its mailbox (Probe hints T3).
        self.hints = HintLane(sessions=self._hint_sessions, log=log, version=self.version, posted=self._hint_posted)
        #: Probe's hooks in Codex, approved again whenever Codex rewrites its
        #: copies of Probe's plugins (#3617), while automatic updates are on.
        #: Never beside an update cycle, an action, a desktop change or a setup
        #: run from a terminal: they write Codex's config too.
        self.codex_trust = CodexTrust(
            log=log,
            changed=self.reevaluate,
            held=lambda: (self.updater.in_progress() or self.actions.running is not None
                          or self.management.running > 0
                          or updater_mod.setup_running(self.registry.state_dirs())),
            enabled=lambda: updater_mod.auto_update_enabled(self.registry.state_dirs()),
        )

    # -- lifecycle -----------------------------------------------------------

    async def run(self, listen: socket.socket, *, on_ready: Callable[[], None] | None = None) -> str:
        """Serve on `listen` until idle, stopped or signalled. Returns why it stopped."""
        self._loop = asyncio.get_running_loop()
        # The loop's unhandled exceptions: logged with their traceback and
        # counted for `service_error` (crash-report plan B2).
        self._loop.set_exception_handler(self._loop_exception)
        self._done = self._loop.create_future()
        # Before anything below can ask what holds the service (an action the
        # last service left unfinished ends during `actions.load`).
        self._discovering_until = time.monotonic() + self.discovery_s
        self.watcher = PidWatcher(self._loop)
        for session in self.registry.load():
            self._watch(session)
        for hold in self.runs.load():
            self._watch_hold(hold)
        self.imports.load(self.watcher.watch)
        self._import_count = len(self.imports.workers)
        self._schedule_expiry()
        self.alerts.changed()
        self.actions.load(self.watcher.watch)
        # The desktop changes an earlier service left running (they hold Update off).
        self.management.load(self.watcher.watch)
        self.updater.attach(self._loop)
        # Before the socket opens, so no `hooks.queue` finds it unready; what a
        # dispatcher queued while no service ran starts running now.
        self.hook_queue.start()
        if paths.WINDOWS:
            # A named pipe only this user can open (`winpipe.py`, plan R3/D17).
            from ...foundation.service_api import winpipe

            self._server = await winpipe.serve(self._loop, listen, self._handle, limit=MAX_LINE_BYTES + 1)
        else:
            self._server = await asyncio.start_unix_server(self._handle, sock=listen, limit=MAX_LINE_BYTES + 1)
        if self.legacy is not None and not paths.WINDOWS:
            await self.legacy.open(self._loop, self._handle)
        if self.discovery_s > 0:
            self._discovery_handle = self._loop.call_later(self.discovery_s, self._discovery_over)
        else:
            self._discovery_over()
        with contextlib.suppress(NotImplementedError, RuntimeError, ValueError):
            for sig in [getattr(signal, name) for name in ("SIGTERM", "SIGINT", "SIGHUP") if hasattr(signal, name)]:
                self._loop.add_signal_handler(sig, self.stop, StopReason.SIGNAL)
        log(
            f"serving (api {API_VERSION}, version {self.version}, pid watch {self.watcher.mechanism}, "
            f"{len(self.registry.sessions)} session(s) restored, grace {self.grace_s}s, "
            f"discovery {self.discovery_s}s)"
        )
        if on_ready is not None:
            on_ready()
        # What fails from here on is watched (crash-report plan B2).
        self.watch.start()
        self.statepost.start()
        self.codex_trust.start()
        # The sessions the last service recorded, from their saved progress
        # (after `on_ready`: the tap's import is no part of the start path).
        self._loop.call_soon(self._resume_recorders)
        # The CLI versions this machine's processes run from, for a home other
        # machines share (`installs.prune`).
        self._loop.run_in_executor(None, _mark_versions)
        # This service starts after every update: an outbox an older release
        # left paused is released now, and a pause that ends later the
        # minute it does, not at the next `probe` command.
        self._outbox_task = self._loop.create_task(self._keep_outbox())
        # The OS keeper (D35): the system starts the service again after a crash.
        self._loop.run_in_executor(None, _keep)
        try:
            return await self._done
        finally:
            await self._shutdown()

    def _discovery_over(self) -> None:
        self._discovery_handle = None
        self._discovering_until = 0.0
        # `probe status`'s `service.state` changes with it (`status.get`'s cache).
        self.status_cache.invalidate()
        self.reevaluate()
        # No updates while discovering (X6): the registry is still filling up.
        self.updater.after_discovery()

    @property
    def discovering(self) -> bool:
        return time.monotonic() < self._discovering_until

    def holds(self) -> bool:
        """Is anything keeping the service alive (plan D1, R3; API v1 "Alive")?
        A live session, a keep-alive client (the app's window), an action in
        progress, an update cycle (for at most its hold), a session's recorder
        still finishing (its last pass and FINALIZE), a manifest refresh in
        flight (at most its child's timeout), queued hook events not yet run
        (each bounded by its lane's budget), a desktop request being answered
        (at most its deadline), a status-line read or a team-note sync waiting
        or in flight (a session's last sync must not be lost), an import
        worker it watches, or an approval of Probe's hooks in Codex in flight
        (`codextrust`). A run hold does not: with no service there is no
        updater to keep off the run."""
        if self.registry.alive_count() > 0 or self.recorders.alive() or self.manifest.in_flight():
            return True
        if self.workers.host_runs() > 0:
            return True  # a session's queue still finishing in the daemon host (plan S5)
        if self.hook_queue.pending() > 0:
            return True  # queued hook events still to run (plan D36)
        if self.management.in_flight() or self.management.running > 0:
            return True  # a desktop request being answered, or a change's child still running
        if self.notes.in_flight() or self.statusline.in_flight() or self.imports.live():
            return True
        if self.codex_trust.asking():
            return True  # Probe's hooks in Codex being approved (at most codextrust.TIMEOUT_S)
        if self.actions.pending() or self.updater.holding():
            return True
        return any(conn.keepalive for conn in self.connections)

    def mutating_holder(self) -> dict | None:
        """What holds the one mutating slot (plan A5): an action, the update
        step that replaces the CLI's env, or a desktop request's change still
        running (until its child exits, past its deadline too: an Update or an
        uninstall must not replace the env under it, whatever wizard lock its
        context names). None when it is free."""
        return self.actions.busy_holder() or self.updater.busy_holder() or self.management.busy_holder()

    def reevaluate(self) -> None:
        if self.stop_reason is not None or self._loop is None:
            return
        if self.discovering:
            self.state = State.DISCOVERING
            return
        if self.holds():
            self.state = State.RUNNING
            if self._grace_handle is not None:
                self._grace_handle.cancel()
                self._grace_handle = None
            return
        if self._grace_handle is None:
            self.state = State.GRACE
            self._grace_handle = self._loop.call_later(self.grace_s, self._grace_over)
            # No session left: the login shell decides `service.stopped`'s consent; read it now.
            self.statepost.prime()

    def _grace_over(self) -> None:
        self._grace_handle = None
        if self.holds():
            self.reevaluate()
            return
        self.stop("idle")


def _mark_versions() -> None:
    with contextlib.suppress(Exception):
        from probe.shared.updates import installs

        if installs.versions_root().is_dir():
            installs.mark_in_use()


def _barrier_up() -> bool:
    """The update barrier or the workers' hold is up (an update's hand-over,
    this service's or one a stopped service left): read by the watch's scan, on
    a thread (files, and `ps` on macOS)."""
    from ..updater.quiet import barrier

    return barrier.workers_held() or not barrier.wait(0)
