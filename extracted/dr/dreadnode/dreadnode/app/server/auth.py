"""Bearer token authentication middleware for the agent runtime server.

Gates ``/api/*`` behind the sandbox's bearer credential. The provisioned
environment credential is the normal source; ``DREADNODE_RUNTIME_TOKEN_FILE``
is a rollback-only bridge that lets the N-1 platform rotate that credential
after an on-prem downgrade.
"""

import typing as t

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from dreadnode.app.server.runtime_credentials import get_credential_source

if t.TYPE_CHECKING:
    from starlette.requests import Request

# Paths that never require authentication
# Readiness sits alongside liveness: the platform polls it before it holds a
# runtime credential, so gating it on auth would make it unusable.
_PUBLIC_PATHS = frozenset({"/api/health", "/api/ready"})
_VALIDATED_BEARER_STATE_ATTR = "_dreadnode_runtime_validated_bearer"


def bearer_token(auth_header: str | None) -> str | None:
    """Extract the bearer credential from an ``Authorization`` header, if present."""
    header = auth_header or ""
    if not header.startswith("Bearer "):
        return None
    return header[7:] or None


def validated_runtime_bearer(request: "Request") -> str | None:
    """Return the bearer validated by this middleware for ``request``."""
    value = getattr(request.state, _VALIDATED_BEARER_STATE_ATTR, None)
    return value if isinstance(value, str) else None


def sandbox_auth_error(path: str, auth_header: str | None) -> str | None:
    """Return an auth error message for a protected runtime path, if any."""
    if path in _PUBLIC_PATHS or not path.startswith("/api/"):
        return None

    source = get_credential_source()
    if not source.enabled():
        return None

    provided_token = bearer_token(auth_header)
    if provided_token is None:
        return "Authorization header with Bearer token required"

    if not source.is_active(provided_token):
        return "Invalid authorization token"

    return None


def sandbox_ws_auth(
    auth_header: str | None,
    ticket: str | None,
    consume_ticket: t.Callable[[str], str | None] | None,
) -> tuple[str | None, str | None]:
    """Authenticate a websocket handshake. Returns ``(error, authenticated_token)``.

    Reports the credential that authenticated so the connection registry can
    close sockets bound to it if N-1 rotates it after a platform rollback.
    """
    source = get_credential_source()
    if not source.enabled():
        return None, None  # auth disabled (local/in-process mode)

    presented = bearer_token(auth_header)
    if presented is not None and source.is_active(presented):
        return None, presented

    # RT-AUTH-009: browsers cannot set an Authorization header on the
    # handshake, so they redeem a single-use ticket instead. The ticket carries
    # the credential that minted it, which must still be the live one.
    if ticket and consume_ticket is not None:
        minted_with = consume_ticket(ticket)
        if minted_with is not None and source.is_active(minted_with):
            return None, minted_with

    if presented is None and not ticket:
        return "Authorization header with Bearer token required", None
    return "Invalid or retired authorization token", None


class SandboxAuthMiddleware(BaseHTTPMiddleware):
    """Validate the Bearer token against the runtime's credential.

    When a runtime token is configured, all ``/api/*`` requests except
    ``/api/health`` must include a matching ``Authorization: Bearer <token>``
    header. When none is configured, requests pass through (local/in-process
    mode).
    """

    async def dispatch(
        self,
        request: "Request",
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.method == "OPTIONS":
            return await call_next(request)

        error = sandbox_auth_error(
            request.url.path,
            request.headers.get("authorization"),
        )
        if error is not None:
            return JSONResponse({"detail": error}, status_code=401)

        if request.url.path.startswith("/api/") and request.url.path not in _PUBLIC_PATHS:
            setattr(
                request.state,
                _VALIDATED_BEARER_STATE_ATTR,
                bearer_token(request.headers.get("authorization")),
            )

        return await call_next(request)
