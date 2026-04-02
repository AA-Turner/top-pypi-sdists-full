"""Tool: approve_outreach — Process user approval for copilot-generated messages.

Handles four approval flows:
1. Invitation approval (from generate_and_send copilot mode)
2. Follow-up DM approval (from send_followup copilot mode)
3. Engagement approval (from engage_prospect copilot mode)
4. Reply approval (from reply_to_prospect copilot mode)

User actions:
- "yes" / "send" → Send the proposed message/action
- "skip" → Cancel this outreach, revert to previous status
- "edit: [custom text]" → Send custom message instead
- "stop" → Pause the campaign
- "react" → Switch from comment to reaction (engagement only)
- "comment" → Switch from reaction to comment (engagement only)
"""

from __future__ import annotations

import json
import logging
from typing import Any

from ..constants import (
    COPILOT_APPROVAL_THRESHOLD,
    OUTREACH_REVIEW_PENDING,
)
from ..db.queries import (
    get_campaign,
    get_outreach,
    get_pending_approval,
    get_setting,
    increment_sent,
    increment_usage,
    log_action,
    save_engagement,
    save_message,
    save_setting,
    update_campaign,
    update_outreach,
)
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)
from ..linkedin.rate_limiter import (
    can_send_now,
    get_next_delay,
    update_limits_after_send,
)
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


