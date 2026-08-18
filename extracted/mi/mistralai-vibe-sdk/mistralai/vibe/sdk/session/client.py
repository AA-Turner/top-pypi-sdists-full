"""Stateful consumer ergonomics over the stateless Session Protocol."""

import asyncio
from collections import deque
from collections.abc import AsyncGenerator
from copy import deepcopy
from dataclasses import dataclass
from typing import cast

from jsonpatch import JsonPatch
from pydantic import JsonValue

from .models.base import SessionModel
from .models.callbacks import CallbackResult
from .models.common import EventId, TurnId
from .models.configuration import AgentConfig
from .models.content import ContentBlock
from .models.events import (
    CallbackOpenedEvent,
    CallbackResolvedEvent,
    ClientEvent,
    Event,
    EventBatch,
    HistoryEntryAddedEvent,
    HistoryEntryCompletedEvent,
    HistoryEntryPatchedEvent,
    JsonPatchAppendOperation,
    JsonPatchOperation,
    SessionTerminatedEvent,
    SessionUpdatedEvent,
    TransportHeartbeat,
    TransportStreamEnded,
    TransportStreamStarted,
    TurnStartedEvent,
    TurnTerminatedEvent,
    TurnUpdatedEvent,
)
from .models.history import (
    HistoryEntry,
    HistoryEntryAdapter,
)
from .models.state import Page, PageRequest, SessionState, TurnState
from .procedures.session import (
    CallbackResultParams,
    CallbackResultResponse,
    ConfigReadParams,
    ConfigReadResponse,
    ConfigWriteParams,
    ConfigWriteResponse,
    EventsReadParams,
    InfoParams,
    InfoResponse,
    PluginInfoParams,
    PluginInfoResponse,
    PluginReloadParams,
    PluginReloadResponse,
    SessionCompactParams,
    SessionCompactResponse,
    SessionForkParams,
    SessionForkResponse,
    SessionHistoryClearParams,
    SessionHistoryClearResponse,
    SessionHistoryListParams,
    SessionHistoryListResponse,
    SessionReadParams,
    SessionReadResponse,
    SessionStartParams,
    SessionStartResponse,
    SessionTurnsListParams,
    SessionTurnsListResponse,
    TurnInterruptParams,
    TurnInterruptResponse,
    TurnStartParams,
    TurnStartResponse,
    TurnSteerParams,
    TurnSteerResponse,
)
from .transport import SessionTransport


class SessionNotAttachedError(RuntimeError):
    """Raised when a session-bound convenience method has no active session."""


class SessionEventSequenceError(RuntimeError):
    """Raised when a transport violates the session-scoped event contract."""


@dataclass(frozen=True, slots=True)
class _EventStreamFailure:
    error: BaseException


class _EventStreamEndedError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class _QueuedEvent:
    event: ClientEvent


_EVENT_STREAM_ENDED = object()
type _SubscriberItem = _QueuedEvent | _EventStreamFailure | object


@dataclass(frozen=True, slots=True)
class _Subscriber:
    id: int
    queue: asyncio.Queue[_SubscriberItem]


@dataclass(slots=True)
class _PendingDelivery:
    event_id: EventId
    subscriber_ids: set[int]


