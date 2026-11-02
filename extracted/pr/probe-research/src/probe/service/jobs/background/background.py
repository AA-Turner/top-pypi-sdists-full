"""BackgroundHost: the service starts a training process's outbox drainer and box watcher as its own children, and posts its
telemetry batches (plan Q5). How and why: DESIGN.md beside this file."""

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

from ....foundation.service_api import paths
from ....foundation.service_api.vocabularies import BackgroundRefusal, BackgroundState
from ....foundation.service_api.env import secret_env
from ...watch.incident import Family
from ...watch.consent import consent_env

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
DRAIN_MODULE = "probe.sdk.outbox_worker"
BOX_MODULE = "probe.box"
#: A box watcher's key: this, then its registry folder (one watcher per registry).
BOX_PREFIX = "box:"
#: Box watchers running at once, at most (one per registry folder).
MAX_BOX_WATCHERS = 4
#: The leases the children hold for their whole life, which say whether one
#: runs: `probe.sdk.delivery.outbox.lease._lease_path`, `probe.box.spawn.lock_path`
#: (tests/test_service_background.py holds them equal).
DRAIN_LEASE = ".worker.lock"
BOX_LEASE = "watcher.lock"
#: `probe.sdk.delivery.outbox.drainers.detached._LOG_NAME`: the drainer's output, beside its queue.
DRAIN_LOG = "drainer.log"
#: Set for every drainer child, as the SDK sets it (no delivery notices in drainer.log).
WORKER_ENV = "PROBE_OUTBOX_WORKER"
#: Test-only (API v1, "Lifecycle"): where the telemetry thread POSTs instead
#: of PostHog. Nothing in production sets it.
TELEMETRY_HOST_ENV = "PROBE_SERVICE_TELEMETRY_HOST"


class _Child:
    __slots__ = ("key", "pid", "popen", "started", "stopped", "free_since", "consent")

    def __init__(self, key: str, popen: subprocess.Popen, env: dict | None = None) -> None:
        self.key = key
        #: The opt-outs of the environment it runs with (the SDK caller's): a
        #: report about it asks them (`watch.consent_env`), never the rest of it.
        self.consent = consent_env(env) if env is not None else None
        self.pid = popen.pid
        self.popen = popen
        self.started = time.monotonic()
        #: Told to stop (`_stop_stalled`): it is not told twice.
        self.stopped = False
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


def _get_child_cwd(request: dict, default: str) -> str:
    """The caller's working folder when it names one that exists: the child
    then imports what the caller's own fork would have (`-m` puts the working
    folder on `sys.path`, and a relative PYTHONPATH reads from it). Else
    `default`."""
    cwd = request.get("cwd")
    return cwd if cwd and os.path.isdir(cwd) else default


def is_other_network(pid: int | None) -> bool:
    """Linux: is `pid` in another network namespace than this service (an
    agent's sandbox with no network, `unshare -n`)? `caller.sandboxed` reads
    the mount and user namespaces, not this one. Unknown counts as yes, as
    there; elsewhere, no."""
    if not sys.platform.startswith("linux"):
        return False
    if pid is None:
        return True
    try:
        theirs, own = os.stat(f"/proc/{pid}/ns/net"), os.stat("/proc/self/ns/net")
    except OSError:
        return True
    return (theirs.st_dev, theirs.st_ino) != (own.st_dev, own.st_ino)


