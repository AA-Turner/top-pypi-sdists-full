# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack webhook handler for Block Kit interactive components.

Processes incoming Slack interaction payloads (button clicks, etc.),
extracts the target Devin session URL from the button value, and
injects a notification message into the session.

When an approval or rejection button is clicked, a thread reply is posted
as a durable, verifiable approval record. The reply URL is included in
the notification injected into the Devin session so that MCP tools can
use it as an `approval_comment_url`.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

import requests

from agent_message_bus.devin_client import INJECT_OK, inject_message

logger = logging.getLogger(__name__)

# Slack allows up to 5 minutes of clock skew for signature validation
_SLACK_TIMESTAMP_MAX_AGE_SECONDS = 300


def verify_slack_signature(
    payload_body: bytes,
    timestamp: str,
    signature: str,
    signing_secret: str,
) -> bool:
    """Verify a Slack request signature (X-Slack-Signature).

    Slack uses HMAC-SHA256 with a versioned signing scheme:
    `v0=HMAC_SHA256(signing_secret, "v0:{timestamp}:{body}")`

    Args:
        payload_body: Raw request body bytes.
        timestamp: Value of X-Slack-Request-Timestamp header.
        signature: Value of X-Slack-Signature header.
        signing_secret: The Slack app's signing secret.

    Returns:
        True if the signature is valid and the timestamp is recent.
    """
    if not timestamp or not signature:
        return False

    # Reject requests older than 5 minutes (replay protection)
    try:
        ts = int(timestamp)
    except ValueError:
        return False

    if abs(time.time() - ts) > _SLACK_TIMESTAMP_MAX_AGE_SECONDS:
        logger.warning("Slack request timestamp too old: %s", timestamp)
        return False

    sig_basestring = f"v0:{timestamp}:{payload_body.decode('utf-8')}"
    expected = (
        "v0="
        + hmac.new(
            signing_secret.encode("utf-8"),
            sig_basestring.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
    )

    return hmac.compare_digest(expected, signature)


def _parse_button_value(action: dict[str, Any]) -> dict[str, Any]:
    """Parse the JSON payload from a Slack button's `value` field.

    Returns the parsed dict, or an empty dict if the value is not valid JSON.
    """
    value = action.get("value", "")
    if not value:
        return {}
    try:
        data = json.loads(value)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, TypeError):
        pass
    return {}


def _extract_session_url_from_action(action: dict[str, Any]) -> str | None:
    """Extract the Devin session URL from a Slack action payload.

    The session URL is expected to be embedded in the button's `value`
    field as a JSON string or a direct URL.

    Args:
        action: A single action element from the Slack interaction payload.

    Returns:
        The session URL if found, None otherwise.
    """
    parsed = _parse_button_value(action)
    if parsed:
        return parsed.get("session_url")

    # Fall back to treating the value as a direct URL
    value = action.get("value", "")
    if "app.devin.ai/sessions/" in value:
        return value

    return None


def _format_slack_notification(
    action: dict[str, Any],
    user: dict[str, Any],
    message_text: str | None = None,
    approval_reply_url: str | None = None,
) -> str:
    """Format a notification message for a Devin session from a Slack action.

    Args:
        action: The Slack action element (button click, etc.).
        user: The Slack user who performed the action.
        message_text: Optional original message text for context.
        approval_reply_url: Optional Slack message URL for the approval
            thread reply. When present, MCP tools can use this as an
            `approval_slack_url` to verify the approver's identity.

    Returns:
        Formatted notification string.
    """
    user_name = user.get("name", user.get("username", "someone"))
    action_id = action.get("action_id", "unknown_action")
    button_text = action.get("text", {}).get("text", action_id)

    parts = [
        f"Slack action received: @{user_name} clicked '{button_text}'",
    ]

    if message_text:
        # Truncate for context
        if len(message_text) > 300:
            message_text = message_text[:300] + "..."
        parts.append(f"Original message context: {message_text}")

    if approval_reply_url:
        parts.append(f"Approval record URL (for MCP tools): {approval_reply_url}")

    return "\n\n".join(parts)


# Action IDs that represent approval/rejection actions whose buttons
# should all be morphed together when any one of them is clicked.
_APPROVAL_ACTION_IDS = frozenset({"approve_request", "reject_request"})


