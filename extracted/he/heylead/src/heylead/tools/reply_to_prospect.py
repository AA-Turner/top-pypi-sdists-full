"""Tool: reply_to_prospect — Generate and send sentiment-aware replies to prospect messages.

Core reply loop:
1. Find next outreach needing a reply (hot_lead or replied with prospect message)
2. Load conversation history + last prospect message + sentiment
3. Resolve chat_id (prospect's linkedin_id → Unipile chat)
4. Generate personalized reply via sentiment-specific pipeline
5. In Copilot mode: show for approval. In Autopilot: send immediately.
6. Update outreach status
"""

from __future__ import annotations

import json
import logging
from typing import Any

from ..ai.prospect_analyzer import analyze_prospect
from ..ai.reply_generator import NEGATIVE_MAX_CHARS, REPLY_MAX_CHARS
from ..ai.reply_pipeline import run_reply_pipeline
from ..ai.sentiment import detect_calendar_url
from ..config import get_tier
from ..constants import (
    COPILOT_APPROVAL_THRESHOLD,
    FREE_MONTHLY_MESSAGES,
    TIER_PRO,
)
from ..db.queries import (
    find_active_campaign,
    get_campaign,
    get_campaign_context,
    get_contact_analysis,
    get_inbound_reply_candidates,
    get_messages_for_outreach,
    get_monthly_usage,
    get_outreach,
    get_outreach_with_contact,
    get_reply_candidates,
    get_setting,
    increment_usage,
    log_action,
    save_contact_analysis,
    save_message,
    update_outreach,
)
from ..formatter import stars
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)

SENTIMENT_ICONS = {
    "positive": "\U0001f525",
    "negative": "\U0001f44e",
    "question": "\u2753",
    "neutral": "\U0001f4ac",
    "engaged": "\U0001f4ac",
    "out_of_office": "\u2708\ufe0f",
    "opt_out": "\U0001f6ab",
}

SENTIMENT_LABELS = {
    "positive": "Positive",
    "negative": "Negative",
    "question": "Question",
    "neutral": "Neutral",
    "engaged": "Engaged",
    "out_of_office": "Out of Office",
    "opt_out": "Opt-Out",
}


