"""Tools for pausing and resuming campaigns.

Provides safety controls to stop outreach when needed
and resume it when ready.
"""

from __future__ import annotations

import json
import logging
import time

from ..db.queries import (
    get_campaign,
    get_setting,
    list_campaigns,
    log_action,
    skip_pending_outreaches,
    update_campaign,
)
from ..db.async_bridge import run_db
from ..services.cloud_sync import sync_campaign_status

logger = logging.getLogger(__name__)


async def run_pause_campaign(campaign_id: str = "") -> str:
    """Pause an active campaign, stopping all outreach.

    If no campaign_id is provided, pauses the first active campaign found.
    """

    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "Setup required before managing campaigns.\n\n"
            "Please run setup_profile first."
        )

    # Find the campaign to pause
    if campaign_id:
        campaign = await run_db(get_campaign, campaign_id)
        if not campaign:
            return f"Campaign not found: {campaign_id}"
    else:
        campaigns = await run_db(list_campaigns, status="active")
        if not campaigns:
            return (
                "No active campaigns to pause.\n\n"
                "Use show_status() to see all campaigns."
            )
        campaign = campaigns[0]
        campaign_id = campaign["id"]

    # Check current status
    status = campaign.get("status", "")
    if status == "paused":
        return (
            f"Campaign '{campaign['name']}' is already paused.\n\n"
            "Use resume_campaign() to resume it."
        )
    if status not in ("active", "draft"):
        return (
            f"Campaign '{campaign['name']}' has status '{status}' and cannot be paused.\n"
            "Only active or draft campaigns can be paused."
        )

    # Pause it, skip pending outreaches, and record pause reason
    skipped = await run_db(skip_pending_outreaches, campaign_id)
    cfg = json.loads(campaign.get("config_json") or "{}")
    cfg["pause_reason"] = "user"
    cfg["paused_at"] = int(time.time())
    await run_db(update_campaign, campaign_id, status="paused", config_json=json.dumps(cfg))

    # Audit log
    await run_db(
        log_action, "campaign_status_change",
        result="paused",
        details={
            "campaign_id": campaign_id,
            "campaign_name": campaign["name"],
            "old_status": status,
            "new_status": "paused",
            "changed_by": "user",
            "reason": "manual_pause",
            "pending_skipped": skipped,
        },
    )

    # Sync to backend so cloud scheduler also stops
    synced = await sync_campaign_status(
        campaign_id, "paused", caller="user", reason="manual_pause",
    )
    logger.info(
        "Paused campaign %s: %s (%d pending skipped, cloud_synced=%s)",
        campaign_id, campaign["name"], skipped, synced,
    )

    cloud_note = ""
    if not synced:
        cloud_note = "\n\n**Warning**: Could not sync to cloud scheduler. Run show_status() to refresh."

    return (
        f"Campaign '{campaign['name']}' is now paused.\n\n"
        f"{skipped} pending outreaches marked as skipped.\n"
        "No invitations or messages will be sent.\n\n"
        f"Use resume_campaign() when you're ready to continue.{cloud_note}"
    )


async def run_resume_campaign(campaign_id: str = "") -> str:
    """Resume a paused campaign, re-enabling outreach.

    If no campaign_id is provided, resumes the first paused campaign found.
    """

    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "Setup required before managing campaigns.\n\n"
            "Please run setup_profile first."
        )

    # Find the campaign to resume
    if campaign_id:
        campaign = await run_db(get_campaign, campaign_id)
        if not campaign:
            return f"Campaign not found: {campaign_id}"
    else:
        campaigns = await run_db(list_campaigns, status="paused")
        if not campaigns:
            return (
                "No paused campaigns to resume.\n\n"
                "Use show_status() to see all campaigns."
            )
        campaign = campaigns[0]
        campaign_id = campaign["id"]

    # Check current status
    status = campaign.get("status", "")
    if status == "active":
        return (
            f"Campaign '{campaign['name']}' is already active.\n\n"
            "Outreach is running normally."
        )
    if status != "paused":
        return (
            f"Campaign '{campaign['name']}' has status '{status}' and cannot be resumed.\n"
            "Only paused campaigns can be resumed."
        )

    # Resume it and clear pause metadata
    cfg = json.loads(campaign.get("config_json") or "{}")
    old_pause_reason = cfg.get("pause_reason", "unknown")
    cfg.pop("pause_reason", None)
    cfg.pop("paused_at", None)
    await run_db(update_campaign, campaign_id, status="active", config_json=json.dumps(cfg))

    # Audit log
    await run_db(
        log_action, "campaign_status_change",
        result="active",
        details={
            "campaign_id": campaign_id,
            "campaign_name": campaign["name"],
            "old_status": "paused",
            "new_status": "active",
            "changed_by": "user",
            "reason": f"manual_resume (was paused by: {old_pause_reason})",
        },
    )

    # Sync to backend so cloud scheduler resumes
    synced = await sync_campaign_status(
        campaign_id, "active", caller="user", reason="manual_resume",
    )
    logger.info(
        "Resumed campaign %s: %s (cloud_synced=%s)",
        campaign_id, campaign["name"], synced,
    )

    cloud_note = ""
    if not synced:
        cloud_note = "\n\n**Warning**: Could not sync to cloud scheduler. Run show_status() to refresh."

    return (
        f"Campaign '{campaign['name']}' is now active again.\n\n"
        f"Outreach will resume. Use generate_and_send() to send the next message.{cloud_note}"
    )
