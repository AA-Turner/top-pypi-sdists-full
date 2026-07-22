# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Zendesk webhook event handler.

Processes incoming Zendesk webhook payloads for new/updated tickets,
triggers the Devin `!zendesk_triage` playbook to produce a structured
triage assessment, and injects the ticket data into the Devin session.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import time
from datetime import datetime
from typing import Any

import requests
from pydantic import BaseModel, Field

from agent_message_bus.devin_client import _get_devin_api_key, _get_devin_org_id

logger = logging.getLogger(__name__)

DEVIN_API_BASE = "https://api.devin.ai/v3"

# Zendesk triage playbook id (the `!zendesk_triage` playbook in the Devin org).
# The v3 sessions API takes a `playbook_id`, not the v1 `playbook_name`.
ZENDESK_TRIAGE_PLAYBOOK_ID = "playbook-cfdfef6b17c44baca369ae48c8593bc9"

# Tags applied to every Devin session created by this handler, so that
# zendesk-triage sessions are easily discoverable in the Devin UI.
SESSION_TAGS = ["zendesk-triage"]

# Reject Zendesk webhook requests older than 5 minutes (replay protection,
# mirrors _SLACK_TIMESTAMP_MAX_AGE_SECONDS in slack_handler.py)
_ZENDESK_TIMESTAMP_MAX_AGE_SECONDS = 300


class TicketData(BaseModel):
    """Extracted ticket information from a Zendesk webhook payload."""

    ticket_id: str = Field(description="Zendesk ticket ID")
    subject: str = Field(default="", description="Ticket subject line")
    comments: list[str] = Field(default_factory=list, description="Ticket comment texts")


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
    ticket_id: str = Field(default="", description="Zendesk ticket ID")
    subject: str = Field(default="", description="Ticket subject (truncated)")
    session_id: str = Field(default="", description="Devin session ID if created")
    session_url: str = Field(default="", description="Devin session URL if created")
    error: str | None = Field(default=None, description="Error message if failed")


def verify_zendesk_signature(
    payload_body: bytes,
    signature_header: str,
    timestamp_header: str,
    signing_secret: str,
) -> bool:
    """Verify the Zendesk webhook signature.

    Zendesk signs webhooks using HMAC-SHA256 over the concatenation of
    the timestamp and the raw body. The signature is Base64-encoded and
    sent in the `X-Zendesk-Webhook-Signature` header.

    Args:
        payload_body: Raw request body bytes.
        signature_header: Value of X-Zendesk-Webhook-Signature header.
        timestamp_header: Value of X-Zendesk-Webhook-Signature-Timestamp header.
        signing_secret: The webhook signing secret from Zendesk.

    Returns:
        True if the signature is valid.
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
    expected_signature = base64.b64encode(
        hmac.new(
            signing_secret.encode("utf-8"),
            signed_content,
            hashlib.sha256,
        ).digest()
    ).decode("utf-8")

    return hmac.compare_digest(expected_signature, signature_header)


def extract_ticket_data(payload: dict[str, Any]) -> TicketData | None:
    """Extract ticket information from a Zendesk webhook payload.

    Zendesk webhook payloads can vary based on the trigger configuration.
    This function handles the common formats.

    Args:
        payload: The parsed JSON webhook payload from Zendesk.

    Returns:
        A TicketData instance, or None if the payload cannot be parsed.
    """
    # Direct ticket payload format (Zendesk trigger webhook)
    ticket_id = payload.get("ticket_id") or payload.get("id")
    subject = payload.get("subject") or payload.get("title", "")
    comments = payload.get("comments", [])
    description = payload.get("description", "")

    # Nested ticket format: {"ticket": {...}}
    ticket = payload.get("ticket")
    if isinstance(ticket, dict):
        ticket_id = ticket_id or ticket.get("id")
        subject = subject or ticket.get("subject") or ticket.get("title", "")
        comments = comments or ticket.get("comments", [])
        description = description or ticket.get("description", "")

    if not ticket_id:
        return None

    # Normalize comments to a list of strings
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

    # If no comments but we have a description, use it as the first comment
    if not comment_texts and description:
        comment_texts.append(description)

    return TicketData(
        ticket_id=str(ticket_id),
        subject=subject,
        comments=comment_texts,
    )


def format_playbook_prompt(ticket_data: TicketData) -> str:
    """Format the ticket data into a prompt for the Devin triage playbook.

    Args:
        ticket_data: TicketData with ticket_id, subject, and comments.

    Returns:
        Formatted prompt string.
    """
    parts = [
        f"Zendesk Ticket ID: {ticket_data.ticket_id}",
        f"Ticket Subject: {ticket_data.subject}",
        "",
        "Ticket Comments:",
    ]

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


def trigger_devin_playbook(prompt: str) -> DevinSessionResult:
    """Trigger a new Devin session with the zendesk_triage playbook.

    Creates a new Devin session via the Devin v3 sessions API and sends
    the ticket data as the initial prompt. The `zendesk_triage` playbook
    id is specified so Devin automatically loads the triage instructions.

    Args:
        prompt: The formatted ticket data prompt.

    Returns:
        A DevinSessionResult with session details or error information.
    """
    try:
        api_key = _get_devin_api_key()
        org_id = _get_devin_org_id()
    except ValueError:
        logger.exception("Devin API configuration missing for Zendesk triage")
        return DevinSessionResult(
            status="error",
            error="Devin API is not configured",
        )

    try:
        response = requests.post(
            f"{DEVIN_API_BASE}/organizations/{org_id}/sessions",
            json={
                "prompt": prompt,
                "playbook_id": ZENDESK_TRIAGE_PLAYBOOK_ID,
                "tags": SESSION_TAGS,
            },
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
    except requests.RequestException:
        logger.exception("Failed to create Devin session for Zendesk triage")
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
            "Created Devin session %s for Zendesk triage",
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

    Extracts ticket data from the payload, formats it as a triage
    prompt, and triggers a new Devin session with the zendesk_triage
    playbook.

    Args:
        payload: The parsed JSON webhook payload from Zendesk.

    Returns:
        ZendeskWebhookResult with processing results.
    """
    ticket_data = extract_ticket_data(payload)
    if not ticket_data:
        return ZendeskWebhookResult(status="skipped", reason="no_ticket_data")

    logger.info(
        "Processing Zendesk ticket %s: %s",
        ticket_data.ticket_id,
        ticket_data.subject[:100] if ticket_data.subject else "(no subject)",
    )

    prompt = format_playbook_prompt(ticket_data)
    result = trigger_devin_playbook(prompt)

    return ZendeskWebhookResult(
        status=result.status,
        ticket_id=ticket_data.ticket_id,
        subject=ticket_data.subject[:100] if ticket_data.subject else "",
        session_id=result.session_id,
        session_url=result.session_url,
        error=result.error,
    )