#: The old name, for one release: 0.357.0's daemon host imports it lazily (`daemon/host/host.py`).
other_network = is_other_network


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
        incident: Callable[..., None] = lambda *args, **kwargs: None,
    ) -> None:
        self.log = log
        #: The service's watch (`watch.Watch.note`): a child that failed early (plan B2).
        self.incident = incident
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
        self._closed = False
        self._telemetry: queue.Queue = queue.Queue(maxsize=MAX_TELEMETRY_BATCHES)
        self._sender: threading.Thread | None = None
        #: The ids of the batches taken lately, oldest first (`telemetry.send`'s `id`).
        self._batches: collections.OrderedDict = collections.OrderedDict()
        self.sent = self.dropped = 0
        #: Test seam: what POSTs one batch (`_post` by default).
        self.transport: Callable[[list], None] | None = None
        self.started = self.ended = self.stopped = 0

    # -- children ------------------------------------------------------------

    def drain(self, request: dict) -> dict:
        """`outbox.drain`: a drainer child for `request["dir"]`."""
        directory = os.path.realpath(request["dir"])
        if not _is_usable_dir(directory):
            return {"accepted": False, "reason": BackgroundRefusal.UNUSABLE}
        return self._start(
            directory,
            [request["python"], "-m", DRAIN_MODULE, directory],
            {**request["env"], WORKER_ENV: "1"},
            lease=os.path.join(directory, DRAIN_LEASE),
            cwd=_get_child_cwd(request, directory),
            log_path=os.path.join(directory, DRAIN_LOG),
            limit=self.max_drains,
            python=request["python"],
        )

    def watch_box(self, request: dict) -> dict:
        """`box.watch`: the watcher child of the box registry PROBE_BOX_DIR
        names (its own lease keeps it one per registry)."""
        named = os.path.abspath(request["env"]["PROBE_BOX_DIR"])
        return self._start(
            BOX_PREFIX + os.path.realpath(named),
            [request["python"], "-m", BOX_MODULE],
            dict(request["env"]),
            # Where the watcher takes it (`spawn.lock_path`: the named folder's
            # parent, a symlinked leaf not followed); the key is the real folder.
            lease=os.path.join(os.path.dirname(named), BOX_LEASE),
            cwd=_get_child_cwd(request, str(paths.service_dir())),
            log_path=None,
            limit=MAX_BOX_WATCHERS,
            python=request["python"],
        )

    def _start(
        self, key: str, argv: list, env: dict, *, lease: str, cwd: str, log_path: str | None, limit: int,
        python: str,
    ) -> dict:
        """Start `argv` for `key` unless someone delivers for it: RUNNING when a start is under way here
        or its lease is held, BUSY past a limit, else a new child (DESIGN.md, Traps: "One drainer per outbox")."""
        if not _is_usable_python(python):
            return {"accepted": False, "reason": BackgroundRefusal.UNUSABLE}
        with self._lock:
            if self._closed:
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
            child = _Child(key, self._spawn(argv, env, cwd=cwd, log_path=log_path), env)
            with self._lock:
                self._children[key] = child
                self._live[child.pid] = child
                self.started += 1
            threading.Thread(
                target=self._wait_for_exit, args=(child,), name=f"probe-background-{child.pid}", daemon=True
            ).start()
        except Exception as exc:  # noqa: BLE001 -- OSError, SubprocessError, no thread: the caller forks its own
            self.log(f"background: could not start {argv[2]} (or its waiter) for {key}: {exc!r}")
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
        self.log(f"background: {argv[2]} started for {key} (pid {child.pid})")
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
            for c in self._live.values():
                if c.key != key or c.stopped or now - c.started < STALL_S or c.popen.poll() is not None:
                    continue
                if c.free_since is None:
                    c.free_since = now
                elif now - c.free_since >= STALL_CONFIRM_S:
                    c.stopped = True
                    stalled.append(c)
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
            os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
            if log_path
            else os.open(os.devnull, os.O_WRONLY)
        )
        # Never a credential, the service's own included (it starts with a
        # clean environment; this keeps that true whatever ran in it since).
        own = {name: value for name, value in os.environ.items() if not secret_env(name)}
        try:
            return subprocess.Popen(  # noqa: S603 -- the caller's interpreter (same user, not sandboxed), our module
                argv,
                stdin=subprocess.DEVNULL,
                stdout=out,
                stderr=out,
                cwd=cwd,
                env={**own, **env},
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
            self.incident(Family.BACKGROUND, "early_exit", None, {
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
            if self._closed:
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
                "box_watchers": [row for k, row in listed if k.startswith(BOX_PREFIX)],
                "started": self.started,
                "telemetry": {"queued": self._telemetry.qsize(), "sent": self.sent, "dropped": self.dropped},
            }

    def close(self, flush_s: float = 0.0) -> None:
        """Take nothing more. The children go on (their outbox and lease are
        theirs). The telemetry already taken is sent for up to `flush_s`
        (the SDK sender's own exit flush, FLUSH_S, when the service stops):
        a batch still unsent after that is dropped, as the sender's own are.
        Blocks up to `flush_s`: the server calls it on a thread."""
        with self._lock:
            self._closed = True
            sender = self._sender
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
