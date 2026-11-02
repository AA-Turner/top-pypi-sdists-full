"""find the daemon workers running here (lock holders, the daemon host) and ask them to hand over before an update."""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import signal
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from ....foundation.service_api import paths
from probe.service.updater.settings import (
    HANDOVER_TOUCH_S,
    WORKER_POLL_S,
    WORKER_STOP_ENV,
    WORKER_STOP_S,
    _env_seconds,
    log,
)


def _flock_held(path: Path) -> bool:
    """Is this lock file held by anyone? Absent: no. Unknown: yes (fail closed).

    A shared, non-blocking probe released at once (as `wizard_lock.running`):
    it conflicts only with a holder's exclusive lock, and creates nothing."""
    try:
        handle = open(path, "rb")  # noqa: SIM115 -- closed below
    except FileNotFoundError:
        return False
    except OSError:
        return True
    try:
        if not paths.try_lock(handle.fileno(), shared=True):
            return True
        paths.unlock(handle.fileno())
        return False
    finally:
        handle.close()


@dataclass(frozen=True)
class Worker:
    """A daemon worker holding its session's lock (`<state>/daemon/<sid>.lock`)."""

    sid: str
    lock: Path
    #: From its `.worker.json` marker (`probe.shared.mailbox.worker_marker.mark_worker_accepts`),
    #: checked to be that worker's process; None when it cannot be told.
    pid: int | None
    #: Its session is not a live one: the worker is finishing the queue of a
    #: session that ended, and a hand-over would leave that tail unrecorded
    #: (no successor ever starts). It is waited for, never asked to stop.
    draining: bool = False

    @property
    def handover(self) -> Path:
        """`probe.shared.mailbox.presence.handover_path`: the worker hands over at its
        next model round while this is fresh."""
        return self.lock.with_suffix(".handover")


#: `daemonhost.ARGV_MARK`: the daemon host's command line carries it.
DAEMON_HOST_MARK = "daemon-host"


def _argv_words(pid: int) -> list[str] | None:
    """`pid`'s command line, word by word; None when it cannot be read."""
    try:
        argv = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
        words = [a.decode("utf-8", "replace") for a in argv]
    except OSError:
        try:
            import subprocess

            out = subprocess.run(
                ["ps", "-ww", "-o", "args=", "-p", str(pid)], capture_output=True, text=True, timeout=5, check=False
            ).stdout
        except (OSError, subprocess.SubprocessError):
            return None
        words = out.split()
    return words


def _is_daemon_host(pid: int) -> bool:
    """Is `pid` the daemon host (every session's worker runs there)?"""
    words = _argv_words(pid)
    return bool(words) and DAEMON_HOST_MARK in words


def _parent_is_service(pid: int) -> bool:
    """Is `pid`'s parent a running Probe service (`python -I -m probe.service`)?"""
    from ....foundation.service_api import procid

    info = procid.proc(pid)
    words = _args(info.ppid) if info is not None and info.ppid > 1 else None
    return bool(words) and "probe.service" in words


def _host_owned_here(pid: int) -> bool:
    """Is the daemon host `pid` this service's own child (stopped run by run,
    `stop_hosted`)? Else it outlived the service that started it (an old tap's
    runs keep it up): nobody here can ask its runs, so it is signalled -- its
    SIGTERM hands every run over (`host.Host.signalled`)."""
    from ....foundation.service_api import procid

    info = procid.proc(pid)
    return info is not None and info.ppid == os.getpid()


def _is_worker(pid: int, sid: str) -> bool:
    """Is `pid` a running `probe daemon worker` for `sid` (never a reused pid)?"""
    words = _argv_words(pid)
    if not words:
        return False
    if DAEMON_HOST_MARK in words:
        return True  # the daemon host runs every session's worker; `.worker.json` names it for this one
    return "daemon" in words and "worker" in words and sid in " ".join(words)


def _worker_pid(state: Path, sid: str) -> int | None:
    try:
        data = json.loads((state / "reads" / "requests" / sid / ".worker.json").read_text(encoding="utf-8"))
        pid = int(data.get("pid"))
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    return pid if pid > 1 and _is_worker(pid, sid) else None


def state_dirs(extra: set | frozenset = frozenset()) -> list[Path]:
    """The default state folder, then every other one a live session named (D13)."""
    out = [paths.state_dir()]
    for raw in sorted(extra):
        path = Path(raw)
        if path not in out:
            out.append(path)
    return out


