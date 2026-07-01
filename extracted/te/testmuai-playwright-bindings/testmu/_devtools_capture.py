"""DevTools capture layer for testmu binding.

Attaches page event listeners (network, console) and installs performance
init scripts based on testmu.configure(devtools={...}) config.

Lifecycle:
1. start_capture(page, context) — called BEFORE user test code runs
2. User test code runs, events accumulate
3. Query functions (devtoolsNetworkQuery, etc.) execute code against captured data
4. stop_capture(page) — called in teardown after user test code completes

Cookies + Storage are snapshot-based (on-demand at query time), no capture needed.
"""
from __future__ import annotations

import asyncio
import base64
import codecs
import logging
import time
from typing import Any
from urllib.parse import urlparse, parse_qs

from testmu import _configure
from testmu._helpers.devtools_types import (
    NetworkEntry, RequestTiming, ConsoleEntry, WebSocketFrame, WebSocketConnection,
    SSEMessage, SSEConnection,
)
from testmu._helpers.sse_parser import SSEWireParser

_log = logging.getLogger("testmu.devtools")

# ── In-memory capture stores ──

_network_entries: list[NetworkEntry] = []
_network_sequence: int = 0
_network_active: bool = False

_console_entries: list[ConsoleEntry] = []
_console_sequence: int = 0
_console_active: bool = False

# WebSocket capture
_ws_connections: list[WebSocketConnection] = []
_ws_active: bool = False
_ws_configured: bool = False          # True once WS capture was started this run
_ws_seq: int = 0                      # global monotonic across all connections
_ws_conn_counter: int = 0             # connection-id allocator
_ws_by_id: dict[int, int] = {}        # id(ws) -> index into _ws_connections
_ws_frame_counter: dict[str, int] = {}  # connection_id -> per-conn frame_index

# SSE capture (CDP-based, Chromium-only). Unlike WS (page.on, auto-managed),
# CDP sessions are NOT auto-managed — we keep a page→CDPSession registry and
# explicitly detach each on stop. Per-request maps are session-local (requestId
# collides across CDP targets); the connection list + counters are global.
_sse_connections: list[SSEConnection] = []
_sse_active: bool = False
_sse_configured: bool = False          # True once SSE capture was started this run
_sse_seq: int = 0                      # global monotonic across all connections
_sse_conn_counter: int = 0             # connection-id allocator
_sse_msg_counter: dict[str, int] = {}  # connection_id -> per-conn message_index
_sse_sessions: dict[int, Any] = {}     # id(page) -> CDPSession (the registry)
_sse_tasks: set = set()                # pending scheduled tasks (response handlers + popup attach)