async def run_approve_outreach(
    action: str,
    outreach_id: str = "",
    custom_message: str = "",
) -> str:
    """Process user approval for a copilot-generated message.

    Flow:
    1. Find the pending outreach (by ID or auto-find latest)
    2. Detect approval type (invitation vs follow-up vs engagement)
    3. Route action to appropriate handler
    4. Clean up next_action field
    5. Track approval metrics
    """

    # ── Step 0: Pre-checks ──
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return "Setup required. Run setup_profile first."

    account_id = get_account_id()
    if not account_id:
        return "No LinkedIn account connected. Run setup_profile first."

    # ── Step 1: Find outreach ──
    if outreach_id:
        outreach = await run_db(get_outreach, outreach_id)
        if not outreach:
            return f"Outreach not found: {outreach_id}"
    else:
        outreach = await run_db(get_pending_approval)
        if not outreach:
            return (
                "No pending approvals.\n\n"
                "Run generate_and_send(), send_followup(), or engage_prospect() "
                "in copilot mode to generate a message for review."
            )
        outreach_id = outreach["id"]

    # ── Step 2: Normalize action ──
    action = action.lower().strip()

    # Handle "edit: text" format — extract custom message
    if action.startswith("edit:"):
        edit_text = action[5:].strip()
        if not edit_text and not custom_message:
            return (
                "Edit requires text.\n\n"
                "Examples:\n"
                "  approve_outreach(action='edit: Hi, love your work!')\n"
                "  approve_outreach(action='send', custom_message='Hi, love your work!')"
            )
        if edit_text:
            custom_message = edit_text
        action = "send"

    # ── Step 2b: Manual status overrides (work with or without pending action) ──
    if action in ("close_happy", "won", "close_unhappy", "lost", "opt_out"):
        status_map = {
            "close_happy": "closed_happy",
            "won": "closed_happy",
            "close_unhappy": "closed_unhappy",
            "lost": "closed_unhappy",
            "opt_out": "opted_out",
        }
        new_status = status_map[action]
        old_status = outreach.get("status", "unknown")
        import time as _time
        outcome_map = {
            "closed_happy": "won",
            "closed_unhappy": "lost",
            "opted_out": "opt_out",
        }
        outcome_data = json.dumps({
            "outcome": outcome_map.get(new_status, action),
            "reason": custom_message or "manual override",
            "closed_at": int(_time.time()),
            "previous_status": old_status,
        })
        await run_db(update_outreach, outreach_id, status=new_status, next_action=None, outcome_json=outcome_data)
        await run_db(log_action, f"manual_{new_status}",
            outreach_id=outreach_id,
            result=new_status,
            details={"previous_status": old_status, "reason": custom_message or "manual override"},)

        # Get contact name for display
        contact = _get_contact(outreach.get("contact_id", ""))
        name = contact.get("name", "Unknown") if contact else "Unknown"

        status_display = {
            "closed_happy": "Closed (Won)",
            "closed_unhappy": "Closed (Lost)",
            "opted_out": "Opted Out",
        }
        return (
            f"{status_display[new_status]}: **{name}**\n"
            f"   Previous status: {old_status}\n"
            + (f"   Reason: {custom_message}\n" if custom_message else "")
            + "\nThis prospect won't receive further outreach."
        )

    # Validate next_action exists (required for send/skip/edit/react/comment)
    next_action = outreach.get("next_action", "")
    if not next_action:
        return (
            f"No pending action for this outreach (status: {outreach['status']}).\n\n"
            "This outreach may have already been processed.\n\n"
            "Available status overrides: approve_outreach(action='won'), "
            "'lost', or 'opt_out' to change status directly."
        )

    # ── Step 3: Handle "stop" — pause campaign immediately ──
    if action == "stop":
        campaign = await run_db(get_campaign, outreach["campaign_id"])
        if campaign:
            await run_db(update_campaign, outreach["campaign_id"], status="paused")
            await run_db(update_outreach, outreach_id, next_action=None)
            return (
                f"Campaign '{campaign['name']}' paused.\n\n"
                "All outreach stopped. Use resume_campaign() to resume."
            )
        else:
            await run_db(update_outreach, outreach_id, next_action=None)
            return "Campaign not found, but pending action cleared."

    # ── Step 4: Detect approval type ──
    approval_type = _detect_approval_type(outreach, next_action)

    # ── Step 5: Route to handler ──
    if approval_type == "cooldown":
        contact = _get_contact(outreach.get("contact_id", ""))
        name = contact.get("name", "Unknown") if contact else "Unknown"
        return (
            f"No pending approval for {name} — outreach is in engagement cooldown.\n\n"
            "The scheduler will pick this up automatically when the cooldown expires."
        )
    elif approval_type == "invitation":
        return await _handle_invitation_approval(
            action, outreach_id, outreach, next_action,
            custom_message, account_id,
        )
    elif approval_type == "followup":
        return await _handle_followup_approval(
            action, outreach_id, outreach, next_action,
            custom_message, account_id,
        )
    elif approval_type == "engagement":
        return await _handle_engagement_approval(
            action, outreach_id, outreach, next_action,
            custom_message, account_id,
        )
    elif approval_type == "reply":
        return await _handle_reply_approval(
            action, outreach_id, outreach, next_action,
            custom_message, account_id,
        )
    else:
        return f"Unable to determine approval type for outreach {outreach_id}."


# ──────────────────────────────────────────────
# Type detection
# ──────────────────────────────────────────────

def _detect_approval_type(outreach: dict, next_action: str) -> str:
    """Detect what type of approval this is.

    Logic:
    - status == "review_pending" → invitation
    - next_action is JSON with "type": "reply" → reply
    - next_action is JSON with "type" key → engagement
    - status == "connected" → follow-up
    - status in ("hot_lead", "replied") → reply
    - Fallback: plain text → follow-up
    """
    status = outreach.get("status", "")

    # Invitation flow sets status = "review_pending"
    if status == OUTREACH_REVIEW_PENDING:
        return "invitation"

    # Try parsing as JSON (engagement stores {"type": "comment"/"react", ...})
    # Reply stores {"type": "reply", "message": ..., "sentiment": ...}
    try:
        data = json.loads(next_action)
        if isinstance(data, dict):
            # Cooldown/scheduler metadata — not a pending approval
            if "skip_engagement_until" in data and "type" not in data:
                return "cooldown"
            if "type" in data:
                if data["type"] == "reply":
                    return "reply"
                return "engagement"
    except (json.JSONDecodeError, TypeError):
        pass

    # Connected status with plain text → follow-up
    if status == "connected":
        return "followup"

    # Hot lead or replied status → reply
    if status in ("hot_lead", "replied"):
        return "reply"

    # Fallback: plain text → follow-up
    return "followup"