def _args(pid: int) -> list[str] | None:
    """`pid`'s command line, or None when it cannot be read."""
    try:
        return [a.decode("utf-8", "replace") for a in Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")]
    except OSError:
        pass
    try:
        import subprocess

        out = subprocess.run(
            ["ps", "-ww", "-o", "args=", "-p", str(pid)], capture_output=True, text=True, timeout=5, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.split() if out.returncode == 0 and out.stdout.strip() else None


#: Set by the service when it records sessions itself (`recorders.RecorderHost.live`):
#: is this session recorded here now (not finishing)? A worker the service's own
#: recorder started has the service as its parent.
_hosted_live: Callable[[str], bool] | None = None
#: The daemon host's word on a session's runs there (`WorkerHost.hosted_draining`):
#: True finishing an ended session's queue, False live, None unknown.
_hosted_draining: Callable[[str], bool | None] | None = None


def set_hosted(live: Callable[[str], bool] | None,
               draining: Callable[[str], bool | None] | None = None) -> None:
    global _hosted_live, _hosted_draining
    _hosted_live, _hosted_draining = live, draining


def _session_ended(pid: int | None, sid: str | None = None) -> bool:
    """Is this worker finishing the queue of a session that ended? Its
    supervisor (`tap watch`, or this service for a session it records:
    `workers.py`, or the tap's own on the recorder's thread) stops it with
    SIGTERM when the session ends, so a worker whose parent is no
    longer a `tap ... watch` -- or, under this service, whose session is no
    longer recorded here -- is draining. Unknown (the parent cannot be read)
    counts as live, as before this check."""
    if pid is None:
        return False
    from ....foundation.service_api import procid

    info = procid.proc(pid)
    if info is None:
        return False
    if _is_daemon_host(pid) and info.ppid != os.getpid():
        # Not this service's host (one its service left, or seen from the update
        # guard): its own file says which runs finish an ended session's queue (never
        # handed over: no successor would record the tail) and which are live.
        from ...sessions.daemon_host import host_runs_on_file

        runs = host_runs_on_file(pid)
        if runs is not None and sid in runs:
            return runs[sid]
        return True  # unknown: never handed over (a tail with no successor is lost; an update can wait)
    if info.ppid <= 1:
        return True
    if info.ppid == os.getpid():
        if _is_daemon_host(pid):
            # The host runs every session's worker, an old tap's too (through the
            # proxy: no recorder here, yet live): its own beat says which runs are
            # finishing an ended session's queue.
            draining = _hosted_draining
            try:
                verdict = draining(sid) if draining is not None and sid is not None else None
            except Exception:  # noqa: BLE001 -- unknown: the recorder's word below
                verdict = None
            if verdict is not None:
                return verdict
        live = _hosted_live
        try:
            return not (live is not None and sid is not None and live(sid))
        except Exception:  # noqa: BLE001 -- unknown counts as live
            return False
    parent = _args(info.ppid)
    if parent is None:
        return False
    return not ("watch" in parent and any("tap" in word for word in parent))


def live_workers(dirs: list[Path]) -> list[Worker] | None:
    """Every daemon worker holding its lock under `dirs`, each marked
    `draining` when its session ended; None when a folder cannot be listed
    (unknown: busy)."""
    found: list[Worker] = []
    for state in dirs:
        try:
            locks = sorted((state / "daemon").glob("*.lock"))
        except OSError:
            return None
        for lock in locks:
            if _flock_held(lock):
                pid = _worker_pid(state, lock.stem)
                found.append(Worker(lock.stem, lock, pid, _session_ended(pid, lock.stem)))
    return found


def daemon_worker_running() -> bool:
    """A daemon worker holds `<state>/daemon/<sid>.lock` for its whole life."""
    workers = live_workers([paths.state_dir()])
    return workers is None or bool(workers)


def hand_over_workers(dirs: list[Path]) -> int:
    """After a side-by-side switch, ask every live session's running worker to
    hand over at its next safe point; its supervisor starts it again through
    `probe` (the tap's) or runtime.json's interpreter (the service's), which
    is the new version now. A worker finishing an ended
    session's queue finishes it on its own version. Returns how many were
    asked. Never raises."""
    asked = 0
    # This service exits right after: nobody re-touches the marker as the D7
    # wait does (`_stop_workers`), and a worker reaches its next safe point
    # after its model round, which can outlast the marker's 10 s. So the marker
    # is dated ahead, by the stop window: fresh until then (the next worker
    # removes it when it takes the session's lock).
    ahead = time.time() + _env_seconds(WORKER_STOP_ENV, WORKER_STOP_S)
    for worker in live_workers(dirs) or []:
        if worker.draining or worker.pid is None or not _is_worker(worker.pid, worker.sid):
            continue
        with contextlib.suppress(OSError):
            worker.handover.touch()
            os.utime(worker.handover, (ahead, ahead))
        if _is_daemon_host(worker.pid) and _parent_is_service(worker.pid):
            # The host of a live service runs every session's worker and is never
            # signalled for one: its runs stop as that service leaves, and hand over
            # on the marker dated ahead above. One its service left is signalled
            # below (its SIGTERM hands every run over).
            asked += 1
            continue
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.kill(worker.pid, signal.SIGTERM)
            asked += 1
    return asked


class WorkersMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    async def _stop_workers(self, workers: list) -> list:
        """Ask each running worker to hand over at its next safe point (D7):
        its `.handover` marker, kept fresh, then SIGTERM. Returns the ones
        still holding their lock after `worker_stop_s`."""
        def touch(found: list) -> None:
            for worker in found:
                with contextlib.suppress(OSError):
                    worker.handover.touch()

        touch(workers)
        for worker in workers:
            if worker.pid is None or not _is_worker(worker.pid, worker.sid):
                continue
            if _is_daemon_host(worker.pid) and _host_owned_here(worker.pid):
                # Every session's worker runs there: its run is stopped, never the host.
                if self.stop_hosted(worker.sid):
                    log(f"asked session {worker.sid}'s run in the daemon host {worker.pid} to hand over for the update")
                continue
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.kill(worker.pid, signal.SIGTERM)
                log(f"asked daemon worker {worker.pid} ({worker.sid}) to hand over for the update")
        deadline = time.monotonic() + self.worker_stop_s
        touched = time.monotonic()
        while True:
            live = [w for w in workers if _flock_held(w.lock)]
            if not live or time.monotonic() >= deadline:
                break
            if time.monotonic() - touched >= HANDOVER_TOUCH_S:
                touch(live)
                touched = time.monotonic()
            await asyncio.sleep(WORKER_POLL_S)
        for worker in workers:
            # Never leave one behind: a later session end must drain, not hand over.
            with contextlib.suppress(OSError):
                worker.handover.unlink()
        return live
