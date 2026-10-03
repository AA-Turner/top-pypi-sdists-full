# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Zendesk webhook event handler.

Processes incoming Zendesk webhook payloads for new/updated tickets and
triggers a Devin playbook — `!zendesk_triage` for new-ticket triage and
manual triage requests, `!moonbot_resolution` for resolution — injecting
the ticket data into the Devin session.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import os
import time
from collections.abc import Sequence
from datetime import datetime
from enum import StrEnum
from typing import Any

import requests
from pydantic import BaseModel, Field

from agent_message_bus.devin_client import _get_devin_api_key, _get_devin_org_id

logger = logging.getLogger(__name__)

DEVIN_API_BASE = "https://api.devin.ai/v3"

# Zendesk triage playbook id (the `!zendesk_triage` playbook in the Devin org).
# The v3 sessions API takes a `playbook_id`, not the v1 `playbook_name`.
ZENDESK_TRIAGE_PLAYBOOK_ID = "playbook-cfdfef6b17c44baca369ae48c8593bc9"

# MoonBot Resolution playbook id, run when a ticket is marked solved.
ZENDESK_RESOLUTION_PLAYBOOK_ID = "playbook-021d9cba306d43378a2cbefc5c142f58"

# Reject Zendesk webhook requests older than 5 minutes (replay protection,
# mirrors _SLACK_TIMESTAMP_MAX_AGE_SECONDS in slack_handler.py)
_ZENDESK_TIMESTAMP_MAX_AGE_SECONDS = 300


class ZendeskAction(StrEnum):
    """Which Devin playbook a Zendesk webhook should trigger."""

    triage = "triage"
    resolution = "resolution"


# Tags applied to every Devin session created by this handler, keyed by
# action, so that zendesk sessions are easily discoverable in the Devin UI.
SESSION_TAGS: dict[ZendeskAction, list[str]] = {
    ZendeskAction.triage: ["zendesk-triage"],
    ZendeskAction.resolution: ["zendesk-resolution"],
}

# Tickets carrying these tags are never auto-triaged.
TRIAGE_SKIP_TAGS: frozenset[str] = frozenset({"triaged", "outreach"})

_ACTION_PLAYBOOKS: dict[ZendeskAction, str] = {
    ZendeskAction.triage: ZENDESK_TRIAGE_PLAYBOOK_ID,
    ZendeskAction.resolution: ZENDESK_RESOLUTION_PLAYBOOK_ID,
}


class TicketData(BaseModel):
    """Extracted ticket information from a Zendesk webhook payload."""

    ticket_id: str = Field(description="Zendesk ticket ID")
    subject: str = Field(default="", description="Ticket subject line")
    status: str = Field(default="", description="Ticket status")
    action: ZendeskAction = Field(
        default=ZendeskAction.triage,
        description="Which playbook action this webhook should trigger",
    )
    comments: list[str] = Field(default_factory=list, description="Ticket comment texts")
    tags: list[str] = Field(default_factory=list, description="Zendesk ticket tags")


class DevinSessionResult(BaseModel):
    """Result of triggering a Devin session."""

    status: str = Field(description="ok or error")
    session_id: str = Field(default="", description="Devin session ID if created")
    session_url: str = Field(default="", description="Devin session URL if created")
    error: str | None = Field(default=None, description="Error message if failed")


class ZendeskWebhookResult(BaseModel):
    """Result of processing a Zendesk webhook event."""

    status: str = Field(description="Processing status: accepted, skipped, ok, or error")
    reason: str | None = Field(default=None, description="Reason if skipped")
    action: str = Field(default="", description="Playbook action routed (triage or resolution)")
    ticket_id: str = Field(default="", description="Zendesk ticket ID")
    subject: str = Field(default="", description="Ticket subject (truncated)")
    session_id: str = Field(default="", description="Devin session ID if created")
    session_url: str = Field(default="", description="Devin session URL if created")
    error: str | None = Field(default=None, description="Error message if failed")


