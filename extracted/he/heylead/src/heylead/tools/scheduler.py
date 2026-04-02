"""Tool: scheduler — View scheduler status or toggle on/off.

Thin dispatcher that routes to existing run_* functions based on the action parameter.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def run_scheduler(
    action: str = "status",
    enabled: bool = True,
    cloud: bool = False,
    hours: int = 24,
    event_type: str = "",
    campaign_id: str = "",
) -> str:
    """Manage the autonomous scheduler.

    Actions:
      status      — Show scheduler status, pending jobs, and recent activity
      toggle      — Enable or disable the scheduler
      always_on   — Enable/disable always-on mode (auto-re-enable + immediate alerts)
      logs        — Event log with metrics and recent failures
      activity    — Real action results from DB: what happened, what didn't, and why
      diagnostics — Full system diagnostics: rate limits, timers, blockers
      report      — Configure periodic email campaign reports

    Args:
        action: What to do: 'status', 'toggle', 'logs', 'diagnostics', or 'report'.
        enabled: True to enable, False to disable (for 'toggle').
            For 'report': True to enable email reports, False to disable.
        cloud: If True, toggle the cloud scheduler for 24/7 operation (for 'toggle').
        hours: Lookback window in hours for 'logs' (default 24).
            For 'report': report interval in hours (1, 2, 4, 8, or 24).
        event_type: Filter events by type for 'logs'.
            For 'report': recipient email (empty = use login email).
        campaign_id: Filter by campaign for 'logs' and 'diagnostics'.
    """
    action = action.lower().strip()

    if action == "status":
        from .scheduler_status import run_scheduler_status
        return await run_scheduler_status()

    if action == "toggle":
        from .scheduler_status import run_toggle_scheduler
        return await run_toggle_scheduler(enabled=enabled, cloud=cloud)

    if action == "logs":
        from .scheduler_status import run_scheduler_logs
        return await run_scheduler_logs(
            hours=hours, event_type=event_type, campaign_id=campaign_id,
        )

    if action == "diagnostics":
        from .scheduler_status import run_scheduler_diagnostics
        return await run_scheduler_diagnostics(campaign_id=campaign_id)

    if action == "activity":
        from .scheduler_status import run_scheduler_activity
        return await run_scheduler_activity(hours=hours, campaign_id=campaign_id)

    if action == "always_on":
        from .scheduler_status import run_toggle_always_on
        return await run_toggle_always_on(enabled=enabled)

    if action == "report":
        return await _run_report_settings(
            enabled=enabled, interval_hours=hours, report_email=event_type,
        )

    return (
        f"Unknown action: '{action}'. "
        f"Use 'status', 'toggle', 'always_on', 'logs', 'activity', 'diagnostics', or 'report'."
    )


async def _run_report_settings(
    enabled: bool = True,
    interval_hours: int = 1,
    report_email: str = "",
) -> str:
    """Configure periodic email campaign report via backend API."""
    from ..config import is_backend_mode

    if not is_backend_mode():
        return (
            "Email reports require backend mode (cloud scheduler).\n"
            "Run `setup_profile` to connect to the backend first."
        )

    import httpx
    from ..services.cloud_sync import _base_url, _headers

    base = _base_url()

    # Build update payload — only include explicitly set values
    body: dict = {"report_enabled": enabled}
    if interval_hours != 24:  # 24 is the default for 'hours' param
        body["report_interval_hours"] = interval_hours
    if report_email:
        body["report_email"] = report_email

    async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
        try:
            resp = await client.post(
                f"{base}/api/v1/scheduler/report-settings",
                json=body,
                headers=_headers(),
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            return f"Failed to update report settings: {e.response.status_code}"
        except httpx.HTTPError as e:
            return f"Failed to reach backend: {e}"

    status = "enabled" if data.get("report_enabled") else "disabled"
    interval = data.get("report_interval_hours", 1)
    email = data.get("report_email", "") or "(login email)"

    lines = [
        f"# Email Report {status.upper()}",
        "",
        f"- Status: **{status}**",
        f"- Interval: every **{interval}h**",
        f"- Recipient: **{email}**",
        "",
    ]

    if data.get("report_enabled"):
        lines.append(
            "The next report will be sent on the next scheduler tick "
            "(within ~5 minutes)."
        )
        lines.append("")
        lines.append("The report includes:")
        lines.append("- Campaign metrics (invitations, engagements, follow-ups, replies)")
        lines.append("- Issue detection (why campaigns may be idle)")
        lines.append("- Copy-pasteable fix commands for Claude Code")
    else:
        lines.append("No more reports will be sent until re-enabled.")

    return "\n".join(lines)
