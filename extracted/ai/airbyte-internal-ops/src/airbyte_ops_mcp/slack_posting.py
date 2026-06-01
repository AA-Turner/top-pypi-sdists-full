# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack message posting utilities.

This module provides core logic for posting messages to Slack channels
and threads. It complements `slack_api` (which handles reading
and approval verification) by adding write operations.

The Slack bot token is resolved from the same environment variables
used by the approval verification path, so no new secrets are required.

Security: Workspace validation ensures only URLs from the expected
Slack workspace are accepted. The tool is scoped to the feedback
workflow, and requiring a valid thread URL provides sufficient guardrails.
"""

from __future__ import annotations

import logging
import re

import requests

from airbyte_ops_mcp.slack_api import (
    SlackAPIError,
    SlackURLParseError,
    _resolve_slack_bot_token,
)

logger = logging.getLogger(__name__)

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


def post_thread_reply(
    channel_id: str,
    thread_ts: str,
    message: str,
    *,
    token: str | None = None,
) -> str:
    """Post a reply to a Slack thread.

    Args:
        channel_id: Slack channel ID (e.g. `C0ACUHRP6B1`).
        thread_ts: Parent thread timestamp in Slack API format.
        message: Message text in Slack mrkdwn format.
        token: Slack bot token. Resolved from environment if not provided.

    Returns:
        The `ts` of the posted reply message.

    Raises:
        SlackAPIError: If the API call fails.
    """
    if token is None:
        token = _resolve_slack_bot_token()

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={
            "channel": channel_id,
            "thread_ts": thread_ts,
            "text": message,
            "unfurl_links": False,
            "unfurl_media": False,
        },
        timeout=30,
    )

    if not response.ok:
        raise SlackAPIError(
            f"Slack API HTTP error: {response.status_code} {response.text[:200]}"
        )

    data = response.json()
    if not data.get("ok"):
        raise SlackAPIError(
            f"Slack API error posting thread reply to {channel_id} "
            f"(thread_ts={thread_ts}): {data.get('error', 'unknown')}"
        )

    reply_ts: str = data.get("ts", "")
    logger.info(
        "Posted thread reply to channel=%s thread_ts=%s -> reply_ts=%s",
        channel_id,
        thread_ts,
        reply_ts,
    )
    return reply_ts
