"""Unified Inbound Pipeline v2 — Classify-First Architecture.

Single-pass pipeline that handles 100% of inbound traffic:
1. DETECT  — Fetch invitations + messages, save as inbound_signals
2. CLASSIFY — AI qualification on every new signal BEFORE any action
3. ACT     — Accept/ignore/decline invitations, respond/react to messages
4. TRACK   — Create outreaches, log actions

Replaces the old accept-first approach where all invitations were
accepted immediately and qualified later.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ..ai.inbound_qualifier import (
    InboundQualification,
    generate_discovery_question,
    qualify_inbound,
)
from ..ai.reply_pipeline import run_reply_pipeline
from ..ai.sentiment import classify_sentiment
from ..constants import (
    INBOUND_MAX_DM_ATTEMPTS,
)
from ..db.async_bridge import run_db
from ..db.queries import (
    count_inbound_dms_today,
    create_outreach,
    get_inbound_signal_by_sender,
    get_messages_for_outreach,
    get_setting,
    list_icps,
    list_inbound_signals,
    log_action,
    save_contact,
    save_inbound_signal,
    save_message,
    save_setting,
    update_inbound_signal,
    update_outreach,
)
from ..db.signal_queries import (
    get_contact_by_linkedin_id,
    get_contact_by_name_company,
    get_contact_by_provider_id,
)

logger = logging.getLogger(__name__)

# ── Configurable thresholds ──────────────────────────────────────────────────

INBOUND_ACCEPT_CONFIDENCE = 0.4   # Min confidence to accept an invitation
INBOUND_DECLINE_SPAM = False       # If True, actively decline spam (default: ignore)
DAILY_INBOUND_ACCEPT_LIMIT = 50   # Max invitations to accept per day


# ── Main Entry Point ─────────────────────────────────────────────────────────

async def process_inbound_pipeline() -> str:
    """Single-pass unified inbound processor.

    1. DETECT: Fetch all inbound signals (invitations, messages)
    2. CLASSIFY: Run AI qualification on every new signal BEFORE any action
    3. ACT: Accept/ignore/decline invitations, respond/react to messages
    4. TRACK: Update DB state, create outreaches, log everything

    Returns a summary string.
    """
    from ..linkedin import UnipileError, get_account_id, get_linkedin_client

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"LinkedIn client error: {e}"

    try:
        # ── DETECT ──
        inv_count = await _detect_invitations(client, account_id)
        msg_count = await _detect_messages(client, account_id)

        # ── CLASSIFY ──
        classified = await _classify_all_new()

        # ── ACT ──
        inv_summary = await _act_on_invitations(client, account_id)
        msg_summary = await _act_on_messages(client, account_id)

        # ── Record scan timestamp for next run's time filter ──
        await run_db(save_setting, "last_inbound_scan_ts", int(time.time()))

        # ── Summary ──
        parts = []
        if inv_count or msg_count:
            parts.append(f"Detected: {inv_count} invitations, {msg_count} messages")
        if classified:
            parts.append(f"Classified: {classified}")
        if inv_summary:
            parts.append(f"Invitations: {inv_summary}")
        if msg_summary:
            parts.append(f"Messages: {msg_summary}")

        return " | ".join(parts) if parts else "No inbound activity."

    except Exception as e:
        logger.error("Inbound pipeline error: %s", e, exc_info=True)
        return f"Inbound pipeline error: {e}"
    finally:
        await client.close()


# ── DETECT ───────────────────────────────────────────────────────────────────

async def _detect_invitations(client: Any, account_id: str) -> int:
    """Fetch received invitations and save new ones as inbound_signals."""
    try:
        invitations = await client.get_received_invitations(account_id)
    except Exception as e:
        logger.warning("Failed to fetch invitations: %s", e)
        return 0

    saved = 0
    for inv in invitations:
        inv_id = inv.get("id", "")
        sender_id = inv.get("sender_id", "")
        if not inv_id or not sender_id:
            continue

        # Dedup by sender_id
        existing = await run_db(get_inbound_signal_by_sender, sender_id, "invitation")
        if existing:
            continue

        await run_db(
            save_inbound_signal,
            signal_type="invitation",
            sender_name=inv.get("sender_name", ""),
            sender_id=sender_id,
            sender_headline=inv.get("headline", ""),
            content=inv.get("message", ""),
            invitation_id=inv_id,
        )
        saved += 1

    if saved:
        logger.info("Detected %d new inbound invitations", saved)
    return saved


async def _detect_messages(client: Any, account_id: str) -> int:
    """Fetch recent messages and save unsolicited ones as inbound_signals.

    Filters out:
    - Our own sent messages (by LinkedIn provider_id)
    - Messages older than last scan (time-based dedup)
    - Senders with existing active inbound signals
    - Known campaign contacts (by linkedin_id or provider_id)
    - Empty messages
    """
    try:
        messages = await client.list_all_messages(account_id, limit=50)
    except Exception as e:
        logger.warning("Failed to list all messages: %s", e)
        return 0

    if not messages:
        return 0

    logger.info("Inbound detect: %d messages fetched from API", len(messages))

    # Resolve our LinkedIn provider_id for own-message filtering.
    # account_id is a Unipile UUID — sender_id is a LinkedIn provider_id (ACoAAA format).
    profile = await run_db(get_setting, "profile", {})
    our_provider_id = ""
    if isinstance(profile, dict):
        our_provider_id = profile.get("provider_id", "")
    if not our_provider_id:
        logger.warning(
            "Inbound detect: no provider_id in profile setting — "
            "own-message filter disabled, false positives possible"
        )

    # Time-based filtering: skip messages older than last scan.
    last_scan_ts = await run_db(get_setting, "last_inbound_scan_ts", 0)
    if not last_scan_ts:
        last_scan_ts = int(time.time()) - 3600  # Default: last hour

    # Skip counters for logging
    skip_own = 0
    skip_old = 0
    skip_signal = 0
    skip_contact = 0
    skip_empty = 0

    saved = 0
    for msg in messages:
        sender_id = msg.get("sender_id", "")
        if not sender_id:
            continue

        # Skip our own sent messages
        if our_provider_id and sender_id == our_provider_id:
            skip_own += 1
            continue

        # Skip messages older than last scan
        msg_ts = msg.get("timestamp", 0)
        if msg_ts and msg_ts <= last_scan_ts:
            skip_old += 1
            continue

        # Skip if this sender already has an inbound signal in ANY active state
        # (check without signal_type filter — a sender who came in as an
        # invitation and was already engaged should NOT be re-detected as a
        # new "message" signal, which caused duplicate discovery DMs).
        existing = await run_db(get_inbound_signal_by_sender, sender_id)
        if existing:
            status = existing.get("status", "")
            if status in ("new", "classified", "accepted", "engaged"):
                skip_signal += 1
                continue
            # For dismissed/ignored/declined: allow re-detection if message is NEW
            existing_content = (existing.get("content") or "").strip()
            new_content = (msg.get("text") or "").strip()
            if existing_content == new_content:
                skip_signal += 1
                continue

        # Known campaign contact — re-activate instead of skipping
        contact = await run_db(get_contact_by_linkedin_id, sender_id)
        if not contact:
            contact = await run_db(get_contact_by_provider_id, sender_id)
        if contact:
            text = msg.get("text", "")
            if text:
                await _reactivate_existing_contact(contact, sender_id, text)
            skip_contact += 1
            continue

        text = msg.get("text", "")
        if not text:
            skip_empty += 1
            continue

        message_id = msg.get("message_id", "")

        await run_db(
            save_inbound_signal,
            signal_type="message",
            sender_name=msg.get("sender_name", ""),
            sender_id=sender_id,
            content=text,
            message_id=message_id,
        )
        saved += 1

    total_skipped = skip_own + skip_old + skip_signal + skip_contact + skip_empty
    logger.info(
        "Inbound detect: %d from API, %d skipped "
        "(own=%d old=%d signal=%d contact=%d empty=%d), %d new signals saved",
        len(messages), total_skipped,
        skip_own, skip_old, skip_signal, skip_contact, skip_empty, saved,
    )
    return saved


async def _reactivate_existing_contact(
    contact: dict[str, Any],
    sender_id: str,
    text: str,
) -> None:
    """Re-activate an existing campaign contact who sent a new message.

    Finds their outreach, updates status to 'replied' or 'hot_lead',
    saves the prospect message, and queues an auto-reply job so the
    scheduler sends a response within 5-15 minutes.
    """
    import random

    from ..constants import AUTO_REPLY_DELAY_MAX, AUTO_REPLY_DELAY_MIN, JOB_AUTO_REPLY
    from ..db.queries import create_scheduler_job, get_pending_outreach_job
    from ..db.schema import get_db

    contact_id = contact.get("id", "")
    if not contact_id:
        return

    # Find the most recent outreach for this contact
    def _find_outreach() -> dict | None:
        db = get_db()
        row = db.execute(
            """SELECT id, status, campaign_id FROM outreaches
               WHERE contact_id = ?
               ORDER BY updated_at DESC LIMIT 1""",
            (contact_id,),
        ).fetchone()
        db.close()
        return dict(row) if row else None

    outreach = await run_db(_find_outreach)
    if not outreach:
        return

    outreach_id = outreach["id"]
    old_status = outreach["status"]

    # Don't re-activate opted_out contacts
    if old_status == "opted_out":
        return

    # Dedup: check if we already saved this exact message
    existing_msgs = await run_db(get_messages_for_outreach, outreach_id)
    if existing_msgs:
        for m in reversed(existing_msgs):
            if m.get("role") == "prospect":
                if m.get("text", "").strip() == text.strip():
                    return  # Already processed
                break

    # Classify sentiment
    sentiment = "neutral"
    try:
        sentiment = await classify_sentiment(text)
    except Exception:
        pass

    # Map sentiment to status
    if sentiment == "opt_out":
        await run_db(update_outreach, outreach_id, status="opted_out")
        return

    new_status = "hot_lead" if sentiment == "positive" else "replied"

    # Re-activate if in a dormant/terminal status
    REACTIVATABLE = (
        "pending", "error", "closed_happy", "closed_unhappy", "exhausted",
        "messaged", "connected", "invited", "sending", "sending_followup",
        "replied", "hot_lead",
    )
    if old_status in REACTIVATABLE:
        await run_db(update_outreach, outreach_id, status=new_status)

    # Save the prospect message
    await run_db(save_message, outreach_id, role="prospect", text=text, sentiment=sentiment)

    # Don't auto-reply to positive/calendar — these prospects want meetings,
    # so the user should decide which ones to take (avoid committing to
    # unwanted meetings autonomously).
    if sentiment in ("positive", "calendar"):
        logger.info(
            "Skipping auto-reply for outreach %s — %s sentiment requires user decision",
            outreach_id[:8], sentiment,
        )
        await run_db(
            log_action,
            "auto_reply_skipped_meeting_intent",
            outreach_id=outreach_id,
            result="skipped",
            details={
                "contact_name": contact.get("name", ""),
                "sentiment": sentiment,
                "reason": "prospect wants a meeting — user should decide",
            },
        )
        # Still log the reactivation below, just skip the auto-reply
        await run_db(
            log_action,
            "outreach_reactivated_inbound",
            outreach_id=outreach_id,
            result="success",
            details={
                "contact_name": contact.get("name", ""),
                "previous_status": old_status,
                "new_status": new_status,
                "sentiment": sentiment,
                "text_preview": text[:100],
                "auto_reply": False,
            },
        )
        logger.info(
            "Re-activated outreach %s for contact %s (%s -> %s, sentiment=%s, no auto-reply)",
            outreach_id[:8], contact.get("name", ""), old_status, new_status, sentiment,
        )
        return

    # Queue auto-reply job immediately (don't wait for planner to discover it)
    has_pending = await run_db(get_pending_outreach_job, outreach_id, JOB_AUTO_REPLY)
    if not has_pending:
        delay = random.randint(AUTO_REPLY_DELAY_MIN, AUTO_REPLY_DELAY_MAX)
        scheduled_at = int(time.time()) + delay
        await run_db(
            create_scheduler_job,
            campaign_id=outreach.get("campaign_id", ""),
            job_type=JOB_AUTO_REPLY,
            scheduled_at=scheduled_at,
            outreach_id=outreach_id,
        )
        logger.info(
            "Queued auto-reply for reactivated outreach %s (delay=%ds)",
            outreach_id[:8], delay,
        )

    await run_db(
        log_action,
        "outreach_reactivated_inbound",
        outreach_id=outreach_id,
        result="success",
        details={
            "contact_name": contact.get("name", ""),
            "previous_status": old_status,
            "new_status": new_status,
            "sentiment": sentiment,
            "text_preview": text[:100],
        },
    )
    logger.info(
        "Re-activated outreach %s for contact %s (%s -> %s, sentiment=%s)",
        outreach_id[:8], contact.get("name", ""), old_status, new_status, sentiment,
    )


# ── SELLER DETECTION ─────────────────────────────────────────────────────────


async def _detect_seller_signal(signal: dict, content: str) -> None:
    """Check if an inbound prospect is a LinkedIn seller.

    If detected, creates a linkedin_seller signal in the signals table
    so the signal scorer can factor it into lead prioritization.
    """
    try:
        from ..linkedin import get_linkedin_client

        client = get_linkedin_client()
        messages = [content] if isinstance(content, str) else content
        result = await client.classify_seller(
            messages=messages,
            author_name=signal.get("sender_name", ""),
            author_headline=signal.get("sender_headline", ""),
        )

        if result.get("is_seller") and result.get("confidence", 0) >= 0.4:
            from ..constants import SIGNAL_LINKEDIN_SELLER
            from ..db.signal_queries import save_signal

            linkedin_id = signal.get("sender_linkedin_id", "")
            if not linkedin_id:
                return

            import json as _json

            await run_db(
                save_signal,
                SIGNAL_LINKEDIN_SELLER,
                "inbound_pipeline",
                linkedin_id=linkedin_id,
                prospect_name=signal.get("sender_name", ""),
                confidence=result["confidence"],
                metadata_json=_json.dumps({
                    "seller_type": result.get("seller_type", ""),
                    "reasoning": result.get("reasoning", ""),
                    "sender_headline": signal.get("sender_headline", ""),
                }),
            )
            logger.info(
                "Seller signal detected for %s (type=%s, conf=%.2f)",
                signal.get("sender_name", "Unknown"),
                result.get("seller_type", ""),
                result["confidence"],
            )
    except Exception as e:
        # Non-critical — don't block inbound pipeline
        logger.debug("Seller detection failed for %s: %s", signal.get("sender_name"), e)


# ── CLASSIFY ─────────────────────────────────────────────────────────────────

async def _classify_all_new() -> str:
    """Run AI qualification on all new (unclassified) inbound signals.

    Returns summary string.
    """
    new_signals = await run_db(list_inbound_signals, status="new", limit=20)
    if not new_signals:
        return ""

    active_icps = await run_db(list_icps, status="active")

    classified_count = 0
    high_conf = 0

    for signal in new_signals:
        profile = {
            "name": signal.get("sender_name", ""),
            "headline": signal.get("sender_headline", ""),
            "company": signal.get("sender_company", ""),
            "title": signal.get("sender_headline", ""),
        }
        content = signal.get("content", "")
        signal_type = signal.get("signal_type", "invitation")

        try:
            qual = await qualify_inbound(
                profile=profile,
                content=content,
                signal_type=signal_type,
                active_icps=active_icps,
            )

            # Resolve best-matching campaign
            campaign_id = _resolve_campaign_for_signal(signal)

            await run_db(
                update_inbound_signal,
                signal["id"],
                intent=qual.intent,
                matched_icp_id=qual.matched_icp_id,
                confidence=qual.confidence,
                recommended_action=qual.recommended_action,
                reasoning=qual.reasoning,
                status="classified",
                qualified_at=int(time.time()),
                **({"campaign_id": campaign_id} if campaign_id else {}),
            )
            classified_count += 1
            if qual.confidence >= 0.7:
                high_conf += 1

            # Seller detection — check if prospect does LinkedIn outreach
            if content and len(content) > 50:
                await _detect_seller_signal(signal, content)

        except Exception as e:
            logger.warning(
                "Failed to classify signal %s (%s): %s",
                signal["id"], signal.get("sender_name"), e,
            )

    summary = f"{classified_count}/{len(new_signals)} classified"
    if high_conf:
        summary += f", {high_conf} high-confidence"
    return summary


# ── ACT: Invitations ────────────────────────────────────────────────────────

async def _act_on_invitations(client: Any, account_id: str) -> str:
    """Accept, ignore, or decline invitations based on classification.

    Decision matrix:
    - buying_signal (conf >= 0.4) → Accept + queue for DM
    - networking (conf >= 0.4) → Accept (no DM)
    - partnership (any) → Accept (no DM)
    - unknown (conf >= 0.3) → Accept + monitor
    - unknown (conf < 0.3) → Ignore (leave pending)
    - job_seeking → Dismiss (ignore)
    - spam → Ignore (or decline if INBOUND_DECLINE_SPAM=True)
    - vendor_pitch (conf >= 0.8) → Ignore (or decline)
    - vendor_pitch (conf < 0.8) → Ignore
    """
    classified = await run_db(
        list_inbound_signals, status="classified", signal_type="invitation", limit=DAILY_INBOUND_ACCEPT_LIMIT,
    )
    if not classified:
        return ""

    accepted = 0
    ignored = 0
    declined = 0
    dismissed = 0
    errors = 0

    for signal in classified:
        intent = signal.get("intent", "unknown")
        confidence = signal.get("confidence", 0) or 0
        invitation_id = signal.get("invitation_id", "")
        now = int(time.time())

        # Determine action
        action = _decide_invitation_action(intent, confidence)

        if action == "accept":
            if not invitation_id:
                # No invitation_id — can't accept, mark as accepted anyway
                # (may have been auto-accepted by LinkedIn)
                await run_db(
                    update_inbound_signal, signal["id"],
                    status="accepted", actioned_at=now,
                )
                accepted += 1
                continue

            try:
                result = await client.handle_invitation(
                    account_id, invitation_id, action="accept",
                )
                if result.get("success"):
                    await run_db(
                        update_inbound_signal, signal["id"],
                        status="accepted", actioned_at=now,
                    )
                    await run_db(
                        log_action,
                        "inbound_invitation_accepted",
                        result="success",
                        details={
                            "signal_id": signal["id"],
                            "sender_name": signal.get("sender_name", ""),
                            "intent": intent,
                            "confidence": confidence,
                        },
                    )
                    accepted += 1
                    logger.info(
                        "Accepted invitation from %s (intent=%s, conf=%.2f)",
                        signal.get("sender_name", "Unknown"), intent, confidence,
                    )
                else:
                    error = result.get("error", "unknown")
                    if "not found" in error.lower() or "already" in error.lower():
                        # Already handled — mark as accepted
                        await run_db(
                            update_inbound_signal, signal["id"],
                            status="accepted", actioned_at=now,
                        )
                        accepted += 1
                    else:
                        errors += 1
                        logger.warning("Failed to accept invitation %s: %s", invitation_id, error)
            except Exception as e:
                errors += 1
                logger.warning("Error accepting invitation %s: %s", invitation_id, e)

        elif action == "decline":
            if invitation_id:
                try:
                    result = await client.handle_invitation(
                        account_id, invitation_id, action="decline",
                    )
                    if result.get("success"):
                        await run_db(
                            update_inbound_signal, signal["id"],
                            status="declined",
                            actioned_at=now,
                            decline_reason=f"Auto-declined: {intent} (conf={confidence:.2f})",
                        )
                        await run_db(
                            log_action,
                            "inbound_invitation_declined",
                            result="success",
                            details={
                                "signal_id": signal["id"],
                                "sender_name": signal.get("sender_name", ""),
                                "intent": intent,
                            },
                        )
                        declined += 1
                    else:
                        # Decline failed — fall back to ignore
                        await run_db(
                            update_inbound_signal, signal["id"],
                            status="ignored", actioned_at=now,
                        )
                        ignored += 1
                except Exception:
                    await run_db(
                        update_inbound_signal, signal["id"],
                        status="ignored", actioned_at=now,
                    )
                    ignored += 1
            else:
                await run_db(
                    update_inbound_signal, signal["id"],
                    status="dismissed", actioned_at=now,
                )
                dismissed += 1

        elif action == "dismiss":
            await run_db(
                update_inbound_signal, signal["id"],
                status="dismissed", actioned_at=now,
            )
            dismissed += 1

        else:  # ignore
            await run_db(
                update_inbound_signal, signal["id"],
                status="ignored", actioned_at=now,
            )
            ignored += 1

    parts = []
    if accepted:
        parts.append(f"{accepted} accepted")
    if ignored:
        parts.append(f"{ignored} ignored")
    if declined:
        parts.append(f"{declined} declined")
    if dismissed:
        parts.append(f"{dismissed} dismissed")
    if errors:
        parts.append(f"{errors} errors")
    return ", ".join(parts)


def _decide_invitation_action(intent: str, confidence: float) -> str:
    """Return 'accept', 'ignore', 'decline', or 'dismiss' for an invitation."""
    if intent in ("spam",):
        return "decline" if INBOUND_DECLINE_SPAM else "dismiss"

    if intent in ("vendor_pitch",):
        return "accept"  # Accept vendors — we counter-pitch our product

    if intent in ("job_seeking",):
        return "dismiss"

    if intent in ("buying_signal",):
        return "accept" if confidence >= INBOUND_ACCEPT_CONFIDENCE else "ignore"

    if intent in ("partnership",):
        return "accept"

    if intent in ("networking",):
        return "accept" if confidence >= INBOUND_ACCEPT_CONFIDENCE else "ignore"

    # unknown
    return "accept" if confidence >= 0.3 else "ignore"


# ── ACT: Messages ───────────────────────────────────────────────────────────

async def _act_on_messages(client: Any, account_id: str) -> str:
    """Send discovery DMs and/or reactions for classified inbound signals.

    Handles both invitation-based signals (after acceptance) and
    unsolicited DM signals.

    - High confidence (>= 0.7): send discovery DM immediately
    - Medium confidence (0.4-0.7): send reaction first, then discovery DM
    - Vendor pitch: counter-pitch our product instead of dismissing
    - Spam/job_seeking: dismissed
    """
    # Process accepted invitations that need DMs
    accepted_inv = await run_db(
        list_inbound_signals, status="accepted", limit=20,
    )
    # Process classified messages (unsolicited DMs)
    classified_msg = await run_db(
        list_inbound_signals, status="classified", signal_type="message", limit=20,
    )

    all_signals = (accepted_inv or []) + (classified_msg or [])
    if not all_signals:
        return ""

    voice = await run_db(get_setting, "voice_signature", {})

    sent = 0
    skipped = 0
    errors = 0

    for signal in all_signals:
        intent = signal.get("intent", "unknown")
        confidence = signal.get("confidence", 0) or 0
        sender_id = signal.get("sender_id", "")

        # Skip intents that shouldn't get DMs
        if intent in ("spam", "job_seeking"):
            await run_db(update_inbound_signal, signal["id"], status="dismissed")
            skipped += 1
            continue

        if not sender_id:
            skipped += 1
            continue

        # Skip if already a known campaign contact (re-activation handled in _detect_messages)
        # Check both linkedin_id (public_id format) AND provider_id (ACoAAA format)
        # since sender_id from Unipile is provider_id but contacts.linkedin_id
        # stores public_id — format mismatch caused dedup misses.
        existing_contact = await run_db(get_contact_by_linkedin_id, sender_id)
        if not existing_contact:
            existing_contact = await run_db(get_contact_by_provider_id, sender_id)
        if not existing_contact:
            sender_name = signal.get("sender_name", "")
            sender_company = signal.get("sender_company", "")
            if sender_name and sender_company:
                existing_contact = await run_db(
                    get_contact_by_name_company, sender_name, sender_company,
                )
        if existing_contact:
            skipped += 1
            continue

        # NOTE: Prior conversation guard removed (v0.10.48).
        # Warm inbound leads from existing connections are the most valuable
        # signals — dismissing them because old messages exist was wrong.
        # The AI classifier already filters spam/vendor/job_seeking intents.

        # For medium confidence DMs, send a reaction first
        message_id = signal.get("message_id", "")
        if message_id and 0.4 <= confidence < 0.7:
            try:
                react_result = await client.add_message_reaction(
                    account_id, message_id,
                )
                if react_result.get("success"):
                    await run_db(
                        update_inbound_signal, signal["id"], reaction_sent=1,
                    )
            except Exception as e:
                logger.debug("Reaction failed for message %s: %s (continuing)", message_id, e)

        # Generate and send discovery DM
        result = await _send_discovery_dm(
            client, account_id, signal, voice,
        )
        if result == "sent":
            sent += 1
        elif result == "error":
            errors += 1
        else:
            skipped += 1

    parts = []
    if sent:
        parts.append(f"{sent} DMs sent")
    if skipped:
        parts.append(f"{skipped} skipped")
    if errors:
        parts.append(f"{errors} failed")
    return ", ".join(parts)


async def _send_discovery_dm(
    client: Any,
    account_id: str,
    signal: dict[str, Any],
    voice: dict[str, Any],
) -> str:
    """Generate and send a contextual reply to an inbound signal.

    Instead of a generic discovery question, generates a reply that
    addresses what the person actually said using the user's voice.

    Returns 'sent', 'skipped', or 'error'.
    """
    sender_id = signal.get("sender_id", "")
    intent = signal.get("intent", "unknown")
    confidence = signal.get("confidence", 0) or 0
    content = signal.get("content", "")

    prospect_profile = {
        "name": signal.get("sender_name", ""),
        "headline": signal.get("sender_headline", ""),
        "company": signal.get("sender_company", ""),
        "title": signal.get("sender_headline", ""),
    }

    # ── Step 1: Create contact + outreach BEFORE generating reply ──
    campaign_id = signal.get("campaign_id") or ""
    now = int(time.time())
    outreach_id = ""
    try:
        _sig_type = signal.get("signal_type", "invitation")
        _inbound_src = {
            "invitation": "inbound_invitation",
            "dm": "inbound_dm",
            "message": "inbound_dm",
            "comment": "inbound_comment",
        }.get(_sig_type, "inbound_invitation")

        contact_id = await run_db(
            save_contact,
            campaign_id=campaign_id,
            name=signal.get("sender_name", ""),
            title=signal.get("sender_headline", ""),
            company=signal.get("sender_company", ""),
            linkedin_url=signal.get("sender_url", ""),
            linkedin_id=sender_id,
            source=_inbound_src,
        )

        # Classify sentiment of the inbound message
        sentiment = "neutral"
        if content:
            try:
                sentiment = await classify_sentiment(content)
            except Exception as e:
                logger.debug("Sentiment classification failed: %s", e)

        # Skip opt-outs entirely
        if sentiment == "opt_out":
            await run_db(update_inbound_signal, signal["id"], status="dismissed")
            return "skipped"

        # Map sentiment to outreach status
        status_map = {
            "positive": "hot_lead",
            "question": "replied",
            "negative": "replied",
            "neutral": "replied",
            "out_of_office": "replied",
        }
        initial_status = status_map.get(sentiment, "replied")

        outreach_id = await run_db(
            create_outreach,
            campaign_id=campaign_id,
            contact_id=contact_id,
            status=initial_status,
            signal_id=signal["id"],
        )
        await run_db(update_outreach, outreach_id, accepted_at=now)

        # Save the inbound prospect message with sentiment
        if content:
            await run_db(
                save_message, outreach_id,
                role="prospect", text=content, sentiment=sentiment,
            )
    except Exception as e:
        logger.warning(
            "Failed to create outreach for inbound %s: %s",
            signal.get("sender_name"), e,
        )
        # Continue anyway — try to send the reply even without tracking

    # ── Step 2: Generate contextual reply ──
    try:
        sender_profile = await run_db(get_setting, "profile", {})

        # For vendor pitches, generate a counter-pitch instead of a discovery DM
        if intent == "vendor_pitch" and content:
            from ..ai.inbound_qualifier import generate_counter_pitch
            # Pull campaign context for counter-pitch
            _cp_ctx: dict[str, Any] = {"target_description": "", "relevance_hook": "", "booking_link": ""}
            _cp_campaign_id = signal.get("campaign_id", "")
            if _cp_campaign_id:
                try:
                    from ..db.queries import get_campaign
                    _cp_campaign = await run_db(get_campaign, _cp_campaign_id)
                    if _cp_campaign:
                        import json as _json
                        _cp_raw = _cp_campaign.get("context_json", "")
                        _cp_parsed = {}
                        if _cp_raw:
                            try:
                                _cp_parsed = _json.loads(_cp_raw)
                            except Exception:
                                pass
                        _cp_ctx["target_description"] = _cp_campaign.get("target_description", "")
                        _cp_ctx["relevance_hook"] = _cp_parsed.get("offerings", "") or _cp_parsed.get("company_context_raw", "")
                        _cp_ctx["booking_link"] = _cp_parsed.get("booking_link", "")
                except Exception:
                    pass
            cp_result = await generate_counter_pitch(
                sender_profile=prospect_profile,
                content=content,
                voice=voice,
                campaign_context=_cp_ctx,
            )
            dm_text = cp_result.get("message", "")
        else:
            dm_text = await _generate_contextual_reply(
                prospect=prospect_profile,
                sender_profile=sender_profile,
                voice_signature=voice,
                content=content,
                sentiment=sentiment if content else "neutral",
                signal=signal,
            )
        if not dm_text:
            return "skipped"

        # Strip any trailing email-style signatures ("- Denys", "Best, Denys").
        # Real people don't sign LinkedIn DMs — and counter-pitch / fallback
        # discovery don't go through run_reply_pipeline, so the strip wouldn't
        # otherwise be applied on those paths.
        from ..ai.reply_pipeline import strip_signature
        dm_text = strip_signature(dm_text, sender_profile)
        if not dm_text:
            return "skipped"

        # ── Step 3: Send the reply (with pre-send dedup) ──
        chat_id = await client.find_chat_for_user(account_id, sender_id)
        if chat_id:
            # Pre-send guard: check if we already sent a message in this chat
            # recently. This is the last line of defense against duplicate
            # discovery DMs from concurrent pipeline runs or signal-type mismatches.
            try:
                recent_msgs = await client.get_chat_messages(
                    account_id, chat_id, limit=5,
                )
                our_provider_id = (await run_db(get_setting, "profile", {})).get("provider_id", "")
                if our_provider_id and recent_msgs:
                    for rmsg in recent_msgs:
                        if rmsg.get("sender_id") == our_provider_id:
                            msg_ts = rmsg.get("timestamp", 0)
                            if msg_ts and (int(time.time()) - msg_ts) < 86400:
                                logger.info(
                                    "Pre-send dedup: already sent message to %s in last 24h, skipping",
                                    signal.get("sender_name", sender_id),
                                )
                                await run_db(
                                    update_inbound_signal, signal["id"],
                                    status="engaged", actioned_at=int(time.time()),
                                )
                                return "skipped"
            except Exception as e:
                logger.debug("Pre-send dedup check failed: %s (continuing)", e)

            result = await client.send_message(
                account_id=account_id,
                chat_id=chat_id,
                text=dm_text,
            )
        else:
            result = await client.send_new_message(
                account_id=account_id,
                provider_id=sender_id,
                text=dm_text,
            )

        if result.get("success"):
            # Save SDR reply and update tracking
            if outreach_id:
                await run_db(save_message, outreach_id, role="sdr", text=dm_text)
                await run_db(
                    update_inbound_signal, signal["id"],
                    status="engaged",
                    outreach_id=outreach_id,
                    actioned_at=now,
                )
            else:
                await run_db(
                    update_inbound_signal, signal["id"],
                    status="engaged", actioned_at=now,
                )

            await run_db(
                log_action,
                "inbound_contextual_reply_sent",
                result="success",
                details={
                    "signal_id": signal["id"],
                    "sender_name": signal.get("sender_name", ""),
                    "intent": intent,
                    "confidence": confidence,
                    "sentiment": sentiment if content else "unknown",
                    "dm_text": dm_text[:200],
                },
            )
            return "sent"

        # Send failed — handle DM attempt tracking
        dm_attempts = (signal.get("dm_attempts") or 0) + 1
        if dm_attempts >= INBOUND_MAX_DM_ATTEMPTS:
            await run_db(
                update_inbound_signal, signal["id"],
                status="dismissed", dm_attempts=dm_attempts,
            )
            return "skipped"
        else:
            await run_db(
                update_inbound_signal, signal["id"],
                dm_attempts=dm_attempts,
            )
            return "skipped"

    except Exception as e:
        logger.warning(
            "Failed to send contextual reply to %s: %s",
            signal.get("sender_name"), e,
        )
        return "error"


async def _generate_contextual_reply(
    prospect: dict[str, Any],
    sender_profile: dict[str, Any],
    voice_signature: dict[str, Any],
    content: str,
    sentiment: str,
    signal: dict[str, Any],
) -> str:
    """Generate a contextual reply using the shared reply pipeline.

    Falls back to generate_discovery_question() if reply generation fails.
    """
    if not content:
        return await _fallback_discovery(prospect, voice_signature, signal)

    conversation_history = [{"role": "prospect", "text": content}]

    # Pull campaign context so replies can reference the user's product/company
    campaign_context: dict[str, Any] = {"target_description": "", "relevance_hook": "", "booking_link": ""}
    campaign_id = signal.get("campaign_id", "")
    if campaign_id:
        try:
            from ..db.queries import get_campaign
            campaign = await run_db(get_campaign, campaign_id)
            if campaign:
                import json as _json
                ctx = {}
                ctx_raw = campaign.get("context_json", "")
                if ctx_raw:
                    try:
                        ctx = _json.loads(ctx_raw)
                    except Exception:
                        pass
                campaign_context["target_description"] = campaign.get("target_description", "")
                campaign_context["relevance_hook"] = ctx.get("offerings", "") or ctx.get("company_context_raw", "")
                campaign_context["booking_link"] = ctx.get("booking_link", "")
        except Exception:
            pass

    try:
        dm_text, _, _ = await run_reply_pipeline(
            prospect=prospect,
            sender_profile=sender_profile,
            voice_signature=voice_signature,
            campaign_context=campaign_context,
            conversation_history=conversation_history,
            reply_text=content,
            sentiment=sentiment,
            max_chars=500,
        )
        if not dm_text:
            return await _fallback_discovery(prospect, voice_signature, signal)
        return dm_text

    except Exception as e:
        logger.warning("Contextual reply generation failed: %s — falling back to discovery", e)
        return await _fallback_discovery(prospect, voice_signature, signal)


async def _fallback_discovery(
    prospect: dict[str, Any],
    voice: dict[str, Any],
    signal: dict[str, Any],
) -> str:
    """Fall back to generic discovery question when contextual reply fails."""
    qual = InboundQualification(
        intent=signal.get("intent", "unknown"),
        matched_icp_id=signal.get("matched_icp_id"),
        confidence=signal.get("confidence", 0) or 0,
        recommended_action=signal.get("recommended_action", "ask_purpose"),
        reasoning=signal.get("reasoning", ""),
    )
    try:
        result = await generate_discovery_question(
            sender_profile=prospect,
            signal_type=signal.get("signal_type", "invitation"),
            content=signal.get("content", ""),
            voice=voice,
            qualification=qual,
        )
        return result.get("message", "")
    except Exception as e:
        logger.warning("Discovery question fallback also failed: %s", e)
        return ""


# ── Helpers ──────────────────────────────────────────────────────────────────

# Re-export shared helpers for backward compatibility (used internally and by backfill_inbox)
from .inbound_helpers import has_prior_conversation as _has_prior_conversation  # noqa: E402,F811
from .inbound_helpers import resolve_campaign_for_signal as _resolve_campaign_for_signal  # noqa: E402,F811
