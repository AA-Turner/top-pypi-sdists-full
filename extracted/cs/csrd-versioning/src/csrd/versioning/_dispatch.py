"""Version-dispatch middleware for FastAPI.

Intercepts inbound requests, resolves the target API version from request
headers, rewrites the ASGI ``path`` to the version-keyed mount, and manages
request-scoped context variables for the duration of each request.
"""

import json
import logging
import uuid

from fastapi import Request
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send

from csrd.context import (
    reset_api_version_context,
    reset_headers_context,
    set_api_version_context,
    set_headers_context,
)
from csrd.context.middleware import REQUEST_SCOPE_KEY
from csrd.versioning._constants import (
    API_VERSION_HEADER_NAME,
    APP_ID_HEADER_NAME,
    HIT_ID_HEADER_NAME,
)
from csrd.versioning._core import map_version_path, normalize_prefix, resolve_version
from csrd.versioning._types import VersionKey, VersionMap

logger = logging.getLogger(__name__)

_DOCS_PREFIXES = ("/swagger-ui", "/openapi", "/_info", "/actuator", "/docs", "/redoc")


def _ensure_request_scope(
    request: Request,
    *,
    hit_id_header: str = HIT_ID_HEADER_NAME,
    app_id_header: str = APP_ID_HEADER_NAME,
) -> None:
    """Ensure request scope has request context even without logging middleware."""
    scope = request.scope.get(REQUEST_SCOPE_KEY)
    if scope is None:
        scope = {}
        request.scope[REQUEST_SCOPE_KEY] = scope

    hit_id = request.headers.get(hit_id_header)
    app_id = request.headers.get(app_id_header)
    if "hit_id" not in scope:
        scope["hit_id"] = hit_id or str(uuid.uuid4())
    if "app_id" not in scope and app_id is not None:
        scope["app_id"] = app_id


def _map_version_endpoint(request: Request, version: str, prefix: str) -> str:
    """Rewrite an incoming path to include resolved version under the API prefix."""
    return map_version_path(str(request.url.path), version=version, prefix=prefix)


def _get_version(
    request: Request,
    *,
    version_mapping: VersionMap | None = None,
    default_version: VersionKey | None = None,
    strict: bool = False,
) -> str:
    """Resolve request version using explicit, deterministic fallback precedence."""
    requested_version = request.headers.get(API_VERSION_HEADER_NAME)
    return resolve_version(
        requested_version=requested_version,
        version_mapping=version_mapping,
        default_version=default_version,
        strict=strict,
    )


def _should_dispatch_request(request: Request, prefix: str) -> bool:
    """Return True when request path is handled by version-dispatch middleware."""
    normalized_prefix = normalize_prefix(prefix)
    path = request.url.path

    return _should_dispatch_path(path, normalized_prefix)


def _should_dispatch_path(path: str, normalized_prefix: str) -> bool:
    """Return True when path is handled by version-dispatch middleware."""

    if any(path == p or path.startswith(f"{p}/") for p in _DOCS_PREFIXES) or path == "/":
        return False

    if normalized_prefix == "/":
        return True

    return path == normalized_prefix or path.startswith(f"{normalized_prefix}/")


async def _send_json_error(
    send: Send,
    scope: Scope,
    *,
    status_code: int,
    detail: str,
) -> None:
    """Send a JSON error response using the raw ASGI ``send`` callable."""
    body = json.dumps({"detail": detail}).encode("utf-8")
    headers: list[list[bytes]] = [
        [b"content-type", b"application/json"],
        [b"content-length", str(len(body)).encode("ascii")],
    ]

    for header_name, header_value in scope.get("headers", []):
        if header_name == b"origin":
            headers.append([b"access-control-allow-origin", header_value])
            headers.append([b"vary", b"origin"])
            break

    await send(
        {
            "type": "http.response.start",
            "status": status_code,
            "headers": headers,
        }
    )
    await send({"type": "http.response.body", "body": body, "more_body": False})


async def _close_websocket_error(send: Send, *, code: int = 1008, reason: str = "") -> None:
    """Close a websocket connection with an explicit policy/error code."""
    await send(
        {
            "type": "websocket.close",
            "code": code,
            "reason": reason,
        }
    )


class VersionDispatchMiddleware:
    """Raw ASGI middleware for version dispatch.

    Unlike ``BaseHTTPMiddleware`` / ``@app.middleware("http")``, this does
    **not** buffer the response body, so ``StreamingResponse`` and SSE
    endpoints work correctly through versioned routes.
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        prefix: str,
        version_mapping: VersionMap,
        default_version: VersionKey | None = None,
        hit_id_header: str = HIT_ID_HEADER_NAME,
        app_id_header: str = APP_ID_HEADER_NAME,
        strict_version_matching: bool = False,
    ) -> None:
        self.app = app
        self.prefix = normalize_prefix(prefix)
        self.version_mapping = version_mapping
        self.default_version = default_version
        self.hit_id_header = hit_id_header
        self.app_id_header = app_id_header
        self.strict_version_matching = strict_version_matching

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope_type = scope["type"]
        if scope_type not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if not _should_dispatch_path(path, self.prefix):
            await self.app(scope, receive, send)
            return

        if scope_type == "http":
            request = Request(scope)
            headers = request.headers
            _ensure_request_scope(
                request,
                hit_id_header=self.hit_id_header,
                app_id_header=self.app_id_header,
            )
        else:
            headers = Headers(scope=scope)

        try:
            version = resolve_version(
                requested_version=headers.get(API_VERSION_HEADER_NAME),
                version_mapping=self.version_mapping,
                default_version=self.default_version,
                strict=self.strict_version_matching,
            )
        except ValueError as exc:
            if scope_type == "http":
                await _send_json_error(send, scope, status_code=400, detail=str(exc))
            else:
                await _close_websocket_error(send, code=1008, reason=str(exc))
            return

        token = set_api_version_context(version)
        scope["api_version"] = version
        try:
            headers_token = set_headers_context(headers)
            try:
                mapped_path = map_version_path(path, version=version, prefix=self.prefix)
                logger.debug(
                    "Version dispatch: %s -> %s (resolved version=%s)",
                    path,
                    mapped_path,
                    version,
                )
                scope["path"] = mapped_path
                original_raw = scope.get("raw_path", b"")
                prefix_bytes = self.prefix.rstrip("/").encode("utf-8")
                version_segment = b"/" + version.encode("utf-8")
                if prefix_bytes == b"":
                    raw_remainder = original_raw
                else:
                    raw_remainder = original_raw[len(prefix_bytes) :]
                if raw_remainder == b"/":
                    raw_remainder = b""
                scope["raw_path"] = prefix_bytes + version_segment + raw_remainder
                await self.app(scope, receive, send)
            finally:
                reset_headers_context(headers_token)
        finally:
            reset_api_version_context(token)
