"""BackgroundHost: a Probe service (the machine's or a delivery one) drains a training process's outbox with its
own code, as its child (plan D8), runs its box watcher as a thread (X9), and posts its telemetry batches.
How and why: DESIGN.md beside this file."""

from __future__ import annotations

import collections
import contextlib
import os
import queue
import stat
import subprocess
import sys
import threading
import time
from collections.abc import Callable

from probe.foundation.service_api import paths
from probe.foundation.service_api.start import build_module_argv, get_argv_module, get_package_dir
from probe.foundation.service_api.vocabularies import BackgroundRefusal, BackgroundState
from probe.foundation.service_api.env import BASE_URL_ENV, CREDENTIAL_ENV, secret_env
from .credentials import HeldCredentials
from .watchers import WatcherThreads, is_same_report_env

#: Drainer children running at once, at most (one per outbox folder).
MAX_DRAINS = 8
#: A child this young is still starting: a hand-off for it is RUNNING, not a
#: second start (shorter than a drainer's shortest life with its lease).
STARTUP_S = 1.0
#: An error exit this soon after the start marks its folder failing ...
EARLY_EXIT_S = 5.0
#: ... and the hand-offs for it are refused this long.
FAILING_S = 300.0
#: The worker's exit codes that are not a failure: drained (or stepped aside),
#: auth-blocked, paused (`probe.sdk.delivery.outbox.outbox.run`).
CLEAN_EXITS = frozenset({0, 3, 4})
#: Live children of one key at once, at most: the one exiting after it let
#: the lease go, and the one that took over.
MAX_PER_KEY = 2
#: A child still running this long after its start while its key's lease is
#: free never took it: its start hangs, and it is told to stop.
STALL_S = 60.0
#: ... seen free on two looks this far apart, at least (`_stop_stalled`).
STALL_CONFIRM_S = 5.0
#: A child whose waiter would not start is killed and reaped within this.
REAP_WAIT_S = 2.0
#: Telemetry batches waiting for the sender thread, at most.
MAX_TELEMETRY_BATCHES = 32
#: The ids of this many batches taken lately are kept, so a resend is taken once.
MAX_BATCH_IDS = 1024
#: What a stopping service gives the telemetry it took, at most: the SDK
#: sender's own exit flush (`probe.analytics.sender.FLUSH_TIMEOUT_S`).
FLUSH_S = 3.5
#: The service's own drain (plan D8), run on this service's interpreter with `-I`.
DRAIN_MODULE = "probe.sdk.delivery.service.background.outbox_drain"
#: The box watcher's own entry (`python -m probe.box` is its older name, private).
BOX_MODULE = "probe.sdk.run.watcher"
#: A box watcher's key: this, then its registry folder (one watcher per registry).
BOX_PREFIX = "box:"
#: Box watchers running at once, at most (one per registry folder).
MAX_BOX_WATCHERS = 4
#: The leases the children hold for their whole life, which say whether one
#: runs: `probe.sdk.delivery.outbox.lease._lease_path`, `probe.sdk.run.watcher.lease.lock_path`
#: (tests/test_service_background.py holds them equal).
DRAIN_LEASE = ".worker.lock"
BOX_LEASE = "watcher.lock"
#: `probe.sdk.delivery.outbox.drainers.detached._LOG_NAME`: the drainer's output, beside its queue.
DRAIN_LOG = "drainer.log"
#: Set for every drainer child, as the SDK sets it (no delivery notices in drainer.log).
WORKER_ENV = "PROBE_OUTBOX_WORKER"
#: What a caller's environment may never set for a child of this service (plan D25): the
#: interpreter, its libraries and search path stay this service's own.
CHILD_ENV_DROPPED = ("LD_", "DYLD_", "PYTHON", "VIRTUAL_ENV", "CONDA_", "UV_TOOL_")
CHILD_ENV_DROPPED_NAMES = frozenset({"PATH"})


