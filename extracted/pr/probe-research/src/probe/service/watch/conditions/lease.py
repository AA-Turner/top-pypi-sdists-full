"""family worker: a live session's daemon lease failing or stalled."""

from __future__ import annotations
from pathlib import Path
from probe.service.watch.files import read_json
from probe.service.watch.settings import LEASE_FAILURES, LEASE_GRACE_S


def lease_condition(state_dir: str, sid: str, now: float) -> tuple[str, dict] | None:
    """A failing daemon lease (`<state>/sessions/<sid>.writer`, the tap's and the
    worker's format), as `(condition, facts)`: `lease_<reason>` when released
    with a failure's reason, `hung` / `not_running` when it expired past
    LEASE_GRACE_S with the worker lock still held / not. None otherwise (no
    lease, a healthy one, a stop on purpose). Blocking: a thread."""
    data = read_json(Path(state_dir) / "sessions" / f"{sid}.writer", limit=64 * 1024)
    if not isinstance(data, dict) or data.get("writer") != "daemon":
        return None
    reason, expires = data.get("reason"), data.get("expires_at")
    if reason in LEASE_FAILURES and not (reason == "gateway" and data.get("offline") is True):
        return f"lease_{reason}", {"lease_reason": reason, "released_at": data.get("renewed_at")}
    if reason is None and isinstance(expires, (int, float)) and now - expires > LEASE_GRACE_S:
        try:
            from ...sessions.workers import lock_held, safe_sid

            held = lock_held(Path(state_dir) / "daemon" / f"{safe_sid(sid)}.lock")
        except Exception:  # noqa: BLE001 -- no flock here (Windows): lapsed, cause unknown
            held = False
        return ("hung" if held else "not_running"), {"expired_s": round(now - expires)}
    return None
