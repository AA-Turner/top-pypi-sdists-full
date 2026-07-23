# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Zendesk Support API client utilities.

This module provides read-only HTTP access to the Zendesk Support API for
fetching tickets and their comments. It is used by MCP tools but is not
MCP-specific.

Authentication uses Zendesk API-token Basic auth: the username is
`{email}/token` and the password is the API token, matching the
`zendesk_triage` / `zendesk_resolution` playbooks in `airbytehq/ai-skills`.

Zendesk API docs: https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/
"""

from __future__ import annotations

import os
from typing import Any

import requests

from airbyte_ops_mcp.constants import USER_AGENT

ENV_ZENDESK_SUBDOMAIN = "ZENDESK_SUBDOMAIN"
"""Environment variable holding the Zendesk subdomain (e.g. `airbyte1416`)."""

ENV_ZENDESK_EMAIL = "ZENDESK_EMAIL"
"""Environment variable holding the agent email used for API-token auth."""

ENV_ZENDESK_API_TOKEN = "ZENDESK_API_TOKEN"
"""Environment variable holding the Zendesk API token."""

_REQUEST_TIMEOUT_SECONDS = 30

# Zendesk caps comment pages at 100 records per page.
_COMMENTS_PER_PAGE = 100


class ZendeskAPIError(Exception):
    """Raised when a Zendesk API call fails or credentials are missing."""


class ZendeskCredentials:
    """Resolved Zendesk connection settings and API-token credentials."""

    def __init__(self, subdomain: str, email: str, api_token: str) -> None:
        self.subdomain = subdomain
        self.email = email
        self.api_token = api_token

    @property
    def base_url(self) -> str:
        """Return the Zendesk Support API base URL for this subdomain."""
        return f"https://{self.subdomain}.zendesk.com/api/v2"

    @property
    def auth(self) -> tuple[str, str]:
        """Return the `requests` Basic-auth tuple for API-token auth."""
        return (f"{self.email}/token", self.api_token)


def resolve_zendesk_credentials() -> ZendeskCredentials:
    """Resolve Zendesk credentials from the environment.

    Reads `ZENDESK_SUBDOMAIN`, `ZENDESK_EMAIL`, and `ZENDESK_API_TOKEN`.

    Raises:
        ZendeskAPIError: If any of the three variables is missing or empty.
    """
    subdomain = os.environ.get(ENV_ZENDESK_SUBDOMAIN, "").strip()
    email = os.environ.get(ENV_ZENDESK_EMAIL, "").strip()
    api_token = os.environ.get(ENV_ZENDESK_API_TOKEN, "").strip()

    missing = [
        name
        for name, value in (
            (ENV_ZENDESK_SUBDOMAIN, subdomain),
            (ENV_ZENDESK_EMAIL, email),
            (ENV_ZENDESK_API_TOKEN, api_token),
        )
        if not value
    ]
    if missing:
        raise ZendeskAPIError(
            "Zendesk credentials are not configured. Missing or empty "
            f"environment variable(s): {', '.join(missing)}."
        )

    return ZendeskCredentials(subdomain=subdomain, email=email, api_token=api_token)


def _zendesk_headers() -> dict[str, str]:
    """Build common HTTP headers for Zendesk API requests."""
    return {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }


def _request(
    credentials: ZendeskCredentials,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Issue an authenticated request against the Zendesk API and return JSON.

    Raises:
        ZendeskAPIError: On network errors, non-2xx responses, or invalid JSON.
    """
    url = f"{credentials.base_url}{path}"
    try:
        response = requests.request(
            method,
            url,
            params=params,
            json=json_body,
            auth=credentials.auth,
            headers=_zendesk_headers(),
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise ZendeskAPIError(f"Zendesk request to {path} failed: {exc}") from exc

    if response.status_code == 404:
        raise ZendeskAPIError(f"Zendesk resource not found: {path}")
    if response.status_code in (401, 403):
        raise ZendeskAPIError(
            f"Zendesk authentication failed ({response.status_code}) for {path}. "
            "Check ZENDESK_EMAIL / ZENDESK_API_TOKEN."
        )
    if not 200 <= response.status_code < 300:
        # Do not include the response body: it can contain customer/PII data
        # and this message is surfaced to the MCP caller.
        raise ZendeskAPIError(
            f"Zendesk {method} {path} failed with status {response.status_code}."
        )

    try:
        return response.json()
    except ValueError as exc:
        raise ZendeskAPIError(
            f"Zendesk {method} {path} returned invalid JSON."
        ) from exc


def _get(
    credentials: ZendeskCredentials,
    path: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Issue an authenticated GET against the Zendesk API and return JSON."""
    return _request(credentials, "GET", path, params=params)


def _put(
    credentials: ZendeskCredentials,
    path: str,
    json_body: dict[str, Any],
) -> dict[str, Any]:
    """Issue an authenticated PUT against the Zendesk API and return JSON."""
    return _request(credentials, "PUT", path, json_body=json_body)


def _clean_tags(tags: list[str]) -> list[str]:
    """Return the trimmed, non-empty tags from `tags`, preserving order."""
    return [tag.strip() for tag in tags if tag.strip()]


def get_ticket(
    ticket_id: int | str,
    credentials: ZendeskCredentials | None = None,
) -> dict[str, Any]:
    """Fetch a single Zendesk ticket by ID.

    Returns the raw `ticket` object from the Zendesk API.

    Raises:
        ZendeskAPIError: If credentials are missing or the API call fails.
    """
    credentials = credentials or resolve_zendesk_credentials()
    data = _get(credentials, f"/tickets/{ticket_id}.json")
    ticket = data.get("ticket")
    if not isinstance(ticket, dict):
        raise ZendeskAPIError(
            f"Zendesk ticket {ticket_id} response missing a `ticket` object."
        )
    return ticket


def get_ticket_comments(
    ticket_id: int | str,
    credentials: ZendeskCredentials | None = None,
    *,
    sort_order: str = "asc",
) -> list[dict[str, Any]]:
    """Fetch the comments for a Zendesk ticket, oldest first by default.

    Returns the first page of comments (up to 100). Tickets rarely exceed a
    single page; pagination is intentionally omitted to keep the read simple.

    Raises:
        ZendeskAPIError: If credentials are missing or the API call fails.
    """
    credentials = credentials or resolve_zendesk_credentials()
    data = _get(
        credentials,
        f"/tickets/{ticket_id}/comments.json",
        params={"sort_order": sort_order, "per_page": _COMMENTS_PER_PAGE},
    )
    comments = data.get("comments")
    if not isinstance(comments, list):
        raise ZendeskAPIError(
            f"Zendesk ticket {ticket_id} comments response missing a `comments` list."
        )
    return comments


def add_internal_note(
    ticket_id: int | str,
    html_body: str,
    credentials: ZendeskCredentials | None = None,
) -> dict[str, Any]:
    """Add an internal (private) HTML note to a Zendesk ticket.

    Posts a non-public comment (`public: false`) via `PUT /tickets/{id}.json`,
    so the note is visible only to agents and not to the ticket requester. The
    note body is sent as `html_body`, so callers can use HTML markup (`<br>`,
    `<strong>`, `<a href>`, ...) and Zendesk auto-derives the plain-text
    fallback. The update carries only the comment, so the ticket's tags and
    other fields are left untouched. Returns the raw Zendesk response (which
    includes the updated `ticket` and the `audit` describing the created
    comment event).

    Tags are intentionally not handled here: callers that also need to tag the
    ticket should call `add_ticket_tags` separately.

    Raises:
        ZendeskAPIError: If credentials are missing, the body is empty, or the
            API call fails.
    """
    if not html_body.strip():
        raise ZendeskAPIError("Internal note body must not be empty.")
    credentials = credentials or resolve_zendesk_credentials()
    ticket_payload: dict[str, Any] = {
        "comment": {"html_body": html_body, "public": False}
    }
    return _put(credentials, f"/tickets/{ticket_id}.json", {"ticket": ticket_payload})


def add_ticket_tags(
    ticket_id: int | str,
    tags: list[str],
    credentials: ZendeskCredentials | None = None,
) -> list[str]:
    """Add tags to a Zendesk ticket without dropping existing ones.

    Reads the ticket's current tags, merges in the new tags (deduped,
    order-preserving), and writes the full union back via
    `PUT /tickets/{id}.json`. Returns the ticket's full tag list after the
    update.

    This deliberately does **not** use the `POST /tickets/{id}/tags.json`
    "add tags" endpoint. In accounts that back tags with "tagger" (drop-down)
    custom fields, that endpoint reconciles the field/tag mapping and can drop
    pre-existing tags and clear their tagger custom fields. Writing the full
    tag set via a ticket update keeps the tagger fields in sync, so existing
    classification tags (priority, severity, support plan, ...) are preserved.

    Raises:
        ZendeskAPIError: If credentials are missing, no non-empty tag is
            supplied, or the API call fails.
    """
    cleaned_tags = _clean_tags(tags)
    if not cleaned_tags:
        raise ZendeskAPIError("At least one non-empty tag is required.")
    credentials = credentials or resolve_zendesk_credentials()

    existing_ticket = get_ticket(ticket_id, credentials)
    merged_tags = [
        tag for tag in existing_ticket.get("tags", []) or [] if isinstance(tag, str)
    ]
    for tag in cleaned_tags:
        if tag not in merged_tags:
            merged_tags.append(tag)

    data = _put(
        credentials,
        f"/tickets/{ticket_id}.json",
        {"ticket": {"tags": merged_tags}},
    )
    updated_ticket = data.get("ticket")
    if not isinstance(updated_ticket, dict):
        raise ZendeskAPIError(
            f"Zendesk ticket {ticket_id} update response missing a `ticket` object."
        )
    result_tags = updated_ticket.get("tags")
    if not isinstance(result_tags, list):
        raise ZendeskAPIError(
            f"Zendesk ticket {ticket_id} tags response missing a `tags` list."
        )
    return [tag for tag in result_tags if isinstance(tag, str)]
