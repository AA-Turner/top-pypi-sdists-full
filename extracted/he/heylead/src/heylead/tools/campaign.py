"""Tool: campaign — Control campaign lifecycle (pause, resume, archive, delete, etc.).

Thin dispatcher that routes to existing run_* functions based on the action parameter.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def run_campaign(
    action: str,
    campaign_id: str = "",
    confirm: bool = False,
) -> str:
    """Control campaign lifecycle.

    Actions:
      pause          — Pause an active campaign
      resume         — Resume a paused campaign
      archive        — Archive a completed campaign
      delete         — Permanently delete a campaign (requires confirm=True)
      emergency_stop — Immediately pause ALL active campaigns
      retry_failed   — Reset error outreaches to pending

    Args:
        action: What to do: 'pause', 'resume', 'archive', 'delete', 'emergency_stop', 'retry_failed'.
        campaign_id: Which campaign to act on. Auto-selects if empty.
        confirm: Must be True for delete action. Safety guard.
    """
    action = action.lower().strip()

    if action == "pause":
        from .campaign_control import run_pause_campaign
        return await run_pause_campaign(campaign_id)

    if action == "resume":
        from .campaign_control import run_resume_campaign
        return await run_resume_campaign(campaign_id)

    if action == "archive":
        from .archive_campaign import run_archive_campaign
        return await run_archive_campaign(campaign_id)

    if action == "delete":
        from .delete_campaign import run_delete_campaign
        return await run_delete_campaign(campaign_id, confirm)

    if action == "emergency_stop":
        from .emergency_stop import run_emergency_stop
        return await run_emergency_stop()

    if action in ("retry_failed", "retry"):
        from .retry_failed import run_retry_failed
        return await run_retry_failed(campaign_id)

    if action in ("status_history", "history", "audit"):
        return await _format_status_history(campaign_id)

    return (
        f"Unknown action: '{action}'. Available actions:\n"
        "  'pause'          — Pause an active campaign\n"
        "  'resume'         — Resume a paused campaign\n"
        "  'archive'        — Archive a completed campaign\n"
        "  'delete'         — Permanently delete (requires confirm=True)\n"
        "  'emergency_stop' — Pause ALL active campaigns\n"
        "  'retry_failed'   — Reset error outreaches to pending\n"
        "  'status_history' — View campaign status change audit log"
    )


async def _format_status_history(campaign_id: str = "") -> str:
    """Format campaign status change history as a readable table."""
    import time as _time
    from ..db.queries import get_campaign_status_history
    from ..db.async_bridge import run_db

    entries = await run_db(get_campaign_status_history, campaign_id, 30)
    if not entries:
        return "No campaign status changes recorded yet."

    lines = ["# Campaign Status History\n"]
    lines.append("| When | Campaign | Change | By | Reason |")
    lines.append("|------|----------|--------|----|--------|")

    for e in entries:
        ts = e.get("timestamp", 0)
        ago = _time_ago(ts)
        name = e.get("campaign_name", "?")[:30]
        old = e.get("old_status", "?")
        new = e.get("new_status", "?")
        by = e.get("changed_by", "?")
        reason = e.get("reason", "")
        lines.append(f"| {ago} | {name} | {old} → {new} | {by} | {reason} |")

    return "\n".join(lines)


def _time_ago(ts: int) -> str:
    """Human-readable time ago from unix timestamp."""
    import time as _time

    diff = int(_time.time()) - ts
    if diff < 60:
        return "just now"
    if diff < 3600:
        return f"{diff // 60}m ago"
    if diff < 86400:
        return f"{diff // 3600}h ago"
    return f"{diff // 86400}d ago"
