"""WebSocket reverse proxy from an app-subdomain request to the resolved
Teleport app (spec §5 Phase 3).

This is the WebSocket sibling of ``browser_proxy/http_proxy.py``. code-server
(the ``vscode-opencode`` product) drives its editor and terminal over
WebSockets, so this is the piece that makes it fully usable in a browser
through the proxy; Phase 2a already covers the plain-HTTP path.

Two things make this endpoint materially different from the HTTP catch-all,
and both are load-bearing security properties:

* **Routing.** A browser WebSocket arrives as an ASGI ``websocket`` scope, not
  through the HTTP catch-all (``@app.api_route``). It is served by a catch-all
  ``@app.websocket("/{full_path:path}")`` registered *after* the apex
  ``/tunnel`` WebSocket route and the ``/mcp`` mount, so Starlette's
  registration-order matching keeps those two surfaces theirs; a
  ``WebSocketRoute`` only matches ``websocket`` scopes, so it never shadows the
  HTTP proxy either. The endpoint additionally host-gates to app subdomains.

* **Auth.** ``APIKeyMiddleware`` is a ``BaseHTTPMiddleware`` and does **not**
  run on ``websocket`` scopes -- so nothing validates the session cookie for
  us on a WS handshake the way it does for an HTTP request. :func:`handle_app_
  proxy_websocket` therefore authenticates and authorizes explicitly, and
  **rejects the handshake (fail closed) before any cube dial-out** if anything
  is off: not an app-subdomain host, missing/invalid credential, cross-origin
  handshake on a cookie session (cross-site WebSocket hijacking defense atop
  ``SameSite=Lax``), or an out-of-scope profile (spec §4.3).

Framing model. The upstream leg is dialed with the exact same tbot-mTLS helper
the HTTP proxy uses (``tunnel.relay.open_app_connection``) and speaks the
client side of the WebSocket protocol over that raw TLS socket via ``wsproto``
(sans-io, depends only on ``h11`` which is already a dependency). The browser
leg is a Starlette ``WebSocket`` -- uvicorn decodes/encodes its frames for us.
We therefore relay **decoded messages** (not raw frames) between the two legs;
each leg negotiates its own ``permessage-deflate`` independently and compresses
transparently, so relaying decoded messages is correct even when one or both
legs compress. The browser's requested subprotocol is forwarded to the upstream
handshake and the upstream's chosen subprotocol is echoed back to the browser.
"""

from __future__ import annotations

import asyncio
import logging
from urllib.parse import urlsplit

from starlette.websockets import WebSocket, WebSocketDisconnect
from wsproto import ConnectionType, WSConnection
from wsproto.events import (
    AcceptConnection,
    BytesMessage,
    CloseConnection,
    Ping,
    Pong,
    RejectConnection,
    Request,
    TextMessage,
)

from cube_cloud.auth import api_keys, session_cookie
from cube_cloud.auth.session_cookie import (
    SESSION_COOKIE_NAME,
    strip_session_cookie as _strip_session_cookie,
)
from cube_cloud.browser_proxy.authz import authorize_app_access
from cube_cloud.browser_proxy.resolver import resolve_app_name
from cube_cloud.tunnel.relay import open_app_connection

logger = logging.getLogger(__name__)

# Close codes used when we reject or tear down. 44xx are app-defined (RFC 6455
# private-use range); 1011 is the standard "internal error" we map dial/upstream
# failures to (the WS equivalent of the HTTP path's 502).
WS_CLOSE_POLICY = 1008  # bad host / no such app route
WS_CLOSE_UNAUTHORIZED = 4401
WS_CLOSE_FORBIDDEN = 4403
WS_CLOSE_UPSTREAM_ERROR = 1011

CONNECT_TIMEOUT = 45  # matches http_proxy/relay: tbot oneshot + TLS + handshake
READ_TIMEOUT = 30  # per-read timeout waiting on the upstream handshake response
UPSTREAM_READ_SIZE = 65536

# Handshake headers we never forward verbatim to the upstream: wsproto
# regenerates all of these itself (Host is passed separately, below), and
# Content-Length has no meaning on a WS handshake.
_WS_HANDSHAKE_SKIP = frozenset({
    "host", "upgrade", "connection", "content-length",
    "sec-websocket-key", "sec-websocket-version",
    "sec-websocket-protocol", "sec-websocket-extensions",
})


class ProxyError(Exception):
    """Raised for any failure dialing or handshaking with the upstream app.

    Never indicates the caller was unauthenticated/unauthorized -- those are
    rejected before a dial is even attempted.
    """


# ---------------------------------------------------------------------------
# Upstream WebSocket (client side over the raw tbot-mTLS socket)
# ---------------------------------------------------------------------------