def strip_caller_env(env: dict) -> dict:
    """`env` without what would change this service's interpreter or where it finds programs."""
    return {
        name: value for name, value in env.items()
        if name not in CHILD_ENV_DROPPED_NAMES and not name.startswith(CHILD_ENV_DROPPED)
    }


#: Test-only (API v1, "Lifecycle"): where the telemetry thread POSTs instead
#: of PostHog. Nothing in production sets it.
TELEMETRY_HOST_ENV = "PROBE_SERVICE_TELEMETRY_HOST"


class _Child:
    __slots__ = ("key", "pid", "popen", "started", "is_stopped", "free_since", "consent")

    def __init__(self, key: str, popen: subprocess.Popen, env: dict | None = None,
                 consent_names: tuple = ()) -> None:
        self.key = key
        #: The opt-outs of the environment it runs with (the SDK caller's): a
        #: report about it asks them (the owner's `consent_names`), never the rest of it.
        self.consent = ({name: env[name] for name in consent_names if isinstance(env.get(name), str)}
                        if env is not None else None)
        self.pid = popen.pid
        self.popen = popen
        self.started = time.monotonic()
        #: Told to stop (`_stop_stalled`): it is not told twice.
        self.is_stopped = False
        #: When its key's lease was first seen free since STALL_S (else None).
        self.free_since: float | None = None


def _is_usable_dir(path: str) -> bool:
    """A folder of this user's (the outbox's journal is 0700, its own)."""
    try:
        st = os.stat(path)
    except OSError:
        return False
    return stat.S_ISDIR(st.st_mode) and st.st_uid == os.getuid()


def _is_usable_python(path: str) -> bool:
    return os.path.isfile(path) and os.access(path, os.X_OK)


def _is_lease_held(path: str) -> bool:
    """Does a live process hold the flock lease at `path`? A shared,
    non-blocking probe let go at once: it conflicts only with a holder's
    exclusive lock, and creates nothing. Absent or unreadable: no -- a child
    is then started, and one that meets a held lease steps aside."""
    import fcntl

    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError:
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    except OSError:
        return False
    else:
        with contextlib.suppress(OSError):
            fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


