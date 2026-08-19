# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack API utilities for approval verification.

This module provides core utilities for verifying Slack-based approval
records.  It mirrors the pattern established in :pymod:`github_api` for
GitHub comment-based approvals but operates against Slack message URLs
instead.

The trust chain is identical to the GitHub path:

1. The calling agent supplies a Slack message URL (verifiable, not
   forgeable by the agent).
2. This module fetches the message server-side from the Slack API.
3. The approver's Slack user ID is extracted from the structured
   metadata block embedded in the message by the message-bus bot.
4. The Slack user ID is resolved to an `@airbyte.io` email address
   via the internal team roster (preferred) or Slack `users.info` API.
5. The email domain is validated before returning.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from airbyte_ops_mcp.constants import EXPECTED_ADMIN_EMAIL_DOMAIN
from airbyte_ops_mcp.internal_team_roster import fetch_roster, search_roster

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Slack workspace URL pattern
# ---------------------------------------------------------------------------

# Matches Slack message URLs of the form:
#   https://{workspace}.slack.com/archives/{channel}/p{ts_digits}
# with optional query params for thread context.
_SLACK_MESSAGE_URL_PATTERN = re.compile(
    r"^https://(?P<workspace>[a-zA-Z0-9_-]+)\.slack\.com"
    r"/archives/(?P<channel>[A-Z0-9]+)"
    r"/p(?P<ts_digits>\d+)"
    r"(?:\?.*)?$"
)

# The workspace slug we expect for Airbyte's Slack.
_EXPECTED_WORKSPACE = "airbytehq-team"
_SLACK_MENTION_PATTERN = re.compile(
    r"^<!(?:subteam)\^(?P<id>[A-Z0-9]+)(?:\|[^>]*)?>$|^<@(?P<user_id>[A-Z0-9]+)>$"
)
_SLACK_USERGROUP_ID_PATTERN = re.compile(r"^S[A-Z0-9]{8,}$")

# Approval record constants
_APPROVAL_RECORD_TYPE = "approval_record"
_ACTION_APPROVED = "approved"
_ACTION_REJECTED = "rejected"
_VALID_ACTIONS = {_ACTION_APPROVED, _ACTION_REJECTED}

# Approval record field names
_FIELD_TYPE = "type"
_FIELD_ACTION = "action"
_FIELD_USER_ID = "user_id"
_FIELD_USER_NAME = "user_name"
_FIELD_TIMESTAMP = "timestamp"
_FIELD_SECRET_ALIAS = "secret_alias"
_FIELD_SESSION_ID = "session_id"
_FIELD_REQUEST_ID = "request_id"

# ---------------------------------------------------------------------------
# Exception classes (parallel to github_api.py)
# ---------------------------------------------------------------------------


class SlackURLParseError(Exception):
    """Raised when a Slack message URL cannot be parsed."""


class SlackAPIError(Exception):
    """Raised when a Slack API call fails."""


class SlackUserEmailNotFoundError(Exception):
    """Raised when a Slack user's @airbyte.io email cannot be resolved."""


class SlackApprovalRecordError(Exception):
    """Raised when the Slack message is not a valid approval record."""


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SlackMessageInfo:
    """Parsed components of a Slack message URL."""

    workspace: str
    """Workspace slug (e.g. `airbytehq-team`)."""

    channel_id: str
    """Slack channel ID (e.g. `C08BHPUMEPJ`)."""

    message_ts: str
    """Message timestamp in Slack API format (e.g. `1773062711.122019`)."""

    thread_ts: str | None
    """Parent thread timestamp, if present in query params."""


@dataclass(frozen=True)
class ApprovalRecord:
    """Structured approval record extracted from a Slack message."""

    action: str
    """`approved` or `rejected`."""

    user_id: str
    """Slack user ID of the approver/rejector."""

    user_name: str
    """Display name of the person."""

    timestamp: str
    """ISO-8601 timestamp of the action."""

    secret_alias: str | None = None
    """Secret alias from the original request, if present."""

    session_id: str | None = None
    """Devin session ID from the original request, if present."""

    request_id: str | None = None
    """Unique request identifier (UUIDv7) for replay-protection."""

    admin_email: str | None = None
    """Resolved `@airbyte.io` email, populated when `resolve_admin_email=True`."""


@dataclass(frozen=True)
class SlackUsergroup:
    """Slack usergroup details used to construct a usergroup mention."""

    id: str
    """Slack usergroup ID."""

    handle: str
    """Slack usergroup handle without the leading `@`."""

    name: str
    """Slack usergroup display name."""

    description: str
    """Slack usergroup description."""

    user_count: int
    """Number of members in the usergroup."""


