"""Bearer token authentication middleware for the local agent runtime server.

Gates ``/api/*`` behind a shared Bearer token when a runtime token is configured
(via ``DREADNODE_RUNTIME_TOKEN_FILE``, or ``DREADNODE_RUNTIME_TOKEN`` / legacy
``SANDBOX_AUTH_TOKEN``). Applies anywhere the runtime is hosted — E2B sandboxes,
Docker containers, local serve with explicit auth — not sandbox-specific despite
the legacy var name.

The token itself is resolved through :mod:`dreadnode.app.server.runtime_token`,
which supports rotation of a file-sourced token at runtime (for lossless
reconnect) while falling back to the env var when no file is configured.
"""

from __future__ import annotations

import typing as t

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from dreadnode.app.server.runtime_token import get_token_source

if t.TYPE_CHECKING:
    from starlette.requests import Request

# Paths that never require authentication
_PUBLIC_PATHS = frozenset({"/api/health"})


def bearer_token(auth_header: str | None) -> str | None:
    """Extract the bearer credential from an ``Authorization`` header, if present."""
    header = auth_header or ""
    if not header.startswith("Bearer "):
        return None
    return header[7:] or None


def sandbox_auth_error(path: str, auth_header: str | None) -> str | None:
    """Return an auth error message for a protected runtime path, if any."""
    source = get_token_source()
    if not source.enabled():
        return None

    if path in _PUBLIC_PATHS or not path.startswith("/api/"):
        return None

    provided_token = bearer_token(auth_header)
    if provided_token is None:
        return "Authorization header with Bearer token required"

    if not source.is_valid(provided_token):
        return "Invalid authorization token"

    return None


def sandbox_ws_auth(
    auth_header: str | None,
    ticket: str | None,
    consume_ticket: t.Callable[[str], str | None] | None,
) -> tuple[str | None, str | None]:
    """Authenticate a websocket handshake. Returns ``(error, authenticated_token)``.

    Two things differ from the REST check:

    1. A websocket must present the **current** token, not merely a *valid* one.
       The grace window exists so an in-flight REST call survives a token
       handoff — not so a client whose token was just rotated out can open a
       fresh long-lived socket. That client is precisely the one the rotation
       kicked; letting it reconnect for the rest of the grace window (or on a
       pre-rotation ticket, for the rest of that ticket's TTL) would leave the
       watch-only connection the force-close exists to sever.

    2. It reports *which* credential authenticated. The socket is registered
       under that token, so a later rotation closes exactly the connections that
       belong to the retired credential — rather than whatever token happened to
       be current when the socket was accepted.
    """
    source = get_token_source()
    if not source.enabled():
        return None, None  # auth disabled (local/in-process mode)

    presented = bearer_token(auth_header)
    if presented is not None and source.is_current(presented):
        return None, presented

    # Browsers cannot set an Authorization header on the handshake, so they
    # redeem a single-use ticket instead. The ticket carries the token that
    # minted it; that token must still be current.
    if ticket and consume_ticket is not None:
        minted_with = consume_ticket(ticket)
        if minted_with is not None and source.is_current(minted_with):
            return None, minted_with

    if presented is None and not ticket:
        return "Authorization header with Bearer token required", None
    return "Invalid, expired, or rotated-out authorization token", None


class SandboxAuthMiddleware(BaseHTTPMiddleware):
    """Validate the Bearer token against the configured runtime token.

    When a runtime token is configured (file or env), all ``/api/*`` requests
    except ``/api/health`` must include a matching ``Authorization: Bearer
    <token>`` header. When none is configured, requests pass through
    (local/in-process mode).
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == "OPTIONS":
            return await call_next(request)

        error = sandbox_auth_error(
            request.url.path,
            request.headers.get("authorization"),
        )
        if error is not None:
            return JSONResponse({"detail": error}, status_code=401)

        return await call_next(request)