def verify_zendesk_signature(
    payload_body: bytes,
    signature_header: str,
    timestamp_header: str,
    signing_secrets: Sequence[str],
) -> bool:
    """Verify the Zendesk webhook signature.

    Zendesk signs webhooks using HMAC-SHA256 over the concatenation of
    the timestamp and the raw body. The signature is Base64-encoded and
    sent in the `X-Zendesk-Webhook-Signature` header. Multiple signing
    secrets are supported (one per registered webhook); the signature is
    valid if it matches any of them.

    Args:
        payload_body: Raw request body bytes.
        signature_header: Value of X-Zendesk-Webhook-Signature header.
        timestamp_header: Value of X-Zendesk-Webhook-Signature-Timestamp header.
        signing_secrets: The webhook signing secrets from Zendesk.

    Returns:
        `True` if the signature is valid for any configured secret.
    """
    if not signature_header or not timestamp_header:
        return False

    try:
        ts_dt = datetime.fromisoformat(timestamp_header.replace("Z", "+00:00"))
        age = abs(time.time() - ts_dt.timestamp())
        if age > _ZENDESK_TIMESTAMP_MAX_AGE_SECONDS:
            logger.warning("Zendesk request timestamp too old: %s", timestamp_header)
            return False
    except (ValueError, OSError):
        logger.warning("Could not parse Zendesk timestamp for age check: %s", timestamp_header)
        return False

    signed_content = timestamp_header.encode("utf-8") + payload_body
    for signing_secret in signing_secrets:
        expected_signature = base64.b64encode(
            hmac.new(
                signing_secret.encode("utf-8"),
                signed_content,
                hashlib.sha256,
            ).digest()
        ).decode("utf-8")
        if hmac.compare_digest(expected_signature, signature_header):
            return True

    return False


def _normalize_comments(comments: Any) -> list[str]:
    """Normalize a comments field to a list of strings."""
    comment_texts: list[str] = []
    if isinstance(comments, list):
        for comment in comments:
            if isinstance(comment, str):
                comment_texts.append(comment)
            elif isinstance(comment, dict):
                body = comment.get("body") or comment.get("plain_body") or comment.get("value", "")
                if body:
                    author = comment.get("author", {})
                    author_name = ""
                    if isinstance(author, dict):
                        author_name = author.get("name", "")
                    elif isinstance(author, str):
                        author_name = author
                    if author_name:
                        comment_texts.append(f"[{author_name}]: {body}")
                    else:
                        comment_texts.append(body)
    return comment_texts


def extract_ticket_data(payload: dict[str, Any]) -> TicketData | None:
    """Extract ticket information from a Zendesk webhook payload.

    Handles three payload shapes:

    - Zendesk event-subscription payload (new-ticket webhook), detected by
      a `type` field starting with `zen:event-type:`:
      `{"type": "zen:event-type:ticket.created", "id": "<uuid>",
      "subject": "zen:ticket:19499", "detail": {...}}`. Ticket ID comes from
      the `zen:ticket:` subject prefix when present, else `detail.id`.
      Action is always `triage`.
    - Zendesk trigger webhook posting our documented JSON body:
      `{"action": "...", "ticket_id": "...", "subject": "...", ...}`.
      `action` is case-insensitive, defaults to `triage`, and an unknown
      value returns `None` so the webhook is skipped with reason
      `unknown_action`. Tags may be a list or whitespace-separated string;
      nested `ticket.tags` is used when top-level tags are absent.
    - Nested trigger format: `{"ticket": {...}}` fallback.

    Args:
        payload: The parsed JSON webhook payload from Zendesk.

    Returns:
        A TicketData instance with normalized tags, or `None` if the payload
        cannot be parsed.
    """
    action = ZendeskAction.triage
    ticket_id: Any = None
    subject = ""
    status = ""
    description = ""
    raw_tags: Any = None
    comments: Any = []
    latest_comment = ""

    detail: dict[str, Any] = {}
    top_subject = payload.get("subject")
    if isinstance(payload.get("type"), str) and payload["type"].startswith("zen:event-type:"):
        # Zendesk event-subscription payload (e.g. ticket.created webhook).
        if isinstance(top_subject, str) and top_subject.startswith("zen:ticket:"):
            ticket_id = top_subject.removeprefix("zen:ticket:")
        if isinstance(payload.get("detail"), dict):
            detail = payload["detail"]
        raw_tags = detail.get("tags")
        ticket_id = ticket_id or detail.get("id")
    else:
        # Trigger webhook: resolve the action first — an unknown action
        # means the whole webhook is skipped.
        raw_action = payload.get("action")
        if raw_action is not None:
            try:
                action = ZendeskAction(str(raw_action).strip().lower())
            except ValueError:
                logger.warning("Unknown Zendesk webhook action: %s", raw_action)
                return None

        ticket_id = payload.get("ticket_id") or payload.get("id")
        subject = payload.get("subject") or payload.get("title", "")
        status = str(payload.get("status") or "")
        description = payload.get("description", "")
        raw_tags = payload.get("tags")
        comments = payload.get("comments", [])
        latest_comment = payload.get("latest_comment") or ""

        # Nested ticket format: {"ticket": {...}}
        ticket = payload.get("ticket")
        if isinstance(ticket, dict):
            ticket_id = ticket_id or ticket.get("id")
            subject = subject or ticket.get("subject") or ticket.get("title", "")
            status = status or str(ticket.get("status") or "")
            description = description or ticket.get("description", "")
            comments = comments or ticket.get("comments", [])
            if raw_tags is None:
                raw_tags = ticket.get("tags")

    subject = subject or str(detail.get("subject") or detail.get("title") or "")
    status = status or str(detail.get("status") or "")
    description = description or detail.get("description", "")
    comments = comments or detail.get("comments", [])

    if not ticket_id:
        return None

    comment_texts = _normalize_comments(comments)

    if latest_comment:
        comment_texts.append(latest_comment)

    # If no comments but we have a description, use it as the first comment
    if not comment_texts and description:
        comment_texts.append(description)

    return TicketData(
        ticket_id=str(ticket_id).strip(),
        subject=subject,
        status=status,
        action=action,
        comments=comment_texts,
        tags=_normalize_tags(raw_tags),
    )


