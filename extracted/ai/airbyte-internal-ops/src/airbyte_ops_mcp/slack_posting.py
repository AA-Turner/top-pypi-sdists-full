# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack message posting utilities.

This module provides core logic for posting messages to Slack channels
and threads. It complements `slack_api` (which handles reading
and approval verification) by adding write operations.

Public API includes:
- `post_channel_message` / `post_thread_reply` — plain mrkdwn text posts
- `send_hitl_notification` — structured Block Kit HITL notification with
  roster-based person resolution
- `SlackPostResult` — strongly typed return for posted messages
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from urllib.parse import urlparse

import requests

from airbyte_ops_mcp.internal_team_roster import fetch_roster
from airbyte_ops_mcp.slack_api import (
    SlackAPIError,
    SlackURLParseError,
    _resolve_slack_bot_token,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SlackPostResult:
    """Strongly typed result from a Slack `chat.postMessage` call."""

    channel_id: str
    """Channel ID where the message was posted."""

    ts: str
    """Timestamp of the posted message (Slack message ID)."""

    @property
    def permalink(self) -> str:
        """Build a Slack permalink from the channel and ts."""
        ts_digits = self.ts.replace(".", "")
        return (
            f"https://airbytehq-team.slack.com/archives/{self.channel_id}/p{ts_digits}"
        )


# Expected Slack workspace subdomain — reject URLs from other workspaces.
_EXPECTED_WORKSPACE = "airbytehq-team"

# Matches Slack message URLs and extracts channel + timestamp digits.
_SLACK_THREAD_URL_PATTERN = re.compile(
    r"^https://(?P<workspace>[a-zA-Z0-9_-]+)\.slack\.com"
    r"/archives/(?P<channel>[A-Z0-9]+)"
    r"/p(?P<ts_digits>\d+)"
    r"(?:\?.*)?$"
)


def parse_slack_thread_url(url: str) -> tuple[str, str]:
    """Parse a Slack message URL into (channel_id, thread_ts).

    Args:
        url: A Slack message permalink, e.g.
            `https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711122019`

    Returns:
        Tuple of `(channel_id, thread_ts)` where `thread_ts` is in
        Slack API format (e.g. `"1773062711.122019"`).

    Raises:
        SlackURLParseError: If the URL does not match the expected format.
    """
    match = _SLACK_THREAD_URL_PATTERN.match(url)
    if not match:
        raise SlackURLParseError(
            f"Invalid Slack thread URL: {url}. "
            "Expected format: https://<workspace>.slack.com/archives/<channel>/p<ts_digits>"
        )

    workspace = match.group("workspace")
    if workspace != _EXPECTED_WORKSPACE:
        raise SlackURLParseError(
            f"Unexpected Slack workspace '{workspace}' in URL: {url}. "
            f"Expected '{_EXPECTED_WORKSPACE}'."
        )

    channel_id = match.group("channel")
    ts_digits = match.group("ts_digits")

    # Reconstruct Slack ts format: first 10 digits are seconds, rest are microseconds.
    if len(ts_digits) <= 10:
        thread_ts = ts_digits
    else:
        thread_ts = f"{ts_digits[:10]}.{ts_digits[10:]}"

    return channel_id, thread_ts


def _post_message(
    channel_id: str,
    text: str,
    *,
    thread_ts: str | None = None,
    blocks: list[dict] | None = None,
    username: str | None = None,
    token: str | None = None,
) -> SlackPostResult:
    """Low-level helper: post a `chat.postMessage` call.

    Args:
        channel_id: Slack channel ID.
        text: Fallback text (shown in notifications / search).
        thread_ts: If provided, the message is posted as a thread reply.
        blocks: Optional Block Kit blocks for rich formatting.
        username: Optional bot display name override.
        token: Slack bot token. Resolved from environment if not provided.

    Raises:
        SlackAPIError: If the API call fails or returns a non-OK response.
    """
    if token is None:
        token = _resolve_slack_bot_token()

    payload: dict = {
        "channel": channel_id,
        "text": text,
        "unfurl_links": False,
        "unfurl_media": False,
    }
    if thread_ts is not None:
        payload["thread_ts"] = thread_ts
    if blocks is not None:
        payload["blocks"] = blocks
    if username is not None:
        payload["username"] = username

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json=payload,
        timeout=30,
    )

    if not response.ok:
        raise SlackAPIError(
            f"Slack API HTTP error: {response.status_code} {response.text[:200]}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise SlackAPIError(
            f"Slack API returned non-JSON response for {channel_id}: "
            f"{response.text[:200]}"
        ) from exc

    if not data.get("ok"):
        raise SlackAPIError(
            f"Slack API error posting to {channel_id}: {data.get('error', 'unknown')}"
        )

    return SlackPostResult(
        channel_id=data.get("channel", channel_id),
        ts=data.get("ts", ""),
    )