class UpstreamWebSocket:
    """A client-side WebSocket to the Teleport app over the mTLS stream.

    Wraps the ``(StreamReader, StreamWriter)`` from ``open_app_connection`` and
    a ``wsproto`` CLIENT connection. Handshake is performed by
    :func:`open_upstream_websocket`; after that, callers use
    :meth:`send_text`/:meth:`send_bytes` to push a browser message upstream and
    iterate :meth:`incoming` to pull decoded upstream messages.
    """

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        conn: WSConnection,
        subprotocol: str | None,
        pending_events: list,
    ) -> None:
        self._reader = reader
        self._writer = writer
        self._conn = conn
        self.subprotocol = subprotocol
        # Any post-handshake events wsproto already parsed out of the same read
        # that delivered AcceptConnection (a server that speaks first). These
        # must be drained before we read more bytes, or those messages are lost.
        self._pending = pending_events
        self._closed = False

    def _write_event(self, event) -> None:
        self._writer.write(self._conn.send(event))

    async def send_text(self, data: str) -> None:
        self._write_event(TextMessage(data=data))
        await self._writer.drain()

    async def send_bytes(self, data: bytes) -> None:
        self._write_event(BytesMessage(data=data))
        await self._writer.drain()

    async def _next_events(self) -> list:
        """Return the next batch of wsproto events (draining pending first).

        No read timeout here, deliberately: an established WebSocket is idle
        for long stretches by design (code-server between keystrokes), so a
        per-read timeout would tear down a perfectly healthy connection. The
        relay instead ends on an actual close/EOF from either side. The
        handshake read (:func:`_read_upstream_handshake`) *does* bound its wait,
        since a hung upstream there must not block the browser indefinitely.

        Tradeoff (accepted for the POC, deferred to spec Phase 5 hardening): an
        authenticated-but-idle or half-open connection holds an mTLS socket +
        two tasks with no idle reaper or absolute-lifetime cap. Behind auth this
        is fine at POC scale; a bounded idle/max-lifetime deadline (or upstream
        keepalive ping) belongs with the Phase 5 held-connection-sizing work.
        """
        if self._pending:
            batch, self._pending = self._pending, []
            return batch
        data = await self._reader.read(UPSTREAM_READ_SIZE)
        if not data:
            return [CloseConnection(code=1006, reason="upstream closed")]
        self._conn.receive_data(data)
        return list(self._conn.events())

    async def incoming(self):
        """Yield decoded upstream messages as ``("text"|"bytes", data)`` until
        the upstream connection closes.

        Coalesces fragmented messages, answers upstream Pings with Pongs
        inline, and stops (returns) once the upstream sends a Close or the TLS
        stream reaches EOF.
        """
        text_buf: list[str] = []
        bytes_buf = bytearray()
        while True:
            for event in await self._next_events():
                if isinstance(event, TextMessage):
                    text_buf.append(event.data)
                    if event.message_finished:
                        yield ("text", "".join(text_buf))
                        text_buf = []
                elif isinstance(event, BytesMessage):
                    bytes_buf.extend(event.data)
                    if event.message_finished:
                        yield ("bytes", bytes(bytes_buf))
                        bytes_buf = bytearray()
                elif isinstance(event, Ping):
                    self._write_event(event.response())
                    await self._writer.drain()
                elif isinstance(event, Pong):
                    continue
                elif isinstance(event, CloseConnection):
                    # Echo the close back if the protocol state still allows it,
                    # then stop. Best-effort: the stream may already be gone.
                    try:
                        self._write_event(event.response())
                        await self._writer.drain()
                    except Exception:
                        pass
                    return

    async def close(self, code: int = 1000) -> None:
        """Send a Close (best-effort) and tear down the TLS stream."""
        if self._closed:
            return
        self._closed = True
        try:
            self._write_event(CloseConnection(code=code))
            await self._writer.drain()
        except Exception:
            pass
        try:
            self._writer.close()
            await self._writer.wait_closed()
        except Exception:
            pass


def build_upstream_handshake_headers(ws: WebSocket) -> list[tuple[bytes, bytes]]:
    """Forward relevant handshake headers to the upstream WS request.

    Drops the headers wsproto regenerates itself (``_WS_HANDSHAKE_SKIP``) and
    strips **our** session cookie from any forwarded ``Cookie`` header so the
    ``cmcp_`` API key is never leaked to the in-cube app -- while preserving the
    app's own cookies, which it may need for its own session.
    """
    out: list[tuple[bytes, bytes]] = []
    for name, value in ws.headers.raw:
        lname = name.decode("latin-1").lower()
        if lname in _WS_HANDSHAKE_SKIP:
            continue
        if lname == "cookie":
            filtered = _strip_session_cookie(value.decode("latin-1"))
            if filtered:
                out.append((b"cookie", filtered.encode("latin-1")))
            continue
        out.append((name, value))
    return out


