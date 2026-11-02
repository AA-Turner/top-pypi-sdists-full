"""WorkerLease: the lease, caps and stop files that say who drains a queue and which op kinds it takes."""

from __future__ import annotations

import os

from ...._shared import oscompat
from ....foundation.durable import durable


def _lease_path(journal) -> str:
    # The WORKER lease, distinct from the per-pass .drain.lock: held for the worker's whole
    # life so the between-passes gap never looks "free" to maybe_spawn and forks a duplicate.
    return str(journal.dir / ".worker.lock")


# -- queue format versioning (plan 1.11) ------------------------------------
# Each worker advertises the op kinds it delivers (a caps file beside its lease); a newer producer
# asks `ready_for(kind)` and leaves a stop file a live older worker obeys between passes.


def _caps_path(journal):
    return journal.dir / ".worker-caps.json"


def _stop_path(journal):
    return journal.dir / ".worker-stop"


def _write_caps(journal) -> None:
    """Advertise what this worker delivers. Best-effort: without the file a producer assumes
    the oldest caps and asks for a restart (safe)."""
    import json

    from ..ops.ops import OP_KINDS

    try:
        import probe

        version = str(getattr(probe, "__version__", "") or "")
    except Exception:  # noqa: BLE001
        version = ""
    try:
        durable.write_text_atomic(
            _caps_path(journal),
            json.dumps(
                {"schema": 1, "version": version, "kinds": sorted(OP_KINDS), "pid": os.getpid()}
            )
            + "\n",
            mode=0o600,
        )
    except OSError:
        pass


def _drop_caps(journal) -> None:
    """Remove the caps file on the way out, if it is still this worker's."""
    import json

    try:
        caps = json.loads(_caps_path(journal).read_text())
        if caps.get("pid") == os.getpid():
            _caps_path(journal).unlink(missing_ok=True)
    except (OSError, ValueError, AttributeError):
        pass


def _pid_alive(pid: object) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        oscompat.probe_pid(pid)
    except ProcessLookupError:
        return False
    except OSError:
        return True  # exists, not ours to signal
    return True


#: What every worker predating caps files delivers; anything else it dead-letters.
_LEGACY_KINDS = frozenset({"http", "upload", "rejected_http"})


def live_worker_kinds(directory: str | None = None) -> frozenset | None:
    """The op kinds the worker delivering ``directory`` can handle, or None
    when no worker is running (the next kick spawns one of this version)."""
    import json

    from ..journal.journal import Journal

    journal = Journal(directory)
    try:
        journal._ensure()
    except OSError:
        return _LEGACY_KINDS
    if _lease_is_free(journal):
        return None
    try:
        caps = json.loads(_caps_path(journal).read_text())
    except (OSError, ValueError):
        return _LEGACY_KINDS  # a worker that predates caps
    if not isinstance(caps, dict) or not _pid_alive(caps.get("pid")):
        return _LEGACY_KINDS  # a stale file; the lease holder is someone else
    kinds = caps.get("kinds")
    return frozenset(k for k in kinds if isinstance(k, str)) if isinstance(kinds, list) else (
        _LEGACY_KINDS
    )


def ready_for(kind: str, directory: str | None = None) -> bool:
    """Whether an op of ``kind`` may be queued in ``directory`` now: the live worker (if any)
    can deliver it. If not, a stop file asks it to exit after its pass so the next kick
    starts one of this version; the caller waits or uses an older op shape meanwhile."""
    import json

    from ..journal.journal import Journal

    kinds = live_worker_kinds(directory)
    if kinds is None or kind in kinds:
        return True
    journal = Journal(directory)
    try:
        wanted = set()
        try:
            wanted = set(json.loads(_stop_path(journal).read_text()).get("kinds") or ())
        except (OSError, ValueError, AttributeError):
            pass
        durable.write_text_atomic(
            _stop_path(journal),
            json.dumps({"kinds": sorted(wanted | {kind})}) + "\n",
            mode=0o600,
        )
    except OSError:
        pass
    return False


def _asked_to_stop(journal) -> bool:
    """A producer left a stop file (see `ready_for`). Exit only if this worker lacks a kind
    it names; either way the request is consumed so its replacement does not exit on it."""
    import json

    from ..ops.ops import OP_KINDS

    path = _stop_path(journal)
    try:
        raw = path.read_text()
    except OSError:
        return False
    try:
        kinds = set(json.loads(raw).get("kinds") or ())
    except (ValueError, AttributeError):
        kinds = {"?"}  # unreadable: assume we are the old one
    path.unlink(missing_ok=True)
    return not kinds <= OP_KINDS


def _lease_is_free(journal, path: str | None = None) -> bool:
    """Non-blocking probe of the worker lease (or another lease `path`). True
    when nobody holds it. The journal directory is known to exist."""
    try:
        handle = open(path or _lease_path(journal), "a+")
    except OSError:
        return False
    try:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        return True
    except BlockingIOError:
        return False
    finally:
        handle.close()


def worker_holder(queue) -> "tuple[object, str] | None":
    """(pid, release) of the live worker holding ``queue``'s lease, from its
    caps file, or None when the lease is free."""
    import json

    if _lease_is_free(queue):
        return None
    try:
        caps = json.loads(_caps_path(queue).read_text())
    except (OSError, ValueError):
        caps = {}
    return caps.get("pid"), str(caps.get("version") or "")
