"""CaptureRegistry: this host's registry of open capture windows -- overlap, ownership, and ignore rules shared by a run's processes."""

from __future__ import annotations
import contextlib
import json
import os
import socket
import time
from pathlib import Path
from typing import Any

from ....foundation.os_backend import os_backend as oscompat
from ...recording_rules import recording_rules as _ignore
from ....foundation.safe_warn import safe_warn as _diagnostics
OWNER_ENV = "PROBE_CAPTURE_OWNER"
ROOT_ENV = "PROBE_CAPTURE_ROOT"
LOG_OWNER_ENV = "PROBE_CAPTURE_LOG_OWNER"


def _this_host(env: str) -> bool:
    owner = (os.environ.get(env) or "").strip()
    return bool(owner) and owner == socket.gethostname()


def log_owned_here() -> bool:
    """A launcher on this host tees this process's output already."""
    return _this_host(LOG_OWNER_ENV)


def outputs_owned_here(root: str) -> bool:
    """A launcher on this host already sweeps a folder containing `root`."""
    if not _this_host(OWNER_ENV):
        return False
    launcher_root = (os.environ.get(ROOT_ENV) or "").strip()
    if not launcher_root:
        return True  # an older launcher that did not say: assume it covers us
    return _within(os.path.realpath(root), os.path.realpath(launcher_root))


def _within(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def _overlap(a: str, b: str) -> bool:
    if not a or not b:
        return False  # a record with no root watches nothing
    return _within(a, b) or _within(b, a)


def _write_json(path: Path, data: Any) -> None:
    from ....foundation.durable.durable import write_text_atomic

    write_text_atomic(path, json.dumps(data), mode=0o600)


# -- liveness ------------------------------------------------------------------------------
def _process_started(pid: int) -> float | None:
    """When ``pid`` started, or None. A pid alone is reused; pid + start is not."""
    try:
        import psutil

        return psutil.Process(pid).create_time()
    except Exception:  # noqa: BLE001
        return None


def _alive(pid: Any, started: Any = None) -> bool:
    """Whether a recorded process is still running. Total over any input: the
    registry is a folder of files anything can damage, and one bad file must
    not break capture for every later run."""
    try:
        pid = int(pid or 0)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        import psutil
    except ImportError:
        # The Windows-safe probe: os.kill(pid, 0) TERMINATES a process there.
        from ...diagnostics import _pid_alive

        return _pid_alive(pid)
    try:
        process = psutil.Process(pid)
        if process.status() == psutil.STATUS_ZOMBIE:
            return False  # exited, just not reaped yet
        now = process.create_time()
    except psutil.NoSuchProcess:
        return False
    except Exception:  # noqa: BLE001 -- access denied and the like: assume alive
        return True
    if isinstance(started, (int, float)) and abs(now - started) > 1.0:
        return False  # the pid was reused
    return True


def _record_alive(record: dict) -> bool:
    return _alive(record.get("pid"), record.get("proc_start"))


def _helper_alive(record: dict) -> bool:
    return _alive(record.get("helper_pid"), record.get("helper_start"))
_shared_warned: set[str] = set()


# -- the registry: who is watching which folder on this host ---------------------------
def _registry() -> Path:
    # Per host: on an HPC cluster HOME (and with it this directory) is shared
    # by every node, and only this host's records mean anything here.
    host = "".join(c if c.isalnum() or c in "-._" else "_" for c in socket.gethostname()) or "host"
    return _private_dir("capture", "active", host)


def _entries() -> list[tuple[Path, dict]]:
    found = []
    for path in _registry().glob("*.json"):
        try:
            record = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(record, dict):
            found.append((path, record))
    return found


#: The key of a window's registry record holding rules OTHER processes of the
#: run handed it (`share_ignore`), and how many it keeps.
SHARED_IGNORE_KEY = "ignore_shared"
MAX_SHARED_IGNORE = 16


def share_ignore(run_id: str, rules: Any) -> int:
    """Hand ``rules`` -- this process's ``.probeignore`` rules, with its own
    ``ignore=`` patterns -- to the windows of the SAME run that other
    processes on this host sweep (plan (n), #2045 review): a ``probe exec``
    launcher sweeps its child's folder after the child exits, with the rules
    it loaded before the child started. The registry record is the channel
    those windows already share (``shared_with`` travels the same way), and
    :meth:`OutputCapture._sweep` re-reads it. Returns how many windows took
    them; never raises."""
    try:
        record = _ignore.to_record(rules)
        if record is None:
            return 0
        from ....foundation.durable.durable import file_lock

        registry = _registry()
        taken = 0
        with file_lock(registry / ".lock"):
            for path, other in _entries():
                if other.get("run_id") != run_id or other.get("pid") == os.getpid():
                    continue
                if other.get("sweeps") is False or not _record_alive(other):
                    continue
                shared = other.setdefault(SHARED_IGNORE_KEY, [])
                if not isinstance(shared, list):
                    continue
                if record not in shared and len(shared) < MAX_SHARED_IGNORE:
                    shared.append(record)
                    _write_json(path, other)
                taken += 1
        return taken
    except Exception:  # noqa: BLE001 -- filtering is never a reason to fail init
        return 0


@contextlib.contextmanager
def _ledger_lock(run_id: str, deadline: float):
    """One sweep of a run at a time on this host, so a rank closing beside
    another sees what that one queued instead of queuing it again. Waiting
    ends at the caller's deadline: dedupe is worth time, not the close."""
    try:
        handle = open(_private_dir("outputs") / f"{run_id}.lock", "a+")
    except OSError:
        yield
        return
    with handle:
        held = False
        while True:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                held = True
                break
            except OSError:
                if time.monotonic() >= deadline:
                    break
                time.sleep(0.05)
        try:
            yield
        finally:
            if held:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)


