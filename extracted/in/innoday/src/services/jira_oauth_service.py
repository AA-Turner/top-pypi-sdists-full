"""
Jira OAuth 2.0 (3LO) service.

GitHub issue #296: Atlassian's edge rejects Basic Auth (email:api_token)
specifically for requests originating from this app's hosting platform
(Railway's shared egress IP range), returning 401 with
`WWW-Authenticate: OAuth`. Confirmed live this is not a bad token or a
permissions problem -- it's network-reputation-based enforcement on
Atlassian's side. A static outbound IP did not resolve it either. The
durable fix is OAuth 2.0 (3LO), Atlassian's supported auth path.

This module owns:
- Building the Atlassian authorize URL + a signed, board-scoped CSRF
  `state` parameter (verified on callback).
- Exchanging an authorization code for tokens.
- Resolving `cloud_id` via the accessible-resources endpoint (matched by
  the board's `board_url`), once at connect-time.
- `ensure_fresh_jira_token`: the token-refresh helper every OAuth-mode
  Jira call routes through. Atlassian **rotates** refresh tokens on every
  use -- the old one is invalidated immediately -- so a refresh must
  always persist the new refresh_token, never just the access_token.

No real Atlassian OAuth app exists yet (registration requires a human
with Jira admin access at developer.atlassian.com) -- BOARD_OAUTH_CLIENT_ID
and BOARD_OAUTH_CLIENT_SECRET are read from the environment as placeholders
until one exists. All Atlassian HTTP calls here are unit-tested with
mocked httpx, never exercised live.

Dual-mode: existing Basic Auth board_credentials rows
({"email": ..., "api_token": ...}, no `auth_type` key) are untouched by
this module. Only boards whose stored payload has
`auth_type == "oauth2"` are handled here -- see
src.services.board_credential_service for the payload shape.
"""

import base64
import hashlib
import hmac
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode, urlparse

import httpx
from sqlmodel import Session

from src.domain.board import BoardRegistration, BoardType
from src.services.board_credential_service import (
    get_board_credential_payload,
    set_board_credential,
)
from src.utils.time_windows import parse_iso_utc

logger = logging.getLogger(__name__)

AUTHORIZE_URL = "https://auth.atlassian.com/authorize"
TOKEN_URL = "https://auth.atlassian.com/oauth/token"
ACCESSIBLE_RESOURCES_URL = "https://api.atlassian.com/oauth/token/accessible-resources"

# Atlassian access tokens are typically ~1hr-lived; refresh proactively
# once fewer than this many seconds remain, rather than waiting for
# outright expiry, so an in-flight Jira call doesn't race against the
# token going stale mid-request.
REFRESH_SAFETY_MARGIN_SECONDS = 5 * 60

# Atlassian's app console offers two scope models: "classic" (bundled
# scopes like read:jira-work) and "granular" (per-entity, e.g.
# read:issue:jira). This app was registered on the granular model, which
# has no read:jira-work/write:jira-work to select -- these are the
# granular equivalents covering exactly the operations this integration
# performs today: board config + board issues (board-scope), issue
# create/read/update + transitions (issue), issue metadata (fields/schema
# needed to interpret e.g. fixVersions correctly), comments, and project
# read access. Deliberately minimal, per this repo's own "Aggressive
# Simplification" principle -- add a scope only when a feature actually
# needs it, not speculatively; a briefly-tried 18-scope superset (covering
# issue links, project roles, work-item-info, etc. that nothing in this
# codebase calls) was reverted back to this list.
#
# read:project:jira is NOT optional despite the operations list above not
# mentioning "projects" directly -- confirmed via a live 401 "Unauthorized;
# scope does not match" on GET /rest/agile/1.0/board/{id}/configuration
# (and even the baseline /rest/api/3/myself), reproduced with a token that
# otherwise had every other requested scope correctly granted. Per
# Atlassian's own community-reported bug with the identical symptom
# (community.developer.atlassian.com, "[Fixed] Jira Agile 'Get All Boards'
# REST API failing"), board endpoints require read:project:jira alongside
# read:board-scope:jira-software -- undocumented up front in Atlassian's
# own API reference, only discoverable by hitting the API directly.
JIRA_OAUTH_SCOPES = (
    "read:board-scope:jira-software "
    "write:board-scope:jira-software "
    "read:issue:jira "
    "write:issue:jira "
    "read:issue-meta:jira "
    "read:comment:jira "
    "write:comment:jira "
    "read:project:jira "
    "offline_access"
)


