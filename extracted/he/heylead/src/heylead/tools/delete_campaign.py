"""Tool: delete_campaign — Permanently delete a campaign and all its data.

Removes the campaign, its contacts, outreaches, messages, engagements,
scheduler jobs, and action logs. This is irreversible.
"""

from __future__ import annotations

import logging

from ..db.queries import (
    get_campaign,
    get_setting,
    list_campaigns,
    log_action,
    skip_pending_outreaches,
)
from ..db.schema import get_db
from ..db.async_bridge import run_db
from ..services.cloud_sync import sync_campaign_delete

logger = logging.getLogger(__name__)


async def run_delete_campaign(campaign_id: str = "", confirm: bool = False) -> str:
    """Permanently delete a campaign and all associated data.

    Deletes: campaign, contacts, outreaches, messages, engagements,
    scheduler jobs, and action logs. This cannot be undone.

    Args:
        campaign_id: Which campaign to delete. If empty, shows all campaigns
            so user can pick one.
        confirm: Must be True to actually delete. Safety guard.
    """

    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "Setup required before managing campaigns.\n\n"
            "Please run setup_profile first."
        )

    # Find the campaign
    if not campaign_id:
        campaigns = await run_db(list_campaigns)
        if not campaigns:
            return "No campaigns to delete."

        lines = ["Which campaign do you want to delete?\n"]
        for c in campaigns:
            status_icon = {
                "active": "\U0001f7e2",
                "paused": "\u23f8\ufe0f",
                "completed": "\u2705",
                "draft": "\U0001f4dd",
            }.get(c.get("status", ""), "\u2753")
            lines.append(
                f"  {status_icon} `{c['id'][:8]}...` — {c['name']} ({c.get('status', '?')})"
            )
        lines.append("")
        lines.append(
            'Call delete_campaign(campaign_id="...", confirm=True) with the ID above.'
        )
        return "\n".join(lines)

    campaign = await run_db(get_campaign, campaign_id)
    if not campaign:
        return f"Campaign not found: {campaign_id}"

    # Safety: require explicit confirmation
    if not confirm:
        return (
            f"\u26a0\ufe0f **Are you sure?** This will permanently delete:\n\n"
            f"  Campaign: **{campaign['name']}**\n"
            f"  Status: {campaign.get('status', '?')}\n\n"
            "  This deletes ALL associated data:\n"
            "  \u2022 Contacts and fit scores\n"
            "  \u2022 Outreaches and status history\n"
            "  \u2022 Messages and conversation threads\n"
            "  \u2022 Engagement records (comments, reactions)\n"
            "  \u2022 Scheduled jobs\n"
            "  \u2022 Action logs\n\n"
            "  **This cannot be undone.**\n\n"
            f'To confirm: delete_campaign(campaign_id="{campaign_id}", confirm=True)'
        )

    # Mark pending outreaches as skipped before deletion
    await run_db(skip_pending_outreaches, campaign_id)

    # ── Delete in correct order (foreign key constraints) ──
    def _delete_campaign_data():
        db = get_db()
        try:
            outreach_rows = db.execute(
                "SELECT id FROM outreaches WHERE campaign_id = ?", (campaign_id,)
            ).fetchall()
            outreach_ids = [r["id"] if isinstance(r, dict) else r[0] for r in outreach_rows]

            deleted_counts = {}

            contact_rows = db.execute(
                "SELECT id FROM contacts WHERE campaign_id = ?", (campaign_id,)
            ).fetchall()
            contact_ids = [r["id"] if isinstance(r, dict) else r[0] for r in contact_rows]

            if outreach_ids:
                placeholders = ",".join("?" for _ in outreach_ids)
                db.execute(f"DELETE FROM messages WHERE outreach_id IN ({placeholders})", tuple(outreach_ids))
                db.execute(f"DELETE FROM actions_log WHERE outreach_id IN ({placeholders})", tuple(outreach_ids))
                db.execute(f"DELETE FROM engagements WHERE outreach_id IN ({placeholders})", tuple(outreach_ids))
                db.execute(f"DELETE FROM prospect_daily_plans WHERE outreach_id IN ({placeholders})", tuple(outreach_ids))

            if contact_ids:
                c_placeholders = ",".join("?" for _ in contact_ids)
                db.execute(f"DELETE FROM post_authors WHERE contact_id IN ({c_placeholders})", tuple(contact_ids))
                db.execute(f"DELETE FROM signals WHERE prospect_id IN ({c_placeholders})", tuple(contact_ids))
                db.execute(f"DELETE FROM crm_mappings WHERE contact_id IN ({c_placeholders})", tuple(contact_ids))

            db.execute("DELETE FROM signals WHERE campaign_id = ?", (campaign_id,))
            db.execute("DELETE FROM scheduler_jobs WHERE campaign_id = ?", (campaign_id,))
            db.execute("DELETE FROM ab_tests WHERE campaign_id = ?", (campaign_id,))
            db.execute("DELETE FROM signal_watchlists WHERE campaign_id = ?", (campaign_id,))
            db.execute("DELETE FROM strategy_actions WHERE campaign_id = ?", (campaign_id,))
            db.execute("DELETE FROM signal_experiments WHERE campaign_id = ?", (campaign_id,))
            db.execute("DELETE FROM outreaches WHERE campaign_id = ?", (campaign_id,))
            deleted_counts["outreaches"] = len(outreach_ids)

            result = db.execute("DELETE FROM contacts WHERE campaign_id = ?", (campaign_id,))
            deleted_counts["contacts"] = result.rowcount if hasattr(result, "rowcount") else 0

            db.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
            db.commit()
            return deleted_counts, None
        except Exception as e:
            return {}, e
        finally:
            db.close()

    deleted_counts, delete_error = await run_db(_delete_campaign_data)
    if delete_error:
        logger.error(f"Delete campaign failed: {delete_error}", exc_info=True)
        return f"Delete failed: {delete_error}\n\nThe campaign may be partially deleted."

    # Sync deletion to backend so cloud scheduler stops processing
    synced = await sync_campaign_delete(campaign_id)

    # Log the deletion (without campaign_id since it's gone)
    await run_db(log_action, "campaign_deleted",
        details={
            "campaign_name": campaign["name"],
            "deleted_outreaches": deleted_counts.get("outreaches", 0),
            "deleted_contacts": deleted_counts.get("contacts", 0),
        },)

    logger.info(f"Deleted campaign: {campaign['name']} ({campaign_id})")

    cloud_note = ""
    if not synced:
        cloud_note = "\n**Warning**: Could not sync deletion to cloud scheduler."

    return (
        f"\U0001f5d1\ufe0f Campaign **{campaign['name']}** has been permanently deleted.\n\n"
        f"Removed:\n"
        f"  \u2022 {deleted_counts.get('outreaches', 0)} outreaches\n"
        f"  \u2022 {deleted_counts.get('contacts', 0)} contacts\n"
        f"  \u2022 Associated messages, engagements, and logs\n\n"
        f"Use create_campaign() to start a new campaign.{cloud_note}"
    )
