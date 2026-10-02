"""Which runs have a live process on this machine, and which process it is.

THE PROBLEM THIS SOLVES. Nothing inside a job can say why the job died. The
hardware rail looks like it could -- it samples the GPU while the job runs --
but `hw/monitor.py` runs it as a daemon THREAD inside the training process, so
it stops existing at the same instant as the thing it would be reporting on. A
process does not get to write its own postmortem.

So the explaining has to be done by something else on the same box, and that
something needs one fact the operating system will not give it: a dead process
id means nothing on its own. `pid 81422 is gone` is not a sentence about
anybody's research. This module is how a run says, before it dies, "that pid is
me, and here is where to report it".

An entry is written when a process starts BEATING AS OWNER, which is the exact
moment the SDK declares that this process's lifetime IS the run's lifetime, and
removed when the run closes cleanly. What is left behind is therefore the set
of runs whose process should still be alive -- and any entry whose process is
gone is a death nobody reported.

PID REUSE IS REAL AND IS HANDLED. Process ids wrap; on a busy box a new
process can take the id of one that died minutes ago, and an agent that trusted
the number alone would eventually report a live stranger as the researcher's
dead job. Every entry therefore records the process's own creation time, which
`psutil` reads from the kernel, and an entry matches only when BOTH agree.

THE COMPARISON IS EXACT, not approximate, and that is a correction: it was
first written with a one-second tolerance, on the theory that a clock might be
read slightly differently at registration and at check time. It is not -- both
readings come from the same `psutil` call against the same kernel field, and
the value round-trips through JSON without loss. Meanwhile an end-to-end test
measured two processes spawned back to back at 0.0015 seconds apart, so a
one-second window declared them the same process. The guard existed and did
nothing. `_SAME_PROCESS_EPSILON` is now only what float formatting can cost.

PER MACHINE, NOT PER RANK. `journal.default_dir()` appends a rank suffix so
sixty-four workers do not share one outbox. The opposite is wanted here: one
watcher per box has to see every rank's entry, so this directory is
deliberately unsuffixed.

Every function swallows. A registry that cannot be written costs the box agent
its knowledge of one run; a registry that raises would cost a researcher their
training job, and that trade is never worth making.
"""

from __future__ import annotations

import json
import os
import socket
import time
from pathlib import Path
from typing import Any

from probe.sdk.durable import write_text_atomic

#: Bumped when the entry shape changes in a way a reader must notice. A watcher
#: that meets a newer schema leaves the entry alone rather than guessing.
SCHEMA = 1

#: How far two readings of one process's creation time may differ and still be
#: the same process. Both readings come from the same kernel field via the same
#: library, so this covers float representation and nothing else. It is NOT a
#: tolerance for clock skew -- see the module note on why a generous window
#: silently disabled the pid-reuse guard.
#:
#: WHAT THE PLATFORM CAN RESOLVE, since it bounds what this check can ever
#: distinguish: Linux reports start time from `/proc/[pid]/stat` in clock
#: ticks, 100 Hz on every box we run, so two processes starting inside the
#: same 10ms tick are indistinguishable there. macOS reports microseconds.
#: That coarseness costs nothing real -- reaching a reused pid means cycling
#: the kernel's entire pid space first, thousands of process creations and
#: orders of magnitude longer than one tick -- but it does mean this check
#: answers "a different process" rather than "a different instant".
_SAME_PROCESS_EPSILON = 0.001


def default_dir() -> Path:
    """Where entries live. Mirrors the journal's root, without the rank
    suffix: a node agent watches the whole box, not one worker."""
    configured = os.environ.get("PROBE_BOX_DIR")
    if configured:
        return Path(configured).expanduser()
    base = os.environ.get("XDG_STATE_HOME")
    root = Path(base) if base else Path.home() / ".local" / "state"
    return root / "probe" / "box" / "runs"


def pid_namespace() -> str | None:
    """This process's PID namespace (`pid:[4026531836]` on Linux), or None
    where the platform has none to name. Two processes can only judge each
    other's pids inside the same one: a container sharing HOME with its host
    sees a different pid space under the same directory."""
    try:
        return os.readlink("/proc/self/ns/pid")
    except OSError:
        return None


def is_local(entry: dict[str, Any]) -> bool:
    """Whether ``entry`` was registered on THIS host, in THIS PID namespace --
    the only entries whose pids mean anything here. HOME, and with it this
    directory, is shared by every node of an HPC cluster and by containers
    that mount it; judging another machine's pid here reads a live run as
    dead (review of #2049). An entry that names no namespace (an older SDK)
    is judged by its host alone."""
    if entry.get("host") != socket.gethostname():
        return False
    recorded = entry.get("pidns")
    return recorded is None or recorded == pid_namespace()


