"""Tool 4: check_replies — Check for new replies across all campaigns.

Fetches new LinkedIn messages, classifies sentiment
(positive/negative/question/neutral), surfaces hot leads,
and auto-handles opt-outs.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

from ..ai.sentiment import classify_sentiment, detect_calendar_url, detect_meeting_agreement
from ..db.async_bridge import run_db
from ..db.queries import (
    get_inbound_signal_by_sender,
    get_messages_for_outreach,
    get_setting,
    increment_accepted,
    list_campaigns,
    list_inbound_signals,
    log_action,
    mark_message_read,
    save_message,
    update_contact,
    update_outreach,
)
from ..db.schema import get_db
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)
from ..linkedin.circuit_breaker import CircuitBreakerOpen, CollectorCircuitBreaker

logger = logging.getLogger(__name__)

_cb = CollectorCircuitBreaker("check_replies")

# Sentiment display config
SENTIMENT_ICONS = {
    "positive": "🔥",
    "negative": "👎",
    "question": "❓",
    "neutral": "💬",
    "engaged": "💬",
    "out_of_office": "✈️",
    "opt_out": "🚫",
}

SENTIMENT_ACTIONS = {
    "positive": "Auto-replying with booking link (if configured) or suggesting a time.",
    "negative": "No action needed. Outreach closed.",
    "question": "ACTION NEEDED: Answer their question.",
    "neutral": "No action needed. Monitor.",
    "engaged": "ACTION NEEDED: Continue the conversation — deepen rapport.",
    "out_of_office": "Will follow up when they're back.",
    "opt_out": "Auto-closed. They won't be contacted again.",
}


def _append_inbound_invitations(
    output: list[str],
    invitations: list[dict[str, Any]],
    limit: int = 10,
) -> None:
    """Append inbound invitation lines with qualification badges if available."""
    output.append(f"📨 Inbound Invitations ({len(invitations)}):")
    for inv in invitations[:limit]:
        inv_name = inv.get("sender_name", "Someone")
        inv_headline = inv.get("headline", "")
        inv_msg = inv.get("message", "")

        # Check if we have qualification data for this sender
        sender_id = inv.get("sender_id", "")
        badge = ""
        if sender_id:
            from ..db.queries import get_inbound_signal_by_sender as _get_sig
            sig = _get_sig(sender_id, "invitation")
            if sig and sig.get("intent"):
                conf = sig.get("confidence", 0) or 0
                intent = sig.get("intent", "unknown")
                if conf >= 0.7:
                    badge = f"  🟢 {conf:.0%} Lead ({intent})"
                elif conf >= 0.4:
                    badge = f"  🟡 {conf:.0%} ({intent})"
                else:
                    badge = f"  🔴 {conf:.0%} ({intent})"

        inv_line = f"   • {inv_name}"
        if inv_headline:
            inv_line += f" — {inv_headline}"
        inv_line += badge
        output.append(inv_line)
        if inv_msg:
            output.append(f"     \"{inv_msg[:100]}\"")
    if len(invitations) > limit:
        output.append(f"   ... and {len(invitations) - limit} more")


async def _sync_silent_connections(client: Any, account_id: str) -> list[dict]:
    """Detect connections that accepted without messaging.

    Calls get_relations() API and cross-references with outreaches
    that are still in 'invited' status. Updates them to 'connected'.

    Returns list of newly detected connections.
    """
    try:
        relations = await _cb.call(
            client.get_relations(account_id, limit=500),
            label="get_relations",
        )
    except (CircuitBreakerOpen, asyncio.TimeoutError) as e:
        logger.warning(f"get_relations timed out or circuit breaker open: {e}")
        return []
    except Exception as e:
        logger.warning(f"Failed to fetch relations for sync: {e}")
        return []

    if not relations:
        return []

    # Build set of connected provider_ids and public_ids
    connected_ids: set[str] = set()
    for rel in relations:
        pid = rel.get("provider_id") or ""
        if pid:
            connected_ids.add(str(pid))
        pub_id = rel.get("public_id") or ""
        if pub_id:
            connected_ids.add(pub_id)

    # Find outreaches stuck in 'invited' whose contact is now connected
    # Limit to 200 most recent to prevent unbounded memory usage
    def _fetch_invited() -> list:
        db = get_db()
        rows = db.execute(
            """SELECT o.id as outreach_id, o.contact_id, o.campaign_id,
                      c.name, c.title, c.company, c.linkedin_id, c.linkedin_url,
                      c.profile_json
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.status = 'invited'
               ORDER BY o.created_at DESC
               LIMIT 200"""
        ).fetchall()
        db.close()
        return rows

    invited_outreaches = await run_db(_fetch_invited)

    newly_connected: list[dict] = []
    matched_ids: set[str] = set()
    for row in invited_outreaches:
        r = dict(row)
        linkedin_id = r.get("linkedin_id") or ""
        # Extract public_id from linkedin_url
        public_id = ""
        url = r.get("linkedin_url") or ""
        if "/in/" in url:
            public_id = url.split("/in/")[-1].strip("/")

        # Extract provider_id from profile_json (stored during campaign creation)
        contact_provider_id = ""
        try:
            profile_data = json.loads(r.get("profile_json") or "{}")
            contact_provider_id = str(profile_data.get("provider_id", ""))
        except (json.JSONDecodeError, TypeError):
            pass

        # Check if this contact is in our connections
        if (linkedin_id and str(linkedin_id) in connected_ids) or \
           (public_id and public_id in connected_ids) or \
           (contact_provider_id and contact_provider_id in connected_ids):
            import time as _time
            await run_db(update_outreach, r["outreach_id"], status="connected", accepted_at=int(_time.time()))
            await run_db(increment_accepted)
            await run_db(
                log_action,
                "silent_connection_detected",
                outreach_id=r["outreach_id"],
                result="success",
                details={"name": r.get("name", ""), "method": "relations_sync"},
            )
            newly_connected.append(r)
            matched_ids.add(r["outreach_id"])

    # Fallback: individually check remaining invited contacts via API (in parallel)
    unmatched = [dict(row) for row in invited_outreaches
                 if dict(row)["outreach_id"] not in matched_ids]
    if unmatched and len(unmatched) <= 20:
        async def _check_relation(r: dict) -> dict | None:
            contact_provider_id = ""
            try:
                profile_data = json.loads(r.get("profile_json") or "{}")
                contact_provider_id = str(profile_data.get("provider_id", ""))
            except (json.JSONDecodeError, TypeError):
                pass

            if not contact_provider_id:
                return None

            try:
                relation = await client.check_existing_relation(
                    account_id, contact_provider_id
                )
                if relation.get("connected") or relation.get("has_chat"):
                    import time as _time
                    await run_db(update_outreach, r["outreach_id"], status="connected", accepted_at=int(_time.time()))
                    await run_db(increment_accepted)
                    await run_db(
                        log_action,
                        "silent_connection_detected",
                        outreach_id=r["outreach_id"],
                        result="success",
                        details={"name": r.get("name", ""), "method": "individual_check"},
                    )
                    return r
            except Exception as e:
                logger.debug(f"Individual relation check failed for {r.get('name', '')}: {e}")
            return None

        results = await asyncio.gather(
            *[_check_relation(r) for r in unmatched],
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, dict):
                newly_connected.append(result)

    return newly_connected


async def run_check_replies() -> str:
    """Check for new replies across all active campaigns.

    Flow:
    1. Fetch recent LinkedIn inbox messages
    2. Match messages to active outreach contacts
    3. Classify sentiment for new messages
    4. Handle opt-outs automatically
    5. Surface hot leads first
    """

    # ── Pre-checks ──
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "❌ Setup required before checking replies.\n\n"
            "Please run setup_profile first — it connects your LinkedIn account.\n\n"
            "Say 'set up my profile' and I'll walk you through it step by step."
        )

    account_id = get_account_id()
    if not account_id:
        return "❌ No LinkedIn account connected. Run setup_profile first."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"❌ {e}"

    # ── Fetch messages from LinkedIn via Unipile ──
    try:
        messages = await _cb.call(
            client.get_chats(account_id=account_id, limit=50),
            label="get_chats",
        )
    except UnipileAuthError:
        await client.close()
        return (
            "🔑 LinkedIn account disconnected.\n\n"
            "Run setup_profile() again to reconnect."
        )
    except (CircuitBreakerOpen, asyncio.TimeoutError) as e:
        logger.error(f"get_chats timed out or circuit breaker open: {e}")
        await client.close()
        return f"⏱️ LinkedIn API too slow — skipped this check. Will retry next cycle."
    except Exception as e:
        logger.error(f"Failed to check messages: {e}")
        await client.close()
        return f"❌ Failed to check LinkedIn messages: {e}"

    # ── Sync silent connections (accepted but no message) ──
    silent_connections = await _sync_silent_connections(client, account_id)

    # ── Fetch profile viewers (inbound signals) ──
    profile_viewers: list[dict[str, Any]] = []
    try:
        profile_viewers = await _cb.call(
            client.get_profile_viewers(account_id),
            label="get_profile_viewers",
        )
    except (CircuitBreakerOpen, asyncio.TimeoutError) as e:
        logger.debug(f"Profile viewers skipped (timeout/circuit breaker): {e}")
    except Exception as e:
        logger.debug(f"Profile viewers fetch failed (non-critical): {e}")

    # ── Fetch inbound invitations ──
    inbound_invitations: list[dict[str, Any]] = []
    try:
        inbound_invitations = await _cb.call(
            client.get_received_invitations(account_id),
            label="get_received_invitations",
        )
    except (CircuitBreakerOpen, asyncio.TimeoutError) as e:
        logger.debug(f"Inbound invitations skipped (timeout/circuit breaker): {e}")
    except Exception as e:
        logger.debug(f"Inbound invitations fetch failed (non-critical): {e}")

    # ── Fetch real-time webhook events (if backend mode) ──
    webhook_events: list[dict[str, Any]] = []
    try:
        if hasattr(client, "get_unprocessed_events"):
            webhook_events = await client.get_unprocessed_events(account_id, limit=20)
            # Auto-acknowledge processed events
            for evt in webhook_events:
                evt_id = evt.get("id")
                if evt_id and hasattr(client, "acknowledge_event"):
                    await client.acknowledge_event(evt_id)
            if webhook_events:
                logger.info("Fetched %d real-time webhook events", len(webhook_events))
    except Exception as e:
        logger.debug(f"Webhook event fetch failed (non-critical): {e}")

    await client.close()

    # NOTE: Inbound invitations are now detected and saved by the unified
    # inbound pipeline (services/inbound_pipeline.py). No need to save here.

    if not messages and not silent_connections:
        # Even with no messages, show inbound signals
        extra_output: list[str] = []
        if inbound_invitations:
            _append_inbound_invitations(extra_output, inbound_invitations, limit=10)
            extra_output.append("   💡 Accept matching leads or let the scheduler auto-accept ICP matches!")
        if profile_viewers:
            if extra_output:
                extra_output.append("")
            extra_output.append(f"👀 Profile Viewers ({len(profile_viewers)}):")
            for v in profile_viewers[:10]:
                name = v.get("name", "Anonymous")
                title = v.get("title", "")
                company = v.get("company", "")
                role = title
                if company:
                    role += f" at {company}" if role else company
                extra_output.append(f"   • {name}" + (f" — {role}" if role else ""))
            if len(profile_viewers) > 10:
                extra_output.append(f"   ... and {len(profile_viewers) - 10} more")
            extra_output.append("   💡 These people checked out your profile — consider reaching out!")
        if extra_output:
            return "📭 No new messages found.\n\n" + "\n".join(extra_output)
        return (
            "📭 No new messages found.\n\n"
            "Tip: Replies usually take 1-3 days after invitations are accepted.\n"
            "Use show_status to see your campaign progress."
        )

    # ── Match messages to outreach contacts ──
    def _fetch_outreach_contacts() -> list:
        db = get_db()
        rows = db.execute(
            """SELECT o.id as outreach_id, o.contact_id, o.status,
                      c.linkedin_id, c.name, c.title, c.company, c.campaign_id, c.fit_score,
                      c.profile_json
               FROM outreaches o
               JOIN contacts c ON o.contact_id = c.id
               WHERE o.status NOT IN ('opted_out')"""
        ).fetchall()
        db.close()
        return rows

    outreach_contacts = await run_db(_fetch_outreach_contacts)

    # Build lookup by both linkedin_id (public_id) and provider_id
    # sender_id from get_chats() is provider_id format (ACoAAA...),
    # but contacts.linkedin_id stores public_id format (slug).
    contact_lookup: dict[str, dict] = {}
    # Name-based fallback for when provider_id is missing from profile_json
    # (common for DM-only campaigns where search results lack provider_id).
    # Key: lowercase name → contact dict (only stored if name is unique).
    name_lookup: dict[str, dict | None] = {}
    for row in outreach_contacts:
        r = dict(row)
        if r.get("linkedin_id"):
            contact_lookup[r["linkedin_id"]] = r
        # Also index by provider_id from profile_json
        pj = r.pop("profile_json", None)
        if pj:
            try:
                profile = json.loads(pj) if isinstance(pj, str) else pj
                provider_id = profile.get("provider_id") or ""
                if provider_id:
                    contact_lookup[provider_id] = r
            except Exception:
                pass
        # Build name fallback (set to None if ambiguous / duplicate name)
        name_key = (r.get("name") or "").strip().lower()
        if name_key:
            if name_key in name_lookup:
                name_lookup[name_key] = None  # ambiguous — disable
            else:
                name_lookup[name_key] = r

    # Get our own provider_id so we can detect chats where WE sent the last message
    our_provider_id = ""
    try:
        profile_json_str = await run_db(get_setting, "profile", "")
        if profile_json_str:
            our_profile = json.loads(profile_json_str) if isinstance(profile_json_str, str) else profile_json_str
            our_provider_id = our_profile.get("provider_id", "")
    except Exception:
        pass

    # ── Process matches ──
    matched_replies: list[dict[str, Any]] = []

    unsolicited_inbound: list[dict[str, Any]] = []

    pending_classifications: list[tuple[dict, dict, str]] = []  # (contact, msg, reply_text)

    # Phase 1: Process messages that have embedded content (direct Unipile mode)
    has_needs_fetch = False
    for msg in messages:
        if msg.get("_needs_fetch"):
            has_needs_fetch = True
            continue  # Will be handled in Phase 1b via server-side batch

        sender_id = msg.get("sender_id") or ""
        if not sender_id:
            continue
        if sender_id not in contact_lookup:
            if our_provider_id and sender_id == our_provider_id:
                continue  # Our own message
            # Fallback: match by sender_name when provider_id is missing
            # from profile_json (common for DM-only / connections-only campaigns).
            sender_name_key = (msg.get("sender_name") or "").strip().lower()
            fallback = name_lookup.get(sender_name_key) if sender_name_key else None
            if fallback is not None:
                # Cache the resolved provider_id so future checks match directly
                contact_lookup[sender_id] = fallback
                logger.info(
                    "Reply matched by name fallback: %s (sender_id=%s, linkedin_id=%s)",
                    sender_name_key, sender_id, fallback.get("linkedin_id", ""),
                )
            else:
                # Unsolicited inbound DM
                existing_sig = await run_db(get_inbound_signal_by_sender, sender_id, "message")
                unsolicited_inbound.append({
                    "name": msg.get("sender_name", "Unknown"),
                    "text": msg.get("text", ""),
                    "signal_id": existing_sig.get("id", "") if existing_sig else "",
                })
                continue

        contact = contact_lookup[sender_id]
        reply_text = msg.get("text") or ""

        # Dedup
        existing_msgs = await run_db(get_messages_for_outreach, contact["outreach_id"])
        last_prospect_msg_existing = None
        for m in reversed(existing_msgs):
            if m.get("role") == "prospect":
                last_prospect_msg_existing = m
                break
        if last_prospect_msg_existing and last_prospect_msg_existing.get("text", "").strip() == reply_text.strip():
            continue

        # Detect connection acceptance
        if contact["status"] == "invited":
            import time as _time
            await run_db(update_outreach, contact["outreach_id"], status="connected", accepted_at=int(_time.time()))
            await run_db(log_action, "connection_accepted", outreach_id=contact["outreach_id"],
                         details={"name": contact.get("name", "")})
            contact["status"] = "connected"

        # Re-activate dormant outreaches
        DORMANT_STATUSES = ("pending", "error", "closed_happy", "closed_unhappy", "exhausted")
        if contact["status"] in DORMANT_STATUSES:
            old_status = contact["status"]
            await run_db(update_outreach, contact["outreach_id"], status="replied")
            await run_db(log_action, "outreach_reactivated", outreach_id=contact["outreach_id"],
                         details={"name": contact.get("name", ""),
                                  "previous_status": old_status,
                                  "trigger": "inbound_message"})
            contact["status"] = "replied"

        pending_classifications.append((contact, msg, reply_text))

    # Phase 1b: Server-side batch fetch for lightweight chat entries.
    # Instead of N+1 client-side calls, use POST /chats/with-replies
    # which fetches messages server-side and returns only prospect replies.
    if has_needs_fetch and hasattr(client, "get_chats_with_replies"):
        all_provider_ids = [pid for pid in contact_lookup if pid != our_provider_id]
        try:
            reply_client = get_linkedin_client()
            logger.debug("Phase 1b: calling get_chats_with_replies with %d provider_ids", len(all_provider_ids))
            server_replies = await asyncio.wait_for(
                reply_client.get_chats_with_replies(
                    account_id=account_id,
                    provider_ids=all_provider_ids,
                    our_provider_id=our_provider_id,
                    limit=100,
                ),
                timeout=120,
            )
            await reply_client.close()
            logger.info("Reply detection: found %d prospect replies via server-side fetch", len(server_replies))
        except Exception as e:
            logger.warning("Server-side reply fetch failed: %s", e)
            server_replies = []

        for reply in server_replies:
            sender_id = reply.get("sender_id") or reply.get("prospect_provider_id") or ""
            if not sender_id or sender_id not in contact_lookup:
                continue
            contact = contact_lookup[sender_id]
            reply_text = (reply.get("text") or "").strip()
            if not reply_text:
                continue

            # Dedup
            existing_msgs = await run_db(get_messages_for_outreach, contact["outreach_id"])
            last_prospect_msg = None
            for m in reversed(existing_msgs):
                if m.get("role") == "prospect":
                    last_prospect_msg = m
                    break
            if last_prospect_msg and last_prospect_msg.get("text", "").strip() == reply_text:
                continue

            # Detect connection acceptance
            if contact["status"] == "invited":
                import time as _time
                await run_db(update_outreach, contact["outreach_id"], status="connected", accepted_at=int(_time.time()))
                await run_db(log_action, "connection_accepted", outreach_id=contact["outreach_id"],
                             details={"name": contact.get("name", "")})
                contact["status"] = "connected"

            # Re-activate dormant outreaches
            DORMANT_STATUSES = ("pending", "error", "closed_happy", "closed_unhappy", "exhausted")
            if contact["status"] in DORMANT_STATUSES:
                old_status = contact["status"]
                await run_db(update_outreach, contact["outreach_id"], status="replied")
                await run_db(log_action, "outreach_reactivated", outreach_id=contact["outreach_id"],
                             details={"name": contact.get("name", ""),
                                      "previous_status": old_status,
                                      "trigger": "inbound_message"})
                contact["status"] = "replied"

            synthetic_msg = {
                "sender_id": sender_id,
                "sender_name": reply.get("sender_name") or contact.get("name", ""),
                "text": reply_text,
                "timestamp": reply.get("timestamp") or 0,
                "conversation_urn": reply.get("chat_id", ""),
            }
            pending_classifications.append((contact, synthetic_msg, reply_text))

    # Phase 2: Classify sentiment in parallel for all pending messages
    if pending_classifications:
        sentiments = await asyncio.gather(
            *[classify_sentiment(text) for _, _, text in pending_classifications]
        )
    else:
        sentiments = []

    # Phase 2b: Reverse-pitch detection for engaged/question/neutral messages
    seller_flags: list[dict[str, Any]] = [{}] * len(sentiments)
    seller_check_indices = [
        i for i, s in enumerate(sentiments)
        if s in ("engaged", "question", "neutral")
    ]
    if seller_check_indices:
        try:
            from ..linkedin import get_linkedin_client as _get_client
            seller_client = _get_client()
            if hasattr(seller_client, "classify_seller"):
                seller_results = await asyncio.gather(
                    *[
                        seller_client.classify_seller(
                            messages=[pending_classifications[i][2]],
                            author_name=pending_classifications[i][0].get("name", ""),
                            author_headline=pending_classifications[i][0].get("title", ""),
                        )
                        for i in seller_check_indices
                    ],
                    return_exceptions=True,
                )
                await seller_client.close()
                for idx, result in zip(seller_check_indices, seller_results):
                    if isinstance(result, dict) and result.get("is_seller") and result.get("confidence", 0) >= 0.4:
                        seller_flags[idx] = result
            else:
                await seller_client.close()
        except Exception as e:
            logger.debug("Reverse-pitch detection failed (non-critical): %s", e)

    # Phase 2c: Detect calendar links in reply text (returns the actual URL or None)
    calendar_flags: list[str | None] = [
        detect_calendar_url(pending_classifications[i][2]) if i < len(pending_classifications) else None
        for i in range(len(sentiments))
    ]

    # Phase 3: Process results (save, update status, detect hot leads)
    for i, ((contact, msg, reply_text), sentiment) in enumerate(zip(pending_classifications, sentiments)):
        # Mark prior SDR messages as read (prospect replied → they read our messages)
        try:
            prior_msgs = await run_db(get_messages_for_outreach, contact["outreach_id"])
            reply_ts = msg.get("timestamp") or int(time.time())
            for pm in prior_msgs:
                if pm.get("role") == "sdr" and not pm.get("read_at"):
                    await run_db(mark_message_read, pm["id"], read_at=reply_ts)
        except Exception:
            pass  # Non-critical

        # Save the reply
        await run_db(
            save_message,
            outreach_id=contact["outreach_id"],
            role="prospect",
            text=reply_text,
            sentiment=sentiment,
        )

        # Check reverse-pitch flag
        is_seller = bool(seller_flags[i]) if i < len(seller_flags) else False
        calendar_url = calendar_flags[i] if i < len(calendar_flags) else None
        has_calendar = bool(calendar_url)

        # Handle opt-outs
        if sentiment == "opt_out":
            await run_db(update_outreach, contact["outreach_id"], status="opted_out")
            await run_db(log_action, "opt_out_detected", outreach_id=contact["outreach_id"],
                         details={"text": reply_text[:200]})

        # Reverse pitch — prospect is selling to us
        elif is_seller:
            await run_db(update_outreach, contact["outreach_id"], status="reverse_pitch")
            await run_db(log_action, "reverse_pitch_detected", outreach_id=contact["outreach_id"],
                         details={
                             "text": reply_text[:200],
                             "seller_type": seller_flags[i].get("seller_type", ""),
                             "confidence": seller_flags[i].get("confidence", 0),
                         })

        # Hot lead detection
        elif sentiment == "positive":
            await run_db(update_outreach, contact["outreach_id"], status="hot_lead")
            details: dict[str, Any] = {"text": reply_text[:200]}
            if calendar_url:
                details["prospect_calendar_url"] = calendar_url
                # Store the prospect's inbound calendar URL in the outreach
                await run_db(
                    update_outreach, contact["outreach_id"],
                    next_action=json.dumps({
                        "type": "book_meeting",
                        "prospect_calendar_url": calendar_url,
                        "prospect_name": contact.get("name", ""),
                    }),
                )
            await run_db(log_action, "hot_lead_detected", outreach_id=contact["outreach_id"],
                         details=details)
            # Bump fit score on positive reply
            current_fit = contact.get("fit_score", 0.5)
            new_fit = min(1.0, current_fit + 0.1)
            if contact.get("contact_id"):
                await run_db(update_contact, contact["contact_id"], fit_score=new_fit)

        # Question — needs attention
        elif sentiment == "question":
            await run_db(update_outreach, contact["outreach_id"], status="replied")

        # Other
        else:
            await run_db(update_outreach, contact["outreach_id"], status="replied")

        matched_replies.append({
            "name": contact.get("name", "Unknown"),
            "title": contact.get("title", ""),
            "company": contact.get("company", ""),
            "text": reply_text,
            "sentiment": sentiment,
            "conversation_urn": msg.get("conversation_urn", ""),
            "is_seller": is_seller,
            "has_calendar": has_calendar,
            "prospect_calendar_url": calendar_url or "",
        })

    # ── Auto-book meetings when prospect shared calendar link ──
    auto_booked: list[dict[str, Any]] = []
    calendar_replies = [
        (i, contact, calendar_flags[i])
        for i, ((contact, msg, reply_text), sentiment) in enumerate(zip(pending_classifications, sentiments))
        if calendar_flags[i]  # has calendar URL
    ]
    if calendar_replies:
        try:
            from ..services.calendar_booker import book_meeting, format_booking_result

            # Get user's name, email, and timezone for booking
            booker_name = ""
            booker_email = ""
            user_tz = "UTC"
            try:
                profile = await run_db(get_setting, "profile", {})
                booker_name = profile.get("name", "") if isinstance(profile, dict) else ""
            except Exception:
                pass
            try:
                from ..config import get_timezone, is_backend_mode
                user_tz = get_timezone() or "UTC"
            except Exception:
                pass
            # Get email from backend if available
            if not booker_email:
                try:
                    from ..config import is_backend_mode
                    if is_backend_mode():
                        from ..linkedin import get_linkedin_client as _get_bc
                        bc = _get_bc()
                        user_info = await bc.get_user_info()
                        booker_email = user_info.get("email", "")
                        await bc.close()
                except Exception as e:
                    logger.debug("Could not get user email for booking: %s", e)

            if booker_name and booker_email:
                for idx, contact, cal_url in calendar_replies:
                    try:
                        result = await book_meeting(
                            calendar_url=cal_url,
                            booker_name=booker_name,
                            booker_email=booker_email,
                            user_tz=user_tz,
                        )
                        auto_booked.append({
                            "name": contact.get("name", "Unknown"),
                            "result": result,
                            "outreach_id": contact.get("outreach_id", ""),
                        })
                        if result.get("success"):
                            # Update outreach with booking confirmation
                            await run_db(
                                update_outreach, contact["outreach_id"],
                                next_action=json.dumps({
                                    "type": "meeting_booked",
                                    "prospect_calendar_url": cal_url,
                                    "booked_time": result.get("booked_time", ""),
                                    "provider": result.get("provider", ""),
                                }),
                            )
                            await run_db(
                                log_action, "meeting_auto_booked",
                                outreach_id=contact["outreach_id"],
                                result="success",
                                details={
                                    "prospect_calendar_url": cal_url,
                                    "booked_time": result.get("booked_time", ""),
                                    "provider": result.get("provider", ""),
                                },
                            )
                            logger.info(
                                "Auto-booked meeting with %s at %s",
                                contact.get("name", ""), result.get("booked_time", ""),
                            )
                        else:
                            logger.info(
                                "Auto-booking failed for %s: %s",
                                contact.get("name", ""), result.get("error", ""),
                            )
                    except Exception as e:
                        logger.warning("Auto-booking error for %s: %s", contact.get("name", ""), e)
            else:
                logger.info("Skipping auto-booking: missing user name=%s email=%s", bool(booker_name), bool(booker_email))
        except Exception as e:
            logger.warning("Auto-booking batch failed: %s", e)

    # ── Auto-create Google Calendar events for meeting agreements ──
    calendar_events_created: list[dict[str, Any]] = []
    try:
        from ..config import is_backend_mode
        if is_backend_mode():
            # Find replies with meeting agreement signals (positive sentiment + scheduling language)
            meeting_candidates = []
            for i, ((contact, msg, reply_text), sentiment) in enumerate(zip(pending_classifications, sentiments)):
                if sentiment in ("positive", "engaged") and detect_meeting_agreement(reply_text):
                    meeting_candidates.append((i, contact, msg, reply_text))

            if meeting_candidates:
                from datetime import date, datetime, timedelta
                bc = get_linkedin_client()
                try:
                    current_date = date.today().isoformat()
                    user_tz = "UTC"
                    try:
                        from ..config import get_timezone
                        user_tz = get_timezone() or "UTC"
                    except Exception:
                        pass

                    for idx, contact, msg, reply_text in meeting_candidates:
                        try:
                            # Get conversation history for context
                            conv_messages = []
                            try:
                                prior = await run_db(get_messages_for_outreach, contact["outreach_id"])
                                for pm in prior:
                                    conv_messages.append({
                                        "role": pm.get("role", "unknown"),
                                        "text": pm.get("text", ""),
                                        "timestamp": pm.get("timestamp", ""),
                                    })
                            except Exception:
                                pass
                            # Add the current reply
                            conv_messages.append({
                                "role": "prospect",
                                "text": reply_text,
                                "timestamp": msg.get("timestamp", ""),
                            })

                            # Extract meeting details via LLM
                            meeting = await bc.extract_meeting(conv_messages, current_date, user_tz)

                            if meeting.get("meeting_agreed") and meeting.get("confidence", 0) >= 0.7:
                                # Build ISO datetime strings
                                m_date = meeting.get("date", "")
                                m_time = meeting.get("time", "")
                                m_tz = meeting.get("timezone", user_tz)
                                m_duration = meeting.get("duration_minutes", 30)

                                if m_date and m_time:
                                    start_dt = f"{m_date}T{m_time}:00"
                                    try:
                                        dt = datetime.fromisoformat(start_dt)
                                        end_dt = (dt + timedelta(minutes=m_duration)).isoformat()
                                    except (ValueError, TypeError):
                                        end_dt = f"{m_date}T{m_time[:-2]}{int(m_time[-2:]) + m_duration:02d}:00"

                                    prospect_name = contact.get("name", "Unknown")
                                    attendee_email = meeting.get("attendee_email", "")
                                    summary = f"Meeting with {prospect_name}"
                                    description = (
                                        f"Auto-scheduled by HeyLead from LinkedIn conversation.\n"
                                        f"Prospect: {prospect_name}"
                                    )
                                    if contact.get("title"):
                                        description += f" — {contact['title']}"
                                    if contact.get("company"):
                                        description += f" at {contact['company']}"

                                    # Create calendar event via backend
                                    result = await bc.create_calendar_event(
                                        summary=summary,
                                        start_datetime=start_dt,
                                        end_datetime=end_dt,
                                        attendee_email=attendee_email,
                                        description=description,
                                    )

                                    if result.get("success"):
                                        calendar_events_created.append({
                                            "name": prospect_name,
                                            "date": m_date,
                                            "time": m_time,
                                            "event_link": result.get("event_link", ""),
                                        })
                                        # Update outreach with calendar event info
                                        await run_db(
                                            update_outreach, contact["outreach_id"],
                                            next_action=json.dumps({
                                                "type": "calendar_event_created",
                                                "event_link": result.get("event_link", ""),
                                                "event_id": result.get("event_id", ""),
                                                "meeting_date": m_date,
                                                "meeting_time": m_time,
                                                "attendee_email": attendee_email,
                                            }),
                                        )
                                        await run_db(
                                            log_action, "calendar_event_created",
                                            outreach_id=contact["outreach_id"],
                                            result="success",
                                            details={
                                                "meeting_date": m_date,
                                                "meeting_time": m_time,
                                                "event_link": result.get("event_link", ""),
                                                "attendee_email": attendee_email,
                                                "prospect_name": prospect_name,
                                            },
                                        )
                                        logger.info(
                                            "Calendar event created for %s on %s at %s",
                                            prospect_name, m_date, m_time,
                                        )
                                    else:
                                        logger.info(
                                            "Calendar event creation failed for %s: %s",
                                            prospect_name, result.get("error", ""),
                                        )
                        except Exception as e:
                            logger.warning(
                                "Meeting extraction/calendar error for %s: %s",
                                contact.get("name", ""), e,
                            )
                finally:
                    await bc.close()
    except Exception as e:
        logger.debug("Calendar event auto-creation skipped: %s", e)

    # Auto-replies are handled exclusively by the scheduler (JOB_AUTO_REPLY)
    # to prevent duplicate replies from concurrent check_replies + scheduler execution.
    # The scheduler's planner picks up positive/engaged replies and creates auto-reply
    # jobs with proper dedup (pending job check + 30-min cooldown + DB message guard).
    auto_replied_names: list[str] = []

    # ── Mark processed chats as read (non-blocking) ──
    try:
        chat_ids_to_mark = set()
        for reply in matched_replies:
            curn = reply.get("conversation_urn", "")
            if curn:
                chat_ids_to_mark.add(curn)
        if chat_ids_to_mark:
            mark_account_id = get_account_id()
            if mark_account_id:
                try:
                    mark_client = get_linkedin_client()
                except Exception:
                    mark_client = None
                if mark_client:
                    try:
                        for cid in chat_ids_to_mark:
                            await mark_client.mark_chat_read(cid)
                    finally:
                        await mark_client.close()
    except Exception:
        pass  # Non-critical — inbox hygiene

    # ── Format output ──
    if not matched_replies and not silent_connections:
        return (
            f"📬 Checked {len(messages)} messages — none from campaign contacts.\n\n"
            "Replies from non-campaign contacts are not tracked.\n"
            "Use show_status to see campaign progress."
        )

    if not matched_replies and silent_connections:
        # Only silent connections, no message replies
        output = [f"📬 No new message replies, but:\n"]
        sc_count = len(silent_connections)
        output.append(f"🤝 {sc_count} silent connection{'s' if sc_count != 1 else ''} detected:")
        for sc in silent_connections[:5]:
            name = sc.get("name", "Unknown")
            title = sc.get("title", "")
            company = sc.get("company", "")
            role = title
            if company:
                role += f" at {company}" if role else company
            output.append(f"   └── {name} ({role}) — accepted your invite!")
        if sc_count > 5:
            output.append(f"   ... and {sc_count - 5} more")
        output.append("   → Use send_followup() to reach out!")
        return "\n".join(output)

    # Sort: hot leads first, then questions, then rest
    priority_order = {"positive": 0, "engaged": 1, "question": 2, "neutral": 3, "negative": 4, "out_of_office": 5, "opt_out": 6}
    matched_replies.sort(key=lambda r: priority_order.get(r["sentiment"], 99))

    output = [f"📬 {len(matched_replies)} new repl{'y' if len(matched_replies) == 1 else 'ies'}:\n"]

    for i, reply in enumerate(matched_replies):
        is_seller = reply.get("is_seller", False)
        has_calendar = reply.get("has_calendar", False)

        if is_seller:
            icon = "🔄"
            action = "REVERSE PITCH — they're selling to you. Auto-reply skipped."
        elif has_calendar:
            icon = "📅"
            cal_url = reply.get("prospect_calendar_url", "")
            action = f"Shared their calendar — book here: {cal_url}" if cal_url else "Shared their calendar link — book a time!"
        else:
            icon = SENTIMENT_ICONS.get(reply["sentiment"], "💬")
            action = SENTIMENT_ACTIONS.get(reply["sentiment"], "")

        name = reply["name"]
        role = reply.get("title", "")
        if reply.get("company"):
            role += f" at {reply['company']}" if role else reply["company"]

        text_preview = reply["text"][:150]
        if len(reply["text"]) > 150:
            text_preview += "..."

        output.append(f"{icon} **{name}** ({role}):")
        output.append(f"   \"{text_preview}\"")
        if action:
            output.append(f"   → {action}")
        output.append("")

    # Summary
    hot_count = sum(1 for r in matched_replies if r["sentiment"] == "positive")
    question_count = sum(1 for r in matched_replies if r["sentiment"] == "question")
    opt_out_count = sum(1 for r in matched_replies if r["sentiment"] == "opt_out")
    seller_count = sum(1 for r in matched_replies if r.get("is_seller"))
    calendar_count = sum(1 for r in matched_replies if r.get("has_calendar"))

    if hot_count > 0:
        if auto_replied_names:
            names_str = ", ".join(auto_replied_names)
            output.append(f"🔥 {hot_count} hot lead{'s' if hot_count > 1 else ''}! Auto-replied to: {names_str}")
        else:
            output.append(f"🔥 {hot_count} hot lead{'s' if hot_count > 1 else ''}! Reply to them ASAP.")
    if calendar_count > 0:
        if auto_booked:
            from ..services.calendar_booker import format_booking_result
            booked_ok = [b for b in auto_booked if b["result"].get("success")]
            booked_fail = [b for b in auto_booked if not b["result"].get("success")]
            if booked_ok:
                output.append(f"📅 Auto-booked {len(booked_ok)} meeting{'s' if len(booked_ok) > 1 else ''}:")
                for b in booked_ok:
                    booked_time = b["result"].get("booked_time", "")
                    provider = b["result"].get("provider", "")
                    try:
                        from datetime import datetime as _dt, timezone as _tz
                        dt = _dt.fromisoformat(booked_time.replace("Z", "+00:00"))
                        time_str = dt.strftime("%a %b %d, %I:%M %p")
                    except (ValueError, TypeError):
                        time_str = booked_time
                    output.append(f"   {b['name']} — {time_str} ({provider.title()})")
            if booked_fail:
                for b in booked_fail:
                    cal_url = b["result"].get("url", "")
                    output.append(f"   {b['name']} — auto-book failed, book manually: {cal_url}")
        else:
            cal_urls = [r["prospect_calendar_url"] for r in matched_replies if r.get("prospect_calendar_url")]
            if cal_urls:
                output.append(f"📅 {calendar_count} prospect{'s' if calendar_count > 1 else ''} shared their calendar:")
                for url in cal_urls:
                    output.append(f"   → {url}")
            else:
                output.append(f"📅 {calendar_count} prospect{'s' if calendar_count > 1 else ''} shared their calendar — book a time!")
    # Calendar events auto-created from meeting agreements
    if calendar_events_created:
        output.append(f"\n📅 Auto-created {len(calendar_events_created)} Google Calendar event{'s' if len(calendar_events_created) > 1 else ''}:")
        for evt in calendar_events_created:
            output.append(f"   {evt['name']} — {evt['date']} at {evt['time']}")
            if evt.get("event_link"):
                output.append(f"      {evt['event_link']}")

    if question_count > 0:
        output.append(f"❓ {question_count} question{'s' if question_count > 1 else ''} to answer.")
    if seller_count > 0:
        output.append(f"🔄 {seller_count} reverse pitch{'es' if seller_count > 1 else ''} detected (auto-reply skipped).")
    if opt_out_count > 0:
        output.append(f"🚫 {opt_out_count} opt-out{'s' if opt_out_count > 1 else ''} (auto-closed).")

    # ── Silent connections ──
    if silent_connections:
        output.append("")
        sc_count = len(silent_connections)
        output.append(f"🤝 {sc_count} silent connection{'s' if sc_count != 1 else ''} detected:")
        for sc in silent_connections[:5]:
            name = sc.get("name", "Unknown")
            title = sc.get("title", "")
            company = sc.get("company", "")
            role = title
            if company:
                role += f" at {company}" if role else company
            output.append(f"   └── {name} ({role}) — accepted your invite!")
        if sc_count > 5:
            output.append(f"   ... and {sc_count - 5} more")
        output.append("   → Use send_followup() to reach out!")

    # ── Profile viewers (inbound signals) ──
    if profile_viewers:
        output.append("")
        output.append(f"👀 Profile Viewers ({len(profile_viewers)}):")
        for v in profile_viewers[:5]:
            name = v.get("name", "Anonymous")
            title = v.get("title", "")
            company = v.get("company", "")
            role = title
            if company:
                role += f" at {company}" if role else company
            output.append(f"   • {name}" + (f" — {role}" if role else ""))
        if len(profile_viewers) > 5:
            output.append(f"   ... and {len(profile_viewers) - 5} more")
        output.append("   💡 These people checked your profile — warm leads!")

    # ── Inbound invitations with qualification badges ──
    if inbound_invitations:
        output.append("")
        _append_inbound_invitations(output, inbound_invitations, limit=5)
        output.append("   💡 Accept matching leads or let the scheduler handle it!")

    # ── Unsolicited inbound DMs ──
    if unsolicited_inbound:
        output.append("")
        output.append(f"📩 Unsolicited Inbound DMs ({len(unsolicited_inbound)}):")
        for ub in unsolicited_inbound[:5]:
            name = ub.get("name", "Unknown")
            text = (ub.get("text") or "")[:100]
            output.append(f"   • {name}: \"{text}\"")
        if len(unsolicited_inbound) > 5:
            output.append(f"   ... and {len(unsolicited_inbound) - 5} more")
        output.append("   💡 New inbound messages detected — pipeline will classify and respond!")

    # ── Inbound Pipeline Status ──
    recent_signals = await run_db(list_inbound_signals, limit=30)
    if recent_signals:
        by_status: dict[str, int] = {}
        for s in recent_signals:
            st = s.get("status", "unknown")
            by_status[st] = by_status.get(st, 0) + 1
        pipeline_parts = []
        for status_name in ("new", "classified", "accepted", "ignored", "engaged", "dismissed"):
            count = by_status.get(status_name, 0)
            if count:
                pipeline_parts.append(f"{count} {status_name}")
        if pipeline_parts:
            output.append("")
            output.append(f"📊 Inbound Pipeline: {', '.join(pipeline_parts)}")

    # ── Real-time webhook events ──
    if webhook_events:
        output.append("")
        new_msg_events = [e for e in webhook_events if e.get("event_type") == "new_message"]
        new_rel_events = [e for e in webhook_events if e.get("event_type") in ("new_relation", "invitation_accepted")]
        disconnect_events = [e for e in webhook_events if e.get("event_type") == "account_disconnected"]
        if new_msg_events:
            output.append(f"⚡ {len(new_msg_events)} real-time message event(s) received via webhook")
        if new_rel_events:
            output.append(f"⚡ {len(new_rel_events)} new connection event(s) via webhook")
        if disconnect_events:
            output.append("⚠️ Account disconnection event detected — check account health!")

    return "\n".join(output)
