"""V2 event streaming transport routes (thread-centric).

These routes implement the v2 event streaming protocol — see
:mod:`langgraph_api.event_streaming` for the session/normalizer layer that
shapes the wire events. Connections are scoped to a thread via the URL
path; there is no server-side session state across connections.

Endpoints:

* ``POST /threads/{thread_id}/stream/events`` — SSE stream with
  ``EventStreamRequest`` filter body. Each connection IS the subscription;
  closing the connection unsubscribes.
* ``POST /threads/{thread_id}/commands`` — JSON command request/response.
* ``WebSocket /threads/{thread_id}/stream/events`` — full-duplex commands and events.
  ``subscription.subscribe`` / ``subscription.unsubscribe`` manage
  subscriptions for the lifetime of the socket.
* ``WebSocket /threads/{thread_id}/runs/{run_id}/protocol`` — compatibility
  route that auto-binds to an existing run on connection.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections import deque
from typing import TYPE_CHECKING, Any
from uuid import uuid4

import orjson
import structlog
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.websockets import WebSocketDisconnect

from langgraph_api.event_streaming.service import ThreadRunManager
from langgraph_api.event_streaming.session import _is_supported_channel
from langgraph_api.event_streaming.types import ErrorResponse, Subscription
from langgraph_api.feature_flags import IS_POSTGRES_OR_GRPC_BACKEND
from langgraph_api.route import ApiRoute, ApiWebSocketRoute
from langgraph_api.serde import json_dumpb
from langgraph_api.sse import EventSourceResponse
from langgraph_api.utils import validate_uuid

if TYPE_CHECKING:
    from collections.abc import Mapping

    from starlette.requests import Request
    from starlette.websockets import WebSocket

if IS_POSTGRES_OR_GRPC_BACKEND:
    from langgraph_api.grpc.ops import Runs, Threads
else:
    from langgraph_runtime.ops import Runs, Threads

logger = structlog.stdlib.get_logger(__name__)


# Maximum number of recently-delivered ``event_id`` values an SSE
# connection remembers for dedup. The dedup window only needs to cover
# the brief race where a single event arrives both via the thread
# source consumer and via the session's send callback (subscription
# install handoff); after that, events flow through one path
# consistently. Cap chosen with ample headroom — a pathological
# replay storm of 2k events still fits in <50 KB of strings per
# connection, vs. the unbounded set this replaces.
_DELIVERED_DEDUP_WINDOW = 2048

# Final frame on SSE and WebSocket when the thread-stream consumer stops
# without being cancelled. A thread stream has no natural end, so that always
# means the read failed. The message is fixed because the exception text can
# carry raw backend errors; the consumer has already logged it.
_THREAD_STREAM_FAILED_DATA = json_dumpb(
    ErrorResponse(
        type="error",
        id=None,
        error="unknown_error",
        message="Thread event stream failed.",
    )
)


def _json_response(content: Any, *, status_code: int = 200) -> Response:
    """JSON response backed by the repo's orjson helper.

    Starlette's default ``JSONResponse`` uses stdlib ``json`` which cannot
    serialize ``UUID`` / ``datetime`` / ``bytes`` — values that regularly
    appear in command responses (e.g. ``run_id`` from ``create_valid_run``).
    Using ``json_dumpb`` matches the serialization used on the event
    stream and keeps the two surfaces consistent.
    """
    return Response(
        json_dumpb(content),
        status_code=status_code,
        media_type="application/json",
    )


def _make_manager(
    thread_id: str,
    send_event: Any = None,
    *,
    headers: Mapping[str, str] | None = None,
    replay_buffer: bool = True,
) -> ThreadRunManager:
    # Auth context is propagated via ``ApiRoute``'s ``with_user`` wrapper
    # — ops reads it off the context var, so we don't thread it through
    # the manager explicitly.
    return ThreadRunManager(
        thread_id=thread_id,
        runs=Runs,
        threads=Threads,
        send_event=send_event,
        headers=headers,
        replay_buffer=replay_buffer,
    )


# ---------------------------------------------------------------------------
# POST /threads/{thread_id}/stream/events — SSE event stream
# ---------------------------------------------------------------------------


async def _thread_events(request: Request) -> Response:
    """SSE stream scoped to a thread.
    ---
    summary: SSE stream scoped to a thread.
    description: |
        Body is an ``EventStreamRequest``:

            {
              "channels": ["values", "messages", ...],
              "namespaces": [["ns1"], ["ns2", "child"]],   // optional
              "depth": 2,                                     // optional
              "since": 42                                     // optional seq
            }

        On reconnect, clients pass the last ``seq`` they received as
        ``since`` in the body. Buffered events with ``seq > since`` are
        replayed before the stream goes live. The endpoint is POST-only, so
        browser-native ``EventSource`` auto-resume (``Last-Event-ID``)
        doesn't apply — clients drive resume explicitly via the body.

        The filter applies for the lifetime of the connection; closing the
        connection unsubscribes. No state is persisted server-side beyond the
        connection.

        If reading the thread's event stream fails, the server ends the
        stream with a final ``event: error`` frame carrying a protocol error
        (``"type": "error"``, ``"id": null``, ``"error": "unknown_error"``).

        A thread the caller isn't allowed to read returns 403 or 404 before
        the stream starts, and a malformed thread ID returns 422.
    """
    thread_id = request.path_params["thread_id"]
    thread_uuid = validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    try:
        body = orjson.loads(await request.body())
    except Exception:
        return _json_response({"detail": "Invalid JSON body"}, status_code=400)

    channels = body.get("channels") if isinstance(body, dict) else None
    if not isinstance(channels, list) or not channels:
        return _json_response(
            {"detail": "channels is required and must be a non-empty array"},
            status_code=400,
        )
    # Reject unknown channel names up front — otherwise the SSE stream
    # would stay open indefinitely with no events flowing, confusing
    # clients that expected a subscription-level error. Aligns the
    # HTTP endpoint with the ``subscription.subscribe`` command which
    # already short-circuits with ``invalid_argument``. ``custom:<name>``
    # passes through ``_is_supported_channel`` unchanged.
    bad: list[str] = []
    validated: list[str] = []
    for c in channels:
        if not isinstance(c, str):
            bad.append(repr(c))
            continue
        if not _is_supported_channel(c):
            bad.append(c)
            continue
        validated.append(c)
    if bad:
        return _json_response(
            {
                "detail": (
                    "channels contains unsupported entries: "
                    + ", ".join(bad[:5])
                    + ". Allowed: values, updates, messages, tools, custom, "
                    "lifecycle, input, tasks, or any `custom:<name>`."
                )
            },
            status_code=400,
        )
    channels = validated

    namespaces = body.get("namespaces") if isinstance(body, dict) else None
    if not isinstance(namespaces, list):
        namespaces = None
    else:
        # only accept list[list[str]]
        filtered_ns: list[list[str]] = []
        for ns in namespaces:
            if isinstance(ns, list) and all(isinstance(seg, str) for seg in ns):
                filtered_ns.append(ns)
        namespaces = filtered_ns or None

    depth = body.get("depth") if isinstance(body, dict) else None
    # ``bool`` is a subclass of ``int``, so a JSON ``"depth": false`` would
    # otherwise fall through as ``depth=0`` ("only the exact prefix
    # namespace, no deeper") and silently mute every nested-subgraph
    # event. Treat any non-int (including bool) as "no depth limit".
    if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
        depth = None

    raw_since = body.get("since") if isinstance(body, dict) else None
    # Reject ``bool`` explicitly — ``isinstance(True, int)`` is ``True``
    # so a JSON ``"since": true`` would otherwise pass as ``since=1``
    # and silently skip the first buffered event on reconnect.
    since: int | None = (
        raw_since
        if isinstance(raw_since, int)
        and not isinstance(raw_since, bool)
        and raw_since >= 0
        else None
    )

    # Checked here, before the 200, because clients retry a 200 that ends in
    # an error instead of giving up.
    auth_filters = await Threads.Stream.check_thread_stream_auth(thread_uuid)

    # Bounded LRU dedup: ``recent_eids`` is the eviction order, ``delivered``
    # is the O(1) membership view. When the deque hits its cap, the oldest
    # entry rolls off; we mirror that on ``delivered`` to keep them in sync.
    recent_eids: deque[str] = deque(maxlen=_DELIVERED_DEDUP_WINDOW)
    delivered: set[str] = set()
    pending_events: list[dict[str, Any]] = []
    flush_pending = asyncio.Event()

    async def on_event(event: dict[str, Any]) -> None:
        eid = event.get("event_id")
        if eid is None or eid in delivered:
            return
        # Guard against events with seq <= since slipping through (e.g.
        # events delivered via the session's send callback before the
        # subscription is installed with replay).
        if since is not None and event.get("seq", 0) <= since:
            return
        if len(recent_eids) == recent_eids.maxlen:
            delivered.discard(recent_eids[0])
        recent_eids.append(eid)
        delivered.add(eid)
        pending_events.append(event)
        flush_pending.set()

    # SSE never replays from the session's buffer: it has no subscribe or
    # reconnect commands, and ``start_thread_stream`` replays from the
    # thread's event stream.
    manager = _make_manager(thread_id, send_event=on_event, replay_buffer=False)

    filter_sub = Subscription(
        id=str(uuid4()),
        channels=set(channels),
        namespaces=namespaces,
        depth=depth,
        active=False,
    )
    await logger.adebug(
        "Installing event streaming subscription",
        thread_id=thread_id,
        subscription_id=filter_sub.id,
        channels=sorted(filter_sub.channels),
        depth=depth,
        since=since,
    )

    manager.install_subscription(filter_sub)
    # ``since`` is enforced by ``on_event`` above as a seq filter on
    # outbound events; the thread-level reader always replays from the
    # beginning so namespace-scoped projections see history. See
    # ``ThreadRunManager.start_thread_stream`` for the rationale.
    manager.start_thread_stream(auth_filters=auth_filters)

    async def body_iter():
        try:
            while True:
                # Race ``flush_pending`` against the thread-stream consumer
                # ending. If the consumer stops (its read failed or its
                # source ended), we want this loop to exit rather than
                # wedge forever waiting for events that will never arrive.
                flush_task = asyncio.create_task(flush_pending.wait())
                done_task = asyncio.create_task(manager.wait_for_thread_stream_end())
                try:
                    done, _pending = await asyncio.wait(
                        {flush_task, done_task},
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                finally:
                    for p in (flush_task, done_task):
                        if not p.done():
                            p.cancel()
                            with contextlib.suppress(asyncio.CancelledError, Exception):
                                await p
                stream_finished = done_task in done
                # Always drain whatever was buffered before exiting so a
                # final batch that arrived alongside the consumer's exit
                # still reaches the client.
                flush_pending.clear()
                events = pending_events[:]
                pending_events.clear()
                for event in events:
                    # The wire ``event_id`` (inside the JSON body) carries
                    # the durable upstream Redis stream entry id used by
                    # the client's ``seenEventIds`` for cross-session
                    # dedup. The SSE ``id:`` field carries the protocol
                    # ``seq`` (session-local monotonic int) so server
                    # logs and traces can correlate against the body
                    # ``since`` cursor a reconnecting client sends.
                    sse_id = event.get("seq")
                    method = event.get("method", "event")
                    yield (
                        method.encode() if isinstance(method, str) else b"event",
                        json_dumpb(event),
                        str(sse_id).encode() if isinstance(sse_id, int) else None,
                    )
                if stream_finished:
                    if manager.thread_stream_failed:
                        yield (b"error", _THREAD_STREAM_FAILED_DATA)
                    break
        finally:
            await manager.close()

    return EventSourceResponse(body_iter())


# ---------------------------------------------------------------------------
# POST /threads/{thread_id}/commands — JSON command
# ---------------------------------------------------------------------------


async def _thread_command(request: Request) -> Response:
    """Handle a single protocol command scoped to a thread.
    ---
    summary: Handle a single protocol command scoped to a thread.
    description: |
        Commands are stateless in the HTTP transport: a fresh manager is
        created, the command is dispatched, and results are returned. For
        ``run.start`` this creates/resumes a run; subsequent event streaming
        happens over a separate ``POST .../stream`` connection.
    """
    thread_id = request.path_params["thread_id"]
    try:
        payload = orjson.loads(await request.body())
    except Exception:
        return _json_response({"detail": "Invalid JSON body"}, status_code=400)

    if (
        not isinstance(payload, dict)
        or not isinstance(payload.get("id"), int)
        or not isinstance(payload.get("method"), str)
    ):
        await logger.awarning(
            "Rejected malformed event streaming command",
            thread_id=thread_id,
            payload_id=payload.get("id") if isinstance(payload, dict) else None,
            payload_method=payload.get("method") if isinstance(payload, dict) else None,
            payload_type=type(payload).__name__,
        )
        return _json_response(
            {
                "type": "error",
                "id": payload.get("id") if isinstance(payload, dict) else None,
                "error": "invalid_argument",
                "message": "Protocol commands must include an integer id and string method.",
            },
            status_code=400,
        )

    manager = _make_manager(thread_id, headers=request.headers)
    try:
        resp = await manager.handle_command(payload)
        return _json_response(resp)
    finally:
        # Commands that create runs (e.g. run.start) leave the run executing in
        # the background on the worker queue. Downstream clients observe it via
        # the thread-level ``POST .../stream/events`` source.
        await manager.close()


# ---------------------------------------------------------------------------
# WebSocket /threads/{thread_id}/stream/events
# ---------------------------------------------------------------------------


async def _close_for_failed_access_check(websocket: WebSocket, exc: Exception) -> None:
    if isinstance(exc, HTTPException) and exc.status_code < 500:
        await websocket.close(code=4000 + exc.status_code)
        return
    logger.exception("Thread stream access check failed")
    await websocket.send_text(_THREAD_STREAM_FAILED_DATA.decode())
    await websocket.close(code=1011, reason="thread stream ended")


async def _thread_websocket(websocket: WebSocket) -> None:
    """Full-duplex protocol connection scoped to a thread.

    Supports ``run.start``, ``input.respond``, ``subscription.subscribe``,
    ``subscription.unsubscribe``, ``agent.getTree``.

    A 4xx from the thread's access check closes the socket with 4000 plus the
    status (4403, 4422). A 404 can be a thread the client minted and has yet
    to create, so the socket then waits for a ``run.start``, which checks
    access like any run start, and closes with 4404 if another command comes
    first. Any other failure of the check, a 5xx included, gets the stream
    error frame and a 1011 close, as when the stream fails later.
    """
    thread_id = websocket.path_params["thread_id"]
    # Browsers report a refused upgrade only as a 1006 close, so accept first
    # to make the close code readable.
    await websocket.accept()
    try:
        thread_uuid = validate_uuid(thread_id, "Invalid thread ID: must be a UUID")
    except HTTPException as exc:
        await _close_for_failed_access_check(websocket, exc)
        return
    awaiting_thread = False
    auth_filters: Any = None
    try:
        auth_filters = await Threads.Stream.check_thread_stream_auth(thread_uuid)
    except Exception as exc:
        if not (isinstance(exc, HTTPException) and exc.status_code == 404):
            await _close_for_failed_access_check(websocket, exc)
            return
        awaiting_thread = True

    async def ws_send_event(event: dict[str, Any]) -> None:
        await websocket.send_text(orjson.dumps(event).decode("utf-8"))

    manager = _make_manager(thread_id, send_event=ws_send_event)

    # Watchdog: when the thread-stream consumer stops, send the error frame
    # (if it wasn't cancelled) and close the socket, instead of leaving the
    # client on an open connection that will never deliver another event.
    # ``receive_text`` below raises ``WebSocketDisconnect`` once the close
    # lands, exiting the loop through its existing handler.
    async def _stream_watchdog() -> None:
        await manager.wait_for_thread_stream_end()
        if manager.thread_stream_failed:
            with contextlib.suppress(Exception):
                await websocket.send_text(_THREAD_STREAM_FAILED_DATA.decode())
        with contextlib.suppress(Exception):
            await websocket.close(code=1011, reason="thread stream ended")

    def start_stream(filters: Any) -> asyncio.Task[None]:
        manager.start_thread_stream(auth_filters=filters)
        return asyncio.create_task(_stream_watchdog())

    watchdog = None if awaiting_thread else start_stream(auth_filters)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                payload = orjson.loads(raw)
            except Exception:
                await websocket.send_json(
                    {
                        "type": "error",
                        "id": None,
                        "error": "invalid_argument",
                        "message": "Protocol commands must be valid JSON.",
                    }
                )
                continue

            if (
                not isinstance(payload, dict)
                or not isinstance(payload.get("id"), int)
                or not isinstance(payload.get("method"), str)
            ):
                await websocket.send_json(
                    {
                        "type": "error",
                        "id": payload.get("id") if isinstance(payload, dict) else None,
                        "error": "invalid_argument",
                        "message": "Protocol commands must include an integer id and string method.",
                    }
                )
                continue

            if awaiting_thread and payload["method"] != "run.start":
                await websocket.close(code=4404)
                return
            response = await manager.handle_command(payload)
            await websocket.send_text(orjson.dumps(response).decode("utf-8"))
            if awaiting_thread and response.get("type") == "success":
                try:
                    auth_filters = await Threads.Stream.check_thread_stream_auth(
                        thread_uuid
                    )
                except Exception as exc:
                    await _close_for_failed_access_check(websocket, exc)
                    return
                watchdog = start_stream(auth_filters)
                awaiting_thread = False
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("Protocol WebSocket error")
    finally:
        if watchdog is not None:
            watchdog.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await watchdog
        await manager.close()


# ---------------------------------------------------------------------------
# Route list
# ---------------------------------------------------------------------------

event_streaming_routes: list[ApiRoute | ApiWebSocketRoute] = [
    ApiRoute(
        "/threads/{thread_id}/stream/events",
        _thread_events,
        methods=["POST"],
    ),
    ApiRoute(
        "/threads/{thread_id}/commands",
        _thread_command,
        methods=["POST"],
    ),
    ApiWebSocketRoute("/threads/{thread_id}/stream/events", _thread_websocket),
]
