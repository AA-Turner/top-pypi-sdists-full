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

Nothing here runs on a timer while idle: owners are watched by the kernel
(pidfd on Linux, kqueue on macOS; a 2 s poll only where neither works), and the
only timers are the discovery end, the grace, a heartbeat-only owner's TTL,
the 6-hourly update check, and two that run only while they have work (plan
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
import re
import select
import signal
import socket
import struct
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path

from . import caller, paths
from .caller import Bound, same_process
from . import updater as updater_mod
from .actions import ActionManager
from .alertpoll import AlertPoller
from .background import FLUSH_S as BACKGROUND_FLUSH_S
from .background import BackgroundHost, other_network
from .hints import HintLane
from .hints import followed as hint_sessions
from .hookhosts import DRAIN_S, UNHOSTED_LANES, HookHosts, Via, run_event, timed_out_answer
from .hookqueue import HookQueue
from .imports import IMPORTS_NAME, ImportWorkers, valid_job_id
from .imports import prepare as prepare_import
from .mailhost import MailHost
from .mailwatch import MAX_TARGETS, MailWatch, Target, default_state
from .management import CALLER_PID_ENV, CALLER_START_ENV, Management
from .manifest import ManifestRefresher
from .notesync import MAX_AGENTS as MAX_NOTE_AGENTS
from .notesync import NoteSync
from .receipts import ReceiptCache, by_harness, journal_roots
from .recorders import SETTLE_S as TAP_SETTLE_S
from .recorders import RecorderHost
from .runholds import RUNS_NAME, Hold, RunHolds
from .statusline import StatuslineRefresher
from .protocol import (
    API_VERSION,
    CAPS,
    Action,
    BusyHolder,
    CLIENTS,
    MAX_HOOK_PATH,
    MAX_LINE_BYTES,
    METHODS,
    MODES,
    MAX_SUBSCRIBE_SESSIONS,
    MailboxPart,
    SESSION_TOPICS,
    NOTES_MODES,
    REPORT_ENV,
    TOPICS,
    CHECK_TRIGGERS,
    BackgroundRefusal,
    Client,
    EndReason,
    ErrorCode,
    Method,
    RefusedReason,
    RpcError,
    State,
    StopReason,
    Topic,
    CheckTrigger,
    encode,
    error,
    event,
    invalid_params,
    need_background,
    is_agent_id,
    need_bool,
    need_choice,
    need_context,
    need_env,
    need_hook_queue,
    need_hook_run,
    need_mailbox_answer,
    need_mailbox_claim,
    need_mailbox_post,
    need_app_check,
    need_app_result,
    need_int,
    need_owner,
    need_sessions,
    need_path,
    need_sid,
    need_state_dir,
    need_str,
    need_telemetry,
    need_wait,
    parse_request,
    result,
    BASE_URL_ENV,
    ORIGIN_DESKTOP,
    Mode,
)
from .registry import HEARTBEAT_TTL_S, SERVICE, Outcome, Registry, Session
from .statepost import StatePost
from .statuscache import StatusCache
from .updater import Updater, preload
from .watch import UPDATE_FAILED_STREAK, Family, Live, TracebackGate, Watch, log_traceback
from .workers import WorkerHost

#: Seconds without a live session (or keep-alive client) before the service exits.
GRACE_S = 5.0
#: Seconds after start in which the service never idles out: registrants of a
#: restarted service re-send within this window (plan X6).
DISCOVERY_S = 15.0
#: Test-only overrides (API v1, "Lifecycle"). Nothing in production sets them.
GRACE_ENV = "PROBE_SERVICE_GRACE_S"
DISCOVERY_ENV = "PROBE_SERVICE_DISCOVERY_S"
TTL_ENV = "PROBE_SERVICE_TTL_S"
#: Where neither pidfd nor kqueue can watch a pid, poll it this often.
POLL_S = 2.0
#: A subscriber whose unread events pass this is dropped, not buffered forever.
MAX_SUBSCRIBER_BUFFER = 4 * 1024 * 1024
#: `hooks.run` events running at once, at most: each holds a thread while its
#: routes run (a caller waits 300 ms by default; a later one waits its turn,
#: within its own wait).
MAX_HOOK_RUNS = 8
#: `hooks.run` events taken in at once (running, or queued for a thread): past
#: it a request is refused at once, so stalled folder checks (a hung network
#: mount) never queue without limit. A queued event whose caller's wait has
#: passed is dropped unrun.
MAX_PENDING_HOOK_RUNS = 2 * MAX_HOOK_RUNS
#: `hooks.run`'s answer may land this long after its deadline: an event that
#: ended right at it still has its output read (`hookhosts.DRAIN_S`).
ANSWER_GRACE_S = DRAIN_S + 0.05
#: Host starts (`hooks.host`, a `hooks.run` warm-up) on their own threads, and
#: at most this many taken in at once.
HOST_START_THREADS = 2
MAX_PENDING_HOST_STARTS = 4
#: After an update, how many times the follow-up asks again about a newer tap
#: folder its agent may still be writing (`_follow_tap`), TAP_SETTLE_S apart.
FOLLOW_TAP_TRIES = 3
#: `hooks.queue` stores (a file write each) on one thread of their own, at
#: most this many taken in at once: past it a dispatcher runs its routes itself.
MAX_PENDING_QUEUE_STORES = 8
#: What a `hooks.queue` answer waits for its store, at most (the dispatcher
#: itself waits 300 ms, then writes the event beside it: one id runs once).
QUEUE_STORE_WAIT_S = 5.0
#: What a `hooks.host` caller waits for its host start, at most.
HOST_START_WAIT_S = 5.0
#: `outbox.drain` / `box.watch` checks and child starts (a stat, a sandbox
#: read, a fork) on their own threads, at most this many taken in at once, and
#: what a caller is answered within (the SDK gives up well before: its budget
#: is `client.HANDOFF_BUDGET_S`).
BACKGROUND_THREADS = 2
MAX_PENDING_BACKGROUND = 8
BACKGROUND_WAIT_S = 2.0
#: A folder's warm host is started for `hooks.run` at most this often (a host
#: that will not stay up is not started again on every tool call): the
#: dispatcher's own `ASK_EVERY_S`.
WARM_EVERY_S = 30.0
#: How long `session.list` waits for its sessions' receipts (`receipts.py`)
#: before it answers with the last ones read: the listing is on every
#: `probe status`'s one-second path.
RECEIPTS_WAIT_S = 0.25
#: The log is cut over to `service.log.1` at start once it passes this.
MAX_LOG_BYTES = 256 * 1024
#: Created while the service stops, so a new instance that finds the lock still
#: held waits for it instead of exiting (the old one is about to let go).
STOPPING_NAME = "service.stopping"
#: How long the next service's starter waits for a restarting one to exit
#: (`Service._start_successor`): its recorders pause for at most PAUSE_JOIN_S.
SUCCESSOR_WAIT_S = 30.0
STOPPING_WAIT_S = 3.0
#: While another process holds the pre-machine-key folder's lock (a service
#: from before the key, still running), look again this often (plan D8).
LEGACY_RETRY_S = 10.0
LEGACY_RETRY_ENV = "PROBE_SERVICE_LEGACY_RETRY_S"
#: `hooks.run` runs only the events pi sends it (plan D38, pi's `serviceGuard.ts`):
#: the pre-tool lane, for the tools pi's guard reads (its `ClaudeTool` names, and
#: Probe's own MCP tools, which routes.json's matcher takes by `probe[-_]research`).
#: Any process of this user reaches the socket, and the payload is the caller's
#: word: another lane or tool would run Probe's consent routes on a forged
#: event -- a typed `/probe inline` on the prompt lane moves the switch, a
#: question-tool pick on the post-tool lane records a yes with the answer key the
#: hook reads, a question tool's pre-tool route records a permission mode the
#: daemon reads as bypass (#3355).
HOOK_RUN_LANES = frozenset({"pre-tool"})
HOOK_RUN_TOOLS = frozenset({"Bash", "Write", "Edit", "MultiEdit"})
PROBE_MCP_TOOL = "probe[-_]research"
#: A refused session or mailbox call is logged once per (session, process) in
#: this long: two agents on one session id retry every 2 s, and the log is
#: rotated only when the service starts.
REFUSAL_LOG_S = 600.0
#: At most this many refusals are remembered for that.
MAX_REFUSALS_LOGGED = 1024
#: `mailbox.answer`'s `key` (a held question's answer key, 64 hex characters:
#: `probe.daemon.approvals.KEY_HEX_CHARS`) is at most this long; checked in full
#: on the mailbox thread (`Board.key_matches`).
MAX_ANSWER_KEY = 128


#: Methods this service answers that are not in `protocol.METHODS` (that file is
#: byte-copied into the tap): only this release's own CLI calls them.
DAEMON_HOST_METHOD = "daemon.host"
LOCAL_METHODS = frozenset({DAEMON_HOST_METHOD})


class Policy:
    """What a method does for its caller (`METHOD_POLICY`), which decides who may call it."""

    #: Answers from what the service knows: anyone (of this user) may ask.
    READ = "read"
    #: Ends or stops what is the caller's own (or the service): benign, anyone.
    CONTROL = "control"
    #: Runs or stores work outside the caller -- a child, a recorder, a hold
    #: that keeps updates off, an upload: never for a caller this service
    #: cannot rule out being confined (`caller.sandboxed`, `other_network`).
    #: Refused before its handler is reached, whatever the handler checks.
    WORK = "work"


#: Every method, classified (tests/test_service_background.py fails on one
#: missing). A method added to `protocol.METHODS` without a class is WORK.
METHOD_POLICY = {
    Method.HELLO: Policy.READ,
    Method.STATUS: Policy.READ,
    Method.SESSION_LIST: Policy.READ,
    Method.EVENTS_SUBSCRIBE: Policy.READ,
    Method.ACTION_STATUS: Policy.READ,
    Method.ACTION_EVENTS: Policy.READ,
    Method.UPDATE_STATUS: Policy.READ,
    Method.SESSION_RECORDING: Policy.READ,
    # Only the session's registrant (or this service) may end it (#3360,
    # `registry.Registry.holds`), checked in the registry.
    Method.SESSION_END: Policy.CONTROL,
    Method.ACTION_CANCEL: Policy.CONTROL,
    Method.STOP: Policy.CONTROL,
    # Not a read: a `refresh` starts a `probe status` child that sends the
    # stored token and each agent's capture token through the proxy and CA
    # the request's `context` names.
    Method.STATUS_GET: Policy.WORK,
    # Stops ANY session's recorder by its id (`session.list` names them all):
    # the same as `recorders.finish`, one session at a time.
    Method.SESSION_FINISH: Policy.WORK,
    Method.ACTION_RUN: Policy.WORK,
    Method.UPDATE_CHECK_NOW: Policy.WORK,
    # It only records what the desktop app reports, but that record decides
    # when the app next checks for its update: a caller in a sandbox must not
    # be able to write it (a forged `current` would hold the check off 6 h).
    Method.UPDATE_APP_RESULT: Policy.WORK,
    Method.SESSION_REGISTER: Policy.WORK,
    Method.SESSION_RECORD: Policy.WORK,
    Method.HOOKS_HOST: Policy.WORK,
    Method.HOOKS_RUN: Policy.WORK,
    Method.HOOKS_QUEUE: Policy.WORK,
    Method.RECORDERS_FINISH: Policy.WORK,
    DAEMON_HOST_METHOD: Policy.WORK,
    Method.RUN_HOLD: Policy.WORK,
    Method.RUN_RELEASE: Policy.WORK,
    Method.MANIFEST_REFRESH: Policy.WORK,
    Method.OUTBOX_DRAIN: Policy.WORK,
    Method.BOX_WATCH: Policy.WORK,
    Method.TELEMETRY_SEND: Policy.WORK,
    # The mailbox writes and claims files for its session (Q2); a desktop
    # request runs a child that reads this user's credentials (Q6). Each of
    # their handlers already refused a sandboxed caller, in this same shape.
    Method.MAILBOX_POST: Policy.WORK,
    Method.MAILBOX_CLAIM: Policy.WORK,
    Method.MAILBOX_ANSWER: Policy.WORK,
    Method.DESKTOP_REQUEST: Policy.WORK,
    # Each starts or schedules a child on the caller's say (a status-line
    # fetch, the team note's sync, an import's worker); their handlers
    # already refused a sandboxed caller (Q4), as `_refuse_sandboxed`.
    Method.STATUSLINE_REFRESH: Policy.WORK,
    Method.NOTES_SYNC: Policy.WORK,
    Method.IMPORT_START: Policy.WORK,
}

#: A WORK method's answer to a caller it refuses for its confinement, in the
#: shape that method's clients already read as "not here, do it yourself";
#: every other WORK method answers error REFUSED with `reason: sandboxed`.
CONFINED_ANSWERS = {
    # `reason` is new beside `refused` (older clients read `refused` alone):
    # pi runs the lane itself on exactly this one.
    Method.HOOKS_HOST: {"refused": "a caller in a sandbox", "reason": RefusedReason.SANDBOXED},
    Method.HOOKS_RUN: {"refused": "a caller in a sandbox", "reason": RefusedReason.SANDBOXED},
    Method.HOOKS_QUEUE: {"refused": "a caller in a sandbox", "reason": RefusedReason.SANDBOXED},
    Method.SESSION_RECORD: {"recording": False, "reason": RefusedReason.SANDBOXED},
    # What a tap reads as "nothing hosted here" (`tap/record_client.py`).
    Method.SESSION_FINISH: {"recording": False, "finished": False},
    # What every tap reads as "do not register this session again"
    # (`service_link`'s `alive: false`), not a refusal to retry every 2 s.
    Method.SESSION_REGISTER: {"alive": False, "reason": RefusedReason.SANDBOXED},
    Method.OUTBOX_DRAIN: {"accepted": False, "reason": BackgroundRefusal.SANDBOXED},
    Method.BOX_WATCH: {"accepted": False, "reason": BackgroundRefusal.SANDBOXED},
    Method.TELEMETRY_SEND: {"accepted": False, "reason": BackgroundRefusal.SANDBOXED},
}


def confined(pid: int | None) -> bool:
    """A caller this service cannot rule out being more confined than itself:
    `caller.sandboxed` (Landlock included), or (Linux) another network namespace."""
    return caller.sandboxed(pid) or other_network(pid)


def screen(pid: int | None, start: str | None) -> str | None:
    """Why a WORK request from the process `pid` (started at `start`, where
    known) is refused, or None. `RefusedReason.CALLER_GONE` when that
    process has exited (a connection handed to a child: who asks can no
    longer be checked, plan D9), else `SANDBOXED` when `confined`. A check
    that fails refuses."""
    try:
        # pid 1 (a container's entrypoint) never reads as alive to `procid`.
        if pid is not None and pid > 1:
            from . import procid

            # As `_refuse_gone_caller` asks (never `os.kill(pid, 0)`: on
            # Windows that would end the caller).
            gone = procid.alive(pid, start) is False if start else not procid.exists(pid)
            if gone:
                return RefusedReason.CALLER_GONE
        return RefusedReason.SANDBOXED if confined(pid) else None
    except Exception:  # noqa: BLE001 -- unknown counts as confined
        return RefusedReason.SANDBOXED


_session_envs: dict | None = None


def session_envs() -> dict:
    """`{harness id: its session-id variable}`, from the harness registry
    (light: stdlib only). Read once; empty if the registry cannot be."""
    global _session_envs
    if _session_envs is None:
        try:
            from probe.harness import get_registry

            _session_envs = {h.id: h.session_env for h in get_registry().all() if h.session_env}
        except Exception as exc:  # noqa: BLE001 -- a context then just cannot name a session
            log(f"harness registry unreadable: {exc!r}")
            _session_envs = {}
    return _session_envs


def session_env_names() -> frozenset:
    """Every coding agent's session-id variable, which a request's `context`
    may set (`protocol.CONTEXT_ENV`)."""
    return frozenset(session_envs().values())


def _version() -> str:
    try:
        from probe import __version__

        return str(__version__)
    except Exception:  # noqa: BLE001 -- never a reason not to serve
        return "0.0.0.dev0"


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        sys.stderr.write(f"[{stamp}] probe-service[{os.getpid()}]: {message}\n")
        sys.stderr.flush()
    except (OSError, ValueError):
        pass


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value >= 0 else default


def peer_uid(sock: socket.socket) -> int | None:
    """The connecting process's uid, where the platform says (plan A6, S6).

    Linux: SO_PEERCRED. macOS: LOCAL_PEERCRED (SOL_LOCAL 0, option 1), which
    Python does not name but `getsockopt` reaches: a `struct xucred` whose
    first two u_ints are its version and the uid. Elsewhere None, and the 0600
    socket in a 0700 folder is the only check.
    """
    try:
        if hasattr(socket, "SO_PEERCRED"):
            raw = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
            return struct.unpack("3i", raw)[1]
        if sys.platform == "darwin":
            raw = sock.getsockopt(0, 1, 76)
            return struct.unpack("II", raw[:8])[1]
    except OSError:
        return None
    return None


class PidWatcher:
    """Calls back once when a pid exits. Event-driven where the kernel can be asked."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self._pidfds: dict[object, int] = {}
        self._kq = None
        self._kq_keys: dict[int, set] = {}
        self._callbacks: dict[object, tuple[int, str, Callable[[], None]]] = {}
        self._polled: set = set()
        self._poll_handle: asyncio.TimerHandle | None = None
        if hasattr(select, "kqueue") and hasattr(select, "KQ_FILTER_PROC"):
            try:
                self._kq = select.kqueue()
                loop.add_reader(self._kq.fileno(), self._drain_kqueue)
            except (OSError, NotImplementedError, ValueError):
                self._kq = None

    @property
    def mechanism(self) -> str:
        if hasattr(os, "pidfd_open"):
            return "pidfd"
        return "kqueue" if self._kq is not None else "poll"

    def watch(self, key: object, pid: int, start: str, callback: Callable[[], None]) -> None:
        self.cancel(key)
        self._callbacks[key] = (pid, start, callback)
        if hasattr(os, "pidfd_open"):
            try:
                fd = os.pidfd_open(pid)
            except ProcessLookupError:
                self.loop.call_soon(self._fire, key)
                return
            except OSError:
                self._poll(key)
                return
            self._pidfds[key] = fd
            self.loop.add_reader(fd, self._fire, key)
            return
        if self._kq is not None:
            keys = self._kq_keys.setdefault(pid, set())
            if not keys:
                try:
                    self._kq.control(
                        [
                            select.kevent(
                                pid,
                                filter=select.KQ_FILTER_PROC,
                                flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
                                fflags=select.KQ_NOTE_EXIT,
                            )
                        ],
                        0,
                        0,
                    )
                except ProcessLookupError:
                    del self._kq_keys[pid]
                    self.loop.call_soon(self._fire, key)
                    return
                except OSError:
                    del self._kq_keys[pid]
                    self._poll(key)
                    return
            keys.add(key)
            return
        self._poll(key)

    def _poll(self, key: object) -> None:
        self._polled.add(key)
        if self._poll_handle is None:
            self._poll_handle = self.loop.call_later(POLL_S, self._poll_tick)

    def _poll_tick(self) -> None:
        from . import procid

        self._poll_handle = None
        for key in list(self._polled):
            pid, start, _ = self._callbacks.get(key, (0, "", None))
            if procid.alive(pid, start) is False:
                self._fire(key)
        if self._polled:
            self._poll_handle = self.loop.call_later(POLL_S, self._poll_tick)

    def _drain_kqueue(self) -> None:
        try:
            events = self._kq.control(None, 64, 0)
        except OSError:
            return
        for ev in events:
            for key in list(self._kq_keys.pop(int(ev.ident), ())):
                self._fire(key)

    def _fire(self, key: object) -> None:
        entry = self._callbacks.get(key)
        self.cancel(key)
        if entry is not None:
            try:
                entry[2]()
            except Exception as exc:  # noqa: BLE001
                log(f"owner-exit callback failed: {exc!r}")

    def cancel(self, key: object) -> None:
        entry = self._callbacks.pop(key, None)
        fd = self._pidfds.pop(key, None)
        if fd is not None:
            with contextlib.suppress(Exception):
                self.loop.remove_reader(fd)
            with contextlib.suppress(OSError):
                os.close(fd)
        self._polled.discard(key)
        if entry is not None and self._kq is not None:
            pid = entry[0]
            keys = self._kq_keys.get(pid)
            if keys is not None:
                keys.discard(key)
                if not keys:
                    del self._kq_keys[pid]
                    with contextlib.suppress(OSError):
                        self._kq.control(
                            [select.kevent(pid, filter=select.KQ_FILTER_PROC, flags=select.KQ_EV_DELETE)],
                            0,
                            0,
                        )

    def close(self) -> None:
        for key in list(self._callbacks):
            self.cancel(key)
        if self._poll_handle is not None:
            self._poll_handle.cancel()
        if self._kq is not None:
            with contextlib.suppress(Exception):
                self.loop.remove_reader(self._kq.fileno())
            self._kq.close()


class Connection:
    def __init__(self, writer: asyncio.StreamWriter, peer_pid: int | None = None) -> None:
        self.writer = writer
        #: The connecting process, as the kernel says (plan D9); None where it cannot.
        self.peer_pid = peer_pid
        #: Its start time when it connected: the same process later, or not.
        self.peer_start: str | None = None
        #: `{pid, start_time}` once a registry change asked (`_caller_of`).
        self.peer_identity: dict | None = None
        #: In the order connections came (the service numbers them): the
        #: newest app connection is the one `app.check` goes to.
        self.serial = 0
        self.hello = False
        self.client: str | None = None
        self.keepalive = False
        self.topics: set = set()
        #: The sessions its SESSION_TOPICS subscription is for: sid -> the
        #: state folder it named (None: the default). Empty: every live one.
        self.sessions: dict = {}
        self.after_reply: Callable[[], None] | None = None

    def send_nowait(self, message: dict) -> bool:
        transport = self.writer.transport
        if transport is None or transport.is_closing():
            return False
        if transport.get_write_buffer_size() > MAX_SUBSCRIBER_BUFFER:
            transport.abort()
            return False
        self.writer.write(encode(message))
        return True

    async def send(self, message: dict) -> None:
        if self.send_nowait(message):
            with contextlib.suppress(ConnectionError, OSError):
                await self.writer.drain()


class Service:
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
        from .daemonhost import DaemonHost

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
        self.statusline = StatuslineRefresher(log=log, changed=self.reevaluate)
        #: The team note's sync, once per machine (`notes.sync`); none starts
        #: while an in-place update replaces the CLI's files.
        self.notes = NoteSync(log=log, changed=self.reevaluate, held=lambda: self.updater.applying)
        #: Approved imports' workers this service started or watches (`import.start`).
        self.imports = ImportWorkers(
            registry.path.parent / IMPORTS_NAME, log=log, changed=self._imports_changed,
            held=lambda: self.updater.applying,
        )
        self._import_count = 0
        #: An update installed a new CLI while an action ran: stop once it ends.
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
            from . import winpipe

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
        or in flight (a session's last sync must not be lost), or an import
        worker it watches. A run hold does not: with no service there is no
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
        if self.actions.running is not None or self.updater.holding():
            return True
        return any(conn.keepalive for conn in self.connections)

    def mutating_holder(self) -> dict | None:
        """What holds the one mutating slot (plan A5): an action, the update
        step that replaces the CLI's env, or a desktop request's change still
        running (until its child exits, past its deadline too: an Update or an
        uninstall must not replace the env under it, whatever wizard lock its
        context names). None when it is free."""
        return self.actions.busy_holder() or self.updater.busy_holder() or self.management.busy_holder()

    def _changed(self) -> None:
        """An action started or ended: what holds the service, and what
        `probe status` would say, may have changed."""
        self.status_cache.invalidate()
        if self._restart_pending and self.actions.running is None:
            self.stop(StopReason.UPDATE)
            return
        self.reevaluate()

    def _management_changed(self) -> None:
        """A desktop change's child exited: what holds the service (and the
        mutating slot) may have changed."""
        self.status_cache.invalidate()
        self.reevaluate()

    def _cycle_changed(self) -> None:
        """An update cycle started or ended: what holds the service may have
        changed, and so may every version `probe status` reports."""
        self.status_cache.invalidate()
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

    # -- the watch's view (crash-report plan B2) ---------------------------------

    def _updating(self) -> bool:
        """An update cycle runs (it drains the daemon workers, raises its
        barrier): what fails meanwhile is its hand-over, which the watch neither
        counts nor reports. Two attributes: cheap from any thread, never a file
        (the barrier itself is read by the watch's scan, `_barrier_up`)."""
        updater = getattr(self, "updater", None)
        return updater is not None and (updater.in_progress() or updater.applying)

    def _live_sessions(self) -> list:
        """Every live registered session (on the loop)."""
        now = time.time()
        return [s for s in self.registry.sessions.values() if s.alive(now, self.registry.ttl)]

    def _voters(self) -> list:
        """Every registered session whose agent runs, mode off included (it is
        never "live", but its opt-out counts): a report's consent (on the loop)."""
        now = time.time()
        out = []
        for session in self.registry.sessions.values():
            running = session.owner_live if session.owner is not None else now - session.heartbeat_at < self.registry.ttl
            if running:
                hosted = self._hosted_env(session.sid)
                out.append(Live(session.sid, hosted_env=dict(hosted) if hosted is not None else None,
                                report_env=session.report_env))
        return out

    async def _watch_receipts(self) -> dict:
        """The delivery receipts of each live session whose agent runs (the
        watch's `capture_stalled`), from the same cache `session.list` reads,
        asked for the same sessions it asks for (every registered one): the
        cache keeps the answers of the sessions its last read asked about."""
        live = {s.sid for s in self._live_sessions() if s.owner is None or s.owner_live}
        if not live:
            return {}
        envs = [rec.params.get("env") for rec in list(self.recorders.recordings.values())]
        found = await self.receipts.get(
            [s["sid"] for s in self.registry.listing()], journal_roots(envs), wait=RECEIPTS_WAIT_S,
            claims=self.recorders.claims(),
        )
        return {sid: receipts for sid, receipts in found.items() if sid in live}

    def _recorder_beats(self) -> list:
        """Each hosted recorder inside `hosted.record` that beat during this
        run of it (`tap.hosted.Controls.beat`; an older tap never does): the age
        of its last beat, for the watch's `stalled` (on the loop)."""
        now = time.monotonic()
        out = []
        for rec in list(self.recorders.recordings.values()):
            controls = rec.controls
            if rec.thread is None or not rec.thread.is_alive() or controls.stop.is_set() or controls.pause.is_set():
                continue
            beaten = getattr(controls, "beaten", None)
            if not rec.in_record or not isinstance(beaten, float) or beaten < rec.record_since:
                continue
            out.append({"sid": rec.sid, "beat_age_s": now - beaten, "owner": rec.params.get("owner")})
        return out

    def _hosted_env(self, sid: str) -> dict | None:
        """The environment a hosted session's recorder runs with (`session.record`'s)."""
        rec = self.recorders.recordings.get(sid)
        env = rec.params.get("env") if rec is not None else None
        return env if isinstance(env, dict) else None

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

    def _recorders_changed(self) -> None:
        self.status_cache.invalidate()
        self.hints.changed()
        self.reevaluate()

    def _imports_changed(self) -> None:
        """An import worker started or ended: one fewer is, for a deferred
        update, as a run's end is (`_run_gone`)."""
        count = len(self.imports.workers)
        fewer = count < self._import_count
        self._import_count = count
        self.status_cache.invalidate()
        if fewer:
            self.updater.session_ended()
        self.reevaluate()

    def _resume_recorders(self) -> None:
        if self.stop_reason is not None:
            return
        try:
            resumed = self.recorders.resume(self._register_saved)
        except Exception as exc:  # noqa: BLE001 -- capture falls back to `tap watch` on the next prompt
            log(f"recorder: resuming failed: {exc!r}")
            resumed = 0
        if resumed:
            log(f"recorder: {resumed} session(s) resumed")
            self.hints.changed()
        self.reevaluate()
        # The service before this one installed a new CLI and restarted onto it:
        # this one, the new code, follows the update up (its recorders resumed
        # on the newest installed tap already: `RecorderHost.resume`).
        with contextlib.suppress(Exception):
            if self.updater.take_followup():
                self._follow_update(tap=False)

    # -- after an update ------------------------------------------------------

    def _update_followup(self, restart: bool) -> None:
        """An update installed something (`Updater.followup`): what open
        sessions read follows it now (`followup.py`, plan C9). When this
        service restarts onto a new CLI first, it only wants the newest
        installed tap for the next one (`follow_installed`, saved); the next
        service does the rest (`take_followup`). Else, on the loop's next turn
        (never inside the cycle's own task): the renderer, the managed block,
        and a restart onto a newer installed tap."""
        if restart:
            with contextlib.suppress(Exception):
                wanted = self.recorders.follow_installed()
                if wanted is not None:
                    log(f"recorder: the next service loads tap {wanted[1]}, installed by this update")
            return
        if self._loop is not None:
            self._loop.call_soon(self._follow_update, True)

    def _follow_update(self, tap: bool = True) -> None:
        """The follow-up itself (see `followup.py`): the status-line renderer
        from the installed plugin copy (on a thread), the note sync with every
        agent's `agent-rules refresh` in each context the recorded sessions run
        in (`notes.sync` reconcile: the managed block), and, with `tap`, a
        restart onto the newest installed tap when it is newer than the one
        loaded (the recorders pause about a second and resume from their saved
        progress: nothing is lost or sent twice). Never raises."""
        if self.stop_reason is not None:
            return
        from . import followup
        from .protocol import NotesMode, is_agent_id

        recorded = self.recorders.contexts()
        contexts = followup.contexts([r.get("env") for r in recorded])
        # Each recorded agent's own instruction file; the CLI's default one
        # when nothing is recorded here.
        agents = sorted({r["harness"] for r in recorded if is_agent_id(r.get("harness"))})[:MAX_NOTE_AGENTS] or [""]

        def renderer() -> None:
            for context in contexts:
                changed = followup.sync_renderer({"HOME": str(paths.home()), **context})
                if changed:
                    log(f"update follow-up: the status line renderer refreshed ({', '.join(changed)})")

        task = asyncio.ensure_future(asyncio.to_thread(renderer))
        self._warming.add(task)
        task.add_done_callback(self._warming.discard)
        for context in contexts:
            with contextlib.suppress(Exception):
                self.notes.request(context, NotesMode.RECONCILE, agents, False)
        log(f"update follow-up: the managed block refreshes in {len(contexts)} context(s)")
        if tap:
            self._follow_tap()

    def _follow_tap(self, tries: int = FOLLOW_TAP_TRIES) -> None:
        """A restart onto the newest installed tap when it is newer than the
        one loaded (`follow_installed`). A newer folder its agent may still be
        writing (Codex: a few seconds after its install, `recorders._settled`)
        is asked about again once it would have settled, at most `tries`
        times. Never raises."""
        if self.stop_reason is not None:
            return
        with contextlib.suppress(Exception):
            wanted = self.recorders.follow_installed()
            if wanted is not None:
                log(f"recorder: tap {wanted[1]} is installed (this service runs {self.recorders.tap_version}): "
                    "restarting onto it")
                self._restart_for_update(StopReason.TAP_UPDATE)
            elif self.recorders.settling and tries > 1 and self._loop is not None:
                self._loop.call_later(TAP_SETTLE_S + 1.0, self._follow_tap, tries - 1)

    def _recorder_claimed(self, sid: str) -> None:
        """A recorder took (or let go of) its session's claim, on its own
        thread: the hint lane looks again now. It reads only sessions whose
        recorder holds the claim (`hints.followed`), and a lone session's
        `session.record` woke it before the claim was taken: it then slept with
        no timer, and that session's first prompt got its hint ~17 s late
        (live test E, 2026-10-24)."""
        loop = self._loop
        if loop is not None:
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self.hints.changed)

    def _register_saved(self, params: dict) -> None:
        """A resumed recorder's session, unless the registry kept it. One that
        is off is registered `off`: it never keeps this service alive."""
        sid = params.get("sid")
        if any(s.sid == sid for s in self.registry.sessions.values()):
            return
        mode = Mode.OFF if self._session_off(params) else params.get("mode")
        self._register(None, {**params, "mode": mode, "generation": int(time.time() * 1000)})

    def _session_off(self, params: dict) -> bool:
        """Is Probe off for this session (`capture_gate`): its switch reads
        `off`, or it was seen off and is not on again yet?"""
        from . import capture_gate

        with contextlib.suppress(Exception):
            if capture_gate.is_open(capture_gate.gaps_of(params)):
                return True
            return self.recorders.off(params)
        return False

    def _recorder_held(self, params: dict) -> None:
        """A recorded session's switch turned it off (its recorder holds it now):
        registered `off` under a new generation, so `session.list` and `probe
        doctor` say so and it keeps nothing alive. Its tap's own registration
        ended with its loop; the tap registers it again once the switch is on."""
        if self.stop_reason is not None:
            return
        with contextlib.suppress(Exception):
            self._register(None, {**params, "mode": Mode.OFF, "generation": int(time.time() * 1000)})

    def _action_finished(self, action: str) -> None:
        if action == Action.UPDATE:
            self.updater.after_update_action()

    def _restart_for_update(self, reason: str) -> None:
        """An update cycle installed a new CLI: this service is old code. Not
        under a running action, though, whose child would lose the rest of its
        events and read as stopped with the service: the action holds the one
        mutating slot meanwhile, and the stop follows the moment it ends."""
        if self.actions.running is not None:
            if not self._restart_pending:
                log("a new CLI is installed: restarting once the running action ends")
            self._restart_pending = True
            return
        self.stop(reason)

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

    def stop(self, reason: str) -> None:
        if self.stop_reason is not None or self._done is None:
            return
        self.stop_reason = reason
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
            from . import guard

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
                from . import client

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

        from . import client

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

    async def _keep_outbox(self) -> None:
        """Lift the outbox's pause when it no longer holds -- an older CLI's
        endless one, which an update releases at once, or a timed one whose
        end passed while nothing ran -- as this service starts (it does after
        every update) and every OUTBOX_LOOK_S after, and start the drainer
        for what it held.

        The look is one stat of the default outbox root, as this service's
        own environment names it: an outbox moved by a `PROBE_OUTBOX_DIR` or
        `XDG_STATE_HOME` set in the person's profile is lifted by their next
        `probe` command instead. The lift never waits on another process's
        append lock (`wait=False`). Only after a lift is the login shell read
        (`_outbox_login_env`), for the drainer's environment -- never this
        service's stripped one (no proxy, CA or config path: a drainer that
        could hold the outbox's lease failing forever) -- and the drainer
        starts only when it can be read, to an endpoint the stored login may
        go to. It drains the root queue; a credential queue's writes go with
        the next command or write. No report from here: the drainer reports,
        under the person's own switches. The rescue of stranded writes stays
        with the CLI, which reads `PROBE_OUTBOX_RESCUE` in the person's own
        environment."""
        period = _outbox_look_s()
        if period <= 0:
            return
        while self.stop_reason is None:
            try:
                lifted, root, held = await asyncio.to_thread(_lift_outbox_pause, None)
                if lifted:
                    log(f"lifted an outbox pause that no longer held ({held} write(s) queued)")
                    env = await _outbox_login_env() if held else None
                    if env is not None:
                        request = {"dir": root, "python": sys.executable, "cwd": None, "env": env}
                        answer = await asyncio.to_thread(
                            lambda: self.background.drain(request) if _drain_url_allowed(env)
                            else {"accepted": False, "reason": BackgroundRefusal.UNKNOWN_ENDPOINT})
                        log(f"outbox drainer: {answer.get('state') or answer.get('reason')}")
            except Exception as exc:  # noqa: BLE001 -- the next look tries again
                log(f"outbox look failed: {type(exc).__name__}")
            await asyncio.sleep(period)

    async def _shutdown(self) -> None:
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
        # Every recorder pauses (after the connections closed: a recorder's link
        # cannot end its session in the registry saved below).
        with contextlib.suppress(Exception):
            await self.recorders.close()
        with contextlib.suppress(Exception):
            await flushing
        self.actions.close()
        for part in (self.statusline, self.notes, self.imports):
            with contextlib.suppress(Exception):
                part.close()
        self.registry.save()

    # -- sessions ------------------------------------------------------------

    def _watch(self, session: Session) -> None:
        if session.owner is None or self.watcher is None:
            return
        key = (session.sid, session.generation)
        self.watcher.watch(
            key,
            session.owner["pid"],
            session.owner["start_time"],
            lambda: self._owner_exited(session.sid, session.generation),
        )

    def _owner_exited(self, sid: str, generation: int) -> None:
        dropped = self.registry.drop(sid, generation)
        if dropped is not None:
            self.registry.forget_daemon_owner(dropped.owner)
            log(f"session {sid} (generation {generation}): owner {dropped.owner['pid']} exited")
            self._emit(Topic.SESSION_ENDED, {"sid": sid, "generation": generation, "reason": EndReason.OWNER_EXIT})
            self.recorders.wake(sid)
            self._session_gone()
        self.reevaluate()

    def _session_gone(self) -> None:
        self.status_cache.invalidate()
        self.updater.session_ended()
        self.mailwatch.changed()

    def _watch_targets(self, extra: dict | None = None) -> set:
        """Every session a SESSION_TOPICS subscriber waits on: the ones it
        named, and every live registered one for a subscriber that named none.
        `extra` (sid -> state folder) counts sessions a subscription would add."""
        targets: set = set()
        default = None
        named = [conn.sessions for conn in self.connections if conn.topics & SESSION_TOPICS and conn.sessions]
        everyone = any(conn.topics & SESSION_TOPICS and not conn.sessions for conn in self.connections)
        for sessions in named + ([extra] if extra else []):
            for sid, state in sessions.items():
                if state is None:
                    default = default or default_state()
                targets.add(Target(sid, state or default))
        if everyone:
            now = time.time()
            for session in self.registry.sessions.values():
                if session.alive(now, self.registry.ttl):
                    if session.state_dir is None:
                        default = default or default_state()
                    targets.add(Target(session.sid, session.state_dir or default))
        return targets

    def _daemon_sessions(self) -> list:
        """`(sid, state folder)` of every live daemon-mode session an
        unconfined registrant registered, for the run-alert poller (which asks
        only for those whose worker wants it)."""
        now = time.time()
        return [
            (s.sid, s.state_dir or default_state())
            for s in sorted(self.registry.sessions.values(), key=lambda s: s.registered_at)
            if s.mode == Mode.DAEMON and s.unconfined and s.alive(now, self.registry.ttl)
        ]

    def _hint_sessions(self) -> list:
        """The sessions the hint lane reads (`hints.followed`): asked on its own
        thread, from snapshots of the recordings and the registry."""
        return hint_sessions(
            list(self.recorders.recordings.values()), list(self.registry.sessions.values()),
            now=time.time(), ttl=self.registry.ttl, default_state=default_state(),
        )

    def _hint_posted(self, sid: str) -> None:
        """From the hint lane's thread: a hint posted or withdrawn in `sid`'s
        mailbox. Its watchers hear at once, as for `mailbox.post`."""
        loop = self._loop
        if loop is not None:
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(
                    self._emit, Topic.MAILBOX_CHANGED, {"sid": sid, "parts": [MailboxPart.MESSAGES]}
                )

    def _schedule_expiry(self) -> None:
        if self._loop is None:
            return
        if self._expiry_handle is not None:
            self._expiry_handle.cancel()
            self._expiry_handle = None
        due = self.registry.next_expiry()
        if due is not None:
            delay = max(0.0, due - time.time()) + 0.01
            self._expiry_handle = self._loop.call_later(delay, self._expire)

    def _expire(self) -> None:
        self._expiry_handle = None
        for session in self.registry.expired():
            if self.registry.drop(session.sid, session.generation) is not None:
                log(f"session {session.sid}: heartbeat lapsed")
                self._emit(
                    Topic.SESSION_ENDED,
                    {"sid": session.sid, "generation": session.generation, "reason": EndReason.EXPIRED},
                )
                self._session_gone()
        self._schedule_expiry()
        self.reevaluate()

    # -- events --------------------------------------------------------------

    def _emit(self, topic: str, payload: dict) -> None:
        """To every subscriber of `topic`; `app.check` goes to one app only (`_send_app_check`)."""
        message = event(topic, payload)
        scoped = topic in SESSION_TOPICS
        for conn in list(self.connections):
            if topic in conn.topics and (not scoped or not conn.sessions or payload.get("sid") in conn.sessions):
                conn.send_nowait(message)

    def _updater_emit(self, topic: str, payload: dict) -> None:
        """The updater's events; at a cycle's end, the lifeboat's part (plan
        fool-proof-updates B1, B5): its `current/` copy becomes known-good
        when this cycle proved it, and what it did is reported."""
        self._emit(topic, payload)
        if topic == Topic.UPDATE_DONE and self._loop is not None:
            self._loop.run_in_executor(None, _lifeboat_after, dict(payload))
            self.statepost.look_for_acted()

    def _app_connections(self) -> list:
        """The desktop app's open connections (`service.hello` client `app`)."""
        return [c for c in self.connections if c.hello and c.client == Client.APP]

    def _app_listeners(self) -> list:
        """The app connections that take `app.check`."""
        return [c for c in self._app_connections() if Topic.APP_CHECK in c.topics]

    def _app_target(self) -> int | None:
        """The one app connection a hand-off goes to: the newest that takes `app.check`."""
        listeners = self._app_listeners()
        return max(c.serial for c in listeners) if listeners else None

    def _send_app_check(self, serial: int, payload: dict) -> bool:
        """`app.check` to that one connection; False when it is gone or closing."""
        for conn in self._app_listeners():
            if conn.serial == serial:
                return conn.send_nowait(event(Topic.APP_CHECK, payload))
        return False

    # -- connections ---------------------------------------------------------

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        sock = writer.get_extra_info("socket")
        uid = peer_uid(sock) if sock is not None else None
        if uid is not None and uid != self.expected_uid:
            log(f"refused a connection from uid {uid}")
            writer.close()
            return
        if paths.WINDOWS:
            from . import winpipe

            peer = winpipe.peer_of(writer)  # the pipe's DACL lets only this user in
        else:
            peer = caller.peer_pid(sock) if sock is not None else None
        conn = Connection(writer, peer)
        conn.serial = next(self._serials)
        if conn.peer_pid is not None and os.path.isdir("/proc/self"):
            # Linux: one /proc read. Elsewhere it would be a `ps` per connection
            # on the loop: there `_action_run` checks only that the pid exists.
            from . import procid

            conn.peer_start = procid.start_time(conn.peer_pid)
        self.connections.add(conn)
        try:
            while self.stop_reason is None:
                try:
                    line = await reader.readuntil(b"\n")
                except asyncio.IncompleteReadError:
                    break
                except asyncio.LimitOverrunError:
                    await conn.send(
                        error(None, RpcError(ErrorCode.INVALID_REQUEST, "invalid request: line over 1 MiB"))
                    )
                    break
                except (ConnectionError, OSError):
                    break
                if not line.strip():
                    continue
                reply = await self.dispatch(conn, line)
                await conn.send(reply)
                if conn.after_reply is not None:
                    action, conn.after_reply = conn.after_reply, None
                    action()
        finally:
            self.connections.discard(conn)
            with contextlib.suppress(Exception):
                writer.close()
            if conn.client == Client.APP:
                # The app check it was handed and never reported is failed (due again).
                self.updater.app_gone(conn.serial)
            if conn.keepalive:
                self.reevaluate()

    async def dispatch(self, conn: Connection, line: bytes) -> dict:
        try:
            id_, method, params = parse_request(line)
        except RpcError as exc:
            id_ = (exc.data or {}).get("id")
            exc.data = None
            return error(id_, exc)
        if not conn.hello and method != Method.HELLO:
            return error(id_, RpcError(ErrorCode.HELLO_REQUIRED, "hello_required: send service.hello first"))
        if method not in METHODS and method not in LOCAL_METHODS:
            return error(id_, RpcError(ErrorCode.UNKNOWN_METHOD, f"unknown method: {method}"))
        if METHOD_POLICY.get(method, Policy.WORK) == Policy.WORK:
            # Before the handler, whatever it checks itself: one rule for
            # every method that runs or stores work (`Policy.WORK`). Inline,
            # as the hook methods always checked: /proc reads on Linux, a
            # `sandbox_check` call on macOS, never a process.
            refusal = screen(conn.peer_pid, conn.peer_start)
            if refusal is not None:
                answer = CONFINED_ANSWERS.get(method)
                if answer is not None:
                    return result(id_, dict(answer))
                if refusal == RefusedReason.CALLER_GONE:
                    return error(id_, RpcError(
                        ErrorCode.REFUSED,
                        "refused: the process that opened this connection has exited; connect again",
                        {"reason": RefusedReason.CALLER_GONE},
                    ))
                return error(id_, RpcError(
                    ErrorCode.REFUSED, "refused: a caller in a sandbox", {"reason": RefusedReason.SANDBOXED}
                ))
        handler = self._handlers()[method]
        try:
            value = handler(conn, params)
            if asyncio.iscoroutine(value):
                value = await value
        except RpcError as exc:
            return error(id_, exc)
        except Exception as exc:  # noqa: BLE001 -- one bad request never stops the service
            self._internal_error(method, exc)
            return error(id_, RpcError(ErrorCode.REFUSED, "internal error", {"reason": RefusedReason.INTERNAL}))
        return result(id_, value)

    def _internal_error(self, method: str, exc: Exception) -> None:
        """A handler's own exception (a bug, answered `internal error`): logged
        with its traceback, and one event of `service_error` (plan B2)."""
        import traceback

        text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        log_traceback(log, f"{method} failed: {exc!r}", text, gate=self._tracebacks,
                      key=("request", method, type(exc).__name__))
        self.watch.note(Family.SERVICE_ERROR, "request_error", facts={
            "method": method, "type": type(exc).__name__, "traceback": text,
        })

    def _handlers(self) -> dict:
        return {
            Method.HELLO: self._hello,
            Method.STATUS: self._status,
            Method.STOP: self._stop,
            Method.SESSION_REGISTER: self._register,
            Method.SESSION_END: self._end,
            Method.SESSION_LIST: self._list,
            Method.EVENTS_SUBSCRIBE: self._subscribe,
            Method.STATUS_GET: self._status_get,
            Method.ACTION_RUN: self._action_run,
            Method.ACTION_STATUS: lambda conn, params: self.actions.status(params),
            Method.ACTION_EVENTS: lambda conn, params: self.actions.events(params),
            Method.ACTION_CANCEL: lambda conn, params: self.actions.cancel(params),
            Method.UPDATE_STATUS: lambda conn, params: self.updater.public(),
            Method.UPDATE_CHECK_NOW: self._check_now,
            Method.UPDATE_APP_RESULT: lambda conn, params: self.updater.app_result(need_app_result(params)),
            Method.HOOKS_HOST: self._hooks_host,
            Method.HOOKS_RUN: self._hooks_run,
            Method.HOOKS_QUEUE: self._hooks_queue,
            Method.SESSION_RECORD: self._record,
            Method.SESSION_RECORDING: self._recording,
            Method.SESSION_FINISH: lambda conn, params: self.recorders.finish(params),
            Method.RECORDERS_FINISH: self._recorders_finish,
            DAEMON_HOST_METHOD: self._daemon_host,
            Method.RUN_HOLD: self._run_hold,
            Method.RUN_RELEASE: self._run_release,
            Method.MANIFEST_REFRESH: self._manifest_refresh,
            Method.MAILBOX_POST: self._mailbox_post,
            Method.MAILBOX_CLAIM: self._mailbox_claim,
            Method.MAILBOX_ANSWER: self._mailbox_answer,
            Method.DESKTOP_REQUEST: self._desktop_request,
            Method.OUTBOX_DRAIN: self._outbox_drain,
            Method.BOX_WATCH: self._box_watch,
            Method.TELEMETRY_SEND: self._telemetry_send,
            Method.STATUSLINE_REFRESH: self._statusline_refresh,
            Method.NOTES_SYNC: self._notes_sync,
            Method.IMPORT_START: self._import_start,
        }

    # -- methods -------------------------------------------------------------

    def _hello(self, conn: Connection, params: dict) -> dict:
        client = need_choice(params, "client", CLIENTS)
        need_str(params, "client_version", max_len=64)
        api = params.get("api")
        if not isinstance(api, int) or isinstance(api, bool):
            raise invalid_params("api must be an integer")
        if api != API_VERSION:
            raise RpcError(
                ErrorCode.UNSUPPORTED_API,
                f"unsupported_api: this service speaks api {API_VERSION}",
                {"supported": [API_VERSION]},
            )
        keepalive = need_bool(params, "keepalive")
        conn.hello = True
        conn.client = client
        conn.keepalive = keepalive
        self.reevaluate()
        return {
            "service_version": self.version,
            "api": API_VERSION,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
            "caps": sorted(CAPS),
            # The env it runs from: a rebuild of the same version lives in a
            # folder of its own (`<v>+g<N>`), which the guard tells apart by it.
            "env": self.env,
        }

    def _status(self, conn: Connection, params: dict) -> dict:
        until = None
        if self.discovering:
            until = self.started_at + self.discovery_s
        return {
            "service_version": self.version,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
            "sessions": self.registry.alive_count(),
            "app_clients": len(self._app_connections()),
            "update": self.updater.public(),
            "actions": {"running": self.actions.busy_holder()},
            "discovering_until": until,
            "hook_hosts": self.hookhosts.public(),
            "hook_queue": self.hook_queue.public(),
            "recorders": self.recorders.public(),
            "workers": self.workers.public(),
            "daemon_host": self.workers.daemon_host.public() if self.workers.daemon_host is not None else None,
            "runs": self.runs.public(),
            # The sessions whose mailbox and held questions a subscriber waits on (Q2).
            "watched": len(self._watch_targets()),
            "background": self.background.public(),

            "imports": self.imports.public(),
            "statusline": self.statusline.public(),
            "notes": self.notes.public(),
            # What fails here and what was reported (crash-report plan B2).
            "watch": self.watch.public(),
        }

    def _stop(self, conn: Connection, params: dict) -> dict:
        if self.updater.in_progress():
            raise RpcError(ErrorCode.REFUSED, "refused: an update is running", {"reason": RefusedReason.UPDATING})
        if self.actions.running is not None:
            raise RpcError(
                ErrorCode.REFUSED, "refused: an action is running", {"reason": RefusedReason.ACTION_RUNNING}
            )
        conn.after_reply = lambda: self.stop(StopReason.STOP)
        return {"stopping": True}

    def _register(self, conn: Connection, params: dict) -> dict:
        sid = need_str(params, "sid", max_len=128)
        harness = need_str(params, "harness", max_len=64)
        mode = need_choice(params, "mode", MODES)
        owner = need_owner(params)
        generation = need_int(params, "generation")
        state_dir = need_state_dir(params)
        # Whether the registrant's environment allows automatic reports (plan
        # B2): a bool, else unsaid (an older registrant: None, read as no).
        report_env = params.get(REPORT_ENV)
        report_env = report_env if isinstance(report_env, bool) else None
        who = self._caller_of(conn)
        try:
            reg = self.registry.register(sid, harness, mode, owner, generation, state_dir, report_env, caller=who)
        except RpcError as exc:
            self._log_unbound(exc, Method.SESSION_REGISTER, sid, who)
            raise
        # Whether the service may poll for it with the user's key (`alertpoll`):
        # never for a registrant in a sandbox, which names the state folder the
        # answers go to. `session.record` refused those already; None: this service.
        reg.session.unconfined = conn is None or not caller.sandboxed(conn.peer_pid)
        if reg.outcome != Outcome.DEAD:
            # Every register, a heartbeat's too: after a restart the sessions
            # come back from `sessions.json` unconfirmed, and only their next
            # register says they may be polled for (both start only once).
            self.alerts.changed()
            self.mailwatch.changed()
            # A session's mode may have moved (off -> on): the hint lane looks again.
            self.hints.changed()
        now = time.time()
        if reg.outcome in (Outcome.NEW, Outcome.REPLACED):
            if reg.previous is not None and self.watcher is not None:
                self.watcher.cancel((reg.previous.sid, reg.previous.generation))
            self._watch(reg.session)
            log(
                f"session {sid} registered ({reg.outcome}, {harness}, {mode}, generation {generation}, "
                f"owner {owner['pid'] if owner else 'heartbeat'})"
            )
            self._emit(
                Topic.SESSION_STARTED,
                {
                    "sid": sid,
                    "harness": harness,
                    "mode": mode,
                    "generation": generation,
                    "alive": reg.session.alive(now, self.registry.ttl),
                },
            )
            self.status_cache.invalidate()
        self._schedule_expiry()
        self.reevaluate()
        return {"alive": reg.session.alive(now, self.registry.ttl) if reg.outcome != Outcome.DEAD else False}

    async def _hooks_host(self, conn: Connection, params: dict) -> dict:
        """`hooks.host` (plan A0): never for a caller in a sandbox, whose events
        (and the interpreter it names) would run outside it. The start itself
        (a folder check, a process start) runs on a thread (`_start_host`)."""
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        return await self._start_host(params)

    def _pool(self, name: str, workers: int):
        pool = getattr(self, name)
        if pool is None:
            from concurrent.futures import ThreadPoolExecutor

            pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix=name.strip("_").replace("_", "-"))
            setattr(self, name, pool)
        return pool

    async def _offload(self, pool: str, workers: int, slots, busy: str, wait: float, fn, *args, late=None):
        """`fn(*args)` on one of `pool`'s threads, never this loop: `(True,
        its value)`, or `(False, None)` when it is not done within `wait`
        (`late`, when given, then gets its value on this loop once it is).

        Admission is a slot of `slots`, taken here (`{"refused": busy}` at once
        when none is free) and given back only by the thread, when it has run
        the item: so the pool never holds more work items than there are slots,
        however many callers come and go while its threads are stalled. A
        caller past its wait gives up on the answer but never cancels the item
        (a cancelled item would keep its place in the queue with its slot
        given back); `fn` drops work whose deadline passed the moment a thread
        takes it (`hookhosts.run_event`)."""
        if not slots.acquire(blocking=False):
            return True, {"refused": busy}
        once = threading.Lock()  # the slot goes back exactly once

        def give_back() -> None:
            if once.acquire(blocking=False):
                slots.release()

        def held():
            try:
                return fn(*args)
            finally:
                give_back()

        try:
            future = asyncio.wrap_future(self._pool(pool, workers).submit(held))
        except RuntimeError:
            # Shut down (the service is stopping), or no thread would start for
            # an item already queued: that item still gives its slot back when
            # it runs, so never twice (a second release raises ValueError).
            give_back()
            return True, {"refused": "the service could not take it (stopping, or no thread would start)"}
        done, _ = await asyncio.wait({future}, timeout=max(wait, 0.0))
        if done:
            return True, future.result()
        future.add_done_callback(lambda settled: _settled(settled, late))
        return False, None

    async def _start_host(self, params: dict) -> dict:
        done, answer = await self._offload(
            "_host_starts", HOST_START_THREADS, self._host_slots, "busy: too many host starts in flight",
            HOST_START_WAIT_S, self.hookhosts.host, params,
        )
        return answer if done else {"refused": "the host is still starting"}

    async def _hooks_run(self, conn: Connection, params: dict) -> dict:
        """`hooks.run` (plan D38): one hook event of a harness that has no hooks
        of its own (pi), run for a Probe plugin folder exactly as its dispatcher
        runs it (`hookhosts.run_event`), and the merged output back. Same
        caller checks as `hooks.host`: the peer's uid (every connection), never
        a caller in a sandbox (or one whose pid the kernel will not name), whose
        event would run outside it with the environment it sent; and only a
        complete Probe plugin folder, checked on the thread (it reads files
        the request names: never on this loop, which every client waits on).
        A folder that had no warm host gets one for its next event, also when
        the event's answer comes past its caller's wait (`late`): where the
        kernel has no `os.waitid` (macOS) stopping an overrun outlasts
        ANSWER_GRACE_S."""
        request = need_hook_run(params)
        request["deadline"] = time.monotonic() + request["timeout_s"]
        refused = _hook_run_refusal(request["lane"], params["payload"].get("tool_name"))
        if refused is not None:
            return {"refused": refused}
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        # The folder's check reads files the request names: on the thread too,
        # and the answer by the deadline whatever that check costs.
        done, answer = await self._offload(
            "_hook_runs", MAX_HOOK_RUNS, self._hook_slots, "busy: too many hook events in flight",
            request["deadline"] - time.monotonic() + ANSWER_GRACE_S, run_event, request, conn.peer_pid,
            late=lambda late_answer: self._warm_after(request, late_answer),
        )
        if not done:
            self._note_hook_run(request, None)
            return timed_out_answer()
        if "refused" in answer:
            return answer
        self._note_hook_run(request, answer)
        self._warm_after(request, answer)
        # Past what a client reads in one line: stderr goes first, then stdout,
        # each marked cut, so an intact stdout keeps its verdict while it fits.
        for stream in ("stderr", "stdout"):
            if len(encode(result(0, answer))) <= MAX_LINE_BYTES:
                break
            answer = {**answer, stream: "", f"{stream}_truncated": True, "truncated": True}
        return answer

    async def _hooks_queue(self, conn: Connection, params: dict) -> dict:
        """`hooks.queue` (plan D36): a session's dispatcher that no warm host
        took an event from ran there only what the agent waits on, and hands
        this the event's record-keeping routes, to run once by its id
        (`hookqueue.HookQueue`: `{"queued": true, "duplicate": bool}`, or
        `{"refused": why}`, and the dispatcher then runs them itself). Never
        from a caller in a sandbox (as `hooks.run`: the event would run outside
        it, with the environment it sent). Stored on a thread (a file write),
        run on the queue's own, never on this loop."""
        item = need_hook_queue(params)
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        done, answer = await self._offload(
            "_queue_stores", 1, self._queue_slots, "busy: too many hook events queued at once",
            QUEUE_STORE_WAIT_S, self.hook_queue.store, item,
        )
        if not done:
            # Still being written, and its caller long gone (it wrote the
            # event beside it, or ran it): the store goes on and runs it once.
            log(f"hooks.queue {item['id']}: still storing after {QUEUE_STORE_WAIT_S}s")
            return {"queued": True, "duplicate": False}
        return answer

    def _note_hook_run(self, request: dict, answer: dict | None) -> None:
        """`hooks.run` ran out of time (`answer` None: not even an answer), or
        the warm host running its event was lost: one event of `hook_host`
        (plan B2). Never its exit code: 2 is a Stop message delivered (or a
        veto), and the dispatcher turns its own failures into 0 (Codex rev-3 #3)."""
        if answer is None or answer.get("timed_out"):
            reason = "timed_out"
        elif answer.get("via") == Via.HOST and answer.get("exit_code") is None:
            reason = "host_lost"
        else:
            return
        self.watch.note(Family.HOOK_HOST, reason, facts={
            "lane": request["lane"], "via": None if answer is None else answer.get("via"),
            "timeout_s": request["timeout_s"],
        }, env=request.get("env"))  # the session's own: its opt-out counts

    def _warm_after(self, request: dict, answer: dict) -> None:
        """After `hooks.run`'s event: its folder's warm host when it ran without one."""
        if (
            "refused" not in answer
            and answer.get("via") != Via.HOST
            and request["lane"] not in UNHOSTED_LANES
            and self.stop_reason is None
        ):
            root = request["root"]
            asyncio.get_running_loop().call_soon(lambda: self._warm(root))

    def _queue_changed(self) -> None:
        """From any thread: queued hook events started or stopped holding the service."""
        loop = self._loop
        if loop is not None and not loop.is_closed():
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self.reevaluate)

    def _warm_soon(self, root: str) -> None:
        """From the queue's thread: `root`'s warm host for its next event."""
        loop = self._loop
        if loop is not None and not loop.is_closed():
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self._warm, root)

    def _warm(self, root: str) -> None:
        """Start `root`'s warm host for its next `hooks.run` (`hooks.host`), at
        most every WARM_EVERY_S, on a thread (`_start_host`): never waited on."""
        now, last = time.monotonic(), self._warmed.get(root)
        if self.stop_reason is not None or (last is not None and now - last < WARM_EVERY_S):
            return
        self._warmed[root] = now
        task = asyncio.ensure_future(self._warm_task(root))
        self._warming.add(task)
        task.add_done_callback(self._warming.discard)

    async def _warm_task(self, root: str) -> None:
        try:
            await self._start_host({"root": root})
        except Exception as exc:  # noqa: BLE001 -- only the next event's speed is at stake
            log(f"hook host for {root} would not start: {exc!r}")

    def _record(self, conn: Connection, params: dict) -> dict:
        """`session.record` (plan A2): `session.register`, then this session's
        recorder on a thread here. `{recording: false, ...}` (the tap then
        starts its own `tap watch`) when it cannot be: a caller in a sandbox, no owner, no loadable tap, or a newer tap than the one loaded
        (`restart: true`: the service restarts onto it, the caller asks the
        next one)."""
        if caller.sandboxed(conn.peer_pid):
            # Its recorder would run here, outside that sandbox, with the
            # environment (PATH included) the caller sent.
            return {"recording": False, "reason": "sandboxed"}
        refused = self.recorders.check(params)
        if refused is not None:
            if refused.get("restart"):
                self._restart_for_update(StopReason.TAP_UPDATE)
            return refused
        # Probe off: taken (no `tap watch` records it instead), held, and
        # registered `off`, which is never alive and never an owner gone: before
        # this a `tap watch` of an off session asked every minute and was told
        # `owner_gone` each time, while it recorded on (live test, bug F).
        off = self._session_off(params)
        if not self.recorders.live(params.get("sid")):
            # Recorded here already: its link keeps the registration (a second
            # generation from here would make the link step back for good).
            registered = self._register(conn, {**params, "mode": Mode.OFF} if off else params)
            if registered.get("alive") is False and not off:
                return {"recording": False, "reason": "owner_gone"}
        answer = self.recorders.record(params)
        self.hints.changed()
        return answer

    def _recording(self, conn: Connection, params: dict) -> dict:
        """`session.recording`: is the session recorded here now? Its switch is
        looked at first, so a CLI that just moved it (`probe session state`)
        has its gap opened or closed at this moment (`capture_gate`). `off`:
        Probe is off for it, so nothing of it is captured."""
        sid = params.get("sid")
        self.recorders.look(sid)
        answer = {"recording": self.recorders.recording(sid)}
        if self.recorders.held_off(sid):
            answer["off"] = True
        return answer

    def _end(self, conn: Connection, params: dict) -> dict:
        sid = need_str(params, "sid", max_len=128)
        generation = need_int(params, "generation")
        who = self._caller_of(conn)
        try:
            removed = self.registry.end(sid, generation, who)
        except RpcError as exc:
            self._log_unbound(exc, Method.SESSION_END, sid, who)
            raise
        if removed is not None:
            if self.watcher is not None:
                self.watcher.cancel((removed.sid, removed.generation))
            log(f"session {sid} ended")
            self._emit(Topic.SESSION_ENDED, {"sid": sid, "generation": removed.generation, "reason": EndReason.END})
            self.recorders.wake(sid)
            self._session_gone()
            self._schedule_expiry()
            self.reevaluate()
        return {}

    async def _list(self, conn: Connection, params: dict) -> dict:
        """`session.list`: every registered session, each with its delivery
        `receipts` (plan D29; `receipts.py`), and `harnesses`, the same per
        agent. `receipts: false` leaves both out (a caller that only counts)."""
        sessions = self.registry.listing()
        if not need_bool(params, "receipts", default=True):
            return {"sessions": sessions}
        envs = [rec.params.get("env") for rec in list(self.recorders.recordings.values())]
        found = await self.receipts.get(
            [s["sid"] for s in sessions], journal_roots(envs), wait=RECEIPTS_WAIT_S, claims=self.recorders.claims()
        )
        for session in sessions:
            session["receipts"] = found.get(session["sid"])
        return {"sessions": sessions, "harnesses": by_harness(sessions)}

    async def _subscribe(self, conn: Connection, params: dict) -> dict:
        """`events.subscribe`. For a SESSION_TOPICS topic, `sessions` (and the
        `state_dir` they keep their files under) say whose mailbox to watch;
        the answer comes once their files are baselined (`MailWatch.baseline`),
        so a change after it is an event, and a refused one watches nothing
        new. Watching only reads, so a caller in a sandbox may watch too, but
        only live registered sessions, where they registered their files. At
        most MAX_SUBSCRIBE_SESSIONS a connection, MAX_TARGETS a machine."""
        topics = params.get("topics")
        if not isinstance(topics, list) or not topics or not all(isinstance(t, str) for t in topics):
            raise invalid_params("topics must be a non-empty list of topic names")
        unknown = sorted(set(topics) - TOPICS)
        if unknown:
            raise invalid_params(f"unknown topics {unknown}")
        sessions = need_sessions(params)
        state_dir = need_state_dir(params)
        if not set(topics) & SESSION_TOPICS and not sessions:
            conn.topics |= set(topics)  # nothing new to watch: no baseline either
            return {}
        added = dict.fromkeys(sessions or (), state_dir)
        if await asyncio.to_thread(caller.sandboxed, conn.peer_pid):
            # Watching only reads, but a caller in a sandbox names only live
            # registered sessions, watched where they keep their files: never
            # a folder of its choosing (a hung mount, a planted FIFO), never
            # every session's held questions.
            if not sessions:
                raise invalid_params("a caller in a sandbox must name its sessions")
            now = time.time()
            for sid in sessions:
                registered = self.registry.sessions.get(sid)
                if registered is None or not registered.alive(now, self.registry.ttl):
                    raise invalid_params(f"session {sid!r} is not registered")
                added[sid] = registered.state_dir
        if len({**conn.sessions, **added}) > MAX_SUBSCRIBE_SESSIONS:
            raise invalid_params(f"a connection watches at most {MAX_SUBSCRIBE_SESSIONS} sessions")
        if len(self._watch_targets(added)) > MAX_TARGETS:
            raise RpcError(ErrorCode.BUSY, f"busy: more than {MAX_TARGETS} sessions are watched")
        before = (set(conn.topics), dict(conn.sessions))
        conn.topics |= set(topics)
        conn.sessions.update(added)
        if not await self.mailwatch.baseline():
            conn.topics, conn.sessions = before  # refused: it watches nothing new
            raise RpcError(ErrorCode.BUSY, "busy: the watched sessions' files could not be read in time")
        return {}

    async def _status_get(self, conn: Connection, params: dict) -> dict:
        refresh = need_bool(params, "refresh")
        max_age = params.get("max_age")
        if max_age is not None and (
            not isinstance(max_age, (int, float)) or isinstance(max_age, bool) or not 0 <= max_age <= 3600
        ):
            raise invalid_params("max_age must be a number of seconds from 0 to 3600")
        return await self.status_cache.get(self._context(params), refresh=refresh, max_age=max_age)

    def _context(self, params: dict) -> dict:
        """The request's context as the child's environment, its endpoint
        checked (plan D10): the CLI config's stored token follows
        `PROBE_BASE_URL`, so a child runs only with an https endpoint that
        config already names. Anything else is refused, and the app runs the
        CLI itself, with its own environment, as it does on any refusal."""
        env = need_context(params, session_env_names())
        url = env.get(BASE_URL_ENV)
        if url is not None and not caller.known_endpoint(url, env):
            raise invalid_params(
                "base_url must be an https endpoint this machine's Probe CLI is already signed in to"
            )
        return env

    def _caller_of(self, conn: Connection | None) -> dict | str | None:
        """Who a registry change comes from (#3360): `registry.SERVICE` for this
        service's own (no connection, or one from this very process: a hosted
        recorder's link), else the connecting process as the kernel names it,
        `{pid, start_time}`; None when it names none. The start time is read
        once a connection where /proc did not give it at connect (`ps`)."""
        if conn is None or conn.peer_pid == self.pid:
            return SERVICE
        if conn.peer_pid is None:
            return None
        if conn.peer_identity is None:
            from . import procid

            start = conn.peer_start or procid.start_time(conn.peer_pid)
            conn.peer_identity = {"pid": conn.peer_pid, "start_time": start or ""}
        return dict(conn.peer_identity)

    def _log_unbound(self, exc: RpcError, method: str, sid: str, who: dict | str | None,
                     now: float | None = None) -> None:
        """Log a `not_registrant` refusal, once per (session, process) every
        REFUSAL_LOG_S: a newer `tap watch` of a session another agent still
        runs is refused at every retry (every 2 s) until that agent exits."""
        if isinstance(exc.data, dict) and exc.data.get("reason") == Bound.NOT_REGISTRANT:
            pid = who.get("pid") if isinstance(who, dict) else who
            if self._first_refusal((sid, pid), now):
                log(f"refused {method} of {sid} from pid {pid}: not the process that registered it"
                    f" (said once per {REFUSAL_LOG_S / 60:g} min)")

    def _first_refusal(self, key: tuple, now: float | None = None) -> bool:
        """Is `key`'s refusal the first in REFUSAL_LOG_S (then it is remembered)?"""
        now = time.monotonic() if now is None else now
        last = self._refusals_logged.get(key)
        if last is not None and now - last < REFUSAL_LOG_S:
            return False
        if len(self._refusals_logged) >= MAX_REFUSALS_LOGGED:
            self._refusals_logged = {k: t for k, t in self._refusals_logged.items() if now - t < REFUSAL_LOG_S}
            if len(self._refusals_logged) >= MAX_REFUSALS_LOGGED:
                self._refusals_logged.clear()
        self._refusals_logged[key] = now
        return True

    def _caller_session(self, conn: Connection, env: dict, seen: tuple | None = None) -> tuple:
        """`(session, daemon sid)`: the registered session the caller runs
        inside (plan D9), or None, and the id of a session the Probe daemon
        records that it runs inside, or None. Its process ancestry passes a
        session's owner (pid and start time), or (Linux) its environment names
        a registered session. EVERY match counts (#3360): a daemon-mode
        session, or an agent process once registered in daemon mode that still
        runs (`Registry.daemon_owner`, which neither a `session.end` nor a
        later register undoes), makes it a daemon caller, so a registration
        forged beside the real one cannot hide it. A session found this way
        that the context did not name joins `env` under its harness's
        variable, so `probe.core.run` refuses what it refuses there.
        `seen`: `(ancestry, environ)` read already, off the loop (`_caller_seen`)."""
        names = session_envs()
        found: Session | None = None
        daemon: str | None = None
        if conn.peer_pid is not None:
            # No owner to meet: no walk (`ps` per process on macOS, on this loop).
            walk = seen is not None or self.registry.daemon_owners or self.registry.owners()
            chain = (seen[0] if seen is not None else caller.ancestry(conn.peer_pid)) if walk else []
            for pid, start in chain:
                for session in self.registry.owned(pid, start):
                    if found is None or (session.mode == Mode.DAEMON and found.mode != Mode.DAEMON):
                        found = session
                    if session.mode == Mode.DAEMON and daemon is None:
                        daemon = session.sid
                remembered = self.registry.daemon_owner(pid, start)
                if remembered is not None and daemon is None:
                    daemon = remembered["sid"]
            carried = seen[1] if seen is not None else caller.environ(conn.peer_pid, frozenset(names.values()))
            now = time.time()
            for value in carried.values():
                candidate = self.registry.sessions.get(value)
                if candidate is not None and candidate.alive(now, self.registry.ttl):
                    if found is None:
                        found = candidate
                    if candidate.mode == Mode.DAEMON and daemon is None:
                        daemon = candidate.sid
                if daemon is None and self.registry.daemon_agent_runs(value):
                    daemon = value
        if found is not None:
            name = names.get(found.harness)
            if name and not any(env.get(n) for n in names.values()):
                env[name] = found.sid
        return found, daemon

    def _caller_seen(self, conn: Connection) -> tuple:
        """`(ancestry, environ)` of the caller, for `_caller_session`: `ps` on
        macOS, so a caller of it runs this on a thread."""
        if conn.peer_pid is None:
            return [], {}
        names = frozenset(session_envs().values())
        return caller.ancestry(conn.peer_pid), caller.environ(conn.peer_pid, names)

    def _refuse_gone_caller(self, conn: Connection) -> None:
        """The process that connected is gone (a connection handed to a child,
        which kept the session's environment): who calls can no longer be
        checked, so nothing changes on its say (plan D9)."""
        if conn.peer_pid is None:
            return
        from . import procid

        if conn.peer_start:
            gone = procid.alive(conn.peer_pid, conn.peer_start) is False
        else:
            gone = not procid.exists(conn.peer_pid)
        if gone:
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: the process that opened this connection has exited; connect again",
                {"reason": RefusedReason.CALLER_GONE},
            )

    async def _action_run(self, conn: Connection, params: dict) -> dict:
        """`action.run`: never for a caller in a sandbox (`Cap.ACTION_SANDBOX`),
        as every other method that runs work: the change would land outside
        it. The caller's own confinement decides, never the client kind its
        hello names (a label anyone can send); the desktop app, which is never
        sandboxed, is unaffected, and a refused CLI runs the action itself,
        inside its sandbox. A `client_request_id` this service accepted
        already gets its action before any check (`ActionManager.existing`;
        it starts nothing): a retry never reads as refused because something
        changed since (the endpoint it signed out of)."""
        known = self.actions.existing(params)
        if known is not None:
            return known
        env = self._context(params)
        self._refuse_gone_caller(conn)
        await self._refuse_sandboxed(conn)
        return self._action_run_now(conn, params, env)

    def _action_run_now(self, conn: Connection, params: dict, env: dict) -> dict:
        _inside, daemon = self._caller_session(conn, env)
        if daemon is not None:
            log(f"refused {params.get('action')!r} from inside session {daemon}, which the Probe daemon records")
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: Probe's settings cannot be changed from inside a coding agent's session the "
                "Probe daemon records; run it from your own terminal or the Probe app",
                {"reason": RefusedReason.DAEMON_SESSION, "sid": daemon},
            )
        if conn.peer_pid is not None:
            # The child resolves the caller's own session from its process too
            # (its environment, a harness-process marker above it), registered
            # or not, as `desktop.request`'s does (#3360; `probe.core.run`).
            env[CALLER_PID_ENV] = str(conn.peer_pid)
            env[CALLER_START_ENV] = conn.peer_start or ""
        if params.get("action") == Action.UPDATE:
            # Before the files it imports from are replaced (R2), as a cycle does.
            try:
                preload()
            except Exception as exc:  # noqa: BLE001 -- a person's Update still runs
                log(f"preload before the update action failed: {exc!r}")
        return self.actions.run(params, env)

    def _check_now(self, conn: Connection, params: dict) -> dict:
        trigger = params.get("trigger", CheckTrigger.CLI)
        if trigger not in CHECK_TRIGGERS:
            raise invalid_params(f"trigger must be one of {sorted(CHECK_TRIGGERS)}")
        return self.updater.check_now(trigger, need_app_check(params, trigger))

    async def _daemon_host(self, conn: Connection, params: dict) -> dict:
        """`daemon.host`: where the daemon host listens, started if need be, for an
        old tap's `probe daemon worker` (the proxy, `probe.daemon.proxy`), which
        then runs its session there. Refused: no host here (off, Windows)."""
        await self._refuse_sandboxed(conn)
        host = self.workers.daemon_host
        if host is None or not host.available():
            raise RpcError(ErrorCode.REFUSED, "refused: no daemon host here", {"reason": "daemon_host_off"})
        try:
            # Its own small pool: proxies all ask at once after a restart, and a host
            # start can take START_TIMEOUT_S; the loop's shared executor serves every
            # other `to_thread` (the caller checks, the mailboxes).
            if self._host_pool is None:
                self._host_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="daemon-host")
            return await asyncio.get_running_loop().run_in_executor(self._host_pool, host.address)
        except Exception as exc:  # noqa: BLE001 -- the proxy runs the worker itself
            raise RpcError(ErrorCode.REFUSED, f"refused: the daemon host is unavailable ({exc})",
                           {"reason": "daemon_host_unavailable"}) from None

    async def _recorders_finish(self, conn: Connection, params: dict) -> dict:
        """`recorders.finish` (`probe capture off` for one agent): every
        recorder of `harness` finishes, as `session.finish` does for one;
        `{finished: [sid], unfinished: [sid]}`, the second still finishing
        after `wait` seconds."""
        harness = need_str(params, "harness", max_len=64)
        wait = need_wait(params)
        await self._refuse_sandboxed(conn)
        sessions = self.registry.sessions

        def harness_of(sid: str) -> str | None:
            session = sessions.get(sid)
            return session.harness if session is not None else None

        answer = await self.recorders.finish_harness(harness, wait, harness_of)
        asked = len(answer["finished"]) + len(answer["unfinished"])
        if asked:
            # The stopper's side of the record (`probe.cli.capture` journals the
            # `tap watch` processes it signals; these it asks here).
            log(
                f"recorders.finish: {asked} recorder(s) of {harness} asked to finish (caller pid "
                f"{conn.peer_pid}); {len(answer['unfinished'])} still finishing after {wait:g} s"
            )
        return answer

    async def _run_hold(self, conn: Connection, params: dict) -> dict:
        """`run.hold`: a `probe exec` holds `run` for as long as `owner` runs.
        `{held: true}`, else `{held: false, reason}` (`owner_gone`,
        `not_caller`, `too_many`, `updating`): its run lock still says it runs.
        Never for a caller in a sandbox (or one the kernel will not name): its
        hold would persist outside it and keep updates off."""
        run = need_str(params, "run", max_len=256)
        owner = need_owner(params)
        if owner is None:
            raise invalid_params("owner must be {pid, start_time}: a hold ends with its process")
        await self._refuse_sandboxed(conn)
        peer = conn.peer_pid

        def check() -> str | None:
            if self.runs.owner_alive(owner["pid"], owner["start_time"]) is False:
                return "owner_gone"
            # The caller holds for itself (or a process it runs under), never
            # for an unrelated one it could keep updates off for.
            if peer is not None and owner["pid"] != peer and (owner["pid"], owner["start_time"]) not in (
                caller.ancestry(peer)
            ):
                return "not_caller"
            return None

        # `ps` on macOS: off the loop.
        refused = await asyncio.to_thread(check)
        if refused is not None:
            return {"held": False, "reason": refused}
        if self.updater.applying:
            # The update's last look is behind it: it would never see this hold.
            return {"held": False, "reason": "updating"}
        hold, new = self.runs.add(run, owner)
        if hold is None:
            return {"held": False, "reason": "too_many"}
        if new:
            self._watch_hold(hold)
            log(f"run {run} held by pid {owner['pid']}")
            self.status_cache.invalidate()
        return {"held": True}

    async def _run_release(self, conn: Connection, params: dict) -> dict:
        """`run.release`: the caller's holds of `run` go from the listing (only
        `owner`'s, when named). `{released: n}`; releasing what is not held,
        or not the caller's, is not an error. Only a hold whose owner is the
        caller or a process it runs under is released, as `run.hold` admits
        it; never from a caller in a sandbox.

        Its process still holds updates off until it exits (`runs.releasing`,
        watched as the hold was): the releasing `probe exec` is still cleaning
        up, importing from the env an update replaces. The deferred update is
        retried at that exit, not now."""
        run = need_str(params, "run", max_len=256)
        owner = params.get("owner")
        pid = None
        if owner is not None:
            pid = owner.get("pid") if isinstance(owner, dict) else None
            if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 1:
                raise invalid_params("owner must be {pid, start_time} or left out")
        await self._refuse_sandboxed(conn)
        chain = set(await asyncio.to_thread(caller.ancestry, conn.peer_pid))  # `ps` on macOS
        gone = self.runs.release(run, chain, pid)
        if gone:
            log(f"run {run} released (its process still holds updates off until it exits)")
            self.status_cache.invalidate()
        return {"released": len(gone)}

    def _watch_hold(self, hold: Hold) -> None:
        if self.watcher is None:
            return
        self.watcher.watch(hold.key, hold.owner["pid"], hold.owner["start_time"], lambda: self._hold_exited(hold))

    def _hold_exited(self, hold: Hold) -> None:
        if self.runs.drop(hold):
            log(f"run {hold.run}: its process {hold.owner['pid']} exited")
            self._run_gone()

    def _run_gone(self) -> None:
        """A run is over: a deferred update gets another try, as when a session ends."""
        self.status_cache.invalidate()
        self.updater.session_ended()

    async def _manifest_refresh(self, conn: Connection, params: dict) -> dict:
        """`manifest.refresh`: the CLI's cached release manifest, refreshed by
        a child with the request's context; `{outcome, done, result}`."""
        env = self._context(params)
        wait = need_wait(params)
        await self._refuse_sandboxed(conn)
        return await self.manifest.refresh(env, wait=wait)

    # -- the mailbox (plan Q2) -----------------------------------------------

    async def _mailbox_post(self, conn: Connection, params: dict) -> dict:
        """`mailbox.post`: a message or a held question written for its session
        (`mailhost.MailHost.post`), and its watchers told at once. Never for a
        caller in a sandbox, which writes the file itself; and only from the
        session's own daemon worker (#3361, `_refuse_foreign_mail`)."""
        request = need_mailbox_post(params)
        await self._refuse_sandboxed(conn)
        await self._refuse_foreign_mail(conn, request["sid"], claim=False)
        request["state"] = request["state_dir"] or default_state()
        answer = self._mailbox_answered(await self.mailhost.run(MailHost.post, request))
        if "error" in answer:
            raise invalid_params(answer["error"])
        if answer.get("posted"):
            if answer.get("kind") == "question":
                self._emit(Topic.APPROVALS_CHANGED, {"sid": request["sid"], "ids": [answer["posted"]]})
            else:
                self._emit(Topic.MAILBOX_CHANGED, {"sid": request["sid"], "parts": [MailboxPart.MESSAGES]})
        return answer

    async def _mailbox_claim(self, conn: Connection, params: dict) -> dict:
        """`mailbox.claim`: the named messages taken once for the caller to show
        (`mailhost.MailHost.claim`). Never for a caller in a sandbox, and only
        from inside the session's own agent or a hook host (#3361,
        `_refuse_foreign_mail`)."""
        request = need_mailbox_claim(params)
        await self._refuse_sandboxed(conn)
        await self._refuse_foreign_mail(conn, request["sid"], claim=True)
        request["state"] = request["state_dir"] or default_state()
        answer = self._mailbox_answered(await self.mailhost.run(MailHost.claim, request))
        if answer.get("claimed"):
            self._emit(Topic.MAILBOX_CHANGED, {"sid": request["sid"],
                                               "parts": [MailboxPart.CLAIMED, MailboxPart.MESSAGES]})
        answer.setdefault("claimed", [])
        answer.setdefault("gone", [])
        return answer

    async def _mailbox_answer(self, conn: Connection, params: dict) -> dict:
        """`mailbox.answer`: the researcher's pick for a held question
        (`mailhost.MailHost.answer`). Never for a caller in a sandbox, and
        never without the question's answer key (`key`, which the answer hook
        reads beside the request; #3355): any process of this user reaches
        this socket, and a yes recorded here is one the daemon acts on. A
        refusal writes nothing, and its caller (an answer hook, of any
        version) writes the answer file itself, which only a caller with the
        approvals folder can. The caller's `channel` is checked (an older
        service requires it) and never recorded: the service names it."""
        request = need_mailbox_answer(params)
        key = params.get("key")
        if key is not None and not (isinstance(key, str) and len(key) <= MAX_ANSWER_KEY):
            raise invalid_params(f"key must be a string of at most {MAX_ANSWER_KEY} characters")
        request["key"] = key
        await self._refuse_sandboxed(conn)
        request["state"] = request["state_dir"] or default_state()
        answer = self._mailbox_answered(await self.mailhost.run(MailHost.answer, request))
        if "refused" in answer:
            raise RpcError(ErrorCode.REFUSED, f"refused: {answer['refused']}")
        if answer.get("answered") and answer.get("sid"):
            self._emit(Topic.APPROVALS_CHANGED, {"sid": answer["sid"], "ids": [request["id"]]})
        return answer

    async def _refuse_foreign_mail(self, conn: Connection, sid: str, *, claim: bool) -> None:
        """Refuse a post to, or a claim from, `sid`'s mailbox by a process that
        is not the session's own (#3361). Any process of this user reaches the
        socket, and a message posted is one the session's agent is shown as
        Probe's, one claimed is one it never sees. The kernel names the caller;
        its process ancestry (pid AND start time, as for owners) decides:

            post    the session's daemon worker: a child of this service
                    (`workers.WorkerHost.pids`), or one under the process that
                    registered the session (`Session.registrant`: a `tap
                    watch` supervising its own worker, an older tap)
            claim   Probe's hooks: run under the session's agent process (its
                    registered owner), or forked from a warm hook host this
                    service runs (`hookhosts.HookHosts.pids`)
            both    this service itself

        The walk stops at this service: what runs above it says nothing. Every
        caller refused here (an older worker that outlived its service, a hook
        of a session registered without an owner) does the step on the files
        itself, as it does on any refusal: delivery never depends on this."""
        peer = conn.peer_pid
        if peer == self.pid:
            return
        session = self.registry.sessions.get(sid)
        owner = session.owner if claim and session is not None else None
        registrant = None
        if not claim and session is not None and isinstance(session.registrant, dict):
            registrant = session.registrant
        children = self.hookhosts.pids() if claim else self.workers.pids(sid)
        me = self.pid

        def belongs() -> bool:
            if peer is None:
                return False
            below = None
            for pid, start in caller.lineage(peer):
                if pid == me:
                    return below in children
                if owner is not None and pid == owner["pid"] and start == owner["start_time"]:
                    return True
                if registrant is not None and same_process(registrant, {"pid": pid, "start_time": start}):
                    return True
                below = pid
            return False

        if await asyncio.to_thread(belongs):
            return
        what = "take messages from" if claim else "post to"
        method = Method.MAILBOX_CLAIM if claim else Method.MAILBOX_POST
        # Once per (method, session) a while: each hook is a new process.
        if self._first_refusal((method, sid)):
            log(f"refused {method} for {sid} from pid {peer}: not the session's own"
                f" (said once per {REFUSAL_LOG_S / 60:g} min)")
        raise RpcError(
            ErrorCode.REFUSED,
            f"refused: only the session's own {'hooks' if claim else 'daemon worker'} may {what} its mailbox",
            {"reason": Bound.NOT_SESSION},
        )

    @staticmethod
    def _mailbox_answered(answer: dict | None) -> dict:
        """A step's answer, or `busy` when none came (a stuck step before it,
        or this one): its caller then works on the files itself."""
        if answer is None:
            raise RpcError(ErrorCode.BUSY, "busy: the mailbox is stuck on a file; work on the files directly")
        return answer
    async def _desktop_request(self, conn: Connection, params: dict) -> dict:
        """`desktop.request` (plan Q6): one of the desktop app's management
        requests, answered as `probe desktop request --json` answers it, by a
        child running the same code (`management.py`). Never for a caller in a
        sandbox (the child reads this user's credentials, with the context it
        chose), nor from a caller that has exited or runs inside a session the
        daemon records (D9: `probe desktop` is refused there too, reads
        included); and no child starts while an update replaces the CLI's
        files under it (`busy`, holder `update`), checked again right before
        it starts."""
        request = params.get("request")
        op = request.get("op") if isinstance(request, dict) else None
        if not isinstance(op, str) or not op or len(op) > 64:
            raise invalid_params('request must be a desktop management request: {"op": ..., ...}')
        origin = params.get("origin")
        if origin is not None and origin != ORIGIN_DESKTOP:
            raise invalid_params(f"origin must be {ORIGIN_DESKTOP} when supplied")
        env = self._context(params)
        await self._refuse_sandboxed(conn)
        self._refuse_gone_caller(conn)
        seen = await asyncio.to_thread(self._caller_seen, conn)
        _inside, daemon = self._caller_session(conn, env, seen)
        if daemon is not None:
            log(f"refused desktop {op!r} from inside session {daemon}, which the Probe daemon records")
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: the Probe app's requests cannot come from inside a coding agent's session the Probe "
                "daemon records; use the Probe app or your own terminal",
                {"reason": RefusedReason.DAEMON_SESSION, "sid": daemon},
            )

        # The caller's own session, registered or not, is resolved by the child
        # from the caller's process (its environment, a harness-process marker
        # above it), as its own `probe` would (`probe.core.run._desktop_refusal`).
        if conn.peer_pid is not None:
            env[CALLER_PID_ENV] = str(conn.peer_pid)
            env[CALLER_START_ENV] = conn.peer_start or ""
        self._desktop_may_start()
        try:
            return await self.management.request(
                request, env, human=origin == ORIGIN_DESKTOP, may_start=self._desktop_may_start
            )
        finally:
            # Answered: what holds the service may have changed.
            self.reevaluate()

    def _desktop_may_start(self) -> None:
        """`busy` while the CLI's files are being replaced under a new child:
        the update cycle applying in place, or a person's Update (`action.run
        update`, which raises no barrier of its own)."""
        if self.updater.applying:
            raise RpcError(
                ErrorCode.BUSY,
                "busy: an update is replacing the Probe CLI",
                {"holder": {"kind": BusyHolder.UPDATE, "cycle_id": self.updater.cycle_id}},
            )
        running = self.actions.running
        if running is not None and running.action == Action.UPDATE:
            raise RpcError(
                ErrorCode.BUSY,
                "busy: an update is replacing the Probe CLI",
                {"holder": self.actions.busy_holder()},
            )

    async def _outbox_drain(self, conn: Connection, params: dict) -> dict:
        """`outbox.drain` (plan Q5): the drainer of the outbox folder `dir`, as
        the service's child on the caller's interpreter and environment
        (`background.py`). `{accepted: true, state}` (started, or this
        service's child for it runs), else `{accepted: false, reason}` and the
        caller forks its own drainer, as before."""
        return await self._background_start(conn, need_background(params, directory=True), self.background.drain)

    async def _box_watch(self, conn: Connection, params: dict) -> dict:
        """`box.watch` (plan Q5): this box's watcher (`probe.box`), likewise."""
        return await self._background_start(conn, need_background(params, directory=False), self.background.watch_box)

    async def _background_start(self, conn: Connection, request: dict, start) -> dict:
        """The caller checks, then `start(request)`, on a thread: a caller in
        a sandbox is refused (its child would run outside it), and so is a
        `PROBE_BASE_URL` the CLI config does not name (plan D10: the stored
        login follows that variable). An answer not ready within
        BACKGROUND_WAIT_S reads `busy`; the start still completes, and the
        caller's own drainer and this one share the outbox's lease."""
        if self.stop_reason is not None:
            return {"accepted": False, "reason": BackgroundRefusal.STOPPING}
        peer = conn.peer_pid

        def checked() -> dict:
            # A caller cut off from the network is confined too: its uploads
            # would go out on this service's.
            if caller.sandboxed(peer) or other_network(peer):
                return {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}
            if not _drain_url_allowed(request["env"]):
                return {"accepted": False, "reason": BackgroundRefusal.UNKNOWN_ENDPOINT}
            return start(request)

        done, answer = await self._offload(
            "_background_starts", BACKGROUND_THREADS, self._background_slots, BackgroundRefusal.BUSY,
            BACKGROUND_WAIT_S, checked,
        )
        if not done or "refused" in answer:
            return {"accepted": False, "reason": BackgroundRefusal.BUSY}
        return answer

    async def _telemetry_send(self, conn: Connection, params: dict) -> dict:
        """`telemetry.send` (plan Q5): one batch the caller built, POSTed from
        the service's telemetry thread. Never for a caller in a sandbox (its
        network would be this service's)."""
        entries, batch_id = need_telemetry(params)
        peer = conn.peer_pid
        if await asyncio.to_thread(lambda: caller.sandboxed(peer) or other_network(peer)):
            return {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}
        return self.background.send_telemetry(entries, batch_id)
    async def _statusline_refresh(self, conn: Connection, params: dict) -> dict:
        """`statusline.refresh`: refresh `sid`'s status-line marker with the
        folder's next fetch child (`statusline.py`); `{scheduled: true,
        due_in}`, else `{scheduled: false, reason}` and the hook fetches
        itself. `plugin_root` must be a Probe plugin folder of this user's
        with the refresh script; `python` the hook's interpreter (a 3.9 or
        newer, else the service PATH's `python3`); `agent` the session's
        harness id, for its capture reading."""
        sid = need_sid(params)
        agent = params.get("agent")
        if agent is not None and not is_agent_id(agent):
            raise invalid_params("agent must be a harness id")
        raw = need_path(params, "plugin_root")
        asked = params.get("python")
        if asked is not None and (not isinstance(asked, str) or not asked.startswith("/") or len(asked) > MAX_HOOK_PATH):
            raise invalid_params("python must be an absolute path")
        env = self._context(params)
        await self._refuse_sandboxed(conn)

        def check() -> tuple:
            root = os.path.realpath(raw)
            verdict = self.statusline.check(root)
            return root, verdict, (None if verdict else self.hookhosts.python_for(asked))

        root, verdict, python = await asyncio.to_thread(check)
        if verdict is not None:
            return {"scheduled": False, "reason": verdict}
        if python is None:
            return {"scheduled": False, "reason": "no python 3.9 or newer"}
        return self.statusline.request(root, python, env, sid, agent)

    async def _notes_sync(self, conn: Connection, params: dict) -> dict:
        """`notes.sync`: the team note's sync for the caller's context, once
        per machine and debounced (`notesync.py`). `mode` push | reconcile;
        `rules_for` the `PROBE_AGENT` values whose `probe agent-rules refresh`
        runs first ("" = the CLI's own default); `feedback` a `probe feedback
        flush` after. `{outcome: scheduled | queued}`, else `{outcome: null,
        reason}` and the hook spawns its own."""
        mode = need_choice(params, "mode", NOTES_MODES)
        rules_for = params.get("rules_for", [])
        if (
            not isinstance(rules_for, list)
            or len(rules_for) > MAX_NOTE_AGENTS
            or not all(agent == "" or is_agent_id(agent) for agent in rules_for)
        ):
            raise invalid_params(f"rules_for must be a list of at most {MAX_NOTE_AGENTS} harness ids (or \"\")")
        feedback = need_bool(params, "feedback")
        env = self._context(params)
        await self._refuse_sandboxed(conn)
        return self.notes.request(env, mode, rules_for, feedback)

    async def _import_start(self, conn: Connection, params: dict) -> dict:
        """`import.start`: start an approved import's worker (`imports.py`)
        with the CLI's own environment (`env`, required), and watch it.
        `{started: true, pid, start_time}`, else `{started: false, reason}`:
        `running` (this service runs it: `pid`, `start_time`), `not_a_job`
        (`detail`), `too_many`, `stopping`, `could_not_start: ...`."""
        job_id = params.get("job_id")
        if not valid_job_id(job_id):
            raise invalid_params("job_id must be an import job id (32 hex digits)")
        directory = need_path(params, "directory")
        attempt = need_int(params, "attempt")
        env = need_env(params)
        if not env:
            raise invalid_params("env is required: the worker runs with the CLI's own environment")
        await self._refuse_sandboxed(conn)
        # The folder's real path names the job (with its id): checked, and
        # its log opened, on a thread; `start` re-checks what runs after it.
        fd, directory, why = await asyncio.to_thread(prepare_import, job_id, directory)
        if fd is None:
            return {"started": False, "reason": "not_a_job", "detail": why}
        worker = self.imports.start(job_id, directory, attempt, env, fd)
        if isinstance(worker, dict):
            return worker
        from . import procid

        start = await asyncio.to_thread(procid.start_time, worker.pid)  # `ps` on macOS
        return self.imports.started(worker, start or "")

    async def _refuse_sandboxed(self, conn: Connection) -> None:
        """Refuse a caller in a sandbox (as `hooks.host` and `session.record`
        do): a child this runs would fetch and write outside it, with the
        context it chose, and a recorder it stops is outside it too. The CLI
        then does it itself, inside. Unknown counts as sandboxed."""
        if await asyncio.to_thread(caller.sandboxed, conn.peer_pid):
            raise RpcError(
                ErrorCode.REFUSED, "refused: a caller in a sandbox", {"reason": RefusedReason.SANDBOXED}
            )


