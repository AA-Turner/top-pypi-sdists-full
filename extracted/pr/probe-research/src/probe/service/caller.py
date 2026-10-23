"""Who is calling: the peer process behind a connection, and the sessions around it (plan D9, D10).

The service changes the device on a request's behalf (`action.run`), so it may
not take the request's word for who sent it. A coding agent's session the
Probe daemon records may not switch who records, sign out or uninstall
(`probe.core.actions._refuse_from_daemon_session`); before this, a caller that
simply left its session's id out of `context` was not refused. So:

    peer pid     Linux SO_PEERCRED, macOS LOCAL_PEERPID: the kernel's word
    ancestry     the pid and its parents (`procid`), matched against the
                 registry's session owners (pid AND start time)
    environment  Linux only: the peer's own session-id variables
                 (/proc/<pid>/environ, same user), which its children inherit,
                 so a job detached from the agent (nohup, setsid, tmux) that
                 kept its environment is still found

Either finding names the session, and the request runs as one from inside it:
the session's id variable joins the child's environment (so `probe.core.run`
refuses what it refuses there), and an action from a daemon-recorded session
is refused here before it is journaled. A same-user process that both detaches
and clears its environment still gets through; nothing stops a same-user
process completely (the review's accepted residue).

`known_endpoint` is D10: the stored token goes only where it was meant to.

Stdlib only (the start path; plan S1). Linux and macOS; elsewhere every
lookup answers "unknown" and the request's own `context` is all there is.
"""

from __future__ import annotations

import json
import os
import socket
import struct
import sys
from pathlib import Path

from . import procid

#: `getsockopt(SOL_LOCAL, LOCAL_PEERPID)` on macOS (sys/un.h): Python names neither.
_SOL_LOCAL = 0
_LOCAL_PEERPID = 2
#: A parent walk stops here (a loop in a broken /proc, or pid 1).
MAX_ANCESTRY = 64
#: The hosted Probe API (`probe.sdk.config.DEFAULT_BASE_URL`), which every
#: install may reach whatever its config says.
DEFAULT_BASE_URL = "https://api.research.prbe.ai"
#: A CLI config larger than this is not read (it is never this big).
MAX_CONFIG_BYTES = 1024 * 1024


def peer_pid(sock: socket.socket) -> int | None:
    """The connecting process's pid, where the kernel says; else None."""
    try:
        if hasattr(socket, "SO_PEERCRED"):
            raw = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
            pid = struct.unpack("3i", raw)[0]
            return pid if pid > 0 else None
        if sys.platform == "darwin":
            raw = sock.getsockopt(_SOL_LOCAL, _LOCAL_PEERPID, struct.calcsize("i"))
            pid = struct.unpack("i", raw)[0]
            return pid if pid > 0 else None
    except (OSError, struct.error):
        return None
    return None


def confinement(pid: int) -> tuple | None:
    """What confines a process: (seccomp, its filter count, no_new_privs, mnt ns, user ns) on
    Linux, (sandboxed,) on macOS; None when it cannot be read. The hook
    host's copy is `hooks/zygote.py::_confinement`."""
    try:
        if sys.platform.startswith("linux"):
            fields = {}
            with open(f"/proc/{pid}/status", encoding="utf-8") as handle:
                for line in handle:
                    key, _, value = line.partition(":")
                    fields[key] = value.strip()
            # The filter count too: a sandbox inside a container that already
            # runs everything under seccomp and no-new-privs adds filters of its own.
            return (fields.get("Seccomp"), fields.get("Seccomp_filters"), fields.get("NoNewPrivs"),
                    os.readlink(f"/proc/{pid}/ns/mnt"), os.readlink(f"/proc/{pid}/ns/user"))
        if sys.platform == "darwin":
            import ctypes

            lib = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
            lib.sandbox_check.restype = ctypes.c_int
            lib.sandbox_check.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
            return (lib.sandbox_check(int(pid), None, 0) != 0,)
    except Exception:  # noqa: BLE001 -- unknown: treated as confined
        return None
    return None