_MAX_NETWORK_ENTRIES = 5000
_MAX_BODY_SIZE = 65536
_MAX_CONSOLE_ENTRIES = 50000
_MAX_WS_CONNECTIONS = 256
_MAX_WS_FRAMES_PER_CONN = 2000
_WS_PRESERVE_FIRST_N = 20
_MAX_SSE_CONNECTIONS = 256
_MAX_SSE_MESSAGES_PER_CONN = 2000
_SSE_PRESERVE_FIRST_N = 20
# Raw-byte budget for a binary frame so its base64 stays <= _MAX_BODY_SIZE chars and
# decodes cleanly (multiple of 3 → no mid-stream base64 padding). (65536//4)*3 = 49152.
_MAX_WS_RAW_BUDGET = (_MAX_BODY_SIZE // 4) * 3

_TEXT_CONTENT_TYPES = ("json", "text", "xml", "html", "javascript", "css", "svg")

# ── References to page/context for snapshot-based queries ──

_page_ref: Any = None
_context_ref: Any = None
_page_listener_active: bool = False  # True once context.on("page") is wired this run
_extra_pages: list = []              # tabs opened mid-run that got capture listeners


# ── Public API ──

async def start_capture(page, context) -> None:
    """Start devtools capture based on configure(devtools={...}).

    Called by _session.py after page creation, before user code.
    """
    global _page_ref, _context_ref
    _page_ref = page
    _context_ref = context

    if _configure.get("clipboard"):
        global _clipboard_store
        from testmu._helpers.clipboard import ClipboardStore, install_clipboard
        _clipboard_store = ClipboardStore()
        await install_clipboard(context, _clipboard_store)
        _log.info("Virtual clipboard installed")

    devtools_cfg = _configure.get("devtools") or {}
    if not devtools_cfg:
        return

    if devtools_cfg.get("network"):
        _start_network_capture(page)

    if devtools_cfg.get("console"):
        _start_console_capture(page)

    if devtools_cfg.get("websocket"):
        _start_websocket_capture(page)

    if devtools_cfg.get("sse"):
        # SSE rides a CDP session (Chromium-only); attach is async. The
        # non-Chromium hard-fail lives in _session.py BEFORE this runs.
        await _start_sse_capture_initial(page)

    # Page-based captures (network/console/websocket/sse) only listen on the page
    # they were attached to. Re-arm them on tabs opened later (window.open,
    # target=_blank) via the context's "page" event — otherwise those tabs are
    # silently uncaptured. (performance/clipboard ride context init scripts and
    # already cover every page.)
    if any(devtools_cfg.get(k) for k in ("network", "console", "websocket", "sse")):
        _attach_context_page_listener(context)

    if devtools_cfg.get("performance"):
        await _install_performance(context)

    enabled = [k for k, v in devtools_cfg.items() if v]
    if enabled:
        _log.info("DevTools capture started: %s", ", ".join(enabled))


def stop_capture(page) -> None:
    """Stop capture and detach listeners. Stores remain readable for queries.

    SSE CDP sessions are detached asynchronously by stop_sse_capture(); this
    sync stop only flips _sse_active off (so handlers short-circuit) and removes
    the context.on('page') listener first, so no new popup-attach task can be
    scheduled before stop_sse_capture() drains and detaches."""
    global _network_active, _console_active, _ws_active, _sse_active
    _detach_context_page_listener()
    if _network_active:
        _stop_network_capture(page)
    if _console_active:
        _stop_console_capture(page)
    if _ws_active:
        _stop_websocket_capture(page)
    _sse_active = False
    # The per-type stops above only detach the initial page; also detach the
    # tabs opened mid-run so no listener outlives the capture session.
    _detach_extra_pages()


# ── New-page propagation — capture tabs opened after start_capture ──

def _attach_context_page_listener(context) -> None:
    """Wire context.on("page", ...) once so tabs opened after start_capture
    inherit the active capture listeners."""
    global _page_listener_active
    if _page_listener_active or context is None:
        return
    try:
        context.on("page", _on_new_page)
        _page_listener_active = True
    except Exception:
        pass


def _detach_context_page_listener() -> None:
    global _page_listener_active
    if _page_listener_active and _context_ref is not None:
        try:
            _context_ref.remove_listener("page", _on_new_page)
        except Exception:
            pass
    _page_listener_active = False


def _detach_extra_pages() -> None:
    """Remove capture listeners from tabs opened mid-run. Removing a listener
    that was never attached (e.g. only network was enabled) is a safe no-op."""
    for p in _extra_pages:
        _detach_network_listeners(p)
        _detach_console_listeners(p)
        _detach_websocket_listeners(p)
    _extra_pages.clear()


def _on_new_page(page) -> None:
    """Attach the currently-active capture listeners to a newly opened page.
    Attach-only — never resets accumulated state (which the _start_* helpers do).
    Each capture type is guarded independently so one failure can't skip the rest."""
    attached = False
    for active, attach in (
        (_network_active, _attach_network_listeners),
        (_console_active, _attach_console_listeners),
        (_ws_active, _attach_websocket_listeners),
    ):
        if not active:
            continue
        try:
            attach(page)
            attached = True
        except Exception:
            pass
    # SSE attach is async (own CDP session) — schedule it as a tracked task.
    # The session is registered in _sse_sessions and detached by stop_sse_capture.
    if _sse_active:
        try:
            _schedule(_attach_sse_to_page(page))
        except Exception:
            pass
    if attached and page not in _extra_pages:
        _extra_pages.append(page)


def reset() -> None:
    """Reset all capture state (for test isolation)."""
    global _network_entries, _network_sequence, _network_active
    global _console_entries, _console_sequence, _console_active
    global _ws_connections, _ws_active, _ws_configured, _ws_seq, _ws_conn_counter
    global _ws_by_id, _ws_frame_counter
    global _sse_connections, _sse_active, _sse_configured, _sse_seq
    global _sse_conn_counter, _sse_msg_counter, _sse_sessions
    global _page_ref, _context_ref
    # Remove any live listeners on the (possibly reused) context/tabs before
    # dropping our refs, so a later start_capture can't double-register them.
    # _detach_context_page_listener() also clears _page_listener_active.
    _detach_context_page_listener()
    _detach_extra_pages()
    _network_entries = []
    _network_sequence = 0
    _network_active = False
    _console_entries = []
    _console_sequence = 0
    _console_active = False
    _ws_connections = []
    _ws_active = False
    _ws_configured = False
    _ws_seq = 0
    _ws_conn_counter = 0
    _ws_by_id = {}
    _ws_frame_counter = {}
    # SSE: synchronous best-effort reset for test isolation. Any live CDP
    # sessions should be detached via stop_sse_capture() in the async teardown;
    # here we drop refs (cancel pending tasks) so a fresh run starts clean.
    for _t in list(_sse_tasks):
        _t.cancel()
    _sse_tasks.clear()
    _sse_connections = []
    _sse_active = False
    _sse_configured = False
    _sse_seq = 0
    _sse_conn_counter = 0
    _sse_msg_counter = {}
    _sse_sessions = {}
    _page_ref = None
    _context_ref = None


# ── Network capture ──

def _start_network_capture(page) -> None:
    global _network_entries, _network_sequence, _network_active
    _network_entries = []
    _network_sequence = 0
    _network_active = True
    _attach_network_listeners(page)


def _attach_network_listeners(page) -> None:
    page.on("request", _on_request)
    page.on("response", _on_response)
    page.on("requestfinished", _on_request_finished)
    page.on("requestfailed", _on_request_failed)


def _detach_network_listeners(page) -> None:
    try:
        page.remove_listener("request", _on_request)
        page.remove_listener("response", _on_response)
        page.remove_listener("requestfinished", _on_request_finished)
        page.remove_listener("requestfailed", _on_request_failed)
    except Exception:
        pass


def _stop_network_capture(page) -> None:
    global _network_active
    _network_active = False
    _detach_network_listeners(page)


_pending_requests: dict[int, int] = {}


def _on_request(request) -> None:
    global _network_sequence
    if not _network_active:
        return
    parsed = urlparse(request.url)
    qp = {}
    for k, v in parse_qs(parsed.query).items():
        qp[k] = v[0] if len(v) == 1 else ",".join(v)

    # Playwright's `request.post_data` is a property that base64-decodes the
    # raw body and then `.decode()`-s it as UTF-8, so binary/gzipped POST
    # bodies (protobuf, multipart, compressed payloads) raise UnicodeDecodeError
    # there. `getattr(..., None)` does NOT shield us — the default is only used
    # for AttributeError — so the error would escape this event listener.
    # Treat any read failure as "no capturable body".
    try:
        post_data = getattr(request, "post_data", None)
    except Exception as exc:
        # Expected for binary/compressed bodies; debug-log so the dropped body
        # is diagnosable rather than silently invisible.
        _log.debug("network capture: skipping unreadable request body: %r", exc)
        post_data = None
    req_body = None
    req_body_truncated = False
    if post_data:
        if len(post_data) > _MAX_BODY_SIZE:
            req_body = post_data[:_MAX_BODY_SIZE]
            req_body_truncated = True
        else:
            req_body = post_data

    entry = NetworkEntry(
        id=f"req_{_network_sequence}",
        sequence=_network_sequence,
        method=request.method,
        url=request.url,
        domain=parsed.hostname or "",
        path=parsed.path or "/",
        query_params=qp,
        resource_type=getattr(request, "resource_type", "other"),
        request_headers=dict(getattr(request, "headers", {}) or {}),
        request_body=req_body,
        request_body_truncated=req_body_truncated,
        timing=RequestTiming(start_ms=time.time() * 1000),
    )
    _network_sequence += 1

    if len(_network_entries) >= _MAX_NETWORK_ENTRIES:
        # Evict oldest 10%
        evict_count = _MAX_NETWORK_ENTRIES // 10
        del _network_entries[:evict_count]

    idx = len(_network_entries)
    _network_entries.append(entry)
    _pending_requests[id(request)] = idx


async def _on_response(response) -> None:
    if not _network_active:
        return
    request = response.request
    idx = _pending_requests.get(id(request))
    if idx is None or idx >= len(_network_entries):
        return
    entry = _network_entries[idx]
    entry.response_status = response.status
    entry.response_headers = dict(getattr(response, "headers", {}) or {})

    content_type = entry.response_headers.get("content-type", "")
    # SSE responses (text/event-stream) are long-lived streams whose body()
    # never resolves until the stream closes — reading it here would hang the
    # capture. SSE is captured separately via CDP, so skip the body read.
    # Match before the generic "text" substring (which catches event-stream).
    if "text/event-stream" in content_type:
        entry.response_body = None
        entry.response_body_truncated = False
    elif any(t in content_type for t in _TEXT_CONTENT_TYPES):
        try:
            body_bytes = await response.body()
            body = body_bytes.decode("utf-8", errors="replace") if isinstance(body_bytes, bytes) else body_bytes
            if body and len(body) > _MAX_BODY_SIZE:
                entry.response_body = body[:_MAX_BODY_SIZE]
                entry.response_body_truncated = True
            else:
                entry.response_body = body
        except Exception:
            pass


def _on_request_finished(request) -> None:
    if not _network_active:
        return
    idx = _pending_requests.pop(id(request), None)
    if idx is not None and idx < len(_network_entries):
        entry = _network_entries[idx]
        if entry.timing:
            elapsed = time.time() * 1000 - entry.timing.start_ms
            entry.timing = RequestTiming(
                start_ms=entry.timing.start_ms,
                duration_ms=elapsed,
            )


def _on_request_failed(request) -> None:
    if not _network_active:
        return
    idx = _pending_requests.pop(id(request), None)
    if idx is not None and idx < len(_network_entries):
        entry = _network_entries[idx]
        entry.failed = True
        entry.failure_reason = request.failure or ""


# ── Console capture ─

_LEVEL_MAP = {"log": "log", "warning": "warning", "error": "error", "info": "info", "debug": "debug"}


def _start_console_capture(page) -> None:
    global _console_entries, _console_sequence, _console_active
    _console_entries = []
    _console_sequence = 0
    _console_active = True
    _attach_console_listeners(page)


def _attach_console_listeners(page) -> None:
    page.on("console", _on_console_message)
    page.on("pageerror", _on_page_error)


def _detach_console_listeners(page) -> None:
    try:
        page.remove_listener("console", _on_console_message)
        page.remove_listener("pageerror", _on_page_error)
    except Exception:
        pass


def _stop_console_capture(page) -> None:
    global _console_active
    _console_active = False
    _detach_console_listeners(page)


async def _on_console_message(msg) -> None:
    global _console_sequence
    if not _console_active:
        return
    level = _LEVEL_MAP.get(msg.type, "log")
    location = getattr(msg, "location", None) or {}

    try:
        parts = []
        for arg in msg.args:
            try:
                val = await arg.json_value()
                parts.append(str(val) if not isinstance(val, str) else val)
            except Exception:
                parts.append("<unresolved>")
        text = " ".join(parts) if parts else msg.text
    except Exception:
        text = msg.text

    entry = ConsoleEntry(
        sequence=_console_sequence,
        level=level,
        text=text,
        url=location.get("url", ""),
        line_number=location.get("lineNumber", 0),
        timestamp_ms=time.time() * 1000,
    )
    _console_sequence += 1
    if len(_console_entries) >= _MAX_CONSOLE_ENTRIES:
        evict_count = _MAX_CONSOLE_ENTRIES // 10
        del _console_entries[:evict_count]
    _console_entries.append(entry)


def _on_page_error(error) -> None:
    global _console_sequence
    if not _console_active:
        return
    entry = ConsoleEntry(
        sequence=_console_sequence,
        level="error",
        text=getattr(error, "message", str(error)),
        url="",
        line_number=0,
        timestamp_ms=time.time() * 1000,
        is_exception=True,
        stack_trace=getattr(error, "stack", None),
    )
    _console_sequence += 1
    if len(_console_entries) >= _MAX_CONSOLE_ENTRIES:
        evict_count = _MAX_CONSOLE_ENTRIES // 10
        del _console_entries[:evict_count]
    _console_entries.append(entry)


# ── WebSocket capture ──

def _ws_url(ws) -> str:
    """playwright-python exposes WebSocket.url as a property; tolerate a callable too."""
    u = getattr(ws, "url", "")
    return (u() if callable(u) else u) or ""


def _start_websocket_capture(page) -> None:
    global _ws_connections, _ws_active, _ws_configured, _ws_seq, _ws_conn_counter
    global _ws_by_id, _ws_frame_counter
    _ws_connections = []
    _ws_active = True
    _ws_configured = True
    _ws_seq = 0
    _ws_conn_counter = 0
    _ws_by_id = {}
    _ws_frame_counter = {}
    _attach_websocket_listeners(page)


def _attach_websocket_listeners(page) -> None:
    page.on("websocket", _on_websocket)


def _detach_websocket_listeners(page) -> None:
    try:
        page.remove_listener("websocket", _on_websocket)
    except Exception:
        pass


def _stop_websocket_capture(page) -> None:
    global _ws_active
    _ws_active = False
    _detach_websocket_listeners(page)


def _on_websocket(ws) -> None:
    global _ws_conn_counter
    if not _ws_active:
        return
    try:
        if len(_ws_connections) >= _MAX_WS_CONNECTIONS:
            _evict_oldest_closed_ws()
        url = _ws_url(ws)
        p = urlparse(url)
        conn = WebSocketConnection(
            connection_id=f"ws_{_ws_conn_counter}",
            url=url,
            domain=p.hostname or "",
            path=p.path or "/",
            opened_ts_ms=time.time() * 1000,
        )
        _ws_conn_counter += 1
        _ws_by_id[id(ws)] = len(_ws_connections)
        _ws_connections.append(conn)
    except Exception:
        return
    # Each frame/close/error handler wraps its own body in try/except so a raising
    # handler cannot propagate out of pyee and fail a later Playwright call.
    ws.on("framesent", lambda payload: _on_ws_frame(ws, "sent", payload))
    ws.on("framereceived", lambda payload: _on_ws_frame(ws, "received", payload))
    ws.on("close", lambda *a: _on_ws_close(ws))
    ws.on("socketerror", lambda err="": _on_ws_error(ws, err))


def _on_ws_frame(ws, direction: str, payload) -> None:
    global _ws_seq
    if not _ws_active:
        return
    try:
        idx = _ws_by_id.get(id(ws))
        if idx is None or idx >= len(_ws_connections):
            return
        conn = _ws_connections[idx]
        is_binary = isinstance(payload, (bytes, bytearray))
        if is_binary:
            # Truncate raw bytes before base64 so the stored payload stays within the
            # cap and decodes cleanly (budget is a multiple of 3 → no mid-stream padding);
            # `truncated` reflects the raw length.
            raw = bytes(payload)
            truncated = len(raw) > _MAX_WS_RAW_BUDGET
            text = base64.b64encode(raw[:_MAX_WS_RAW_BUDGET]).decode()
        else:
            text = str(payload)
            truncated = len(text) > _MAX_BODY_SIZE
            if truncated:
                text = text[:_MAX_BODY_SIZE]
        cid = conn.connection_id
        fidx = _ws_frame_counter.get(cid, 0)
        _ws_frame_counter[cid] = fidx + 1
        frame = WebSocketFrame(
            connection_id=cid,
            direction=direction,
            payload=text,
            is_binary=is_binary,
            truncated=truncated,
            ts_ms=time.time() * 1000,
            seq=_ws_seq,
            frame_index=fidx,
        )
        _ws_seq += 1
        _append_ws_frame(conn, frame)
    except Exception:
        pass


def _on_ws_close(ws) -> None:
    try:
        idx = _ws_by_id.get(id(ws))
        if idx is not None and idx < len(_ws_connections):
            _ws_connections[idx].closed_ts_ms = time.time() * 1000
    except Exception:
        pass


def _on_ws_error(ws, err="") -> None:
    try:
        idx = _ws_by_id.get(id(ws))
        if idx is not None and idx < len(_ws_connections):
            _ws_connections[idx].error = str(err)
    except Exception:
        pass


def _append_ws_frame(conn, frame) -> None:
    # Per-connection ring with first-N preserved; frame_index stays monotonic
    # via _ws_frame_counter (NOT len(frames), which repeats after eviction).
    if len(conn.frames) >= _MAX_WS_FRAMES_PER_CONN:
        drop_at = _WS_PRESERVE_FIRST_N
        if drop_at < len(conn.frames):
            del conn.frames[drop_at]
            conn.dropped_frames += 1
    conn.frames.append(frame)


def _evict_oldest_closed_ws() -> None:
    """Connection-count cap: evict the oldest CLOSED connection first; if none
    closed, drop the oldest. Re-index _ws_by_id around the removal and drop the
    evicted connection's frame counter so it doesn't leak."""
    global _ws_connections, _ws_by_id
    for i, c in enumerate(_ws_connections):
        if c.closed_ts_ms is not None:
            _ws_frame_counter.pop(c.connection_id, None)
            del _ws_connections[i]
            _ws_by_id = {k: (v - 1 if v > i else v) for k, v in _ws_by_id.items() if v != i}
            return
    if _ws_connections:
        _ws_frame_counter.pop(_ws_connections[0].connection_id, None)
        del _ws_connections[0]
        _ws_by_id = {k: v - 1 for k, v in _ws_by_id.items() if v != 0}


class _WsConnectionsAdapter:
    """Read-only view exposing `._connections` for devtools_network_query(ws_log=...).
    Shared by websocket_log() and the query wrapper."""

    def __init__(self, connections):
        self._connections = connections


def websocket_log():
    """Accessor exposing ._connections so generated test code can call
    devtools_network_query(code, network_log(), ws_log=websocket_log())."""
    return _WsConnectionsAdapter(_ws_connections)


# ── SSE capture (CDP, Chromium-only) ──

def _schedule(coro):
    """Schedule a coroutine as a tracked task so teardown can drain it. The task
    removes itself from the set on completion to keep the set bounded."""
    t = asyncio.ensure_future(coro)
    _sse_tasks.add(t)
    t.add_done_callback(_sse_tasks.discard)
    return t


def _norm_sse_event(name) -> str | None:
    # CDP eventName "" or "message" -> None (default event type).
    return None if (name or "") in ("", "message") else name


def _is_event_stream(resp: dict) -> bool:
    mime = (resp.get("mimeType") or "").split(";")[0].strip().lower()
    if mime == "text/event-stream":
        return True
    headers = resp.get("headers") or {}
    ct = headers.get("content-type") or headers.get("Content-Type") or ""
    return "text/event-stream" in ct.lower()


def _alloc_sse_conn(url: str, transport: str) -> SSEConnection:
    global _sse_conn_counter
    if len(_sse_connections) >= _MAX_SSE_CONNECTIONS:
        _evict_oldest_closed_sse()
    p = urlparse(url or "")
    conn = SSEConnection(
        connection_id=f"sse_{_sse_conn_counter}",
        url=url or "",
        domain=p.hostname or "",
        path=p.path or "/",
        opened_ts_ms=time.time() * 1000,
        transport=transport,
    )
    _sse_conn_counter += 1
    _sse_connections.append(conn)
    return conn


def _append_sse_message(conn, msg) -> None:
    # Per-connection ring with first-N preserved; message_index stays monotonic
    # via _sse_msg_counter (NOT len(messages), which repeats after eviction).
    if len(conn.messages) >= _MAX_SSE_MESSAGES_PER_CONN:
        drop_at = _SSE_PRESERVE_FIRST_N
        if drop_at < len(conn.messages):
            del conn.messages[drop_at]
            conn.dropped_messages += 1
    conn.messages.append(msg)


def _evict_oldest_closed_sse() -> None:
    """Connection-count cap: evict the oldest CLOSED connection first; if none
    closed, drop the oldest. Session request-maps hold object refs (not indices),
    so no re-indexing is needed; just drop the evicted conn's message counter."""
    global _sse_connections
    for i, c in enumerate(_sse_connections):
        if c.closed_ts_ms is not None:
            _sse_msg_counter.pop(c.connection_id, None)
            del _sse_connections[i]
            return
    if _sse_connections:
        _sse_msg_counter.pop(_sse_connections[0].connection_id, None)
        del _sse_connections[0]


def _emit_sse(conn, ev: dict, transport: str) -> None:
    global _sse_seq
    if not _sse_active:
        return
    try:
        data = ev.get("data", "") or ""
        truncated = bool(ev.get("truncated")) or len(data) > _MAX_BODY_SIZE
        data = data[:_MAX_BODY_SIZE]
        cid = conn.connection_id
        midx = _sse_msg_counter.get(cid, 0)
        _sse_msg_counter[cid] = midx + 1
        msg = SSEMessage(
            connection_id=cid,
            data=data,
            event=ev.get("event"),
            id=ev.get("id"),
            retry=ev.get("retry"),
            transport=transport,
            truncated=truncated,
            ts_ms=time.time() * 1000,
            seq=_sse_seq,
            message_index=midx,
        )
        _sse_seq += 1
        _append_sse_message(conn, msg)
    except Exception:
        pass


async def _start_sse_capture(page):
    """Create a CDP session on `page`, wire SSE handlers, register it in the
    page→session registry, and return the session. Handlers close over per-session
    request maps (requestId collides across CDP targets)."""
    cdp = await page.context.new_cdp_session(page)
    await cdp.send("Network.enable")

    streams: dict = {}   # requestId -> (conn, SSEWireParser, incremental decoder, transport)  [fetch/xhr]
    native: dict = {}    # requestId -> conn                                                    [EventSource]

    def _get_native_conn(rid, url=""):
        conn = native.get(rid)
        if conn is None:
            conn = _alloc_sse_conn(url, "eventsource")
            native[rid] = conn
        elif url and not conn.url:
            conn.url = url
            p = urlparse(url)
            conn.domain = p.hostname or ""
            conn.path = p.path or "/"
        return conn

    def _on_event_source_message(p):
        if not _sse_active:
            return
        try:
            conn = _get_native_conn(p.get("requestId"))
            _emit_sse(conn, {
                "event": _norm_sse_event(p.get("eventName")),
                "data": p.get("data", ""),
                "id": p.get("eventId") or None,
                "retry": None,
            }, "eventsource")
        except Exception:
            pass

    async def _on_response(p):
        if not _sse_active:
            return
        try:
            resp = p.get("response") or {}
            if not _is_event_stream(resp):
                return
            rid = p.get("requestId")
            rtype = p.get("type") or "Other"
            if rtype == "EventSource":
                # Native EventSource is pre-parsed; eventSourceMessageReceived
                # covers it. Pre-create the connection so a zero-message stream
                # still shows up. NEVER stream it (would double-count).
                _get_native_conn(rid, resp.get("url", ""))
                return
            transport = rtype.lower()
            conn = _alloc_sse_conn(resp.get("url", ""), transport)
            # NOT-yet-primed: dataReceived arriving during the streamResourceContent
            # await is queued (not fed) so bufferedData (earlier bytes) parses first —
            # ordering must not rely on event-loop scheduling (a buffered burst on
            # connect would otherwise corrupt the parse).
            entry = {
                "conn": conn,
                "parser": SSEWireParser(),
                "dec": codecs.getincrementaldecoder("utf-8")(),
                "transport": transport,
                "primed": False,
                "pending": [],
            }
            streams[rid] = entry
            try:
                res = await cdp.send("Network.streamResourceContent", {"requestId": rid})
                buf = (res or {}).get("bufferedData")
            except Exception:
                buf = None
            if buf:
                for ev in entry["parser"].feed(entry["dec"].decode(base64.b64decode(buf))):
                    _emit_sse(conn, ev, transport)
            for chunk in entry["pending"]:
                for ev in entry["parser"].feed(entry["dec"].decode(base64.b64decode(chunk))):
                    _emit_sse(conn, ev, transport)
            entry["pending"] = []
            entry["primed"] = True
        except Exception:
            pass

    def _on_data(p):
        if not _sse_active:
            return
        try:
            rid = p.get("requestId")
            entry = streams.get(rid)
            if entry is None:
                return
            b64 = p.get("data")
            if not b64:
                return
            if not entry["primed"]:
                entry["pending"].append(b64)
                return
            for ev in entry["parser"].feed(entry["dec"].decode(base64.b64decode(b64))):
                _emit_sse(entry["conn"], ev, entry["transport"])
        except Exception:
            pass

    def _mark_closed(rid, error=None):
        try:
            entry = streams.get(rid)
            conn = entry["conn"] if entry else native.get(rid)
            if conn is None:
                return
            conn.closed_ts_ms = time.time() * 1000
            if error:
                conn.error = str(error)
        except Exception:
            pass

    cdp.on("Network.eventSourceMessageReceived", _on_event_source_message)
    cdp.on("Network.responseReceived", lambda p: _schedule(_on_response(p)))
    cdp.on("Network.dataReceived", _on_data)
    cdp.on("Network.loadingFinished", lambda p: _mark_closed(p.get("requestId")))
    cdp.on("Network.loadingFailed", lambda p: _mark_closed(p.get("requestId"), error=p.get("errorText")))

    _sse_sessions[id(page)] = cdp
    return cdp


def _start_sse_capture_initial(page):
    """Reset SSE state, mark active/configured, and return the coroutine that
    attaches the primary page's CDP session. Mirrors _start_websocket_capture's
    state reset but the attach is async."""
    global _sse_connections, _sse_active, _sse_configured, _sse_seq
    global _sse_conn_counter, _sse_msg_counter, _sse_sessions
    _sse_connections = []
    _sse_active = True
    _sse_configured = True
    _sse_seq = 0
    _sse_conn_counter = 0
    _sse_msg_counter = {}
    _sse_sessions = {}
    return _start_sse_capture(page)


async def _attach_sse_to_page(page):
    """Popup attach: a tab opened after start_capture gets its own CDP session."""
    try:
        await _start_sse_capture(page)
    except Exception:
        pass


async def stop_sse_capture() -> None:
    """Async SSE teardown: stop handlers, drain pending tasks, detach every CDP
    session. The context.on('page') listener is removed by the sync stop_capture
    BEFORE this runs, so no new popup-attach task can be scheduled mid-teardown."""
    global _sse_active
    _sse_active = False
    # Drain scheduled response/attach tasks so none touches a detached session.
    pending = [t for t in list(_sse_tasks) if not t.done()]
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)
    for cdp in list(_sse_sessions.values()):
        try:
            await cdp.detach()
        except Exception:
            pass
    _sse_sessions.clear()


