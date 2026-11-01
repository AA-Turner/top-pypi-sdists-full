"""one run's spool in this process: its folder, owner and liveness markers, and the per-run writer (_RunReads)."""

from __future__ import annotations

import contextlib
import json
import os
import socket
import threading
import urllib.parse
from datetime import datetime
from probe.foundation.compat.compat import UTC
from pathlib import Path
from typing import Any
from .....foundation.durable import homedir
from ....recording_rules import ignore as _ignore
#: The most one of those looks may take; the next continues where it stopped.
WRITE_CHECK_SWEEP_S = 1.0
#: Where a recording process keeps what it last saw of each file it wrote:
#: ``<host>.<pid>.wf.json`` beside its spool (`_RunReads.check_writes`).
WF_SUFFIX = ".wf.json"

MAX_PATHS = 10_000
_local = threading.local()


def state_dir() -> Path:
    """``<state>/probe/reads``; under a private ``$TMPDIR`` folder when the
    state folder cannot be written (``HOME=/``, `homedir.state_base`)."""
    return homedir.state_base() / "probe" / "reads"


#: What a run id cannot carry into its folder's name (`run_folder`): a path
#: separator, or PYTHONPATH's (``os.pathsep``) -- an offline run's
#: ``local:<key>`` split its spawned workers' hook folder in two on
#: PYTHONPATH, and no worker ever loaded the hook. ``%`` is the escape itself.
_NOT_IN_FOLDER = frozenset("%:;/\\" + os.sep + (os.altsep or "") + os.pathsep)


def run_folder(run_id: str) -> str:
    """``run_id``'s folder name under `state_dir`: the id, with ``%``, ``:``,
    ``;``, ``/`` and ``\\`` escaped as ``%XX``. A server id (a uuid) is its own
    name; ``local:<key>`` is ``local%3A<key>``. Stable and reversible
    (`_folder_run`): the owner, its workers' hook, a recovery and ``probe
    sync`` all find the same folder, and a spool header still names the run
    by its id."""
    return "".join(f"%{ord(char):02X}" if char in _NOT_IN_FOLDER else char for char in run_id)


def _folder_run(name: str) -> str:
    """The run id whose `run_folder` is ``name``."""
    return urllib.parse.unquote(name) if "%" in name else name


def run_dir(run_id: str) -> Path:
    return state_dir() / run_folder(run_id)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _host() -> str:
    """This machine, as spool names carry it: a shared home directory (NFS on a
    cluster) holds every node's spools, and only this node's are this node's."""
    name = socket.gethostname() or "host"
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


def _spool_owner(spool: Path) -> tuple[str, int] | None:
    host, _, pid = spool.stem.rpartition(".")
    try:
        return host, int(pid)
    except ValueError:
        return None


@contextlib.contextmanager
def internal():
    """Mark the current thread's file opens as Probe's own work."""
    depth = getattr(_local, "internal", 0)
    _local.internal = depth + 1
    try:
        yield
    finally:
        _local.internal = depth


def _ident(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def _stat_is_file(st: os.stat_result) -> bool:
    import stat as _stat

    return _stat.S_ISREG(st.st_mode)


def _before(path: str) -> list | None:
    """A file's identity as a spool list, or None when it is not there (or not
    a regular file): what a write note records as the file BEFORE the open."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    return list(_ident(st)) if _stat_is_file(st) else None


def _write_owner(
    run_id: str,
    *,
    base_url: str | None = None,
    token_id: str | None = None,
    ignore: Any = None,
    offline_dir: str | os.PathLike | None = None,
    writes: bool = False,
) -> None:
    """``owner.json``: whose spools these are, and the run's ``.probeignore``
    rules (plan (n)), so reads a recovery sends -- the spools of a launcher or
    process that never collected them, a Ctrl-C'd ``probe exec`` among them --
    are filtered exactly as the run's own close would have filtered them.
    ``writes``: whether writes are noted too; a process collecting spools it
    did not record (a launcher, a recovery) sends a write list only then, so
    an empty list never claims "wrote nothing" for a run that opted out."""
    directory = run_dir(run_id)
    record = _ignore.to_record(ignore)
    with internal():
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "owner.json").write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "pid": os.getpid(),
                    "base_url": base_url,
                    "token_id": token_id,
                    "host": _host(),
                    "started_at": _now_iso(),
                    **({"ignore": record} if record else {}),
                    **({"offline_dir": os.fspath(offline_dir)} if offline_dir else {}),
                    "writes": bool(writes),
                }
            )
        )


def _pid_alive(pid: int) -> bool:
    from ....._shared import oscompat

    try:
        oscompat.probe_pid(pid)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _mark_live(run_id: str) -> None:
    """Say this process may still write to ``run_id``'s folder. Spools appear
    lazily, at the first read: without a marker, another rank closing first
    (or recovery) would see an empty folder and delete it under this one."""
    directory = run_dir(run_id)
    with internal():
        directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{_host()}.{os.getpid()}.live").touch()


def _live_here(directory: Path) -> bool:
    """A live process on this host, other than this one, marked the folder."""
    host, me = _host(), os.getpid()
    for marker in directory.glob("*.live"):
        owner = _spool_owner(marker)
        if owner is not None and owner[0] == host and owner[1] != me and _pid_alive(owner[1]):
            return True
    return False


def _live_elsewhere(directory: Path) -> bool:
    """`_live_here`, or a marker from another host, whose pids mean nothing here."""
    host = _host()
    for marker in directory.glob("*.live"):
        owner = _spool_owner(marker)
        if owner is not None and owner[0] != host:
            return True
    return _live_here(directory)


def _drop_markers(directory: Path) -> None:
    """Remove this process's marker and those of this host's ended processes."""
    host, me = _host(), os.getpid()
    for marker in directory.glob("*.live"):
        owner = _spool_owner(marker)
        if owner is not None and owner[0] == host and (owner[1] == me or not _pid_alive(owner[1])):
            with contextlib.suppress(OSError):
                marker.unlink()