def sandboxed(pid: int | None) -> bool:
    """Is the caller more confined than this service (an agent's sandboxed tool
    command)? What it asks for would then run outside its sandbox, with the
    environment and PATH it chose. Unknown counts as yes."""
    if pid is None:
        return True
    own, theirs = confinement(os.getpid()), confinement(pid)
    return own is None or theirs is None or theirs != own


def ancestry(pid: int) -> list[tuple[int, str]]:
    """`[(pid, start time), (its parent, ...), ...]` up to init, or as far as
    the platform can read. Empty when `pid` cannot be read at all."""
    chain: list[tuple[int, str]] = []
    seen: set[int] = set()
    while pid > 1 and pid not in seen and len(chain) < MAX_ANCESTRY:
        seen.add(pid)
        info = procid.proc(pid)
        if info is None:
            break
        chain.append((pid, info.start))
        pid = info.ppid
    return chain


def environ(pid: int, names: frozenset) -> dict:
    """The values of `names` in `pid`'s environment (Linux, same user), else {}."""
    try:
        raw = Path(f"/proc/{pid}/environ").read_bytes()
    except OSError:
        return {}
    found: dict = {}
    for entry in raw.split(b"\0"):
        name, sep, value = entry.partition(b"=")
        if not sep:
            continue
        key = name.decode("utf-8", "replace")
        if key in names and value:
            found[key] = value.decode("utf-8", "replace")
    return found


# -- D10: where the stored token may go -----------------------------------------


def _config_path(env: dict) -> Path:
    """The CLI config the child would read (`probe.sdk.config.config_path`),
    with the child's exact environment (`children.child_env`: the service's,
    the request's context over it), so an empty value means what it means there."""
    child = {**os.environ, **env}
    override = child.get("PROBE_CONFIG_PATH")
    if override:
        return Path(override)
    base = child.get("XDG_CONFIG_HOME")
    root = Path(base) if base else Path(child.get("HOME") or Path.home()) / ".config"
    return root / "probe" / "config.json"


def _read_config(path: Path) -> str:
    """The config's text: a regular file of at most MAX_CONFIG_BYTES, read
    without blocking. A request names this path (`context.PROBE_CONFIG_PATH`),
    so a FIFO or `/dev/zero` must not hang or fill the service. OSError else."""
    import stat

    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0))
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_CONFIG_BYTES:
            raise OSError(f"{path} is not a config file")
        data = os.read(fd, MAX_CONFIG_BYTES + 1)
    finally:
        os.close(fd)
    if len(data) > MAX_CONFIG_BYTES:
        raise OSError(f"{path} is too large")
    return data.decode("utf-8")


def _normal(url: str) -> str:
    return url.strip().rstrip("/")


def known_endpoints(env: dict) -> set:
    """The endpoints the stored token may go to: the CURRENT context's base URL
    in the CLI config the child reads (a v1 flat file's own), else the hosted
    API. Only that context's token follows `PROBE_BASE_URL`
    (`probe.sdk.config.resolve` -> `load_context`), so another context's
    address would receive a token signed in somewhere else."""
    hosted = {_normal(DEFAULT_BASE_URL)}
    try:
        data = json.loads(_read_config(_config_path(env)))
    except (OSError, ValueError):
        return hosted
    if not isinstance(data, dict):
        return hosted
    contexts = data.get("contexts")
    if isinstance(contexts, dict):
        row = contexts.get(data.get("current_context") or "default")
    else:
        row = data  # v1: one flat context
    url = row.get("base_url") if isinstance(row, dict) else None
    if isinstance(url, str) and url.strip():
        return {_normal(url)}
    return hosted


def known_endpoint(url: str, env: dict) -> bool:
    """May a child run with this base URL? Only https, and only the endpoint
    the CLI config the child reads is signed in to now (its current context's,
    or the hosted API when that names none): the config's stored token follows
    `PROBE_BASE_URL` (`probe.sdk.config.resolve`), so any other address would
    receive it."""
    return url.startswith("https://") and _normal(url) in known_endpoints(env)
