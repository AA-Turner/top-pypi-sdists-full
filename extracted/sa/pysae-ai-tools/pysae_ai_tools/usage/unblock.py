"""Block-state override for the usage hook (account-wide — scoped to the Claude plan window).

"Session"/"window" means the Claude **plan** window (5H / weekly), not the Claude-Code
session, so the override is global. It overlays the hook's automatic ``--block-at``
threshold with one of three states:

- ``"unblock"`` — blocking suspended. Set by "débloque l'extra usage pour cette session".
- ``"block"`` — blocking forced on. Set by "bloque la session".
- ``None`` — follow the automatic threshold.

The override is bound to the **current window**, identified by its ``resets_at`` (the API
exposes no explicit id; ``resets_at`` is unique per window and changes when usage falls
back to 0%). It is active while the live window id matches *or* a time fallback ``until``
hasn't passed — so it clears automatically when the window resets. API-key mode has no
window, so it uses ``until`` alone.

State file: ``{"mode": "block"|"unblock", "window": "<resets_at iso>", "until": <epoch>}``.
"""

import json
from datetime import datetime

from . import account

OVERRIDE_PATH = account.active_state_dir() / "usage-unblock.json"


def _read() -> dict[str, object]:
    try:
        data = json.loads(OVERRIDE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _write(mode: str, window: str, until: float) -> None:
    account.ensure_dir(OVERRIDE_PATH.parent)
    OVERRIDE_PATH.write_text(
        json.dumps({"mode": mode, "window": window, "until": until}, ensure_ascii=False),
        encoding="utf-8",
    )


def set_unblock(window: str = "", until: float = 0.0) -> None:
    """Suspend blocking for the current window (``window`` = its resets_at id) / until ``until``."""
    _write("unblock", window, until)


def set_block(window: str = "", until: float = 0.0) -> None:
    """Force blocking on for the current window / until ``until``."""
    _write("block", window, until)


def clear() -> None:
    """Return to automatic threshold behaviour."""
    try:
        OVERRIDE_PATH.unlink()
    except OSError:
        pass


def state(now: float, current_window: str = "") -> str | None:
    """Effective override (``"block"``/``"unblock"``/None), given the live window id.

    Active while the stored window id still matches the live one, or the ``until``
    fallback hasn't elapsed. A new window (different id) with a past ``until`` = auto.
    """
    data = _read()
    mode = data.get("mode")
    if not isinstance(mode, str) or mode not in ("block", "unblock"):
        return None
    window = data.get("window")
    until = data.get("until")
    if current_window and window == current_window:
        return mode
    if isinstance(until, (int, float)) and until > now:
        return mode
    return None


def active_until(now: float) -> float | None:
    """The override's time fallback if still in the future (for display), else None."""
    until = _read().get("until")
    return float(until) if isinstance(until, (int, float)) and until > now else None


def parse_until(value: str) -> float | None:
    """Parse an ISO-8601 instant into an epoch, or None if invalid."""
    try:
        return datetime.fromisoformat(value).timestamp()
    except ValueError:
        return None