def _hook_run_refusal(lane: str, tool: object) -> str | None:
    """Why `hooks.run` will not run this event (`HOOK_RUN_LANES`, `HOOK_RUN_TOOLS`),
    or None: only what pi's guard sends."""
    if lane not in HOOK_RUN_LANES:
        return f"hooks.run runs only pi's guard: lane {lane!r} is not served"
    if not isinstance(tool, str) or not (tool in HOOK_RUN_TOOLS or re.search(PROBE_MCP_TOOL, tool)):
        return "hooks.run runs only pi's guard: not a tool it reads"
    return None


def _settled(future: asyncio.Future, then: Callable[[object], None] | None = None) -> None:
    """An answer nobody waits for any more: read, so it is never reported
    unread, and handed to `then` (when given) if it is a value."""
    if not future.cancelled() and future.exception() is None and then is not None:
        then(future.result())


class LegacyDoor:
    """The socket clients from before the machine key connect to (plan D8).

    A session started before the update that brought the key runs a tap, and
    a desktop app not yet updated computes, `~/.local/state/probe/service/
    service.sock`. This service serves that path too whenever it holds that
    folder's `service.lock`, exactly as the service of that time did, so those
    clients register, read status and run actions here. While another process
    holds it (a service from before the key, still running), it looks again
    every LEGACY_RETRY_S. One per HOME: on a shared home folder, one machine's
    service serves the old clients, as before the key."""

    def __init__(self) -> None:
        self.fd: int | None = None
        self.server: asyncio.AbstractServer | None = None
        self.bound: tuple[int, int] | None = None
        self.path = paths.legacy_socket_path()
        self._retry: asyncio.TimerHandle | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._handler: Callable | None = None
        self.retry_s = _env_float(LEGACY_RETRY_ENV, LEGACY_RETRY_S)

    async def open(self, loop: asyncio.AbstractEventLoop, handler: Callable) -> None:
        self._loop, self._handler = loop, handler
        await self._try()

    async def _try(self) -> None:
        self._retry = None
        if self.server is not None or self._loop is None:
            return
        fd = _take_lock(paths.legacy_lock_path(), wait_for_stopping=False)
        if fd is None:
            self._retry = self._loop.call_later(self.retry_s, lambda: asyncio.ensure_future(self._try()))
            return
        try:
            paths.private_dir(self.path.parent)
            listen = _bind(self.path)
            st = os.stat(self.path)
            self.server = await asyncio.start_unix_server(self._handler, sock=listen, limit=MAX_LINE_BYTES + 1)
        except OSError as exc:
            log(f"cannot serve the pre-machine-key socket {self.path}: {exc}")
            os.close(fd)
            self._retry = self._loop.call_later(self.retry_s, lambda: asyncio.ensure_future(self._try()))
            return
        self.fd = fd
        self.bound = (st.st_dev, st.st_ino)
        log(f"also serving {self.path} (clients from before the machine key)")

    def close(self) -> None:
        if self._retry is not None:
            self._retry.cancel()
            self._retry = None
        if self.server is not None:
            self.server.close()
            self.server = None
        # Unlink only OUR socket, and before the lock goes, as `run_service` does.
        with contextlib.suppress(OSError):
            st = os.stat(self.path)
            if self.bound is not None and (st.st_dev, st.st_ino) == self.bound:
                os.unlink(self.path)
        if self.fd is not None:
            with contextlib.suppress(OSError):
                os.close(self.fd)
            self.fd = None


