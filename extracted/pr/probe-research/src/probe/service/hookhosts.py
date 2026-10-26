"""The warm hook hosts the service runs, one per plugin folder sessions use (plan A0, D34).

    hooks.host {root}    a session's dispatcher found no host for its plugin
                         folder: start `python3 -S <root>/hooks/zygote.py`, which
                         serves `/tmp/probe-<uid>/hooks-<hash>.sock`
                         (`hooks/dispatch.py` `host_socket`). Its events then run
                         as children forked from it, warm, until it exits.

    hooks.run {plugin_root, lane, payload, env, cwd, timeout_ms}
                         a harness with no hooks of its own (pi, plan D38) has
                         one event run for a plugin folder: that lane's routes,
                         exactly as the folder's dispatcher runs them for
                         Claude Code, and their merged output comes back
                         (`run_event`). On the folder's warm host when one
                         answers in time (the service is its client, and hands
                         it pipes of its own for the event's stdout and
                         stderr, the fds a socket from Node cannot carry); else
                         as a fresh `hooks/dispatch.sh <lane>`, and the host is
                         started for the next event.

Every event handed to a host carries the host's key (`host_key_path`, written
by the host beside its socket): a host runs nothing for a client without it,
so a process that merely reaches the socket cannot hand it a forged event
(#3355). A host from before keys ignores the field.

The host is the plugin's own code, run by the system `python3` the way every
hook runs, never the CLI's environment: what a hook does is unchanged, only
where it starts from. The service owns the processes: it starts them, keeps
at most MAX_HOSTS (the oldest stops first), and stops them when it stops (they
also exit when it is gone, after IDLE_S idle, or when their folder's
dispatcher changes). A folder is hosted only when it holds a Probe plugin's
dispatcher and host, so a request cannot name some other program.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import select
import shutil
import signal
import socket
import stat
import subprocess
import threading
import time
from pathlib import Path

from . import paths
from .watch import Family

MAX_HOSTS = 8
#: A plugin folder's manifest or routes.json is read only when it is a regular
#: file of at most this many bytes (they are a few KB): a request names the
#: folder, so a FIFO there must not block the service, nor a huge file fill it.
MAX_PLUGIN_FILE = 1024 * 1024
#: `hooks.run`: lanes never handed to a host (`hooks/dispatch.py` UNHOSTED_LANES):
#: SessionEnd (its 1.5 s phase cannot wait on a host holding its pipes).
UNHOSTED_LANES = frozenset({"session-end"})
#: `hooks.run`: each hosted lane's own budget (`hooks/dispatch.py` `budget`,
#: from its frozen hooks.json entry's timeout): an event the host started runs
#: to its end within it, as every hosted event does, whether or not its caller
#: still waits (tests/test_service_hooks_run.py holds the two equal).
LANE_BUDGET_S = {
    "session-start": 59.0,
    "prompt": 9.0,
    "pre-compact": 10.0,
    "pre-tool": 5.0,
    "post-tool": 5.0,
    "stop": 15.0,
    "turn-started": 5.0,
}
#: `dispatch.py` MARGIN_S: a hosted event's deadline is its budget and this.
HOST_MARGIN_S = 1.0
#: `hooks.run`: what comes back of each of the event's stdout and stderr, at most.
MAX_HOOK_OUTPUT = 128 * 1024
#: `hooks.run`: once the event's process has exited, how long its pipes are
#: still read (something it left behind may hold them open, as `dispatch.py`'s
#: `run_all` allows).
DRAIN_S = 0.05
#: `hooks.run`: how often a waiting run looks whether its dispatcher exited.
POLL_S = 0.01
#: `hooks.run`: an overrun dispatcher is asked to stop (its own handler stops
#: every route it started) this long before it is killed.
KILL_WAIT_S = 0.1
#: The variables a `hooks.run` event gets from the service, never from the
#: caller: what the harness and the dispatcher set themselves.
RUN_OWNED_ENV = (
    "PLUGIN_ROOT",
    "CLAUDE_PLUGIN_ROOT",
    "PROBE_HOOKS_HANDED_OVER",
    "PROBE_HOOK_HOSTED",
    "PROBE_HOOK_HOST",
    "PROBE_HOOK_DEADLINE",
    "PROBE_HOOK_PARENT_PID",
)
#: A queued event (`hooks.queue`) keeps its harness's root variables, the
#: event's own: only the dispatcher's are set here instead.
QUEUE_OWNED_ENV = RUN_OWNED_ENV[2:]

#: The plugin manifests a hosted folder must carry (one is enough), naming a Probe plugin.
MANIFESTS = (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".kimi-plugin/plugin.json")
PROBE_PLUGINS = ("probe-research", "probe-research-daemon")


class Via:
    """`hooks.run`'s `via`: where the event ran (null: nowhere, out of time)."""

    HOST = "host"
    PROCESS = "process"


