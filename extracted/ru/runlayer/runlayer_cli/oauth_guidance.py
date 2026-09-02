"""Actionable guidance for OAuth failures surfaced by ``runlayer run``.

Two failure modes that used to surface as raw, unactionable errors:

1. Dynamic client registration (DCR) rejected by the upstream IdP — e.g. Okta
   answering ``403 {"errorCode":"E0000005","errorSummary":"Invalid session"}``.
   The fix is manual OAuth client configuration in the Runlayer server
   settings, but the raw IdP body never says so.
2. An interactive browser OAuth login that never completes because the IdP
   rejects the localhost callback redirect URI. The user sees an IdP error
   page in the browser, and the CLI just times out (the 30s tools/list
   upstream timeout, or the 5-minute callback wait).

This module is intentionally lightweight (stdlib plus ``regex_safe``; no
``mcp``/``httpx``) so it can be imported anywhere in the CLI without dragging
heavy dependencies.
"""

from __future__ import annotations

import time

from runlayer_cli import regex_safe


# --- Registration (DCR) failure classification ---

# mcp SDK raises OAuthRegistrationError(f"Registration failed: {status} {body}")
_REGISTRATION_ERROR_RE = regex_safe.compile(
    r"Registration failed: (\d{3})\s*(.*)", regex_safe.DOTALL
)

# Redact values of secret-shaped keys in an IdP error body before it reaches
# logs or the console. Registration responses shouldn't contain tokens, but
# never trust an upstream body to be safe to print verbatim.
_SECRET_KEY_RE = regex_safe.compile(
    r"(?i)([\"']?(?:[a-z0-9_-]*(?:token|secret|password|authorization|api[_-]?key))"
    r"[\"']?\s*[:=]\s*)([\"'][^\"']*[\"']|[A-Za-z0-9._~+/=-]+)"
)

_DETAIL_MAX_CHARS = 300


def sanitize_upstream_detail(text: str, max_chars: int = _DETAIL_MAX_CHARS) -> str:
    """Redact secret-shaped values and truncate an upstream error body."""
    sanitized = _SECRET_KEY_RE.sub(r"\1[REDACTED]", text).strip()
    if len(sanitized) > max_chars:
        sanitized = sanitized[:max_chars] + "... [truncated]"
    return sanitized


def registration_rejected_message(status_code: int, detail: str) -> str:
    detail_part = f" Upstream response (for support): {detail}" if detail else ""
    return (
        "The upstream identity provider rejected automatic OAuth client "
        f"registration (dynamic client registration) with HTTP {status_code}. "
        "This usually means the IdP requires OAuth apps to be registered "
        "manually: create an OAuth app in the identity provider, then "
        "configure Manual OAuth (client ID, plus a client secret or public "
        "client) in this server's settings in Runlayer and try again." + detail_part
    )


def registration_failure_status(error_message: str) -> int | None:
    """HTTP status parsed from an mcp ``OAuthRegistrationError`` message.

    ``None`` when the message doesn't carry the SDK's
    ``Registration failed: <status> <body>`` shape. Shared by the guidance
    below and flow telemetry's error classification
    (``error_classification.py``), so the message-shape knowledge lives once.
    """
    match = _REGISTRATION_ERROR_RE.search(error_message)
    if match is None:
        return None
    return int(match.group(1))


def classify_registration_failure(error_message: str) -> str | None:
    """Turn a DCR failure message into actionable guidance.

    Returns the guidance string for HTTP 4xx registration rejections (the
    IdP refusing automatic registration — a configuration problem the user
    must fix via Manual OAuth), or ``None`` for anything else (5xx and
    unrecognized messages stay as-is: likely transient, and the manual-OAuth
    advice would be wrong).
    """
    match = _REGISTRATION_ERROR_RE.search(error_message)
    if match is None:
        return None
    status_code = int(match.group(1))
    if not 400 <= status_code < 500:
        return None
    detail = sanitize_upstream_detail(match.group(2))
    return registration_rejected_message(status_code, detail)


# --- Pending interactive OAuth flow (browser login awaiting callback) ---

# A pending marker older than this is considered stale (self-heals leaked
# state from an aborted flow). Must exceed the 5-minute callback wait in
# ``oauth.OAuth.callback_handler`` so its own timeout still classifies.
_PENDING_MAX_AGE_SECONDS = 600.0

_pending_flow: dict[str, float | int] | None = None


def mark_oauth_flow_started(callback_port: int) -> None:
    """Record that a browser OAuth login is waiting for its localhost callback.

    Called when the flow hands off to the browser; cleared by
    ``mark_oauth_flow_finished`` once the callback delivers an auth code.
    Deliberately NOT cleared on timeout/cancellation: a timed-out flow is
    exactly the state the guidance describes, and the staleness window
    self-heals leaked markers.
    """
    global _pending_flow
    _pending_flow = {"port": callback_port, "started_at": time.monotonic()}


def mark_oauth_flow_finished() -> None:
    global _pending_flow
    _pending_flow = None


def pending_oauth_flow_port() -> int | None:
    """Port of a currently-pending (non-stale) browser OAuth login, or None."""
    if _pending_flow is None:
        return None
    age = time.monotonic() - float(_pending_flow["started_at"])
    if age > _PENDING_MAX_AGE_SECONDS:
        return None
    return int(_pending_flow["port"])


def oauth_pending_timeout_message(callback_port: int) -> str:
    callback_url = f"http://localhost:{callback_port}/callback"
    return (
        "Timed out while an OAuth browser login was still waiting for its "
        f"callback on {callback_url}. Complete the login in the browser. If "
        "the browser shows an error page instead of a Runlayer 'login "
        "complete' page, the identity provider rejected the redirect URI: "
        f"{callback_url} must be registered as a redirect URI for this OAuth "
        "client in the IdP. Use --oauth-callback-port (or "
        "RUNLAYER_OAUTH_CALLBACK_PORT) to pin the port to one the IdP allows."
    )