def unwrap_slack_identifier(identifier: str) -> str:
    """Unwrap a pasted Slack user or usergroup mention to its ID.

    Plain identifiers are returned unchanged apart from surrounding whitespace.
    """
    normalized_identifier = identifier.strip()
    match = _SLACK_MENTION_PATTERN.fullmatch(normalized_identifier)
    if match:
        return match.group("id") or match.group("user_id") or normalized_identifier
    return normalized_identifier


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------


def _parse_slack_message_url(url: str) -> SlackMessageInfo:
    """Parse a Slack message URL into its components.

    Args:
        url: A Slack message permalink, e.g.
            `https://airbytehq-team.slack.com/archives/C08BHPUMEPJ/p1773062711122019`

    Returns:
        :class:`SlackMessageInfo` with extracted fields.

    Raises:
        SlackURLParseError: If the URL does not match the expected format.
    """
    match = _SLACK_MESSAGE_URL_PATTERN.match(url)
    if not match:
        raise SlackURLParseError(
            f"Invalid Slack message URL: {url}. "
            "Expected format: https://<workspace>.slack.com/archives/<channel>/p<ts_digits>"
        )

    workspace = match.group("workspace")
    if workspace != _EXPECTED_WORKSPACE:
        raise SlackURLParseError(
            f"Unexpected Slack workspace '{workspace}' in URL. "
            f"Expected '{_EXPECTED_WORKSPACE}'."
        )

    ts_digits = match.group("ts_digits")
    # Slack timestamps are epoch seconds with microseconds, e.g. "1773062711.122019"
    # The URL encodes this without the dot, so we reconstruct it.
    # Standard format: first 10 digits are seconds, rest are microseconds.
    if len(ts_digits) <= 10:
        message_ts = ts_digits
    else:
        message_ts = f"{ts_digits[:10]}.{ts_digits[10:]}"

    # Extract thread_ts from query params if present
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    thread_ts: str | None = query_params.get("thread_ts", [None])[0]

    return SlackMessageInfo(
        workspace=workspace,
        channel_id=match.group("channel"),
        message_ts=message_ts,
        thread_ts=thread_ts,
    )


# ---------------------------------------------------------------------------
# Slack API interactions
# ---------------------------------------------------------------------------


def _resolve_slack_bot_token() -> str:
    """Resolve the Slack bot token from environment variables.

    Checks `SLACK_BOT_TOKEN` and `SLACK_BOT_TOKEN_HITL` in order.

    Returns:
        The token string.

    Raises:
        SlackAPIError: If no token is found.
    """
    token = os.environ.get("SLACK_BOT_TOKEN") or os.environ.get("SLACK_BOT_TOKEN_HITL")
    if not token:
        raise SlackAPIError(
            "No Slack bot token found. Set SLACK_BOT_TOKEN or SLACK_BOT_TOKEN_HITL "
            "environment variable."
        )
    return token


def list_slack_usergroups(*, token: str | None = None) -> list[SlackUsergroup]:
    """List Slack usergroups visible to the configured bot token.

    Args:
        token: Slack bot token. Resolved from the environment when omitted.

    Returns:
        Usergroups with the fields needed to resolve Slack mention IDs.

    Raises:
        SlackAPIError: If the Slack API call fails or the token lacks
            `usergroups:read`.
    """
    if token is None:
        token = _resolve_slack_bot_token()

    client = WebClient(token=token)
    try:
        response = client.usergroups_list(include_disabled=False, include_users=True)
    except SlackApiError as error:
        slack_error = error.response.get("error", "unknown")
        if slack_error == "missing_scope":
            raise SlackAPIError(
                "Slack usergroup lookup requires the usergroups:read scope "
                "on the bot token."
            ) from error
        raise SlackAPIError(f"Slack usergroups.list failed: {slack_error}") from error

    return [
        SlackUsergroup(
            id=group.get("id", ""),
            handle=group.get("handle", ""),
            name=group.get("name", ""),
            description=group.get("description", ""),
            user_count=group.get("user_count", len(group.get("users", []))),
        )
        for group in response.get("usergroups", [])
    ]


