"""
cvc.dashboard.routes — Dashboard API router.

Re-exports the gateway API endpoints for modular use.
The primary API endpoints live directly in ``cvc.gateway`` since the
gateway FastAPI app owns the lifespan and singletons.

This module provides utility functions used by both the gateway
and any future dashboard extensions.
"""

from __future__ import annotations

import time
from typing import Any


def format_uptime(seconds: float) -> str:
    """Format seconds into a human-readable uptime string."""
    if seconds <= 0:
        return "-"
    if seconds < 60:
        return f"{int(seconds)}s"
    if seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    return f"{hrs}h {mins}m"


def format_timestamp(ts: float | None) -> str:
    """Format a UNIX timestamp to ISO 8601 string."""
    if not ts:
        return "-"
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def build_service_summary(services: dict[str, Any]) -> list[dict[str, Any]]:
    """Build a summary list from raw service records for the dashboard."""
    summary = []
    status_icons = {
        "running": "green",
        "stopped": "red",
        "starting": "yellow",
        "paused": "orange",
        "error": "red",
        "unknown": "gray",
    }
    for name, svc in services.items():
        if isinstance(svc, dict):
            status = svc.get("status", "unknown")
            started_at = svc.get("started_at")
        else:
            status = getattr(svc, "status", "unknown")
            started_at = getattr(svc, "started_at", None)

        uptime = 0.0
        if started_at and status == "running":
            uptime = time.time() - started_at

        summary.append({
            "name": name,
            "display_name": name.upper() if name != "sdk" else "SDK",
            "status": status,
            "color": status_icons.get(status, "gray"),
            "uptime": format_uptime(uptime),
            "started_at": format_timestamp(started_at),
        })
    return summary