async def run_reply_to_prospect(
    outreach_id: str = "",
    mode: str = "autopilot",
    format: str = "text",
) -> str:
    """Generate and send (or queue) a sentiment-aware reply to a prospect.

    Flow:
    1. Find the active campaign and next outreach needing a reply
    2. Load conversation history and detect last prospect message
    3. Resolve chat_id
    4. Generate sentiment-aware reply
    5. Validate the reply (reply-specific pipeline)
    6. Copilot: show for review. Autopilot: send directly.

    Args:
        format: "text" (default) or "voice" (generates audio via Hume TTS).
    """

    # ── Step 0: Pre-checks ──
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "Setup required before replying.\n\n"
            "Please run setup_profile first."
        )

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected. Run setup_profile first."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"{e}"

    # ── Step 1: Find outreach needing a reply ──
    campaign = None
    campaign_id = ""

    if outreach_id:
        # Specific outreach requested
        outreach = await run_db(get_outreach, outreach_id)
        if not outreach:
            await client.close()
            return f"Outreach not found: {outreach_id}"
        if outreach["status"] not in ("hot_lead", "replied"):
            await client.close()
            return (
                f"Outreach status is '{outreach['status']}', not 'hot_lead' or 'replied'.\n"
                "Replies can only be sent to prospects who have messaged you.\n"
                "Use check_replies() first to detect new messages."
            )
        # Inbound outreaches have empty campaign_id — that's OK
        if outreach["campaign_id"]:
            campaign = await run_db(get_campaign, outreach["campaign_id"])
            if not campaign:
                await client.close()
                return "Campaign not found for this outreach."
            campaign_id = campaign["id"]
        else:
            campaign = None
            campaign_id = ""
        candidate = await run_db(get_outreach_with_contact, outreach_id)
        if not candidate:
            await client.close()
            return "Could not load contact data for this outreach."
    else:
        # Search ALL active campaigns for reply candidates (not just the first)
        from ..db.queries import list_campaigns
        all_campaigns = await run_db(list_campaigns, status="active")
        candidates = []
        for camp in all_campaigns:
            if camp.get("status") == "paused":
                continue
            camp_candidates = await run_db(get_reply_candidates, camp["id"])
            if camp_candidates:
                candidates = camp_candidates
                campaign = camp
                campaign_id = camp["id"]
                break

        # Also check inbound (campaign-less) outreaches
        if not candidates:
            candidates = await run_db(get_inbound_reply_candidates)

        if not candidates:
            await client.close()
            label = f"in '{campaign['name']}'" if campaign else "across campaigns or inbound"
            return (
                f"No prospects need a reply {label}.\n\n"
                "Prospects must have sent you a message first.\n"
                "Use check_replies() to detect new messages, or "
                "generate_and_send() to reach new prospects."
            )
        candidate = candidates[0]
        outreach_id = candidate["outreach_id"]
        # Update campaign reference from the candidate
        if candidate.get("campaign_id"):
            campaign = await run_db(get_campaign, candidate["campaign_id"])
            campaign_id = candidate["campaign_id"]
        else:
            campaign = None
            campaign_id = ""

    # ── Step 2: Check tier limits ──
    tier = get_tier()
    if tier != TIER_PRO:
        usage = await run_db(get_monthly_usage)
        if usage.get("messages_sent", 0) >= FREE_MONTHLY_MESSAGES:
            await client.close()
            return (
                f"Free tier limit reached: {FREE_MONTHLY_MESSAGES} messages/month.\n\n"
                "Upgrade to Pro ($29/mo) for unlimited messages."
            )

    # ── Step 3: Resolve chat_id ──
    # Prefer provider_id (ACoAAA format) from profile_json — that's what
    # chat attendees use.  Fall back to linkedin_id (public_id / slug).
    prospect_linkedin_id = ""
    pj = candidate.get("profile_json")
    if pj:
        try:
            _profile = json.loads(pj) if isinstance(pj, str) else pj
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

    if not chat_id:
        await client.close()
        # Log the failure so we can retry later. Uses actions_log instead of
        # saving a fake SDR message, which would permanently block the outreach
        # from auto-reply candidates via the NOT EXISTS guard in the query.
        await run_db(log_action, "chat_not_found", outreach_id=outreach_id,
                   result="skipped", details={"prospect": candidate.get("name", "Unknown")})
        return (
            f"Could not find a chat with {candidate.get('name', 'the prospect')}.\n\n"
            "The chat may not have synced yet. Will retry on next scheduler cycle.\n"
            "Try check_replies() to update conversation data."
        )

    # ── Step 3b: Chat-scoped dedup (cross-campaign) ──
    # The outreach-scoped dedup below only sees messages inside THIS outreach.
    # When the same prospect is in multiple campaigns, each campaign's outreach
    # can independently auto-reply to the same LinkedIn chat — e.g. prospect asks
    # "are you a bot?" and gets two bot-sounding replies from two campaigns.
    # Here we query the actual LinkedIn chat and skip if any of our own messages
    # has a timestamp newer than the prospect's latest message in that chat.
    if mode == "autopilot":
        try:
            _our_provider_id = (await run_db(get_setting, "profile", {})).get("provider_id", "")
            if _our_provider_id:
                _recent_chat_msgs = await client.get_chat_messages(
                    account_id, chat_id, limit=10,
                )
                if _recent_chat_msgs:
                    # Last prospect-side message timestamp from the actual chat
                    _last_prospect_ts_chat = 0
                    for _rm in _recent_chat_msgs:
                        if _rm.get("sender_id") and _rm.get("sender_id") != _our_provider_id:
                            _ts = _rm.get("timestamp") or 0
                            if _ts > _last_prospect_ts_chat:
                                _last_prospect_ts_chat = _ts
                    # Any SDR message (from us) newer than that = already replied
                    if _last_prospect_ts_chat:
                        _already_replied = any(
                            _rm.get("sender_id") == _our_provider_id
                            and (_rm.get("timestamp") or 0) > _last_prospect_ts_chat
                            for _rm in _recent_chat_msgs
                        )
                        if _already_replied:
                            await client.close()
                            await run_db(
                                log_action, "reply_dedup_blocked_chat_scoped",
                                outreach_id=outreach_id,
                                result="skipped",
                                details={
                                    "reason": "already_replied_in_linkedin_chat",
                                    "chat_id": chat_id,
                                    "prospect": candidate.get("name", "Unknown"),
                                },
                            )
                            return (
                                f"Already replied to {candidate.get('name', 'Unknown')} "
                                f"in this LinkedIn chat (possibly from another campaign) — skipping."
                            )
        except Exception as e:
            logger.debug("Chat-scoped dedup check failed: %s (continuing)", e)

    # ── Step 4: Load conversation history (enriched with LinkedIn) ──
    sender_provider_id = (await run_db(get_setting, "profile", {})).get("provider_id", "")
    if chat_id and sender_provider_id:
        try:
            from ..services.conversation_enricher import get_enriched_conversation
            messages = await get_enriched_conversation(
                client, account_id, chat_id, outreach_id, sender_provider_id,
            )
        except Exception as e:
            logger.warning("Conversation enrichment failed, using local-only: %s", e)
            messages = await run_db(get_messages_for_outreach, outreach_id)
    else:
        messages = await run_db(get_messages_for_outreach, outreach_id)

    # Safety cap: block reply if last N messages are all from SDR (talking to ourselves).
    # Uses enriched messages (synced with LinkedIn) so prospect replies aren't missed.
    MAX_CONSECUTIVE_SDR = 3
    consecutive_sdr = 0
    for m in reversed(messages):
        if m.get("role") == "sdr":
            consecutive_sdr += 1
        else:
            break
    if consecutive_sdr >= MAX_CONSECUTIVE_SDR:
        await client.close()
        await run_db(log_action, "reply_cap_reached", outreach_id=outreach_id,
                   result="skipped", details={"consecutive_sdr": consecutive_sdr, "limit": MAX_CONSECUTIVE_SDR})
        return (
            f"⏭️ Message cap reached for {candidate.get('name', 'Unknown')} "
            f"({consecutive_sdr} consecutive SDR messages without prospect response)."
        )

    # ── Dedup guard: block if we already replied to the latest prospect message ──
    # Uses LOCAL DB (not enriched/LinkedIn) for consistency during concurrent jobs.
    # This prevents the race where multiple auto-reply jobs fire at the same time
    # and all pass the consecutive-SDR check because none have saved yet.
    if mode == "autopilot":
        local_msgs = await run_db(get_messages_for_outreach, outreach_id)
        _last_prospect_ts = 0
        for m in reversed(local_msgs):
            if m.get("role") == "prospect":
                _last_prospect_ts = m.get("timestamp") or m.get("created_at") or 0
                break
        if _last_prospect_ts:
            _sdr_after_prospect = any(
                m.get("role") == "sdr"
                and (m.get("timestamp") or m.get("created_at") or 0) >= _last_prospect_ts
                for m in local_msgs
            )
            if _sdr_after_prospect:
                await client.close()
                await run_db(log_action, "reply_dedup_blocked", outreach_id=outreach_id,
                           result="skipped", details={"reason": "already_replied_to_last_prospect_msg"})
                return (
                    f"Already replied to {candidate.get('name', 'Unknown')}'s last message — skipping."
                )

    # Find the last prospect message and its sentiment
    last_prospect_msg = None
    for msg in reversed(messages):
        if msg.get("role") == "prospect":
            last_prospect_msg = msg
            break

    if not last_prospect_msg:
        await client.close()
        return (
            f"No prospect message found for this outreach.\n\n"
            "The prospect needs to have sent you a message first.\n"
            "Use check_replies() to detect new messages."
        )

    reply_text = last_prospect_msg.get("text", "")
    sentiment = last_prospect_msg.get("sentiment", "neutral")

    # Read prospect calendar URL stored by check_replies (in outreach.next_action)
    prospect_calendar_url = ""
    next_action_raw = candidate.get("next_action") or ""
    if next_action_raw:
        try:
            _next_action = json.loads(next_action_raw)
            if _next_action.get("type") == "book_meeting":
                prospect_calendar_url = _next_action.get("prospect_calendar_url", "")
        except (json.JSONDecodeError, TypeError):
            pass

    # Calendar intent fallback: if prospect says "check my calendar" and we have
    # a stored calendar URL from an earlier message, force calendar sentiment
    if prospect_calendar_url and sentiment not in ("opt_out", "negative"):
        from ..ai.sentiment import detect_calendar_intent
        if detect_calendar_intent(reply_text) or detect_calendar_url(reply_text):
            sentiment = "calendar"

    # Don't auto-reply to opt_out, out_of_office, or negative sentiment
    if sentiment == "opt_out":
        await client.close()
        return (
            "This prospect has opted out of communication.\n"
            "No reply will be sent. Their outreach has been closed."
        )
    if sentiment == "out_of_office":
        await client.close()
        return (
            "This prospect is out of office.\n"
            "Wait for them to return before replying.\n"
            "Use send_followup() later when they're back."
        )
    if sentiment == "negative" and mode == "autopilot":
        await client.close()
        await run_db(update_outreach, outreach_id, status="opted_out")
        await run_db(log_action, "auto_reply_skipped_negative", outreach_id=outreach_id,
                   result="skipped", details={"text": reply_text[:200]})
        return (
            f"Prospect sent a negative/decline message — skipping auto-reply.\n"
            f"   \"{reply_text[:100]}\"\n"
            "Outreach closed. No further messages will be sent."
        )

    # Keyword-based decline detection (catches misclassified sentiments)
    # Especially important for non-English messages where sentiment may be wrong
    _decline_keywords = [
        "not interested", "no thanks", "no thank you", "don't contact",
        "remove me", "unsubscribe", "stop messaging", "other priorities",
        "не цікавить", "не зацікавлений", "інших пріоритет",  # Ukrainian
        "не интересует", "других приоритет",  # Russian
    ]
    reply_lower = reply_text.lower()
    if mode == "autopilot" and any(kw in reply_lower for kw in _decline_keywords):
        await client.close()
        await run_db(update_outreach, outreach_id, status="opted_out")
        await run_db(log_action, "auto_reply_skipped_decline_keywords", outreach_id=outreach_id,
                   result="skipped", details={"text": reply_text[:200]})
        return (
            f"Prospect's message contains decline keywords — skipping auto-reply.\n"
            f"   \"{reply_text[:100]}\"\n"
            "Outreach closed. No further messages will be sent."
        )

    # Fast vendor-pitch keyword guard (catches obvious pitches before LLM call)
    _vendor_phrases = [
        "we've worked with similar", "how we can do it for you",
        "would love to tell you", "would love to show you",
        "candidates to interview", "turn around on candidates",
        "we can help you", "we can get you",
        "happy to walk you through", "love to walk you through",
        "i can show you how", "i can walk you through",
    ]
    if mode == "autopilot" and any(vp in reply_lower for vp in _vendor_phrases):
        await client.close()
        await run_db(update_outreach, outreach_id, status="reverse_pitch")
        await run_db(log_action, "reverse_pitch_keyword", outreach_id=outreach_id,
                   result="skipped", details={"text": reply_text[:200]})
        return (
            f"Vendor pitch detected (keyword match) from {candidate.get('name', 'Unknown')}.\n"
            f"   \"{reply_text[:100]}\"\n"
            "They're selling to you, not buying. Auto-reply skipped.\n"
            "Use send_message(action='reply') to respond manually if needed."
        )

    # Reverse-pitch detection: check if prospect is selling to us
    if mode == "autopilot" and sentiment in ("engaged", "question", "neutral"):
        try:
            seller_result = None
            if hasattr(client, "classify_seller"):
                # Collect all prospect messages for better detection
                prospect_messages = [m["text"] for m in messages if m.get("role") == "prospect"]
                seller_result = await client.classify_seller(
                    messages=prospect_messages,
                    author_name=candidate.get("name", ""),
                    author_headline=candidate.get("title", ""),
                )
            if seller_result and seller_result.get("is_seller") and seller_result.get("confidence", 0) >= 0.4:
                await client.close()
                await run_db(update_outreach, outreach_id, status="reverse_pitch")
                await run_db(log_action, "reverse_pitch_detected", outreach_id=outreach_id,
                           result="skipped", details={
                               "text": reply_text[:200],
                               "seller_type": seller_result.get("seller_type", ""),
                               "confidence": seller_result.get("confidence", 0),
                           })
                seller_type = seller_result.get("seller_type", "unknown")
                return (
                    f"Reverse pitch detected from {candidate.get('name', 'Unknown')} "
                    f"(type: {seller_type}, confidence: {seller_result.get('confidence', 0):.0%}).\n"
                    f"   \"{reply_text[:100]}\"\n"
                    "They're selling to you, not buying. Auto-reply skipped.\n"
                    "Use send_message(action='reply') to respond manually if needed."
                )
        except Exception as e:
            logger.debug("Reverse-pitch check failed (non-critical): %s", e)

    # ── Step 5: Load context for reply generation ──
    sender_profile = await run_db(get_setting, "profile", {})
    voice_signature = await run_db(get_setting, "voice_signature", {})

    if campaign:
        campaign_config = json.loads(campaign.get("config_json") or "{}")
        icp_data = json.loads(campaign.get("icp_json") or "{}")
        campaign_context = {
            "target_description": campaign_config.get("target_description", ""),
            "relevance_hook": icp_data.get("relevance_hook", ""),
            "booking_link": campaign_config.get("booking_link", ""),
        }
        campaign_ctx = await run_db(get_campaign_context, campaign_id)
        # Merge context_json fields (offerings, case_studies, social_proofs) into campaign_context
        campaign_context.update(campaign_ctx)
        booking_link = campaign_config.get("booking_link", "")
    else:
        # Inbound outreach — no campaign context available
        campaign_config = {}
        icp_data = {}
        campaign_context = {"target_description": "", "relevance_hook": "", "booking_link": ""}
        campaign_ctx = {}
        booking_link = ""

    prospect_data = json.loads(candidate.get("profile_json", "{}")) if candidate.get("profile_json") else {
        "name": candidate.get("name", ""),
        "title": candidate.get("title", ""),
        "company": candidate.get("company", ""),
        "headline": f"{candidate.get('title', '')} at {candidate.get('company', '')}",
    }

    # ── Prospect Intelligence: load cached or generate ──
    prospect_analysis = None
    contact_db_id = candidate.get("contact_db_id") or candidate.get("contact_id", "")
    if contact_db_id:
        prospect_analysis = await run_db(get_contact_analysis, contact_db_id)
    if not prospect_analysis:
        try:
            prospect_analysis = await analyze_prospect(
                prospect=prospect_data,
                campaign_context=campaign_context,
                icp_data=icp_data,
            )
            if contact_db_id:
                await run_db(save_contact_analysis, contact_db_id, prospect_analysis)
        except Exception as e:
            logger.warning(f"Prospect analysis failed, proceeding without: {e}")

    # Format conversation history for the generator
    conversation_history = [
        {"role": m["role"], "text": m["text"]}
        for m in messages
    ]

    # ── Step 6: Generate → Improve → Validate → Fix pipeline ──
    max_chars = NEGATIVE_MAX_CHARS if sentiment == "negative" else REPLY_MAX_CHARS
    previous_sdr_messages = [m["text"] for m in messages if m.get("role") == "sdr"]

    message, reasoning, validation = await run_reply_pipeline(
        prospect=prospect_data,
        sender_profile=sender_profile,
        voice_signature=voice_signature,
        campaign_context=campaign_context,
        conversation_history=conversation_history,
        reply_text=reply_text,
        sentiment=sentiment,
        prospect_analysis=prospect_analysis,
        booking_link=booking_link,
        max_chars=max_chars,
        previous_sdr_messages=previous_sdr_messages,
        prospect_calendar_url=prospect_calendar_url,
    )

    if not message:
        await client.close()
        return f"Failed to generate reply: pipeline returned empty message"

    if not validation or not validation.is_valid:
        issues_text = "\n".join(f"  \u26a0\ufe0f {issue}" for issue in (validation.issues if validation else []))
        if mode == "autopilot":
            logger.warning(f"Autopilot blocked invalid reply: {issues_text}")
            await run_db(log_action, "validation_blocked", outreach_id=outreach_id, result="blocked",
                       details={"issues": validation.issues if validation else [], "type": "reply"})
            await client.close()
            return (
                f"\u26a0\ufe0f Reply for {candidate.get('name', 'Unknown')} failed validation "
                f"after Generate \u2192 Improve \u2192 Fix pipeline.\n\n"
                f"Issues:\n{issues_text}\n\n"
                "The message was NOT sent to protect your account.\n"
                "Try: reply_to_prospect(mode='copilot') to review and edit manually."
            )
        else:
            logger.warning(f"Copilot reply has validation warnings: {issues_text}")

    # ── Step 7: Copilot vs Autopilot ──
    prospect_name = candidate.get("name", "Unknown")
    prospect_title = candidate.get("title", "")
    prospect_company = candidate.get("company", "")
    fit_score = candidate.get("fit_score", 0)

    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company

    sentiment_icon = SENTIMENT_ICONS.get(sentiment, "\U0001f4ac")
    sentiment_label = SENTIMENT_LABELS.get(sentiment, "Unknown")

    if False:  # copilot mode removed
        # Show message for review — store reply context in next_action as JSON
        reply_context = json.dumps({
            "type": "reply",
            "message": message,
            "sentiment": sentiment,
        })
        await run_db(update_outreach, outreach_id, next_action=reply_context)

        output = [
            f"Reply to **{prospect_name}** ({role_str}) \u2014 Sentiment: {sentiment_icon} {sentiment_label}",
            f"   Fit: {stars(fit_score)}",
            "",
            f'   Their message: "{reply_text[:200]}{"..." if len(reply_text) > 200 else ""}"',
            "",
            f'   "{message}"',
            f"   ({len(message)}/{max_chars} chars)",
            "",
        ]

        # Show reasoning
        if reasoning:
            strategy = reasoning.get("strategy", "") or reasoning.get("answer_approach", "") or reasoning.get("close_style", "") or reasoning.get("angle", "")
            if strategy:
                output.append(f"   Strategy: {strategy}")
                output.append("")

        # Show validation warnings
        if validation and validation.warnings:
            for w in validation.warnings:
                output.append(f"   {w}")
            output.append("")

        output.extend([
            "Send this? Reply with:",
            "  'yes' / 'send' to send this reply",
            "  'skip' to skip this prospect",
            "  'edit: [your text]' to send a custom message instead",
            "  'stop' to pause the campaign",
        ])

        await client.close()
        return "\n".join(line for line in output if line is not None)

    else:
        # Autopilot — send immediately
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
                send_result = await client.send_voice_message(
                    account_id=account_id,
                    chat_id=chat_id,
                    audio_path=audio_path,
                )
                if not send_result.get("success"):
                    logger.warning("Voice send failed (%s), falling back to text", send_result.get("error"))
                    actual_format = "text"

            if actual_format == "text":
                send_result = await client.send_message(
                    account_id=account_id,
                    chat_id=chat_id,
                    text=message,
                )
        except UnipileAuthError:
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
            await client.close()
            if audio_path:
                try:
                    from ..ai.voice_memo_generator import cleanup_voice_memo
                    cleanup_voice_memo(audio_path)
                except Exception:
                    pass
            return f"Failed to send reply: {e}"
        finally:
            await client.close()
            if audio_path:
                try:
                    from ..ai.voice_memo_generator import cleanup_voice_memo
                    cleanup_voice_memo(audio_path)
                except Exception:
                    pass

        if send_result.get("success"):
            # Update status based on sentiment
            if sentiment == "negative":
                new_status = "closed_unhappy"
                import time as _time
                outcome_data = json.dumps({
                    "outcome": "lost",
                    "reason": "Prospect declined (negative reply)",
                    "closed_at": int(_time.time()),
                    "previous_status": candidate.get("status", ""),
                })
                await run_db(update_outreach, outreach_id, status=new_status, outcome_json=outcome_data, next_action=None)
            elif candidate.get("status") == "hot_lead":
                new_status = "hot_lead"  # Stay hot_lead
                await run_db(update_outreach, outreach_id, status=new_status)
            else:
                new_status = "messaged"  # Back to messaged, waiting for their response
                await run_db(update_outreach, outreach_id, status=new_status)
            local_msg_id = await run_db(save_message, outreach_id, role="sdr", text=message, format=actual_format)
            await run_db(increment_usage, "messages_sent")
            await run_db(log_action, "reply_sent",
                outreach_id=outreach_id,
                result="success",
                details={
                    "prospect": prospect_name,
                    "sentiment": sentiment,
                    "message_length": len(message),
                    "reasoning": reasoning,
                },)

            # Post-send verification (background, non-blocking)
            if actual_format == "text" and chat_id:
                from ..services.engagement_verifier import schedule_post_send_verify
                schedule_post_send_verify(
                    account_id=account_id, chat_id=chat_id,
                    sent_text=message, outreach_id=outreach_id,
                    local_message_id=local_msg_id, message_type="reply",
                    voice_signature=voice_signature,
                )

            status_note = ""
            if sentiment == "negative":
                status_note = "\nOutreach closed gracefully."
            elif sentiment == "positive":
                status_note = "\nConversation continues \u2014 check back for their response."
            elif sentiment == "engaged":
                status_note = "\nConversation deepening \u2014 building rapport before any pitch."

            return (
                f"Sent reply to {prospect_name} ({role_str}) \u2014 {sentiment_icon} {sentiment_label}\n"
                f'   "{message}"\n'
                f"{status_note}"
            )
        else:
            error = send_result.get("error", "Unknown error")
            await run_db(log_action, "reply_failed",
                outreach_id=outreach_id,
                result="error",
                details={"error": error},)
            return f"Reply failed for {prospect_name}: {error}"