def _normalize_tags(tags: Any) -> list[str]:
    """Normalize a Zendesk tag list or whitespace-separated string."""
    if isinstance(tags, str):
        tag_values = tags.split()
    elif isinstance(tags, list) and all(isinstance(tag, str) for tag in tags):
        tag_values = tags
    else:
        return []

    normalized: list[str] = []
    for tag in tag_values:
        value = tag.strip().lower()
        if value:
            normalized.append(value)
    return normalized


def format_playbook_prompt(ticket_data: TicketData) -> str:
    """Format the ticket data into a prompt for the Devin playbook.

    Args:
        ticket_data: TicketData with ticket_id, subject, status, action, and comments.

    Returns:
        Formatted prompt string.
    """
    if ticket_data.action is ZendeskAction.resolution:
        parts = [
            "Run the MoonBot Resolution playbook on this ticket.",
            "",
            f"Ticket ID: {ticket_data.ticket_id}",
            f"Subject: {ticket_data.subject}",
            f"Status: {ticket_data.status}",
        ]
        if ticket_data.comments:
            parts.append("")
            parts.append("Ticket Comments:")
            for i, comment in enumerate(ticket_data.comments, 1):
                parts.append(f"--- Comment {i} ---")
                parts.append(comment)
                parts.append("")
        return "\n".join(parts)

    parts = [
        f"Zendesk Ticket ID: {ticket_data.ticket_id}",
        f"Ticket Subject: {ticket_data.subject}",
    ]
    if ticket_data.status:
        parts.append(f"Ticket Status: {ticket_data.status}")
    parts.extend(
        [
            "",
            "Ticket Comments:",
        ]
    )

    if ticket_data.comments:
        for i, comment in enumerate(ticket_data.comments, 1):
            parts.append(f"--- Comment {i} ---")
            parts.append(comment)
            parts.append("")
    else:
        parts.append("(No comments available)")

    parts.append("")
    parts.append(
        "Please triage this ticket following the zendesk_triage playbook instructions. "
        "Produce the triage JSON and write the results back to the Zendesk ticket."
    )

    return "\n".join(parts)


def _resolution_session_secrets() -> list[dict[str, str | bool]]:
    """Build the Devin `session_secrets` payload for a resolution session.

    The MoonBot Resolution playbook curls the Zendesk API directly for the
    custom-field write-back, so it needs the Zendesk credentials inside the
    Devin session. Triage sessions use the Ops MCP instead and must NOT
    receive these secrets.

    Returns:
        A list of three `session_secrets` entries matching the shape the
        Devin v3 `POST /organizations/{org}/sessions` endpoint accepts, or
        an empty list if any required env var is missing.
    """
    subdomain = os.environ.get("ZENDESK_SUBDOMAIN", "")
    email = os.environ.get("ZENDESK_EMAIL", "")
    token = os.environ.get("ZENDESK_API_TOKEN", "")
    if not (subdomain and email and token):
        logger.warning(
            "Zendesk MoonBot credentials not configured; resolution session "
            "will run without write-back credentials"
        )
        return []
    return [
        {"key": "ZENDESK_SUBDOMAIN", "value": subdomain, "sensitive": False},
        {"key": "ZENDESK_EMAIL", "value": email, "sensitive": False},
        {"key": "ZENDESK_API_TOKEN", "value": token, "sensitive": True},
    ]