# ──────────────────────────────────────────────
# Contact data helper
# ──────────────────────────────────────────────

def _get_contact(contact_id: str) -> dict | None:
    """Fetch contact data by ID."""
    from ..db.schema import get_db
    db = get_db()
    row = db.execute(
        "SELECT * FROM contacts WHERE id = ?", (contact_id,)
    ).fetchone()
    db.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────
# Handler: Invitation approval
# ──────────────────────────────────────────────

async def _handle_invitation_approval(
    action: str,
    outreach_id: str,
    outreach: dict,
    message: str,
    custom_message: str,
    account_id: str,
) -> str:
    """Handle invitation approval flow.

    Mirrors generate_send.py autopilot branch (lines 252-321).
    """
    contact = _get_contact(outreach["contact_id"])
    if not contact:
        return f"Contact not found for outreach {outreach_id}."

    prospect_name = contact.get("name", "Unknown")
    prospect_title = contact.get("title", "")
    prospect_company = contact.get("company", "")
    role_str = prospect_title
    if prospect_company:
        role_str += f" at {prospect_company}" if role_str else prospect_company

    # ── Skip ──
    if action == "skip":
        await run_db(update_outreach, outreach_id, status="pending", next_action=None)
        await run_db(log_action, "invitation_skipped", outreach_id=outreach_id, result="skipped",
                   details={"prospect": prospect_name})
        return f"Skipped {prospect_name}. Moved back to pending queue."

    # ── Send (yes/send) ──
    if action in ("yes", "send"):
        final_message = custom_message if custom_message else message

        # Get provider_id
        profile_json = contact.get("profile_json", "{}")
        try:
            profile_data = json.loads(profile_json) if profile_json else {}
        except (json.JSONDecodeError, TypeError):
            profile_data = {}

        provider_id = (
            profile_data.get("provider_id", "")
            or contact.get("linkedin_id", "")
            or profile_data.get("public_id", "")
        )
        if not provider_id:
            await run_db(update_outreach, outreach_id, status="error", next_action=None)
            return f"No LinkedIn ID for {prospect_name}. Cannot send invitation."

        # Rate limit gate
        can_send, rate_reason, _ = await can_send_now()
        if not can_send:
            return (
                f"⏸️ Cannot send right now: {rate_reason}\n\n"
                "The message is still queued — try again when the limit resets.\n"
                "Use show_status() to check your account health."
            )

        # Send via client
        try:
            client = get_linkedin_client()
        except UnipileError as e:
            return f"{e}"

        try:
            result = await client.send_invitation(
                account_id=account_id,
                provider_id=provider_id,
                message=final_message,
            )
        except UnipileAuthError:
            await client.close()
            await run_db(update_outreach, outreach_id, status="pending", next_action=None)
            return (
                "LinkedIn account disconnected.\n\n"
                "Run setup_profile() again to reconnect."
            )
        except Exception as e:
            await client.close()
            await run_db(update_outreach, outreach_id, status="error", next_action=None)
            return f"Send failed for {prospect_name}: {e}"
        finally:
            await client.close()

        # Update rate limits
        await run_db(increment_sent)
        new_limit = await update_limits_after_send(blocked=result.get("blocked", False))

        if result.get("success"):
            await run_db(update_outreach, outreach_id, status="invited", next_action=None)
            await run_db(save_message, outreach_id, role="sdr", text=final_message)
            await run_db(increment_usage, "invitations_sent")

            # Increment approval counter
            approvals = await run_db(get_setting, "copilot_approvals", 0)
            await run_db(save_setting, "copilot_approvals", approvals + 1)

            await run_db(log_action, "invitation_sent", outreach_id=outreach_id, result="success",
                details={
                    "prospect": prospect_name,
                    "message_length": len(final_message),
                    "approval_type": "edit" if custom_message else "approved",
                },)

            delay = get_next_delay()
            delay_minutes = delay // 60

            output = (
                f"Sent to {prospect_name} ({role_str})\n"
                f'   "{final_message}"\n\n'
                f"Next send in ~{delay_minutes} minutes\n"
                f"Daily limit: {new_limit}/day"
            )

            # Suggest autopilot after threshold
            if approvals + 1 >= COPILOT_APPROVAL_THRESHOLD:
                output += (
                    f"\n\nYou've approved {approvals + 1} messages in a row. "
                    "Ready to switch to autopilot? Use generate_and_send(mode='autopilot')"
                )

            return output

        else:
            error = result.get("error", "Unknown error")
            if result.get("auth_error"):
                await run_db(update_outreach, outreach_id, status="pending", next_action=None)
                await run_db(log_action, "auth_error", outreach_id=outreach_id, result="blocked",
                           details={"error": error})
                return (
                    "LinkedIn account disconnected.\n\n"
                    "Run setup_profile() again to reconnect."
                )
            elif result.get("blocked"):
                await run_db(update_outreach, outreach_id, status="pending", next_action=None)
                await run_db(log_action, "invitation_blocked", outreach_id=outreach_id, result="blocked",
                           details={"error": error})
                return (
                    f"LinkedIn blocked the send: {error}\n\n"
                    f"Daily limit reduced to {new_limit}. Will retry later."
                )
            else:
                await run_db(update_outreach, outreach_id, status="error", next_action=None)
                await run_db(log_action, "invitation_failed", outreach_id=outreach_id, result="error",
                           details={"error": error})
                return f"Send failed for {prospect_name}: {error}"

    return _unknown_action(action, "invitation")