# -- process entry ------------------------------------------------------------


def _open_log() -> int | None:
    path = paths.log_path()
    try:
        if path.stat().st_size > MAX_LOG_BYTES:
            os.replace(path, path.with_name(path.name + ".1"))
    except OSError:
        pass
    try:
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except OSError:
        return None


def _take_lock(path: Path | None = None, *, wait_for_stopping: bool = True) -> int | None:
    """The life-long `service.lock` (this machine's, unless `path` names
    another), or None when another service holds it."""
    try:
        fd = os.open(path or paths.lock_path(), os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except OSError:
        if path is None:
            raise
        return None
    deadline = None
    while True:
        if paths.try_lock(fd):
            return fd
        # A service that is stopping lets go within moments; one that runs
        # does not, and then this instance is the duplicate and leaves.
        if not wait_for_stopping or not (paths.service_dir() / STOPPING_NAME).exists():
            os.close(fd)
            return None
        if deadline is None:
            deadline = time.monotonic() + STOPPING_WAIT_S
        if time.monotonic() >= deadline:
            os.close(fd)
            return None
        time.sleep(0.05)


def _keep() -> None:
    with contextlib.suppress(Exception):
        from . import keeper

        # The lifeboat first (`lifeboat.install`), then the units that run it;
        # env.json with the login shell's index settings (never this clean env's).
        login = None
        if keeper.wanted():
            from . import lifeboat

            login = lifeboat.login_env()
        outcome = keeper.install(login)
        if outcome not in ("current", "not wanted"):
            log(f"keeper: {outcome}")


def _lifeboat_after(result: dict) -> None:
    with contextlib.suppress(Exception):
        from . import lifeboat

        if lifeboat.after_cycle(result):
            log("lifeboat: current/ proved itself and is the known-good copy now")


#: How often the service looks for an outbox pause that no longer holds: one stat.
OUTBOX_LOOK_S = 60.0
#: Test-only: the look's period in seconds, "0" off (the suite's services).
OUTBOX_LOOK_ENV = "PROBE_SERVICE_OUTBOX_S"


def _outbox_look_s() -> float:
    try:
        return float(os.environ.get(OUTBOX_LOOK_ENV) or OUTBOX_LOOK_S)
    except ValueError:
        return OUTBOX_LOOK_S


async def _outbox_login_env() -> dict | None:
    """The outbox drainer's environment, from the login shell as every other
    network child of this service gets it (`loginenv`): PATH, where the outbox
    and the stored login are, the proxies and CAs, and the person's report
    switches (`watch.CONSENT_VARS`), by `runtime_env_name` (never a
    credential). None when the login shell cannot be read."""
    from . import loginenv, watch
    from .protocol import runtime_env_name

    names = tuple(sorted({*loginenv.NAMES, *watch.CONSENT_VARS, "PROBE_OUTBOX_DIR"}))
    read = await loginenv.read(names=names)
    if read is None:
        return None
    login_path, values = read
    env = {"PATH": loginenv.build_path(login_path, os.environ.get("PATH"), paths.home())}
    env.update({name: value for name, value in values.items() if value and runtime_env_name(name)})
    return env


def _drain_url_allowed(env: dict) -> bool:
    """May a drainer run with `env`'s PROBE_BASE_URL (plan D10: the stored
    login follows it)? Unset, or https and an endpoint that login may go to
    (`caller.known_endpoint`). Blocking (reads the CLI config): a thread."""
    url = env.get(BASE_URL_ENV) or None  # empty is unset, as `config.resolve` reads it
    return url is None or (url.startswith("https://") and caller.known_endpoint(url, env))


def _lift_outbox_pause(env: dict | None) -> tuple[bool, str, int]:
    """Lift the pause of the outbox `env` names (the login shell's variables;
    None: this service's own) when it no longer holds, reporting nothing:
    `(lifted, outbox root, writes it held)`. One stat when there is no marker."""
    from probe.sdk import outbox_worker
    from probe.sdk.journal import Journal, default_root

    root = default_root(env)
    if not os.path.lexists(root / "paused"):
        return False, str(root), 0
    status = Journal.read_status(str(root)) or {}
    lifted = outbox_worker.lift_stale_pause(Journal(str(root)), status, base_url=None, wait=False)
    return lifted, str(root), int(status.get("pending") or 0) + int(status.get("waiting") or 0)


def _mark_versions() -> None:
    with contextlib.suppress(Exception):
        from probe._shared import installs

        if installs.versions_root().is_dir():
            installs.mark_in_use()


def _name_holder(fd: int) -> None:
    """Write `<pid> <start time>` into the lock file this service holds: the
    guard (D5) finds a replacement that hangs without answering there, and
    stops that exact process (`guard.holder`). Never raises."""
    from . import procid

    with contextlib.suppress(OSError):
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, f"{os.getpid()} {procid.start_time(os.getpid()) or ''}\n".encode())


