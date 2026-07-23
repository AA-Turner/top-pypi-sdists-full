import asyncio
import contextlib
import threading
import typing as t
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from uuid import uuid4

from fastapi import WebSocket
from loguru import logger
from pydantic import ValidationError
from starlette.websockets import WebSocketDisconnect

from dreadnode.app.api.models import HumanInputResponse
from dreadnode.app.server.auth import sandbox_ws_auth
from dreadnode.app.server.runtime_events import (
    CONTROL_COMMAND_ACK,
    CONTROL_COMMAND_ERROR,
    CONTROL_FORWARDER_FAILED,
    CONTROL_HELLO_ACK,
    CONTROL_PONG,
    CONTROL_SESSION_SNAPSHOT,
    CONTROL_TRANSPORT_RESYNC,
    EventBus,
    EventBusSubscription,
    PromptRespondCommandPayload,
    RuntimeCommandEnvelope,
    RuntimeControlEnvelope,
    RuntimeEventEnvelope,
    RuntimeSessionSnapshot,
    SubscribeCommandPayload,
    TurnCancelCommandPayload,
    TurnStartCommandPayload,
)
from dreadnode.app.server.runtime_token import get_token_source
from dreadnode.app.server.utils import serialize_ws_frame

_WS_CLOSE_UNAUTHORIZED = 4401
_WS_CLOSE_INVALID_COMMAND = 4400
# Closed by the server because the runtime token rotated; clients should
# reconnect (with the new token, which they fetch/hold out of band).
_WS_CLOSE_TOKEN_ROTATED = 4402
RuntimeOutboundEnvelope = RuntimeControlEnvelope | RuntimeEventEnvelope


@dataclass(eq=False)
class _WsConnHandle:
    """A live websocket plus what's needed to close it safely from another thread:
    the loop it runs on, the runtime token it authed under (so a rotation can
    target it), and a shared sink holding a strong reference to the in-flight
    close task."""

    websocket: WebSocket
    loop: asyncio.AbstractEventLoop
    token: str | None
    tasks: "set[asyncio.Task[None]]"

    def schedule_close(self) -> None:
        # Hop onto the connection's own loop; the retire callback that triggers
        # this may run on a different thread.
        with contextlib.suppress(RuntimeError):  # loop already closed
            self.loop.call_soon_threadsafe(self._spawn_close)

    def _spawn_close(self) -> None:
        with contextlib.suppress(RuntimeError):
            # Hold a strong reference until the task settles — the event loop
            # only keeps a weak one, so a bare fire-and-forget task can be
            # garbage-collected before it runs and the socket would never close.
            task = asyncio.ensure_future(self._close())
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

    async def _close(self) -> None:
        await _close_token_rotated(self.websocket)