def _update_message_after_action(
    response_url: str,
    original_message: dict[str, Any],
    clicked_action_id: str,
    user_name: str,
) -> None:
    """Update the original Slack message after an approval or rejection.

    When an approval-family button (approve or reject) is clicked, *all*
    sibling approval-family buttons are replaced with non-interactive
    status indicators so that neither can be clicked again.  Non-approval
    buttons (e.g. "View PR", "View Details") are left untouched.

    Args:
        response_url: The response_url from the Slack interaction payload.
        original_message: The original message dict from the payload.
        clicked_action_id: The action_id of the button that was clicked.
        user_name: Display name of the user who clicked.
    """
    if not response_url:
        logger.warning("No response_url in payload, cannot update message")
        return

    is_rejection = clicked_action_id == "reject_request"
    action_at = datetime.now(tz=timezone.utc).strftime("%b %-d, %Y at %H:%M UTC")

    # Compute status fields before iterating elements so they are
    # available for both the clicked button and its sibling.
    if is_rejection:
        status_emoji = ":x:"
        status_verb = "Rejected"
        dialog_title = "Action Already Rejected"
    else:
        status_emoji = ":white_check_mark:"
        status_verb = "Approved"
        dialog_title = "Action Already Approved"

    # Generic confirm body used for the sibling button (the clicked
    # button builds its own confirm_body that includes the original
    # action summary from the confirmation dialog).
    sibling_confirm_body = f"{status_verb} by @{user_name} on {action_at}"

    blocks = original_message.get("blocks", [])
    updated_blocks: list[dict[str, Any]] = []

    for block in blocks:
        if block.get("type") != "actions":
            updated_blocks.append(block)
            continue

        # Rebuild the actions block: morph all approval-family buttons
        new_elements: list[dict[str, Any]] = []
        for element in block.get("elements", []):
            element_action_id = element.get("action_id", "")

            if element_action_id not in _APPROVAL_ACTION_IDS:
                # Keep non-approval buttons (View PR, View Details, etc.)
                new_elements.append(element)
                continue

            is_clicked = element_action_id == clicked_action_id

            if is_clicked:
                # The button the user actually clicked — show full status
                original_action_summary = element.get("confirm", {}).get("text", {}).get("text", "")
                confirm_lines: list[str] = []
                if original_action_summary:
                    confirm_lines.append(original_action_summary)

                confirm_lines.append(f"{status_verb} by @{user_name} on {action_at}")
                confirm_body = "\n\n".join(confirm_lines)[:300]

                replacement: dict[str, Any] = {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": f"{status_emoji} {status_verb} by @{user_name}",
                        "emoji": True,
                    },
                    "action_id": f"{element_action_id}_done",
                    "confirm": {
                        "title": {
                            "type": "plain_text",
                            "text": dialog_title,
                        },
                        "text": {
                            "type": "mrkdwn",
                            "text": confirm_body,
                        },
                        "confirm": {
                            "type": "plain_text",
                            "text": "OK",
                        },
                        "deny": {
                            "type": "plain_text",
                            "text": "Close",
                        },
                    },
                }
                new_elements.append(replacement)
            else:
                # Sibling approval button that was NOT clicked — grey it out
                # but show the same no-op dialog so users know the outcome.
                new_elements.append(
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": element.get("text", {}).get("text", element_action_id),
                            "emoji": True,
                        },
                        "action_id": f"{element_action_id}_done",
                        "confirm": {
                            "title": {
                                "type": "plain_text",
                                "text": dialog_title,
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": sibling_confirm_body,
                            },
                            "confirm": {
                                "type": "plain_text",
                                "text": "OK",
                            },
                            "deny": {
                                "type": "plain_text",
                                "text": "Close",
                            },
                        },
                    }
                )

        updated_blocks.append({"type": "actions", "elements": new_elements})

    try:
        resp = requests.post(
            response_url,
            json={
                "replace_original": True,
                "blocks": updated_blocks,
            },
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if resp.ok:
            logger.info("Updated Slack message after %s action", clicked_action_id)
        else:
            logger.warning(
                "Failed to update Slack message via response_url: %s %s",
                resp.status_code,
                resp.text[:200],
            )
    except requests.RequestException as exc:
        logger.warning("Error posting to response_url: %s", exc)


def _get_slack_bot_token() -> str | None:
    """Retrieve the Slack bot token from environment.

    Returns:
        The bot token string, or None if not configured.
    """
    return os.environ.get("SLACK_BOT_TOKEN") or os.environ.get("SLACK_BOT_TOKEN_HITL")


def _build_slack_message_url(
    channel_id: str,
    message_ts: str,
    *,
    thread_ts: str | None = None,
) -> str:
    """Build a Slack message permalink from channel and timestamp.

    Constructs a URL in the format:
    `https://airbytehq-team.slack.com/archives/{channel}/p{ts_without_dot}`

    If *thread_ts* is provided the `?thread_ts=...&cid=...` query params
    are appended so the link opens inside the thread.

    Args:
        channel_id: Slack channel ID (e.g. `C08BHPUMEPJ`).
        message_ts: Message timestamp (e.g. `1773062711.122019`).
        thread_ts: Parent thread timestamp, if the message is a reply.

    Returns:
        Slack message URL string.
    """
    ts_no_dot = message_ts.replace(".", "")
    base = f"https://airbytehq-team.slack.com/archives/{channel_id}/p{ts_no_dot}"
    if thread_ts:
        base += f"?thread_ts={thread_ts}&cid={channel_id}"
    return base


def _post_approval_thread_reply(
    channel_id: str,
    thread_ts: str,
    user_id: str,
    user_name: str,
    is_approved: bool,
    bot_token: str,
    approval_metadata: dict[str, str] | None = None,
) -> str | None:
    """Post a thread reply as a durable approval/rejection record.

    The reply contains both a human-readable summary and a structured
    metadata block that MCP tools can reliably parse to extract the
    approver's Slack user ID.

    Args:
        channel_id: Slack channel where the original message lives.
        thread_ts: Timestamp of the parent message (used as `thread_ts`).
        user_id: Slack user ID of the person who clicked the button.
        user_name: Display name of the person.
        is_approved: True for approval, False for rejection.
        bot_token: Slack Bot User OAuth Token.
        approval_metadata: Optional key-value pairs from the button payload
            to include in the approval record (e.g. `secret_alias`,
            `session_id`).

    Returns:
        The Slack message URL of the posted reply, or None on failure.
    """
    action_at_utc = datetime.now(tz=timezone.utc)
    action_at = action_at_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Display timestamp in US/Pacific (auto-detects PST vs PDT)
    pacific_tz = ZoneInfo("America/Los_Angeles")
    action_at_pacific = action_at_utc.astimezone(pacific_tz)
    # Determine PST vs PDT label
    tz_abbr = action_at_pacific.strftime("%Z")  # e.g. "PST" or "PDT"
    if not tz_abbr or tz_abbr == action_at_pacific.strftime("%z"):
        # strftime %Z may return empty or offset on some platforms; fall back
        tz_abbr = "PT"
    action_at_display = action_at_pacific.strftime(f"%b %-d, %Y at %H:%M {tz_abbr}")

    if is_approved:
        emoji = ":white_check_mark:"
        verb = "Approved"
    else:
        emoji = ":x:"
        verb = "Rejected"

    # Human-readable line
    text = f"{emoji} *{verb}* by <@{user_id}> \u2014 _{action_at_display}_"

    # Structured metadata block for machine parsing
    record: dict[str, str] = {
        "type": "approval_record",
        "action": "approved" if is_approved else "rejected",
        "user_id": user_id,
        "user_name": user_name,
        "timestamp": action_at,
    }
    # Include passthrough metadata (e.g. secret_alias, session_id)
    if approval_metadata:
        for key, value in approval_metadata.items():
            if key not in record:  # don't overwrite core fields
                record[key] = value
    metadata_json = json.dumps(record)

    blocks: list[dict[str, Any]] = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": text},
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"```{metadata_json}```",
                }
            ],
        },
    ]

    try:
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {bot_token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={
                "channel": channel_id,
                "thread_ts": thread_ts,
                "blocks": blocks,
                "text": f"{verb} by @{user_name}",
                "unfurl_links": False,
                "unfurl_media": False,
            },
            timeout=10,
        )
        data = resp.json()
        if not data.get("ok"):
            logger.warning(
                "Slack API error posting approval reply: %s",
                data.get("error", "unknown"),
            )
            return None

        reply_ts = data.get("ts", "")
        reply_channel = data.get("channel", channel_id)
        reply_url = _build_slack_message_url(
            channel_id=reply_channel,
            message_ts=reply_ts,
            thread_ts=thread_ts,
        )
        logger.info(
            "Posted approval thread reply in %s (ts=%s): %s",
            reply_channel,
            reply_ts,
            reply_url,
        )
        return reply_url

    except requests.RequestException as exc:
        logger.warning("Error posting approval thread reply: %s", exc)
        return None