def trigger_devin_playbook(
    prompt: str,
    playbook_id: str,
    tags: list[str],
    session_secrets: list[dict[str, str | bool]] | None = None,
) -> DevinSessionResult:
    """Trigger a new Devin session with the given playbook.

    Creates a new Devin session via the Devin v3 sessions API and sends
    the ticket data as the initial prompt. The playbook id is specified
    so Devin automatically loads the playbook instructions.

    Args:
        prompt: The formatted ticket data prompt.
        playbook_id: Devin playbook id to attach to the session.
        tags: Tags to apply to the created session.
        session_secrets: Optional Devin session secrets (e.g. Zendesk
            credentials for the resolution playbook's write-back). Only sent
            when non-empty; never logged.

    Returns:
        A DevinSessionResult with session details or error information.
    """
    try:
        api_key = _get_devin_api_key()
        org_id = _get_devin_org_id()
    except ValueError:
        logger.exception("Devin API configuration missing for Zendesk webhook")
        return DevinSessionResult(
            status="error",
            error="Devin API is not configured",
        )

    try:
        body: dict[str, Any] = {
            "prompt": prompt,
            "playbook_id": playbook_id,
            "tags": tags,
        }
        if session_secrets:
            body["session_secrets"] = session_secrets
        response = requests.post(
            f"{DEVIN_API_BASE}/organizations/{org_id}/sessions",
            json=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
    except requests.RequestException:
        logger.exception("Failed to create Devin session for Zendesk webhook")
        return DevinSessionResult(
            status="error",
            error="Network error contacting Devin API",
        )

    if response.ok:
        try:
            data = response.json()
        except ValueError:
            logger.exception("Devin API returned a non-JSON success response")
            return DevinSessionResult(
                status="error",
                error="Invalid response from Devin API",
            )

        session_id = data.get("session_id", "")
        if not session_id:
            logger.error(
                "Devin API success response missing session_id: %s",
                response.text[:200],
            )
            return DevinSessionResult(
                status="error",
                error="Devin API response missing session_id",
            )

        session_url = data.get("url", f"https://app.devin.ai/sessions/{session_id}")
        logger.info(
            "Created Devin session %s for Zendesk webhook",
            session_id,
        )
        return DevinSessionResult(
            status="ok",
            session_id=session_id,
            session_url=session_url,
        )

    logger.warning(
        "Devin API returned %d when creating session: %s",
        response.status_code,
        response.text[:200],
    )
    return DevinSessionResult(
        status="error",
        error=f"Devin API returned {response.status_code}",
    )


def handle_zendesk_webhook(payload: dict[str, Any]) -> ZendeskWebhookResult:
    """Process a Zendesk webhook event.

    Extracts ticket data and the requested action from the payload,
    formats it as a playbook prompt, and triggers a new Devin session
    with the matching playbook (triage or resolution). Triage tickets tagged
    `triaged` or `outreach` are skipped.

    Args:
        payload: The parsed JSON webhook payload from Zendesk.

    Returns:
        ZendeskWebhookResult with processing results.
    """
    ticket_data = extract_ticket_data(payload)
    if not ticket_data:
        reason = "unknown_action" if _unknown_action(payload) else "no_ticket_data"
        return ZendeskWebhookResult(status="skipped", reason=reason)

    if ticket_data.action is ZendeskAction.triage:
        matched_tags = sorted(set(ticket_data.tags) & TRIAGE_SKIP_TAGS)
        if matched_tags:
            logger.info(
                "Skipping Zendesk triage for ticket %s; matched tags: %s",
                ticket_data.ticket_id,
                ", ".join(matched_tags),
            )
            return ZendeskWebhookResult(
                status="skipped",
                reason="triage_skip_tag",
                action=str(ticket_data.action),
                ticket_id=ticket_data.ticket_id,
            )

    logger.info(
        "Processing Zendesk ticket %s (action=%s): %s",
        ticket_data.ticket_id,
        ticket_data.action,
        ticket_data.subject[:100] if ticket_data.subject else "(no subject)",
    )

    session_secrets = (
        _resolution_session_secrets() if ticket_data.action is ZendeskAction.resolution else []
    )
    prompt = format_playbook_prompt(ticket_data)
    result = trigger_devin_playbook(
        prompt,
        playbook_id=_ACTION_PLAYBOOKS[ticket_data.action],
        tags=SESSION_TAGS[ticket_data.action],
        session_secrets=session_secrets,
    )

    return ZendeskWebhookResult(
        status=result.status,
        action=str(ticket_data.action),
        ticket_id=ticket_data.ticket_id,
        subject=ticket_data.subject[:100] if ticket_data.subject else "",
        session_id=result.session_id,
        session_url=result.session_url,
        error=result.error,
    )


def _unknown_action(payload: dict[str, Any]) -> bool:
    """Return `True` if the payload carries an unrecognized `action` value."""
    raw = payload.get("action")
    if raw is None:
        return False
    try:
        ZendeskAction(str(raw).strip().lower())
    except ValueError:
        return True
    return False