def host_socket(root: str) -> Path:
    """The host's socket: `hooks/dispatch.py` `host_socket`, the same bytes."""
    digest = hashlib.sha256(os.fsencode(os.path.realpath(root))).hexdigest()[:16]
    return Path("/tmp") / f"probe-{os.getuid()}" / f"hooks-{digest}.sock"


def host_key_path(root: str) -> Path:
    """The host's key beside its socket (`hooks/zygote.py` `key_path`, `dispatch.py` `host_key_path`)."""
    return host_socket(root).with_suffix(".key")


def _host_key(root: str) -> str | None:
    """The folder's host key, which every event this service hands the host must
    carry (#3355), or None: a host from before keys (it ignores the field).
    Never waits (`read_plugin_file`'s open: non-blocking, no symlink, a regular
    file only), so a FIFO at the key's path never stalls a `hooks.run`."""
    try:
        fd = os.open(host_key_path(root), os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
                     | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NOCTTY", 0))
    except OSError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        key = os.read(fd, 130).decode("ascii", "replace").strip()
    except OSError:
        return None
    finally:
        os.close(fd)
    return key if len(key) == 64 and all(c in "0123456789abcdef" for c in key) else None


def read_plugin_file(path: Path) -> str | None:
    """A plugin folder's small file, or None: a regular file (never followed
    through a symlink, never a FIFO or device: opened non-blocking, checked
    after opening) of at most MAX_PLUGIN_FILE bytes, read bounded."""
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_NOCTTY", 0))
    except OSError:
        return None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_PLUGIN_FILE:
            return None
        chunks, size = [], 0
        while size <= MAX_PLUGIN_FILE:
            chunk = os.read(fd, 65536)
            if not chunk:
                return b"".join(chunks).decode("utf-8")
            chunks.append(chunk)
            size += len(chunk)
        return None
    except (OSError, UnicodeDecodeError):
        return None
    finally:
        os.close(fd)


def probe_plugin(root: Path) -> bool:
    """Is `root` a Probe plugin folder with a dispatcher and a host, owned by this user?"""
    try:
        if root.lstat().st_uid != os.getuid():
            return False
    except OSError:
        return False
    hooks = root / "hooks"
    if not (hooks / "zygote.py").is_file() or not (hooks / "dispatch.py").is_file():
        return False
    for name in MANIFESTS:
        text = read_plugin_file(root / name)
        if text is None:
            continue
        try:
            data = json.loads(text)
        except ValueError:
            continue
        if isinstance(data, dict) and data.get("name") in PROBE_PLUGINS:
            return True
    return False


class HookHosts:
    """The hosts, safe to use from several threads: the service starts them on
    worker threads (`hooks.host`, a `hooks.run` warm-up), since checking a
    folder and starting a process block, and reads them on its loop
    (`service.status`). The lock guards `hosts` and is never held across a
    file read or a process start; a folder being started is in `_starting`,
    so two requests never start two hosts for it, and one about to start
    holds a place in `_reserved`: running hosts and reserved places together
    never pass MAX_HOSTS (the oldest host stops to make room)."""

    def __init__(self, log, *, incident=lambda *args, **kwargs: None) -> None:
        self.log = log
        #: The service's watch (`watch.Watch.note`): a host that died (plan B2).
        self.incident = incident
        #: realpath of the plugin folder -> (process, started monotonic)
        self.hosts: dict = {}
        #: interpreter -> is it 3.9 or newer (asked once: the check is a process start)
        self._checked: dict = {}
        self._lock = threading.Lock()
        self._starting: set = set()
        self._reserved: set = set()
        self._closed = False

    def _python(self, asked: object = None) -> str | None:
        """The interpreter the asking dispatcher runs on (the harness's, as a
        fresh event would have), else the service PATH's `python3`; only a
        3.9 or newer (the host's `recv_fds`)."""
        found = []
        if isinstance(asked, str) and asked.startswith("/") and len(asked) <= 4096:
            found.append(asked)
        found.append(shutil.which("python3") or ("/usr/bin/python3" if os.path.exists("/usr/bin/python3") else ""))
        for python in found:
            if not python or not os.path.isfile(python) or not os.access(python, os.X_OK):
                continue
            if python not in self._checked:
                try:
                    done = subprocess.run(  # noqa: S603 -- a version check, no shell
                        [python, "-S", "-c", "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"],
                        stdin=subprocess.DEVNULL, capture_output=True, timeout=2, check=False,
                    )
                    self._checked[python] = done.returncode == 0
                except (OSError, subprocess.SubprocessError):
                    self._checked[python] = False
            if self._checked[python]:
                return python
        return None

    def python_for(self, asked: object = None) -> str | None:
        """`_python`, for another of the plugin's scripts the service runs the
        way a hook runs it (`statusline.refresh`). Blocking: a worker thread."""
        return self._python(asked)

    def _reap(self) -> None:
        """Under the lock. A host that exited on its own with an error or a
        signal is one event of `hook_host` (plan B2): one the service stopped
        left `hosts` first (`_stop`), and an idle or outdated host exits 0."""
        for root, (proc, _) in list(self.hosts.items()):
            code = proc.poll()
            if code is not None:
                del self.hosts[root]
                if code != 0:
                    self.log(f"hook host for {root} (pid {proc.pid}) exited {code}")
                    self.incident(Family.HOOK_HOST, "host_exited", None, {"code": code, "root": root})

    def host(self, params: dict) -> dict:
        """`hooks.host`: `{"running": bool, "started": bool}`, or `{"refused": why}`.
        Blocking (it reads the folder and starts a process): the service calls
        it on a worker thread, never its loop."""
        if os.name == "nt":
            return {"refused": "no hook host on Windows (it forks each event)"}
        raw = params.get("root")
        if not isinstance(raw, str) or not raw.startswith("/") or len(raw) > 4096:
            return {"refused": "root must be an absolute path"}
        root = Path(os.path.realpath(raw))
        with self._lock:
            if self._closed:
                return {"refused": "the service is stopping"}
            self._reap()
            if str(root) in self.hosts or str(root) in self._starting:
                return {"running": True, "started": False}
            self._starting.add(str(root))
        try:
            return self._start(root, params)
        finally:
            with self._lock:
                self._starting.discard(str(root))
                self._reserved.discard(str(root))

    def _make_room(self) -> None:
        """Under the lock: stop the oldest hosts until one more fits beside the
        running ones and the places reserved."""
        while self.hosts and len(self.hosts) + len(self._reserved) >= MAX_HOSTS:
            oldest = min(self.hosts, key=lambda r: self.hosts[r][1])
            self._stop(oldest)

    def _start(self, root: Path, params: dict) -> dict:
        if not probe_plugin(root):
            return {"refused": "not a Probe plugin folder with a hook host"}
        python = self._python(params.get("python"))
        if python is None:
            return {"refused": "no python 3.9 or newer"}
        with self._lock:
            self._make_room()
            if len(self.hosts) + len(self._reserved) >= MAX_HOSTS:
                return {"refused": "busy: too many hosts starting"}
            self._reserved.add(str(root))
        sock = host_socket(str(root))
        try:
            paths.private_dir(sock.parent)
            paths.private_dir(paths.service_dir())
            log_fd = os.open(paths.log_path(), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        except OSError as exc:
            return {"refused": f"cannot prepare the host: {exc}"}
        try:
            proc = subprocess.Popen(  # noqa: S603 -- the system python, the plugin's own host
                [python, "-S", str(root / "hooks" / "zygote.py"), str(sock), str(os.getpid())],
                stdin=subprocess.DEVNULL,
                stdout=log_fd,
                stderr=log_fd,
                cwd=str(root),
                env=dict(os.environ),
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            return {"refused": f"the host would not start: {exc}"}
        finally:
            os.close(log_fd)
        with self._lock:
            self._reserved.discard(str(root))
            if self._closed:
                # The service stopped while this one started: it stops too.
                with contextlib.suppress(OSError):
                    proc.send_signal(signal.SIGTERM)
                return {"refused": "the service is stopping"}
            self._make_room()
            self.hosts[str(root)] = (proc, time.monotonic())
        self.log(f"hook host started for {root} (pid {proc.pid})")
        return {"running": True, "started": True}

    def _stop(self, root: str) -> None:
        """Under the lock."""
        entry = self.hosts.pop(root, None)
        if entry is None:
            return
        proc = entry[0]
        with contextlib.suppress(OSError):
            proc.send_signal(signal.SIGTERM)

    def close(self) -> None:
        with self._lock:
            self._closed = True
            for root in list(self.hosts):
                self._stop(root)

    def public(self) -> list:
        with self._lock:
            self._reap()
            return [{"root": root, "pid": proc.pid} for root, (proc, _) in self.hosts.items()]

    def pids(self) -> set:
        """The pids of the warm hosts this service runs and has not reaped: the
        events forked from them are Probe's hooks, run for a dispatcher that
        held the host's key (#3355), so they may take a session's messages
        (`mailbox.claim`, #3361)."""
        with self._lock:
            return {proc.pid for proc, _ in self.hosts.values() if proc.returncode is None}


def runnable(request: dict) -> dict | None:
    """`hooks.run`'s folder check, as `hooks.host`'s: None when `request`'s root
    is a complete Probe plugin folder with a dispatcher and a host (its `root`
    is then that folder's real path), else `{"refused": why}`. It reads files
    the request names, so it runs on a `hooks.run` thread, never the loop."""
    if os.name != "posix":
        return {"refused": "hooks run on POSIX only"}
    root = Path(os.path.realpath(request["root"]))
    if not probe_plugin(root):
        return {"refused": "not a Probe plugin folder with a hook host"}
    if not complete(root):
        # A dispatcher with no routes.json exits 0 (fail open): an answer
        # the caller would read as "allowed", where its own check is better.
        return {"refused": "the plugin folder is incomplete"}
    request["root"] = str(root)
    return None


def complete(root: Path) -> bool:
    """`dispatch.py` `_complete`: dispatch.sh and dispatch.py, a routes.json
    that parses, and every hooks/ file its routes name. A copy still being
    written (or half deleted) answers nothing."""
    import re

    hooks = root / "hooks"
    if not os.access(hooks / "dispatch.sh", os.X_OK) or not os.access(hooks / "dispatch.py", os.R_OK):
        return False
    text = read_plugin_file(hooks / "routes.json")
    if text is None:
        return False
    try:
        wiring = json.loads(text)
    except ValueError:
        return False
    if not isinstance(wiring, dict) or not isinstance(wiring.get("hooks"), dict):
        return False
    named = set(re.findall(r"\$ROOT/hooks/([A-Za-z0-9_.-]+)", json.dumps(wiring)))
    return all((hooks / name).is_file() for name in named)


# -- hooks.run (plan D38) ----------------------------------------------------------


def _private(folder: str) -> bool:
    """`dispatch.py` `_private`: ours, a folder, writable by nobody else."""
    try:
        st = os.lstat(folder)
    except OSError:
        return False
    return stat.S_ISDIR(st.st_mode) and st.st_uid == os.getuid() and not st.st_mode & 0o022


def event_env(request: dict, parent: int | None, *, hosted: bool) -> dict:
    """The event's environment: the caller's (its session's, as a harness hands
    its hooks theirs), with what the harness and the dispatcher set themselves
    set here instead (RUN_OWNED_ENV). The routes find the folder through
    `CLAUDE_PLUGIN_ROOT` (`$ROOT`), so they run as Claude Code's plugin's, never
    as a Codex session's (`PLUGIN_ROOT`); a queued event (`request["queued"]`,
    `hooks.queue`) keeps the root variable its own harness set. The walk up to the agent
    (`_session_marker._ancestors`) starts at the caller (PROBE_HOOK_PARENT_PID),
    the process that asked: pi itself. A fresh dispatcher never hands the event
    on (`PROBE_HOOK_HOST=off`, no host: the service just asked it; the folder is
    the caller's to name, so no hand-over to another installed copy either)."""
    queued = bool(request.get("queued"))
    owned = QUEUE_OWNED_ENV if queued else RUN_OWNED_ENV
    env = {k: v for k, v in request["env"].items() if k not in owned}
    for name in ("HOME", "PATH"):
        if not env.get(name) and os.environ.get(name):
            env[name] = os.environ[name]
    if queued:
        # A queued event (plan D36) runs as its own harness ran it: under
        # Codex its routes read `PLUGIN_ROOT` (and export PROBE_AGENT=codex).
        env["PLUGIN_ROOT" if env.get("PLUGIN_ROOT") else "CLAUDE_PLUGIN_ROOT"] = request["root"]
    else:
        env["CLAUDE_PLUGIN_ROOT"] = request["root"]
    if parent is not None and parent > 1:
        env["PROBE_HOOK_PARENT_PID"] = str(parent)
    if hosted:
        env["PROBE_HOOK_HOSTED"] = "1"
    else:
        env["PROBE_HOOK_HOST"] = "off"
        env["PROBE_HOOKS_HANDED_OVER"] = request["root"]
    return env


def event_argv(request: dict) -> list:
    """The dispatcher's arguments: the lane, then a queued event's
    `--record-keeping` (`hooks/dispatch.py` RECORD_KEEPING: only its
    record-keeping routes run)."""
    return list(request.get("argv") or [request["lane"]])


def timed_out_answer() -> dict:
    """`hooks.run`'s answer for an event its deadline passed before: no verdict."""
    return _answer(None, None, timed_out=True, via=None)


def _answer(code: int | None, out: "_Output | None", *, timed_out: bool, via: str | None) -> dict:
    """The answer. Truncation is per stream (`stdout_truncated`,
    `stderr_truncated`; `truncated`: either): a stderr flood never costs an
    intact stdout its verdict."""
    stdout, stderr = out.text() if out is not None else ("", "")
    cut_out, cut_err = out.cut() if out is not None else (False, False)
    return {
        "exit_code": code,
        "stdout": stdout,
        "stderr": stderr,
        "timed_out": timed_out,
        "truncated": cut_out or cut_err,
        "stdout_truncated": cut_out,
        "stderr_truncated": cut_err,
        "via": via,
    }


class _Output:
    """The event's stdout and stderr, read as they come, MAX_HOOK_OUTPUT each."""

    def __init__(self, out_fd: int, err_fd: int) -> None:
        self.order = (out_fd, err_fd)
        self.data = {out_fd: bytearray(), err_fd: bytearray()}
        self.open = {out_fd, err_fd}
        self.truncated: set = set()
        for fd in self.order:
            os.set_blocking(fd, False)

    def read(self, ready) -> None:
        for fd in ready:
            if fd not in self.open:
                continue
            try:
                chunk = os.read(fd, 65536)
            except BlockingIOError:
                continue
            except OSError:
                chunk = b""
            if not chunk:
                self.open.discard(fd)
                continue
            kept = self.data[fd]
            room = max(MAX_HOOK_OUTPUT - len(kept), 0)
            kept += chunk[:room]
            if len(chunk) > room:
                self.truncated.add(fd)

    def cut(self) -> tuple[bool, bool]:
        """(stdout, stderr): which was cut at MAX_HOOK_OUTPUT."""
        return self.order[0] in self.truncated, self.order[1] in self.truncated

    def text(self) -> tuple[str, str]:
        out, err = (bytes(self.data[fd]).decode("utf-8", "replace") for fd in self.order)
        return out, err


def _drain(out: _Output, until: float) -> None:
    """Read what is left until both pipes end or `until` (monotonic). Called
    once the event has ended, with `until` DRAIN_S from then and never capped
    at the run's deadline: what it wrote before it ended is its answer, however
    late the end was seen."""
    while out.open:
        left = until - time.monotonic()
        if left <= 0:
            return
        ready, _, _ = select.select(list(out.open), [], [], left)
        if not ready:
            return
        out.read(ready)


def _via_host(request: dict, parent: int | None, deadline: float) -> dict | None:
    """The event on the folder's warm host, as `dispatch.py` `via_host` hands it
    one, with the service's own pipes for its stdout and stderr: the answer,
    or None when the host is not there or not ready in time (it then never runs
    the event: `G` goes only before `deadline`, `zygote.py`'s exactly-once).
    Once told to go the event is the host's, and runs to its end within its
    lane's budget like any hosted event: an end the service cannot see by
    `deadline` (out of time, the host lost) answers `exit_code: null`."""
    path = host_socket(request["root"])
    if not _private(str(path.parent)) or not path.exists():
        return None
    owned: list = []
    sock = None

    def left() -> float:
        return deadline - time.monotonic()

    try:
        if left() <= 0:
            return None
        try:
            out_r, out_w = os.pipe()
            owned += [out_r, out_w]
            err_r, err_w = os.pipe()
            owned += [err_r, err_w]
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(left())
            sock.connect(str(path))
            header = {
                "v": 1, "argv": event_argv(request), "cwd": request["cwd"],
                "env": event_env(request, parent, hosted=True),
                "parent": parent if parent is not None and parent > 1 else os.getpid(),
                # The event's own deadline, as `via_host` gives it: once started it
                # is the host's (and its dispatcher's budget stops its routes).
                "deadline": time.time() + LANE_BUDGET_S[request["lane"]] + HOST_MARGIN_S,
                "payload": len(request["payload"]),
            }
            key = _host_key(request["root"])
            if key is not None:
                header["key"] = key  # the host runs nothing without it (#3355)
            data = json.dumps(header).encode("utf-8") + b"\n" + request["payload"]
            # The fds ride the first send, which may take less than it was given.
            sent = socket.send_fds(sock, [data[:65536]], [out_w, err_w])
            if sent < len(data):
                sock.sendall(data[sent:])
        except OSError:
            return None
        # The host holds its own copies now: the pipes end when the event's do.
        for fd in (out_w, err_w):
            os.close(fd)
            owned.remove(fd)
        told = False
        try:
            sock.settimeout(max(left(), 0.001))
            if sock.recv(1) != b"R" or left() <= 0:
                return None
            sock.sendall(b"G")
            told = True
            sock.settimeout(max(left(), 0.001))
            started = sock.recv(1)
        except OSError:
            # Before `G`: never run. After it: maybe running there, so never here too.
            return _answer(None, None, timed_out=left() <= 0, via=Via.HOST) if told else None
        if started == b"N":
            return None
        if started != b"S":
            return _answer(None, None, timed_out=left() <= 0, via=Via.HOST)
        out = _Output(out_r, err_r)
        sock.setblocking(False)
        reply = b""
        code: int | None = None
        lost = False
        while True:
            now = time.monotonic()
            if code is not None or lost:
                _drain(out, now + DRAIN_S)
                break
            if now >= deadline:
                break
            readers = [sock, *out.open]
            ready, _, _ = select.select(readers, [], [], deadline - now)
            if sock in ready:
                try:
                    chunk = sock.recv(4096)
                except BlockingIOError:
                    chunk = None
                except OSError:
                    chunk = b""
                if chunk == b"":
                    lost = True
                elif chunk:
                    reply += chunk
                    if b"\n" in reply:
                        try:
                            got = json.loads(reply.split(b"\n", 1)[0].decode("utf-8")).get("exit")
                        except (ValueError, AttributeError):
                            got = None
                        code = got if isinstance(got, int) and 0 <= got < 256 else None
                        lost = code is None
            out.read([fd for fd in ready if fd is not sock])
        return _answer(code, out, timed_out=code is None and not lost, via=Via.HOST)
    finally:
        if sock is not None:
            sock.close()
        for fd in owned:
            with contextlib.suppress(OSError):
                os.close(fd)


def _stop_group(proc: subprocess.Popen) -> None:
    """An overrun dispatcher: its group asked to stop first (the dispatcher's
    handler stops every route it started, each in a group of its own), then,
    once it has gone or KILL_WAIT_S passed, the whole group killed, whatever
    in it ignored the first signal. The dispatcher (the group's leader, its pid
    the group's id) is reaped only after that kill: until then its pid cannot
    be reused, so the kill reaches only the group this service created."""
    with contextlib.suppress(OSError):
        os.killpg(proc.pid, signal.SIGTERM)
    end = time.monotonic() + KILL_WAIT_S
    waitid = getattr(os, "waitid", None)
    while time.monotonic() < end:
        try:
            # Exited, left unreaped (WNOWAIT): the group's id stays ours. Where
            # waitid is missing, the whole grace passes instead.
            if waitid is not None and waitid(os.P_PID, proc.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT) is not None:
                break
        except ChildProcessError:
            break
        time.sleep(POLL_S)
    with contextlib.suppress(OSError):
        os.killpg(proc.pid, signal.SIGKILL)
    with contextlib.suppress(subprocess.TimeoutExpired):
        proc.wait(KILL_WAIT_S)


def _via_process(request: dict, parent: int | None, deadline: float) -> dict:
    """The event as a fresh dispatcher, as the hooks.json entry runs it:
    `hooks/dispatch.sh <lane>` with the payload on its stdin, in its own process
    group, stopped with what stayed in that group past `deadline`."""
    script = Path(request["root"]) / "hooks" / "dispatch.sh"
    if not os.access(script, os.X_OK):
        # The entry's own `[ -x "$ROOT/hooks/dispatch.sh" ] || exit 0` would
        # answer "allowed" with nothing having run: say nothing ran instead.
        return _answer(None, None, timed_out=False, via=None)
    env = event_env(request, parent, hosted=False)
    cwd = request["cwd"]
    if not os.path.isdir(cwd):
        cwd = env["HOME"] if os.path.isdir(env.get("HOME") or "") else "/"
    try:
        proc = subprocess.Popen(  # noqa: S603 -- the plugin's own dispatcher, as its hooks.json entry runs it
            [str(script), *event_argv(request)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            env=env,
            start_new_session=True,
            close_fds=True,
        )
    except OSError:
        return _answer(None, None, timed_out=False, via=None)

    def feed() -> None:
        try:
            proc.stdin.write(request["payload"])
        except (OSError, ValueError):
            pass
        finally:
            with contextlib.suppress(OSError, ValueError):
                proc.stdin.close()

    code: int | None = None
    try:
        threading.Thread(target=feed, daemon=True).start()
        out = _Output(proc.stdout.fileno(), proc.stderr.fileno())
        while True:
            code = proc.poll()
            now = time.monotonic()
            if code is not None:
                # Exited: what it wrote is read even past the deadline (bounded).
                _drain(out, now + DRAIN_S)
                break
            if now >= deadline:
                break
            if out.open:
                ready, _, _ = select.select(list(out.open), [], [], min(POLL_S, deadline - now))
                out.read(ready)
            else:
                time.sleep(min(POLL_S, deadline - now))
        if code is None:
            _stop_group(proc)
            return _answer(None, out, timed_out=True, via=Via.PROCESS)
        # Killed by a signal: what its shell would report (128 + n), never a veto.
        return _answer(code if code >= 0 else 128 - code, out, timed_out=False, via=Via.PROCESS)
    except BaseException:
        if proc.returncode is None:
            _stop_group(proc)
        raise
    finally:
        for pipe in (proc.stdout, proc.stderr):
            with contextlib.suppress(OSError, ValueError):
                pipe.close()


def run_event(request: dict, parent: int | None) -> dict:
    """`hooks.run`: one event, checked by `protocol.need_hook_run`, its folder
    checked here (`runnable`: `{"refused": why}` for one that is not a
    complete Probe plugin folder), run for that folder within `timeout_s`.
    Blocking (a thread of the service's). `parent`: the caller's pid (the
    kernel's word).

    The answer: `exit_code` (the dispatcher's, as a harness reads it: 2 vetoes
    a PreToolUse or UserPromptSubmit; null when the service cannot say how the
    event ended), `stdout` (the routes' merged output, `dispatch.py` MERGE),
    `stderr`, `timed_out`, `truncated` (an output past MAX_HOOK_OUTPUT) and
    `via` (Via, or null: nothing started). The time counts from `deadline`
    (monotonic) when the request carries one: from when it was asked, not
    from when a thread took it."""
    deadline = request.get("deadline") or time.monotonic() + request["timeout_s"]
    if time.monotonic() >= deadline:
        return timed_out_answer()  # waited its turn past its caller's wait: nothing to do
    refused = runnable(request)
    if refused is not None:
        return refused
    if time.monotonic() >= deadline:
        return timed_out_answer()  # the folder's check took it all
    if request["lane"] not in UNHOSTED_LANES:
        hosted = _via_host(request, parent, deadline)
        if hosted is not None:
            return hosted
    if time.monotonic() >= deadline:
        return timed_out_answer()
    return _via_process(request, parent, deadline)
