"""Tool: send_followup — Generate and send follow-up DMs after connection acceptance.

Core follow-up loop:
1. Find next "connected" outreach that needs a follow-up
2. Load conversation history
3. Resolve chat_id (prospect's linkedin_id → Unipile chat)
4. Generate personalized follow-up via 3-stage pipeline
5. In Copilot mode: show for approval. In Autopilot: send immediately.
6. Update outreach status and followup_count
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from ..ai.followup_generator import generate_followup, FOLLOWUP_MAX_CHARS
from ..ai.llm_validator import llm_validate
from ..ai.message_fixer import fix_message
from ..ai.message_improver import improve_message
from ..ai.message_validator import validate_followup
from ..ai.prospect_analyzer import analyze_prospect
from ..config import get_tier
from ..constants import (
    COPILOT_APPROVAL_THRESHOLD,
    FREE_MAX_FOLLOWUPS,
    FREE_MONTHLY_MESSAGES,
    PRO_FOLLOWUP_SCHEDULE_DAYS,
    PRO_MAX_FOLLOWUPS,
    TIER_PRO,
)
from ..db import aio as db
from ..db.async_bridge import run_db
from ..formatter import stars
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)

logger = logging.getLogger(__name__)


async def run_send_followup(
    campaign_id: str = "",
    outreach_id: str = "",
    mode: str = "autopilot",
    format: str = "text",
) -> str:
    """Generate and send (or queue) a personalized follow-up DM.

    Flow:
    1. Find the active campaign and next "connected" outreach
    2. Check tier limits and follow-up schedule
    3. Load conversation history and resolve chat_id
    4. Generate follow-up using voice signature
    5. Validate the message (follow-up pipeline)
    6. Copilot: show for review. Autopilot: send directly.

    Args:
        format: "text" (default) or "voice" (generates audio via Hume TTS).
    """

    # ── Step 0: Pre-checks ──
    setup_done = await db.get_setting("setup_complete", False)
    if not setup_done:
        return (
            "Setup required before sending follow-ups.\n\n"
            "Please run setup_profile first."
        )

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected. Run setup_profile first."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"{e}"

    # ── Step 1: Find campaign + follow-up candidate ──
    tier = get_tier()
    max_followups = PRO_MAX_FOLLOWUPS if tier == TIER_PRO else FREE_MAX_FOLLOWUPS

    if outreach_id:
        # Specific outreach requested
        outreach = await db.get_outreach(outreach_id)
        if not outreach:
            await client.close()
            return f"Outreach not found: {outreach_id}"
        if outreach["status"] != "connected":
            await client.close()
            return (
                f"Outreach status is '{outreach['status']}', not 'connected'.\n"
                "Follow-ups can only be sent to connected prospects."
            )
        if outreach.get("followup_count", 0) >= max_followups:
            await client.close()
            return (
                f"Max follow-ups reached ({max_followups}) for this outreach.\n"
                f"{'Upgrade to Pro for up to 5 follow-ups.' if tier != TIER_PRO else 'Maximum follow-ups sent.'}"
            )
        campaign = await db.get_campaign(outreach["campaign_id"])
        if not campaign:
            await client.close()
            return "Campaign not found for this outreach."
        campaign_id = campaign["id"]
        candidate = await db.get_outreach_with_contact(outreach_id)
        if not candidate:
            await client.close()
            return "Could not load contact data for this outreach."
    else:
        # Find campaign
        campaign, err = await db.find_active_campaign(campaign_id)
        if not campaign:
            await client.close()
            return err
        campaign_id = campaign["id"]

        # Block sends when campaign is paused
        if campaign.get("status") == "paused":
            await client.close()
            return (
                f"Campaign '{campaign['name']}' is paused.\n\n"
                "No messages will be sent while the campaign is paused.\n"
                "Use resume_campaign() to resume outreach."
            )

        # Find next follow-up candidate
        candidates = await db.get_followup_candidates(campaign_id, max_followups)
        if not candidates:
            # Log detailed breakdown of why no candidates are eligible
            breakdown = await db.get_followup_breakdown(campaign_id, max_followups)
            await db.log_action(
                "followup_no_candidates",
                result="skipped",
                details={
                    "campaign_id": campaign_id,
                    "campaign_name": campaign["name"],
                    "total_connected_messaged": breakdown["total"],
                    "eligible": breakdown["eligible"],
                    "maxed_out": breakdown["maxed_out"],
                    "max_followups": breakdown["max_followups"],
                    "distribution": breakdown["distribution"],
                    "by_status": breakdown["by_status"],
                    "reason": (
                        "no connected/messaged prospects"
                        if breakdown["total"] == 0
                        else f"all {breakdown['maxed_out']} maxed out at {max_followups} followups"
                        if breakdown["eligible"] == 0
                        else "eligible but filtered by delay schedule"
                    ),
                },
            )
            logger.info(
                "No followup candidates for '%s': total=%d, eligible=%d, maxed=%d",
                campaign["name"],
                breakdown["total"],
                breakdown["eligible"],
                breakdown["maxed_out"],
            )
            await client.close()
            return (
                f"No prospects ready for follow-up in '{campaign['name']}'.\n\n"
                "Prospects need to accept your connection first (status: 'connected').\n"
                "Use check_replies() to detect new connections, or generate_and_send() "
                "to reach new prospects."
            )
        candidate = candidates[0]
        outreach_id = candidate["outreach_id"]

    # ── Exclusion gate: skip contacts excluded from automation ──
    from ..db.global_contact_queries import is_excluded_by_contact_id
    _cid = candidate.get("contact_id", "")
    if _cid and await run_db(is_excluded_by_contact_id, _cid):
        await client.close()
        return (
            f"Skipped {candidate.get('name', 'Unknown')} — excluded from automation.\n\n"
            "This contact has the 'do-not-automate' tag or 'do_not_contact' lifecycle.\n"
            "Remove the tag with contacts(action='tag', tag='-do-not-automate') to re-enable."
        )

    # ── Step 2: Check tier limits ──
    if tier != TIER_PRO:
        usage = await db.get_monthly_usage()
        if usage.get("messages_sent", 0) >= FREE_MONTHLY_MESSAGES:
            await client.close()
            return (
                f"Free tier limit reached: {FREE_MONTHLY_MESSAGES} messages/month.\n\n"
                "Upgrade to Pro ($29/mo) for unlimited follow-ups."
            )

    # ── Step 3: Check follow-up schedule ──
    # Minimum 1-day delay between ANY messages (including the first DM).
    # Pro tier uses the full escalating schedule for subsequent follow-ups.
    MIN_MESSAGE_GAP_DAYS = 1
    followup_count = candidate.get("followup_count", 0)

    # Check last actual message timestamp from DB (more reliable than updated_at)
    last_sdr_ts = 0
    try:
        def _fetch_last_sdr_ts(oid: str) -> int:
            from ..db.schema import get_db as _get_db_ts
            _ts_db = _get_db_ts()
            _ts_row = _ts_db.execute(
                "SELECT MAX(timestamp) as last_ts FROM messages WHERE outreach_id = ? AND role = 'sdr'",
                (oid,),
            ).fetchone()
            _ts_db.close()
            if _ts_row and _ts_row["last_ts"]:
                return _ts_row["last_ts"]
            return 0

        last_sdr_ts = await run_db(_fetch_last_sdr_ts, outreach_id)
    except Exception:
        pass

    # Fallback to outreach updated_at if no message timestamps
    if not last_sdr_ts:
        outreach_data = await db.get_outreach(outreach_id) or {}
        last_sdr_ts = outreach_data.get("updated_at", 0)

    days_since_last = (int(time.time()) - last_sdr_ts) // 86400 if last_sdr_ts else 999

    # Determine required delay
    if tier == TIER_PRO and followup_count > 0:
        schedule_idx = min(followup_count, len(PRO_FOLLOWUP_SCHEDULE_DAYS) - 1)
        required_days = PRO_FOLLOWUP_SCHEDULE_DAYS[schedule_idx]
    else:
        required_days = MIN_MESSAGE_GAP_DAYS

    if days_since_last < required_days:
        wait_days = required_days - days_since_last
        await db.log_action(
            "followup_delay_pending",
            outreach_id=outreach_id,
            result="skipped",
            details={
                "prospect_name": candidate.get("name", "Unknown"),
                "followup_number": followup_count + 1,
                "days_since_last": days_since_last,
                "required_days": required_days,
                "wait_days": wait_days,
                "schedule": PRO_FOLLOWUP_SCHEDULE_DAYS,
            },
        )
        logger.info(
            "Followup #%d for %s delayed: %dd since last, need %dd (wait %dd)",
            followup_count + 1,
            candidate.get("name", "?"),
            days_since_last,
            required_days,
            wait_days,
        )
        await client.close()
        return (
            f"Too early for follow-up #{followup_count + 1}.\n\n"
            f"Schedule: wait {required_days} days between follow-ups.\n"
            f"Last message was {days_since_last} day(s) ago.\n"
            f"Next follow-up in {wait_days} day{'s' if wait_days != 1 else ''}."
        )

    # ── Step 4: Resolve chat_id ──
    # Prefer provider_id (ACoAAA format) from profile_json — that's what
    # chat attendees use.  Fall back to linkedin_id (public_id / slug).
    prospect_linkedin_id = ""
    pj = candidate.get("profile_json")
    if pj:
        try:
            import json as _json
            _profile = _json.loads(pj) if isinstance(pj, str) else pj
            prospect_linkedin_id = _profile.get("provider_id", "")
        except Exception:
            pass
    if not prospect_linkedin_id:
        prospect_linkedin_id = candidate.get("linkedin_id", "")
    if not prospect_linkedin_id:
        await client.close()
        return f"No LinkedIn ID for {candidate.get('name', 'Unknown')}. Cannot send DM."

    try:
        chat_id = await client.find_chat_for_user(account_id, prospect_linkedin_id)
    except Exception as e:
        logger.error(f"Failed to find chat: {e}")
        chat_id = None

    # No existing chat — will create one when sending (first DM after acceptance).
    # Flag so the send step uses send_new_message() instead of send_message().
    create_new_chat = chat_id is None

    # For new chats, we need the provider_id (not the public slug).
    # Extract from miniProfileUrn in the LinkedIn URL if available.
    prospect_provider_id = prospect_linkedin_id
    if create_new_chat and not prospect_linkedin_id.startswith("ACo"):
        url = candidate.get("linkedin_url") or ""
        from urllib.parse import urlparse, parse_qs, unquote
        qs = parse_qs(urlparse(url).query)
        urn = unquote(qs.get("miniProfileUrn", [""])[0])
        if urn:
            prospect_provider_id = urn.split(":")[-1]

    # ── Step 5: Load conversation history (enriched with LinkedIn) ──
    sender_provider_id = (await db.get_setting("profile", {})).get("provider_id", "")
    if chat_id and sender_provider_id:
        try:
            from ..services.conversation_enricher import get_enriched_conversation
            messages = await get_enriched_conversation(
                client, account_id, chat_id, outreach_id, sender_provider_id,
            )
        except Exception as e:
            logger.warning("Conversation enrichment failed, using local-only: %s", e)
            messages = await db.get_messages_for_outreach(outreach_id)
    else:
        messages = await db.get_messages_for_outreach(outreach_id)

    # ── Step 5a: Hard message cap — never exceed MAX messages per prospect ──
    MAX_SDR_MESSAGES_PER_PROSPECT = 3
    existing_sdr_msgs = [m for m in await db.get_messages_for_outreach(outreach_id) if m.get("role") == "sdr"]
    if len(existing_sdr_msgs) >= MAX_SDR_MESSAGES_PER_PROSPECT:
        await client.close()
        await db.log_action(
            "followup_cap_reached",
            outreach_id=outreach_id,
            result="skipped",
            details={"sent": len(existing_sdr_msgs), "limit": MAX_SDR_MESSAGES_PER_PROSPECT},
        )
        return (
            f"⏭️ Message cap reached for {candidate.get('name', 'Unknown')} "
            f"({len(existing_sdr_msgs)}/{MAX_SDR_MESSAGES_PER_PROSPECT} messages sent)."
        )

    # ── Step 5b: Pre-send safety — abort if prospect ever messaged us ──
    # Check for ANY prospect message in the conversation, not just the most recent.
    # This catches inbound leads who messaged first (e.g. months ago) — we shouldn't
    # pile automated follow-ups on top of their messages.
    prospect_msgs = [m for m in messages if m.get("role") == "prospect"]
    if prospect_msgs:
        last_prospect_text = prospect_msgs[-1].get("text", "")[:100]
        await client.close()
        await db.log_action(
            "followup_skipped_prospect_replied",
            outreach_id=outreach_id,
            result="skipped",
            details={
                "prospect_messages": len(prospect_msgs),
                "last_prospect_msg": last_prospect_text,
            },
        )
        # Update status so scheduler stops trying to follow up
        outreach_data_check = await db.get_outreach(outreach_id) or {}
        if outreach_data_check.get("status") in ("connected", "messaged"):
            await db.update_outreach(outreach_id, status="replied")
        return (
            f"⏭️ Skipped follow-up for {candidate.get('name', 'Unknown')} — "
            f"prospect has {len(prospect_msgs)} message(s) in conversation.\n"
            f"   Last from them: \"{last_prospect_text}\"\n"
            f"Use send_message(action='reply') to respond."
        )

    # ── Step 6: Generate follow-up message ──
    sender_profile = await db.get_setting("profile", {})
    voice_signature = await db.get_setting("voice_signature", {})
    campaign_config = json.loads(campaign.get("config_json") or "{}")
    icp_data = json.loads(campaign.get("icp_json") or "{}")

    campaign_context = {
        "target_description": campaign_config.get("target_description", ""),
        "relevance_hook": icp_data.get("relevance_hook", ""),
        "booking_link": campaign_config.get("booking_link", ""),
    }

    # Load campaign context (offerings, case_studies, social_proofs, preferences)
    campaign_ctx = await db.get_campaign_context(campaign_id)

    prospect_data = json.loads(candidate.get("profile_json", "{}")) if candidate.get("profile_json") else {
        "name": candidate.get("name", ""),
        "title": candidate.get("title", ""),
        "company": candidate.get("company", ""),
        "headline": f"{candidate.get('title', '')} at {candidate.get('company', '')}",
    }

    # ── Prospect Intelligence: load cached or generate ──
    prospect_analysis = None
    contact_db_id = candidate.get("contact_id") or candidate.get("contact_db_id", "")
    if contact_db_id:
        prospect_analysis = await db.get_contact_analysis(contact_db_id)
    if not prospect_analysis:
        try:
            prospect_analysis = await analyze_prospect(
                prospect=prospect_data,
                campaign_context=campaign_context,
                icp_data=icp_data,
            )
            if contact_db_id:
                await db.save_contact_analysis(contact_db_id, prospect_analysis)
        except Exception as e:
            logger.warning(f"Prospect analysis failed, proceeding without: {e}")

    # Format conversation history for the generator
    conversation_history = [
        {"role": m["role"], "text": m["text"]}
        for m in messages
    ]

    # ── Generate → Improve → Validate → Fix pipeline ──
    message = ""
    reasoning = {}
    validation = None
    previous_sdr_messages = [m["text"] for m in messages if m.get("role") == "sdr"]

    # Attempt 1: Generate + Improve + Validate (+ Fix if needed)
    memory_entry = None
    try:
        result = await generate_followup(
            prospect=prospect_data,
            sender_profile=sender_profile,
            voice_signature=voice_signature,
            campaign_context=campaign_context,
            conversation_history=conversation_history,
            followup_number=followup_count + 1,
            prospect_analysis=prospect_analysis,
            campaign_ctx=campaign_ctx,
            outreach_id=outreach_id,
        )
        message = result.get("message", "")
        reasoning = result.get("reasoning", {})
        memory_entry = result.get("memory_entry")
    except Exception as e:
        logger.error(f"Follow-up generation failed: {e}")
        await client.close()
        return f"Failed to generate follow-up: {e}"

    # Improve stage — polish for naturalness
    try:
        message = await improve_message(
            draft=message,
            voice_signature=voice_signature,
            message_type="followup",
            max_chars=FOLLOWUP_MAX_CHARS,
        )
    except Exception as e:
        logger.warning(f"Improve stage failed, using raw message: {e}")

    # Validate (rule-based)
    validation = validate_followup(
        message,
        voice_signature,
        previous_messages=previous_sdr_messages,
        max_chars=FOLLOWUP_MAX_CHARS,
    )

    # LLM validation — context-sensitive checks (v63 validate prompt)
    if validation.is_valid:
        try:
            sender_company = sender_profile.get("company", "")
            llm_result = await llm_validate(
                message=message,
                history=conversation_history,
                company=sender_company,
                calendar_link=campaign_context.get("booking_link", ""),
            )
            if not llm_result.is_valid:
                validation.issues.extend(llm_result.issues)
                validation.is_valid = False
                logger.info("LLM validation caught issues: %s", llm_result.issues)
        except Exception as e:
            logger.warning(f"LLM validation skipped: {e}")

    # Fix stage — if validation failed, surgically fix issues
    if not validation.is_valid:
        logger.info(f"Follow-up validation failed, attempting fix: {validation.issues}")
        try:
            message = await fix_message(
                message=message,
                issues=validation.issues,
                voice_signature=voice_signature,
                message_type="followup",
                max_chars=FOLLOWUP_MAX_CHARS,
            )
            validation = validate_followup(
                message,
                voice_signature,
                previous_messages=previous_sdr_messages,
                max_chars=FOLLOWUP_MAX_CHARS,
            )
        except Exception as e:
            logger.warning(f"Fix stage failed: {e}")

    # Last resort: regenerate from scratch if still invalid
    if not validation.is_valid:
        logger.info(f"Fix failed, regenerating follow-up from scratch: {validation.issues}")
        try:
            result = await generate_followup(
                prospect=prospect_data,
                sender_profile=sender_profile,
                voice_signature=voice_signature,
                campaign_context=campaign_context,
                conversation_history=conversation_history,
                followup_number=followup_count + 1,
                prospect_analysis=prospect_analysis,
                campaign_ctx=campaign_ctx,
                outreach_id=outreach_id,
            )
            message = result.get("message", "")
            reasoning = result.get("reasoning", {})
            memory_entry = result.get("memory_entry")
            message = await improve_message(
                draft=message,
                voice_signature=voice_signature,
                message_type="followup",
                max_chars=FOLLOWUP_MAX_CHARS,
            )
            validation = validate_followup(
                message,
                voice_signature,
                previous_messages=previous_sdr_messages,
                max_chars=FOLLOWUP_MAX_CHARS,
            )
        except Exception as e:
            logger.error(f"Regeneration failed: {e}")

    if not validation or not validation.is_valid:
        issues_text = "\n".join(f"  ⚠️ {issue}" for issue in (validation.issues if validation else []))
        if mode == "autopilot":
            logger.warning(f"Autopilot blocked invalid follow-up: {issues_text}")
            await db.log_action("validation_blocked", outreach_id=outreach_id, result="blocked",
                       details={"issues": validation.issues if validation else [], "type": "followup"})
            await client.close()
            return (
                f"⚠️ Follow-up for {candidate.get('name', 'Unknown')} failed validation "
                f"after Generate → Improve → Fix pipeline.\n\n"
                f"Issues:\n{issues_text}\n\n"
                "The message was NOT sent to protect your account.\n"
                "Try: send_followup(mode='copilot') to review and edit manually."
            )
        else:
            logger.warning(f"Copilot follow-up has validation warnings: {issues_text}")

    # ── Step 7: Copilot vs Autopilot ──
    prospect_name = candidate.get("name", "Unknown")
    prospect_title = candidate.get("title", "")
    prospect_company = candidate.get("company", "")
    fit_score = candidate.get("fit_score", 0)

    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company

    if False:  # copilot mode removed
        # Show message for review
        await db.update_outreach(outreach_id, next_action=message)

        output = [
            f"Follow-up #{followup_count + 1} for **{prospect_name}** ({role_str}):",
            f"   Fit: {stars(fit_score)}",
            "",
            f'   "{message}"',
            f"   ({len(message)}/{FOLLOWUP_MAX_CHARS} chars)",
            "",
        ]

        # Show reasoning
        if reasoning:
            hook = reasoning.get("hook", "")
            cta = reasoning.get("cta_choice", "")
            if hook:
                output.append(f"   Angle: {hook}")
            if cta:
                output.append(f"   CTA type: {cta}")
            output.append("")

        # Show validation warnings
        if validation and validation.warnings:
            for w in validation.warnings:
                output.append(f"   {w}")
            output.append("")

        output.extend([
            "Send this? Reply with:",
            "  'yes' / 'send' to send this follow-up",
            "  'skip' to skip this prospect",
            "  'edit: [your text]' to send a custom message instead",
            "  'stop' to pause the campaign",
        ])

        await client.close()
        return "\n".join(line for line in output if line is not None)

    else:
        # Autopilot — send immediately

        # ── Optimistic lock: claim this outreach atomically ──
        # Prevents duplicate follow-ups when multiple scheduler jobs target the same prospect.
        # CAS: only succeeds if status is still 'connected' or 'messaged'.
        # 'messaged' is needed for DM-only campaigns and subsequent follow-ups.
        def _try_claim_followup(oid: str) -> tuple[str, int]:
            from ..db.schema import get_db as _get_db_lock
            lock_db = _get_db_lock()
            pre_lock_row = lock_db.execute(
                "SELECT status FROM outreaches WHERE id = ?", (oid,),
            ).fetchone()
            pre_status = pre_lock_row["status"] if pre_lock_row else "connected"
            rows = lock_db.execute(
                "UPDATE outreaches SET status = 'sending_followup' WHERE id = ? AND status IN ('connected', 'messaged')",
                (oid,),
            ).rowcount
            lock_db.commit()
            lock_db.close()
            return pre_status, rows

        pre_lock_status, claimed = await run_db(_try_claim_followup, outreach_id)
        if not claimed:
            logger.info("Outreach %s already claimed by another follow-up job, skipping", outreach_id)
            await client.close()
            return "Prospect already being processed by another follow-up job. Skipping."

        async def _release_followup_claim() -> None:
            """Release the optimistic lock on failure — reset status to pre-lock value."""
            try:
                def _do_release(oid: str, orig_st: str) -> None:
                    from ..db.schema import get_db as _get_db_rel
                    rel_db = _get_db_rel()
                    rel_db.execute(
                        "UPDATE outreaches SET status = ? WHERE id = ? AND status = 'sending_followup'",
                        (orig_st, oid),
                    )
                    rel_db.commit()
                    rel_db.close()
                await run_db(_do_release, outreach_id, pre_lock_status)
            except Exception as e:
                logger.error("Failed to release follow-up claim for %s: %s", outreach_id, e)

        # ── EMAIL FOLLOW-UP PATH ──
        outreach_record = await db.get_outreach(outreach_id)
        outreach_channel = (outreach_record or {}).get("channel", "linkedin")
        if outreach_channel == "email":
            result = await _send_email_followup(
                client, account_id, outreach_id, candidate,
                prospect_name, role_str, message, followup_count,
                max_followups, voice_signature, reasoning, memory_entry,
            )
            # Release lock if email send failed (success path sets status="messaged")
            if result and ("failed" in result.lower() or "error" in result.lower()):
                await _release_followup_claim()
            return result

        # ── Pre-send connection check (mirrors generate_send.py) ──
        # Verify prospect is actually a 1st-degree connection before DM.
        # Without this, stale connections table entries cause 403 subscription_required.
        from ..services.connection_sync import (
            is_first_degree,
            is_first_degree_by_public_id,
            sync_connections,
            get_sync_age,
        )
        dm_prov_id = (prospect_provider_id or "").strip()
        dm_pub_id = (candidate.get("linkedin_id") or candidate.get("public_id") or "").strip()

        # Re-sync connections if older than 30 min
        try:
            sync_age = await run_db(get_sync_age, account_id)
            if sync_age is None or sync_age > 1800:
                await sync_connections(client, account_id)
        except Exception as e:
            logger.warning("Connection re-sync before follow-up DM failed: %s", e)

        _followup_connected = False
        if dm_prov_id and await run_db(is_first_degree, account_id, dm_prov_id):
            _followup_connected = True
        elif dm_pub_id and await run_db(is_first_degree_by_public_id, account_id, dm_pub_id):
            _followup_connected = True

        if not _followup_connected:
            reason = f"provider_id={dm_prov_id}, public_id={dm_pub_id}"
            error_msg = f"Not in local 1st-degree connections ({reason})"
            await _release_followup_claim()
            await db.update_outreach(outreach_id, status="error",
                            last_attempt_error=error_msg)
            await db.log_action("dm_not_connected", outreach_id=outreach_id,
                       result="error",
                       details={"prospect": prospect_name, "reason": reason})
            logger.warning("Blocking follow-up DM to %s — not in local connections DB (%s)",
                           prospect_name, reason)
            await client.close()
            return (
                f"⏭️ Skipped follow-up to {prospect_name} — "
                f"not found in local 1st-degree connections. "
                f"Marked as error to avoid 403."
            )

        # ── LINKEDIN DM PATH ──
        actual_format = "text"
        audio_path = ""
        if format == "voice":
            try:
                from ..ai.voice_memo_generator import generate_voice_memo, cleanup_voice_memo
                from ..config import is_voice_memo_enabled
                if is_voice_memo_enabled():
                    voice_result = await generate_voice_memo(
                        message,
                        voice_signature=voice_signature,
                        humanize=campaign_config.get("voice_humanize", True),
                        noise_type=campaign_config.get("voice_noise_type", "auto"),
                        noise_volume=campaign_config.get("voice_noise_volume", "subtle"),
                    )
                    if voice_result.get("success"):
                        audio_path = voice_result["audio_path"]
                        actual_format = "voice"
                    else:
                        logger.warning("Voice gen failed (%s), falling back to text", voice_result.get("error"))
            except Exception as e:
                logger.warning("Voice gen error (%s), falling back to text", e)

        try:
            if actual_format == "voice" and audio_path:
                if create_new_chat:
                    send_result = await client.send_new_voice_message(
                        account_id=account_id,
                        provider_id=prospect_provider_id,
                        audio_path=audio_path,
                    )
                else:
                    send_result = await client.send_voice_message(
                        account_id=account_id,
                        chat_id=chat_id,
                        audio_path=audio_path,
                    )
                # If voice send failed, fall back to text
                if not send_result.get("success"):
                    logger.warning("Voice send failed (%s), falling back to text", send_result.get("error"))
                    actual_format = "text"

            if actual_format == "text":
                if create_new_chat:
                    send_result = await client.send_new_message(
                        account_id=account_id,
                        provider_id=prospect_provider_id,
                        text=message,
                    )
                else:
                    send_result = await client.send_message(
                        account_id=account_id,
                        chat_id=chat_id,
                        text=message,
                    )
        except UnipileAuthError:
            await _release_followup_claim()
            await client.close()
            if audio_path:
                try:
                    from ..ai.voice_memo_generator import cleanup_voice_memo
                    cleanup_voice_memo(audio_path)
                except Exception:
                    pass
            return (
                "LinkedIn account disconnected.\n\n"
                "Run setup_profile() again to reconnect."
            )
        except Exception as e:
            await _release_followup_claim()
            await client.close()
            if audio_path:
                try:
                    from ..ai.voice_memo_generator import cleanup_voice_memo
                    cleanup_voice_memo(audio_path)
                except Exception:
                    pass
            return f"Failed to send follow-up: {e}"
        finally:
            await client.close()
            if audio_path:
                try:
                    from ..ai.voice_memo_generator import cleanup_voice_memo
                    cleanup_voice_memo(audio_path)
                except Exception:
                    pass

        if send_result.get("success"):
            # Verify the DM was actually delivered by reading back the conversation.
            # DMs can only be sent to 1st-degree connections — if delivery fails
            # silently we must not count it.
            verify_chat_id = chat_id
            if create_new_chat and send_result.get("chat_id"):
                verify_chat_id = send_result["chat_id"]
            dm_verified = False
            if verify_chat_id and actual_format == "text":
                try:
                    dm_verified = await client.verify_message_sent(
                        account_id, verify_chat_id, message,
                    )
                except Exception as e:
                    logger.warning("DM verification error: %s", e)
            else:
                # Voice messages can't be text-verified; trust the API response
                dm_verified = True

            if not dm_verified:
                logger.warning(
                    "DM to %s not confirmed in conversation (chat_id=%s)",
                    prospect_name, verify_chat_id,
                )
                await db.update_outreach(
                    outreach_id,
                    last_attempt_error="DM delivery not confirmed — message not found in conversation",
                )
                await db.log_action(
                    "followup_delivery_failed",
                    outreach_id=outreach_id,
                    result="unverified",
                    details={
                        "prospect": prospect_name,
                        "chat_id": verify_chat_id or "",
                        "message_id": send_result.get("message_id", ""),
                    },
                )
                return (
                    f"⚠️ DM to {prospect_name} was not confirmed as delivered.\n"
                    "The API accepted the request but the message was not found "
                    "in the conversation. Will retry on next run."
                )

            # Update DB — delivery confirmed
            new_count = followup_count + 1
            await db.update_outreach(outreach_id, status="messaged", followup_count=new_count, last_attempt_error=None)
            local_msg_id = await db.save_message(outreach_id, role="sdr", text=message, format=actual_format)
            await db.increment_usage("messages_sent")

            # Save conversation memory for future follow-ups
            if memory_entry:
                try:
                    await db.save_outreach_memory(outreach_id, memory_entry)
                except Exception as e:
                    logger.debug("Memory save failed: %s", e)
            await db.log_action(
                "followup_sent",
                outreach_id=outreach_id,
                result="success",
                details={
                    "prospect": prospect_name,
                    "followup_number": new_count,
                    "message_length": len(message),
                    "reasoning": reasoning,
                    "message_id": send_result.get("message_id", ""),
                    "verified": True,
                },
            )

            # Post-send background verification (garble check + auto-delete)
            if actual_format == "text" and verify_chat_id:
                from ..services.engagement_verifier import schedule_post_send_verify
                schedule_post_send_verify(
                    account_id=account_id, chat_id=verify_chat_id,
                    sent_text=message, outreach_id=outreach_id,
                    local_message_id=local_msg_id, message_type="followup",
                    voice_signature=voice_signature,
                )

            remaining = max_followups - new_count
            return (
                f"Sent follow-up #{new_count} to {prospect_name} ({role_str})\n"
                f'   "{message}"\n\n'
                f"Follow-ups remaining: {remaining}/{max_followups}"
            )
        else:
            await _release_followup_claim()
            error = send_result.get("error", "Unknown error")
            await db.log_action(
                "followup_failed",
                outreach_id=outreach_id,
                result="error",
                details={"error": error},
            )
            return f"Follow-up failed for {prospect_name}: {error}"


async def _send_email_followup(
    client: Any,
    account_id: str,
    outreach_id: str,
    candidate: dict,
    prospect_name: str,
    role_str: str,
    message: str,
    followup_count: int,
    max_followups: int,
    voice_signature: dict,
    reasoning: str,
    memory_entry: dict | None,
) -> str:
    """Send a follow-up via email channel."""
    from ..ai.email_generator import generate_email_followup
    from ..services.channel_selector import get_email_account_id, _extract_email

    email_account_id = get_email_account_id()
    if not email_account_id:
        await client.close()
        return "No email account connected for follow-up."

    prospect_email = _extract_email(candidate)
    if not prospect_email:
        await client.close()
        return f"No email address for {prospect_name}. Cannot send email follow-up."

    # Get previous email subject from messages
    previous_messages = await db.get_messages_for_outreach(outreach_id)
    previous_subject = ""
    previous_body = ""
    for msg in previous_messages:
        if msg.get("role") == "sdr":
            text = msg.get("text", "")
            if text.startswith("[EMAIL] Subject: "):
                lines = text.split("\n\n", 1)
                previous_subject = lines[0].replace("[EMAIL] Subject: ", "")
                previous_body = lines[1] if len(lines) > 1 else ""
            break

    sender_profile = await db.get_setting("profile", {})
    try:
        email_result = await generate_email_followup(
            prospect={"name": prospect_name, **candidate},
            sender_profile=sender_profile,
            voice_signature=voice_signature,
            previous_subject=previous_subject,
            previous_body=previous_body,
            followup_count=followup_count,
        )
    except Exception as e:
        await client.close()
        return f"Email follow-up generation failed: {e}"

    subject = email_result["subject"]
    body = email_result["body"]

    try:
        result = await client.send_email(
            account_id=email_account_id,
            to_email=prospect_email,
            to_name=prospect_name,
            subject=subject,
            body=body,
        )
    except Exception as e:
        await client.close()
        return f"Email follow-up send failed: {e}"
    finally:
        await client.close()

    if result.get("success"):
        new_count = followup_count + 1
        await db.update_outreach(outreach_id, status="messaged", followup_count=new_count)
        await db.save_message(outreach_id, role="sdr", text=f"[EMAIL] Subject: {subject}\n\n{body}")
        await db.increment_usage("messages_sent")

        if memory_entry:
            try:
                await db.save_outreach_memory(outreach_id, memory_entry)
            except Exception:
                pass

        await db.log_action(
            "email_followup_sent", outreach_id=outreach_id, result="success",
            details={
                "prospect": prospect_name,
                "followup_number": new_count,
                "channel": "email",
                "subject": subject,
            },
        )

        remaining = max_followups - new_count
        return (
            f"📧 Email follow-up #{new_count} sent to {prospect_name} ({role_str})\n"
            f"   Subject: {subject}\n"
            f'   Body: "{body[:120]}..."\n\n'
            f"Follow-ups remaining: {remaining}/{max_followups}"
        )
    else:
        error = result.get("error", "Unknown error")
        await db.log_action(
            "email_followup_failed", outreach_id=outreach_id, result="error",
            details={"error": error, "channel": "email"},
        )
        return f"Email follow-up failed for {prospect_name}: {error}"
