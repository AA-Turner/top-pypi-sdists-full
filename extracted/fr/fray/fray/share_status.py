"""Utility helpers for computing share expiry status labels.

These helpers are shared between the guided pipeline, dashboard, and report builder
so that expiry warnings remain consistent everywhere.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

_WARN_WINDOW = timedelta(days=3)


def _parse_iso8601(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    value = ts.strip()
    if not value:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _format_delta(delta: timedelta) -> str:
    seconds = int(abs(delta.total_seconds()))
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    if days:
        return f"{days}d {hours}h".strip()
    if hours:
        return f"{hours}h {minutes}m".strip()
    if minutes:
        return f"{minutes}m"
    return f"{max(seconds, 0)}s"


def share_status(expires_at: Optional[str], *, now: Optional[datetime] = None,
                 warn_window: timedelta = _WARN_WINDOW) -> Dict[str, str]:
    """Return a {'label', 'state'} dict describing expiry timing.

    States:
        - unknown: no expiry metadata is available
        - expired: expiry timestamp is in the past
        - warn: expiry is within the configured warning window (default: 3 days)
        - ok: expiry is farther away than the warning window
    """
    dt = _parse_iso8601(expires_at)
    if not dt:
        return {"label": "expiry unknown", "state": "unknown"}

    now_dt = now or datetime.now(timezone.utc)
    diff = dt - now_dt
    label_delta = _format_delta(diff)
    if diff.total_seconds() < 0:
        return {"label": f"expired {label_delta} ago", "state": "expired"}
    if diff <= warn_window:
        return {"label": f"expires in {label_delta}", "state": "warn"}
    return {"label": f"expires in {label_delta}", "state": "ok"}
