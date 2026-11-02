"""the barrier file that lets a half-done uninstall be resumed by its owner, and finishing one an earlier process left."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import sys
import time

from probe.foundation.compat.compat import StrEnum
BARRIER_VERSION = 1


# -- the barrier (the WRITER; `probe.shared.updates.uninstall_barrier` is the one reader) ----------


def _write_barrier(run: Run, phase: str) -> None:
    """The barrier at `phase`, owned by this process: written ATOMICALLY every
    time (a temp file in the same folder, fsynced, renamed over it, the folder
    fsynced), 0600 in a 0700 folder. A reader never sees half a record (the
    frozen lifeboat v3 reads an unreadable one as LIVE). A resumed run writes
    RESUMING before "server": LIVE whoever wrote it."""
    from probe.foundation.service_api import paths, procid

    target = paths.uninstall_barrier_path()
    paths.private_dir(target.parent)
    record = {
        "v": BARRIER_VERSION,
        "pid": os.getpid(),
        "start": procid.start_time(os.getpid()) or "",
        "at": time.time(),
        "plan": str(paths.uninstall_plan_path()),
        "phase": str(phase),
        # A shared home: another machine's reader sees an owner it cannot
        # check, and counts it as running (`uninstall_barrier._other_machine`).
        "host": _hostname(),
        "machine_key": str(run.plan.get("machine_key") or paths.machine_key()),
    }
    tmp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with open(fd, "w", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, target)
        run.wrote_barrier = True
        if os.name == "posix":
            with contextlib.suppress(OSError):
                folder = os.open(target.parent, os.O_RDONLY)
                try:
                    os.fsync(folder)
                finally:
                    os.close(folder)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def _hostname() -> str:
    import socket

    try:
        return socket.gethostname()
    except OSError:
        return ""


def _is_self(record: dict) -> bool:
    """Did THIS process write `record` (this machine, this pid)?"""
    from probe.shared.updates import uninstall_barrier as reader

    return record.get("pid") == os.getpid() and not reader._other_machine(record)  # noqa: SLF001


def _owner_runs(record: dict) -> bool:
    """Does the process that wrote this barrier still run (pid and start)? One
    on another machine sharing this home does, as far as this one can tell."""
    from probe.shared.updates import uninstall_barrier as reader
    from probe.foundation.service_api import procid

    if reader._other_machine(record):  # noqa: SLF001 -- the reader's one rule for a shared home
        return True
    pid, start = record.get("pid"), record.get("start")
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 1 or not isinstance(start, str) or not start:
        return False
    return procid.alive(pid, start) is not False


def _owns_barrier(run: Run, record: object) -> bool:
    """Is `record` (the barrier on disk) the one THIS run wrote: its flag set,
    and the record's pid and start this process's? Anything else (another
    run's barrier, an unreadable one) is never called off from here."""
    from probe.foundation.service_api import procid

    if not run.wrote_barrier or not isinstance(record, dict):
        return False
    pid = os.getpid()
    return record.get("pid") == pid and record.get("start") == (procid.start_time(pid) or "")


def _drop_barrier() -> None:
    """Cancel before the point of no return: the uninstall's folder goes, so
    Probe starts again as it was (the keeper and lifeboat come back with the
    service's next start). Only for what this run wrote (`_owns_barrier`)."""
    from probe.foundation.service_api import paths

    shutil.rmtree(paths.uninstall_dir(), ignore_errors=True)


def halfway_notice() -> str | None:
    """The line `probe doctor` and `probe status` print FIRST while an
    uninstall that stopped halfway keeps Probe off (its barrier LIVE, its owner
    gone): nothing of Probe starts or updates until it is finished. None
    otherwise (no barrier, or an uninstall running right now). Never raises."""
    try:
        from probe.shared.updates import uninstall_barrier as reader

        record = reader.read()
        if reader.state(record) != reader.State.LIVE or reader._owner_runs(record or {}):  # noqa: SLF001
            return None
        phase = (record or {}).get("phase")
    except Exception:  # noqa: BLE001 - a status line never breaks the command
        return None
    if phase in PHASES:
        return (f"An uninstall of Probe stopped halfway (phase {phase}). Run `probe repair` (or `npx "
                "probe-research`) to finish it and set Probe up again, or `probe uninstall` to finish removing it.")
    # How far it got is unknown: only `probe uninstall` itself runs it (`finish_interrupted`).
    return (f"An uninstall of Probe stopped halfway (phase {phase or 'unknown'}). Run `probe uninstall` to finish "
            "removing it; `npx probe-research` then sets Probe up again.")


class Interrupted(StrEnum):
    """What `finish_interrupted` found."""

    NONE = "none"  # no uninstall to finish (none, or a stale one: the installer clears it)
    RUNNING = "running"  # an uninstall runs right now: the installer refuses
    FINISHED = "finished"  # one had stopped halfway; it is finished now: install afresh
    FAILED = "failed"  # one had stopped halfway and could not be finished: refuse


def finish_interrupted() -> tuple[Interrupted, str]:
    """For every install entry, before it takes the install lock: an uninstall
    that stopped halfway (its barrier LIVE, its owner gone, past "draining" or
    unreadable) is finished first, as `probe uninstall` resumes it, and only
    then does the install go on: the owner chose a clean slate, and a person
    reinstalling wants Probe back. One line says so. An uninstall running right
    now (its owner alive) is never touched: RUNNING, with the reader's refusal.
    Returns (what, the line to print when the installer refuses)."""
    from probe.shared.updates import uninstall_barrier as reader

    record = reader.read()
    if reader.state(record) != reader.State.LIVE:
        return Interrupted.NONE, ""
    record = record or {}
    if reader._owner_runs(record):  # noqa: SLF001 -- the one reader's own judgement of its owner
        return Interrupted.RUNNING, reader.refusal(record) or "an uninstall of Probe is running"
    phase = record.get("phase")
    if record.get("_unreadable") or phase not in PHASES:
        # How far it got is unknown (an unreadable record, "resuming", a
        # phase this release does not know): only `probe uninstall` itself,
        # which asks about what is unsent, may run it from the start.
        what = "its record cannot be read" if record.get("_unreadable") else f"phase {phase or 'unknown'}"
        return Interrupted.RUNNING, (f"an uninstall of Probe stopped halfway ({what}); finish it with "
                                     "`probe uninstall`, then install again")
    print(f"An uninstall stopped halfway (phase {phase}); finishing it first", file=sys.stderr, flush=True)
    telemetry = os.environ.get("PROBE_TELEMETRY")
    try:
        code = run(Options(yes=True, embedded=True))
    finally:
        # The state phase turns this process's telemetry off; the install goes on.
        if telemetry is None:
            os.environ.pop("PROBE_TELEMETRY", None)
        else:
            os.environ["PROBE_TELEMETRY"] = telemetry
    if code == EXIT_DONE and reader.state() != reader.State.LIVE:
        return Interrupted.FINISHED, ""
    return Interrupted.FAILED, (
        "the uninstall that stopped halfway could not be finished; run `probe uninstall` (or `probe uninstall "
        "--offline` without a network) to finish it, then install again")
from probe.cli.install.uninstall.state import Options, PHASES, Run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import EXIT_DONE, run  # noqa: E402 -- pieces need each other; the front door loads this one first