def post_channel_message(
    channel_id: str,
    text: str,
    *,
    token: str | None = None,
) -> SlackPostResult:
    """Post a message to a Slack channel.

    Args:
        channel_id: Slack channel ID (e.g. `C06D5RCLBV4`).
        text: Message text in Slack mrkdwn format.
        token: Slack bot token. Resolved from environment if not provided.

    Returns:
        `SlackPostResult` with channel_id and ts of the posted message.

    Raises:
        SlackAPIError: If the API call fails.
    """
    result = _post_message(channel_id, text, token=token)
    logger.info("Posted message to channel=%s -> ts=%s", channel_id, result.ts)
    return result


def post_thread_reply(
    channel_id: str,
    thread_ts: str,
    message: str,
    *,
    token: str | None = None,
) -> SlackPostResult:
    """Post a reply to a Slack thread.

    Args:
        channel_id: Slack channel ID (e.g. `C0ACUHRP6B1`).
        thread_ts: Parent thread timestamp in Slack API format.
        message: Message text in Slack mrkdwn format.
        token: Slack bot token. Resolved from environment if not provided.

    Returns:
        `SlackPostResult` with channel_id and ts of the posted reply.

    Raises:
        SlackAPIError: If the API call fails.
    """
    result = _post_message(channel_id, message, thread_ts=thread_ts, token=token)
    logger.info(
        "Posted thread reply to channel=%s thread_ts=%s -> reply_ts=%s",
        channel_id,
        thread_ts,
        result.ts,
    )
    return result


# ---------------------------------------------------------------------------
# HITL notification helpers
# ---------------------------------------------------------------------------

_SLACK_ID_PATTERN = re.compile(r"^U[A-Z0-9]{8,}$")
_SLACK_USERGROUP_ID_PATTERN = re.compile(r"^S[A-Z0-9]{8,}$")


def _resolve_to_slack_id(
    identifier: str,
    roster: list[dict[str, str | int | None]],
) -> str | None:
    """Resolve an identifier to a Slack user or usergroup ID.

    Slack IDs and usergroup IDs bypass roster lookup. Other identifiers are
    matched against email, GitHub handle, and Slack ID fields.
    """
    identifier = identifier.strip()
    if identifier.startswith("@"):
        identifier = identifier[1:]
        if not identifier:
            return None

    if _SLACK_ID_PATTERN.match(identifier) or _SLACK_USERGROUP_ID_PATTERN.match(
        identifier
    ):
        return identifier

    identifier_lower = identifier.lower()

    for person in roster:
        slack_email = person.get("slack_email")
        if (
            slack_email
            and isinstance(slack_email, str)
            and slack_email.lower() == identifier_lower
        ):
            slack_id = person.get("slack_id")
            if slack_id and isinstance(slack_id, str):
                return slack_id

        github_handle = person.get("github_handle")
        if (
            github_handle
            and isinstance(github_handle, str)
            and github_handle.lower() == identifier_lower
        ):
            slack_id = person.get("slack_id")
            if slack_id and isinstance(slack_id, str):
                return slack_id

        github_email = person.get("github_public_email")
        if (
            github_email
            and isinstance(github_email, str)
            and github_email.lower() == identifier_lower
        ):
            slack_id = person.get("slack_id")
            if slack_id and isinstance(slack_id, str):
                return slack_id

    return None