class JiraOAuthError(Exception):
    """Raised for any Jira OAuth 2.0 (3LO) flow failure -- code exchange,
    refresh, or cloud_id resolution. Callers must never fall back to a
    stale/invalid token when this is raised."""


# Vendor suffix keeps each board OAuth app's credentials independently
# configurable -- e.g. a future Notion OAuth app would use
# BOARD_OAUTH_CLIENT_ID_NOTION alongside this without any collision or
# code change to this module's naming scheme. Only Jira needs an OAuth
# app today (GitHub issue #296); the suffix exists so that stays true if
# a second board vendor ever needs one.
_VENDOR_SUFFIX = "JIRA"


def _client_id() -> str:
    key = f"BOARD_OAUTH_CLIENT_ID_{_VENDOR_SUFFIX}"
    value = os.getenv(key)
    if not value:
        raise JiraOAuthError(f"{key} is not configured")
    return value


def _client_secret() -> str:
    key = f"BOARD_OAUTH_CLIENT_SECRET_{_VENDOR_SUFFIX}"
    value = os.getenv(key)
    if not value:
        raise JiraOAuthError(f"{key} is not configured")
    return value


def _redirect_uri() -> str:
    key = f"BOARD_OAUTH_REDIRECT_URI_{_VENDOR_SUFFIX}"
    value = os.getenv(key)
    if not value:
        raise JiraOAuthError(f"{key} is not configured")
    return value


def _state_secret() -> bytes:
    """Secret used to sign the CSRF `state` param. Falls back to this
    vendor's OAuth client secret so no extra env var is strictly
    required, but a dedicated BOARD_OAUTH_STATE_SECRET_JIRA can be set to
    rotate independently of the Atlassian app credential."""
    state_key = f"BOARD_OAUTH_STATE_SECRET_{_VENDOR_SUFFIX}"
    secret_key = f"BOARD_OAUTH_CLIENT_SECRET_{_VENDOR_SUFFIX}"
    secret = os.getenv(state_key) or os.getenv(secret_key, "")
    if not secret:
        raise JiraOAuthError(f"Neither {state_key} nor {secret_key} is configured")
    return secret.encode("utf-8")


def generate_state(organization_id: str, board_id: str) -> str:
    """
    Build a signed, org+board-scoped CSRF state token: base64url(payload) +
    "." + hex HMAC-SHA256 signature of that payload, where payload is
    "<organization_id>:<board_id>:<random-nonce>". Verified server-side on
    callback via verify_state/parse_and_verify_state -- doesn't require
    storing anything server-side (no session/cache dependency), since the
    signature alone proves the value wasn't tampered with and both IDs are
    embedded directly.

    The fixed Atlassian callback URL (BOARD_OAUTH_REDIRECT_URI_JIRA) has no
    room for path params, so organization_id/board_id must round-trip
    through this token instead of the URL. ":" is a safe delimiter here --
    both IDs are UUIDs (see BoardRegistration/Organization models, which
    use `str(uuid4())`), and UUIDs never contain ":".
    """
    nonce = secrets.token_urlsafe(16)
    raw_payload = f"{organization_id}:{board_id}:{nonce}"
    payload_b64 = base64.urlsafe_b64encode(raw_payload.encode("utf-8")).decode("ascii")
    signature = hmac.new(
        _state_secret(), payload_b64.encode("ascii"), hashlib.sha256
    ).hexdigest()
    return f"{payload_b64}.{signature}"


