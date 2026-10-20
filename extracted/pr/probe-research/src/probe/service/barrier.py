"""The update barrier: no new Probe process starts while the service updates (plan X1).

The service applies a CLI or plugin update only on a quiet machine (no daemon
worker, no run, no wizard, no action). A quiet check alone races: a `probe`
started a moment after it would import from the env `uv tool upgrade` is
replacing. So the service raises this barrier FIRST, checks again, and only
then updates; every CLI start and every daemon worker start looks for it:

    absent (the common case)      one stat, go on
    present, its owner alive      wait up to WAIT_S for it to go, else busy
                                  (the owner: the service, then the update
                                  child, so a service stopped mid-update
                                  leaves it up until the update is done)
    present, but stale            go on (its owner died, or it is too old)
    present, and ours             go on: the update's own child processes
                                  (`probe --version` from `uv tool upgrade`'s
                                  checks) carry its token in TOKEN_ENV

`<service dir>/update.barrier` = `{"pid", "start_time", "token", "created_at"}`,
0600, written atomically. Fixed under `$HOME` like everything of the service's.

Stdlib only, and nothing but `paths` at import: `probe._entry` imports this
before the CLI on every `probe` command (a training loop's `probe log`
included), so the common path costs one import of two small modules and one
stat.
"""

from __future__ import annotations

import contextlib
import json
import os
import time

from . import paths

#: Set in the update's own child processes, so the barrier never stops its owner.
TOKEN_ENV = "PROBE_UPDATE_BARRIER_TOKEN"
#: How long a CLI start waits for an update to finish before it gives up.
WAIT_S = 10.0
#: A barrier older than this is stale whatever its pid says: the update step
#: holds the service at most 10 minutes (plan R3), so 15 is a crashed one.
MAX_AGE_S = 15 * 60
POLL_S = 0.1
#: A `probe` command turned away by the barrier exits with this (EX_TEMPFAIL,
#: as `wizard_lock.BUSY_EXIT_CODE`): nothing ran, try again.
BUSY_EXIT_CODE = 75
#: ... and `probe daemon worker` with this: `probe.daemon.worker.EXIT_RESPAWN_LATER`,
#: which the tap's supervisor answers with a later respawn, not a crash count.
#: (`tests/test_service_updater.py` keeps the two equal.)
WORKER_BUSY_EXIT_CODE = 5
MESSAGE = "Probe is updating itself on this machine; try again in a moment"


def read() -> dict | None:
    """The barrier's record, or None when there is none (or it cannot be read)."""
    try:
        data = json.loads(paths.barrier_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _blocks(data: dict | None, now: float) -> bool:
    """Does this record stop a start? Not when it is ours, stale or unreadable."""
    if data is None:
        return False
    token = os.environ.get(TOKEN_ENV)
    if token and data.get("token") == token:
        return False
    try:
        if now - float(data.get("created_at", 0)) > MAX_AGE_S:
            return False
        pid = int(data.get("pid", 0))
        start = str(data.get("start_time") or "")
    except (TypeError, ValueError):
        return False
    from . import procid

    # Unknown (None) counts as alive: waiting 10 s costs less than starting
    # under an update.
    return procid.alive(pid, start) is not False


def wait(timeout: float | None = None) -> bool:
    """True once no barrier stops this process (at once on the common path);
    False when one still does after `timeout` (default WAIT_S). Never raises."""
    try:
        os.stat(paths.barrier_path())
    except OSError:
        return True
    deadline = time.monotonic() + (WAIT_S if timeout is None else timeout)
    while True:
        try:
            if not _blocks(read(), time.time()):
                return True
        except Exception:  # noqa: BLE001 -- a broken barrier must not stop every command
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(POLL_S)


def raise_barrier(token: str, pid: int | None = None) -> None:
    """Write the barrier for `pid` (default: this process, the service), which
    it lasts as long as. The update names its child once that runs, so a
    service stopped mid-update leaves the barrier up until `uv tool upgrade`
    is done. Raises OSError."""
    from . import procid

    pid = os.getpid() if pid is None else pid
    target = paths.barrier_path()
    paths.private_dir(target.parent)
    record = {
        "pid": pid,
        "start_time": procid.start_time(pid) or "",
        "token": token,
        "created_at": time.time(),
    }
    tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    try:
        with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
            json.dump(record, handle)
        os.replace(tmp, target)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def lower(token: str) -> None:
    """Remove the barrier if it is still the one `token` raised. Never raises."""
    data = read()
    if data is not None and data.get("token") != token:
        return
    with contextlib.suppress(OSError):
        paths.barrier_path().unlink()