def _bind(path: Path) -> socket.socket:
    """Bind the socket 0600 (we hold service.lock, so anything there is stale)."""
    with contextlib.suppress(FileNotFoundError):
        os.unlink(path)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    old = os.umask(0o177)
    try:
        sock.bind(str(path))
    finally:
        os.umask(old)
    os.chmod(path, 0o600)
    sock.listen(64)
    sock.setblocking(False)
    return sock


def _barrier_up() -> bool:
    """The update barrier or the workers' hold is up (an update's hand-over,
    this service's or one a stopped service left): read by the watch's scan, on
    a thread (files, and `ps` on macOS)."""
    from . import barrier

    return barrier.workers_held() or not barrier.wait(0)


def _thread_exception(service: Service, args) -> None:
    """`threading.excepthook`: never raises."""
    try:
        if args.exc_type is SystemExit:
            return
        import traceback

        text = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
        name = args.thread.name if args.thread is not None else "?"
        # A thread's name carries a pid or a counter: its site is the name without digits.
        site = "".join(ch for ch in name if not ch.isdigit())
        log_traceback(log, f"thread {name}: unhandled {args.exc_type.__name__}", text, gate=service._tracebacks,
                      key=("thread", site, args.exc_type.__name__))
        service.watch.note(Family.SERVICE_ERROR, "thread_exception", facts={
            "thread": name, "type": args.exc_type.__name__, "traceback": text,
        })
    except Exception:  # noqa: BLE001
        pass


