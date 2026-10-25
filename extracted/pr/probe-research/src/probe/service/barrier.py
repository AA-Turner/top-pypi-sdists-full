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
    present, replacing nothing    go on: an update side by side (D6) installs
    a `probe` runs from           the new CLI in a folder of its own and
                                  switches in one rename, one of the plugins
                                  only leaves the CLI alone (`replaces_cli`
                                  false), and a process pinned to a version
                                  env (`probe-versions/<v>`, `pinned`) is
                                  never replaced: the installed version runs
                                  at once (plan C6; every `probe` waited ~10 s
                                  and exited 75 during any update before)

`<service dir>/update.barrier` = `{"pid", "start_time", "token", "created_at",
"replaces_cli"}`, 0600, written atomically. Fixed under `$HOME` like everything
of the service's. A record without `replaces_cli` (a service before it) blocks
as before.

A caller with a deadline of its own (a hook: Claude Code and Codex kill it at
its entry's timeout) says so in DEADLINE_ENV, and waits only until then (plan
D12): a hook that gives up busy beats a hook killed mid-run.

`workers.hold` (same record) comes first, while the service asks the daemon
workers to stop at a safe point before an update (plan D7): it stops NEW
`probe daemon worker` starts only (they exit WORKER_BUSY_EXIT_CODE, which the
tap's supervisor answers with a later respawn; the service's own starts none
while it is up: `workers.py`), so a worker restarted by its
supervisor meanwhile does not start on the code about to be replaced, while
every other `probe` command, the stopping workers' own included, runs on.

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
#: An absolute deadline (epoch seconds) a caller must finish by: the hook
#: dispatcher sets it to its own (`hooks/dispatch.py`). The barrier waits at
#: most until DEADLINE_MARGIN_S before it.
DEADLINE_ENV = "PROBE_HOOK_DEADLINE"
DEADLINE_MARGIN_S = 0.5
#: A deadline this far past was inherited by a process the hook left behind.
STALE_DEADLINE_S = 60.0
HOLD_NAME = "workers.hold"
#: Touched when the hold ends: a worker that handed over for the update reads
#: as handing over until DAEMON_HANDOVER_STALE_S after this
#: (`session_marker.daemon_status`), not after its own release.
HOLD_RELEASED_NAME = "workers.released"
#: In the prefix of an interpreter that runs from a version env
#: (`probe._shared.installs.running_from_versions`, VERSIONS_DIRNAME): nothing
#: an update does replaces its files (tests/test_service_updater.py holds the
#: two equal).
PINNED_DIR = "/probe-versions/"
#: A hold older than this is stale: the service waits for workers at most
#: `updater.WORKER_STOP_S`, then updates (minutes), then lets go.
HOLD_MAX_AGE_S = 45 * 60


