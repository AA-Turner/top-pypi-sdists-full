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

DETACHED, AND DELIBERATELY NOT A CHILD. `start_new_session` puts the watcher in
its own session and process group. A watcher that stayed in the training job's
group would take the same Ctrl-C the job takes -- and a Ctrl-C is precisely one
of the deaths it is supposed to observe. The observer cannot share the fate of
the observed.

Fail-open throughout. A watcher that cannot be spawned costs the box its
explanations and costs the run nothing.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def lock_path(directory: Path | str | None = None) -> Path:
    from probe.box import registry

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
    """Start a watcher if this box has none. Returns whether one was started.

    Cheap by requirement: this runs when a run starts beating, which on a
    sixty-four rank job means sixty-four calls within a second. The only work
    before the lock probe is a path join.
    """
    try:
        from probe.box import watch

        if not watch.enabled():
            return False
        if already_running(directory):
            return False
        env = dict(os.environ)
        if directory is not None:
            env["PROBE_BOX_DIR"] = str(directory)
        # `-m probe.box` rather than a console script: the watcher must run on
        # the SAME interpreter as the job that spawned it, which is the one
        # that has the client installed. A console script resolves through
        # PATH and can find a different environment entirely.
        subprocess.Popen(  # noqa: S603 -- argv is ours, not a caller's
            [sys.executable, "-m", "probe.box"],
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True,
        )
        return True
    except Exception as exc:  # noqa: BLE001 -- never let this touch the run
        logger.debug("box: could not spawn a watcher: %s", exc)
        return False


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