def run_service() -> int:
    """`python -m probe.service`: one instance; exits 0 when idle or as a duplicate."""
    try:
        sock_path = paths.ensure_dirs()
    except OSError as exc:
        log(f"cannot use {paths.service_dir()}: {exc}")
        return 1
    lock_fd = _take_lock()
    if lock_fd is None:
        return 0  # another service runs: this one is the duplicate
    from . import watch

    # The service before this one, as it named itself in the lock file: read
    # before this one names itself there (crash-report plan B2).
    previous = watch.previous_holder()
    _name_holder(lock_fd)
    log_fd = _open_log()
    if log_fd is not None and not os.isatty(2):
        os.dup2(log_fd, 1)
        os.dup2(log_fd, 2)
    with contextlib.suppress(Exception):
        import faulthandler

        # A fatal signal's traceback (a crash in C, an abort) lands in service.log too.
        faulthandler.enable(file=sys.stderr, all_threads=True)
    with contextlib.suppress(OSError):
        (paths.service_dir() / STOPPING_NAME).unlink()
    # How it ended: no stop record on this boot, or a recorded crash, is a
    # `service_crash` to report (`watch.last_run`; this one's own record next).
    crashed = watch.last_run(previous, _version())
    if paths.WINDOWS:
        listen, bound = paths.pipe_name(), None
    else:
        try:
            listen = _bind(sock_path)
        except OSError as exc:
            log(f"cannot bind {sock_path}: {exc}")
            watch.record_crash(f"cannot bind the socket: {exc}", "")
            return 1
        bound = os.stat(sock_path)
    registry = Registry(paths.registry_path(), ttl=_env_float(TTL_ENV, HEARTBEAT_TTL_S))
    service = Service(
        registry=registry,
        grace_s=_env_float(GRACE_ENV, GRACE_S),
        discovery_s=_env_float(DISCOVERY_ENV, DISCOVERY_S),
        legacy=None if paths.WINDOWS else LegacyDoor(),
    )
    if crashed is not None:
        why = crashed.pop("reason")
        service.statepost.crashed = why
        log(f"the service before this one ended without stopping ({why}): reported once consent allows")
        service.watch.note(Family.SERVICE_CRASH, why, facts=crashed)
    # A thread's unhandled exception: logged with its traceback, and counted
    # for `service_error` (crash-report plan B2).
    threading.excepthook = lambda args: _thread_exception(service, args)
    try:
        reason = asyncio.run(service.run(listen))
    except Exception as exc:  # noqa: BLE001
        import traceback

        text = traceback.format_exc()
        log_traceback(log, f"crashed: {exc!r}", text)
        # What the next service reports (`watch.last_run`): this one wrote no stop record.
        watch.record_crash(repr(exc), text)
        reason = "crash"
    finally:
        # Unlink only OUR socket, and before the lock goes (process exit): a new
        # service can bind only after that, so this never removes its socket.
        with contextlib.suppress(OSError):
            st = os.stat(sock_path)
            if bound is not None and (st.st_dev, st.st_ino) == (bound.st_dev, bound.st_ino):
                os.unlink(sock_path)
        with contextlib.suppress(OSError):
            (paths.service_dir() / STOPPING_NAME).unlink()
    log(f"exited ({reason})")
    return 0 if reason != "crash" else 1


__all__ = ["LegacyDoor", "PidWatcher", "Registry", "Service", "peer_uid", "run_service"]
