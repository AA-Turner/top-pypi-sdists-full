"""Is an experiment running on this box now? Keeps auto-update off a live run; FAILS CLOSED (doubt = maybe live).

Per-run entries: an flock (SDK, `probe exec`) or a lease (bare `run start`/`run end`). Why: DESIGN.md (run_lock.py).
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from probe.shared.updates import version_policy

RUNS_DIRNAME = "runs"
FLOCK_SUFFIX = ".flock"
LEASE_SUFFIX = ".lease"

#: Seconds a bare-bracket lease lives unrenewed: ordinary logging renews it (free, on writes the
#: run makes); a run killed between `start` and `end` frees the box within the hour.
LEASE_SECONDS = 1800

#: "1" asserts no run is live, whatever the state: for tests, and a user clearing a stuck lease.
OVERRIDE_ENV = "PROBE_ASSUME_NO_RUNS"

#: Above this many entries, report live without scanning: a big sweep is tens, so more means
#: cleanup failed, and the every-command path must not pay for it.
MAX_SCAN_ENTRIES = 512


def runs_dir() -> Path:
    return version_policy.state_dir() / RUNS_DIRNAME


def _to_safe_name(run_id: str) -> str:
    """A filesystem-safe stem for a run ref (ids or slugs, may carry `/`). Two refs sharing
    a name share an entry, which errs the safe way."""
    return "".join(char if char.isalnum() or char in "-_." else "_" for char in run_id) or "run"


def _fcntl():
    """The flock provider: `probe._shared.oscompat` (fcntl's flock on POSIX, msvcrt's byte
    lock on Windows), or None on a platform with neither. Reported, never swallowed (unlike
    the outbox's `_kick_drainer`): swallowing would break fail-closed exactly there."""
    try:
        from ..._shared import oscompat

        return oscompat
    except ImportError:
        return None


# flock tier: SDK and `probe exec`.


class RunLock:
    """An flock held while this object is open. Keep a reference for the run's lifetime;
    dropping it, closing it or dying releases the lock (dying being the point)."""

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self.path = runs_dir() / f"{_to_safe_name(run_id)}{FLOCK_SUFFIX}"
        self._handle = None

    def acquire(self) -> bool:
        """Take the lock. False when it cannot be taken, never fatal: a failed run is worse
        than an unprotected one, so callers proceed."""
        module = _fcntl()
        if module is None:
            return False
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            handle = open(self.path, "a+")  # noqa: SIM115 -- held on purpose
        except OSError:
            return False
        try:
            module.flock(handle.fileno(), module.LOCK_EX | module.LOCK_NB)
        except (OSError, ValueError):
            handle.close()
            return False
        try:
            handle.seek(0)
            handle.truncate()
            handle.write(json.dumps({"pid": os.getpid(), "run": self.run_id, "at": int(time.time())}))
            handle.flush()
        except OSError:
            pass  # the LOCK is the signal; its contents are only for humans
        self._handle = handle
        return True

    def release(self) -> None:
        """Drop the lock and remove the entry. Idempotent, never raises."""
        handle, self._handle = self._handle, None
        if handle is None:
            return
        try:
            handle.close()  # closing the fd releases the flock
        except OSError:
            pass
        try:
            self.path.unlink(missing_ok=True)
        except OSError:
            pass

    def __enter__(self) -> RunLock:
        self.acquire()
        return self

    def __exit__(self, *_exc: object) -> None:
        self.release()


def acquire(run_id: str) -> RunLock | None:
    """Take a process-held lock for `run_id`, or None if it could not be taken.

    Never raises: instrumentation must not be able to break the run it measures.
    """
    try:
        lock = RunLock(run_id)
        return lock if lock.acquire() else None
    except Exception:  # noqa: BLE001 -- see docstring
        return None


# Lease tier: the bare `run start` / `run end` bracket.


def touch_lease(
    run_id: str, *, seconds: int = LEASE_SECONDS, write_epoch: int | None = None
) -> None:
    """Start or renew the lease for `run_id` (`probe run start`, then every run-scoped write).
    Never raises.

    ``write_epoch`` (0185) pins the writer generation `run start` opened the bracket under, so
    later CLI writes stamp THAT epoch and a bracket superseded by a reopen elsewhere is refused
    instead of splicing. Renewals pass ``None``; the pin survives them.
    """
    try:
        path = runs_dir() / f"{_to_safe_name(run_id)}{LEASE_SUFFIX}"
        payload: dict = {"run": run_id, "expires_at": int(time.time()) + int(seconds)}
        if write_epoch is None:
            try:
                prior = json.loads(path.read_text())
                if isinstance(prior, dict) and prior.get("write_epoch") is not None:
                    payload["write_epoch"] = int(prior["write_epoch"])
            except (OSError, ValueError):
                pass
        else:
            payload["write_epoch"] = int(write_epoch)
        version_policy.atomic_write_json(path, payload)
    except Exception:  # noqa: BLE001
        pass


def lease_write_epoch(run_id: str) -> int | None:
    """The epoch `run start` pinned for this run's bracket, if a LIVE lease
    carries one. Never raises; an expired or absent lease answers None and the
    caller falls back to the row's current epoch (best-effort, like the lease
    tier itself)."""
    try:
        path = runs_dir() / f"{_to_safe_name(run_id)}{LEASE_SUFFIX}"
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            return None
        if float(data.get("expires_at", 0)) < time.time():
            return None
        epoch = data.get("write_epoch")
        return int(epoch) if epoch is not None else None
    except Exception:  # noqa: BLE001
        return None


def renew_lease_if_stale(run_id: str, *, seconds: int = LEASE_SECONDS) -> None:
    """Extend an EXISTING lease once it is half spent (the CLI's run-handle path). Never raises.

    Only an existing lease: an flock-tier run (SDK, `probe exec`) must not sprout a lease it
    never clears. Only past halfway: `probe log` in a tight loop would write on every call, on
    the every-command path a perf review held to O(1).
    """
    try:
        path = runs_dir() / f"{_to_safe_name(run_id)}{LEASE_SUFFIX}"
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            return  # no lease here: an flock-tier run, or none at all
        if not isinstance(data, dict):
            return
        expires_at = float(data.get("expires_at", 0))
        if expires_at - time.time() > (seconds / 2):
            return  # still comfortably valid; skip the write
        touch_lease(run_id, seconds=seconds)
    except Exception:  # noqa: BLE001
        pass


def clear_lease(run_id: str) -> None:
    """Drop the lease at `probe run end`. Never raises."""
    try:
        (runs_dir() / f"{_to_safe_name(run_id)}{LEASE_SUFFIX}").unlink(missing_ok=True)
    except OSError:
        pass


def _lease_is_live(path: Path, now: float) -> bool:
    """An unreadable or malformed lease counts as LIVE: fail-closed per entry, since
    guessing "dead" is guessing the expensive way."""
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        return True
    if not isinstance(data, dict):
        return True
    try:
        return float(data.get("expires_at", 0)) > now
    except (TypeError, ValueError):
        return True


def _flock_is_held(path: Path) -> bool:
    """Probe without disturbing the holder: a non-blocking take that succeeds means nobody
    had it (release, report dead). A fresh `open()` reads right even when the holder is
    THIS process. `outbox_worker._lease_is_free`, inverted."""
    module = _fcntl()
    if module is None:
        return True  # cannot prove absence -> assume presence
    try:
        handle = open(path, "a+")  # noqa: SIM115 -- closed below
    except OSError:
        return True
    try:
        module.flock(handle.fileno(), module.LOCK_EX | module.LOCK_NB)
    except BlockingIOError:
        return True  # somebody holds it: a live run
    except (OSError, ValueError):
        return True  # unknown -> fail closed
    else:
        try:
            module.flock(handle.fileno(), module.LOCK_UN)
        except (OSError, ValueError):
            pass
        # A dead process's leftover: drop it. Windows cannot delete an open file, so close first;
        # the delete then fails if another process opened it meanwhile (the safe side).
        if os.name == "nt":
            handle.close()
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        return False
    finally:
        handle.close()


# The question the apply gate asks.


def any_live(directory: Path | None = None) -> bool:
    """True when a run may be in flight. FAILS CLOSED: an unreadable directory, an error, a
    malformed lease or no fcntl all read True; False only for a directory read cleanly with
    nothing held or unexpired. `directory`: another state folder's runs (the Probe service
    checks every registered session's, plan D13); default `runs_dir()`.
    """
    if os.environ.get(OVERRIDE_ENV) == "1":
        return False
    try:
        directory = runs_dir() if directory is None else directory
        if not directory.is_dir():
            return False  # never any runs here: the one confident False
        if _fcntl() is None:
            # No lock on this platform: SDK and `exec` runs (flock tier) are invisible, so
            # unprovable reads as live.
            return True
        now = time.time()
        entries = sorted(directory.iterdir())
    except OSError:
        return True
    if len(entries) > MAX_SCAN_ENTRIES:
        # Every-command path: past any plausible run count, cleanup is broken and a scan would
        # slow every command; refuse, and unknown reads as live.
        return True
    for entry in entries:
        try:
            if entry.name.endswith(FLOCK_SUFFIX):
                if _flock_is_held(entry):
                    return True
            elif entry.name.endswith(LEASE_SUFFIX):
                if _lease_is_live(entry, now):
                    return True
                try:
                    entry.unlink(missing_ok=True)
                except OSError:
                    pass
        except Exception:  # noqa: BLE001 -- one bad entry must not read as "all clear"
            return True
    return False


def live_runs() -> list[str]:
    """Names of the runs holding the box, for `probe doctor` (diagnostic; `any_live()` is the
    gate): shows WHY a box has not updated in six days."""
    found: list[str] = []
    try:
        directory = runs_dir()
        if not directory.is_dir():
            return found
        now = time.time()
        for entry in sorted(directory.iterdir()):
            if entry.name.endswith(FLOCK_SUFFIX) and _flock_is_held(entry):
                found.append(entry.name[: -len(FLOCK_SUFFIX)])
            elif entry.name.endswith(LEASE_SUFFIX) and _lease_is_live(entry, now):
                found.append(entry.name[: -len(LEASE_SUFFIX)])
    except OSError:
        pass
    return found