class _SseConnectionsAdapter:
    """Read-only view exposing `._connections` for devtools_network_query(sse_log=...).
    Shared by sse_log() and the query wrapper."""

    def __init__(self, connections):
        self._connections = connections


def sse_log():
    """Accessor exposing ._connections so generated test code can call
    devtools_network_query(code, network_log(), sse_log=sse_log())."""
    return _SseConnectionsAdapter(_sse_connections)


# ── Performance (web-vitals init script injection) ──

_WEB_VITALS_INIT_SCRIPT = (
    # Vendored web-vitals v4 IIFE (https://unpkg.com/web-vitals@4/dist/web-vitals.iife.js)
    """var webVitals=function(e){"use strict";var n,t,r,i,o,a=-1,c=function(e){addEventListener("pageshow",(function(n){n.persisted&&(a=n.timeStamp,e(n))}),!0)},u=function(){var e=self.performance&&performance.getEntriesByType&&performance.getEntriesByType("navigation")[0];if(e&&e.responseStart>0&&e.responseStart<performance.now())return e},s=function(){var e=u();return e&&e.activationStart||0},f=function(e,n){var t=u(),r="navigate";a>=0?r="back-forward-cache":t&&(document.prerendering||s()>0?r="prerender":document.wasDiscarded?r="restore":t.type&&(r=t.type.replace(/_/g,"-")));return{name:e,value:void 0===n?-1:n,rating:"good",delta:0,entries:[],id:"v4-".concat(Date.now(),"-").concat(Math.floor(8999999999999*Math.random())+1e12),navigationType:r}},d=function(e,n,t){try{if(PerformanceObserver.supportedEntryTypes.includes(e)){var r=new PerformanceObserver((function(e){Promise.resolve().then((function(){n(e.getEntries())}))}));return r.observe(Object.assign({type:e,buffered:!0},t||{})),r}}catch(e){}},l=function(e,n,t,r){var i,o;return function(a){n.value>=0&&(a||r)&&((o=n.value-(i||0))||void 0===i)&&(i=n.value,n.delta=o,n.rating=function(e,n){return e>n[1]?"poor":e>n[0]?"needs-improvement":"good"}(n.value,t),e(n))}},p=function(e){requestAnimationFrame((function(){return requestAnimationFrame((function(){return e()}))}))},v=function(e){document.addEventListener("visibilitychange",(function(){"hidden"===document.visibilityState&&e()}))},m=function(e){var n=!1;return function(){n||(e(),n=!0)}},h=-1,g=function(){return"hidden"!==document.visibilityState||document.prerendering?1/0:0},T=function(e){"hidden"===document.visibilityState&&h>-1&&(h="visibilitychange"===e.type?e.timeStamp:0,E())},y=function(){addEventListener("visibilitychange",T,!0),addEventListener("prerenderingchange",T,!0)},E=function(){removeEventListener("visibilitychange",T,!0),removeEventListener("prerenderingchange",T,!0)},C=function(){return h<0&&(h=g(),y(),c((function(){setTimeout((function(){h=g(),y()}),0)}))),{get firstHiddenTime(){return h}}},L=function(e){document.prerendering?addEventListener("prerenderingchange",(function(){return e()}),!0):e()},S=[1800,3e3],b=function(e,n){n=n||{},L((function(){var t,r=C(),i=f("FCP"),o=d("paint",(function(e){e.forEach((function(e){"first-contentful-paint"===e.name&&(o.disconnect(),e.startTime<r.firstHiddenTime&&(i.value=Math.max(e.startTime-s(),0),i.entries.push(e),t(!0)))}))}));o&&(t=l(e,i,S,n.reportAllChanges),c((function(r){i=f("FCP"),t=l(e,i,S,n.reportAllChanges),p((function(){i.value=performance.now()-r.timeStamp,t(!0)}))})))}))},w=[.1,.25],I=0,P=1/0,A=0,F=function(e){e.forEach((function(e){e.interactionId&&(P=Math.min(P,e.interactionId),A=Math.max(A,e.interactionId),I=A?(A-P)/7+1:0)}))},M=function(){return n?I:performance.interactionCount||0},k=function(){"interactionCount"in performance||n||(n=d("event",F,{type:"event",buffered:!0,durationThreshold:0}))},D=[],B=new Map,R=0,x=function(){var e=Math.min(D.length-1,Math.floor((M()-R)/50));return D[e]},H=[],N=function(e){if(H.forEach((function(n){return n(e)})),e.interactionId||"first-input"===e.entryType){var n=D[D.length-1],t=B.get(e.interactionId);if(t||D.length<10||e.duration>n.latency){if(t)e.duration>t.latency?(t.entries=[e],t.latency=e.duration):e.duration===t.latency&&e.startTime===t.entries[0].startTime&&t.entries.push(e);else{var r={id:e.interactionId,latency:e.duration,entries:[e]};B.set(r.id,r),D.push(r)}D.sort((function(e,n){return n.latency-e.latency})),D.length>10&&D.splice(10).forEach((function(e){return B.delete(e.id)}))}}},q=function(e){var n=self.requestIdleCallback||self.setTimeout,t=-1;return e=m(e),"hidden"===document.visibilityState?e():(t=n(e),v(e)),t},O=[200,500],j=[2500,4e3],V={},_=[800,1800],z=function e(n){document.prerendering?L((function(){return e(n)})):"complete"!==document.readyState?addEventListener("load",(function(){return e(n)}),!0):setTimeout(n,0)},G={passive:!0,capture:!0},J=new Date,K=function(e,n){t||(t=n,r=e,i=new Date,W(removeEventListener),Q())},Q=function(){if(r>=0&&r<i-J){var e={entryType:"first-input",name:t.type,target:t.target,cancelable:t.cancelable,startTime:t.timeStamp,processingStart:t.timeStamp+r};o.forEach((function(n){n(e)})),o=[]}},U=function(e){if(e.cancelable){var n=(e.timeStamp>1e12?new Date:performance.now())-e.timeStamp;"pointerdown"==e.type?function(e,n){var t=function(){K(e,n),i()},r=function(){i()},i=function(){removeEventListener("pointerup",t,G),removeEventListener("pointercancel",r,G)};addEventListener("pointerup",t,G),addEventListener("pointercancel",r,G)}(n,e):K(n,e)}},W=function(e){["mousedown","keydown","touchstart","pointerdown"].forEach((function(n){return e(n,U,G)}))},X=[100,300];return e.CLSThresholds=w,e.FCPThresholds=S,e.FIDThresholds=X,e.INPThresholds=O,e.LCPThresholds=j,e.TTFBThresholds=_,e.onCLS=function(e,n){n=n||{},b(m((function(){var t,r=f("CLS",0),i=0,o=[],a=function(e){e.forEach((function(e){if(!e.hadRecentInput){var n=o[0],t=o[o.length-1];i&&e.startTime-t.startTime<1e3&&e.startTime-n.startTime<5e3?(i+=e.value,o.push(e)):(i=e.value,o=[e])}})),i>r.value&&(r.value=i,r.entries=o,t())},u=d("layout-shift",a);u&&(t=l(e,r,w,n.reportAllChanges),v((function(){a(u.takeRecords()),t(!0)})),c((function(){i=0,r=f("CLS",0),t=l(e,r,w,n.reportAllChanges),p((function(){return t()}))})),setTimeout(t,0))})))},e.onFCP=b,e.onFID=function(e,n){n=n||{},L((function(){var i,a=C(),u=f("FID"),s=function(e){e.startTime<a.firstHiddenTime&&(u.value=e.processingStart-e.startTime,u.entries.push(e),i(!0))},p=function(e){e.forEach(s)},h=d("first-input",p);i=l(e,u,X,n.reportAllChanges),h&&(v(m((function(){p(h.takeRecords()),h.disconnect()}))),c((function(){var a;u=f("FID"),i=l(e,u,X,n.reportAllChanges),o=[],r=-1,t=null,W(addEventListener),a=s,o.push(a),Q()})))}))},e.onINP=function(e,n){"PerformanceEventTiming"in self&&"interactionId"in PerformanceEventTiming.prototype&&(n=n||{},L((function(){var t;k();var r,i=f("INP"),o=function(e){q((function(){e.forEach(N);var n=x();n&&n.latency!==i.value&&(i.value=n.latency,i.entries=n.entries,r())}))},a=d("event",o,{durationThreshold:null!==(t=n.durationThreshold)&&void 0!==t?t:40});r=l(e,i,O,n.reportAllChanges),a&&(a.observe({type:"first-input",buffered:!0}),v((function(){o(a.takeRecords()),r(!0)})),c((function(){R=M(),D.length=0,B.clear(),i=f("INP"),r=l(e,i,O,n.reportAllChanges)})))})))},e.onLCP=function(e,n){n=n||{},L((function(){var t,r=C(),i=f("LCP"),o=function(e){n.reportAllChanges||(e=e.slice(-1)),e.forEach((function(e){e.startTime<r.firstHiddenTime&&(i.value=Math.max(e.startTime-s(),0),i.entries=[e],t())}))},a=d("largest-contentful-paint",o);if(a){t=l(e,i,j,n.reportAllChanges);var u=m((function(){V[i.id]||(o(a.takeRecords()),a.disconnect(),V[i.id]=!0,t(!0))}));["keydown","click"].forEach((function(e){addEventListener(e,(function(){return q(u)}),{once:!0,capture:!0})})),v(u),c((function(r){i=f("LCP"),t=l(e,i,j,n.reportAllChanges),p((function(){i.value=performance.now()-r.timeStamp,V[i.id]=!0,t(!0)}))}))}}))},e.onTTFB=function(e,n){n=n||{};var t=f("TTFB"),r=l(e,t,_,n.reportAllChanges);z((function(){var i=u();i&&(t.value=Math.max(i.responseStart-s(),0),t.entries=[i],r(!0),c((function(){t=f("TTFB",0),(r=l(e,t,_,n.reportAllChanges))(!0)})))}))},e}({});"""
    "\n"
    # Glue: wire web-vitals callbacks into window.__v16_perf
    """window.__v16_perf = {lcp: null, cls: null, fcp: null, inp: null, ttfb: null};
webVitals.onLCP(m => { window.__v16_perf.lcp = m.value; }, {reportAllChanges: true});
webVitals.onCLS(m => { window.__v16_perf.cls = m.value; }, {reportAllChanges: true});
webVitals.onINP(m => { window.__v16_perf.inp = m.value; }, {reportAllChanges: true});
webVitals.onFCP(m => { window.__v16_perf.fcp = m.value; }, {reportAllChanges: true});
webVitals.onTTFB(m => { window.__v16_perf.ttfb = m.value; }, {reportAllChanges: true});
"""
)


