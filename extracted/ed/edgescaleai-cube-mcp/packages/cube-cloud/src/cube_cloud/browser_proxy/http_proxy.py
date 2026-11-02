"""HTTP reverse proxy from an app-subdomain request to the resolved Teleport
app (spec §5 Phase 2a -- the MVP go/no-go).

Dial path: reuses ``tunnel.relay.open_app_connection`` verbatim -- the same
tbot-mTLS dial the ``/tunnel`` WebSocket relay uses for the agent's raw TCP
app_proxy. That call returns a plain ``(StreamReader, StreamWriter)`` TLS
connection to the Teleport proxy, SNI/ALPN-routed to the target app; for an
HTTP app it negotiates a normal HTTP/1.1 conversation, which this module
speaks using ``h11`` (a sans-io HTTP/1.1 implementation, already a transitive
dependency via httpx -> httpcore).

Design choices (POC-scoped, revisit for Phase 4/5):
  * One fresh mTLS connection per proxied request (no keep-alive/pooling).
    Simpler and correct; tbot's own cert cache keeps this cheap.
  * The request body is buffered in full (no chunked-request streaming),
    capped at ``settings.app_proxy_max_body_bytes`` to bound per-request
    memory use, and sent with an explicit, recomputed Content-Length. The
    response is streamed to the browser without buffering.
  * The original browser-facing Host header is forwarded to the app verbatim
    (NOT rewritten to the internal Teleport SNI host) -- this is what makes
    absolute URLs the app emits resolve correctly against the subdomain
    origin the browser is using (spec Appendix A). The Teleport dial itself
    doesn't care what HTTP Host header rides over it: routing to the right
    app already happened via SNI + the app-scoped mTLS cert.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator

import h11
from starlette.requests import ClientDisconnect, Request
from starlette.responses import JSONResponse, Response, StreamingResponse

from cube_cloud.auth.session_cookie import SESSION_COOKIE_NAME, strip_session_cookie
from cube_cloud.browser_proxy.authz import authorize_app_access
from cube_cloud.browser_proxy.rate_limit import SlidingWindowRateLimiter
from cube_cloud.browser_proxy.resolver import resolve_app_name
from cube_cloud.config import settings
from cube_cloud.tunnel.relay import open_app_connection

logger = logging.getLogger(__name__)

# RFC 7230 §6.1 hop-by-hop headers -- never forwarded in either direction.
# Content-Length is handled separately (always recomputed by the sender).
HOP_BY_HOP_HEADERS = frozenset({
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailer", "transfer-encoding", "upgrade",
})

CONNECT_TIMEOUT = 45  # matches relay.py's CONNECT timeout (tbot oneshot + TLS)
READ_TIMEOUT = 30  # per-chunk read timeout while waiting on the app


class ProxyError(Exception):
    """Raised for any failure dialing or speaking to the resolved app.

    Callers should treat this as a 502 -- it never indicates the caller was
    unauthenticated/unauthorized (those are rejected before a dial is even
    attempted).
    """


class RequestBodyTooLarge(Exception):
    """Raised when the browser's request body exceeds the configured cap."""


async def _close_writer(writer: asyncio.StreamWriter) -> None:
    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass


async def read_request_body_capped(request: Request, max_bytes: int) -> bytes:
    """Buffer the request body, aborting early past ``max_bytes``.

    Reads via ``request.stream()`` rather than trusting the client's
    Content-Length (which is just a claim) -- this is what actually bounds
    memory use per proxied request. Raises ``RequestBodyTooLarge`` as soon as
    the cap is exceeded, without buffering the rest.
    """
    chunks: list[bytes] = []
    total = 0
    async for chunk in request.stream():
        total += len(chunk)
        if total > max_bytes:
            raise RequestBodyTooLarge(f"body exceeds {max_bytes} byte cap")
        chunks.append(chunk)
    return b"".join(chunks)


def build_request_headers(request: Request, body_len: int) -> list[tuple[bytes, bytes]]:
    """Build the outbound header list for the app, from the browser's request.

    Strips hop-by-hop headers, the original Content-Length (recomputed from the
    actual buffered body below), and our ``cmcp_session`` cookie from the Cookie
    header (so the API key never reaches the app); preserves everything else,
    including Host (see module docstring).
    """
    headers: list[tuple[bytes, bytes]] = []
    for name, value in request.headers.items():
        lname = name.lower()
        if lname in HOP_BY_HOP_HEADERS or lname == "content-length":
            continue
        if lname == "cookie":
            # Strip our session cookie so the cmcp_ API key is never forwarded to
            # the in-cube app; keep the app's own cookies. Symmetric with the WS
            # leg (ws_proxy.build_upstream_handshake_headers).
            filtered = strip_session_cookie(value)
            if filtered:
                headers.append((b"cookie", filtered.encode("latin-1")))
            continue
        headers.append((name.encode("latin-1"), value.encode("latin-1")))
    headers.append((b"content-length", str(body_len).encode("ascii")))
    return headers


