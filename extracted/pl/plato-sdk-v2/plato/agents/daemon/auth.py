"""Bearer-token auth middleware for the daemon."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from aiohttp import web

from plato.agents.daemon.state import DaemonContext
from plato.rpc.errors import HTTP_STATUS_BY_CODE, RpcError
from plato.rpc.protocol import API_PREFIX, HEADER_REQUEST_ID

_Handler = Callable[[web.Request], Awaitable[web.StreamResponse]]

# Paths exempt from auth: liveness probe only. The mesh is session-private, but
# everything that reads or mutates state still requires the session token.
_EXEMPT_PATHS = frozenset({"/healthz"})


def _error_response(request: web.Request, code: str, message: str) -> web.Response:
    error = RpcError(
        code=code,  # type: ignore[arg-type]  # callers pass ErrorCode literals
        message=message,
        request_id=request.headers.get(HEADER_REQUEST_ID, ""),
    )
    return web.json_response(
        error.model_dump(mode="json"),
        status=HTTP_STATUS_BY_CODE[code],
        headers={HEADER_REQUEST_ID: error.request_id},
    )


# Paths that remain answerable after the VM is reclaimed: liveness, the
# handshake (so a re-acquiring world can still read capabilities), and the
# reclaim endpoint itself (idempotent).
_RECLAIM_OK_SUFFIXES = ("/handshake", "/pool/reclaim")


def build_auth_middleware(ctx: DaemonContext):
    @web.middleware
    async def auth_middleware(request: web.Request, handler: _Handler) -> web.StreamResponse:
        if request.path in _EXEMPT_PATHS or not request.path.startswith(API_PREFIX):
            return await handler(request)
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")
        if scheme.lower() != "bearer" or not ctx.token_matches(credentials.strip()):
            return _error_response(request, "UNAUTHORIZED", "Missing or invalid bearer token")
        # Once reclaimed, every op except the exempt suffixes gets a typed
        # RECLAIMED error — the world sees a semantic state instead of a
        # dropped connection (pool-churn exit-255 fix).
        if ctx.reclaimed and not request.path.endswith(_RECLAIM_OK_SUFFIXES):
            return _error_response(request, "RECLAIMED", "VM is being reclaimed by the warm pool")
        return await handler(request)

    return auth_middleware