# ──────────────────────────────────────────────
# Handler: Follow-up DM approval
# ──────────────────────────────────────────────

async def _handle_followup_approval(
    action: str,
    outreach_id: str,
    outreach: dict,
    message: str,
    custom_message: str,
    account_id: str,
) -> str:
    """Handle follow-up DM approval flow.

    Mirrors send_followup.py autopilot branch (lines 321-370).
    """
    contact = _get_contact(outreach["contact_id"])
    if not contact:
        return f"Contact not found for outreach {outreach_id}."

    prospect_name = contact.get("name", "Unknown")

    # ── Skip ──
    if action == "skip":
        await run_db(update_outreach, outreach_id, next_action=None)
        await run_db(log_action, "followup_skipped", outreach_id=outreach_id, result="skipped",
                   details={"prospect": prospect_name})
        return f"Skipped follow-up for {prospect_name}."

    # ── Send ──
    if action in ("yes", "send"):
        final_message = custom_message if custom_message else message

        # Resolve chat_id — prefer provider_id (ACoAAA) from profile_json
        prospect_linkedin_id = ""
        pj = contact.get("profile_json")
        if pj:
            try:
                import json as _json
                _profile = _json.loads(pj) if isinstance(pj, str) else pj
                prospect_linkedin_id = _profile.get("provider_id", "")
            except Exception:
                pass
        if not prospect_linkedin_id:
            prospect_linkedin_id = contact.get("linkedin_id", "")
        if not prospect_linkedin_id:
            return f"No LinkedIn ID for {prospect_name}. Cannot send DM."

        try:
            client = get_linkedin_client()
        except UnipileError as e:
            return f"{e}"

        try:
            chat_id = await client.find_chat_for_user(account_id, prospect_linkedin_id)
        except Exception as e:
            logger.error(f"Failed to find chat: {e}")
            chat_id = None

        create_new_chat = chat_id is None

        # For new chats, extract provider_id from miniProfileUrn in URL
        prospect_provider_id = prospect_linkedin_id
        if create_new_chat and not prospect_linkedin_id.startswith("ACo"):
            url = contact.get("linkedin_url") or ""
            from urllib.parse import urlparse, parse_qs, unquote
            qs = parse_qs(urlparse(url).query)
            urn = unquote(qs.get("miniProfileUrn", [""])[0])
            if urn:
                prospect_provider_id = urn.split(":")[-1]

        # Send message
        logger.info(
            "Sending followup to %s (outreach=%s, new_chat=%s, chat_id=%s, provider=%s)",
            prospect_name, outreach_id, create_new_chat, chat_id, prospect_provider_id,
        )
        try:
            if create_new_chat:
                send_result = await client.send_new_message(
                    account_id=account_id,
                    provider_id=prospect_provider_id,
                    text=final_message,
                )
            else:
                send_result = await client.send_message(
                    account_id=account_id,
                    chat_id=chat_id,
                    text=final_message,
                )
        except UnipileAuthError as e:
            logger.error("UnipileAuthError sending followup to %s: %s", prospect_name, e)
            await client.close()
            return (
                f"LinkedIn account disconnected.\n\n"
                f"Detail: {e}\n"
                f"Run setup_profile() again to reconnect."
            )
        except Exception as e:
            logger.error("Exception sending followup to %s: %s", prospect_name, e)
            await client.close()
            return f"Failed to send follow-up: {e}"
        finally:
            await client.close()

        logger.info("Followup send_result for %s: %s", prospect_name, send_result)

        if send_result.get("success"):
            new_count = outreach.get("followup_count", 0) + 1
            await run_db(update_outreach, outreach_id, status="messaged",
                followup_count=new_count, next_action=None,)
            await run_db(save_message, outreach_id, role="sdr", text=final_message)
            await run_db(increment_usage, "messages_sent")

            # Save conversation memory for future follow-ups
            try:
                from ..ai.memory_extractor import extract_memory_heuristic
                from ..db.queries import save_outreach_memory
                memory_entry = extract_memory_heuristic(final_message, new_count)
                await run_db(save_outreach_memory, outreach_id, memory_entry)
            except Exception as e:
                logger.debug("Memory save on approval failed: %s", e)

            await run_db(log_action, "followup_sent",
                outreach_id=outreach_id,
                result="success",
                details={
                    "prospect": prospect_name,
                    "followup_number": new_count,
                    "message_length": len(final_message),
                    "approval_type": "edit" if custom_message else "approved",
                },)
            return (
                f"Sent follow-up #{new_count} to {prospect_name}\n"
                f'   "{final_message}"'
            )
        else:
            error = send_result.get("error", "Unknown error")
            logger.error(
                "Followup failed for %s: error=%s full_result=%s",
                prospect_name, error, send_result,
            )
            await run_db(log_action, "followup_failed", outreach_id=outreach_id,
                result="error", details={"error": error},)
            return f"Follow-up failed for {prospect_name}: {error}"

    return _unknown_action(action, "follow-up")


