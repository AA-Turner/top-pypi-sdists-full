"""Starting the watcher: exactly one per box, owned by nobody.

THE LEASE IS THE WHOLE DESIGN. Every run that starts beating as owner tries to
spawn a watcher, because no run can know whether it is the first on this
machine. Sixty-four ranks starting together would otherwise produce sixty-four
watchers, each reporting the same death. A held file lock is what makes that
race harmless: the winner spawns, everyone else finds the lock taken and moves
on, and the cost to a losing rank is one failed lock acquisition.

The lock is held by the WATCHER for its whole life, not by the spawner. That is
what makes it a lease rather than a mutex: when the watcher exits, or is killed,
or its host reboots, the lock goes with the process and the next run to start
takes over. Nothing has to clean up after a crash, which matters for a component
whose entire purpose is to be present when things die badly.

NEVER THE JOB'S CHILD. The run asks the Probe service to watch (plan D9, D20:
the training process only observes): the service runs the watcher as a THREAD
(`thread.WatcherThread`), or as a child of its own on this interpreter when
this process's login or network settings differ from the service's, starting
the service where none runs. Either way it takes this same lease, and it never
shares the job's process group or its Ctrl-C, one of the deaths it observes.

Fail-open throughout. A watcher the service cannot start costs the box its
explanations and costs the run nothing; nothing is forked here.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

#: What a run spawns: this package's own `__main__` (the old `probe.box` stays an alias).
WATCHER_MODULE = "probe.sdk.run.watcher"


def lock_path(directory: Path | str | None = None) -> Path:
    from probe.sdk.run.watcher import registry

    d = Path(directory) if directory is not None else registry.default_dir()
    return d.parent / "watcher.lock"


def already_running(directory: Path | str | None = None) -> bool:
    """Whether a watcher holds the lease right now.

    Probed by trying to take the lock and immediately dropping it, which is the
    only honest test: a pid file can outlive its process, a lock held by a dead
    process cannot.
    """
    import fcntl

    path = lock_path(directory)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = path.open("a+")
    except Exception:  # noqa: BLE001 -- an unwritable state dir is not an error
        return True  # assume owned; never spawn into an unknown
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    except Exception:  # noqa: BLE001
        return True
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return False
    finally:
        handle.close()


def maybe_spawn(directory: Path | str | None = None) -> bool:
    """Ask the service to watch this box when no watcher holds the lease (plan D9): on a thread of
    its own, so a run's start never waits on the service's. True when the ask went out.

    Cheap by requirement: this runs when a run starts beating, which on a sixty-four rank job
    means sixty-four calls within a second; the lease probe stops all but the first.
    """
    try:
        from probe.sdk.run.watcher import watcher as watch

        if not watch.enabled():
            return False
        if already_running(directory):
            return False
        thread = threading.Thread(target=ask_service, args=(directory,), name="probe-box-watch", daemon=True)
        thread.start()
        return True
    except Exception as exc:  # noqa: BLE001 -- never let this touch the run
        logger.debug("box: could not ask for a watcher: %s", exc)
        return False


def ask_service(directory: Path | str | None = None) -> str | None:
    """`box.watch` for the registry `directory` (default: this process's): the service's answer's
    state, or None (no service, a refusal). Its env: this process's settings and credentials
    (plan D11), `PROBE_BOX_DIR` the registry. Never raises."""
    try:
        from probe.foundation.service_api import handoff
        from probe.foundation.service_api.wire import Method
        from probe.sdk.run.watcher import registry

        env = {**handoff.runtime_env(), **handoff.credential_env()}
        env["PROBE_BOX_DIR"] = os.path.abspath(str(directory if directory is not None else registry.default_dir()))
        parameters = {"python": sys.executable, "env": env}
        cwd = handoff.cwd()
        if cwd:
            parameters["cwd"] = cwd
        answer = handoff.request(Method.BOX_WATCH, parameters, timeout=10.0)
        return answer.get("state") if isinstance(answer, dict) and answer.get("accepted") else None
    except Exception as exc:  # noqa: BLE001 -- the watcher is never the run's problem
        logger.debug("box: the service took no watcher: %s", exc)
        return None


def hold_lease(directory: Path | str | None = None):
    """Take the lease for the caller's lifetime, or return None if taken.

    The handle is returned rather than closed: closing it drops the lock, so
    the caller keeps it alive for exactly as long as it intends to be the
    watcher on this box.
    """
    import fcntl

    path = lock_path(directory)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = path.open("a+")
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except Exception:  # noqa: BLE001 -- somebody else has it, or we cannot write
        return None
    try:
        handle.seek(0)
        handle.truncate()
        handle.write(f"{os.getpid()}\n")
        handle.flush()
    except Exception:  # noqa: BLE001 -- the pid is a courtesy, the lock is the lease
        pass
    return handle