def handle_slack_interaction(payload: dict[str, Any]) -> dict[str, Any]:
    """Process a Slack interactive component payload.

    Extracts the Devin session URL from button values and injects
    a notification message into the target session. After successful
    delivery, updates the original Slack message to mark the button
    as approved.

    For approval/rejection actions, a thread reply is posted as a
    durable approval record before injecting the notification. The
    reply URL is included in the notification so MCP tools can use
    it as an `approval_comment_url`.

    Args:
        payload: The parsed Slack interaction payload.

    Returns:
        Summary dict with processing results.
    """
    payload_type = payload.get("type", "")

    if payload_type != "block_actions":
        return {"status": "skipped", "reason": f"unsupported_type: {payload_type}"}

    actions = payload.get("actions", [])
    user = payload.get("user", {})
    message = payload.get("message", {})
    message_text = message.get("text", "")
    response_url = payload.get("response_url", "")
    user_name = user.get("name", user.get("username", "someone"))
    user_id = user.get("id", "")

    # Extract channel and thread info for posting approval replies
    channel = payload.get("channel", {})
    channel_id = channel.get("id", "") if isinstance(channel, dict) else str(channel)
    message_ts = message.get("ts", "")

    bot_token = _get_slack_bot_token()

    notified = 0
    errors = 0

    for action in actions:
        action_id = action.get("action_id", "")

        # Skip post-action "done" buttons — they are non-interactive status
        # indicators created by _update_message_after_action and carry no
        # session URL.  Clicking them is harmless but should not log warnings.
        if action_id.endswith("_done"):
            logger.debug("Ignoring post-action button click: %s", action_id)
            continue

        session_url = _extract_session_url_from_action(action)
        if not session_url:
            logger.warning(
                "No session URL found in Slack action value: %s",
                action.get("value", ""),
            )
            continue

        # Post approval thread reply for approval-family actions
        approval_reply_url: str | None = None
        if action_id in _APPROVAL_ACTION_IDS and bot_token and channel_id and message_ts:
            is_approved = action_id != "reject_request"
            # Extract passthrough metadata from the button value
            button_data = _parse_button_value(action)
            meta = button_data.get("approval_metadata")
            approval_reply_url = _post_approval_thread_reply(
                channel_id=channel_id,
                thread_ts=message_ts,
                user_id=user_id,
                user_name=user_name,
                is_approved=is_approved,
                bot_token=bot_token,
                approval_metadata=meta if isinstance(meta, dict) else None,
            )
        elif action_id in _APPROVAL_ACTION_IDS and not bot_token:
            logger.warning(
                "Cannot post approval thread reply: "
                "SLACK_BOT_TOKEN / SLACK_BOT_TOKEN_HITL not configured"
            )

        notification = _format_slack_notification(
            action, user, message_text, approval_reply_url=approval_reply_url
        )
        result = inject_message(session_url, notification)

        if result == INJECT_OK:
            notified += 1
            # Update the original message to reflect the action taken
            if action_id and response_url:
                _update_message_after_action(
                    response_url=response_url,
                    original_message=message,
                    clicked_action_id=action_id,
                    user_name=user_name,
                )
        else:
            errors += 1
            logger.warning(
                "Failed to inject Slack action into session %s (result=%s)",
                session_url,
                result,
            )

    return {
        "status": "processed",
        "actions_received": len(actions),
        "notified": notified,
        "errors": errors,
    }