def filter_response_headers(raw_headers: list[tuple[bytes, bytes]]) -> list[tuple[bytes, bytes]]:
    """Strip hop-by-hop + framing headers from the app's response.

    Content-Length and Transfer-Encoding are dropped unconditionally: the
    response is re-streamed to the browser via a Starlette StreamingResponse,
    which lets uvicorn pick correct framing (chunked) for a body of unknown
    total length -- reusing the app's original framing headers verbatim would
    desynchronize from what we actually stream (h11 already de-chunked the
    body for us). The app's own Set-Cookie headers pass through, multi-valued and
    untouched, with ONE exception: a Set-Cookie for our own session cookie name is
    dropped (see below).
    """
    out = []
    for name, value in raw_headers:
        lname = name.decode("latin-1").lower()
        if lname in HOP_BY_HOP_HEADERS or lname == "content-length":
            continue
        if lname == "set-cookie" and _sets_session_cookie(value):
            # Cookie-tossing guard. App subdomains are children of `.<apex>`, so a
            # proxied in-cube app could emit
            #   Set-Cookie: cmcp_session=<its own key>; Domain=.<apex>; Path=/
            # and overwrite a visitor's session for EVERY host under the apex,
            # including the apex console. An in-cube app has no legitimate reason
            # to set our session cookie name, so this is dropped rather than
            # forwarded. Symmetric with `strip_session_cookie`, which already
            # keeps our key from reaching the app on the request leg.
            logger.warning(
                "app_proxy dropped a Set-Cookie for %s from the upstream app",
                SESSION_COOKIE_NAME,
            )
            continue
        out.append((name, value))
    return out


def _sets_session_cookie(set_cookie_value: bytes) -> bool:
    """True iff this Set-Cookie header assigns our session cookie name.

    Only the cookie NAME is inspected (everything before the first `=`), so an
    app cookie that merely mentions the name in its value is unaffected.
    """
    raw = set_cookie_value.decode("latin-1", "replace")
    cookie_name = raw.split("=", 1)[0].strip().lower()
    return cookie_name == SESSION_COOKIE_NAME.lower()


async def _pump_until(reader: asyncio.StreamReader, conn: h11.Connection) -> None:
    try:
        data = await asyncio.wait_for(reader.read(65536), timeout=READ_TIMEOUT)
    except asyncio.TimeoutError as e:
        raise ProxyError("timed out waiting for the app") from e
    conn.receive_data(data)


async def _read_response_head(
    reader: asyncio.StreamReader, conn: h11.Connection,
) -> tuple[int, list[tuple[bytes, bytes]]]:
    """Pump ``reader`` into ``conn`` until the final response head arrives."""
    while True:
        try:
            event = conn.next_event()
        except h11.RemoteProtocolError as e:
            raise ProxyError(f"malformed response from app: {e}") from e
        if event is h11.NEED_DATA:
            await _pump_until(reader, conn)
            continue
        if isinstance(event, h11.InformationalResponse):
            continue  # skip 1xx and wait for the final response
        if isinstance(event, h11.Response):
            return event.status_code, list(event.headers.raw_items())
        if isinstance(event, h11.ConnectionClosed):
            raise ProxyError("app closed the connection before sending a response")
        raise ProxyError(f"unexpected response event from app: {event!r}")