# ──────────────────────────────────────────────
# Handler: Engagement approval (comment/react)
# ──────────────────────────────────────────────

async def _handle_engagement_approval(
    action: str,
    outreach_id: str,
    outreach: dict,
    next_action_json: str,
    custom_message: str,
    account_id: str,
) -> str:
    """Handle engagement (comment/react) approval flow.

    Mirrors engage_prospect.py _send_comment() and _handle_reaction() autopilot.
    """
    # Parse next_action
    try:
        action_data = json.loads(next_action_json)
    except (json.JSONDecodeError, TypeError):
        return f"Invalid engagement data. Please run engage_prospect() again."

    engagement_type = action_data.get("type", "")
    post_id = action_data.get("post_id", "")
    comment_text = action_data.get("comment", "")

    if not post_id:
        return "Missing post ID in engagement data. Please run engage_prospect() again."

    contact = _get_contact(outreach["contact_id"])
    prospect_name = contact.get("name", "Unknown") if contact else "Unknown"

    # ── Skip ──
    if action == "skip":
        await run_db(update_outreach, outreach_id, next_action=None)
        await run_db(log_action, "engagement_skipped", outreach_id=outreach_id, result="skipped",
                   details={"prospect": prospect_name, "type": engagement_type})
        return f"Skipped engagement for {prospect_name}."

    # ── Mode switch: react (while reviewing a comment) ──
    if action == "react" and engagement_type == "comment":
        engagement_type = "react"
        comment_text = ""

    # ── Mode switch: comment (while reviewing a reaction) ──
    if action == "comment" and engagement_type == "react":
        await run_db(update_outreach, outreach_id, next_action=None)
        return (
            "Cannot switch to comment mode without regenerating.\n\n"
            "Run engage_prospect(action='comment') to generate a comment."
        )

    # ── Send ──
    if action in ("yes", "send", "react"):
        try:
            client = get_linkedin_client()
        except UnipileError as e:
            return f"{e}"

        if engagement_type == "comment":
            final_comment = custom_message if custom_message else comment_text

            try:
                result = await client.send_post_comment(account_id, post_id, final_comment)
            except UnipileAuthError:
                await client.close()
                return "LinkedIn account disconnected. Run setup_profile() again."
            except Exception as e:
                await client.close()
                return f"Failed to send comment: {e}"
            finally:
                await client.close()

            if result.get("success"):
                await run_db(save_engagement, outreach_id=outreach_id,
                    action_type="comment",
                    post_id=post_id,
                    post_text=action_data.get("post_text", ""),
                    text=final_comment,
                    status="sent",)
                await run_db(increment_usage, "engagements_sent")
                await run_db(update_outreach, outreach_id, next_action=None)
                await run_db(log_action, "engagement_comment", outreach_id=outreach_id,
                    result="success",
                    details={
                        "prospect": prospect_name,
                        "post_id": post_id,
                        "comment_length": len(final_comment),
                        "approval_type": "edit" if custom_message else "approved",
                    },)
                return f'Commented on {prospect_name}\'s post:\n   "{final_comment}"'
            else:
                error = result.get("error", "Unknown error")
                await run_db(log_action, "engagement_comment_failed", outreach_id=outreach_id,
                           result="error", details={"error": error})
                return f"Comment failed: {error}"

        elif engagement_type == "react":
            try:
                result = await client.send_post_reaction(account_id, post_id, "LIKE")
            except UnipileAuthError:
                await client.close()
                return "LinkedIn account disconnected. Run setup_profile() again."
            except Exception as e:
                await client.close()
                return f"Failed to react: {e}"
            finally:
                await client.close()

            if result.get("success"):
                await run_db(save_engagement, outreach_id=outreach_id,
                    action_type="react",
                    post_id=post_id,
                    post_text=action_data.get("post_text", ""),
                    reaction_type="LIKE",
                    status="sent",)
                await run_db(increment_usage, "engagements_sent")
                await run_db(update_outreach, outreach_id, next_action=None)
                await run_db(log_action, "engagement_react", outreach_id=outreach_id,
                    result="success",
                    details={"prospect": prospect_name, "post_id": post_id},)
                return f"Liked {prospect_name}'s post."
            else:
                error = result.get("error", "Unknown error")
                await run_db(log_action, "engagement_react_failed", outreach_id=outreach_id,
                           result="error", details={"error": error})
                return f"Reaction failed: {error}"

        elif engagement_type == "follow":
            provider_id = action_data.get("provider_id", "")
            if not provider_id:
                await client.close()
                return "Cannot follow: no provider_id in action data."

            try:
                result = await client.follow_profile(account_id, provider_id)
            except UnipileAuthError:
                await client.close()
                return "LinkedIn account disconnected. Run setup_profile() again."
            except Exception as e:
                await client.close()
                return f"Failed to follow: {e}"
            finally:
                await client.close()

            if result.get("success"):
                await run_db(save_engagement, outreach_id=outreach_id,
                    action_type="follow",
                    post_id="",
                    post_text="",
                    text=f"Followed {prospect_name}",
                    status="sent",)
                await run_db(increment_usage, "engagements_sent")
                await run_db(update_outreach, outreach_id, next_action=None)
                await run_db(log_action, "engagement_follow", outreach_id=outreach_id,
                    result="success",
                    details={"prospect": prospect_name, "provider_id": provider_id},)
                return (
                    f"Followed **{prospect_name}**\n\n"
                    "They'll get a notification: \"X started following you\"."
                )
            else:
                error = result.get("error", "Unknown error")
                await run_db(log_action, "engagement_follow_failed", outreach_id=outreach_id,
                           result="error", details={"error": error})
                return f"Follow failed: {error}"

        elif engagement_type == "endorse":
            provider_id = action_data.get("provider_id", "")
            if not provider_id:
                await client.close()
                return "Cannot endorse: no provider_id in action data."

            try:
                result = await client.endorse_skill(account_id, provider_id)
            except UnipileAuthError:
                await client.close()
                return "LinkedIn account disconnected. Run setup_profile() again."
            except Exception as e:
                await client.close()
                return f"Failed to endorse: {e}"
            finally:
                await client.close()

            if result.get("success"):
                await run_db(save_engagement, outreach_id=outreach_id,
                    action_type="endorse",
                    post_id="",
                    post_text="",
                    text=f"Endorsed {prospect_name}'s skills",
                    status="sent",)
                await run_db(increment_usage, "engagements_sent")
                await run_db(update_outreach, outreach_id, next_action=None)
                await run_db(log_action, "engagement_endorse", outreach_id=outreach_id,
                    result="success",
                    details={"prospect": prospect_name, "provider_id": provider_id},)
                return (
                    f"Endorsed **{prospect_name}**'s skills\n\n"
                    "They'll get a notification: \"X endorsed your skills\"."
                )
            else:
                error = result.get("error", "Unknown error")
                await run_db(log_action, "engagement_endorse_failed", outreach_id=outreach_id,
                           result="error", details={"error": error})
                return f"Endorsement failed: {error}"
        else:
            await client.close()
            return f"Unknown engagement type: {engagement_type}"

    return _unknown_action(action, "engagement")