def lookup_slack_usergroup(
    id_or_handle: str,
    *,
    token: str | None = None,
) -> list[SlackUsergroup]:
    """Find a Slack usergroup by handle, name, or exact usergroup ID.

    The `id_or_handle` value must be non-empty. A leading `@` is ignored so callers can
    search with either `oc-apis` or `@oc-apis`. Handle and name searches are
    case-insensitive partial matches. S-prefixed usergroup IDs are matched
    exactly.

    Raises:
        ValueError: If `id_or_handle` is empty or contains only whitespace.
    """
    normalized_id_or_handle = unwrap_slack_identifier(id_or_handle).removeprefix("@")
    if not normalized_id_or_handle:
        raise ValueError("Slack usergroup lookup id_or_handle must be non-empty.")

    usergroups = list_slack_usergroups(token=token)
    if _SLACK_USERGROUP_ID_PATTERN.fullmatch(normalized_id_or_handle):
        return [
            usergroup
            for usergroup in usergroups
            if usergroup.id == normalized_id_or_handle
        ]

    normalized_id_or_handle = normalized_id_or_handle.casefold()
    return [
        usergroup
        for usergroup in usergroups
        if normalized_id_or_handle in usergroup.handle.casefold()
        or normalized_id_or_handle in usergroup.name.casefold()
    ]


def _fetch_slack_message(
    channel_id: str,
    message_ts: str,
    *,
    token: str | None = None,
) -> dict:
    """Fetch a single Slack message by channel and timestamp.

    Uses `conversations.history` with `latest=ts`, `inclusive=true`,
    `limit=1` to retrieve the exact message.

    Args:
        channel_id: Slack channel ID.
        message_ts: Message timestamp.
        token: Slack bot token. Resolved from env if not provided.

    Returns:
        The message dict from the Slack API.

    Raises:
        SlackAPIError: If the API call fails or message is not found.
    """
    if token is None:
        token = _resolve_slack_bot_token()

    response = requests.get(
        "https://slack.com/api/conversations.history",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        params={
            "channel": channel_id,
            "latest": message_ts,
            "inclusive": "true",
            "limit": "1",
        },
        timeout=15,
    )
    if not response.ok:
        raise SlackAPIError(
            f"Slack API HTTP error: {response.status_code} {response.text[:200]}"
        )
    data = response.json()

    if not data.get("ok"):
        raise SlackAPIError(
            f"Slack API error fetching message in {channel_id} at ts={message_ts}: "
            f"{data.get('error', 'unknown')}"
        )

    messages = data.get("messages", [])
    if not messages:
        raise SlackAPIError(
            f"No message found in channel {channel_id} at timestamp {message_ts}."
        )

    msg = messages[0]
    # Verify we got the exact message we asked for
    if msg.get("ts") != message_ts:
        raise SlackAPIError(
            f"Timestamp mismatch: requested {message_ts}, got {msg.get('ts')}."
        )

    return msg


def _fetch_slack_thread_reply(
    channel_id: str,
    thread_ts: str,
    reply_ts: str,
    *,
    token: str | None = None,
) -> dict:
    """Fetch a specific reply within a Slack thread.

    Uses `conversations.replies` with the thread timestamp and then
    finds the specific reply by its timestamp.

    Args:
        channel_id: Slack channel ID.
        thread_ts: Parent thread timestamp.
        reply_ts: Timestamp of the specific reply to fetch.
        token: Slack bot token. Resolved from env if not provided.

    Returns:
        The reply message dict from the Slack API.

    Raises:
        SlackAPIError: If the API call fails or reply is not found.
    """
    if token is None:
        token = _resolve_slack_bot_token()

    response = requests.get(
        "https://slack.com/api/conversations.replies",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        params={
            "channel": channel_id,
            "ts": thread_ts,
            "oldest": reply_ts,
            "latest": reply_ts,
            "inclusive": "true",
            "limit": "2",
        },
        timeout=15,
    )
    if not response.ok:
        raise SlackAPIError(
            f"Slack API HTTP error: {response.status_code} {response.text[:200]}"
        )
    data = response.json()

    if not data.get("ok"):
        raise SlackAPIError(
            f"Slack API error fetching thread reply in {channel_id} "
            f"(thread_ts={thread_ts}, reply_ts={reply_ts}): "
            f"{data.get('error', 'unknown')}"
        )

    # Find the exact reply in the response
    for msg in data.get("messages", []):
        if msg.get("ts") == reply_ts:
            return msg

    raise SlackAPIError(
        f"Reply not found at ts={reply_ts} in thread {thread_ts} "
        f"of channel {channel_id}."
    )


# ---------------------------------------------------------------------------
# Approval record extraction
# ---------------------------------------------------------------------------


