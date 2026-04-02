"""Cloud sync service — push/pull state between MCP client and backend scheduler.

MCP client pushes campaign/outreach state to the backend for 24/7 scheduling.
Backend executes outreach jobs (invites, follow-ups, engagements, reply checks)
via Cloud Scheduler every 5 minutes, even when the user's laptop is closed.

MCP client pulls back changes (outreach status updates, new messages) periodically.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from .. import config
from ..db import queries, signal_queries
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(30.0, connect=15.0, read=30.0, write=30.0)


class BackendAuthError(Exception):
    """Raised when the backend returns 401/403 — JWT expired or invalid."""

    pass


def _headers() -> dict[str, str]:
    """Build auth headers for backend API calls."""
    _, jwt = config.get_backend_config()
    return {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _base_url() -> str:
    """Get backend base URL."""
    url, _ = config.get_backend_config()
    return url.rstrip("/")


# ── Push: Sync local state to backend ──


async def sync_to_cloud() -> dict[str, Any]:
    """Push all active autopilot campaign state to the backend for cloud scheduling.

    Gathers campaigns, contacts, outreaches, messages, engagements, and settings
    from the local DB and POSTs them to /api/v1/scheduler/sync.

    Returns the backend's response dict.
    """
    if not config.is_backend_mode():
        return {"error": "Backend mode not configured"}

    # ── Gather settings ──
    voice_signature = await run_db(queries.get_setting, "voice_signature", {})
    profile = await run_db(queries.get_setting, "profile", {})
    tier = config.get_tier()
    cfg = config.load_config()
    working_hours = cfg.get("working_hours", {})

    # ── Gather all autopilot campaigns (including paused) ──
    # Must sync paused campaigns too so backend reflects emergency_stop state.
    all_campaigns = await run_db(queries.list_campaigns)
    autopilot_campaigns = [
        c for c in all_campaigns
        if c.get("mode") == "autopilot" and c.get("status") in ("active", "paused")
    ]

    sync_campaigns = []
    sync_contacts = []
    sync_outreaches = []
    sync_messages = []
    sync_engagements = []

    for camp in autopilot_campaigns:
        camp_id = camp["id"]

        sync_campaigns.append({
            "id": camp_id,
            "name": camp.get("name", ""),
            "mode": camp.get("mode", "autopilot"),
            "status": camp.get("status", "active"),
            "icp_json": camp.get("icp_json", ""),
            "config_json": camp.get("config_json", ""),
            "context_json": camp.get("context_json", ""),
        })

        # Contacts
        contacts = await run_db(queries.get_contacts_for_campaign, camp_id)
        for contact in contacts:
            sync_contacts.append({
                "id": contact["id"],
                "campaign_id": camp_id,
                "name": contact.get("name") or "",
                "title": contact.get("title") or "",
                "company": contact.get("company") or "",
                "linkedin_id": contact.get("linkedin_id") or "",
                "linkedin_url": contact.get("linkedin_url") or "",
                "profile_json": contact.get("profile_json") or "",
                "analysis_json": contact.get("analysis_json") or "",
                "fit_score": contact.get("fit_score") or 0.0,
                "source": contact.get("source") or "",
                "source_detail": contact.get("source_detail") or "",
            })

        # Outreaches
        def _get_outreaches(cid):
            db = queries.get_db()
            rows = db.execute(
                "SELECT * FROM outreaches WHERE campaign_id = ?", (cid,)
            ).fetchall()
            db.close()
            return rows

        outreach_rows = await run_db(_get_outreaches, camp_id)
        for o in outreach_rows:
            out = dict(o)
            sync_outreaches.append({
                "id": out["id"],
                "campaign_id": camp_id,
                "contact_id": out["contact_id"],
                "status": out.get("status") or "pending",
                "next_action": out.get("next_action") or "",
                "followup_count": out.get("followup_count") or 0,
                "memory_json": out.get("memory_json") or "",
                "outcome_json": out.get("outcome_json") or "",
                "invited_at": out.get("invited_at"),
                "accepted_at": out.get("accepted_at"),
                "first_reply_at": out.get("first_reply_at"),
            })

            # Messages for each outreach
            messages = await run_db(queries.get_messages_for_outreach, out["id"])
            for msg in messages:
                sync_messages.append({
                    "id": msg["id"],
                    "outreach_id": out["id"],
                    "role": msg.get("role") or "",
                    "text": msg.get("text") or "",
                    "sentiment": msg.get("sentiment") or "",
                    "timestamp": msg.get("timestamp") or 0,
                })

        # Engagements
        def _get_engagements(cid):
            db2 = queries.get_db()
            rows = db2.execute(
                "SELECT e.* FROM engagements e "
                "JOIN outreaches o ON e.outreach_id = o.id "
                "WHERE o.campaign_id = ?",
                (cid,),
            ).fetchall()
            db2.close()
            return rows

        eng_rows = await run_db(_get_engagements, camp_id)
        for eng in eng_rows:
            e = dict(eng)
            sync_engagements.append({
                "id": e["id"],
                "outreach_id": e["outreach_id"],
                "action_type": e.get("action_type") or "",
                "post_id": e.get("post_id") or "",
                "post_text": e.get("post_text") or "",
                "text": e.get("text") or "",
                "reaction_type": e.get("reaction_type") or "",
                "status": e.get("status") or "sent",
            })

    # ── POST to backend ──
    has_sales_nav = await run_db(queries.get_setting, "has_sales_navigator", False)

    # Brand strategy data for cloud scheduler
    brand_analysis = await run_db(queries.get_setting, "brand_analysis")
    brand_strategy = await run_db(queries.get_setting, "brand_strategy")
    brand_baseline = await run_db(queries.get_setting, "brand_baseline")
    brand_actions_completed = await run_db(queries.get_setting, "brand_actions_completed")

    payload = {
        "settings": {
            "voice_signature": voice_signature,
            "profile": profile,
            "tier": tier,
            "working_hours": working_hours,
            "has_sales_navigator": has_sales_nav,
            "brand_analysis": brand_analysis,
            "brand_strategy": brand_strategy,
            "brand_baseline": brand_baseline,
            "brand_actions_completed": brand_actions_completed,
            "always_on": config.is_scheduler_always_on(),
        },
        "campaigns": sync_campaigns,
        "contacts": sync_contacts,
        "outreaches": sync_outreaches,
        "messages": sync_messages,
        "engagements": sync_engagements,
    }

    base = _base_url()
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(
                f"{base}/api/v1/scheduler/sync",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
            result = resp.json()
            logger.info(
                "Cloud sync complete: %d campaigns, %d contacts, %d outreaches",
                result.get("campaigns", 0),
                result.get("contacts", 0),
                result.get("outreaches", 0),
            )
        except httpx.HTTPStatusError as e:
            logger.error("Cloud sync HTTP error: %s %s", e.response.status_code, e.response.text)
            return {"error": f"Sync failed: HTTP {e.response.status_code}"}
        except httpx.HTTPError as e:
            logger.error("Cloud sync failed: %s", e)
            return {"error": f"Sync failed: {e}"}

    # ── Push signals to backend (separate endpoint) ──
    try:
        await _sync_signals_to_cloud()
    except Exception as e:
        logger.warning("Signal sync failed (non-fatal): %s", e)

    return result


async def _sync_signals_to_cloud() -> None:
    """Push locally-collected signals to the backend via /signals/ingest/batch.

    Uses last_signal_sync_ts setting to only push new signals.
    Backend deduplicates by linkedin_id + signal_type within 24h.
    """
    import time as _time

    last_sync = await run_db(queries.get_setting, "last_signal_sync_ts", 0)
    if not isinstance(last_sync, (int, float)):
        last_sync = 0

    signals = await run_db(signal_queries.list_signals_for_sync, int(last_sync))
    if not signals:
        return

    # Map local signal format to backend ingest format
    batch: list[dict[str, Any]] = []
    max_detected = int(last_sync)

    for sig in signals:
        detected = sig.get("detected_at", 0) or 0
        if detected > max_detected:
            max_detected = detected

        metadata: dict[str, Any] = {}
        if sig.get("metadata_json"):
            try:
                metadata = json.loads(sig["metadata_json"])
            except (json.JSONDecodeError, TypeError):
                pass

        batch.append({
            "signal_type": sig.get("signal_type", "custom"),
            "prospect_name": sig.get("prospect_name") or "",
            "prospect_title": sig.get("prospect_title") or "",
            "linkedin_id": sig.get("linkedin_id") or "",
            "company": metadata.get("company", ""),
            "content": sig.get("content") or "",
            "source": sig.get("source") or "mcp",
            "campaign_id": sig.get("campaign_id") or "",
            "metadata": metadata,
            "intent": sig.get("intent") or "",
            "confidence": sig.get("confidence") or 0.0,
        })

    # Send in batches of 50 (backend max)
    base = _base_url()
    total_ingested = 0

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for i in range(0, len(batch), 50):
            chunk = batch[i : i + 50]
            try:
                resp = await client.post(
                    f"{base}/api/v1/signals/ingest/batch",
                    json={"signals": chunk},
                    headers=_headers(),
                )
                resp.raise_for_status()
                result = resp.json()
                total_ingested += result.get("ingested", 0)
            except httpx.HTTPError as e:
                logger.warning("Signal batch sync failed: %s", e)

    if total_ingested > 0:
        logger.info("Synced %d signals to backend", total_ingested)

    # Update last sync timestamp
    await run_db(queries.save_setting, "last_signal_sync_ts", max_detected)


# ── Pull: Fetch changes from backend ──


async def pull_changes(since: int) -> dict[str, Any]:
    """Pull state changes made by the backend scheduler since a timestamp.

    Applies outreach status updates and saves new messages to the local DB.
    Returns the changes dict from the backend.
    """
    if not config.is_backend_mode():
        return {"error": "Backend mode not configured"}

    base = _base_url()
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.get(
                f"{base}/api/v1/scheduler/changes",
                params={"since": since},
                headers=_headers(),
            )
            resp.raise_for_status()
            changes = resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (401, 403):
                raise BackendAuthError(
                    "Backend returned %d — JWT expired or invalid."
                    % e.response.status_code
                )
            logger.error("Pull changes HTTP error: %s", e.response.status_code)
            return {"error": f"Pull failed: HTTP {e.response.status_code}"}
        except httpx.HTTPError as e:
            logger.error("Pull changes failed: %s", e)
            return {"error": f"Pull failed: {e}"}

    # Apply outreach updates to local DB
    outreach_updates = changes.get("outreach_updates", [])
    for update in outreach_updates:
        oid = update.get("id")
        if not oid:
            continue
        local = await run_db(queries.get_outreach, oid)
        if not local:
            continue
        kwargs: dict[str, Any] = {}
        if "status" in update:
            kwargs["status"] = update["status"]
        if "followup_count" in update:
            kwargs["followup_count"] = update["followup_count"]
        # Sync event timestamps for velocity metrics
        for field in ("invited_at", "accepted_at", "first_reply_at", "outcome_json"):
            if update.get(field):
                kwargs[field] = update[field]
        if kwargs:
            await run_db(queries.update_outreach, oid, **kwargs)
            logger.debug("Applied cloud update to outreach %s: %s", oid, kwargs)

    # Save new messages
    new_messages = changes.get("new_messages", [])
    for msg in new_messages:
        outreach_id = msg.get("outreach_id")
        if not outreach_id:
            continue
        # Check if message already exists locally
        local_msgs = await run_db(queries.get_messages_for_outreach, outreach_id)
        existing_ids = {m["id"] for m in local_msgs}
        if msg.get("id") in existing_ids:
            continue
        await run_db(queries.save_message,
            outreach_id=outreach_id,
            role=msg.get("role", "sdr"),
            text=msg.get("text", ""),
            sentiment=msg.get("sentiment", ""),
        )
        logger.debug("Saved cloud message for outreach %s", outreach_id)

    # Apply brand strategy updates from backend
    brand_updates = changes.get("brand_updates", {})
    if brand_updates.get("brand_strategy"):
        await run_db(queries.save_setting, "brand_strategy", brand_updates["brand_strategy"])
        logger.debug("Applied brand strategy update from cloud")
    if brand_updates.get("brand_analysis"):
        await run_db(queries.save_setting, "brand_analysis", brand_updates["brand_analysis"])
        logger.debug("Applied brand analysis update from cloud")

    # Sync new engagements from backend
    new_engagements = changes.get("new_engagements", [])
    for eng in new_engagements:
        outreach_id = eng.get("outreach_id")
        if not outreach_id:
            continue
        try:
            await run_db(queries.save_engagement,
                outreach_id=outreach_id,
                action_type=eng.get("action_type", ""),
                post_id=eng.get("post_id", ""),
                text=eng.get("text", ""),
                reaction_type=eng.get("reaction_type", ""),
                status=eng.get("status", "sent"),
                campaign_id=eng.get("campaign_id", ""),
            )
            logger.debug("Saved cloud engagement for outreach %s", outreach_id)
        except Exception as e:
            logger.debug("Engagement sync failed for outreach %s: %s", outreach_id, e)

    # Sync usage counters from backend (overwrite local with authoritative backend data)
    usage = changes.get("usage", {})
    if usage:
        try:
            from ..db.queries import set_monthly_usage
            await run_db(set_monthly_usage, usage)
            logger.debug("Applied usage sync from cloud: %s", usage)
        except Exception as e:
            logger.debug("Usage sync failed: %s", e)

    # Sync rate limits from backend (authoritative for cloud-scheduled sends)
    rate_limits = changes.get("rate_limits", {})
    if rate_limits:
        try:
            await run_db(_apply_rate_limits, rate_limits)
            logger.debug("Applied rate limits sync from cloud: %s", rate_limits)
        except Exception as e:
            logger.debug("Rate limits sync failed: %s", e)

    applied = len(outreach_updates) + len(new_messages) + len(new_engagements)
    if applied or brand_updates or rate_limits:
        logger.info(
            "Pulled %d outreach updates + %d messages + %d engagements from cloud",
            len(outreach_updates),
            len(new_messages),
            len(new_engagements),
        )

    # Save last pull timestamp
    import time
    await run_db(queries.save_setting, "last_pull_timestamp", int(time.time()))

    return changes


def _apply_rate_limits(rate_limits: dict[str, Any]) -> None:
    """Apply backend rate_limits data to local rate_limits table."""
    import datetime

    from ..db.schema import get_db

    today = datetime.date.today().isoformat()
    sent = rate_limits.get("sent_today", 0)
    accepted = rate_limits.get("accepted_today", 0)
    daily_limit = rate_limits.get("daily_limit", 15)

    db = get_db()
    # Upsert today's rate limits with backend-authoritative values
    existing = db.execute(
        "SELECT id FROM rate_limits WHERE date = ?", (today,)
    ).fetchone()
    if existing:
        db.execute(
            "UPDATE rate_limits SET sent = ?, accepted = ?, daily_limit = ? WHERE date = ?",
            (sent, accepted, daily_limit, today),
        )
    else:
        import uuid
        db.execute(
            "INSERT INTO rate_limits (id, date, sent, accepted, daily_limit) "
            "VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), today, sent, accepted, daily_limit),
        )
    db.commit()
    db.close()


# ── Ensure Synced: Auto-pull before dashboard reads ──


async def ensure_synced() -> dict[str, Any]:
    """Pull changes from backend if enough time has passed since last pull.

    Called before show_status() and campaign_report() to keep local DB fresh.
    Uses last_pull_timestamp setting to avoid redundant pulls.
    Minimum interval: 30 seconds between pulls.
    """
    if not config.is_backend_mode():
        return {}

    import time

    last_pull = await run_db(queries.get_setting, "last_pull_timestamp", 0)
    if not isinstance(last_pull, (int, float)):
        last_pull = 0
    now = int(time.time())

    # Skip if pulled recently (< 30 seconds ago)
    if now - last_pull < 30:
        logger.debug("Skipping pull — last pull was %ds ago", now - last_pull)
        return {}

    try:
        return await pull_changes(int(last_pull))
    except BackendAuthError:
        raise
    except Exception as e:
        logger.warning("ensure_synced failed: %s", e)
        return {"error": str(e)}


# ── Campaign Status Sync ──


async def sync_campaign_status(
    campaign_id: str,
    status: str,
    *,
    caller: str = "user",
    reason: str = "",
) -> bool:
    """Push a single campaign status change to the backend.

    Called from pause/resume/emergency_stop to keep backend in sync.
    Returns True if sync succeeded, False otherwise (local change still applies).
    """
    if not config.is_backend_mode():
        return False

    base = _base_url()
    action = "pause" if status == "paused" else "resume"
    url = f"{base}/api/v1/campaigns/{campaign_id}/{action}"

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(url, headers=_headers())
            resp.raise_for_status()
            logger.info(
                "Synced campaign %s status=%s to backend (caller=%s, reason=%s)",
                campaign_id, status, caller, reason,
            )
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (401, 403):
                logger.warning("Backend auth error during status sync: %s", e.response.status_code)
            else:
                logger.warning("Backend status sync failed: %s", e.response.status_code)
            return False
        except httpx.HTTPError as e:
            logger.warning("Backend status sync error: %s", e)
            return False


async def sync_emergency_stop() -> bool:
    """Push emergency stop to the backend (pauses all active campaigns).

    Returns True if sync succeeded.
    """
    if not config.is_backend_mode():
        return False

    base = _base_url()
    url = f"{base}/api/v1/campaigns/emergency-stop"

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(url, headers=_headers())
            resp.raise_for_status()
            result = resp.json()
            logger.info(
                "Emergency stop synced to backend: %d campaigns paused",
                result.get("paused_count", 0),
            )
            return True
        except httpx.HTTPError as e:
            logger.warning("Backend emergency stop sync failed: %s", e)
            return False


# ── Live Stats: Fetch dashboard data directly from backend ──


async def fetch_live_stats() -> dict[str, Any] | None:
    """Fetch live dashboard stats from the backend.

    Returns dict with campaigns, rate_limits, usage, engagements, hot_leads.
    Returns None if backend is unreachable or not in backend mode.
    """
    if not config.is_backend_mode():
        return None

    base = _base_url()
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.get(
                f"{base}/api/v1/stats",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (401, 403):
                raise BackendAuthError(
                    "Backend returned %d — JWT expired or invalid."
                    % e.response.status_code
                )
            logger.warning("Live stats HTTP error: %s", e.response.status_code)
            return None
        except httpx.HTTPError as e:
            logger.warning("Live stats failed: %s", e)
            return None


# ── Toggle: Enable/disable cloud scheduler ──


async def toggle_cloud_scheduler(enabled: bool) -> str:
    """Enable or disable the cloud scheduler on the backend.

    If enabling: syncs local state first, then toggles.
    If disabling: just toggles (no sync needed).

    Returns a user-facing status message.
    """
    if not config.is_backend_mode():
        return "Cloud scheduling requires backend mode. Set up your profile first."

    base = _base_url()

    if enabled:
        # Sync first, then enable
        sync_result = await sync_to_cloud()
        if "error" in sync_result:
            return f"Cloud sync failed: {sync_result['error']}\nCannot enable cloud scheduler."

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(
                f"{base}/api/v1/scheduler/toggle",
                json={"enabled": enabled},
                headers=_headers(),
            )
            resp.raise_for_status()
            result = resp.json()
        except httpx.HTTPStatusError as e:
            detail = ""
            try:
                detail = e.response.json().get("detail", "")
            except Exception:
                detail = e.response.text
            return f"Toggle failed: {detail}"
        except httpx.HTTPError as e:
            return f"Toggle failed: {e}"

    status = result.get("status", "unknown")
    if status == "enabled":
        return (
            "Cloud scheduler **enabled**.\n\n"
            "The backend will now process outreach every 5 minutes, 24/7 "
            "even when your laptop is off:\n"
            "- Send invitations to pending prospects (autopilot campaigns)\n"
            "- Send follow-ups on schedule (day 1, 7, 14, 21, 28)\n"
            "- Check for replies and classify sentiment\n"
            "- Engage with prospect posts (comments & reactions)\n\n"
            "All actions respect rate limits, working hours, and daily caps.\n"
            "Use `scheduler_status()` to monitor cloud activity."
        )
    else:
        return (
            "Cloud scheduler **disabled**.\n\n"
            "The backend will stop processing new outreach.\n"
            "Already-running jobs will complete.\n\n"
            "Use `toggle_scheduler(enabled=True, cloud=True)` to re-enable."
        )


# ── Status: Get cloud scheduler status ──


async def get_cloud_scheduler_status() -> dict[str, Any]:
    """Fetch scheduler status from the backend.

    Returns dict with enabled, pending_jobs, recent_activity, campaigns, etc.
    """
    if not config.is_backend_mode():
        return {"error": "Backend mode not configured"}

    base = _base_url()
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.get(
                f"{base}/api/v1/scheduler/status",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Status check failed: HTTP {e.response.status_code}"}
        except httpx.HTTPError as e:
            return {"error": f"Status check failed: {e}"}


# ── Archive / Delete Campaign Sync ──


async def sync_campaign_archive(campaign_id: str) -> bool:
    """Push a campaign archive to the backend.

    Returns True if sync succeeded.
    """
    if not config.is_backend_mode():
        return False

    base = _base_url()
    url = f"{base}/api/v1/campaigns/{campaign_id}/archive"

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(url, headers=_headers())
            resp.raise_for_status()
            logger.info("Synced campaign %s archive to backend", campaign_id)
            return True
        except httpx.HTTPError as e:
            logger.warning("Backend archive sync failed for %s: %s", campaign_id, e)
            return False


async def sync_campaign_delete(campaign_id: str) -> bool:
    """Push a campaign deletion to the backend.

    Returns True if sync succeeded.
    """
    if not config.is_backend_mode():
        return False

    base = _base_url()
    url = f"{base}/api/v1/campaigns/{campaign_id}"

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.delete(url, headers=_headers())
            resp.raise_for_status()
            logger.info("Synced campaign %s deletion to backend", campaign_id)
            return True
        except httpx.HTTPError as e:
            logger.warning("Backend delete sync failed for %s: %s", campaign_id, e)
            return False


# ── Prospect / Outreach Sync ──


async def sync_outreach_skip(outreach_id: str, reason: str = "") -> bool:
    """Push an outreach skip to the backend.

    Returns True if sync succeeded.
    """
    if not config.is_backend_mode():
        return False

    base = _base_url()
    url = f"{base}/api/v1/prospects/{outreach_id}/skip"

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(
                url, json={"reason": reason}, headers=_headers(),
            )
            resp.raise_for_status()
            logger.info("Synced outreach %s skip to backend", outreach_id)
            return True
        except httpx.HTTPError as e:
            logger.warning("Backend skip sync failed for %s: %s", outreach_id, e)
            return False


async def sync_outreach_close(
    outreach_id: str,
    outcome: str,
    reason: str = "",
    meeting_link: str = "",
) -> bool:
    """Push an outreach close to the backend.

    Returns True if sync succeeded.
    """
    if not config.is_backend_mode():
        return False

    base = _base_url()
    url = f"{base}/api/v1/prospects/{outreach_id}/close"
    payload: dict[str, str] = {"outcome": outcome}
    if reason:
        payload["reason"] = reason
    if meeting_link:
        payload["meeting_link"] = meeting_link

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.post(url, json=payload, headers=_headers())
            resp.raise_for_status()
            logger.info("Synced outreach %s close (outcome=%s) to backend", outreach_id, outcome)
            return True
        except httpx.HTTPError as e:
            logger.warning("Backend close sync failed for %s: %s", outreach_id, e)
            return False


# ── Campaign Settings Sync ──


async def sync_campaign_settings(campaign_id: str, settings: dict) -> bool:
    """Push campaign settings changes to the backend.

    Returns True if sync succeeded.
    """
    if not config.is_backend_mode():
        return False

    base = _base_url()
    url = f"{base}/api/v1/campaigns/{campaign_id}/settings"

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.patch(url, json=settings, headers=_headers())
            resp.raise_for_status()
            logger.info("Synced campaign %s settings to backend: %s", campaign_id, list(settings.keys()))
            return True
        except httpx.HTTPError as e:
            logger.warning("Backend settings sync failed for %s: %s", campaign_id, e)
            return False