# ──────────────────────────────────────────────
# Handler: Reply approval
# ──────────────────────────────────────────────

async def _handle_reply_approval(
    action: str,
    outreach_id: str,
    outreach: dict,
    next_action: str,
    custom_message: str,
    account_id: str,
) -> str:
    """Handle reply approval flow.

    Mirrors reply_to_prospect.py autopilot branch.
    """
    # Parse next_action — may be JSON {"type": "reply", "message": ..., "sentiment": ...}
    # or plain text (fallback)
    reply_message = next_action
    sentiment = "neutral"
    try:
        data = json.loads(next_action)
        if isinstance(data, dict):
            reply_message = data.get("message", next_action)
            sentiment = data.get("sentiment", "neutral")
    except (json.JSONDecodeError, TypeError):
        pass

    contact = _get_contact(outreach["contact_id"])
    if not contact:
        return f"Contact not found for outreach {outreach_id}."

    prospect_name = contact.get("name", "Unknown")

    # ── Skip ──
    if action == "skip":
        await run_db(update_outreach, outreach_id, next_action=None)
        await run_db(log_action, "reply_skipped", outreach_id=outreach_id, result="skipped",
                   details={"prospect": prospect_name, "sentiment": sentiment})
        return f"Skipped reply to {prospect_name}."

    # ── Send ──
    if action in ("yes", "send"):
        final_message = custom_message if custom_message else reply_message

        # Resolve chat_id — prefer provider_id (ACoAAA) from profile_json
        prospect_linkedin_id = ""
        pj = contact.get("profile_json")
        if pj:
            try:
                import json as _json
                _profile = _json.loads(pj) if isinstance(pj, str) else pj
                prospect_linkedin_id = _profile.get("provider_id", "")
            except Exception:
                pass
        if not prospect_linkedin_id:
            prospect_linkedin_id = contact.get("linkedin_id", "")
        if not prospect_linkedin_id:
            return f"No LinkedIn ID for {prospect_name}. Cannot send DM."

        try:
            client = get_linkedin_client()
        except UnipileError as e:
            return f"{e}"

        try:
            chat_id = await client.find_chat_for_user(account_id, prospect_linkedin_id)
        except Exception as e:
            logger.error(f"Failed to find chat: {e}")
            chat_id = None

        create_new_chat = chat_id is None

        # For new chats, extract provider_id from miniProfileUrn in URL
        prospect_provider_id = prospect_linkedin_id
        if create_new_chat and not prospect_linkedin_id.startswith("ACo"):
            url = contact.get("linkedin_url") or ""
            from urllib.parse import urlparse, parse_qs, unquote
            qs = parse_qs(urlparse(url).query)
            urn = unquote(qs.get("miniProfileUrn", [""])[0])
            if urn:
                prospect_provider_id = urn.split(":")[-1]

        # Send message
        try:
            if create_new_chat:
                send_result = await client.send_new_message(
                    account_id=account_id,
                    provider_id=prospect_provider_id,
                    text=final_message,
                )
            else:
                send_result = await client.send_message(
                    account_id=account_id,
                    chat_id=chat_id,
                    text=final_message,
                )
        except UnipileAuthError:
            await client.close()
            return (
                "LinkedIn account disconnected.\n\n"
                "Run setup_profile() again to reconnect."
            )
        except Exception as e:
            await client.close()
            return f"Failed to send reply: {e}"
        finally:
            await client.close()

        if send_result.get("success"):
            # Determine new status based on sentiment
            if sentiment == "negative":
                new_status = "closed_unhappy"
                import time as _time
                outcome_data = json.dumps({
                    "outcome": "lost",
                    "reason": "Prospect declined (negative reply)",
                    "closed_at": int(_time.time()),
                    "previous_status": outreach.get("status", ""),
                })
                await run_db(update_outreach, outreach_id, status=new_status, next_action=None, outcome_json=outcome_data)
            elif outreach.get("status") == "hot_lead":
                new_status = "hot_lead"
                await run_db(update_outreach, outreach_id, status=new_status, next_action=None)
            else:
                new_status = "messaged"
                await run_db(update_outreach, outreach_id, status=new_status, next_action=None)
            await run_db(save_message, outreach_id, role="sdr", text=final_message)
            await run_db(increment_usage, "messages_sent")
            await run_db(log_action, "reply_sent",
                outreach_id=outreach_id,
                result="success",
                details={
                    "prospect": prospect_name,
                    "sentiment": sentiment,
                    "message_length": len(final_message),
                    "approval_type": "edit" if custom_message else "approved",
                },)
            return (
                f"Replied to {prospect_name} (sentiment: {sentiment})\n"
                f'   "{final_message}"'
            )
        else:
            error = send_result.get("error", "Unknown error")
            await run_db(log_action, "reply_failed", outreach_id=outreach_id,
                result="error", details={"error": error},)
            return f"Reply failed for {prospect_name}: {error}"

    return _unknown_action(action, "reply")


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _unknown_action(action: str, context: str) -> str:
    """Return a helpful message for unknown actions."""
    valid = {
        "invitation": "'yes', 'send', 'skip', 'edit: [text]', 'stop'",
        "follow-up": "'yes', 'send', 'skip', 'edit: [text]', 'stop'",
        "engagement": "'yes', 'send', 'skip', 'edit: [text]', 'react', 'stop'",
        "reply": "'yes', 'send', 'skip', 'edit: [text]', 'stop'",
    }
    options = valid.get(context, "'yes', 'send', 'skip', 'edit: [text]', 'stop'")
    return f"Unknown action: '{action}'. Valid actions for {context}: {options}"