class CaptureRegistryMixin:
    """Part of OutputCapture: its methods run with `self` the OutputCapture; compose() folds them into OutputCapture."""

    def _register(self) -> None:
        """Record this window on the host: overlap detection, and what a
        recovery needs if the process dies without closing it."""
        from ....foundation.durable.durable import file_lock

        registry = _registry()
        _prune(registry)
        self._entry = self._entry or registry / f"{self._key}.json"
        shared: list[str] = []
        with file_lock(registry / ".lock"):
            for path, other in _entries():
                if path == self._entry or not _record_alive(other):
                    continue
                if not _overlap(self.root, str(other.get("root") or "")):
                    continue
                if other.get("run_id") == self.run_id:
                    # Another process of THIS run (a rank): both sweep -- this
                    # one may write after that one closes -- and the ledger
                    # keeps them from queuing a file twice. The log is per
                    # process, so it needs a name of its own.
                    if self.log_name == LOG_NAME:
                        self.log_name = f"probe/run.{self.pid}.log"
                    continue
                if not self.sweeps or other.get("sweeps") is False:
                    continue  # a log-only window claims no files
                shared.append(str(other.get("run_id")))
                mates = other.setdefault("shared_with", [])
                if isinstance(mates, list) and self.run_id not in mates:
                    mates.append(self.run_id)
                    _write_json(path, other)
            if self.sweeps:
                baselines = _private_dir("capture", "baselines")
                _prune(baselines)
                self._baseline_file = baselines / f"{self._key}.json"
                _write_json(self._baseline_file, self.baseline)
            _write_json(self._entry, self._record(shared_with=shared))

    def _record(self, *, shared_with: list[str]) -> dict:
        context = getattr(self.journal, "context", None) or {}
        return {
            "run_id": self.run_id,
            "pid": self.pid,
            "proc_start": _process_started(self.pid),
            "host": self.host,
            "root": self.root,
            "started_at": self.started_at,
            "launcher": self.launcher,
            "sweeps": self.sweeps,
            "baseline": str(self._baseline_file) if self._baseline_file else None,
            "log_path": self._log_path,
            "log_name": self.log_name,
            "helper_pid": self._helper_pid,
            "helper_start": _process_started(self._helper_pid) if self._helper_pid else None,
            "journal_dir": str(getattr(self.journal, "dir", "") or ""),
            "context": {
                "name": context.get("name"),
                "base_url": context.get("base_url"),
                # Which credential the run wrote with (#2035), so the log a
                # recovery queues is delivered as the run, not as the machine.
                **({"principal": context["principal"]} if context.get("principal") else {}),
            },
            "shared_with": shared_with,
            # A recovery in a fresh interpreter excludes what this run did.
            "ignore": _ignore.to_record(self.ignore),
            "writer": self.writer or None,
        }

    def _rewrite_record(self, **fields: Any) -> None:
        if self._entry is None:
            return
        try:
            from ....foundation.durable.durable import file_lock

            # Under the registry's lock: another process may be adding to
            # this record (`shared_with`, `share_ignore`) at the same moment.
            with file_lock(self._entry.parent / ".lock"):
                record = json.loads(self._entry.read_text())
                record.update(fields)
                _write_json(self._entry, record)
        except (OSError, ValueError, AttributeError, ImportError):
            pass

    def _sweep_ignore(self) -> Any:
        """This window's rules plus those other processes of the run handed
        it in its record (`share_ignore`): a ``probe exec`` child's own
        ``ignore=``. Re-read at the sweep, as ``shared_with`` is; a recovery
        reads the same record."""
        extra = []
        if self._entry is not None:
            try:
                shared = json.loads(self._entry.read_text()).get(SHARED_IGNORE_KEY) or []
                if isinstance(shared, list):
                    extra = [_ignore.from_record(r) for r in shared[:MAX_SHARED_IGNORE]]
            except (OSError, ValueError, AttributeError):
                pass
        return _ignore.combine(self.ignore, *extra)

    def note_helper(self, pid: int) -> None:
        self._helper_pid = pid
        self._rewrite_record(helper_pid=pid, helper_start=_process_started(pid))

    def _is_rival(self, path: Path, other: dict) -> bool:
        """Another run, alive, sweeping a folder that overlaps this one."""
        return (
            path != self._entry
            and other.get("run_id") != self.run_id
            and other.get("sweeps") is not False
            and _record_alive(other)
            and _overlap(self.root, str(other.get("root") or ""))
        )

    def _shared_with(self) -> list[str]:
        """Runs that watched an overlapping folder on this host while this one
        was open: marked at either run's start, or still alive now."""
        shared: set[str] = set()
        if self._entry is not None:
            try:
                mates = json.loads(self._entry.read_text()).get("shared_with") or []
                if isinstance(mates, list):
                    shared.update(str(m) for m in mates)
            except (OSError, ValueError, AttributeError):
                pass
        for path, other in _entries():
            if self._is_rival(path, other):
                shared.add(str(other.get("run_id")))
        return sorted(shared)

    def _unregister(self) -> None:
        markers = (
            list(self._entry.parent.glob(f"{self._entry.name}.writer-*"))
            if self._entry is not None
            else []
        )
        for path in (self._entry, self._baseline_file, *markers):
            if path is not None:
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass


def _warn_shared(run_id: str, others: list[str], root: str) -> None:
    if run_id in _shared_warned:
        return
    _shared_warned.add(run_id)
    _diagnostics.warn(
        f"probe: run {run_id} and {', '.join(others)} wrote to {root} at the same time, so "
        "their output files cannot be told apart; output capture skipped them (logs are "
        "still saved). Give each run its own folder with probe.init(outputs=...)."
    )
from probe.sdk.capture.outputs.log import LOG_NAME, _private_dir, _prune  # noqa: E402 -- pieces need each other; the front door loads this one first