def _format_mention(identifier: str, slack_id: str | None) -> str:
    """Format a person or usergroup as a Slack mention or fallback plain text."""
    if slack_id:
        if _SLACK_USERGROUP_ID_PATTERN.match(slack_id):
            return f"<!subteam^{slack_id}>"
        return f"<@{slack_id}>"

    mention_id = identifier.strip()
    if _SLACK_USERGROUP_ID_PATTERN.match(mention_id):
        return f"<!subteam^{mention_id}>"
    if _SLACK_ID_PATTERN.match(mention_id):
        return f"<@{mention_id}>"
    return f"`{mention_id}` (could not resolve to Slack)"


def format_github_login_contact(github_login: str) -> str:
    """Format a GitHub login as a Slack mention when the roster resolves it."""
    try:
        roster = fetch_roster()
        slack_id = _resolve_to_slack_id(github_login, roster)
    except Exception as exc:
        logger.warning(
            "Could not resolve GitHub login %s through the internal roster: %s",
            github_login,
            exc,
        )
        return github_login
    if slack_id:
        return _format_mention(github_login, slack_id)
    return github_login


def _extract_short_session_token(url: str, length: int = 8) -> str | None:
    """Extract a short token from the trailing path segment of a URL.

    For `https://app.devin.ai/sessions/7b60ceb6abab46c19cbe689ebdfed874`
    returns `7b60ceb6` (first `length` hex characters).
    """
    path = urlparse(url).path.rstrip("/")
    segment = path.rsplit("/", 1)[-1] if "/" in path else ""
    if segment and len(segment) >= length and re.fullmatch(r"[0-9a-fA-F-]+", segment):
        return segment[:length]
    return None


def _extract_number_from_url(url: str) -> str | None:
    """Extract the trailing numeric identifier from a GitHub PR or issue URL."""
    match = re.search(r"/(pull|issues|actions/runs)/([0-9]+)(?:/|$)", url)
    if match:
        return match.group(2)
    return None


def _derive_agent_name(agent_session_url: str) -> str:
    """Derive an agent display name from the session URL.

    For `https://app.devin.ai/sessions/...` returns `Devin.ai`.
    Falls back to the full hostname if the domain has fewer than two parts.
    """
    hostname = urlparse(agent_session_url).hostname or ""
    parts = hostname.rsplit(".", 2)
    if len(parts) >= 2:
        base = f"{parts[-2]}.{parts[-1]}"
        return base[0].upper() + base[1:]
    return hostname.capitalize() if hostname else "Agent"


