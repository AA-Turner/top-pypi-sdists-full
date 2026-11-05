"""Who is calling a Probe service: the peer process the kernel names, how confined it is, and where a
stored key may go. Shared by the machine service (`service/actions/caller.py` serves these names) and
the delivery service. Stdlib only: the machine service's start path imports it (plan S1)."""

from __future__ import annotations

import json
import os
import socket
import stat
import struct
import sys
from pathlib import Path

#: `getsockopt(SOL_LOCAL, LOCAL_PEERPID)` on macOS (sys/un.h): Python names neither.
_SOL_LOCAL = 0
_LOCAL_PEERPID = 2
#: The hosted Probe API (`probe.sdk.settings.settings.DEFAULT_BASE_URL`), which every
#: install may reach whatever its config says.
DEFAULT_BASE_URL = "https://api.research.prbe.ai"
#: A CLI config larger than this is not read (it is never this big).
MAX_CONFIG_BYTES = 1024 * 1024


def get_peer_pid(sock: socket.socket) -> int | None:
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


def get_peer_uid(sock: socket.socket) -> int | None:
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


# -- how confined a caller is ------------------------------------------------------------


def get_confinement(pid: int) -> tuple | None:
    """What confines a process: (seccomp, its filter count, no_new_privs, mnt ns, user ns) on
    Linux, (sandboxed,) on macOS; None when it cannot be read. The hook host's copy is
    `hooks/zygote.py::_confinement` (and `_sandboxed` there follows `is_sandboxed` here)."""
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


def is_sandboxed(pid: int | None) -> bool:
    """Is the caller more confined than this service (an agent's sandboxed tool
    command)? What it asks for would then run outside its sandbox, with the
    environment and PATH it chose. Unknown counts as yes, and so does what
    cannot be ruled out (`is_landlock_possible`)."""
    if pid is None:
        return True
    own, theirs = get_confinement(os.getpid()), get_confinement(pid)
    return own is None or theirs is None or theirs != own or is_landlock_possible(theirs)


def is_landlock_possible(found: tuple) -> bool:
    """Linux: could the process `found` describes (`get_confinement`) be in a Landlock domain?
    Landlock shows in none of those fields, and a process with no_new_privs set may add one
    whenever it likes (`landlock_restrict_self` needs no_new_privs, or CAP_SYS_ADMIN). So a
    caller with no_new_privs (here: this service has it too, or the two tuples would differ)
    cannot be told from a sandboxed one, and counts as one. Elsewhere, no.

    OUTSIDE THE SUPPORTED MODEL: a caller with CAP_SYS_ADMIN (an agent run as root) may add a
    Landlock domain WITHOUT no_new_privs, and this cannot see it: running the coding agent, or
    a tool sandbox inside it, as root with CAP_SYS_ADMIN is not a setup the service keeps a
    sandbox for. (A root that unshares its user namespace first is in another one, and refused
    by the tuple above.)"""
    return sys.platform.startswith("linux") and len(found) >= 3 and found[2] == "1"


def is_other_network(pid: int | None) -> bool:
    """Linux: is `pid` in another network namespace than this service (an agent's sandbox with
    no network, `unshare -n`)? `is_sandboxed` reads the mount and user namespaces, not this one.
    Unknown counts as yes, as there; elsewhere, no."""
    if not sys.platform.startswith("linux"):
        return False
    if pid is None:
        return True
    try:
        theirs, own = os.stat(f"/proc/{pid}/ns/net"), os.stat("/proc/self/ns/net")
    except OSError:
        return True
    return (theirs.st_dev, theirs.st_ino) != (own.st_dev, own.st_ino)


def is_confined(pid: int | None) -> bool:
    """A caller this service cannot rule out being more confined than itself: `is_sandboxed`
    (Landlock included), or another network namespace."""
    return is_sandboxed(pid) or is_other_network(pid)


def is_confined_unlike_this_service(pid: int | None) -> bool:
    """The public delivery service's test (D31): a caller confined otherwise than this service, or in
    another network namespace. Never the Landlock doubt: a delivery service is started by the SDK it
    serves, in that process's container or sandbox (a child inherits a Landlock domain), so a caller
    confined just as it is has nothing to escape here. Unknown counts as yes."""
    if pid is None:
        return True
    own, theirs = get_confinement(os.getpid()), get_confinement(pid)
    return own is None or theirs is None or theirs != own or is_other_network(pid)


# -- D10, D26: where a stored key may go ---------------------------------------------------


def get_config_path(env: dict) -> Path:
    """The CLI config a child would read (`probe.sdk.settings.settings.config_path`), with the
    child's exact environment (this process's, `env` over it), so an empty value means what it
    means there."""
    child = {**os.environ, **env}
    override = child.get("PROBE_CONFIG_PATH")
    if override:
        return Path(override)
    base = child.get("XDG_CONFIG_HOME")
    root = Path(base) if base else Path(child.get("HOME") or Path.home()) / ".config"
    return root / "probe" / "config.json"


def read_config(path: Path) -> str:
    """The config's text: a regular file of at most MAX_CONFIG_BYTES, read without blocking. A
    request names this path (`context.PROBE_CONFIG_PATH`), so a FIFO or `/dev/zero` must not hang
    or fill the service. OSError else."""
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


def normalize_url(url: str) -> str:
    """Endpoints compare in one normal form (`settings.normalize_endpoint`). Imported here: off the
    service's start path (plan S1), loaded with the first request that names an endpoint."""
    from probe.sdk.settings.settings import normalize_endpoint

    return normalize_endpoint(url)


def get_known_endpoints(env: dict) -> set:
    """The endpoints the stored token may go to: the CURRENT context's base URL in the CLI
    config the child reads (a v1 flat file's own), else the hosted API. Only that context's
    token follows `PROBE_BASE_URL` (`probe.sdk.settings.settings.resolve` -> `load_context`), so
    another context's address would receive a token signed in somewhere else."""
    hosted = {normalize_url(DEFAULT_BASE_URL)}
    try:
        data = json.loads(read_config(get_config_path(env)))
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
        return {normalize_url(url)}
    return hosted


def is_known_endpoint(url: str, env: dict) -> bool:
    """May a child run with this base URL? Only https, and only the endpoint the CLI config the
    child reads is signed in to now (its current context's, or the hosted API when that names
    none): the config's stored token follows `PROBE_BASE_URL`, so any other address would get it.
    This gate is the control; the CLI's stored-address rule for its checks
    (`probe.cli.wizard.state.device_state.get_sendable_token`) only backs it up."""
    return url.startswith("https://") and normalize_url(url) in get_known_endpoints(env)


#: Its old name (`background.other_network`), one release.
other_network = is_other_network