async def open_upstream_websocket(
    app_name: str,
    profile: str,
    *,
    host: str,
    target: str,
    subprotocols: list[str],
    extra_headers: list[tuple[bytes, bytes]],
    connect_timeout: float = CONNECT_TIMEOUT,
) -> UpstreamWebSocket:
    """Dial the resolved Teleport app and perform the client WS handshake.

    ``host`` is forwarded verbatim as the upstream Host header (spec Appendix A:
    absolute URLs the app emits must resolve against the subdomain origin the
    browser uses). Raises :class:`ProxyError` on any dial or handshake failure;
    the socket is closed before the exception escapes so nothing leaks.
    """
    try:
        reader, writer = await asyncio.wait_for(
            open_app_connection(app_name, profile=profile), timeout=connect_timeout,
        )
    except asyncio.TimeoutError as e:
        raise ProxyError(f"connection to '{app_name}' timed out") from e
    except Exception as e:
        raise ProxyError(f"failed to connect to '{app_name}': {e}") from e

    conn = WSConnection(ConnectionType.CLIENT)
    try:
        request = Request(
            host=host,
            target=target,
            subprotocols=subprotocols,
            extra_headers=extra_headers,
        )
        writer.write(conn.send(request))
        await writer.drain()

        accepted, pending = await _read_upstream_handshake(reader, conn)
    except ProxyError:
        await _close_writer(writer)
        raise
    except Exception as e:
        await _close_writer(writer)
        raise ProxyError(f"WS handshake to '{app_name}' failed: {e}") from e

    return UpstreamWebSocket(reader, writer, conn, accepted.subprotocol, pending)


async def _read_upstream_handshake(
    reader: asyncio.StreamReader, conn: WSConnection,
) -> tuple[AcceptConnection, list]:
    """Pump ``reader`` into ``conn`` until the upstream accepts (or rejects).

    Returns ``(AcceptConnection, pending_events)`` where ``pending_events`` are
    any message/close/ping events wsproto parsed from the same read that
    delivered the accept (a server that speaks immediately after 101).
    """
    while True:
        try:
            data = await asyncio.wait_for(reader.read(UPSTREAM_READ_SIZE), timeout=READ_TIMEOUT)
        except asyncio.TimeoutError as e:
            raise ProxyError("timed out waiting for the app's WS handshake") from e
        if not data:
            raise ProxyError("app closed the connection during the WS handshake")
        conn.receive_data(data)

        accepted: AcceptConnection | None = None
        pending: list = []
        for event in conn.events():
            if isinstance(event, AcceptConnection):
                accepted = event
            elif isinstance(event, RejectConnection):
                raise ProxyError(f"app rejected the WS handshake: HTTP {event.status_code}")
            elif accepted is not None:
                pending.append(event)
            # else: pre-accept event we don't expect; ignore.
        if accepted is not None:
            return accepted, pending
        # No terminal event yet -- keep reading.


async def _close_writer(writer: asyncio.StreamWriter) -> None:
    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Bidirectional relay
# ---------------------------------------------------------------------------


async def _browser_to_upstream(ws: WebSocket, up: UpstreamWebSocket) -> None:
    """Pump decoded browser messages upstream until the browser disconnects."""
    try:
        while True:
            message = await ws.receive()
            if message["type"] == "websocket.disconnect":
                return
            text = message.get("text")
            if text is not None:
                await up.send_text(text)
                continue
            data = message.get("bytes")
            if data is not None:
                await up.send_bytes(data)
    except WebSocketDisconnect:
        return


async def _upstream_to_browser(ws: WebSocket, up: UpstreamWebSocket) -> None:
    """Pump decoded upstream messages to the browser until the upstream closes."""
    async for kind, data in up.incoming():
        if kind == "text":
            await ws.send_text(data)
        else:
            await ws.send_bytes(data)