def _build_hitl_blocks(
    target_person: str,
    target_slack_id: str | None,
    cc_mentions: list[str],
    message: str,
    *,
    agent_session_url: str | None = None,
    pr_url: str | None = None,
    issue_url: str | None = None,
    additional_actions: dict[str, str] | None = None,
    approval_requested: bool = False,
    approval_request_summary: str | None = None,
    approval_request_detail_url: str | None = None,
    approval_metadata: dict[str, str] | None = None,
    sender_name: str = "Agent (No-Reply)",
    header_emoji: str = "\U0001f64b",
    header_label: str = "Human-in-the-loop request",
    context_footer: str | None = None,
    connector_name: str | None = None,
) -> list[dict]:
    """Build Slack Block Kit blocks for an HITL notification message."""
    blocks: list[dict] = []

    # -- Header --
    if connector_name:
        header_text = f"{header_emoji} {header_label} \u2014 {connector_name}"
    else:
        header_text = f"{header_emoji} {header_label}"
    blocks.append(
        {
            "type": "header",
            "text": {"type": "plain_text", "text": header_text, "emoji": True},
        }
    )

    # -- To / CC line --
    target_mention = _format_mention(target_person, target_slack_id)
    to_line = f"*To:* {target_mention}"
    if cc_mentions:
        to_line += f"  |  *CC:* {', '.join(cc_mentions)}"

    blocks.append(
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": to_line}],
        }
    )

    blocks.append({"type": "divider"})

    # -- Message body --
    blocks.append(
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": message},
        }
    )

    blocks.append({"type": "divider"})

    # -- Action buttons --
    buttons: list[dict] = []
    if approval_requested:
        button_payload: dict[str, str | dict[str, str]] = {}
        if agent_session_url:
            button_payload["session_url"] = agent_session_url
        if approval_metadata:
            button_payload["approval_metadata"] = approval_metadata
        approve_value = json.dumps(button_payload)
        approve_button: dict = {
            "type": "button",
            "text": {"type": "plain_text", "text": "Approve", "emoji": True},
            "style": "primary",
            "value": approve_value,
            "action_id": "approve_request",
        }
        if approval_request_summary:
            approve_button["confirm"] = {
                "title": {"type": "plain_text", "text": "Confirm Approval"},
                "text": {
                    "type": "mrkdwn",
                    "text": f"> {approval_request_summary}"[:300],
                },
                "confirm": {"type": "plain_text", "text": "Yes, Approve"},
                "deny": {"type": "plain_text", "text": "Cancel"},
            }
        buttons.append(approve_button)

        reject_button: dict = {
            "type": "button",
            "text": {"type": "plain_text", "text": "Reject", "emoji": True},
            "style": "danger",
            "value": approve_value,
            "action_id": "reject_request",
        }
        if approval_request_summary:
            reject_button["confirm"] = {
                "title": {"type": "plain_text", "text": "Confirm Rejection"},
                "text": {
                    "type": "mrkdwn",
                    "text": f"> {approval_request_summary}"[:300],
                },
                "confirm": {"type": "plain_text", "text": "Yes, Reject"},
                "deny": {"type": "plain_text", "text": "Cancel"},
            }
        buttons.append(reject_button)

    if approval_request_detail_url:
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "View Details", "emoji": True},
                "url": approval_request_detail_url,
                "action_id": "view_approval_details",
            }
        )

    if pr_url:
        pr_number = _extract_number_from_url(pr_url)
        pr_label = f"View PR #{pr_number}" if pr_number else "View PR"
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": pr_label, "emoji": True},
                "url": pr_url,
                "action_id": "view_pr",
            }
        )
    if issue_url:
        issue_number = _extract_number_from_url(issue_url)
        issue_label = f"View Issue #{issue_number}" if issue_number else "View Issue"
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": issue_label, "emoji": True},
                "url": issue_url,
                "action_id": "view_issue",
            }
        )
    if additional_actions:
        for label, url in additional_actions.items():
            buttons.append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": label[:75],
                        "emoji": True,
                    },
                    "url": url,
                    "action_id": f"extra_{label[:50]}",
                }
            )

    # "View Session" button — only rendered when agent_session_url is provided
    if agent_session_url:
        session_token = _extract_short_session_token(agent_session_url)
        session_label = (
            f"View Session ({session_token})" if session_token else "View Session"
        )
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": session_label, "emoji": True},
                "url": agent_session_url,
                "action_id": "view_session",
            }
        )

    if buttons:
        if not approval_requested:
            buttons[0]["style"] = "primary"
        blocks.append({"type": "actions", "elements": buttons})

    # -- Footer --
    footer_parts = [
        f"Sent by *{sender_name}*. Please respond in the linked session or PR, not in this thread."
    ]
    if context_footer:
        footer_parts.append(context_footer)

    blocks.append(
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "\n".join(footer_parts)}],
        }
    )

    return blocks


