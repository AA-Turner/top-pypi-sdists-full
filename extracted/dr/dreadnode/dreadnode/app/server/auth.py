"""Bearer token authentication middleware for the local agent runtime server.

Gates ``/api/*`` behind a shared Bearer token when ``DREADNODE_RUNTIME_TOKEN``
(legacy: ``SANDBOX_AUTH_TOKEN``) is set. Applies anywhere the runtime is hosted
— E2B sandboxes, Docker containers, local serve with explicit auth — not
sandbox-specific despite the legacy var name.
"""

from __future__ import annotations

import secrets
import typing as t

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from dreadnode.app.env import read_env_with_deprecation

if t.TYPE_CHECKING:
    from starlette.requests import Request

# Paths that never require authentication
_PUBLIC_PATHS = frozenset({"/api/health"})


def sandbox_auth_error(path: str, auth_header: str | None) -> str | None:
    """Return an auth error message for a protected runtime path, if any."""
    token = read_env_with_deprecation("DREADNODE_RUNTIME_TOKEN", "SANDBOX_AUTH_TOKEN")
    if token is None:
        return None

    if path in _PUBLIC_PATHS or not path.startswith("/api/"):
        return None

    normalized_header = auth_header or ""
    if not normalized_header.startswith("Bearer "):
        return "Authorization header with Bearer token required"

    provided_token = normalized_header[7:]
    if not secrets.compare_digest(provided_token, token):
        return "Invalid authorization token"

    return None


class SandboxAuthMiddleware(BaseHTTPMiddleware):
    """Validate Bearer token against the runtime auth env var.

    When ``DREADNODE_RUNTIME_TOKEN`` (or legacy ``SANDBOX_AUTH_TOKEN``) is set,
    all ``/api/*`` requests except ``/api/health`` must include a matching
    ``Authorization: Bearer <token>`` header. When unset, requests pass
    through (local/in-process mode).
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