async def _install_performance(context) -> None:
    """Install web-vitals v4 init script on context (covers all pages)."""
    await context.add_init_script(_WEB_VITALS_INIT_SCRIPT)


# ── Query wrappers (single-arg, called by generated test code) ──

async def devtoolsNetworkQuery(code: str) -> str:
    """Execute Python code against captured NetworkLog. Single-arg wrapper.

    Builds ws_log / sse_log independently of each other so a query can read
    network only, +ws, +sse, or all three. When neither was configured the call
    is the exact 2-arg form (network-only), byte-identical to before."""
    from testmu._helpers.devtools_network import devtools_network_query

    class _StoreAdapter:
        def __init__(self, entries):
            self._entries = entries

    store = _StoreAdapter(_network_entries)
    kwargs: dict = {}
    if _ws_configured:
        kwargs["ws_log"] = _WsConnectionsAdapter(_ws_connections)
    if _sse_configured:
        kwargs["sse_log"] = _SseConnectionsAdapter(_sse_connections)
    result = devtools_network_query(code, store, **kwargs)
    return result.value if result.success else ""


async def devtoolsConsoleQuery(code: str) -> str:
    """Execute Python code against captured ConsoleLog. Single-arg wrapper."""
    from testmu._helpers.devtools_console import devtools_console_query

    class _StoreAdapter:
        def __init__(self, entries):
            self._entries = entries

    store = _StoreAdapter(_console_entries)
    result = devtools_console_query(code, store)
    return result.value if result.success else ""