def send_hitl_notification(
    target_person: str,
    message: str,
    *,
    agent_session_url: str | None = None,
    connector_name: str | None = None,
    header_emoji: str = "\U0001f64b",
    header_label: str = "Human-in-the-loop request",
    cc_persons: list[str] | None = None,
    pr_url: str | None = None,
    issue_url: str | None = None,
    additional_actions: dict[str, str] | None = None,
    approval_requested: bool = False,
    approval_request_summary: str | None = None,
    approval_request_detail_url: str | None = None,
    approval_metadata: dict[str, str] | None = None,
    channel_override: str | None = None,
    context_footer: str | None = None,
    slack_token: str | None = None,
    github_token: str | None = None,
    roster: list[dict[str, str | int | None]] | None = None,
) -> SlackPostResult:
    """Send a Slack HITL notification with Block Kit formatting and roster resolution.

    This is the primary Python interface for HITL notifications. It resolves
    person identifiers to Slack user IDs via the team roster, builds Block Kit
    blocks, and posts to Slack.

    Args:
        target_person: Primary recipient (email, GitHub handle, Slack user ID,
            or Slack usergroup ID).
        message: Message body in Slack mrkdwn format.
        agent_session_url: Optional URL to the agent session or CI run. When
            provided, a "View Session" button is rendered in the message.
        connector_name: Optional connector name for the header.
        header_emoji: Emoji prefix for the header block.
        header_label: Label text for the header block.
        cc_persons: Additional person or Slack usergroup identifiers to CC.
        pr_url: Optional PR URL for an action button.
        issue_url: Optional issue URL for an action button.
        additional_actions: Extra action buttons as `{label: url}` pairs.
        approval_requested: Whether to render Approve/Reject buttons.
        approval_request_summary: Short summary shown in confirmation dialog.
        approval_request_detail_url: URL for a "View Details" button.
        approval_metadata: Key-value pairs embedded in approval button payloads.
        channel_override: Slack channel ID override. Defaults to env
            `SLACK_CHANNEL_HITL` or `"human-in-the-loop"`.
        context_footer: Additional text appended to the footer.
        slack_token: Slack bot token. Resolved from `SLACK_BOT_TOKEN_HITL` /
            `SLACK_HYDRA_BOT_TOKEN` / `SLACK_BOT_TOKEN_AIRBYTE_TEAM` if None.
        github_token: GitHub token for roster download. Resolved from env if None.
        roster: Pre-loaded roster list. If provided, skips `fetch_roster()` call.

    Raises:
        RuntimeError: If no Slack bot token is available.
        SlackAPIError: If the Slack API call fails.
    """
    token = slack_token or os.environ.get(
        "SLACK_BOT_TOKEN_HITL",
        os.environ.get(
            "SLACK_HYDRA_BOT_TOKEN",
            os.environ.get("SLACK_BOT_TOKEN_AIRBYTE_TEAM", ""),
        ),
    )
    if not token:
        raise RuntimeError(
            "No Slack bot token found. Set SLACK_BOT_TOKEN_HITL, "
            "SLACK_HYDRA_BOT_TOKEN, or SLACK_BOT_TOKEN_AIRBYTE_TEAM."
        )

    channel = channel_override or os.environ.get(
        "SLACK_CHANNEL_HITL", "human-in-the-loop"
    )

    if roster is None:
        roster = fetch_roster(token=github_token)

    target_slack_id = _resolve_to_slack_id(target_person, roster)

    cc_mentions: list[str] = []
    if cc_persons:
        for person in cc_persons:
            cc_slack_id = _resolve_to_slack_id(person, roster)
            cc_mentions.append(_format_mention(person, cc_slack_id))

    sender_name: str
    if agent_session_url:
        sender_name = f"{_derive_agent_name(agent_session_url)} (No-Reply)"
    else:
        sender_name = "Airbyte Ops (No-Reply)"

    blocks = _build_hitl_blocks(
        target_person=target_person,
        target_slack_id=target_slack_id,
        cc_mentions=cc_mentions,
        message=message,
        agent_session_url=agent_session_url,
        pr_url=pr_url,
        issue_url=issue_url,
        additional_actions=additional_actions,
        approval_requested=approval_requested,
        approval_request_summary=approval_request_summary,
        approval_request_detail_url=approval_request_detail_url,
        approval_metadata=approval_metadata,
        sender_name=sender_name,
        header_emoji=header_emoji,
        header_label=header_label,
        context_footer=context_footer,
        connector_name=connector_name,
    )

    target_mention = _format_mention(target_person, target_slack_id)
    fallback_text = f"{header_label} for {target_mention}: {message}"

    return _post_message(
        channel,
        fallback_text,
        blocks=blocks,
        username=sender_name,
        token=token,
    )