class BackgroundHost:
    """Children for outbox drains and box watchers, and a telemetry thread (DESIGN.md).

    The server calls `drain` and `watch_box` on a thread, never its loop: they stat files and fork.
    A child counts against the limits until its waiter reaps it."""

    def __init__(
        self, *, log: Callable[[str], None], max_drains: int = MAX_DRAINS,
        incident: Callable[..., None] = lambda *args, **kwargs: None, consent_names: tuple = (),
    ) -> None:
        self.log = log
        #: `incident(what, run, facts, env=...)`: a child that failed early (plan B2); the machine
        #: service reports it (its watch), a delivery service does not.
        self.incident = incident
        #: The variables a report about a child asks for its consent (the machine's watch's).
        self.consent_names = consent_names
        self.max_drains = max_drains
        self._lock = threading.Lock()
        #: key -> its latest child (what `_is_young` asks about).
        self._children: dict[str, _Child] = {}
        #: pid -> every child not reaped yet.
        self._live: dict[int, _Child] = {}
        #: Keys whose child is being started right now (outside the lock).
        self._starting: set[str] = set()
        #: key -> until when (monotonic) hand-offs for it are refused.
        self._failing: dict[str, float] = {}
        self._is_closed = False
        self._telemetry: queue.Queue = queue.Queue(maxsize=MAX_TELEMETRY_BATCHES)
        self._sender: threading.Thread | None = None
        #: The ids of the batches taken lately, oldest first (`telemetry.send`'s `id`).
        self._batches: collections.OrderedDict = collections.OrderedDict()
        self.sent = self.dropped = 0
        #: Test seam: what POSTs one batch (`_post` by default).
        self.transport: Callable[[list], None] | None = None
        self.started = self.ended = self.stopped = 0
        #: Box watchers as threads of this service (X9); a caller it cannot report for gets a child.
        self.watchers = WatcherThreads(
            log=log, cwd=lambda: str(paths.service_dir()),
            spawn=lambda argv, env, **kw: self._spawn(argv, strip_caller_env(env), **kw),
        )
        #: In-code keys handed over for their queues' drains (`credentials.hold`, plan D21).
        self.credentials = HeldCredentials()
        #: The interpreter the drains run on: this service's own (plan D8; tests point it at a script).
        self.drain_python = sys.executable

    # -- children ------------------------------------------------------------

    def drain(self, request: dict) -> dict:
        """`outbox.drain`: this service's own drain of `request["dir"]` (plan D8), a child on this
        service's interpreter. Its environment: the caller's settings and credentials (D11), else
        a key held for that credential queue (`credentials.hold`); never written anywhere."""
        # Here, not at the top: the service's start path imports nothing past the stdlib and itself.
        from probe.analytics import WORKER_SURFACE_ENV, ProductSurface

        directory = os.path.realpath(request["dir"])
        if not _is_usable_dir(directory):
            return {"accepted": False, "reason": BackgroundRefusal.UNUSABLE}
        # The drainer's events say `service`, whoever asked for it (S4).
        env = {**self.credentials.get_env_for(directory), **strip_caller_env(request["env"]), WORKER_ENV: "1",
               WORKER_SURFACE_ENV: ProductSurface.SERVICE.value}
        return self._start(
            directory,
            build_module_argv(self.drain_python, DRAIN_MODULE, [directory], get_package_dir()),
            env,
            lease=os.path.join(directory, DRAIN_LEASE),
            cwd=directory,
            log_path=os.path.join(directory, DRAIN_LOG),
            limit=self.max_drains,
            python=self.drain_python,
        )

    def watch_box(self, request: dict) -> dict:
        """`box.watch`: the watcher of the box registry PROBE_BOX_DIR names, a thread of this
        service (X9: no process), or a child on this service's interpreter (`-I`, never one the
        caller names, D25) with the caller's settings when its login or network settings differ
        from the service's. The registry's lease keeps it one per registry either way."""
        named = os.path.abspath(request["env"]["PROBE_BOX_DIR"])
        key = BOX_PREFIX + os.path.realpath(named)
        if is_same_report_env(request["env"]):
            return self.watchers.start(key, named, request["env"], room=self._get_box_room())
        # One watcher serves every run in its registry, and each entry names its own address:
        # never the caller's key or address, or one job's key reports another's runs (#4287 review).
        env = {name: value for name, value in strip_caller_env(request["env"]).items()
               if name not in CREDENTIAL_ENV and name != BASE_URL_ENV}
        return self._start(
            key,
            build_module_argv(self.drain_python, BOX_MODULE, [], get_package_dir()),
            env,
            # Where the watcher takes it (`spawn.lock_path`: the named folder's
            # parent, a symlinked leaf not followed); the key is the real folder.
            lease=os.path.join(os.path.dirname(named), BOX_LEASE),
            cwd=str(paths.service_dir()),
            log_path=None,
            limit=MAX_BOX_WATCHERS,
            python=self.drain_python,
        )

    def _get_box_room(self) -> int:
        """Box watchers this service may still add besides its threads (`WatcherThreads.start`
        counts those under its own lock)."""
        with self._lock:
            children = sum(1 for c in self._live.values() if c.key.startswith(BOX_PREFIX))
            children += sum(1 for k in self._starting if k.startswith(BOX_PREFIX))
        return MAX_BOX_WATCHERS - children

    def resume_watcher(self) -> None:
        """At the service's start: watch this machine's registry when it still lists a run (an
        earlier service died without handing it off). Blocking (reads a folder): a thread."""
        try:
            from probe.sdk.run.watcher import registry, watcher

            if not watcher.enabled():
                return
            named = os.path.abspath(str(registry.default_dir()))
            if not any(registry.is_local(entry) for entry in registry.entries(named)):
                return
            self.watchers.start(BOX_PREFIX + os.path.realpath(named), named, {}, room=self._get_box_room())
        except Exception as exc:  # noqa: BLE001 -- the next run to start asks again
            self.log(f"background: could not resume the watcher: {exc!r}")

    def _start(
        self, key: str, argv: list, env: dict, *, lease: str, cwd: str, log_path: str | None, limit: int,
        python: str,
    ) -> dict:
        """Start `argv` for `key` unless someone delivers for it: RUNNING when a start is under way here
        or its lease is held, BUSY past a limit, else a new child (DESIGN.md, Traps: "One drainer per outbox")."""
        if not _is_usable_python(python):
            return {"accepted": False, "reason": BackgroundRefusal.UNUSABLE}
        with self._lock:
            if self._is_closed:
                return {"accepted": False, "reason": BackgroundRefusal.STOPPING}
            if key in self._starting or self._is_young(key):
                return {"accepted": True, "state": BackgroundState.RUNNING}
            if self._failing.get(key, 0.0) > time.monotonic():
                return {"accepted": False, "reason": BackgroundRefusal.FAILING}
        if _is_lease_held(lease):
            with self._lock:  # someone holds it: no child of this key is seen free any more
                for c in self._live.values():
                    if c.key == key:
                        c.free_since = None
            return {"accepted": True, "state": BackgroundState.RUNNING}
        self._stop_stalled(key)
        box = key.startswith(BOX_PREFIX)
        with self._lock:
            # Again: another thread may have started one since the first look.
            if key in self._starting or self._is_young(key):
                return {"accepted": True, "state": BackgroundState.RUNNING}
            self._failing.pop(key, None)
            mine = sum(1 for c in self._live.values() if c.key == key)
            kind = sum(1 for c in self._live.values() if c.key.startswith(BOX_PREFIX) == box)
            kind += sum(1 for k in self._starting if k.startswith(BOX_PREFIX) == box)
            if box:
                kind += self.watchers.count()
            if mine >= MAX_PER_KEY or kind >= limit:
                return {"accepted": False, "reason": BackgroundRefusal.BUSY}
            # Its slot, held while it starts: the lock is never held over a
            # fork (`service.status` reads `public` on the service's loop).
            self._starting.add(key)
        return self._launch(key, argv, env, cwd=cwd, log_path=log_path)

    def _launch(self, key: str, argv: list, env: dict, *, cwd: str, log_path: str | None) -> dict:
        """Fork `key`'s reserved child and its waiter; the slot is let go whatever happens."""
        child = None
        try:
            child = _Child(key, self._spawn(argv, env, cwd=cwd, log_path=log_path), env, self.consent_names)
            with self._lock:
                self._children[key] = child
                self._live[child.pid] = child
                self.started += 1
            threading.Thread(
                target=self._wait_for_exit, args=(child,), name=f"probe-background-{child.pid}", daemon=True
            ).start()
        except Exception as exc:  # noqa: BLE001 -- OSError, SubprocessError, no thread: the next ask tries again
            self.log(f"background: could not start {get_argv_module(argv)} (or its waiter) for {key}: {exc!r}")
            if child is not None:
                # No waiter would ever reap it: it goes now (still importing:
                # nothing of the outbox is its yet), and it counts until it is
                # gone, so a thread that will not start never lets children
                # past the limits.
                self._kill_and_reap(child)
            return {"accepted": False, "reason": BackgroundRefusal.UNUSABLE}
        finally:
            with self._lock:
                self._starting.discard(key)
        self.log(f"background: {get_argv_module(argv)} started for {key} (pid {child.pid})")
        return {"accepted": True, "state": BackgroundState.STARTED}

    def _kill_and_reap(self, child: _Child) -> None:
        """SIGKILL a child no waiter watches and reap it here; it leaves the
        books only once reaped (one that will not die keeps its place)."""
        with contextlib.suppress(OSError):
            child.popen.kill()
        try:
            child.popen.wait(REAP_WAIT_S)
        except subprocess.TimeoutExpired:
            self.log(f"background: {child.key}'s child (pid {child.pid}) would not die: it stays counted")
            return
        with self._lock:
            if self._children.get(child.key) is child:
                del self._children[child.key]
            self._live.pop(child.pid, None)

    def _is_young(self, key: str) -> bool:
        """`key`'s child started under STARTUP_S ago and runs: it is still
        importing, its lease not taken yet. (A worker that took its lease keeps
        it longer than that: it lingers `outbox.linger._LINGER_SECONDS` with
        its queue empty before it exits.) Under the lock."""
        child = self._children.get(key)
        return child is not None and time.monotonic() - child.started < STARTUP_S and child.popen.poll() is None

    def _stop_stalled(self, key: str) -> None:
        """`key`'s lease is free. A child of it started STALL_S ago or more
        and still running, which found it free on two looks STALL_CONFIRM_S
        apart, never took it: its start hangs. (One look is not enough: a
        drainer that ran a long while lets its lease go a moment before it
        exits, its last report still to send, and is gone within FLUSH_S.)
        SIGTERM, once; it stays counted until its waiter reaps it."""
        now = time.monotonic()
        stalled = []
        with self._lock:
            for live in self._live.values():
                if live.key != key or live.is_stopped or now - live.started < STALL_S or live.popen.poll() is not None:
                    continue
                if live.free_since is None:
                    live.free_since = now
                elif now - live.free_since >= STALL_CONFIRM_S:
                    live.is_stopped = True
                    stalled.append(live)
        for child in stalled:
            with contextlib.suppress(OSError):
                child.popen.terminate()
            self.stopped += 1
            self.log(f"background: {key}'s child (pid {child.pid}) never took its lease in {STALL_S:.0f} s: stopped")

    @staticmethod
    def _spawn(argv: list, env: dict, *, cwd: str, log_path: str | None) -> subprocess.Popen:
        """The child, in a session of its own (it outlives this service, and a
        signal to the service's group is not its). Its environment: the
        service's own clean one plus the caller's (`env`). Output to its log
        (0600, never through a symlink planted there), else nowhere."""
        out = (
            # Never a link or a FIFO planted at its name (#4279 round 3: never blocks the service's thread).
            os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0),
                    0o600)
            if log_path
            else os.open(os.devnull, os.O_WRONLY)
        )
        # Never a credential, the service's own included (it starts with a
        # clean environment; this keeps that true whatever ran in it since). The request's part
        # was stripped of loader, Python and PATH overrides already (`strip_caller_env`); the
        # service's own are kept (H-4: a module-loaded Python needs its LD_LIBRARY_PATH).
        own = {name: value for name, value in os.environ.items() if not secret_env(name)}
        env = {**own, **env}
        try:
            return subprocess.Popen(  # noqa: S603 -- this service's interpreter, `-I`, our module
                argv,
                stdin=subprocess.DEVNULL,
                stdout=out,
                stderr=out,
                cwd=cwd,
                env=env,
                start_new_session=True,
                close_fds=True,
            )
        finally:
            os.close(out)

    def _wait_for_exit(self, child: _Child) -> None:
        code = child.popen.wait()
        lived = time.monotonic() - child.started
        with self._lock:
            if self._children.get(child.key) is child:
                del self._children[child.key]
            self._live.pop(child.pid, None)
            self.ended += 1
            failed = code > 0 and code not in CLEAN_EXITS and lived < EARLY_EXIT_S
            if failed:
                self._failing[child.key] = time.monotonic() + FAILING_S
        if failed:
            self.log(
                f"background: {child.key}'s child (pid {child.pid}) exited {code} after {lived:.1f} s; "
                f"its callers start their own for {FAILING_S:.0f} s"
            )
            # Its FAILING state: a `background` report (plan B2).
            self.incident("early_exit", None, {
                "kind": "box_watch" if child.key.startswith(BOX_PREFIX) else "outbox_drain", "code": code,
                "lived_s": round(lived, 1),
            }, env=child.consent)
        else:
            self.log(f"background: {child.key}'s child (pid {child.pid}) exited {code} after {lived:.1f} s")

    # -- telemetry -----------------------------------------------------------

    def send_telemetry(self, entries: list, batch_id: str | None = None) -> dict:
        """`telemetry.send`: queue one batch for the sender thread. A batch
        whose id was taken already is acknowledged again and not queued twice:
        before any refusal, since what was taken stays taken (a caller that
        had no answer in time resends it, and a STOPPING then would make it
        send its own copy)."""
        with self._lock:
            if batch_id is not None and batch_id in self._batches:
                return {"accepted": True}
            if self._is_closed:
                return {"accepted": False, "reason": BackgroundRefusal.STOPPING}
            try:
                self._telemetry.put_nowait(entries)
            except queue.Full:
                return {"accepted": False, "reason": BackgroundRefusal.BUSY}
            if batch_id is not None:
                self._batches[batch_id] = None
                while len(self._batches) > MAX_BATCH_IDS:
                    self._batches.popitem(last=False)
            if self._sender is None or not self._sender.is_alive():
                self._sender = threading.Thread(target=self._run_sender, name="probe-telemetry-send", daemon=True)
                self._sender.start()
        return {"accepted": True}

    def _run_sender(self) -> None:
        while True:
            entries = self._telemetry.get()
            if entries is None:
                return
            try:
                (self.transport or _post)(entries)
                self.sent += 1
            except Exception:  # noqa: BLE001 -- telemetry is a bystander: PostHog down costs nothing
                self.dropped += 1

    # -- the service ---------------------------------------------------------

    def public(self) -> dict:
        with self._lock:
            now = time.monotonic()
            listed = [(c.key, {"pid": c.pid, "running_s": round(now - c.started, 1)}) for c in self._live.values()]
            return {
                "drains": [row for k, row in listed if not k.startswith(BOX_PREFIX)],
                "box_watchers": [row for k, row in listed if k.startswith(BOX_PREFIX)] + self.watchers.list_rows(),
                "started": self.started + self.watchers.started,
                "telemetry": {"queued": self._telemetry.qsize(), "sent": self.sent, "dropped": self.dropped},
            }

    def close(self, flush_s: float = 0.0) -> None:
        """Take nothing more. The children go on (their outbox and lease are
        theirs). The telemetry already taken is sent for up to `flush_s`
        (the SDK sender's own exit flush, FLUSH_S, when the service stops):
        a batch still unsent after that is dropped, as the sender's own are.
        Blocks up to `flush_s`: the server calls it on a thread. The watcher
        threads stop, each handed to a detached watcher while its registry
        lists a run (`watchers.WatcherThreads.close`)."""
        with self._lock:
            self._is_closed = True
            sender = self._sender
        self.watchers.close()
        if sender is None:
            return
        with contextlib.suppress(queue.Full):
            self._telemetry.put_nowait(None)  # after what is queued: it is sent first
        if flush_s > 0:
            sender.join(flush_s)


def _post(entries: list) -> None:
    """One batch, over the SDK's TLS trust (`probe.foundation.tls.tls`, the rule every
    connection of the package follows), as the caller's sender would have."""
    from probe.analytics import core as core
    from probe.foundation.tls.tls import ssl_context

    host = os.environ.get(TELEMETRY_HOST_ENV)
    if host:
        core.POSTHOG_HOST = host  # test-only; this process sends nothing else through the core
    core.post_batch(entries, context=ssl_context())
