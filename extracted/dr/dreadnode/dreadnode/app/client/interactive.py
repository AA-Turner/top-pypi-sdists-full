import asyncio
import contextlib
import json
import typing as t
from uuid import uuid4

from loguru import logger

from dreadnode.app.api.client import AuthenticationError
from dreadnode.app.client.transports import (
    StreamingASGITransport,
    _RuntimeSocketProtocol,
    _WebsocketsRuntimeSocket,
)
from dreadnode.app.server.runtime_events import TERMINAL_TURN_KINDS
from dreadnode.core.tls import cached_platform_ssl_context

if t.TYPE_CHECKING:
    from dreadnode.app.api.models import HumanInputResponse
    from dreadnode.app.client.runtime_client import RuntimeClient


class _InteractiveCommandError(RuntimeError):
    """Structured command error returned by the runtime websocket transport."""

    def __init__(self, detail: str, *, status_code: int = 400) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class TurnFailedError(RuntimeError):
    """Raised by :meth:`RuntimeClient.run_turn` on a ``turn.failed`` terminal.

    Carries the synthesized turn trajectory (CAP-WEVT-008) so callers can
    inspect ``error_type``, ``partial_response``, and any tool calls the
    model attempted before the failure.
    """

    def __init__(
        self,
        error_type: str,
        message: str,
        *,
        partial_response: str | None = None,
        tool_calls_attempted: list[dict[str, t.Any]] | None = None,
        turn_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.partial_response = partial_response
        self.tool_calls_attempted = tool_calls_attempted or []
        self.turn_id = turn_id


class TurnCancelledError(RuntimeError):
    """Raised by :meth:`RuntimeClient.run_turn` on a ``turn.cancelled`` terminal.

    Carries the synthesized turn trajectory (CAP-WEVT-009) so callers can
    recover any ``partial_response`` the agent produced before cancellation.
    """

    def __init__(
        self,
        reason: str,
        *,
        partial_response: str | None = None,
        turn_id: str | None = None,
    ) -> None:
        super().__init__(f"Turn cancelled: {reason}")
        self.reason = reason
        self.partial_response = partial_response
        self.turn_id = turn_id


def _ack_turn_id(ack: dict[str, t.Any]) -> str:
    """Extract the turn_id from a ``turn.start`` command ack payload.

    The server must echo the assigned turn_id in the ack so the client
    can scope subsequent event-stream reads to the same turn, rejecting
    stragglers from a prior cancelled turn that remain in the
    per-session queue. A missing or non-string turn_id is a protocol
    violation and raised loudly rather than silently degrading.
    """
    payload = ack.get("payload")
    if not isinstance(payload, dict):
        raise TypeError(f"turn.start ack missing payload: {ack!r}")
    turn_id = payload.get("turn_id")
    if not isinstance(turn_id, str):
        raise TypeError(f"turn.start ack missing turn_id: {payload!r}")
    return turn_id


def _envelope_belongs_to_turn(envelope: dict[str, t.Any], expected_turn_id: str) -> bool:
    """Return True when ``envelope`` should be consumed by the current turn.

    Session-scoped envelopes with no ``turn_id`` (snapshots, resync
    notifications) are always in-scope. An envelope whose ``turn_id``
    differs from the expected turn is a straggler from a prior turn and
    should be skipped.
    """
    env_turn_id = envelope.get("turn_id")
    if env_turn_id is None:
        return True
    return env_turn_id == expected_turn_id


class _RuntimeInteractiveTransport:
    """Persistent interactive websocket transport for runtime chat operations."""

    def __init__(self, client: "RuntimeClient") -> None:
        self._client = client
        self._socket: _RuntimeSocketProtocol | None = None
        self._receiver_task: asyncio.Task[None] | None = None
        self._connect_lock = asyncio.Lock()
        self._send_lock = asyncio.Lock()
        self._subscription_lock = asyncio.Lock()
        self._command_waiters: dict[str, asyncio.Future[dict[str, t.Any]]] = {}
        self._session_queues: dict[str, asyncio.Queue[dict[str, t.Any] | None]] = {}
        self._desired_sessions: set[str] = set()
        self._subscribed_sessions: set[str] = set()
        self._last_seq_by_session: dict[str, int] = {}
        self._latest_snapshot_by_session: dict[str, dict[str, t.Any]] = {}
        self._latest_resync_by_session: dict[str, dict[str, t.Any]] = {}
        self._receiver_error: BaseException | None = None

    async def close(self) -> None:
        receiver_task = self._receiver_task
        socket = self._socket
        self._receiver_task = None
        self._socket = None
        self._receiver_error = None
        self._desired_sessions.clear()
        self._subscribed_sessions.clear()
        self._last_seq_by_session.clear()
        self._latest_snapshot_by_session.clear()
        self._latest_resync_by_session.clear()
        self._reject_pending_commands(RuntimeError("Interactive transport closed"))
        for session_queue in self._session_queues.values():
            await session_queue.put(None)
        self._session_queues.clear()
        if socket is not None:
            with contextlib.suppress(Exception):
                await socket.close()
        if receiver_task is not None:
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await receiver_task

    async def stream_chat(
        self,
        *,
        session_id: str,
        message: str,
        model: str | None = None,
        agent: str | None = None,
        reset: bool = False,
        generate_params_extra: dict[str, t.Any] | None = None,
    ) -> t.AsyncIterator[dict[str, t.Any]]:
        await self.ensure_connected()
        await self._ensure_subscribed(session_id)
        ack = await self._send_command(
            "turn.start",
            session_id=session_id,
            payload={
                "message": message,
                **({"model": model} if model is not None else {}),
                **({"agent": agent} if agent is not None else {}),
                "reset": reset,
                **(
                    {"generate_params_extra": generate_params_extra}
                    if generate_params_extra is not None
                    else {}
                ),
            },
        )
        expected_turn_id = _ack_turn_id(ack)

        session_queue = self._session_queue(session_id)
        while True:
            envelope = await session_queue.get()
            if envelope is None:
                if await self._recover_stream_session(session_id):
                    continue
                error = self._receiver_error or RuntimeError("Interactive transport closed")
                raise error

            if not _envelope_belongs_to_turn(envelope, expected_turn_id):
                # Straggler from a cancelled or earlier turn — the session
                # queue is session-scoped, and older turns can leave
                # events behind when their stream_chat was aborted. Drop
                # silently so this turn only sees its own events.
                continue

            raw_event = self._raw_event_from_envelope(envelope)
            if raw_event is not None:
                yield raw_event

            if str(envelope.get("kind", "")) in TERMINAL_TURN_KINDS:
                # Terminal envelopes carry the synthesized trajectory
                # (CAP-WEVT-007..009) — consumers that want the final
                # response, tool calls, or error detail should use
                # :meth:`run_turn` rather than iterating raw events.
                return

    async def run_turn(
        self,
        *,
        session_id: str,
        message: str,
        model: str | None = None,
        agent: str | None = None,
        reset: bool = False,
        generate_params_extra: dict[str, t.Any] | None = None,
    ) -> dict[str, t.Any]:
        """Run a turn to completion and return the terminal ``turn.completed``
        payload (CAP-WEVT-007).

        Raises :class:`TurnFailedError` on ``turn.failed`` and
        :class:`TurnCancelledError` on ``turn.cancelled``.
        """
        await self.ensure_connected()
        await self._ensure_subscribed(session_id)
        ack = await self._send_command(
            "turn.start",
            session_id=session_id,
            payload={
                "message": message,
                **({"model": model} if model is not None else {}),
                **({"agent": agent} if agent is not None else {}),
                "reset": reset,
                **(
                    {"generate_params_extra": generate_params_extra}
                    if generate_params_extra is not None
                    else {}
                ),
            },
        )
        expected_turn_id = _ack_turn_id(ack)

        session_queue = self._session_queue(session_id)
        while True:
            envelope = await session_queue.get()
            if envelope is None:
                if await self._recover_stream_session(session_id):
                    continue
                error = self._receiver_error or RuntimeError("Interactive transport closed")
                raise error

            if not _envelope_belongs_to_turn(envelope, expected_turn_id):
                continue

            kind = str(envelope.get("kind", ""))
            if kind not in TERMINAL_TURN_KINDS:
                continue

            payload = envelope.get("payload")
            payload_dict = payload if isinstance(payload, dict) else {}
            if kind == "turn.completed":
                return dict(payload_dict)
            if kind == "turn.failed":
                error_dict = payload_dict.get("error") or {}
                if isinstance(error_dict, dict):
                    error_type = str(error_dict.get("type") or "RuntimeError")
                    error_message = str(error_dict.get("message") or "turn failed")
                else:
                    error_type = "RuntimeError"
                    error_message = str(error_dict)
                raise TurnFailedError(
                    error_type,
                    error_message,
                    partial_response=payload_dict.get("partial_response"),
                    tool_calls_attempted=payload_dict.get("tool_calls_attempted") or [],
                    turn_id=payload_dict.get("turn_id"),
                )
            # turn.cancelled
            raise TurnCancelledError(
                str(payload_dict.get("reason") or "cancelled"),
                partial_response=payload_dict.get("partial_response"),
                turn_id=payload_dict.get("turn_id"),
            )

    async def _recover_stream_session(self, session_id: str) -> bool:
        error = self._receiver_error
        if error is None or isinstance(error, AuthenticationError):
            return False

        logger.warning(
            "Interactive websocket dropped; attempting replay recovery | session={}",
            session_id[:8],
        )
        try:
            await self.ensure_connected()
            await self._ensure_subscribed(session_id)
        except Exception as reconnect_error:
            self._receiver_error = reconnect_error
            return False

        logger.info(
            "Interactive websocket recovered; resumed session subscription | session={}",
            session_id[:8],
        )
        return True

    async def cancel_session(self, session_id: str) -> None:
        await self.ensure_connected()
        await self._send_command("turn.cancel", session_id=session_id)

    async def send_permission_response(
        self,
        session_id: str,
        request_id: str,
        decision: str,
    ) -> None:
        await self.ensure_connected()
        await self._send_command(
            "prompt.respond",
            session_id=session_id,
            payload={
                "request_id": request_id,
                "decision": decision,
            },
        )

    async def send_human_input_response(
        self,
        session_id: str,
        response: "HumanInputResponse",
    ) -> None:
        await self.ensure_connected()
        await self._send_command(
            "prompt.respond",
            session_id=session_id,
            payload=response.model_dump(),
        )

    async def ping(self) -> None:
        """Probe the interactive websocket transport."""
        await self.ensure_connected()
        await self._send_command("ping")

    async def subscribe_session(self, session_id: str) -> None:
        """Ensure a session stays subscribed on the interactive transport."""
        await self.ensure_connected()
        await self._ensure_subscribed(session_id)

    async def unsubscribe_session(self, session_id: str) -> None:
        """Remove a session from the interactive transport subscription set."""
        async with self._subscription_lock:
            self._desired_sessions.discard(session_id)
            socket = self._socket
            receiver_task = self._receiver_task
            if socket is None or receiver_task is None or receiver_task.done():
                self._subscribed_sessions.discard(session_id)
                return
            try:
                await self._send_command("unsubscribe", session_id=session_id)
            finally:
                self._subscribed_sessions.discard(session_id)

    def latest_session_snapshot(self, session_id: str) -> dict[str, t.Any] | None:
        """Return the last snapshot observed for a session."""
        snapshot = self._latest_snapshot_by_session.get(session_id)
        if snapshot is None:
            return None
        return dict(snapshot)

    def latest_resync_required(self, session_id: str) -> dict[str, t.Any] | None:
        """Return the last replay-miss payload observed for a session."""
        payload = self._latest_resync_by_session.get(session_id)
        if payload is None:
            return None
        return dict(payload)

    def desired_session_ids(self) -> set[str]:
        """Return the current desired session subscription set."""
        return set(self._desired_sessions)

    def subscribed_session_ids(self) -> set[str]:
        """Return the currently acknowledged session subscription set."""
        return set(self._subscribed_sessions)

    async def ensure_connected(self) -> None:
        if (
            self._socket is not None
            and self._receiver_task is not None
            and not self._receiver_task.done()
        ):
            return

        async with self._connect_lock:
            if (
                self._socket is not None
                and self._receiver_task is not None
                and not self._receiver_task.done()
            ):
                return

            self._receiver_error = None
            self._socket = await self._connect_socket()
            self._receiver_task = asyncio.create_task(self._receiver_loop())
            await self._send_command("hello")
            await self._restore_subscriptions()

    async def _connect_socket(self) -> _RuntimeSocketProtocol:
        interactive_url = self._client._interactive_websocket_url()
        headers = self._client._build_auth_headers()
        http_transport = self._client._http_client._transport
        if isinstance(http_transport, StreamingASGITransport):
            return await http_transport.websocket_connect(url=interactive_url, headers=headers)
        # A caller-supplied transport has no websocket equivalent, so falling
        # through would open a real network socket the caller never asked for.
        # Mirrors the guard on the sibling event-stream path.
        if self._client._injected_transport is not None:
            raise RuntimeError(
                "Interactive transport is unavailable with an injected HTTP transport"
            )

        from websockets.asyncio.client import connect

        # Match the HTTP client's trust store — a self-hosted runtime behind an
        # internal CA must not fail here after its health check already passed.
        # websockets rejects a context on ws:// and rejects None on wss://,
        # so this has to track the scheme exactly.
        connection = await connect(
            interactive_url,
            additional_headers=headers or None,
            ping_interval=20,
            ping_timeout=20,
            ssl=(cached_platform_ssl_context() if interactive_url.startswith("wss://") else None),
        )
        return _WebsocketsRuntimeSocket(connection)

    async def _ensure_subscribed(self, session_id: str) -> None:
        async with self._subscription_lock:
            self._desired_sessions.add(session_id)
            if session_id in self._subscribed_sessions:
                return
            self._session_queue(session_id)
            payload: dict[str, t.Any] = {}
            after_seq = self._last_seq_by_session.get(session_id)
            if after_seq is not None:
                payload["after_seq"] = after_seq
            await self._send_command("subscribe", session_id=session_id, payload=payload)
            self._subscribed_sessions.add(session_id)

    async def _restore_subscriptions(self) -> None:
        async with self._subscription_lock:
            for session_id in sorted(self._desired_sessions):
                self._session_queue(session_id)
                payload: dict[str, t.Any] = {}
                after_seq = self._last_seq_by_session.get(session_id)
                if after_seq is not None:
                    payload["after_seq"] = after_seq
                await self._send_command("subscribe", session_id=session_id, payload=payload)
                self._subscribed_sessions.add(session_id)

    def _session_queue(self, session_id: str) -> asyncio.Queue[dict[str, t.Any] | None]:
        queue_obj = self._session_queues.get(session_id)
        if queue_obj is None:
            queue_obj = asyncio.Queue()
            self._session_queues[session_id] = queue_obj
        return queue_obj

    async def _send_command(
        self,
        op: str,
        *,
        session_id: str | None = None,
        payload: dict[str, t.Any] | None = None,
    ) -> dict[str, t.Any]:
        socket = self._socket
        if socket is None:
            raise RuntimeError("Interactive websocket not connected")

        command_id = uuid4().hex
        loop = asyncio.get_running_loop()
        waiter: asyncio.Future[dict[str, t.Any]] = loop.create_future()
        self._command_waiters[command_id] = waiter
        envelope = {
            "schema_version": 2,
            "command_id": command_id,
            "op": op,
            "session_id": session_id,
            "payload": payload or {},
        }

        try:
            async with self._send_lock:
                await socket.send_text(json.dumps(envelope))
        except Exception:
            self._command_waiters.pop(command_id, None)
            raise

        try:
            result = await waiter
        finally:
            self._command_waiters.pop(command_id, None)
        return result

    async def _receiver_loop(self) -> None:
        error: BaseException | None = None
        try:
            assert self._socket is not None
            while True:
                raw_message = await self._socket.recv_text()
                parsed = json.loads(raw_message)
                if not isinstance(parsed, dict):
                    logger.warning("Interactive transport received non-dict payload")
                    continue

                command_id = parsed.get("command_id")
                kind = str(parsed.get("kind", ""))
                if isinstance(command_id, str) and kind in {
                    "hello.ack",
                    "command.ack",
                    "command.error",
                    "pong",
                }:
                    waiter = self._command_waiters.get(command_id)
                    if waiter is not None and not waiter.done():
                        if kind == "command.error":
                            payload = parsed.get("payload", {})
                            detail = "Interactive command failed"
                            status_code = 400
                            if isinstance(payload, dict):
                                detail = str(payload.get("detail") or detail)
                                status_code = int(payload.get("status_code") or status_code)
                            waiter.set_exception(
                                self._command_exception(detail, status_code=status_code)
                            )
                        else:
                            waiter.set_result(parsed)
                    continue

                session_id = parsed.get("session_id")
                if isinstance(session_id, str):
                    seq = parsed.get("seq")
                    if isinstance(seq, int):
                        self._last_seq_by_session[session_id] = seq
                    if kind == "transport.resync_required":
                        payload = parsed.get("payload")
                        if isinstance(payload, dict):
                            self._latest_resync_by_session[session_id] = dict(payload)
                            logger.warning(
                                "Interactive replay miss requires resync | session={} after_seq={} oldest={} latest={}",
                                session_id[:8],
                                payload.get("after_seq"),
                                payload.get("oldest_buffered_seq"),
                                payload.get("latest_seq"),
                            )
                    elif kind == "session.snapshot":
                        payload = parsed.get("payload")
                        if isinstance(payload, dict):
                            self._latest_snapshot_by_session[session_id] = dict(payload)
                    session_queue = self._session_queues.get(session_id)
                    if session_queue is not None:
                        await session_queue.put(parsed)
        except asyncio.CancelledError:
            raise
        except BaseException as exc:
            error = exc
            raise
        finally:
            self._receiver_error = error
            self._reject_pending_commands(error or RuntimeError("Interactive transport closed"))
            for session_queue in self._session_queues.values():
                await session_queue.put(None)
            self._subscribed_sessions.clear()
            self._socket = None
            self._receiver_task = None

    def _reject_pending_commands(self, error: BaseException) -> None:
        for waiter in self._command_waiters.values():
            if not waiter.done():
                waiter.set_exception(error)
        self._command_waiters.clear()

    @staticmethod
    def _command_exception(detail: str, *, status_code: int) -> BaseException:
        if status_code == 401:
            return AuthenticationError(f"401: {detail}")
        return _InteractiveCommandError(detail, status_code=status_code)

    @staticmethod
    def _raw_event_from_envelope(envelope: dict[str, t.Any]) -> dict[str, t.Any] | None:
        kind = str(envelope.get("kind", ""))
        payload = envelope.get("payload")
        payload_dict = payload if isinstance(payload, dict) else {}
        if kind in {"turn.event", "prompt.required", "transport.heartbeat", "turn.cancelled"}:
            raw_event = payload_dict.get("raw_event")
            if isinstance(raw_event, dict):
                return raw_event
        return None
