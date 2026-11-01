"""CredentialHolders: which processes hold an env or in-code credential with queued writes, and whether they still run."""

from __future__ import annotations
import os
import time
from probe.foundation.compat.compat import StrEnum
from pathlib import Path
from .....foundation.durable.durable import now_iso


#: Credentials `record_holder` keeps, and live holders per credential.
_HOLDERS_KEPT = 256
_HOLDERS_PER_CREDENTIAL = 8
#: A holder recorded on ANOTHER host (a home folder shared over NFS) cannot be looked up
#: from here: it counts as possibly alive this long after its last renewal
#: (`_HOLDER_RENEW_SECONDS`).
_OTHER_HOST_HOLDER_SECONDS = 24 * 3600.0
_HOLDER_RENEW_SECONDS = 3600.0


def _older_than(at, seconds: float) -> bool:
    from datetime import datetime, timezone

    try:
        when = datetime.fromisoformat(str(at or ""))
    except ValueError:
        return True
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - when).total_seconds() > seconds


def _holders_path() -> Path:
    """Which processes queued writes with an env or in-code credential:
    `<state>/probe/credential-holders.json`, so `probe outbox status` can say who holds a
    credential whose writes wait (restart it, or adopt them) and the rescue never takes a
    credential a live process still holds. A pid, its start time, the host, the SDK version
    and two basenames: never argv."""
    return _accounts_path().with_name("credential-holders.json")


class HolderState(StrEnum):
    """Whether a recorded holder process still runs (`holder_state`)."""

    #: The pid runs and started when the record says: the same process.
    ALIVE = "alive"
    #: No such pid, or one that started at another time (a reused pid).
    GONE = "gone"
    #: Cannot tell: no start time recorded or readable, or another host's.
    UNKNOWN = "unknown"


def _process_started(pid: int) -> float | None:
    """When ``pid`` started (seconds since the epoch), or None. A pid alone is reused; pid +
    start is one process."""
    try:
        import psutil

        return float(psutil.Process(pid).create_time())
    except Exception:  # noqa: BLE001
        return None


def _this_host() -> str:
    import socket

    try:
        return socket.gethostname()
    except OSError:
        return ""


def holder_state(holder: dict) -> HolderState:
    """Total over any input: the record is a file anything can damage."""
    try:
        pid = int(holder.get("pid") or 0)
    except (TypeError, ValueError, AttributeError):
        return HolderState.UNKNOWN
    if pid <= 0:
        return HolderState.UNKNOWN
    host = holder.get("host")
    if host and host != _this_host():
        return HolderState.UNKNOWN  # its pids are another machine's
    try:
        import psutil
    except ImportError:
        return HolderState.UNKNOWN
    try:
        process = psutil.Process(pid)
        if process.status() == psutil.STATUS_ZOMBIE:
            return HolderState.GONE
        started = process.create_time()
    except psutil.NoSuchProcess:  # ZombieProcess included
        return HolderState.GONE
    except Exception:  # noqa: BLE001 -- access denied and the like
        return HolderState.UNKNOWN
    recorded = holder.get("started")
    if not isinstance(recorded, (int, float)):
        return HolderState.UNKNOWN
    return HolderState.ALIVE if abs(started - recorded) <= 1.0 else HolderState.GONE


def _holder_may_live(holder: dict) -> bool:
    """Whether ``holder`` may still be running: alive here, or recorded on another host within
    `_OTHER_HOST_HOLDER_SECONDS`."""
    from datetime import datetime, timezone

    state = holder_state(holder)
    if state == HolderState.ALIVE:
        return True
    if state == HolderState.GONE:
        return False
    if not holder.get("host") or holder.get("host") == _this_host():
        return True  # here, but unreadable: it may be running
    try:
        at = datetime.fromisoformat(str(holder.get("at") or ""))
    except ValueError:
        return False
    if at.tzinfo is None:
        at = at.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - at).total_seconds() < _OTHER_HOST_HOLDER_SECONDS


def record_holder(fingerprint: str | None) -> None:
    """Remember that THIS process holds the credential ``fingerprint`` and queues writes with
    it. Holders found gone are dropped as one is added. Skipped when another process is
    writing the record. Never raises: evidence for `probe outbox status` and the rescue, not
    a delivery step."""
    if not fingerprint:
        return
    import sys

    try:
        import probe

        version = str(getattr(probe, "__version__", "") or "")
    except Exception:  # noqa: BLE001
        version = ""
    pid = os.getpid()
    entry = {
        "pid": pid,
        "started": _process_started(pid),
        "host": _this_host(),
        "sdk": version,
        "program": os.path.basename(sys.executable or ""),
        "script": os.path.basename(sys.argv[0]) if sys.argv and sys.argv[0] else "",
        "at": now_iso(),
    }

    def change(records: dict) -> bool:
        current = records.get(fingerprint)
        holders = current.get("holders") if isinstance(current, dict) else None
        same = [
            h
            for h in (holders if isinstance(holders, list) else [])
            if isinstance(h, dict) and h.get("pid") == pid and h.get("started") == entry["started"]
        ]
        if same and not _older_than(same[0].get("at"), _HOLDER_RENEW_SECONDS):
            return False  # this process again (a sweep's next `probe.init()`)
        kept = [
            h
            for h in (holders if isinstance(holders, list) else [])
            if isinstance(h, dict) and h.get("pid") != pid and holder_state(h) != HolderState.GONE
        ]
        kept.append(entry)
        records[fingerprint] = {"at": entry["at"], "holders": kept[-_HOLDERS_PER_CREDENTIAL:]}
        return True

    for _attempt in range(3):  # ranks starting together: a short wait, never a queue
        try:
            if _update_records(_holders_path(), change, kept=_HOLDERS_KEPT, wait=False):
                return
        except Exception:  # noqa: BLE001 -- see docstring
            return
        time.sleep(0.02)


def credential_holders(fingerprint: str | None) -> list[dict]:
    """The processes recorded holding ``fingerprint``, newest last, each with its ``state``
    (`HolderState`). Empty when none was recorded (every process of a release before this
    record included)."""
    if not fingerprint:
        return []
    current = _read_records(_holders_path()).get(fingerprint)
    holders = current.get("holders") if isinstance(current, dict) else None
    return [
        {**h, "state": holder_state(h).value}
        for h in (holders if isinstance(holders, list) else [])
        if isinstance(h, dict)
    ]
from probe.sdk.delivery.outbox.drain.accounts import _accounts_path, _read_records, _update_records  # noqa: E402 -- pieces need each other; the front door loads this one first
