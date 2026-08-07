"""When the registry credential was last checked, rotated, and swept for rotation.

Rotation runs unattended — a detached process on an hourly tick — so without a
record of it there is nothing to show the user: the credential simply changes
under them. This module is that record, and it is also what throttles the tick
(``last_swept_at``), so no second cache file is needed for it.

Three distinct instants, deliberately:

- ``checked_at`` — GitLab last answered about the token's validity.
- ``rotated_at`` — the token was last replaced.
- ``last_swept_at`` — the rotation pass last *ran*, whether or not it had a
  token to check. Throttling on the check instant instead would respawn the
  sweep on every command for a developer who has no credential at all.

Timestamps are UTC. Never holds the token itself.
"""

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ...config import CACHE_DIR
from ..fs import atomic_write_text

JOURNAL_FILE = CACHE_DIR / "registry-credential.json"

_CHECKED = "checked_at"
_ROTATED = "rotated_at"
_SWEPT = "last_swept_at"


@dataclass(frozen=True)
class Journal:
    """The recorded instants, all ``None`` on a machine that never ran a pass."""

    checked_at: datetime | None = None
    rotated_at: datetime | None = None
    last_swept_at: datetime | None = None


def age_seconds(instant: datetime | None, now: datetime | None = None) -> float | None:
    """Seconds elapsed since ``instant``, or ``None`` when it never happened."""
    if instant is None:
        return None
    return ((now or datetime.now(UTC)) - instant).total_seconds()


def _path() -> Path:
    return JOURNAL_FILE


def _parse(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    # A journal hand-edited (or written by an older build) may carry a naive
    # timestamp; treating it as UTC keeps every comparison timezone-aware.
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def read() -> Journal:
    """The recorded instants. An unreadable or absent journal reads as empty."""
    try:
        data = json.loads(_path().read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return Journal()
    if not isinstance(data, dict):
        return Journal()
    return Journal(
        checked_at=_parse(data.get(_CHECKED)),
        rotated_at=_parse(data.get(_ROTATED)),
        last_swept_at=_parse(data.get(_SWEPT)),
    )


def _record(**instants: datetime) -> None:
    """Merge ``instants`` into the journal. Best-effort: never raises.

    Read-modify-write, deliberately unlocked. The hourly detached pass and a
    foreground command can interleave, and the later writer then keeps the
    instant the other had just recorded at its previous value. Both outcomes are
    bounded: a display timestamp reads older than it is, or a lost
    ``last_swept_at`` costs one extra pass. Neither can cause a double rotation —
    that is governed by the token's expiry threshold, read from GitLab, not from
    here — so a lock file (as ``version_check`` uses to serialise actual updates)
    would buy nothing.
    """
    current = read()
    payload = {
        _CHECKED: current.checked_at,
        _ROTATED: current.rotated_at,
        _SWEPT: current.last_swept_at,
    }
    payload.update(instants)
    try:
        path = _path()
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(path, json.dumps({k: v.isoformat() for k, v in payload.items() if v is not None}))
    except OSError:
        pass


def record_check(now: datetime | None = None) -> None:
    """Note that GitLab just answered about the token's validity."""
    _record(**{_CHECKED: now or datetime.now(UTC)})


def record_rotation(now: datetime | None = None) -> None:
    """Note that the token was just replaced — a check, by construction, too."""
    instant = now or datetime.now(UTC)
    _record(**{_ROTATED: instant, _CHECKED: instant})


def record_sweep(now: datetime | None = None) -> None:
    """Note that the rotation pass ran, whatever it found."""
    _record(**{_SWEPT: now or datetime.now(UTC)})


def clear() -> None:
    """Forget every recorded instant (uninstall, tests)."""
    try:
        _path().unlink(missing_ok=True)
    except OSError:
        pass
