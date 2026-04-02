"""Tool 3: generate_and_send — Generate a personalized message and send (or queue for review).

Core outreach loop:
1. Pick next prospect from campaign queue
2. Generate personalized invitation message (voice-matched)
3. Run 5-stage validation
4. In Copilot mode: show for approval. In Autopilot: send immediately.
5. Track rate limits and scheduling
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from ..ai.message_fixer import fix_message
from ..ai.message_generator import generate_message
from ..ai.message_improver import improve_message
from ..ai.message_validator import validate_message
from ..ai.llm_validator import llm_validate
from ..ai.prospect_analyzer import analyze_prospect
from ..config import get_tier
from ..constants import (
    FREE_MONTHLY_INVITATIONS,
    INVITATION_NOTE_MAX_CHARS,
    MIN_WARMUP_ENGAGEMENTS,
    TIER_PRO,
)
from ..db import aio as adb
from ..db.async_bridge import run_db
from ..db.queries import (
    find_active_campaign,
    get_campaign_context,
    get_contact_analysis,
    get_contacts_for_campaign,
    get_engagement_count_for_outreach,
    get_monthly_usage,
    get_setting,
    increment_sent,
    increment_usage,
    log_action,
    save_contact_analysis,
    save_message,
    update_campaign,
    update_outreach,
)
from ..formatter import stars
from ..linkedin.rate_limiter import can_send_now, get_next_delay, update_limits_after_send
from ..services.channel_selector import (
    CHANNEL_EMAIL,
    CHANNEL_LINKEDIN,
    select_channel,
    has_email_channel,
    _extract_email,
)
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)

logger = logging.getLogger(__name__)


async def run_generate_and_send(
    campaign_id: str = "",
    mode: str = "autopilot",
    force_channel: str = "",
    target_outreach_id: str = "",
) -> str:
    """Generate and send (or queue) a personalized LinkedIn message.

    Flow:
    1. Find the active campaign and next pending prospect
    2. Generate a personalized message using voice signature
    3. Validate the message (5-stage pipeline)
    4. Copilot: show for review. Autopilot: send directly.

    Args:
        campaign_id: Campaign to send from.
        mode: Always autopilot (copilot mode removed).
        force_channel: Override channel choice ("email" forces email path).
        target_outreach_id: Specific outreach to send (for email overflow).
    """

    # ── Step 0: Pre-checks ──
    setup_done = await adb.get_setting("setup_complete", False)
    if not setup_done:
        return (
            "❌ Setup required before sending messages.\n\n"
            "Please run setup_profile first — it connects your LinkedIn account and "
            "creates your voice signature so messages sound like you.\n\n"
            "Say 'set up my profile' and I'll walk you through it step by step."
        )

    account_id = get_account_id()
    if not account_id:
        return "❌ No LinkedIn account connected. Run setup_profile first."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"❌ {e}"

    # ── Ensure connections are synced at least once for accurate dedup ──
    try:
        from ..services.connection_sync import get_connection_count, ensure_synced
        if await run_db(get_connection_count, account_id) == 0:
            logger.info("No local connections cached — triggering initial sync for account %s", account_id)
            await ensure_synced(client, account_id)
    except Exception as e:
        logger.warning("Initial connection sync failed (non-critical): %s", e)

    # ── Step 1: Find campaign + next prospect ──
    campaign, err = await adb.find_active_campaign(campaign_id)
    if not campaign:
        return f"❌ {err}"
    campaign_id = campaign["id"]

    # Block sends when campaign is paused
    if campaign.get("status") == "paused":
        return (
            f"⏸️ Campaign '{campaign['name']}' is paused.\n\n"
            "No messages will be sent while the campaign is paused.\n"
            "Use resume_campaign() to resume outreach."
        )

    # Find next pending outreach (or specific target for email overflow)
    # For DM sends (connections-only campaigns), also pick 'connected' prospects
    # that haven't been messaged yet.  The reply checker may have detected existing
    # connections and set status to 'connected' before any DM was sent.
    dm_statuses = "('pending', 'connected')" if force_channel == "dm" else "('pending')"

    def _fetch_next_prospect(target_oid: str, cid: str) -> dict | None:
        from ..db.schema import get_db as _get_db
        _db = _get_db()
        if target_oid:
            _row = _db.execute(
                f"""SELECT o.id as outreach_id, o.contact_id, o.variant,
                          c.id as contact_db_id, c.campaign_id as contact_campaign_id,
                          c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                          c.profile_json, c.analysis_json, c.fit_score, c.status as contact_status
                   FROM outreaches o
                   JOIN contacts c ON o.contact_id = c.id
                   WHERE o.id = ? AND o.status IN {dm_statuses}
                   LIMIT 1""",
                (target_oid,),
            ).fetchone()
        else:
            _row = _db.execute(
                f"""SELECT o.id as outreach_id, o.contact_id, o.variant,
                          c.id as contact_db_id, c.campaign_id as contact_campaign_id,
                          c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                          c.profile_json, c.analysis_json, c.fit_score, c.status as contact_status
                   FROM outreaches o
                   JOIN contacts c ON o.contact_id = c.id
                   WHERE o.campaign_id = ? AND o.status IN {dm_statuses}
                   ORDER BY c.fit_score DESC
                   LIMIT 1""",
                (cid,),
            ).fetchone()
        _db.close()
        return dict(_row) if _row else None

    row = await run_db(_fetch_next_prospect, target_outreach_id, campaign_id)

    if not row:
        return (
            f"✅ All prospects in this campaign have been reached!\n\n"
            f"Campaign: {campaign['name']}\n"
            "Use show_status to see results, or create_campaign for a new target."
        )

    prospect = row
    outreach_id = prospect["outreach_id"]
    contact_id = prospect["contact_id"]

    # ── Company profile gate: skip business pages ──
    from ..services.dedup_service import is_company_profile
    _prospect_for_check = {
        "name": prospect.get("name", ""),
        "linkedin_url": prospect.get("linkedin_url", ""),
        "title": prospect.get("title", ""),
        "company": prospect.get("company", ""),
    }
    if is_company_profile(_prospect_for_check):
        await adb.update_outreach(outreach_id, status="error",
                        last_attempt_error="Company/business profile — cannot message")
        await adb.log_action("company_profile_skipped", outreach_id=outreach_id,
                   result="skipped",
                   details={"prospect": prospect.get("name", ""), "reason": "company_page"})
        logger.info("Skipping company profile: %s", prospect.get("name", ""))
        return (
            f"⏭️ Skipped **{prospect.get('name', 'Unknown')}** — looks like a company/business page, "
            f"not a personal profile. Marked as error to prevent future retries."
        )

    # ── Exclusion gate: skip contacts excluded from automation ──
    from ..db.global_contact_queries import is_excluded_by_contact_id
    if await run_db(is_excluded_by_contact_id, contact_id):
        return (
            f"⏭️ Skipped {prospect.get('name', 'Unknown')} — excluded from automation.\n\n"
            "This contact has the 'do-not-automate' tag or 'do_not_contact' lifecycle.\n"
            "Remove the tag with contacts(action='tag', tag='-do-not-automate') to re-enable."
        )

    # ── Optimistic lock: claim this outreach atomically ──
    # Prevents duplicate sends when multiple scheduler jobs target the same prospect.
    # CAS: only succeeds if status is still in the expected set (pending or connected for DMs).
    def _try_claim(oid: str) -> tuple[str, int]:
        from ..db.schema import get_db as _get_db_lock
        lock_db = _get_db_lock()
        orig_row = lock_db.execute("SELECT status FROM outreaches WHERE id = ?", (oid,)).fetchone()
        orig_status = orig_row["status"] if orig_row else "pending"
        count = lock_db.execute(
            f"UPDATE outreaches SET status = 'sending' WHERE id = ? AND status IN {dm_statuses}",
            (oid,),
        ).rowcount
        lock_db.commit()
        lock_db.close()
        return orig_status, count

    original_status, claimed = await run_db(_try_claim, outreach_id)
    if not claimed:
        logger.info("Outreach %s already claimed by another job, skipping", outreach_id)
        return "⏸️ Prospect already being processed by another job. Skipping."

    async def _release_claim() -> None:
        """Release the optimistic lock on failure — reset to original status."""
        try:
            def _do_release(oid: str, orig_st: str) -> None:
                from ..db.schema import get_db as _get_db_rel
                rel_db = _get_db_rel()
                rel_db.execute(
                    "UPDATE outreaches SET status = ? WHERE id = ? AND status = 'sending'",
                    (orig_st, oid),
                )
                rel_db.commit()
                rel_db.close()
            await run_db(_do_release, outreach_id, original_status)
        except Exception as e:
            logger.warning("Failed to release outreach claim %s: %s", outreach_id, e)

    # ── Fit score gate: skip prospects below threshold ──
    from ..constants import MIN_FIT_SCORE_THRESHOLD
    prospect_fit = prospect.get("fit_score") or 0
    # Load per-campaign override if set
    try:
        cfg = json.loads(campaign.get("config_json") or "{}")
        campaign_threshold = cfg.get("min_fit_score", MIN_FIT_SCORE_THRESHOLD)
    except (json.JSONDecodeError, TypeError):
        campaign_threshold = MIN_FIT_SCORE_THRESHOLD
    if prospect_fit < campaign_threshold:
        await _release_claim()
        await adb.update_outreach(outreach_id, status="skipped")
        await adb.log_action(
            "fit_score_below_threshold",
            outreach_id=outreach_id,
            result="skipped",
            details={"fit_score": prospect_fit, "threshold": campaign_threshold},
        )
        return (
            f"⏭️ Skipped {prospect.get('name', 'Unknown')} — fit score {prospect_fit:.2f} "
            f"below threshold {campaign_threshold:.2f}."
        )

    # ── Hard message cap: never send more than MAX messages to any single prospect ──
    MAX_SDR_MESSAGES_PER_PROSPECT = 3
    existing_sdr_count = 0
    try:
        def _get_sdr_count(oid: str) -> int:
            from ..db.schema import get_db as _get_db_cap
            cap_db = _get_db_cap()
            cap_row = cap_db.execute(
                "SELECT COUNT(*) as cnt FROM messages WHERE outreach_id = ? AND role = 'sdr'",
                (oid,),
            ).fetchone()
            cap_db.close()
            return cap_row["cnt"] if cap_row else 0
        existing_sdr_count = await run_db(_get_sdr_count, outreach_id)
    except Exception:
        pass
    if existing_sdr_count >= MAX_SDR_MESSAGES_PER_PROSPECT:
        await _release_claim()
        await adb.log_action(
            "message_cap_reached",
            outreach_id=outreach_id,
            result="skipped",
            details={"sent": existing_sdr_count, "limit": MAX_SDR_MESSAGES_PER_PROSPECT},
        )
        # Fix status if inconsistent
        if original_status in ("pending", "connected"):
            await adb.update_outreach(outreach_id, status="messaged")
        return (
            f"⏭️ Message cap reached for {prospect.get('name', 'Unknown')} "
            f"({existing_sdr_count}/{MAX_SDR_MESSAGES_PER_PROSPECT} messages sent)."
        )

    # ── Minimum message gap: at least 1 day between messages to same prospect ──
    MIN_MESSAGE_GAP_SECONDS = 86400  # 24 hours
    if existing_sdr_count > 0:
        try:
            def _get_last_sdr_ts(oid: str) -> int:
                from ..db.schema import get_db as _get_db_gap
                gap_db = _get_db_gap()
                gap_row = gap_db.execute(
                    "SELECT MAX(timestamp) as last_ts FROM messages WHERE outreach_id = ? AND role = 'sdr'",
                    (oid,),
                ).fetchone()
                gap_db.close()
                return gap_row["last_ts"] if gap_row and gap_row["last_ts"] else 0
            last_ts = await run_db(_get_last_sdr_ts, outreach_id)
            if last_ts:
                seconds_since = int(time.time()) - last_ts
                if seconds_since < MIN_MESSAGE_GAP_SECONDS:
                    hours_left = (MIN_MESSAGE_GAP_SECONDS - seconds_since) // 3600
                    await _release_claim()
                    await adb.log_action(
                        "message_gap_too_short",
                        outreach_id=outreach_id,
                        result="skipped",
                        details={"seconds_since": seconds_since, "min_gap": MIN_MESSAGE_GAP_SECONDS},
                    )
                    return (
                        f"⏭️ Too soon to message {prospect.get('name', 'Unknown')} again "
                        f"(last message {seconds_since // 3600}h ago, minimum gap 24h). "
                        f"Retry in ~{hours_left}h."
                    )
        except Exception as e:
            logger.debug("Message gap check failed (non-critical): %s", e)

    # ── Channel selection ──
    from ..linkedin.rate_limiter import BLOCK_DAILY, BLOCK_WEEKLY
    _, _, block_type = await can_send_now()
    linkedin_limit_hit = block_type in (BLOCK_DAILY, BLOCK_WEEKLY)

    outreach_data = {"channel": "linkedin"}  # Default
    channel = select_channel(
        outreach=outreach_data,
        prospect=prospect,
        campaign_config=json.loads(campaign.get("config_json") or "{}"),
        force_channel=force_channel,
        linkedin_limit_hit=linkedin_limit_hit,
    )

    # ── Step 1.5: Warm-up check (skip for DM channel — existing connections) ──
    eng_count = await adb.get_engagement_count_for_outreach(outreach_id)

    if eng_count < MIN_WARMUP_ENGAGEMENTS and mode == "autopilot" and channel != "dm":
        # Autopilot: skip un-warmed prospects, find a warmed-up one
        def _fetch_warmed(cid: str, min_eng: int) -> dict | None:
            from ..db.schema import get_db as _get_db
            db2 = _get_db()
            _row = db2.execute(
                """SELECT o.id as outreach_id, o.contact_id, o.variant,
                          c.id as contact_db_id, c.campaign_id as contact_campaign_id,
                          c.name, c.title, c.company, c.linkedin_url, c.linkedin_id,
                          c.profile_json, c.analysis_json, c.fit_score, c.status as contact_status
                   FROM outreaches o
                   JOIN contacts c ON o.contact_id = c.id
                   WHERE o.campaign_id = ? AND o.status = 'pending'
                     AND (SELECT COUNT(*) FROM engagements e WHERE e.outreach_id = o.id) >= ?
                   ORDER BY c.fit_score DESC
                   LIMIT 1""",
                (cid, min_eng),
            ).fetchone()
            db2.close()
            return dict(_row) if _row else None

        warmed_row = await run_db(_fetch_warmed, campaign_id, MIN_WARMUP_ENGAGEMENTS)

        if warmed_row:
            prospect = warmed_row
            outreach_id = prospect["outreach_id"]
            contact_id = prospect["contact_id"]
            eng_count = MIN_WARMUP_ENGAGEMENTS  # Known to be warmed
        else:
            await _release_claim()
            return (
                f"⏸️ No warmed-up prospects in '{campaign['name']}'.\n\n"
                f"All pending prospects need engagement warm-up first.\n"
                f"Run engage_prospect() to warm them up, then try again.\n"
                f"Check warm-up status or skip to send anyway."
            )

    # ── Step 2: Check rate limits ──
    can_send, reason, _block = await can_send_now()
    if not can_send and mode == "autopilot":
        if channel == CHANNEL_EMAIL:
            # Email overflow — LinkedIn limits don't block email sends.
            # Check email-specific limits instead.
            from ..linkedin.rate_limiter import can_send_email_now
            can_email, email_reason = await can_send_email_now()
            if not can_email:
                await _release_claim()
                return f"⏸️ Email sending paused: {email_reason}\n\nThe queue is ready — will resume automatically."
            # Proceed with email path
        else:
            await _release_claim()
            return f"⏸️ Sending paused: {reason}\n\nThe queue is ready — will resume automatically."

    # ── Step 2.5: Check LinkedIn pending invitation count ──
    if channel != CHANNEL_EMAIL and channel != "dm":
        from ..linkedin.rate_limiter import (
            check_pending_limit,
            invalidate_pending_cache,
            withdraw_oldest_to_free_spot,
        )
        can_send_pending, pending_reason, pending_block = await check_pending_limit(client, account_id)
        if not can_send_pending:
            # Try to free a spot by withdrawing the oldest invitation
            withdrawal = await withdraw_oldest_to_free_spot(client, account_id)
            if withdrawal.get("success"):
                await adb.log_action(
                    "pending_limit_auto_withdraw",
                    outreach_id=outreach_id,
                    result="success",
                    details={
                        "withdrawn_id": withdrawal["invitation_id"],
                        "days_old": withdrawal["days_old"],
                        "name": withdrawal.get("name", ""),
                    },
                )
                # Re-check after withdrawal
                can_send_pending, pending_reason, _ = await check_pending_limit(client, account_id)

            if not can_send_pending:
                await _release_claim()
                await adb.log_action(
                    "invitation_blocked_pending_limit",
                    outreach_id=outreach_id,
                    result="blocked",
                    details={"reason": pending_reason},
                )
                return (
                    f"⏸️ LinkedIn pending invitation limit reached.\n\n"
                    f"{pending_reason}\n"
                    "Invitations already sent are pending acceptance. "
                    "Will retry when pending count drops."
                )

    # Check free tier monthly limit
    tier = get_tier()
    if tier != TIER_PRO:
        usage = await adb.get_monthly_usage()
        if usage.get("invitations_sent", 0) >= FREE_MONTHLY_INVITATIONS:
            await _release_claim()
            return (
                f"⚠️ Free tier limit reached: {FREE_MONTHLY_INVITATIONS} invitations/month.\n\n"
                "Upgrade to Pro ($29/mo) for unlimited outreach.\n"
                "Your campaign will resume next month if you stay on Free."
            )

    # ── Step 3: Generate message ──
    sender_profile = await adb.get_setting("profile", {})
    voice_signature = await adb.get_setting("voice_signature", {})
    campaign_config = json.loads(campaign.get("config_json") or "{}")
    icp_data = json.loads(campaign.get("icp_json") or "{}")

    campaign_context = {
        "target_description": campaign_config.get("target_description", ""),
        "relevance_hook": icp_data.get("relevance_hook", ""),
    }

    # Load campaign context (offerings, case_studies, social_proofs, preferences)
    campaign_ctx = await adb.get_campaign_context(campaign_id)

    prospect_data = json.loads(prospect.get("profile_json", "{}")) if prospect.get("profile_json") else {
        "name": prospect.get("name", ""),
        "title": prospect.get("title", ""),
        "company": prospect.get("company", ""),
        "headline": f"{prospect.get('title', '')} at {prospect.get('company', '')}",
    }

    # ── Company Enrichment: fetch company profile for better personalization ──
    company_name = prospect_data.get("company") or prospect.get("company", "")
    if company_name and not prospect_data.get("company_data"):
        try:
            company_data = await client.get_company_profile(account_id, company_name)
            if company_data and company_data.get("name"):
                prospect_data["company_data"] = company_data
                logger.info(f"Enriched company data for {company_name}: {company_data.get('industry', 'unknown industry')}")
        except Exception as e:
            logger.debug(f"Company enrichment failed for {company_name} (non-critical): {e}")

    # ── Pre-send connection check ──
    # For DMs: use LOCAL connections DB as the definitive gate (not Unipile API).
    # The Unipile profile API can return stale/wrong is_relationship data,
    # causing 403 subscription_required when we DM a non-connection.
    mutual_info = ""
    _profile_for_enrichment: dict = {}
    _dm_connection_verified = False  # Fail closed: must be explicitly set True

    if channel == "dm":
        from ..services.connection_sync import (
            is_first_degree,
            is_first_degree_by_public_id,
            sync_connections,
            get_sync_age,
        )
        dm_prov_id = (prospect_data.get("provider_id") or "").strip()
        dm_pub_id = (prospect_data.get("public_id") or prospect.get("linkedin_id", "")).strip()

        # Re-sync connections if older than 30 min to catch recent accepts
        try:
            sync_age = await run_db(get_sync_age, account_id)
            if sync_age is None or sync_age > 1800:
                await sync_connections(client, account_id)
        except Exception as e:
            logger.warning("Connection re-sync before DM failed: %s", e)

        # Check local DB — this is the definitive 1st-degree source
        if dm_prov_id and await run_db(is_first_degree, account_id, dm_prov_id):
            _dm_connection_verified = True
        elif dm_pub_id and await run_db(is_first_degree_by_public_id, account_id, dm_pub_id):
            _dm_connection_verified = True

        if not _dm_connection_verified:
            reason = f"provider_id={dm_prov_id}, public_id={dm_pub_id}"
            error_msg = f"Not in local 1st-degree connections ({reason})"
            await adb.update_outreach(outreach_id, status="error",
                            last_attempt_error=error_msg)
            await adb.log_action("dm_not_connected", outreach_id=outreach_id,
                       result="error",
                       details={"prospect": prospect.get("name", ""),
                                "provider_id": dm_prov_id,
                                "public_id": dm_pub_id})
            logger.warning("Blocking DM to %s — not in local connections DB (%s)",
                           prospect.get("name", ""), reason)
            return (
                f"⏭️ Skipped {prospect.get('name', 'prospect')} — "
                f"not found in local 1st-degree connections. "
                f"Marked as error to avoid 403."
            )

    # Profile enrichment + connection detection for invitation path
    try:
        linkedin_id = prospect.get("linkedin_id") or prospect_data.get("public_id") or ""
        if linkedin_id:
            _profile_for_enrichment = await client.get_profile(account_id, linkedin_id)
            if isinstance(_profile_for_enrichment, dict) and _profile_for_enrichment:
                is_rel = _profile_for_enrichment.get("is_relationship", False)
                net_dist = _profile_for_enrichment.get("network_distance", "")
                is_connected = is_rel or net_dist == "FIRST_DEGREE"

                if channel != "dm" and is_connected:
                    from ..services.connection_sync import mark_connected
                    prov_id = (
                        prospect_data.get("provider_id", "")
                        or prospect.get("linkedin_id", "")
                    )
                    await run_db(mark_connected, account_id, prov_id, prospect.get("name", ""), linkedin_id)
                    await adb.update_outreach(outreach_id, status="connected", channel=CHANNEL_LINKEDIN)
                    await adb.log_action("pre_send_already_connected", outreach_id=outreach_id,
                               result="connected",
                               details={"prospect": prospect.get("name", ""),
                                        "network_distance": net_dist})
                    return (
                        f"Already connected with {prospect.get('name', 'prospect')} "
                        f"(detected via profile) — skipping invitation, queued for follow-up DM."
                    )
    except Exception as e:
        logger.warning("Profile connection check failed for %s: %s", prospect.get("name", ""), e)

    # ── Mutual Connections: check for warm intro paths ──
    try:
        if isinstance(_profile_for_enrichment, dict) and _profile_for_enrichment:
            shared = _profile_for_enrichment.get("shared_connections") or _profile_for_enrichment.get("mutual_connections") or 0
            if shared and int(shared) > 0:
                mutual_info = f"You share {shared} mutual connection(s) with this prospect."
                prospect_data["mutual_connections"] = int(shared)
                logger.info("Warm intro path: %d mutual connections with %s", shared, prospect.get("name", ""))
    except Exception as e:
        logger.debug("Mutual connection check failed (non-critical): %s", e)

    # ── Job Intent Signals: check if prospect's company is hiring ──
    try:
        prospect_co = prospect_data.get("company") or prospect.get("company", "")
        campaign_target = campaign_context.get("target_description", "")
        if prospect_co and campaign_target:
            from ..services.intent_signals import search_job_intent, build_intent_context
            intent_companies = await search_job_intent(
                client, account_id, campaign_target, limit=10,
            )
            # Find if prospect's company is among hiring companies
            co_lower = prospect_co.lower().strip()
            for ic in intent_companies:
                if ic["company_name"].lower().strip() == co_lower:
                    prospect_data["hiring_intent"] = ic["intent_signal"]
                    prospect_data["hiring_jobs"] = ic["jobs"][:3]
                    logger.info("Hiring intent found for %s: %s", prospect_co, ic["intent_signal"])
                    break
    except Exception as e:
        logger.debug("Job intent check failed (non-critical): %s", e)

    # ── Prospect Intelligence: analyze or load cached ──
    prospect_analysis = None
    contact_db_id = prospect.get("contact_db_id") or contact_id
    cached = await adb.get_contact_analysis(contact_db_id)
    if cached:
        prospect_analysis = cached
        logger.info(f"Loaded cached prospect analysis for {prospect.get('name', 'Unknown')}")
    else:
        try:
            prospect_analysis = await analyze_prospect(
                prospect=prospect_data,
                campaign_context=campaign_context,
                icp_data=icp_data,
            )
            await adb.save_contact_analysis(contact_db_id, prospect_analysis)
            logger.info(f"Generated and cached prospect analysis for {prospect.get('name', 'Unknown')}")
        except Exception as e:
            logger.warning(f"Prospect analysis failed, proceeding without: {e}")

    # ── A/B Test Variant: inject variant instructions if test is running ──
    outreach_variant = prospect.get("variant") if prospect else None
    if outreach_variant and campaign_id:
        try:
            running_tests = await adb.list_ab_tests(campaign_id, status="running")
            if running_tests:
                test = running_tests[0]
                variant_desc = test["variant_a"] if outreach_variant == "A" else test["variant_b"]
                variant_instruction = (
                    f"\n\nA/B TEST ACTIVE — This prospect is in Variant {outreach_variant}.\n"
                    f"Messaging instruction for this variant: {variant_desc}\n"
                    f"Follow this instruction precisely for controlled testing."
                )
                campaign_ctx = campaign_ctx or {}
                existing_prefs = campaign_ctx.get("campaign_preferences", "")
                campaign_ctx["campaign_preferences"] = (existing_prefs + variant_instruction).strip()
                logger.info("Applied A/B variant %s instruction for outreach", outreach_variant)
        except Exception as e:
            logger.debug("A/B variant injection failed (non-critical): %s", e)

    # ── Pre-outreach conversation history ──
    # Check for ANY existing conversation with this prospect — not just DM campaigns.
    # This prevents spamming people who already messaged us (inbound) or who we
    # already have a thread with from a different campaign.
    conversation_history: list[dict] | None = None
    try:
        conv_provider_id = (
            prospect_data.get("provider_id", "")
            or prospect.get("linkedin_id", "")
            or prospect_data.get("public_id", "")
        )
        if conv_provider_id:
            conv_chat_id = await client.find_chat_for_user(account_id, conv_provider_id)
            if conv_chat_id:
                conv_sender_id = sender_profile.get("provider_id", "")
                if conv_sender_id:
                    from ..services.conversation_enricher import fetch_linkedin_history
                    conversation_history = await fetch_linkedin_history(
                        client, account_id, conv_chat_id, conv_sender_id, limit=15,
                    )
                    if conversation_history:
                        logger.info(
                            "Found %d prior messages with %s for outreach",
                            len(conversation_history), prospect.get("name", "Unknown"),
                        )
    except Exception as e:
        logger.debug("Pre-outreach chat lookup failed (non-critical): %s", e)

    # ── Pre-send safety: abort if ANY prior conversation exists with prospect ──
    # Two checks:
    # 1. If prospect ever messaged us (inbound) → skip entirely (they initiated contact)
    # 2. If we already sent messages outside this outreach → skip (cross-campaign overlap)
    if conversation_history:
        prospect_msgs = [m for m in conversation_history if m.get("role") == "prospect"]
        sdr_msgs = [m for m in conversation_history if m.get("role") == "sdr"]
        local_sdr_ids = set()
        try:
            def _fetch_local_sdr_ids(oid: str) -> set:
                from ..db.schema import get_db as _get_db_conv
                _conv_db = _get_db_conv()
                _local_rows = _conv_db.execute(
                    "SELECT external_id FROM messages WHERE outreach_id = ? AND role = 'sdr' AND external_id IS NOT NULL",
                    (oid,),
                ).fetchall()
                _conv_db.close()
                return {r["external_id"] for r in _local_rows if r["external_id"]}
            local_sdr_ids = await run_db(_fetch_local_sdr_ids, outreach_id)
        except Exception:
            pass

        # Count SDR messages NOT from this outreach (i.e. from another campaign or manual)
        foreign_sdr_msgs = [
            m for m in sdr_msgs
            if m.get("external_id") and m["external_id"] not in local_sdr_ids
        ]

        if prospect_msgs:
            # Prospect messaged us at some point — this is an existing conversation
            last_prospect_text = prospect_msgs[-1].get("text", "")[:100]
            await _release_claim()
            await adb.log_action(
                "dm_skipped_existing_conversation",
                outreach_id=outreach_id,
                result="skipped",
                details={
                    "prospect_messages": len(prospect_msgs),
                    "sdr_messages": len(sdr_msgs),
                    "last_prospect_msg": last_prospect_text,
                },
            )
            if original_status in ("pending", "connected"):
                await adb.update_outreach(outreach_id, status="replied")
            return (
                f"⏭️ Skipped {prospect.get('name', 'Unknown')} — "
                f"existing conversation detected ({len(prospect_msgs)} inbound message(s)).\n"
                f"   Last from them: \"{last_prospect_text}\"\n"
                f"Use send_message(action='reply') to respond, or prospect(action='skip') to remove."
            )
        elif foreign_sdr_msgs and not local_sdr_ids:
            # We sent messages from another campaign/manually — don't pile on
            await _release_claim()
            await adb.log_action(
                "dm_skipped_cross_campaign_thread",
                outreach_id=outreach_id,
                result="skipped",
                details={
                    "foreign_sdr_messages": len(foreign_sdr_msgs),
                    "last_msg": foreign_sdr_msgs[-1].get("text", "")[:100],
                },
            )
            await adb.update_outreach(outreach_id, status="skipped")
            return (
                f"⏭️ Skipped {prospect.get('name', 'Unknown')} — "
                f"already messaged in another thread ({len(foreign_sdr_msgs)} prior message(s))."
            )

    # ── Generate → Improve → Validate → Fix pipeline ──
    message = ""
    reasoning = ""
    validation = None

    # Attempt 1: Generate + Improve + Validate (+ Fix if needed)
    try:
        result = await generate_message(
            prospect=prospect_data,
            sender_profile=sender_profile,
            voice_signature=voice_signature,
            campaign_context=campaign_context,
            prospect_analysis=prospect_analysis,
            campaign_ctx=campaign_ctx,
            conversation_history=conversation_history,
        )
        message = result["message"]
        reasoning = result.get("reasoning", "")
    except Exception as e:
        logger.error(f"Message generation failed: {e}")
        await _release_claim()
        return f"❌ Failed to generate message: {e}"

    # Log reasoning for debugging/quality analysis
    if reasoning:
        await adb.log_action("message_reasoning", outreach_id=outreach_id,
                   details={"reasoning": reasoning[:500]})

    # Improve stage — polish for naturalness
    try:
        message = await improve_message(
            draft=message,
            voice_signature=voice_signature,
            message_type="invitation",
            max_chars=INVITATION_NOTE_MAX_CHARS,
        )
    except Exception as e:
        logger.warning(f"Improve stage failed, using raw message: {e}")

    # Validate (rule-based)
    validation = validate_message(message, voice_signature, INVITATION_NOTE_MAX_CHARS)

    # LLM validation — context-sensitive checks (guardrails, company names, etc.)
    if validation.is_valid:
        try:
            sender_company = sender_profile.get("company", "")
            prospect_co = prospect_data.get("company", prospect.get("company", ""))
            llm_result = await llm_validate(
                message=message,
                history=[],
                company=sender_company,
                message_type="invitation",
                prospect_company=prospect_co,
                max_chars=INVITATION_NOTE_MAX_CHARS,
            )
            if not llm_result.is_valid:
                validation.issues.extend(llm_result.issues)
                validation.is_valid = False
                logger.info("LLM validation caught invitation issues: %s", llm_result.issues)
        except Exception as e:
            logger.warning(f"LLM validation skipped: {e}")

    # Fix stage — if validation failed, surgically fix issues
    if not validation.is_valid:
        logger.info(f"Validation failed, attempting fix: {validation.issues}")
        try:
            message = await fix_message(
                message=message,
                issues=validation.issues,
                voice_signature=voice_signature,
                message_type="invitation",
                max_chars=INVITATION_NOTE_MAX_CHARS,
            )
            validation = validate_message(message, voice_signature, INVITATION_NOTE_MAX_CHARS)
        except Exception as e:
            logger.warning(f"Fix stage failed: {e}")

    # Last resort: regenerate from scratch if still invalid
    if not validation.is_valid:
        logger.info(f"Fix failed, regenerating from scratch: {validation.issues}")
        try:
            result = await generate_message(
                prospect=prospect_data,
                sender_profile=sender_profile,
                voice_signature=voice_signature,
                campaign_context=campaign_context,
                prospect_analysis=prospect_analysis,
                campaign_ctx=campaign_ctx,
                conversation_history=conversation_history,
            )
            message = result["message"]
            message = await improve_message(
                draft=message,
                voice_signature=voice_signature,
                message_type="invitation",
                max_chars=INVITATION_NOTE_MAX_CHARS,
            )
            validation = validate_message(message, voice_signature, INVITATION_NOTE_MAX_CHARS)
        except Exception as e:
            logger.error(f"Regeneration failed: {e}")

    if not validation or not validation.is_valid:
        issues_text = "\n".join(f"  ⚠️ {issue}" for issue in (validation.issues if validation else []))
        if mode == "autopilot":
            # CRITICAL: Never send invalid messages in autopilot mode
            logger.warning(f"Autopilot blocked invalid message: {issues_text}")
            await adb.log_action("validation_blocked", outreach_id=outreach_id, result="blocked",
                       details={"issues": validation.issues if validation else []})
            await _release_claim()
            return (
                f"⚠️ Message for {prospect.get('name', 'Unknown')} failed validation "
                f"after Generate → Improve → Fix pipeline.\n\n"
                f"Issues:\n{issues_text}\n\n"
                "The message was NOT sent to protect your account.\n"
                "Check message validation errors and try again."
            )
        else:
            # Copilot: user will see warnings and decide
            logger.warning(f"Copilot message has validation warnings: {issues_text}")

    # ── Step 4: Copilot vs Autopilot ──
    prospect_name = prospect.get("name", "Unknown")
    prospect_title = prospect.get("title", "")
    prospect_company = prospect.get("company", "")
    prospect_url = prospect.get("linkedin_url", "")
    fit_score = prospect.get("fit_score", 0)

    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company

    # Send immediately
    if not can_send:
        await adb.update_outreach(outreach_id, status="pending", next_action=message)
        return f"⏸️ Queued for later: {reason}"

    # ── EMAIL CHANNEL PATH ──
    if channel == CHANNEL_EMAIL:
        return await _send_email_outreach(
            client, account_id, outreach_id, prospect, prospect_data,
            prospect_name, role_str, message, voice_signature,
            campaign_context, campaign_ctx, prospect_analysis,
        )

    # ── DM CHANNEL PATH (connections-only campaigns) ──
    if channel == "dm":
        provider_id = prospect_data.get("provider_id", "")
        # Fallback: extract provider_id from miniProfileUrn in LinkedIn URL
        # (same logic as send_followup.py lines 284-292).
        if not provider_id or not provider_id.startswith("ACo"):
            url = prospect.get("linkedin_url") or prospect_data.get("linkedin_url") or ""
            if url:
                from urllib.parse import urlparse, parse_qs, unquote
                qs = parse_qs(urlparse(url).query)
                urn = unquote(qs.get("miniProfileUrn", [""])[0])
                if urn:
                    extracted = urn.split(":")[-1]
                    if extracted.startswith("ACo"):
                        logger.info("Extracted provider_id from miniProfileUrn for %s", prospect_name)
                        provider_id = extracted
        if not provider_id or not provider_id.startswith("ACo"):
            slug = prospect.get("linkedin_id", "") or prospect_data.get("public_id", "")
            logger.warning(
                "No valid provider_id (ACoAAA) for %s — only have slug '%s'. Cannot send DM.",
                prospect_name, slug,
            )
            await adb.update_outreach(outreach_id, status="error",
                            last_attempt_error=f"No valid provider_id for DM (only slug: {slug})")
            await client.close()
            return f"❌ No valid provider_id for {prospect_name}. Need ACoAAA format for DMs."

        try:
            result = await client.send_new_message(
                account_id=account_id,
                provider_id=provider_id,
                text=message,
            )
            if result.get("success"):
                # Inline read-back verification: confirm the DM actually
                # appeared in the conversation before updating status.
                dm_chat_id = result.get("chat_id", "")
                dm_verified = True  # default to trusted if no chat_id
                if dm_chat_id:
                    try:
                        dm_verified = await client.verify_message_sent(
                            account_id, dm_chat_id, message,
                        )
                    except Exception as e:
                        logger.warning("DM verification error for %s: %s", prospect_name, e)
                        dm_verified = True  # fail open — trust API response

                if not dm_verified:
                    logger.warning(
                        "DM to %s not confirmed in conversation (chat=%s)",
                        prospect_name, dm_chat_id,
                    )
                    await adb.update_outreach(outreach_id,
                                    last_attempt_error="DM delivery not confirmed")
                    await adb.log_action("dm_unverified", outreach_id=outreach_id,
                               result="warning",
                               details={"prospect": prospect_name,
                                        "chat_id": dm_chat_id})
                    await _release_claim()
                    await client.close()
                    return (
                        f"⚠️ DM to {prospect_name} was not confirmed as delivered.\n"
                        f"The API returned success but the message was not found "
                        f"in the conversation. Will retry on next scheduler tick."
                    )

                await adb.update_outreach(outreach_id, status="messaged", channel="linkedin",
                                last_attempt_error=None, followup_count=1)
                # Persist provider_id into contact's profile_json so that
                # check_replies can match future messages by provider_id.
                # Search results often lack provider_id, causing reply
                # detection to fail for DM-only / connections-only campaigns.
                if provider_id and contact_id:
                    try:
                        def _backfill_provider_id(cid: str, prov_id: str) -> None:
                            from ..db.schema import get_db as _get_db_pj
                            _db = _get_db_pj()
                            _r = _db.execute(
                                "SELECT profile_json FROM contacts WHERE id = ?",
                                (cid,),
                            ).fetchone()
                            if _r and _r["profile_json"]:
                                pj = json.loads(_r["profile_json"])
                                if not pj.get("provider_id"):
                                    pj["provider_id"] = prov_id
                                    _db.execute(
                                        "UPDATE contacts SET profile_json = ? WHERE id = ?",
                                        (json.dumps(pj), cid),
                                    )
                                    _db.commit()
                            _db.close()
                        await run_db(_backfill_provider_id, contact_id, provider_id)
                    except Exception:
                        pass  # Non-critical — don't break DM flow
                local_msg_id = await adb.save_message(outreach_id, role="sdr", text=message)
                await adb.increment_usage("messages_sent")
                await adb.log_action("dm_sent", outreach_id=outreach_id, result="success",
                           details={"prospect": prospect_name,
                                     "message_length": len(message),
                                     "verified": True})
                # Schedule async post-send re-verification for extra confidence
                if dm_chat_id:
                    from ..services.engagement_verifier import schedule_post_send_verify
                    schedule_post_send_verify(
                        account_id=account_id, chat_id=dm_chat_id,
                        sent_text=message, outreach_id=outreach_id,
                        local_message_id=local_msg_id, message_type="dm",
                        voice_signature=voice_signature,
                    )
                await client.close()
                return (
                    f"✅ DM sent to {prospect_name} ({role_str})\n"
                    f'   "{message}"\n'
                )
            else:
                error = result.get("error", "Unknown error")
                # Permanent failures (subscription_required, not connected)
                # should mark the outreach as error to stop retries
                if result.get("permanent"):
                    await adb.update_outreach(outreach_id, status="error",
                                    last_attempt_error=error)
                    await adb.log_action("dm_permanent_failure", outreach_id=outreach_id,
                               result="error", details={"prospect": prospect_name,
                                                        "error": error[:200]})
                else:
                    await _release_claim()
                    await adb.update_outreach(outreach_id, last_attempt_error=error)
                await client.close()
                return f"❌ DM failed for {prospect_name}: {error}"
        except Exception as e:
            await _release_claim()
            await adb.update_outreach(outreach_id, last_attempt_error=str(e))
            await client.close()
            return f"❌ DM failed for {prospect_name}: {e}"

    # ── LINKEDIN CHANNEL PATH ──
    # Guard: skip company pages — they can't receive connection invitations
    first_name = prospect_data.get("first_name", "")
    last_name = prospect_data.get("last_name", "")
    _pname = (prospect_data.get("name") or prospect.get("name", "")).strip()
    _pcompany = (prospect_data.get("company") or prospect.get("company", "")).strip()
    is_likely_company = (
        (not first_name and not last_name and _pname and _pcompany and _pname.lower() == _pcompany.lower())
        or prospect_data.get("is_company", False)
    )
    if is_likely_company:
        await adb.update_outreach(outreach_id, status="skipped",
                        last_attempt_error="Skipped: company page, not a person")
        await adb.log_action("invitation_company_skip", outreach_id=outreach_id,
                   result="skipped", details={"prospect": _pname})
        await client.close()
        return f"Skipped {_pname}: looks like a company page, not a person."

    # Get the provider_id for Unipile invitation
    provider_id = (
        prospect_data.get("provider_id", "")
        or prospect.get("linkedin_id", "")
        or prospect_data.get("public_id", "")
    )
    if not provider_id:
        await adb.update_outreach(outreach_id, status="error")
        await client.close()
        return f"❌ No LinkedIn ID for {prospect_name}. Skipping."

    # Guard: validate provider_id format — Unipile expects ACoAAA… or a slug,
    # bare numeric IDs (e.g. "2488212") cause 400 "User ID does not match
    # provider's expected format".
    if provider_id.isdigit():
        # Try to extract a valid provider_id from profile enrichment
        _enriched_pid = prospect_data.get("provider_id", "")
        _public_id = prospect_data.get("public_id", "")
        if _enriched_pid and not _enriched_pid.isdigit():
            provider_id = _enriched_pid
        elif _public_id and not _public_id.isdigit():
            provider_id = _public_id
        else:
            await adb.update_outreach(outreach_id, status="error",
                            last_attempt_error=f"Invalid provider_id format: {provider_id} (numeric-only)")
            await adb.log_action("invitation_bad_id", outreach_id=outreach_id,
                       result="error", details={"provider_id": provider_id, "prospect": prospect_name})
            await client.close()
            return f"❌ Invalid LinkedIn ID format for {prospect_name} ({provider_id}). Needs ACoAAA or slug format."

    # Track invite attempt
    try:
        current = await adb.get_outreach(outreach_id) or {}
        attempts = (current.get("invite_attempts") or 0) + 1
        await adb.update_outreach(outreach_id, invite_attempts=attempts)
    except Exception:
        attempts = 1

    # Circuit-breaker: skip after too many failed attempts
    from ..constants import MAX_INVITE_ATTEMPTS
    if attempts > MAX_INVITE_ATTEMPTS:
        await adb.update_outreach(outreach_id, status="skipped",
                        last_attempt_error=f"Exceeded {MAX_INVITE_ATTEMPTS} invite attempts")
        await adb.log_action("invitation_max_attempts", outreach_id=outreach_id,
                   result="skipped", details={"attempts": attempts, "prospect": prospect_name})
        await client.close()
        return f"Skipped {prospect_name}: exceeded {MAX_INVITE_ATTEMPTS} invite attempts."

    # ── Final connection guard: check local connections DB ──
    try:
        from ..services.connection_sync import is_first_degree, is_first_degree_by_public_id, mark_connected
        clean_prov_id = (prospect_data.get("provider_id") or "").strip()
        clean_pub_id = (prospect_data.get("public_id") or prospect.get("linkedin_id", "")).strip()
        is_connected = False
        matched_by = ""
        if clean_prov_id and await run_db(is_first_degree, account_id, clean_prov_id):
            is_connected = True
            matched_by = f"provider_id={clean_prov_id}"
        elif clean_pub_id and await run_db(is_first_degree_by_public_id, account_id, clean_pub_id):
            is_connected = True
            matched_by = f"public_id={clean_pub_id}"
        if is_connected:
            await run_db(mark_connected, account_id, clean_prov_id or provider_id, prospect_name, clean_pub_id)
            await adb.update_outreach(outreach_id, status="connected", channel=CHANNEL_LINKEDIN)
            await adb.log_action("pre_send_connection_guard", outreach_id=outreach_id,
                       result="connected",
                       details={"prospect": prospect_name, "matched_by": matched_by})
            logger.info("Connection guard caught %s (%s) — skipping invitation", prospect_name, matched_by)
            return (
                f"Already connected with {prospect_name} "
                f"(detected via local connections DB) — skipping invitation, queued for follow-up DM."
            )
    except Exception as e:
        logger.warning("Connection guard check failed (non-blocking): %s", e)

    # Live connection check via Unipile API — catches connections not yet
    # in the local DB (e.g. accepted between sync intervals).
    try:
        relation = await client.check_existing_relation(account_id, provider_id)
        if relation.get("connected") or relation.get("has_chat"):
            import time as _time
            await adb.update_outreach(outreach_id, status="connected", channel=CHANNEL_LINKEDIN, accepted_at=int(_time.time()))
            await adb.log_action("pre_send_api_guard", outreach_id=outreach_id,
                       result="connected",
                       details={"prospect": prospect_name, "source": "unipile_api"})
            await client.close()
            return (
                f"ℹ️ {prospect_name} is already a 1st-degree connection.\n"
                "Skipping invitation — use send_followup() to send a DM."
            )
        if relation.get("pending_invite"):
            await adb.update_outreach(outreach_id, status="invited")
            await client.close()
            return f"ℹ️ {prospect_name} already has a pending invitation. Skipping."
    except Exception as e:
        logger.debug("Live connection check failed for %s: %s — proceeding with invitation", prospect_name, e)

    # Send the invitation via Unipile
    result = await client.send_invitation(
        account_id=account_id,
        provider_id=provider_id,
        message=message,
    )

    try:
        # Update rate limits
        await adb.increment_sent()
        new_limit = await update_limits_after_send(blocked=result.get("blocked", False))

        if result["success"]:
            # Update DB
            await adb.update_outreach(outreach_id, status="invited", channel=CHANNEL_LINKEDIN, last_attempt_error=None)
            await adb.save_message(outreach_id, role="sdr", text=message)
            await adb.increment_usage("invitations_sent")
            await adb.log_action("invitation_sent", outreach_id=outreach_id, result="success",
                       details={
                           "prospect": prospect_name,
                           "message_length": len(message),
                           "invitation_id": result.get("invitation_id", ""),
                           "response_status": result.get("response_status", ""),
                       })
            # Invalidate pending invitation cache after successful send
            from ..linkedin.rate_limiter import invalidate_pending_cache
            invalidate_pending_cache()

            delay = get_next_delay()
            delay_minutes = delay // 60

            return (
                f"✅ Sent to {prospect_name} ({role_str})\n"
                f'   "{message}"\n\n'
                f"⏱️ Next send in ~{delay_minutes} minutes\n"
                f"📊 Daily limit: {new_limit}/day"
            )
        else:
            error = result.get("error", "Unknown error")
            if result.get("auth_error"):
                # Account disconnected — don't change outreach status, just alert user
                await adb.update_outreach(outreach_id, status="pending")
                await adb.log_action("auth_error", outreach_id=outreach_id, result="blocked",
                           details={"error": error})
                return (
                    "🔑 LinkedIn account disconnected.\n\n"
                    "Run setup_profile() again to reconnect your LinkedIn account."
                )
            elif result.get("rate_limited_422"):
                # 422 temporary_provider_limit — LinkedIn restricts personalized
                # invites (weekly limit or non-Sales Navigator). Retry without message.
                if message:
                    await adb.log_action("invitation_retry_no_message", outreach_id=outreach_id,
                               result="retrying", details={"error": error})
                    result2 = await client.send_invitation(
                        account_id=account_id,
                        provider_id=provider_id,
                        message="",
                    )
                    if result2["success"]:
                        await adb.update_outreach(outreach_id, status="invited", channel=CHANNEL_LINKEDIN,
                                        last_attempt_error=None)
                        await adb.save_message(outreach_id, role="sdr", text="")
                        await adb.increment_usage("invitations_sent")
                        await adb.log_action("invitation_sent", outreach_id=outreach_id, result="success",
                                   details={"prospect": prospect_name, "message_length": 0,
                                            "note": "retried without message (422 rate limit)"})
                        return (
                            f"✅ Sent to {prospect_name} (without personalized message)\n"
                            f"   LinkedIn restricted personalized invites — sent blank invite.\n\n"
                            f"📊 Daily limit: {new_limit}/day"
                        )
                    # Retry also failed — treat as rate limit block
                    error = result2.get("error", error)
                # No message or retry also failed: keep as pending, don't skip
                await adb.update_outreach(outreach_id, status="pending", last_attempt_error=error[:500])
                await adb.log_action("invitation_blocked", outreach_id=outreach_id, result="blocked",
                           details={"error": error, "note": "422 weekly/personalized limit"})
                return (
                    f"⚠️ LinkedIn invitation limit (422): {error}\n\n"
                    f"Daily limit reduced to {new_limit}. Will retry later."
                )
            elif result.get("blocked"):
                await adb.update_outreach(outreach_id, status="pending", last_attempt_error=error[:500])
                await adb.log_action("invitation_blocked", outreach_id=outreach_id, result="blocked",
                           details={"error": error})
                return (
                    f"⚠️ LinkedIn blocked the send: {error}\n\n"
                    f"Daily limit reduced to {new_limit}. Will retry later."
                )
            elif "already connected" in str(error).lower() or "invitation pending" in str(error).lower():
                # 409 = already connected or invitation pending — mark as connected
                from ..services.connection_sync import mark_connected
                await run_db(mark_connected, account_id, provider_id, prospect_name)
                await adb.update_outreach(outreach_id, status="connected", channel=CHANNEL_LINKEDIN,
                                last_attempt_error=None)
                await adb.log_action("already_connected_409", outreach_id=outreach_id, result="connected",
                           details={"prospect": prospect_name, "error": error})
                return (
                    f"Already connected with {prospect_name} — queued for follow-up DM."
                )
            elif "422" in str(error):
                # 422 = invalid profile or permanently rejected — don't retry
                await adb.update_outreach(outreach_id, status="skipped", last_attempt_error=error[:500])
                await adb.log_action("invitation_permanent_error", outreach_id=outreach_id, result="skipped",
                           details={"error": error, "attempts": attempts})
                return f"Skipped {prospect_name}: permanent error (422) — {error}"
            else:
                await adb.update_outreach(outreach_id, status="error", last_attempt_error=error[:500])
                await adb.log_action("invitation_failed", outreach_id=outreach_id, result="error",
                           details={"error": error})
                return f"❌ Send failed for {prospect_name}: {error}"
    finally:
        await client.close()


async def _send_email_outreach(
    client: Any,
    account_id: str,
    outreach_id: str,
    prospect: dict,
    prospect_data: dict,
    prospect_name: str,
    role_str: str,
    linkedin_message: str,
    voice_signature: dict,
    campaign_context: dict,
    campaign_ctx: dict | None,
    prospect_analysis: dict | None,
) -> str:
    """Send outreach via email channel instead of LinkedIn.

    Generates a proper email (subject + body) and sends via connected email account.
    """
    from ..ai.email_generator import generate_email
    from ..services.channel_selector import get_email_account_id

    email_account_id = get_email_account_id()
    if not email_account_id:
        await client.close()
        return "❌ No email account connected. Connect email via setup_profile."

    # Extract prospect email
    prospect_email = _extract_email(prospect) or _extract_email(prospect_data)
    if not prospect_email:
        # Can't send email without an address — fall back to LinkedIn
        await client.close()
        return (
            f"❌ No email address found for {prospect_name}.\n\n"
            "Email outreach requires a prospect email. Falling back to LinkedIn.\n"
            "Run generate_and_send() again (will use LinkedIn)."
        )

    # Generate email
    sender_profile = await adb.get_setting("profile", {})
    full_ctx = dict(campaign_context)
    if campaign_ctx:
        full_ctx.update(campaign_ctx)

    try:
        email_result = await generate_email(
            prospect=prospect_data,
            sender_profile=sender_profile,
            voice_signature=voice_signature,
            campaign_context=full_ctx,
            prospect_analysis=prospect_analysis,
        )
    except Exception as e:
        await client.close()
        return f"❌ Email generation failed: {e}"

    subject = email_result["subject"]
    body = email_result["body"]

    # Send via Unipile email API
    try:
        result = await client.send_email(
            account_id=email_account_id,
            to_email=prospect_email,
            to_name=prospect_name,
            subject=subject,
            body=body,
            tracking_label=f"campaign_{outreach_id[:8]}",
        )
    except Exception as e:
        await client.close()
        return f"❌ Email send failed: {e}"
    finally:
        await client.close()

    if result.get("success"):
        await adb.update_outreach(outreach_id, status="invited", channel=CHANNEL_EMAIL)
        await adb.save_message(outreach_id, role="sdr", text=f"[EMAIL] Subject: {subject}\n\n{body}")
        await adb.increment_usage("invitations_sent")
        # Track email-specific rate limit
        from ..linkedin.rate_limiter import increment_email_sent as _inc_email
        await _inc_email()
        await adb.log_action(
            "email_sent", outreach_id=outreach_id, result="success",
            details={
                "prospect": prospect_name,
                "email": prospect_email,
                "subject": subject,
                "channel": "email",
            },
        )
        return (
            f"📧 Email sent to {prospect_name} ({role_str})\n"
            f"   To: {prospect_email}\n"
            f"   Subject: {subject}\n"
            f'   Body: "{body[:150]}..."\n\n'
            "Open/click tracking enabled."
        )
    else:
        error = result.get("error", "Unknown error")
        await adb.update_outreach(outreach_id, status="error")
        await adb.log_action(
            "email_failed", outreach_id=outreach_id, result="error",
            details={"error": error, "channel": "email"},
        )
        return f"❌ Email failed for {prospect_name}: {error}"
