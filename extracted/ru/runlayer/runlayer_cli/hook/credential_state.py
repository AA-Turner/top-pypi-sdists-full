"""Device-local record of the last Runlayer credential rejection (HTTP 401).

Written by the relay on a 401; read by Monitor-mode dispatch to skip
re-verification for a few minutes and to show one user notice an hour.
Enforce never reads it: a fail-closed hook re-verifies every call so a
re-minted key recovers at once. Best-effort throughout: any read or write
failure degrades to "no record", never to a hook error. Concurrent hooks
(inline processes, daemon threads) are last-writer-wins on the record —
every writer is recording the same fact. Stdlib-only (hook closure).
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from runlayer_cli.paths import get_runlayer_dir

# Only 401 is a credential answer from the API itself; a 403 can come from a
# corporate proxy or WAF on the path, per request, and must not arm anything.
CREDENTIAL_REJECTED_STATUS = 401

# Monitor-only negative cache. Hooks fire on every tool call and prompt (dozens
# a minute under an agent), while the managed check-in that would pick up a
# re-minted key runs every 15 minutes: five minutes stops a Monitor device from
# hammering the API with doomed calls yet notices a fixed key well inside one
# check-in interval.
NEGATIVE_CACHE_TTL_S = 300.0
# One user-visible notice per device per hour: enough to explain the gap in
# monitoring, not enough to nag on every tool call.
NOTICE_INTERVAL_S = 3600.0

_STATE_FILENAME = "credential_rejected.json"

# Serializes read-modify-write within one process (the daemon runs hooks on
# threads of a single pid); the temp-file + replace handles other processes.
_lock = threading.Lock()


@dataclass(frozen=True, slots=True)
class CredentialRejection:
    at: float
    status: int
    # Which credential was rejected, so a re-minted key or host repoint is
    # never answered from the cache.
    fingerprint: str


def credential_fingerprint(host: str, secret: str) -> str:
    return hashlib.sha256(f"{host}{secret}".encode()).hexdigest()[:16]


def _state_dir() -> Path:
    return get_runlayer_dir() / "state"


def read_rejection() -> CredentialRejection | None:
    """Last recorded rejection, or ``None`` when absent or unreadable."""
    try:
        raw = json.loads((_state_dir() / _STATE_FILENAME).read_text(encoding="utf-8"))
        rejection = CredentialRejection(
            at=float(raw["at"]),
            status=int(raw["status"]),
            fingerprint=str(raw["fingerprint"]),
        )
    except Exception:
        return None
    return rejection


def _is_fresh(rejection: CredentialRejection, now: float) -> bool:
    return 0 <= now - rejection.at < NEGATIVE_CACHE_TTL_S


def record_rejection(status: int, fingerprint: str) -> None:
    """Persist the rejection unless an equivalent record is still fresh, so an
    Enforce device paying a deny per tool call costs one read, not a write."""
    with _lock:
        now = time.time()
        current = read_rejection()
        if (
            current is not None
            and current.status == status
            and current.fingerprint == fingerprint
            and _is_fresh(current, now)
        ):
            return
        _write({"at": now, "status": status, "fingerprint": fingerprint})


def recent_rejection(fingerprint: str) -> CredentialRejection | None:
    """The fresh rejection for exactly this credential, else ``None``."""
    rejection = read_rejection()
    if rejection is None or rejection.fingerprint != fingerprint:
        return None
    if not _is_fresh(rejection, time.time()):
        return None
    return rejection


def claim_notice(kind: str = "credential") -> bool:
    """Reserve this hour's user notice of ``kind``; ``True`` for exactly one caller.

    An ``O_EXCL`` marker per hour bucket is atomic across processes and
    threads, which a field in the JSON record could not be. Each ``kind``
    (credential rejection, hook host override, ...) has its own hourly budget.
    """
    bucket = int(time.time() // NOTICE_INTERVAL_S)
    prefix = f"{kind}_notice."
    state_dir = _state_dir()
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        fd = os.open(
            state_dir / f"{prefix}{bucket}",
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        os.close(fd)
    except Exception:
        return False
    _prune_notice_markers(state_dir, prefix=prefix, keep_bucket=bucket)
    return True


def _prune_notice_markers(state_dir: Path, *, prefix: str, keep_bucket: int) -> None:
    keep = f"{prefix}{keep_bucket}"
    with contextlib.suppress(Exception):
        for entry in os.scandir(state_dir):
            if entry.name.startswith(prefix) and entry.name != keep:
                with contextlib.suppress(Exception):
                    os.unlink(entry.path)


def _write(record: dict[str, object]) -> None:
    """Unique temp file + atomic replace, so a concurrent reader never sees a
    torn record and parallel writers never share a temp path."""
    state_dir = _state_dir()
    path = state_dir / _STATE_FILENAME
    tmp_path: str | None = None
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=state_dir, prefix=f"{path.name}.")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(record))
        os.replace(tmp_path, path)
    except Exception:
        if tmp_path is not None:
            with contextlib.suppress(Exception):
                os.unlink(tmp_path)