async def relay(ws: WebSocket, up: UpstreamWebSocket) -> None:
    """Relay frames both ways until either side closes, then tear both down.

    Whichever direction finishes first (browser disconnect, upstream close/EOF,
    or an error in either) cancels the other and closes both the upstream TLS
    socket and the browser WebSocket -- no leaked tasks or sockets.
    """
    b2u = asyncio.create_task(_browser_to_upstream(ws, up))
    u2b = asyncio.create_task(_upstream_to_browser(ws, up))
    try:
        done, pending = await asyncio.wait(
            {b2u, u2b}, return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        # Surface an unexpected error from the finished direction (a normal
        # disconnect/close returns None and is not an error).
        for task in done:
            exc = task.exception()
            if exc is not None and not isinstance(exc, WebSocketDisconnect):
                logger.debug("app_proxy ws relay direction ended with: %s", exc)
    finally:
        await up.close()
        try:
            await ws.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Endpoint entry point (auth + authz + dial + relay)
# ---------------------------------------------------------------------------


def _extract_credential(ws: WebSocket) -> tuple[str | None, bool]:
    """Return ``(raw_key, via_cookie)``.

    Mirrors ``APIKeyMiddleware``: a ``Bearer`` header wins; the parent-domain
    session cookie is the browser fallback. The caller has already host-gated to
    an app subdomain, which is the only place cookie-auth is honored (spec §4.2
    CSRF rule) -- ``/tunnel`` and ``/mcp`` are separate routes and never reach
    here.
    """
    auth_header = ws.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:], False
    return ws.cookies.get(SESSION_COOKIE_NAME), True


def _origin_matches_host(ws: WebSocket, host: str) -> bool:
    """True iff the handshake's Origin is same-origin with the target host.

    Defense-in-depth against cross-site WebSocket hijacking: because auth is
    cookie-based, a malicious page could try to open an authenticated WS.
    ``SameSite=Lax`` should already stop the browser from attaching the session
    cookie to a cross-site WS handshake; this Origin check is a second, explicit
    barrier. A legitimate browser always sends Origin on a WS handshake, so a
    missing Origin fails closed.
    """
    origin = ws.headers.get("origin")
    if not origin:
        return False
    parts = urlsplit(origin)
    return parts.scheme == "https" and (parts.hostname or "").lower() == host.lower()


def _audit(profile: str, host: str, app_name: str, status: str) -> None:
    """One structured line per WS handshake attempt (mirrors the HTTP audit)."""
    logger.info(
        "app_proxy ws profile=%s host=%s app=%s status=%s",
        profile, host, app_name, status,
    )


async def handle_app_proxy_websocket(ws: WebSocket) -> None:
    """Top-level handler for the app-subdomain WebSocket catch-all route.

    Authenticates + authorizes explicitly (APIKeyMiddleware does not run on
    websocket scopes), then dials the resolved app and relays. Every failure
    rejects the handshake (``ws.close`` before ``accept``) so no dial-out
    happens for a request that doesn't clear every gate -- fail closed.
    """
    host = ws.url.hostname or ""

    if not session_cookie.is_app_subdomain_host(host):
        # Not an app-subdomain WS this proxy owns (e.g. apex). Reject; the
        # Bearer-only /mcp + /tunnel surfaces are separate routes.
        await ws.close(code=WS_CLOSE_POLICY)
        return

    app_name = resolve_app_name(host)
    if app_name is None:
        await ws.close(code=WS_CLOSE_POLICY)
        return

    raw_key, via_cookie = _extract_credential(ws)
    if not raw_key:
        _audit("-", host, app_name, "4401-nocred")
        await ws.close(code=WS_CLOSE_UNAUTHORIZED)
        return

    try:
        item = await api_keys.validate_key(raw_key)
    except Exception as e:
        logger.error("app_proxy ws auth error: %s", e)
        item = None
    if not item:
        _audit("-", host, app_name, "4401-badkey")
        await ws.close(code=WS_CLOSE_UNAUTHORIZED)
        return
    profile = item["profile"]

    # Cross-site WebSocket hijacking defense (cookie sessions only; a Bearer
    # token can't be attached by a cross-site page, so it isn't CSRF-able).
    if via_cookie and not _origin_matches_host(ws, host):
        _audit(profile, host, app_name, "4403-origin")
        await ws.close(code=WS_CLOSE_FORBIDDEN)
        return

    if not await authorize_app_access(profile, app_name):
        _audit(profile, host, app_name, "4403-authz")
        await ws.close(code=WS_CLOSE_FORBIDDEN)
        return

    target = ws.url.path
    if ws.url.query:
        target += f"?{ws.url.query}"
    upstream_host = ws.headers.get("host") or host
    subprotocols = list(ws.scope.get("subprotocols") or [])
    extra_headers = build_upstream_handshake_headers(ws)

    try:
        up = await open_upstream_websocket(
            app_name, profile,
            host=upstream_host,
            target=target,
            subprotocols=subprotocols,
            extra_headers=extra_headers,
        )
    except ProxyError as e:
        logger.warning("app_proxy ws dial failed app=%s: %s", app_name, e)
        _audit(profile, host, app_name, "1011-dial")
        await ws.close(code=WS_CLOSE_UPSTREAM_ERROR)
        return

    _audit(profile, host, app_name, "101")
    await ws.accept(subprotocol=up.subprotocol)
    try:
        await relay(ws, up)
    finally:
        await up.close()