def _extract_approval_record(message: dict) -> ApprovalRecord:
    """Extract the structured approval record from a Slack message.

    The approval record is embedded as a JSON code block in a `context`
    block element, posted by :func:`_post_approval_thread_reply` in the
    message bus.

    Args:
        message: The Slack message dict.

    Returns:
        :class:`ApprovalRecord` with extracted fields.

    Raises:
        SlackApprovalRecordError: If the message does not contain a valid
            approval record.
    """
    blocks = message.get("blocks", [])

    for block in blocks:
        if block.get("type") != "context":
            continue
        for element in block.get("elements", []):
            text = element.get("text", "")
            # The metadata is wrapped in a Slack code block: ```{json}```
            json_match = re.search(r"```(.+?)```", text, re.DOTALL)
            if not json_match:
                continue
            try:
                record_data = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                continue

            if record_data.get(_FIELD_TYPE) != _APPROVAL_RECORD_TYPE:
                continue

            action = record_data.get(_FIELD_ACTION, "")
            user_id = record_data.get(_FIELD_USER_ID, "")
            user_name = record_data.get(_FIELD_USER_NAME, "")
            timestamp = record_data.get(_FIELD_TIMESTAMP, "")

            if not user_id:
                raise SlackApprovalRecordError(
                    f"Approval record is missing '{_FIELD_USER_ID}' field."
                )
            if action not in _VALID_ACTIONS:
                raise SlackApprovalRecordError(
                    f"Invalid approval action: '{action}'. "
                    f"Expected one of {_VALID_ACTIONS}."
                )

            return ApprovalRecord(
                action=action,
                user_id=user_id,
                user_name=user_name,
                timestamp=timestamp,
                secret_alias=record_data.get(_FIELD_SECRET_ALIAS),
                session_id=record_data.get(_FIELD_SESSION_ID),
                request_id=record_data.get(_FIELD_REQUEST_ID),
            )

    raise SlackApprovalRecordError(
        "Message does not contain a valid approval record. "
        "Expected a context block with a JSON code block containing "
        f"type='{_APPROVAL_RECORD_TYPE}'."
    )


def _validate_bot_authorship(message: dict) -> None:
    """Validate that a Slack message was posted by a bot (not a human).

    The approval record messages are posted by the message-bus bot. We
    verify `bot_id` is present and `subtype` is `bot_message` to
    ensure the record was not forged by a regular user.

    Args:
        message: The Slack message dict.

    Raises:
        SlackApprovalRecordError: If the message was not posted by a bot.
    """
    # Slack bot messages have a bot_id field or subtype "bot_message"
    has_bot_id = bool(message.get("bot_id"))
    is_bot_subtype = message.get("subtype") == "bot_message"

    if not has_bot_id and not is_bot_subtype:
        raise SlackApprovalRecordError(
            "The approval record message was not posted by a bot. "
            "Only bot-authored approval records are trusted."
        )


# ---------------------------------------------------------------------------
# Email resolution
# ---------------------------------------------------------------------------


def _resolve_slack_user_email(user_id: str) -> str:
    """Resolve a Slack user ID to an `@airbyte.io` email address.

    Resolution strategy:

    1. **Internal team roster** (preferred) — fast, cached, no extra API
       call needed. Searches by Slack user ID.
    2. **Slack `users.info` API** — fallback if the roster is unavailable
       or doesn't contain the user.

    Args:
        user_id: Slack user ID (e.g. `U05AKF1BCC9`).

    Returns:
        The user's `@airbyte.io` email address.

    Raises:
        SlackUserEmailNotFoundError: If the email cannot be resolved or
            is not an `@airbyte.io` address.
    """
    # Strategy 1: Internal team roster
    email = _resolve_via_roster(user_id)
    if email:
        return email

    # Strategy 2: Slack users.info API
    email = _resolve_via_slack_api(user_id)
    if email:
        return email

    raise SlackUserEmailNotFoundError(
        f"Could not resolve Slack user '{user_id}' to an {EXPECTED_ADMIN_EMAIL_DOMAIN} "
        f"email address. The user may not be in the internal team roster and may not "
        f"have an {EXPECTED_ADMIN_EMAIL_DOMAIN} email in their Slack profile."
    )


def _resolve_via_roster(user_id: str) -> str | None:
    """Try to resolve a Slack user ID via the internal team roster.

    Args:
        user_id: Slack user ID.

    Returns:
        The `@airbyte.io` email if found, else None.
    """
    try:
        roster = fetch_roster()
        matches = search_roster(roster, user_id)
        for person in matches:
            if person.get("slack_id") == user_id:
                email = person.get("slack_email")
                if isinstance(email, str) and email.endswith(
                    EXPECTED_ADMIN_EMAIL_DOMAIN
                ):
                    return email
    except Exception:
        logger.debug(
            "Roster lookup failed for Slack user %s, will try Slack API",
            user_id,
            exc_info=True,
        )
    return None


