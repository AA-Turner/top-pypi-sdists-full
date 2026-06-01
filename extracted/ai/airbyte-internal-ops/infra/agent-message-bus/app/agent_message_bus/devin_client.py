# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Devin API client for injecting messages into sessions."""

from __future__ import annotations

import logging
import os

import requests

from agent_message_bus.url_parser import extract_session_id

logger = logging.getLogger(__name__)

DEVIN_API_BASE = "https://api.devin.ai/v3"


def _get_devin_api_key() -> str:
    """Retrieve the Devin API key from environment.

    Returns:
        The API key string.

    Raises:
        ValueError: If DEVIN_AI_API_KEY is not set.
    """
    key = os.environ.get("DEVIN_AI_API_KEY")
    if not key:
        raise ValueError("DEVIN_AI_API_KEY environment variable is not set")
    return key


def _get_devin_org_id() -> str:
    """Retrieve the Devin organization ID from environment.

    Returns:
        The org ID string.

    Raises:
        ValueError: If DEVIN_ORG_ID is not set.
    """
    org_id = os.environ.get("DEVIN_ORG_ID")
    if not org_id:
        raise ValueError("DEVIN_ORG_ID environment variable is not set")
    return org_id


# Sentinel return values for inject_message().
# Using strings rather than an enum keeps the module lightweight.
INJECT_OK = "ok"
INJECT_SESSION_DEAD = "session_dead"  # 404 — session not found
INJECT_AUTH_ERROR = "auth_error"  # 401/403 — credentials/permissions issue
INJECT_TRANSIENT_ERROR = "transient_error"  # network/timeout/5xx


def inject_message(session_url: str, message: str) -> str:
    """Inject a message into a Devin session.

    Posts a message to the Devin API that will appear in the session's
    conversation as if it were a user message.

    Args:
        session_url: The Devin session URL.
        message: The message text to inject.

    Returns:
        One of the module-level `INJECT_*` constants:
        - `INJECT_OK` - message delivered successfully.
        - `INJECT_SESSION_DEAD` - session not found (404); the caller
          should clean up the subscription.
        - `INJECT_AUTH_ERROR` - credentials or permissions problem
          (401/403); do **not** delete the subscription.
        - `INJECT_TRANSIENT_ERROR` - temporary failure (network,
          timeout, 5xx); do **not** delete the subscription.
    """
    try:
        session_id = extract_session_id(session_url)
    except ValueError:
        logger.error("Cannot inject message: invalid session URL %s", session_url)
        return INJECT_SESSION_DEAD

    api_key = _get_devin_api_key()
    org_id = _get_devin_org_id()
    devin_id = f"devin-{session_id}"
    url = f"{DEVIN_API_BASE}/organizations/{org_id}/sessions/{devin_id}/messages"

    try:
        response = requests.post(
            url,
            json={"message": message},
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        if response.ok:
            logger.info("Injected message into session %s", session_id)
            return INJECT_OK

        logger.warning(
            "Devin API returned %d for session %s: %s",
            response.status_code,
            session_id,
            response.text[:200],
        )

        if response.status_code == 404:
            return INJECT_SESSION_DEAD
        if response.status_code in (401, 403):
            return INJECT_AUTH_ERROR
        return INJECT_TRANSIENT_ERROR

    except requests.RequestException:
        logger.exception("Failed to inject message into session %s", session_id)
        return INJECT_TRANSIENT_ERROR