class WebSocketConnectionRegistry:
    """Tracks live runtime websocket connections so they can be force-closed when
    the runtime token rotates.

    On lossless reconnect the platform rotates the sandbox's runtime token; a
    connection established under the *retired* token must re-establish (with the
    new token) rather than linger as a watch-only socket. ``close_for_token`` is
    invoked from the token source's retire callback, which may run on any thread —
    each close is therefore scheduled on the connection's own event loop.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._conns: set[_WsConnHandle] = set()
        # Strong references to in-flight close tasks (see ``_spawn_close``).
        self._close_tasks: set[asyncio.Task[None]] = set()

    def register(self, websocket: WebSocket, *, token: str | None) -> _WsConnHandle:
        handle = _WsConnHandle(websocket, asyncio.get_running_loop(), token, self._close_tasks)
        with self._lock:
            self._conns.add(handle)
        return handle

    def unregister(self, handle: _WsConnHandle) -> None:
        with self._lock:
            self._conns.discard(handle)

    def close_for_token(self, token: str) -> int:
        """Close every live connection authed under ``token`` (a rotated-out token).

        Targeting the retired token — rather than closing everything — leaves
        alone a client that already reconnected under the *new* token during the
        grace window, instead of needlessly bouncing it. Returns the number of
        connections closed.
        """
        with self._lock:
            handles = [handle for handle in self._conns if handle.token == token]
            self._conns.difference_update(handles)
        for handle in handles:
            handle.schedule_close()
        return len(handles)

    def close_all(self) -> None:
        """Close every live connection (shutdown / blunt fallback)."""
        with self._lock:
            handles = list(self._conns)
            self._conns.clear()
        for handle in handles:
            handle.schedule_close()


async def _close_token_rotated(websocket: WebSocket) -> None:
    """Close a socket because the runtime token it authenticated with was rotated
    out. Single source of the close code + reason the browser reconnect keys off."""
    with suppress(Exception):
        await websocket.close(code=_WS_CLOSE_TOKEN_ROTATED, reason="runtime token rotated")


async def _sever_if_rotated(websocket: WebSocket, authed_token: str | None) -> bool:
    """Close the socket if ``authed_token`` is no longer the current runtime token.

    The single check-then-close used everywhere a socket must re-verify its
    credential after the handshake: the accept↔register race, and — because a
    rotation is only *observed* when something calls the token source — before
    every inbound command and every outbound event delivery, so a socket that
    only sends (or only receives) is still severed rather than lingering until
    some unrelated auth call happens to fire the retire sweep. Returns True if it
    closed the socket. ``None`` means auth is disabled, so nothing to rotate.
    """
    if authed_token is None:
        return False
    if get_token_source().is_current(authed_token):
        return False
    await _close_token_rotated(websocket)
    return True


class RuntimeSessionProtocol(t.Protocol):
    """Behavior the websocket transport needs from a runtime session."""

    session_id: str

    @property
    def active_turn_id(self) -> str | None: ...

    async def build_snapshot(self) -> RuntimeSessionSnapshot: ...

    async def enqueue_chat(
        self,
        message: str,
        *,
        model: str | None = None,
        agent: str | None = None,
        reset: bool = False,
        generate_params_extra: dict[str, t.Any] | None = None,
    ) -> tuple[str, asyncio.Queue[dict[str, t.Any] | None]]: ...

    async def cancel(self) -> bool: ...

    def resolve_human_response(self, response: HumanInputResponse) -> bool: ...

    def resolve_permission(self, request_id: str, decision: str) -> None: ...


class SyncAcceptedTurnProtocol(t.Protocol):
    """Callback used to persist accepted-turn metadata to the platform."""

    def __call__(
        self,
        session: RuntimeSessionProtocol,
        *,
        model: str | None = None,
        agent: str | None = None,
    ) -> None: ...


class RuntimeWebSocketTransport:
    """Stateful websocket command router and broker fan-out coordinator."""

    def __init__(
        self,
        websocket: WebSocket,
        *,
        event_bus: "EventBus",
        resolve_session: Callable[[str], RuntimeSessionProtocol],
        get_session: Callable[[str], RuntimeSessionProtocol | None],
        sync_accepted_turn: SyncAcceptedTurnProtocol,
        consume_ticket: "Callable[[str], str | None] | None" = None,
        connection_registry: "WebSocketConnectionRegistry | None" = None,
    ) -> None:
        self._websocket = websocket
        self._event_bus = event_bus
        self._resolve_session = resolve_session
        self._get_session = get_session
        self._sync_accepted_turn = sync_accepted_turn
        self._consume_ticket = consume_ticket
        self._connection_registry = connection_registry
        self._conn_handle: _WsConnHandle | None = None
        self._connection_id = f"conn_{uuid4().hex}"
        self._outbound_queue: asyncio.Queue[RuntimeOutboundEnvelope | None] = asyncio.Queue()
        self._subscriptions: dict[str, EventBusSubscription] = {}
        self._forwarders: dict[str, asyncio.Task[None]] = {}
        # Background platform-sync tasks dispatched from turn.start. Held in
        # a set so the asyncio event loop keeps a strong reference (otherwise
        # tasks may be garbage-collected mid-flight) and so we can observe
        # failures via a done callback.
        self._background_sync_tasks: set[asyncio.Task[None]] = set()
        self._hello_received = False
        # The credential this socket authenticated with (None when auth is
        # disabled). Re-checked before every inbound command and every outbound
        # frame so a rotated-out socket can't keep issuing or receiving until the
        # next auth call happens to fire the retire sweep.
        self._authed_token: str | None = None

    async def serve(self) -> None:
        """Run the websocket transport until disconnect."""
        error, authed_token = sandbox_ws_auth(
            self._websocket.headers.get("authorization"),
            self._websocket.query_params.get("ticket"),
            self._consume_ticket,
        )
        if error is not None:
            logger.warning(
                "Runtime websocket auth failed | path={} reason={}",
                self._websocket.url.path,
                error,
            )
            await self._websocket.close(code=_WS_CLOSE_UNAUTHORIZED, reason=error)
            return

        self._authed_token = authed_token
        await self._websocket.accept()
        if self._connection_registry is not None:
            # Register under the credential that authenticated us, so a rotation
            # closes exactly the sockets belonging to the retired token.
            self._conn_handle = self._connection_registry.register(
                self._websocket, token=authed_token
            )
            if await _sever_if_rotated(self._websocket, authed_token):
                self._connection_registry.unregister(self._conn_handle)
                self._conn_handle = None
                return
        logger.debug("Runtime websocket opened | connection_id={}", self._connection_id)
        sender_task = asyncio.create_task(self._sender())

        try:
            while True:
                try:
                    raw_command = await self._websocket.receive_text()
                except WebSocketDisconnect:
                    logger.debug(
                        "Runtime websocket disconnected | connection_id={}", self._connection_id
                    )
                    break

                # Re-authorize every command against the current token: the
                # handshake check is a point-in-time snapshot, and a rotation
                # after it must not let this socket keep issuing commands.
                if await _sever_if_rotated(self._websocket, self._authed_token):
                    logger.debug(
                        "Runtime websocket token rotated mid-session | connection_id={}",
                        self._connection_id,
                    )
                    break

                try:
                    command = RuntimeCommandEnvelope.model_validate_json(raw_command)
                except (ValidationError, ValueError) as exc:
                    await self._send_command_error(detail=f"Invalid command envelope: {exc}")
                    continue

                await self._dispatch_command(command)
        finally:
            if self._connection_registry is not None and self._conn_handle is not None:
                self._connection_registry.unregister(self._conn_handle)
            for session_id in list(self._subscriptions):
                await self._unsubscribe_session(session_id)
            sender_task.cancel()
            with suppress(asyncio.CancelledError, RuntimeError, WebSocketDisconnect):
                await sender_task
            await self._drain_background_sync_tasks()
            logger.debug(
                "Runtime websocket closed | connection_id={} subscribed_sessions={}",
                self._connection_id,
                len(self._subscriptions),
            )

    async def _drain_background_sync_tasks(self, *, timeout: float = 5.0) -> None:  # noqa: ASYNC109
        """Wait briefly for in-flight platform sync tasks before returning.

        Pending tasks are *not* cancelled — they're best-effort writes to
        the platform API and cancelling mid-write could leave the platform
        in a half-written state. If they don't finish within ``timeout``,
        we log and let them continue in the background; the done callback
        keeps a strong reference until each one settles.
        """
        if not self._background_sync_tasks:
            return
        pending = list(self._background_sync_tasks)
        _, still_pending = await asyncio.wait(pending, timeout=timeout)
        if still_pending:
            logger.warning(
                "Runtime websocket closing with {} background sync task(s) still "
                "running | connection_id={}",
                len(still_pending),
                self._connection_id,
            )

    async def _sender(self) -> None:
        while True:
            envelope = await self._outbound_queue.get()
            if envelope is None:
                return
            # Re-authorize before every outbound frame. Session events reach this
            # socket through a separate forwarder task, not the inbound command
            # loop — so a client that subscribes and then only *watches* (sends
            # no commands) would otherwise keep receiving another credential's
            # events after a rotation, until some unrelated auth fired the retire
            # sweep. This closes that the moment the next frame would be sent.
            if await _sever_if_rotated(self._websocket, self._authed_token):
                logger.debug(
                    "Runtime websocket token rotated; halting outbound | connection_id={}",
                    self._connection_id,
                )
                return
            await self._websocket.send_text(serialize_ws_frame(envelope.model_dump(mode="json")))

    async def _dispatch_command(self, command: RuntimeCommandEnvelope) -> None:
        if command.op != "hello" and not self._hello_received:
            await self._send_command_error(
                detail="Send hello before interactive websocket commands",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
                status_code=_WS_CLOSE_INVALID_COMMAND,
            )
            return

        if command.op == "hello":
            self._hello_received = True
            await self._send_control(
                kind=CONTROL_HELLO_ACK,
                command_id=command.command_id,
                payload={
                    "supported_ops": [
                        "hello",
                        "subscribe",
                        "unsubscribe",
                        "turn.start",
                        "turn.cancel",
                        "prompt.respond",
                        "ping",
                    ]
                },
            )
            return

        if command.op == "ping":
            await self._send_control(
                kind=CONTROL_PONG,
                command_id=command.command_id,
                session_id=command.session_id,
                payload={"op": "ping"},
            )
            return

        if command.session_id is None:
            await self._send_command_error(
                detail=f"{command.op} requires session_id",
                command_id=command.command_id,
                op=command.op,
            )
            return

        if command.op == "unsubscribe":
            await self._unsubscribe_session(command.session_id)
            await self._send_command_ack(
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
            )
            return

        if command.op == "subscribe":
            await self._handle_subscribe(command)
            return

        if command.op == "turn.start":
            await self._handle_turn_start(command)
            return

        if command.op == "turn.cancel":
            await self._handle_turn_cancel(command)
            return

        if command.op == "prompt.respond":
            await self._handle_prompt_respond(command)
            return

        await self._send_command_error(
            detail=f"Unsupported operation: {command.op}",
            command_id=command.command_id,
            session_id=command.session_id,
            op=command.op,
        )

    async def _handle_subscribe(self, command: RuntimeCommandEnvelope) -> None:
        try:
            payload = SubscribeCommandPayload.model_validate(command.payload)
        except ValidationError as exc:
            await self._send_command_error(
                detail=f"Invalid subscribe payload: {exc}",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
            )
            return

        assert command.session_id is not None
        session = self._resolve_session(command.session_id)
        snapshot = await session.build_snapshot()

        # Determine the replay cursor. If the client is behind the replay
        # window (needs_resync), snap to snapshot.latest_seq so only future
        # events arrive after the snapshot — replaying the surviving tail
        # would re-duplicate UI state.
        subscribe_after_seq = snapshot.latest_seq
        needs_resync = False
        if payload.after_seq is not None:
            subscribe_after_seq = payload.after_seq

        await self._unsubscribe_session(command.session_id)
        subscription = await self._event_bus.subscribe(
            session_id=command.session_id,
            after_seq=subscribe_after_seq,
        )
        if subscription.needs_resync:
            needs_resync = True
            await self._event_bus.unsubscribe(subscription)
            subscription = await self._event_bus.subscribe(
                session_id=command.session_id,
                after_seq=snapshot.latest_seq,
            )
        self._subscriptions[command.session_id] = subscription

        await self._send_command_ack(
            command_id=command.command_id,
            session_id=command.session_id,
            op=command.op,
        )
        if needs_resync:
            logger.warning(
                "Runtime websocket resync required | connection_id={} session_id={} after_seq={} latest_seq={}",
                self._connection_id,
                command.session_id,
                payload.after_seq,
                snapshot.latest_seq,
            )
            await self._send_control(
                kind=CONTROL_TRANSPORT_RESYNC,
                session_id=command.session_id,
                payload={
                    "after_seq": payload.after_seq,
                    "latest_seq": snapshot.latest_seq,
                    "oldest_buffered_seq": self._event_bus.session_oldest_buffered_seq(
                        command.session_id
                    ),
                },
            )
        await self._send_control(
            kind=CONTROL_SESSION_SNAPSHOT,
            session_id=command.session_id,
            payload=snapshot.model_dump(mode="json"),
        )

        self._forwarders[command.session_id] = asyncio.create_task(
            self._forward_session_subscription(subscription)
        )

    async def _handle_turn_start(self, command: RuntimeCommandEnvelope) -> None:
        try:
            payload = TurnStartCommandPayload.model_validate(command.payload)
        except ValidationError as exc:
            await self._send_command_error(
                detail=f"Invalid turn.start payload: {exc}",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
            )
            return

        assert command.session_id is not None
        session = self._resolve_session(command.session_id)
        turn_id, _ = await session.enqueue_chat(
            payload.message,
            model=payload.model,
            agent=payload.agent,
            reset=payload.reset,
            generate_params_extra=payload.generate_params_extra,
        )
        # Platform sync is best-effort and runs off the event loop so the
        # websocket handler doesn't block on a network round-trip. The task
        # is tracked so it can't be garbage-collected mid-flight, and the
        # done callback ensures any failure is logged instead of silently
        # swallowed.
        sync_task = asyncio.create_task(
            asyncio.to_thread(
                self._sync_accepted_turn,
                session,
                model=payload.model,
                agent=payload.agent,
            ),
            name=f"platform-sync-{command.session_id}",
        )
        self._background_sync_tasks.add(sync_task)
        sync_task.add_done_callback(self._on_background_sync_done)
        # Echo turn_id in the ack so the client can scope subsequent
        # queue reads to this turn and reject stragglers from a prior
        # cancelled turn (see InteractiveTransport.stream_chat).
        await self._send_command_ack(
            command_id=command.command_id,
            session_id=command.session_id,
            op=command.op,
            payload={"turn_id": turn_id},
        )

    def _on_background_sync_done(self, task: asyncio.Task[None]) -> None:
        """Discard a finished platform-sync task and log any failure.

        Cancellation is silently ignored — it only happens during transport
        teardown when nothing useful can be done about it.
        """
        self._background_sync_tasks.discard(task)
        if task.cancelled():
            return
        exc = task.exception()
        if exc is not None:
            logger.opt(exception=exc).warning(
                "Background platform sync failed | connection_id={} task={}",
                self._connection_id,
                task.get_name(),
            )

    async def _handle_turn_cancel(self, command: RuntimeCommandEnvelope) -> None:
        try:
            payload = TurnCancelCommandPayload.model_validate(command.payload)
        except ValidationError as exc:
            await self._send_command_error(
                detail=f"Invalid turn.cancel payload: {exc}",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
            )
            return

        assert command.session_id is not None
        session = self._get_session(command.session_id)
        if session is None:
            await self._send_command_error(
                detail=f"Session not found: {command.session_id}",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
                status_code=404,
            )
            return
        if payload.turn_id is not None and payload.turn_id != session.active_turn_id:
            await self._send_command_error(
                detail=(
                    f"Active turn mismatch: requested {payload.turn_id}, "
                    f"current {session.active_turn_id}"
                ),
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
                status_code=409,
            )
            return

        was_busy = await session.cancel()
        await self._send_command_ack(
            command_id=command.command_id,
            session_id=command.session_id,
            op=command.op,
            payload={"status": "cancelled" if was_busy else "idle"},
        )

    async def _handle_prompt_respond(self, command: RuntimeCommandEnvelope) -> None:
        try:
            payload = PromptRespondCommandPayload.model_validate(command.payload)
            response = self._build_human_input_response(payload)
        except (ValidationError, ValueError) as exc:
            await self._send_command_error(
                detail=f"Invalid prompt.respond payload: {exc}",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
            )
            return

        assert command.session_id is not None
        session = self._get_session(command.session_id)
        if session is None:
            await self._send_command_error(
                detail=f"Session not found: {command.session_id}",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
                status_code=404,
            )
            return

        if response is not None:
            resolved = session.resolve_human_response(response)
        else:
            assert payload.decision is not None
            session.resolve_permission(payload.request_id, payload.decision)
            resolved = True

        if not resolved:
            await self._send_command_error(
                detail=f"Unknown or expired request_id: {payload.request_id}",
                command_id=command.command_id,
                session_id=command.session_id,
                op=command.op,
                status_code=409,
            )
            return

        await self._send_command_ack(
            command_id=command.command_id,
            session_id=command.session_id,
            op=command.op,
            payload={
                "request_id": payload.request_id,
                "status": "resolved",
            },
        )

    async def _send_control(
        self,
        *,
        kind: str,
        command_id: str | None = None,
        session_id: str | None = None,
        payload: dict[str, t.Any] | None = None,
    ) -> None:
        await self._outbound_queue.put(
            RuntimeControlEnvelope(
                connection_id=self._connection_id,
                command_id=command_id,
                session_id=session_id,
                kind=kind,
                payload=payload or {},
            )
        )

    async def _send_command_ack(
        self,
        *,
        command_id: str | None,
        session_id: str | None,
        op: str,
        payload: dict[str, t.Any] | None = None,
    ) -> None:
        ack_payload = {"op": op}
        if payload:
            ack_payload.update(payload)
        await self._send_control(
            kind=CONTROL_COMMAND_ACK,
            command_id=command_id,
            session_id=session_id,
            payload=ack_payload,
        )

    async def _send_command_error(
        self,
        *,
        detail: str,
        command_id: str | None = None,
        session_id: str | None = None,
        op: str | None = None,
        status_code: int = 400,
    ) -> None:
        payload: dict[str, t.Any] = {
            "detail": detail,
            "status_code": status_code,
        }
        if op is not None:
            payload["op"] = op
        await self._send_control(
            kind=CONTROL_COMMAND_ERROR,
            command_id=command_id,
            session_id=session_id,
            payload=payload,
        )

    async def _unsubscribe_session(self, session_id: str) -> None:
        forwarder = self._forwarders.pop(session_id, None)
        if forwarder is not None:
            forwarder.cancel()
            with suppress(asyncio.CancelledError):
                await forwarder

        subscription = self._subscriptions.pop(session_id, None)
        if subscription is not None:
            await self._event_bus.unsubscribe(subscription)

    async def _forward_session_subscription(self, subscription: EventBusSubscription) -> None:
        """Pump events from one session subscription onto the websocket outbound queue.

        Any unhandled exception here used to kill the task silently — the
        dead task remained in ``self._forwarders`` while events stopped
        flowing for that session and the user saw the UI freeze mid-turn.
        We now log the failure, drop the dead bookkeeping, release the
        bus subscription, and emit a ``transport.forwarder_failed``
        control message so clients can resubscribe.
        """
        session_id = subscription.session_filter
        try:
            while True:
                envelope = await subscription.queue.get()
                await self._outbound_queue.put(
                    envelope.model_copy(update={"connection_id": self._connection_id})
                )
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.opt(exception=True).warning(
                "Runtime event forwarder terminated unexpectedly | connection_id={} session_id={}",
                self._connection_id,
                session_id,
            )
            self._forwarders.pop(session_id, None) if session_id else None
            existing = self._subscriptions.pop(session_id, None) if session_id else None
            if existing is not None:
                with suppress(Exception):
                    await self._event_bus.unsubscribe(existing)
            with suppress(Exception):
                await self._send_control(
                    kind=CONTROL_FORWARDER_FAILED,
                    session_id=session_id,
                    payload={
                        "detail": (
                            "Event forwarder terminated unexpectedly. "
                            "Resubscribe to resume receiving events."
                        )
                    },
                )

    @staticmethod
    def _build_human_input_response(
        payload: PromptRespondCommandPayload,
    ) -> HumanInputResponse | None:
        """Validate the human-input branch of ``prompt.respond``.

        Returns ``None`` when the payload is a permission decision (``decision``
        present, ``action`` absent); raises ``ValueError`` when the payload
        carries neither or both.
        """
        if (payload.action is None) == (payload.decision is None):
            raise ValueError(
                "prompt.respond requires exactly one of ``action`` (human input) "
                "or ``decision`` (permission)",
            )
        if payload.action is None:
            return None
        return HumanInputResponse.model_validate(
            {
                "request_id": payload.request_id,
                "action": payload.action,
                "answers": payload.answers,
            },
        )


async def serve_runtime_websocket(
    websocket: WebSocket,
    *,
    event_bus: EventBus,
    resolve_session: Callable[[str], RuntimeSessionProtocol],
    get_session: Callable[[str], RuntimeSessionProtocol | None],
    sync_accepted_turn: SyncAcceptedTurnProtocol,
    consume_ticket: "Callable[[str], str | None] | None" = None,
    connection_registry: "WebSocketConnectionRegistry | None" = None,
) -> None:
    """Run the runtime websocket transport on the provided FastAPI socket."""
    transport = RuntimeWebSocketTransport(
        websocket,
        event_bus=event_bus,
        resolve_session=resolve_session,
        get_session=get_session,
        sync_accepted_turn=sync_accepted_turn,
        consume_ticket=consume_ticket,
        connection_registry=connection_registry,
    )
    await transport.serve()


async def serve_runtime_event_stream(
    websocket: WebSocket,
    *,
    event_bus: EventBus,
    consume_ticket: "t.Callable[[str], str | None] | None" = None,
    connection_registry: "WebSocketConnectionRegistry | None" = None,
) -> None:
    """Serve the runtime-bus event subscription stream (CAP-WCLI-018..020).

    One subscription per websocket. ``kinds`` is read from repeated
    ``?kinds=<kind>`` query params; an empty list subscribes to every
    kind. Both session- and runtime-scope envelopes are forwarded so the
    consumer can inspect ``session_id`` to distinguish scopes. Replayed
    buffer entries are suppressed — consumers receive only events emitted
    after the subscription is established.
    """
    error, authed_token = sandbox_ws_auth(
        websocket.headers.get("authorization"),
        websocket.query_params.get("ticket"),
        consume_ticket,
    )
    if error is not None:
        logger.warning(
            "Runtime event-stream auth failed | path={} reason={}",
            websocket.url.path,
            error,
        )
        await websocket.close(code=_WS_CLOSE_UNAUTHORIZED, reason=error)
        return

    raw_kinds = [k.strip() for k in websocket.query_params.getlist("kinds") if k.strip()]
    kinds: frozenset[str] | None = frozenset(raw_kinds) if raw_kinds else None

    # Register the bus subscription before accepting the websocket so that
    # by the time the client's connect() unblocks, the subscription is
    # already receiving events. Without this ordering there is a brief
    # race where events published immediately after connect are missed
    # while the subscribe() call is still awaiting the bus lock.
    subscription = await event_bus.subscribe(
        session_id=None,
        kinds=kinds,
        include_runtime=True,
    )
    try:
        await websocket.accept()
    except Exception:
        await event_bus.unsubscribe(subscription)
        raise

    conn_handle: _WsConnHandle | None = None
    if connection_registry is not None:
        # Register under the credential that authenticated us, so a rotation
        # closes exactly the sockets belonging to the retired token.
        conn_handle = connection_registry.register(websocket, token=authed_token)
        if await _sever_if_rotated(websocket, authed_token):
            # Rotation landed between auth and registration — this socket's
            # credential is already retired.
            connection_registry.unregister(conn_handle)
            await event_bus.unsubscribe(subscription)
            return

    logger.debug(
        "Runtime event stream opened | kinds={}",
        sorted(kinds) if kinds else "*",
    )

    async def _pump() -> None:
        while True:
            envelope = await subscription.queue.get()
            # CAP-WCLI-020: subscribe does not replay history. Suppress the
            # replay-flagged envelopes the bus drains from its buffer at
            # subscribe time.
            if envelope.replay:
                continue
            # Re-authorize before forwarding (same reason as the interactive
            # sender): a watch-only subscriber sends no commands, so delivery is
            # the only place its credential can be re-checked. Severs it the
            # moment the next event would leak; if none flows, nothing leaks.
            if await _sever_if_rotated(websocket, authed_token):
                logger.debug("Runtime event stream token rotated mid-stream; closing")
                return
            await websocket.send_text(serialize_ws_frame(envelope.model_dump(mode="json")))

    async def _watch_disconnect() -> None:
        # Consumers don't send commands on this stream — we only read to
        # observe the disconnect promptly so the pump stops and the bus
        # subscription is released, rather than waiting for the next event
        # to surface the broken transport.
        with suppress(WebSocketDisconnect):
            while True:
                await websocket.receive_text()

    pump_task = asyncio.create_task(_pump(), name="runtime-event-stream-pump")
    watch_task = asyncio.create_task(_watch_disconnect(), name="runtime-event-stream-watch")
    try:
        _, pending = await asyncio.wait(
            [pump_task, watch_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
    finally:
        if connection_registry is not None and conn_handle is not None:
            connection_registry.unregister(conn_handle)
        await event_bus.unsubscribe(subscription)
        with suppress(Exception):
            await websocket.close()
        logger.debug("Runtime event stream closed")