def read(path=None) -> dict | None:
    """The barrier's record, or None when there is none (or it cannot be read)."""
    try:
        data = json.loads((path or paths.barrier_path()).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def pinned(prefix: str | None = None) -> bool:
    """Does this interpreter run from a version env (`probe-versions/<v>/...`,
    D6)? Then no update replaces its files: a new version goes in a folder of
    its own, and a version in use is never pruned."""
    import sys

    return PINNED_DIR in (prefix if prefix is not None else sys.prefix).replace(os.sep, "/")


def _blocks(data: dict | None, now: float) -> bool:
    """Does this record stop a start? Not when it is ours, stale or
    unreadable, nor when the update replaces nothing this process runs from
    (`replaces_cli` false, or a `pinned` interpreter)."""
    if data is None:
        return False
    token = os.environ.get(TOKEN_ENV)
    if token and data.get("token") == token:
        return False
    if data.get("replaces_cli") is False or pinned():
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


def budget(default: float | None = None) -> float:
    """How long this process may wait: `default` (WAIT_S), cut to what
    DEADLINE_ENV leaves (less DEADLINE_MARGIN_S), never below 0. Never raises."""
    default = WAIT_S if default is None else default
    raw = os.environ.get(DEADLINE_ENV)
    if not raw:
        return default
    try:
        left = float(raw) - time.time() - DEADLINE_MARGIN_S
    except ValueError:
        return default
    if left != left or left < -STALE_DEADLINE_S:
        # NaN, or long past: a process that outlived the hook that started it
        # (a detached job inherits the variable) waits as any command does.
        return default
    return max(0.0, min(default, left))


def hook_deadline_live() -> bool:
    """Is this process a hook's call: DEADLINE_ENV is set and is not long past
    (a detached job that outlived its hook inherits the variable, and waits as
    any command does: `budget`)? Never raises."""
    raw = os.environ.get(DEADLINE_ENV)
    if not raw:
        return False
    try:
        left = float(raw) - time.time()
    except ValueError:
        return False
    return left == left and left >= -STALE_DEADLINE_S


def wait(timeout: float | None = None) -> bool:
    """True once no barrier stops this process (at once on the common path);
    False when one still does after `timeout` (default: WAIT_S, cut to the
    caller's deadline). Never raises."""
    # This machine's barrier, and the one a service from before the machine key
    # raises (`paths.legacy_barrier_path`): during the update that brings this
    # code, that older service is the one replacing the files.
    present = []
    for path in (paths.barrier_path(), paths.legacy_barrier_path()):
        try:
            os.stat(path)
        except OSError:
            continue
        present.append(path)
    if not present:
        return True
    deadline = time.monotonic() + (budget() if timeout is None else timeout)
    while True:
        try:
            if not any(_blocks(read(path), time.time()) for path in present):
                return True
        except Exception:  # noqa: BLE001 -- a broken barrier must not stop every command
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(POLL_S)


def raise_barrier(token: str, pid: int | None = None, *, replaces_cli: bool = True) -> None:
    """Write the barrier for `pid` (default: this process, the service), which
    it lasts as long as. The update names its child once that runs, so a
    service stopped mid-update leaves the barrier up until `uv tool upgrade`
    is done. `replaces_cli`: does it replace the files a `probe` started now
    runs from (an in-place CLI update); false for one side by side or of the
    plugins only, which holds no start back. Raises OSError."""
    _write(paths.barrier_path(), token, pid, replaces_cli=replaces_cli)


def _write(target, token: str, pid: int | None, *, replaces_cli: bool = True) -> None:
    from . import procid

    pid = os.getpid() if pid is None else pid
    paths.private_dir(target.parent)
    record = {
        "pid": pid,
        "start_time": procid.start_time(pid) or "",
        "token": token,
        "created_at": time.time(),
        "replaces_cli": replaces_cli,
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


def hold_path():
    return paths.service_dir() / HOLD_NAME


def hold_workers(token: str) -> None:
    """Stop new daemon worker starts while the service stops the running ones
    (plan D7); lasts as long as this process. Raises OSError."""
    _write(hold_path(), token, None)


def release_workers(token: str) -> None:
    """Remove the hold if it is still `token`'s. Never raises."""
    try:
        data = json.loads(hold_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = None
    if isinstance(data, dict) and data.get("token") != token:
        return
    with contextlib.suppress(OSError):
        hold_path().unlink()
    with contextlib.suppress(OSError):
        (paths.service_dir() / HOLD_RELEASED_NAME).touch()


def workers_held() -> bool:
    """Is a `probe daemon worker` start to come back later? One stat when not.
    Stale (its owner gone, or older than HOLD_MAX_AGE_S) or unreadable: no.
    Never raises."""
    try:
        os.stat(hold_path())
    except OSError:
        return False
    try:
        data = json.loads(hold_path().read_text(encoding="utf-8"))
        if not isinstance(data, dict) or time.time() - float(data.get("created_at", 0)) > HOLD_MAX_AGE_S:
            return False
        from . import procid

        return procid.alive(int(data.get("pid", 0)), str(data.get("start_time") or "")) is not False
    except Exception:  # noqa: BLE001 -- a broken hold must not stop every worker
        return False