async def devtoolsCookiesQuery(code: str) -> str:
    """Snapshot cookies, then execute Python code against them."""
    from testmu._helpers.devtools_cookies import devtools_cookies_query
    from testmu._helpers.devtools_types import CookieEntry

    # Snapshot cookies from context at query time
    raw_cookies = []
    if _context_ref:
        raw_cookies = await _context_ref.cookies()

    entries = [
        CookieEntry(
            name=c.get("name", ""),
            value=c.get("value", ""),
            domain=c.get("domain", ""),
            path=c.get("path", "/"),
            expires=c.get("expires", -1),
            http_only=c.get("httpOnly", False),
            secure=c.get("secure", False),
            same_site=c.get("sameSite", "None"),
        )
        for c in raw_cookies
    ]

    class _StoreAdapter:
        def __init__(self, entries):
            self._entries = entries

    store = _StoreAdapter(entries)
    result = devtools_cookies_query(code, store)
    return result.value if result.success else ""


async def devtoolsStorageQuery(code: str) -> str:
    """Snapshot localStorage, then execute Python code against it."""
    from testmu._helpers.devtools_storage import devtools_storage_query

    # Snapshot localStorage from page at query time
    storage_data = {}
    if _page_ref:
        try:
            storage_data = await _page_ref.evaluate("() => { const s = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); s[k] = localStorage.getItem(k); } return s; }")
        except Exception:
            pass

    class _StoreAdapter:
        def __init__(self, data):
            self._data = data
        def all(self):
            return dict(self._data)

    store = _StoreAdapter(storage_data)
    result = devtools_storage_query(code, store)
    return result.value if result.success else ""


