# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Common utilities for interacting with the Devin v3 API.

Provides reusable helpers for session ID extraction, URL resolution, and
message delivery.  These are consumed by CLI commands, MCP tools, and
workflow scripts that need to communicate with Devin sessions.

All API calls target the org-scoped v3 REST API and require a service-user
token with the appropriate RBAC permissions (e.g. `ManageOrgSessions` for
message delivery).

Environment variables:
    `DEVIN_AI_ADMIN_SERVICE_TOKEN` or `DEVIN_API_KEY` — Bearer token
    for the Devin v3 API. Must be a service-user token, not a personal
    user API key.

    `DEVIN_ORG_ID` or `DEVIN_AI_ORG_ID` — Organization ID (e.g.
    `org_abc123`). Required for all org-scoped v3 endpoints.
"""

from __future__ import annotations

import logging
import os
import re

import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEVIN_API_BASE = "https://api.devin.ai"
"""Base URL for the Devin REST API."""

DEVIN_SESSION_URL_PREFIX = "https://app.devin.ai/sessions/"
"""URL prefix for Devin session deep-links."""

_SESSION_ID_PATTERN = re.compile(r"[0-9a-fA-F]{32}")
"""Matches a 32-character lowercase/uppercase hex session ID."""

_TOKEN_ENV_VARS = ("DEVIN_AI_ADMIN_SERVICE_TOKEN", "DEVIN_API_KEY")
"""Environment variables checked (in order) for the Devin v3 bearer token.

Both names are accepted so existing callers keep working. The value must be
a service-user token with the RBAC permissions required by the endpoint.
"""

_ORG_ID_ENV_VARS = ("DEVIN_ORG_ID", "DEVIN_AI_ORG_ID")
"""Environment variables checked (in order) for the Devin organization ID."""

_DEVIN_ID_PREFIX = "devin-"
"""Prefix applied to session IDs when addressing the v3 sessions endpoint."""


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------


def extract_session_id(session: str) -> str:
    """Extract a 32-character hex session ID from a URL or raw string.

    Args:
        session: A Devin session URL
            (e.g. `https://app.devin.ai/sessions/abc123...`) or a bare
            32-character hex session ID.

    Returns:
        The 32-character hex session ID.

    Raises:
        ValueError: If no valid session ID is found in the input.
    """
    match = _SESSION_ID_PATTERN.search(session)
    if not match:
        raise ValueError(
            f"No valid session ID found in '{session}'. "
            "Expected a 32-character hex string."
        )
    return match.group(0)


def resolve_session_url(session: str) -> str:
    """Return a full Devin session URL, constructing one if needed.

    If *session* already contains the Devin session URL prefix, it is
    returned as-is.  Otherwise `extract_session_id` is called and
    a URL is constructed.

    Args:
        session: A Devin session URL or bare session ID.

    Returns:
        A full `https://app.devin.ai/sessions/<id>` URL.

    Raises:
        ValueError: If no valid session ID is found (delegated to
            `extract_session_id`).
    """
    if DEVIN_SESSION_URL_PREFIX in session:
        return session
    session_id = extract_session_id(session)
    return f"{DEVIN_SESSION_URL_PREFIX}{session_id}"


# ---------------------------------------------------------------------------
# Token resolution
# ---------------------------------------------------------------------------


def resolve_devin_api_token() -> str:
    """Resolve the Devin v3 service-user bearer token from the environment.

    Checks `DEVIN_AI_ADMIN_SERVICE_TOKEN` and `DEVIN_API_KEY` in
    order and returns the first non-empty value.

    Raises:
        RuntimeError: If no token is found in any of the expected
            environment variables.
    """
    for var in _TOKEN_ENV_VARS:
        token = os.environ.get(var)
        if token:
            return token
    raise RuntimeError(
        "No Devin API token found. Set one of: " + ", ".join(_TOKEN_ENV_VARS)
    )


def resolve_devin_org_id() -> str:
    """Resolve the Devin organization ID from the environment.

    Checks `DEVIN_ORG_ID` and `DEVIN_AI_ORG_ID` in order and returns
    the first non-empty value.

    Raises:
        RuntimeError: If no organization ID is found in any of the
            expected environment variables.
    """
    for var in _ORG_ID_ENV_VARS:
        value = os.environ.get(var)
        if value:
            return value
    raise RuntimeError(
        "No Devin organization ID found. Set one of: " + ", ".join(_ORG_ID_ENV_VARS)
    )


# ---------------------------------------------------------------------------
# API operations
# ---------------------------------------------------------------------------


def send_session_message(session_id: str, message: str) -> None:
    """Send a message to a Devin session via the v3 API.

    Calls `POST /v3/organizations/{org_id}/sessions/{devin_id}/messages`,
    which requires a service-user token with the `ManageOrgSessions`
    permission scoped to the target organization.

    Both the bearer token and organization ID are resolved from the
    environment (`DEVIN_AI_ADMIN_SERVICE_TOKEN` / `DEVIN_API_KEY` and
    `DEVIN_ORG_ID` / `DEVIN_AI_ORG_ID`, respectively).

    Args:
        session_id: Session ID in either bare 32-character hex form
            (e.g. `abc123...`) or prefixed v3 form (e.g. `devin-abc123...`).
            The `devin-` prefix is applied automatically when missing.
        message: The message body to deliver.

    Raises:
        RuntimeError: If the token or organization ID cannot be resolved.
        requests.RequestException: If the API call fails.
    """
    token = resolve_devin_api_token()
    org_id = resolve_devin_org_id()
    devin_id = (
        session_id
        if session_id.startswith(_DEVIN_ID_PREFIX)
        else f"{_DEVIN_ID_PREFIX}{session_id}"
    )

    url = f"{DEVIN_API_BASE}/v3/organizations/{org_id}/sessions/{devin_id}/messages"
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"message": message},
        timeout=30,
    )
    response.raise_for_status()