class SessionClient:
    """Compose stateless Session procedures for one currently attached session."""

    def __init__(self, transport: SessionTransport) -> None:
        self._transport = transport
        self._state: SessionState | None = None
        self._last_event_id: EventId | None = None
        self._latest_received_event_id: EventId | None = None
        self._event_task: asyncio.Task[None] | None = None
        self._event_subscribers: dict[int, _Subscriber] = {}
        self._next_subscriber_id = 0
        self._pending_deliveries: deque[_PendingDelivery] = deque()

    @property
    def state(self) -> SessionState:
        if self._state is None:
            raise SessionNotAttachedError("The Session client is not attached to a session")
        return self._state

    @property
    def session_id(self) -> str:
        return self.state.session.id

    @property
    def last_event_id(self) -> EventId:
        if self._last_event_id is None:
            raise SessionNotAttachedError("The Session client has no event cursor")
        return self._last_event_id

    async def request[ResultT: SessionModel](
        self,
        method: str,
        params: SessionModel,
        result_type: type[ResultT],
    ) -> ResultT:
        """Call a typed shared or namespaced Session procedure."""

        return await self._transport.request(method, params, result_type)

    async def info(self, params: InfoParams | None = None) -> InfoResponse:
        return await self.request("app_server/info", params or InfoParams(), InfoResponse)

    async def start_session(self, params: SessionStartParams) -> SessionStartResponse:
        response = await self.request("app_server/session/start", params, SessionStartResponse)
        await self.adopt_session_snapshot(response.state, response.last_event_id)
        return response

    async def fork_session(self, params: SessionForkParams) -> SessionForkResponse:
        response = await self.request("app_server/session/fork", params, SessionForkResponse)
        await self.adopt_session_snapshot(response.state, response.last_event_id)
        return response

    async def compact_session(self, instructions: str | None = None) -> SessionCompactResponse:
        response = await self.request(
            "app_server/session/compact",
            SessionCompactParams(session_id=self.session_id, instructions=instructions),
            SessionCompactResponse,
        )
        await self.adopt_session_snapshot(response.state, response.last_event_id)
        return response

    async def clear_session_history(
        self, *, idempotency_key: str | None = None
    ) -> SessionHistoryClearResponse:
        response = await self.request(
            "app_server/session/history/clear",
            SessionHistoryClearParams(idempotency_key=idempotency_key, session_id=self.session_id),
            SessionHistoryClearResponse,
        )
        await self.adopt_session_snapshot(response.state, response.last_event_id)
        return response

    async def read_session(
        self,
        *,
        history: PageRequest | None = None,
        turns: PageRequest | None = None,
    ) -> SessionReadResponse:
        response = await self.request(
            "app_server/session/read",
            SessionReadParams(session_id=self.session_id, history=history, turns=turns),
            SessionReadResponse,
        )
        await self.adopt_session_snapshot(response.state, response.last_event_id)
        return response

    async def adopt_session_snapshot(self, state: SessionState, last_event_id: EventId) -> None:
        """Atomically replace local state and restart attached event readers."""

        event_task = self._event_task
        if event_task is not None and not event_task.done():
            event_task.cancel()
            await asyncio.gather(event_task, return_exceptions=True)
        self._event_task = None
        self._pending_deliveries.clear()
        for subscriber in self._event_subscribers.values():
            while not subscriber.queue.empty():
                subscriber.queue.get_nowait()
        self._state = state
        self._last_event_id = last_event_id
        self._latest_received_event_id = last_event_id
        if self._event_subscribers:
            self._event_task = asyncio.create_task(
                self._pump_events(100),
                name=f"session-events:{state.session.id}",
            )

    async def list_history(
        self,
        *,
        turn_id: TurnId | None = None,
        page: PageRequest | None = None,
    ) -> SessionHistoryListResponse:
        return await self.request(
            "app_server/session/history/list",
            SessionHistoryListParams(
                session_id=self.session_id,
                turn_id=turn_id,
                page=page or PageRequest(),
            ),
            SessionHistoryListResponse,
        )

    async def list_turns(self, page: PageRequest | None = None) -> SessionTurnsListResponse:
        return await self.request(
            "app_server/session/turns/list",
            SessionTurnsListParams(session_id=self.session_id, page=page or PageRequest()),
            SessionTurnsListResponse,
        )

    async def start_turn(
        self,
        message: list[ContentBlock],
        *,
        message_entry_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> TurnStartResponse:
        return await self.request(
            "app_server/session/turn/start",
            TurnStartParams(
                idempotency_key=idempotency_key or message_entry_id,
                session_id=self.session_id,
                message_entry_id=message_entry_id,
                message=message,
            ),
            TurnStartResponse,
        )

    async def run_turn(
        self,
        message: list[ContentBlock],
        *,
        message_entry_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> AsyncGenerator[ClientEvent, None]:
        """Start one turn and yield canonical events through its completion."""

        subscriber = self._subscribe_events()
        response: TurnStartResponse | None = None
        terminated = False
        try:
            response = await self.start_turn(
                message,
                message_entry_id=message_entry_id,
                idempotency_key=idempotency_key,
            )
            while True:
                event = await self._next_event(subscriber)
                terminated = (
                    isinstance(event.payload, TurnTerminatedEvent)
                    and event.payload.turn.id == response.turn.id
                )
                yield event
                if terminated:
                    return
        finally:
            self._unsubscribe_events(subscriber)
            if response is not None and not terminated:
                await self.interrupt_turn(response.turn.id)

    async def steer_turn(
        self,
        expected_turn_id: TurnId,
        message: list[ContentBlock],
        *,
        message_entry_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> TurnSteerResponse:
        return await self.request(
            "app_server/session/turn/steer",
            TurnSteerParams(
                idempotency_key=idempotency_key or message_entry_id,
                session_id=self.session_id,
                expected_turn_id=expected_turn_id,
                message_entry_id=message_entry_id,
                message=message,
            ),
            TurnSteerResponse,
        )

    async def interrupt_turn(self, expected_turn_id: TurnId) -> TurnInterruptResponse:
        return await self.request(
            "app_server/session/turn/interrupt",
            TurnInterruptParams(
                session_id=self.session_id,
                expected_turn_id=expected_turn_id,
            ),
            TurnInterruptResponse,
        )

    async def read_config(self) -> ConfigReadResponse:
        return await self.request(
            "app_server/session/config/read",
            ConfigReadParams(session_id=self.session_id),
            ConfigReadResponse,
        )

    async def write_config(self, config: AgentConfig) -> ConfigWriteResponse:
        return await self.request(
            "app_server/session/config/write",
            ConfigWriteParams(session_id=self.session_id, config=config),
            ConfigWriteResponse,
        )

    async def plugin_info(self) -> PluginInfoResponse:
        return await self.request(
            "app_server/session/plugin/info",
            PluginInfoParams(session_id=self.session_id),
            PluginInfoResponse,
        )

    async def reload_plugins(self) -> PluginReloadResponse:
        return await self.request(
            "app_server/session/plugin/reload",
            PluginReloadParams(session_id=self.session_id),
            PluginReloadResponse,
        )

    async def answer_callback(self, result: CallbackResult) -> CallbackResultResponse:
        return await self.request(
            "app_server/session/callback/result",
            CallbackResultParams(session_id=self.session_id, result=result),
            CallbackResultResponse,
        )

    async def events(self, *, batch_size: int = 100) -> AsyncGenerator[ClientEvent, None]:
        """Yield one shared event stream to any number of local subscribers."""

        subscriber = self._subscribe_events(batch_size=batch_size)
        try:
            while True:
                yield await self._next_event(subscriber)
        except _EventStreamEndedError:
            return
        finally:
            self._unsubscribe_events(subscriber)

    async def close(self) -> None:
        task = self._event_task
        if task is not None and not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        self._event_task = None
        self._broadcast(_EVENT_STREAM_ENDED)
        await self._transport.close()

    def _receive_event(self, event: ClientEvent) -> None:
        if event.session_id != self.session_id:
            raise SessionEventSequenceError(
                f"Expected an event for {self.session_id}, received {event.session_id}"
            )
        if event.event_id == self._latest_received_event_id:
            raise SessionEventSequenceError(f"Duplicate Session event: {event.event_id}")
        self._state = _reduce_session_event(self.state, event)
        self._latest_received_event_id = event.event_id

    def _subscribe_events(self, *, batch_size: int = 100) -> _Subscriber:
        self._next_subscriber_id += 1
        subscriber = _Subscriber(self._next_subscriber_id, asyncio.Queue())
        self._event_subscribers[subscriber.id] = subscriber
        if self._event_task is None or self._event_task.done():
            self._event_task = asyncio.create_task(
                self._pump_events(batch_size),
                name=f"session-events:{self.session_id}",
            )
        return subscriber

    def _unsubscribe_events(self, subscriber: _Subscriber) -> None:
        self._event_subscribers.pop(subscriber.id, None)
        if self._event_subscribers:
            for delivery in self._pending_deliveries:
                delivery.subscriber_ids.discard(subscriber.id)
            self._advance_delivery_cursor()
        else:
            self._pending_deliveries.clear()
            self._latest_received_event_id = self._last_event_id
        task = self._event_task
        if not self._event_subscribers and task is not None and not task.done():
            task.cancel()

    async def _next_event(self, subscriber: _Subscriber) -> ClientEvent:
        item = await subscriber.queue.get()
        if item is _EVENT_STREAM_ENDED:
            raise _EventStreamEndedError("The Session event stream ended")
        if isinstance(item, _EventStreamFailure):
            raise item.error
        if not isinstance(item, _QueuedEvent):
            raise TypeError(f"Unexpected Session event stream item: {type(item).__name__}")
        self._acknowledge_delivery(subscriber.id, item.event.event_id)
        return item.event

    async def _pump_events(self, batch_size: int) -> None:
        params = EventsReadParams(
            session_id=self.session_id,
            after_event_id=self.last_event_id,
            batch_size=batch_size,
        )
        try:
            async for item in self._transport.read_events(params):
                if not self._event_subscribers:
                    return
                match item:
                    case Event():
                        self._publish_event(_as_client_event(item))
                    case EventBatch(events=events):
                        for event in events:
                            if not self._event_subscribers:
                                return
                            self._publish_event(_as_client_event(event))
                    case TransportStreamStarted() | TransportHeartbeat() | TransportStreamEnded():
                        continue
        except asyncio.CancelledError:
            raise
        except BaseException as error:
            self._broadcast(_EventStreamFailure(error))
        else:
            self._broadcast(_EVENT_STREAM_ENDED)
        finally:
            if asyncio.current_task() is self._event_task:
                self._event_task = None

    def _publish_event(self, event: ClientEvent) -> None:
        self._receive_event(event)
        subscriber_ids = set(self._event_subscribers)
        if not subscriber_ids:
            return
        self._pending_deliveries.append(
            _PendingDelivery(event_id=event.event_id, subscriber_ids=subscriber_ids)
        )
        self._broadcast(_QueuedEvent(event))

    def _broadcast(self, item: _SubscriberItem) -> None:
        for subscriber in tuple(self._event_subscribers.values()):
            subscriber.queue.put_nowait(item)

    def _acknowledge_delivery(self, subscriber_id: int, event_id: EventId) -> None:
        delivery = next(
            (
                item
                for item in self._pending_deliveries
                if item.event_id == event_id and subscriber_id in item.subscriber_ids
            ),
            None,
        )
        if delivery is None:
            raise SessionEventSequenceError(f"No pending delivery for Session event: {event_id}")
        delivery.subscriber_ids.remove(subscriber_id)
        self._advance_delivery_cursor()

    def _advance_delivery_cursor(self) -> None:
        while self._pending_deliveries and not self._pending_deliveries[0].subscriber_ids:
            self._last_event_id = self._pending_deliveries.popleft().event_id


def _reduce_session_event(state: SessionState, event: ClientEvent) -> SessionState:
    payload = event.payload
    match payload:
        case SessionUpdatedEvent(state=updated) | SessionTerminatedEvent(state=updated):
            return updated
        case HistoryEntryAddedEvent(entry=entry) | HistoryEntryCompletedEvent(entry=entry):
            return state.model_copy(update={"history": _upsert_history(state.history, entry)})
        case HistoryEntryPatchedEvent(entry_id=entry_id, entry_index=entry_index, patches=patches):
            if state.history is None:
                return state
            previous = next(
                (candidate for candidate in state.history.items if candidate.id == entry_id),
                None,
            )
            if previous is None:
                raise SessionEventSequenceError(f"History patch targets unknown entry: {entry_id}")
            if previous.index != entry_index:
                raise SessionEventSequenceError(
                    f"History patch index mismatch for {entry_id}: "
                    f"expected {previous.index}, received {entry_index}"
                )
            try:
                document = previous.model_dump(mode="json", by_alias=True)
                patched = _apply_json_patch(document, patches)
                updated = HistoryEntryAdapter.validate_python(patched)
            except Exception as error:
                raise SessionEventSequenceError(
                    f"Invalid history patch for entry {entry_id}"
                ) from error
            return state.model_copy(update={"history": _upsert_history(state.history, updated)})
        case TurnStartedEvent(turn=turn) | TurnUpdatedEvent(turn=turn):
            active_turn_id = turn.id if turn.status in {"running", "blocked"} else None
            status = "running" if active_turn_id is not None else "waiting"
            return _with_turn(state, turn, active_turn_id, status, event.emitted_at)
        case TurnTerminatedEvent(turn=turn):
            return _with_turn(state, turn, None, "waiting", event.emitted_at)
        case CallbackOpenedEvent(callback=callback):
            callbacks = [
                candidate for candidate in state.active_callbacks if candidate.id != callback.id
            ]
            callbacks.append(callback)
            return state.model_copy(update={"active_callbacks": callbacks})
        case CallbackResolvedEvent(callback_id=callback_id):
            return state.model_copy(
                update={
                    "active_callbacks": [
                        callback
                        for callback in state.active_callbacks
                        if callback.id != callback_id
                    ]
                }
            )
        case _:
            return state


def _upsert_history(
    page: Page[HistoryEntry] | None, entry: HistoryEntry
) -> Page[HistoryEntry] | None:
    if page is None:
        return None
    items = [candidate for candidate in page.items if candidate.id != entry.id]
    items.append(entry)
    items.sort(key=lambda candidate: candidate.index)
    return page.model_copy(update={"items": items})


def _with_turn(
    state: SessionState,
    turn: TurnState,
    active_turn_id: TurnId | None,
    status: str,
    emitted_at: int,
) -> SessionState:
    turns = state.turns
    if turns is not None:
        items = [candidate for candidate in turns.items if candidate.id != turn.id]
        items.append(turn)
        turns = turns.model_copy(update={"items": items})
    session = state.session.model_copy(
        update={
            "status": status,
            "updated_at": max(state.session.updated_at, emitted_at),
        }
    )
    return state.model_copy(
        update={
            "session": session,
            "active_turn_id": active_turn_id,
            "turns": turns,
        }
    )


def _as_client_event(event: Event) -> ClientEvent:
    if isinstance(event, ClientEvent):
        return event
    return ClientEvent.model_validate(event.model_dump(mode="json", by_alias=True))


def _apply_json_patch(
    document: dict[str, JsonValue],
    patches: list[JsonPatchOperation],
) -> dict[str, JsonValue]:
    current = cast(dict[str, JsonValue], deepcopy(document))
    for patch in patches:
        if isinstance(patch, JsonPatchAppendOperation):
            _apply_append_patch(current, patch)
            continue
        operation = patch.model_dump(mode="json", by_alias=True)
        current = cast(dict[str, JsonValue], JsonPatch([operation]).apply(current))
    return current


def _apply_append_patch(document: JsonValue, patch: JsonPatchAppendOperation) -> None:
    parent, key = _resolve_json_pointer_parent(document, patch.path)
    if isinstance(parent, dict):
        value = parent.get(key)
        if not isinstance(value, str):
            raise ValueError(f"JSON Patch append target is not a string: {patch.path}")
        parent[key] = value + patch.value
        return
    if isinstance(parent, list):
        if key == "-":
            raise ValueError("JSON Patch append cannot target a new list element")
        index = _parse_json_pointer_index(key, len(parent))
        value = parent[index]
        if not isinstance(value, str):
            raise ValueError(f"JSON Patch append target is not a string: {patch.path}")
        parent[index] = value + patch.value
        return
    raise ValueError(f"JSON Patch append target parent is not a container: {patch.path}")


def _resolve_json_pointer_parent(document: JsonValue, path: str) -> tuple[JsonValue, str]:
    tokens = _json_pointer_tokens(path)
    if not tokens:
        raise ValueError("JSON Patch append cannot target the document root")
    current: JsonValue = document
    for token in tokens[:-1]:
        if isinstance(current, dict):
            if token not in current:
                raise ValueError(f"JSON Pointer path does not exist: {path}")
            current = current[token]
        elif isinstance(current, list):
            current = current[_parse_json_pointer_index(token, len(current))]
        else:
            raise ValueError(f"JSON Pointer path crosses a scalar: {path}")
    return current, tokens[-1]


def _json_pointer_tokens(path: str) -> list[str]:
    if path == "":
        return []
    if not path.startswith("/"):
        raise ValueError(f"Invalid JSON Pointer path: {path}")
    return [token.replace("~1", "/").replace("~0", "~") for token in path[1:].split("/")]


def _parse_json_pointer_index(token: str, length: int) -> int:
    if not token.isdigit():
        raise ValueError(f"JSON Pointer list token is not an index: {token}")
    index = int(token)
    if index >= length:
        raise ValueError(f"JSON Pointer list index is out of range: {token}")
    return index


__all__ = [
    "SessionClient",
    "SessionEventSequenceError",
    "SessionNotAttachedError",
]