async def snapshotPerformanceTrace() -> str:
    """Snapshot Core Web Vitals from page."""
    if not _page_ref:
        return ""
    from testmu._helpers.devtools_performance import snapshotPerformanceTrace as _snapshot
    cwv = await _snapshot(_page_ref)
    # Return string representation for variable assignment
    parts = []
    if cwv.lcp_ms is not None:
        parts.append(f"LCP={cwv.lcp_ms:.0f}ms")
    if cwv.fcp_ms is not None:
        parts.append(f"FCP={cwv.fcp_ms:.0f}ms")
    if cwv.cls is not None:
        parts.append(f"CLS={cwv.cls:.3f}")
    if cwv.inp_ms is not None:
        parts.append(f"INP={cwv.inp_ms:.0f}ms")
    if cwv.ttfb_ms is not None:
        parts.append(f"TTFB={cwv.ttfb_ms:.0f}ms")
    return ", ".join(parts) if parts else ""


# ---------------------------------------------------------------------------
# Virtual clipboard (configure(clipboard=True)) — see _helpers/clipboard.py
# ---------------------------------------------------------------------------

_clipboard_store = None


def _require_clipboard():
    if _clipboard_store is None:
        raise RuntimeError(
            "Virtual clipboard not installed — call testmu.configure(clipboard=True)"
        )
    return _clipboard_store


async def clipboardWrite(text: str, html: str | None = None) -> None:
    """Write the virtual test clipboard (text/plain + optional text/html)."""
    _require_clipboard().write(text, html=html)


async def clipboardPaste() -> None:
    """Paste the virtual clipboard at the focused element of the active page."""
    from testmu._helpers.clipboard import paste_via_page
    store = _require_clipboard()
    if not _page_ref:
        raise RuntimeError("No active page for clipboardPaste()")
    await paste_via_page(_page_ref, store)


async def clipboardClear() -> None:
    """Clear the virtual test clipboard."""
    _require_clipboard().clear()


async def devtoolsClipboardQuery(code: str) -> str:
    """Execute Python query code against the virtual clipboard store."""
    from testmu._helpers.clipboard import devtools_clipboard_query
    result = devtools_clipboard_query(code, _require_clipboard())
    return result.value if result.success else ""