def _create_time(pid: int) -> float | None:
    """The process's own start time, as the kernel reports it. None when it
    cannot be read, which makes the entry fall back to pid alone."""
    try:
        import psutil

        return float(psutil.Process(pid).create_time())
    except Exception:  # noqa: BLE001 -- an unreadable clock is not an error here
        return None


def _path(directory: Path, run_id: str) -> Path:
    # The run id is a server-minted UUID, but it arrives here from a caller, and
    # it is about to become a filename. Anything that is not a plain id is
    # refused rather than allowed to place a file outside the directory.
    safe = "".join(c for c in str(run_id) if c.isalnum() or c in "-_")
    return directory / f"{safe}.json"


def register(
    run_id: str,
    *,
    pid: int | None = None,
    context: str | None = None,
    base_url: str | None = None,
    directory: Path | str | None = None,
    writer: dict | None = None,
) -> Path | None:
    """Declare that this process owns `run_id`. Returns the entry path, or None
    if anything at all went wrong. ``writer`` (SDK reliability 2.2) is the
    session, epoch and sole-writer belief the watcher needs to report this
    process's death to the server, not only as a span."""
    try:
        d = Path(directory) if directory is not None else default_dir()
        d.mkdir(parents=True, exist_ok=True)
        this_pid = os.getpid() if pid is None else int(pid)
        entry = {
            "schema": SCHEMA,
            "run_id": str(run_id),
            "pid": this_pid,
            # Together with the pid, this is the identity. See the module note.
            "create_time": _create_time(this_pid),
            "registered_at": time.time(),
            "host": socket.gethostname(),
            # With the host, where the pid means anything (see `is_local`).
            "pidns": pid_namespace(),
            # WHERE to report what happens to this run. The agent is a separate
            # process with no memory of how this one was configured.
            "context": context,
            "base_url": base_url,
            "writer": dict(writer) if writer else None,
        }
        path = _path(d, run_id)
        write_text_atomic(path, json.dumps(entry, indent=2) + "\n", mode=0o600)
        return path
    except Exception:  # noqa: BLE001 -- never let bookkeeping touch the run
        return None


def deregister(run_id: str, *, directory: Path | str | None = None) -> bool:
    """The run closed itself, so its absence needs no explaining."""
    try:
        d = Path(directory) if directory is not None else default_dir()
        _path(d, run_id).unlink(missing_ok=True)
        return True
    except Exception:  # noqa: BLE001
        return False


def entries(directory: Path | str | None = None) -> list[dict[str, Any]]:
    """Every readable entry. A corrupt or future-schema file is skipped, not
    raised on: one bad entry must not blind the watcher to the others."""
    d = Path(directory) if directory is not None else default_dir()
    out: list[dict[str, Any]] = []
    try:
        candidates = sorted(d.glob("*.json"))
    except Exception:  # noqa: BLE001 -- no directory yet is not an error
        return out
    for path in candidates:
        try:
            entry = json.loads(path.read_text())
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(entry, dict) or entry.get("schema", 0) > SCHEMA:
            continue
        if not entry.get("run_id") or not isinstance(entry.get("pid"), int):
            continue
        entry["_path"] = str(path)
        out.append(entry)
    return out


def process_is_alive(entry: dict[str, Any]) -> bool:
    """Whether the process this entry names is STILL THAT PROCESS.

    Both halves matter. `pid_exists` alone says a process holds that number;
    the creation time says it is the same one that registered. Without the
    second check a recycled id reads as a healthy run forever, which is the
    quiet failure: the watcher would never report the death it exists to find.

    Returns True when it cannot tell. An unreadable process is not evidence of
    a death, and inventing one would put a crash email in front of somebody
    whose job is running fine.
    """
    try:
        import psutil
    except Exception:  # noqa: BLE001 -- no psutil, no opinion
        return True
    pid = entry.get("pid")
    if not isinstance(pid, int):
        return True
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return False
    except Exception:  # noqa: BLE001 -- permissions, a racing exit, a weird box
        return True
    recorded = entry.get("create_time")
    if recorded is None:
        return True
    try:
        return abs(float(proc.create_time()) - float(recorded)) <= _SAME_PROCESS_EPSILON
    except Exception:  # noqa: BLE001
        return True