def _decode_and_verify(state: str) -> Optional[Tuple[str, str, str]]:
    """Shared verification core: checks signature and decodes the payload.
    Returns (organization_id, board_id, nonce) on success, None on any
    malformed/tampered input. Never raises."""
    if not state or "." not in state:
        return None

    payload_b64, _, signature = state.partition(".")
    expected_signature = hmac.new(
        _state_secret(), payload_b64.encode("ascii"), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        return None

    try:
        raw_payload = base64.urlsafe_b64decode(payload_b64.encode("ascii")).decode(
            "utf-8"
        )
    except Exception:
        return None

    parts = raw_payload.split(":", 2)
    if len(parts) != 3:
        return None

    organization_id, board_id, nonce = parts
    return organization_id, board_id, nonce


def verify_state(
    state: str, expected_organization_id: str, expected_board_id: str
) -> bool:
    """Verify a state token was generated by generate_state for the given
    organization_id/board_id and hasn't been tampered with. Returns False
    (never raises) on any malformed input -- the authorize endpoint (which
    already knows both IDs from the URL path) treats any False as a 400
    CSRF rejection."""
    decoded = _decode_and_verify(state)
    if decoded is None:
        return False

    organization_id, board_id, _nonce = decoded
    return organization_id == expected_organization_id and board_id == expected_board_id


def parse_and_verify_state(state: str) -> Optional[Tuple[str, str]]:
    """Verify a state token's signature and, if valid, extract and return
    (organization_id, board_id) from it. Returns None (never raises) on any
    malformed/tampered input.

    Used by the callback endpoint, which -- unlike the authorize endpoint --
    does NOT know organization_id/board_id in advance (the fixed Atlassian
    callback URL carries no path params), so it must recover both IDs from
    the signed state token itself before it can look up the board.
    """
    decoded = _decode_and_verify(state)
    if decoded is None:
        return None

    organization_id, board_id, _nonce = decoded
    return organization_id, board_id


def build_authorize_url(organization_id: str, board_id: str) -> Tuple[str, str]:
    """Build the Atlassian authorize redirect URL for a board, returning
    (url, state). The caller (router) is responsible for redirecting the
    user's browser to `url`; `state` is embedded in the URL already but
    also returned for logging/testing convenience."""
    state = generate_state(organization_id, board_id)
    params = {
        "audience": "api.atlassian.com",
        "client_id": _client_id(),
        "scope": JIRA_OAUTH_SCOPES,
        "redirect_uri": _redirect_uri(),
        "state": state,
        "response_type": "code",
        "prompt": "consent",
    }
    url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    return url, state


async def exchange_code_for_tokens(code: str) -> Dict[str, Any]:
    """POST the authorization_code grant to Atlassian's token endpoint.
    Returns the raw JSON response (access_token, refresh_token,
    expires_in, ...). Raises JiraOAuthError on any non-2xx response."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            TOKEN_URL,
            json={
                "grant_type": "authorization_code",
                "client_id": _client_id(),
                "client_secret": _client_secret(),
                "code": code,
                "redirect_uri": _redirect_uri(),
            },
            headers={"Content-Type": "application/json"},
        )

    if response.status_code != 200:
        logger.error(
            "Jira OAuth code exchange failed: %s %s",
            response.status_code,
            response.text,
        )
        raise JiraOAuthError(
            f"Jira OAuth code exchange failed: HTTP {response.status_code}"
        )

    return response.json()


async def _refresh_tokens(refresh_token: str) -> Dict[str, Any]:
    """POST the refresh_token grant. Raises JiraOAuthError on failure --
    never returns a stale/partial result the caller could mistake for a
    valid refresh."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            TOKEN_URL,
            json={
                "grant_type": "refresh_token",
                "client_id": _client_id(),
                "client_secret": _client_secret(),
                "refresh_token": refresh_token,
            },
            headers={"Content-Type": "application/json"},
        )

    if response.status_code != 200:
        logger.error(
            "Jira OAuth token refresh failed: %s %s",
            response.status_code,
            response.text,
        )
        raise JiraOAuthError(
            f"Jira OAuth token refresh failed: HTTP {response.status_code}"
        )

    return response.json()


def _board_url_host(board_url: str) -> str:
    parsed = urlparse(board_url)
    return parsed.netloc or board_url