async def proxy_http_request(
    app_name: str,
    profile: str,
    method: str,
    target: str,
    headers: list[tuple[bytes, bytes]],
    body: bytes,
) -> tuple[int, list[tuple[bytes, bytes]], AsyncIterator[bytes]]:
    """Dial the resolved Teleport app and forward one HTTP request.

    Returns ``(status_code, response_headers, body_aiter)``. The connection
    is closed automatically once ``body_aiter`` is fully consumed or closed
    (including on early client disconnect, via the async generator's
    ``finally``). Raises ``ProxyError`` on any dial or protocol failure.
    """
    try:
        reader, writer = await asyncio.wait_for(
            open_app_connection(app_name, profile=profile), timeout=CONNECT_TIMEOUT,
        )
    except asyncio.TimeoutError as e:
        raise ProxyError(f"connection to '{app_name}' timed out") from e
    except Exception as e:
        raise ProxyError(f"failed to connect to '{app_name}': {e}") from e

    conn = h11.Connection(our_role=h11.CLIENT)
    try:
        req_event = h11.Request(method=method, target=target, headers=headers)
        writer.write(conn.send(req_event))
        if body:
            writer.write(conn.send(h11.Data(data=body)))
        writer.write(conn.send(h11.EndOfMessage()))
        await writer.drain()

        status_code, resp_headers = await _read_response_head(reader, conn)
    except ProxyError:
        await _close_writer(writer)
        raise
    except Exception as e:
        # Covers h11.LocalProtocolError (e.g. a request header value h11
        # refuses to frame) and anything else unexpected while sending --
        # never let this escape as an unhandled exception, or the caller
        # skips both the 502 response and the audit log line.
        await _close_writer(writer)
        raise ProxyError(f"failed to send request to '{app_name}': {e}") from e

    async def body_iter() -> AsyncIterator[bytes]:
        try:
            while True:
                try:
                    event = conn.next_event()
                except h11.RemoteProtocolError as e:
                    raise ProxyError(f"malformed response from app: {e}") from e
                if event is h11.NEED_DATA:
                    await _pump_until(reader, conn)
                    continue
                if isinstance(event, h11.Data):
                    yield bytes(event.data)
                    continue
                if isinstance(event, (h11.EndOfMessage, h11.ConnectionClosed)):
                    break
        finally:
            await _close_writer(writer)

    return status_code, resp_headers, body_iter()


def _audit(profile: str, host: str, app_name: str, method: str, path: str, status: int) -> None:
    """One structured line per proxied request (spec §5 Phase 2a security floor)."""
    logger.info(
        "app_proxy request profile=%s host=%s app=%s method=%s path=%s status=%s",
        profile, host, app_name, method, path, status,
    )


async def handle_app_proxy_request(
    request: Request, rate_limiter: SlidingWindowRateLimiter,
) -> Response:
    """Top-level entry point for the app-proxy catch-all route in main.py.

    By the time this runs, APIKeyMiddleware has already authenticated the
    request (it never calls through to routing otherwise) -- so
    ``request.state.profile`` is always set here. Fail-closed ordering: host
    resolution, rate limit, then authorization (spec §4.3), all before any
    dial or even reading the request body. No dial is ever attempted for a
    request that doesn't clear every gate.
    """
    host = request.url.hostname or ""
    app_name = resolve_app_name(host)
    if app_name is None:
        # Not an app-subdomain request this proxy owns -- plain 404, not an
        # audited proxy event.
        return JSONResponse(status_code=404, content={"error": "Not found"})

    profile = request.state.profile
    session_key = request.state.session_key
    method = request.method
    path = request.url.path

    if "upgrade" in request.headers:
        _audit(profile, host, app_name, method, path, 501)
        return JSONResponse(
            status_code=501,
            content={"error": "WebSocket is not supported by the app proxy yet."},
        )

    if not rate_limiter.allow(session_key):
        _audit(profile, host, app_name, method, path, 429)
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    if not await authorize_app_access(profile, app_name):
        _audit(profile, host, app_name, method, path, 403)
        return JSONResponse(status_code=403, content={"error": "Forbidden"})

    try:
        body = await read_request_body_capped(request, settings.app_proxy_max_body_bytes)
    except ClientDisconnect:
        # Client is already gone; nothing to send a response to, but still
        # audit the attempt and return cleanly rather than let this escape
        # as an unhandled exception.
        _audit(profile, host, app_name, method, path, 499)
        return Response(status_code=499)
    except RequestBodyTooLarge:
        _audit(profile, host, app_name, method, path, 413)
        return JSONResponse(status_code=413, content={"error": "Request body too large"})

    headers = build_request_headers(request, len(body))
    target = path
    if request.url.query:
        target += f"?{request.url.query}"

    try:
        status_code, resp_headers, body_aiter = await proxy_http_request(
            app_name, profile, method, target, headers, body,
        )
    except ProxyError as e:
        logger.warning("app_proxy dial failed app=%s: %s", app_name, e)
        _audit(profile, host, app_name, method, path, 502)
        return JSONResponse(status_code=502, content={"error": "Failed to reach the app"})

    _audit(profile, host, app_name, method, path, status_code)
    response = StreamingResponse(body_aiter, status_code=status_code)
    response.raw_headers.extend(filter_response_headers(resp_headers))
    return response