def _resolve_via_slack_api(user_id: str) -> str | None:
    """Try to resolve a Slack user ID via the Slack `users.info` API.

    Args:
        user_id: Slack user ID.

    Returns:
        The `@airbyte.io` email if found, else None.
    """
    try:
        token = _resolve_slack_bot_token()
        response = requests.get(
            "https://slack.com/api/users.info",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            params={"user": user_id},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            logger.debug(
                "Slack users.info failed for %s: %s",
                user_id,
                data.get("error", "unknown"),
            )
            return None

        profile = data.get("user", {}).get("profile", {})
        email = profile.get("email", "")
        if email and email.endswith(EXPECTED_ADMIN_EMAIL_DOMAIN):
            return email

        logger.debug(
            "Slack user %s has email '%s' which does not end with %s",
            user_id,
            email,
            EXPECTED_ADMIN_EMAIL_DOMAIN,
        )

    except Exception:
        logger.debug(
            "Slack API lookup failed for user %s",
            user_id,
            exc_info=True,
        )

    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate_slack_approval_record(
    approval_slack_url: str,
    *,
    require_approved: bool = True,
    expected_secret_alias: str | None = None,
    expected_request_id: str | None = None,
    resolve_admin_email: bool = False,
) -> ApprovalRecord:
    """Validate a Slack approval record URL and return the record.

    Parses the URL, fetches the message, validates bot authorship, and
    extracts the structured approval record.

    Args:
        approval_slack_url: Slack message URL pointing to the approval
            thread reply posted by the message bus.
        require_approved: If True (default), raises
            `SlackApprovalRecordError` when the record action is not
            `approved`.
        expected_secret_alias: If provided, validates that the approval
            record's `secret_alias` field matches. Raises
            `SlackApprovalRecordError` on mismatch.
        expected_request_id: If provided, validates that the approval
            record's `request_id` field matches. Raises
            `SlackApprovalRecordError` on mismatch. Used for
            replay-protection.
        resolve_admin_email: If True, resolves the approver's Slack
            user ID to an `@airbyte.io` email and populates
            `ApprovalRecord.admin_email`.

    Returns:
        The validated `ApprovalRecord` (with `admin_email` populated
        when `resolve_admin_email=True`).

    Raises:
        SlackURLParseError: If the URL cannot be parsed.
        SlackAPIError: If Slack API calls fail.
        SlackApprovalRecordError: If the message is not a valid approval
            record, was not authored by the bot, the action is not
            `approved` (when `require_approved`), the secret alias
            does not match (when `expected_secret_alias` is given),
            or the request ID does not match (when
            `expected_request_id` is given).
        SlackUserEmailNotFoundError: If `resolve_admin_email` is True
            and the email cannot be resolved.
    """
    msg_info = _parse_slack_message_url(approval_slack_url)

    if msg_info.thread_ts:
        message = _fetch_slack_thread_reply(
            channel_id=msg_info.channel_id,
            thread_ts=msg_info.thread_ts,
            reply_ts=msg_info.message_ts,
        )
    else:
        message = _fetch_slack_message(
            channel_id=msg_info.channel_id,
            message_ts=msg_info.message_ts,
        )

    _validate_bot_authorship(message)
    record = _extract_approval_record(message)

    if require_approved and record.action != _ACTION_APPROVED:
        raise SlackApprovalRecordError(
            f"Request was not approved. Action: '{record.action}' "
            f"by {record.user_name or record.user_id}."
        )

    if expected_secret_alias and record.secret_alias != expected_secret_alias:
        raise SlackApprovalRecordError(
            f"Secret alias mismatch: approval record is for "
            f"'{record.secret_alias}' but expected '{expected_secret_alias}'."
        )

    if expected_request_id and record.request_id != expected_request_id:
        raise SlackApprovalRecordError(
            f"Request ID mismatch: approval record has request_id "
            f"'{record.request_id}' but expected '{expected_request_id}'. "
            f"This may indicate a replay attack or stale approval."
        )

    if resolve_admin_email:
        email = _resolve_slack_user_email(record.user_id)
        # Return a new frozen dataclass instance with admin_email set
        return ApprovalRecord(
            action=record.action,
            user_id=record.user_id,
            user_name=record.user_name,
            timestamp=record.timestamp,
            secret_alias=record.secret_alias,
            session_id=record.session_id,
            request_id=record.request_id,
            admin_email=email,
        )

    return record