async def resolve_cloud_id(access_token: str, board_url: str) -> Tuple[str, str]:
    """
    Resolve the Atlassian `cloud_id` for a board by matching board_url's
    host against the accessible-resources list -- done once at
    connect-time (never re-resolved per API call; the caller persists the
    result via set_board_credential).
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            ACCESSIBLE_RESOURCES_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

    if response.status_code != 200:
        logger.error(
            "Jira accessible-resources lookup failed: %s %s",
            response.status_code,
            response.text,
        )
        raise JiraOAuthError(
            f"Failed to resolve Jira cloud_id: HTTP {response.status_code}"
        )

    resources = response.json()
    target_host = _board_url_host(board_url)

    for resource in resources:
        resource_url = resource.get("url", "")
        if _board_url_host(resource_url) == target_host:
            return resource["id"], resource_url

    raise JiraOAuthError(
        f"No accessible Atlassian resource matched board_url host '{target_host}'"
    )


def _parse_expires_at(expires_at: Optional[str]) -> Optional[datetime]:
    """The stored expiry as an aware datetime, or None if it cannot be read.

    Aware, not naive: the only thing this value does is get compared against an
    aware `now` to decide whether the access token still has life in it.

    **None is a real answer, and the caller must treat it as "expired".** This
    used to be `datetime.fromisoformat(payload["expires_at"])` -- an unguarded
    parse of a stored string, plus a bare index. A credential row written by an
    older version, hand-edited, or truncated therefore raised `ValueError` or
    `KeyError` from inside token refresh, which surfaces as a board sync dying
    rather than as a token that needs renewing.

    Refusing to guess is the safe direction here: assuming a missing expiry
    means "still valid" would send a probably-dead token to Atlassian and turn
    one bad field into a 401 nobody can explain. Treating it as expired costs
    one unnecessary refresh, which is the operation that would have fixed it.
    """
    parsed = parse_iso_utc(expires_at)
    if parsed is None and expires_at:
        logger.warning(
            "Unparseable Jira token expiry %r; treating the token as expired",
            expires_at,
        )
    return parsed


def _compute_expires_at(expires_in_seconds: Any) -> str:
    try:
        seconds = int(expires_in_seconds)
    except (TypeError, ValueError):
        seconds = 3600
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


async def ensure_fresh_jira_token(
    session: Session, board_registration_id: str
) -> Tuple[str, str]:
    """
    Return a valid (access_token, cloud_id) pair for a board's stored
    OAuth credential, refreshing it first if fewer than
    REFRESH_SAFETY_MARGIN_SECONDS remain before expiry.

    Every JiraBoardAdapter OAuth-mode call routes through this before
    hitting the Jira API. Atlassian rotates refresh tokens on every use --
    the old refresh_token is invalidated immediately -- so a refresh here
    always persists BOTH the new access_token and the new refresh_token
    via set_board_credential, never just the access_token.

    Raises JiraOAuthError if:
    - no credential is stored for this board,
    - the stored credential isn't OAuth (auth_type != "oauth2"),
    - the refresh call itself fails (never silently returns a stale
      token in that case).
    """
    payload = get_board_credential_payload(session, board_registration_id)
    if not payload:
        raise JiraOAuthError(
            f"No stored credential found for board {board_registration_id}"
        )

    if payload.get("auth_type") != "oauth2":
        raise JiraOAuthError(
            f"Board {board_registration_id} credential is not OAuth "
            f"(auth_type={payload.get('auth_type', 'basic')!r})"
        )

    access_token = payload["access_token"]
    refresh_token = payload["refresh_token"]
    cloud_id = payload["cloud_id"]
    expires_at = _parse_expires_at(payload.get("expires_at"))

    now = datetime.now(timezone.utc)
    # An unreadable or absent expiry is treated as already expired, so the
    # refresh below runs rather than a raise escaping into the caller's sync.
    seconds_remaining = (
        (expires_at - now).total_seconds() if expires_at is not None else -1.0
    )

    if seconds_remaining > REFRESH_SAFETY_MARGIN_SECONDS:
        return access_token, cloud_id

    logger.info(
        "jira_oauth.refreshing board_id=%s seconds_remaining=%.0f",
        board_registration_id,
        seconds_remaining,
    )
    token_response = await _refresh_tokens(refresh_token)

    new_access_token = token_response["access_token"]
    # Atlassian is documented to always rotate the refresh token, but fall
    # back to the old one defensively if a response is ever missing it,
    # rather than persisting a payload with no refresh_token at all.
    new_refresh_token = token_response.get("refresh_token", refresh_token)
    new_expires_at = _compute_expires_at(token_response.get("expires_in"))

    new_payload = dict(payload)
    new_payload.update(
        {
            "auth_type": "oauth2",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "expires_at": new_expires_at,
            "cloud_id": cloud_id,
        }
    )

    organization_id = _lookup_organization_id(session, board_registration_id)

    set_board_credential(
        session,
        board_registration_id=board_registration_id,
        organization_id=organization_id,
        board_type=BoardType.JIRA,
        payload=new_payload,
    )

    return new_access_token, cloud_id


def _lookup_organization_id(session: Session, board_registration_id: str) -> str:
    """set_board_credential's SQL function requires organization_id as a
    defense-in-depth scoping check even though board_registration_id
    alone is already unique -- look it up from the BoardRegistration
    row rather than trusting a value embedded in the Vault payload."""
    registration = session.get(BoardRegistration, board_registration_id)
    return registration.organization_id if registration else ""
