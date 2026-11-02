"""Typed HTTP client for the vibe_agents sessions API."""

import asyncio
import contextlib
import json
import time
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from http import HTTPMethod, HTTPStatus
from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload
from uuid import UUID, uuid4

import httpx
import structlog
from pydantic import BaseModel, ValidationError

from mistralai.vibe_agents._http import _InternalHTTPClient
from mistralai.vibe_agents.session_workflow import (
    AGENTS_SDK_COMMAND_SOURCE,
    CallbackResultPayload,
    CommandMetadata,
    JsonObject,
    MessageInput,
    SessionAgentCustomization,
    SessionWorkflowCommand,
    SessionWorkflowSubscription,
)
from mistralai.vibe_agents.sessions_client.api_models import (
    AgentSessionResponse,
    ArchiveSessionRequest,
    CancelAgentSessionRequest,
    IdempotencyKey,
    InterruptAgentSessionRequest,
    ListSessionsResult,
    ObservedControllerEventResponse,
    RenameSessionRequest,
    RootsScopeInput,
    SessionCatalogScopeInput,
    SessionEventsHistoryResponse,
    SessionProtocol,
    StartAgentSessionRequest,
    StartAgentSessionResponse,
    SubmitAgentMessageRequest,
    SubmitAgentMessageResponse,
    SubmitCallbackResultRequest,
    SubmitCallbackResultResponse,
)
from mistralai.vibe_agents.sessions_client.rendered_session import (
    Callback,
    SessionRenderer,
)

if TYPE_CHECKING:
    from mistralai.vibe.harness.app_server.session import (
        CallbacksTreeResponse,
        ContentBlock,
        ContextMessage,
        InitialTurn,
        SessionModel,
    )
    from mistralai.vibe.harness.app_server.session.models.common import HistoryEntryId
    from mistralai.vibe_agents.sessions_client.api_models_v1 import MessageSendResponse
    from mistralai.vibe_agents.sessions_client.rendered_session_v1 import RenderedSessionV1

logger = structlog.get_logger(__name__)

_RETRYABLE_STATUS_CODES = [502, 503, 504]
_SSE_DATA_PREFIX = "data: "

_T_APIModel = TypeVar("_T_APIModel", bound=BaseModel)
# The Session protocol routes, ``POST /sessions/{id}/<route>``.
type ProcedureRoute = Literal["message/send", "turn/start", "turn/steer", "turn/interrupt", "cancel", "callback/result"]
RendererT = TypeVar("RendererT", bound=SessionRenderer)


def _parse_sse_data_line(line: str, model: type[_T_APIModel]) -> _T_APIModel | None:
    """Return a parsed frame for ``data: <json>`` lines; ``None`` otherwise.

    The vibe_agents SSE endpoints emit one event per
    ``id: ... / event: ... / data: <json>`` triplet separated by a blank
    line. We only consume the ``data:`` line; sequence/cursor metadata
    lives inside the JSON payload.
    """
    if not line or not line.startswith(_SSE_DATA_PREFIX):
        return None
    payload = line[len(_SSE_DATA_PREFIX) :].strip()
    if not payload:
        return None
    try:
        return model.model_validate(json.loads(payload))
    except (json.JSONDecodeError, ValidationError) as error:
        # A single malformed frame must not tear down the whole stream: skip it and
        # keep folding subsequent events, mirroring RenderedSession's count-and-continue.
        logger.debug("Skipping malformed SSE frame", model=model.__name__, error=str(error))
        return None


class SessionsAPIError(httpx.HTTPStatusError):
    """The sessions API answered with an error status.

    The message includes the server's ``detail``, so a refusal reads the same in a
    traceback as in the response body. ``detail`` holds it as the server sent it: a
    string, a coded object, or ``None`` when the body has none. Callers that check
    ``response.status_code`` on an ``httpx.HTTPStatusError`` keep working.
    """

    def __init__(self, error: httpx.HTTPStatusError) -> None:
        response = error.response
        self.detail = _response_detail(response)
        request = error.request
        status = f"{response.status_code} {response.reason_phrase}"
        message = f"Sessions API answered {status} to {request.method} {request.url.path}"
        detail_message = _detail_message(self.detail)
        if detail_message:
            message = f"{message}: {detail_message}"
        super().__init__(message, request=request, response=response)


async def _raise_for_status(response: httpx.Response) -> None:
    """Raise ``SessionsAPIError`` on an error status, for plain and streamed responses alike."""

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        # A streamed response has not read its body yet, and the detail is in it.
        await response.aread()
        raise SessionsAPIError(error) from None


def _response_detail(response: httpx.Response) -> object:
    try:
        body = response.json()
    except ValueError:
        return None
    return body.get("detail") if isinstance(body, dict) else None


def _detail_message(detail: object) -> str | None:
    """The human message of a ``detail``, which is a string or a coded object."""

    if isinstance(detail, dict):
        detail = detail.get("message") or detail.get("code")
    return str(detail) if detail else None


def _default_renderer() -> SessionRenderer:
    from mistralai.vibe_agents.sessions_client.rendered_session_v1 import RenderedSessionV1  # noqa: PLC0415

    return RenderedSessionV1()


class SessionCommandRejectedError(RuntimeError):
    """The Session refused a compare-and-set command.

    Raised when a steer or interrupt named a Turn with ``expected_turn_id`` and the Session
    is running a different one. The command reached the Session and was deliberately not
    applied, so an unchanged retry fails the same way.
    """


def _raise_if_command_rejected(error: httpx.HTTPStatusError, *, expected_turn_id: str | None) -> None:
    """Turn a 409 on a Turn-scoped command into the typed refusal.

    Takes the raised error rather than the response because ``_request`` calls
    ``raise_for_status``: by the time a caller sees a refusal it is already an exception,
    and a check against the response would never run.

    Only a command that named a Turn can be refused for naming the wrong one. 409 also
    answers a reused ``command_id``, which is a different mistake and stays an HTTP error.
    """

    if expected_turn_id is None or error.response.status_code != HTTPStatus.CONFLICT:
        return
    detail: object = None
    with contextlib.suppress(ValueError):
        body = error.response.json()
        detail = body.get("detail") if isinstance(body, dict) else None
    raise SessionCommandRejectedError(str(detail) if detail else "The Session refused the command as stale") from error


def _is_transient_stream_status(status_code: int) -> bool:
    """Statuses worth reconnecting on when opening ``/events``.

    Opening ``/events`` can transiently return 404 (session-event-projector
    read-after-write race) or 5xx (rolling deploy with no Ready replica); both
    clear on a retry within the deadline rather than being real failures.
    """
    return status_code == 404 or status_code >= 500


class SessionsClient(_InternalHTTPClient):
    """Typed client for the vibe_agents sessions HTTP API."""

    async def create_session(
        self,
        *,
        initial_command: SessionWorkflowCommand | None = None,
        agent_name: str | None = None,
        agent: SessionAgentCustomization | dict[str, str] | None = None,
        app_context: JsonObject | None = None,
        initial_subscriptions: tuple[SessionWorkflowSubscription, ...] = (),
        idempotency_key: IdempotencyKey | None = None,
        session_protocol: SessionProtocol | None = SessionProtocol.SESSION_V1,
        session_inputs: JsonObject | None = None,
        initial_turn: "InitialTurn | None" = None,
    ) -> StartAgentSessionResponse:
        """Create a session.

        ``idempotency_key`` (1 to 256 characters) names the create call for
        exact retries: a retry by the same caller with the same key returns the
        same session, and a different request with the same key is refused with
        409. Defaults to a fresh key per call, so every call starts a new
        session: if your call site retries, pass a UUID generated once per
        request.

        ``session_protocol`` selects the session event format and is fixed
        for the life of the session. It defaults to
        ``SessionProtocol.SESSION_V1``, the canonical Session v1 events the
        UI traces are built from. Pass
        ``SessionProtocol.LEGACY_TASK_PROTOCOL`` to opt into the legacy task
        protocol, or ``None`` for the server default.

        ``session_inputs`` carries the Session inputs keyed by input ID,
        fixed for the Session's lifetime.

        ``initial_turn`` starts the Session with its first Turn, whose ID the
        response's ``initial_turn`` names. It needs a Unified Harness Session
        on Session v1. A control plane that predates it answers 422.
        """
        if idempotency_key is None:
            # One key per call: the transport's 502/503/504 retries reuse it.
            idempotency_key = str(uuid4())
        initial_turn_json: JsonObject | None = None
        if initial_turn is not None:
            # A control plane that predates context messages refuses the key, even empty.
            initial_turn_json = initial_turn.model_dump(
                mode="json",
                exclude_none=True,
                exclude=None if initial_turn.context_messages else {"context_messages"},
            )
        body = StartAgentSessionRequest(
            idempotency_key=idempotency_key,
            agent_name=agent_name,
            agent=SessionAgentCustomization.model_validate(agent) if agent is not None else None,
            initial_command=initial_command,
            app_context=app_context,
            initial_subscriptions=list(initial_subscriptions),
            session_protocol=session_protocol,
            session_inputs=session_inputs,
            initial_turn=initial_turn_json,
        )
        response = await self._request(
            HTTPMethod.POST,
            "/sessions",
            json=body.model_dump(mode="json"),
        )
        return StartAgentSessionResponse.model_validate(response.json())

    async def get_session(
        self,
        *,
        agent_session_id: UUID,
    ) -> AgentSessionResponse:
        response = await self._request(
            HTTPMethod.GET,
            f"/sessions/{agent_session_id}",
        )
        return AgentSessionResponse.model_validate(response.json())

    async def list_sessions(
        self,
        *,
        scope: SessionCatalogScopeInput | None = None,
        include_archived: bool = False,
        limit: int = 50,
        cursor: str | None = None,
    ) -> ListSessionsResult:
        params = (scope or RootsScopeInput()).model_dump(mode="json")
        params.update({"include_archived": str(include_archived).lower(), "limit": limit})
        if cursor is not None:
            params["cursor"] = cursor
        response = await self._request(HTTPMethod.GET, "/sessions", params=params)
        return ListSessionsResult.model_validate(response.json())

    async def rename_session(self, *, agent_session_id: UUID, title: str | None) -> AgentSessionResponse:
        body = RenameSessionRequest(title=title)
        response = await self._request(
            HTTPMethod.POST, f"/sessions/{agent_session_id}/rename", json=body.model_dump(mode="json")
        )
        return AgentSessionResponse.model_validate(response.json())

    async def archive_session(self, *, agent_session_id: UUID, archived: bool = True) -> AgentSessionResponse:
        body = ArchiveSessionRequest(archived=archived)
        response = await self._request(
            HTTPMethod.POST, f"/sessions/{agent_session_id}/archive", json=body.model_dump(mode="json")
        )
        return AgentSessionResponse.model_validate(response.json())

    async def submit_message(
        self,
        *,
        agent_session_id: UUID,
        message: MessageInput,
        source: str = AGENTS_SDK_COMMAND_SOURCE,
        command_id: UUID | None = None,
        metadata: CommandMetadata | None = None,
        expected_turn_id: str | None = None,
    ) -> SubmitAgentMessageResponse:
        """Submit a follow-up user message to an existing session.

        ``command_id`` is the client-owned message-submission identity;
        retries that reuse the same id are deduplicated by the server.
        Defaults to ``uuid4()`` when ``None``, fine for one-shot calls
        but defeats caller-level retry — pass an explicit value if your
        call site retries on transient errors the SDK does not auto-retry.
        Reusing the same ``command_id`` for a different message is a
        client contract violation per the server schema.
        """
        body = SubmitAgentMessageRequest(
            command_id=command_id if command_id is not None else uuid4(),
            source=source,
            message=message,
            metadata=metadata,
            expected_turn_id=expected_turn_id,
        )
        try:
            response = await self._request(
                HTTPMethod.POST,
                f"/sessions/{agent_session_id}/commands",
                json=body.model_dump(mode="json"),
            )
        except httpx.HTTPStatusError as error:
            _raise_if_command_rejected(error, expected_turn_id=expected_turn_id)
            raise
        return SubmitAgentMessageResponse.model_validate(response.json())

    async def send_message(
        self,
        *,
        agent_session_id: UUID,
        message: "Sequence[ContentBlock]",
        idempotency_key: IdempotencyKey,
        context_messages: "Sequence[ContextMessage]" = (),
        message_entry_id: "HistoryEntryId | None" = None,
        source: str = AGENTS_SDK_COMMAND_SOURCE,
    ) -> "MessageSendResponse":
        """Harness ``app_server/session/message/send``: start a Turn or steer the running one.

        A retry with the same ``idempotency_key``, message, ``message_entry_id`` and
        ``context_messages`` returns the original receipt. ``message_entry_id`` names the user
        message entry; without it, the Session derives one from the key. ``context_messages`` reach
        the model only: history, snapshots, and events never show them.
        ``source`` names the calling product, as on the other commands.
        Refusals stay ``httpx.HTTPStatusError``: 429 when the Session applied nothing yet (retry;
        ``detail.code`` is ``session_busy``, ``intake_overloaded`` or ``session_continuing``),
        409 with ``detail.code`` ``idempotency_conflict``, 410 for a Session that takes no more
        messages, 422 for a message it never takes, 501 when it cannot serve this procedure, and
        503 for an unknown outcome.
        """

        # Loaded on first use, so importing sessions_client does not load the Harness.
        from mistralai.vibe_agents.sessions_client import api_models_v1  # noqa: PLC0415

        return await self._post_procedure(
            agent_session_id=agent_session_id,
            route="message/send",
            body=api_models_v1.MessageSendRequest(
                idempotency_key=idempotency_key,
                message=list(message),
                context_messages=list(context_messages),
                message_entry_id=message_entry_id,
                source=source,
            ),
            response_type=api_models_v1.MessageSendResponse,
            # A control plane that predates context messages refuses the key, even empty.
            exclude=None if context_messages else {"context_messages"},
        )

    async def _post_procedure[ResponseT: "SessionModel"](
        self,
        *,
        agent_session_id: UUID,
        route: ProcedureRoute,
        body: "SessionModel",
        response_type: type[ResponseT],
        exclude: set[str] | None = None,
    ) -> ResponseT:
        """Call a Session protocol route; the remote transport owns its retries and fallback.

        Private to the SDK while the transport falls back to ``/commands`` on a control plane
        without the route. Refusals stay ``httpx.HTTPStatusError``.
        """

        response = await self._request(
            HTTPMethod.POST,
            f"/sessions/{agent_session_id}/{route}",
            json=body.model_dump(mode="json", exclude_none=True, exclude=exclude),
        )
        procedure_response: ResponseT = response_type.model_validate(response.json())
        return procedure_response

    async def interrupt_session(
        self,
        *,
        agent_session_id: UUID,
        expected_turn_id: str,
        source: str = AGENTS_SDK_COMMAND_SOURCE,
        reason: str = "interrupt requested",
        command_id: UUID | None = None,
    ) -> SubmitAgentMessageResponse:
        body = InterruptAgentSessionRequest(
            command_id=command_id if command_id is not None else uuid4(),
            source=source,
            expected_turn_id=expected_turn_id,
            reason=reason,
        )
        try:
            response = await self._request(
                HTTPMethod.POST,
                f"/sessions/{agent_session_id}/commands",
                json=body.model_dump(mode="json"),
            )
        except httpx.HTTPStatusError as error:
            _raise_if_command_rejected(error, expected_turn_id=expected_turn_id)
            raise
        return SubmitAgentMessageResponse.model_validate(response.json())

    async def submit_callback_result(
        self,
        *,
        agent_session_id: UUID,
        callback_id: UUID,
        result: CallbackResultPayload,
    ) -> SubmitCallbackResultResponse:
        body = SubmitCallbackResultRequest(result=result)
        response = await self._request(
            HTTPMethod.POST,
            f"/sessions/{agent_session_id}/callbacks/{callback_id}",
            json=body.model_dump(mode="json"),
        )
        return SubmitCallbackResultResponse.model_validate(response.json())

    async def read_session_events_history(
        self,
        *,
        agent_session_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> SessionEventsHistoryResponse:
        """Read finite projected event history at ``/events/history``."""
        params: dict[str, str] = {"limit": str(limit)}
        if cursor is not None:
            params["cursor"] = cursor

        response = await self._request(
            HTTPMethod.GET,
            f"/sessions/{agent_session_id}/events/history",
            params=params,
        )
        return SessionEventsHistoryResponse.model_validate(response.json())

    async def stream_session_events(
        self,
        *,
        agent_session_id: UUID,
        cursor: str | None = None,
        on_open: Callable[[], None] | None = None,
        on_activity: Callable[[], None] | None = None,
    ) -> AsyncIterator[ObservedControllerEventResponse]:
        """Tail the controller-compatible session stream at ``/events``.

        ``on_open`` is called when the server accepts the stream, before the first event.
        ``on_activity`` is called for each line the server sends, heartbeat comments included. An
        open stream can stay quiet for minutes, but the server sends a heartbeat every 15 seconds,
        so activity shows that a reconnected stream works.
        """
        params: dict[str, str] = {}
        if cursor is not None:
            params["cursor"] = cursor

        stream_ctx = await self.stream(
            HTTPMethod.GET,
            f"/sessions/{agent_session_id}/events",
            params=params,
        )
        async with stream_ctx as response:
            await _raise_for_status(response)
            if on_open is not None:
                on_open()
            async for line in response.aiter_lines():
                if on_activity is not None:
                    on_activity()
                event = _parse_sse_data_line(line, ObservedControllerEventResponse)
                if event is not None:
                    yield event

    async def read_session_callbacks(self, *, agent_session_id: UUID) -> "CallbacksTreeResponse":
        """Read the open callbacks of a Session and its descendants at ``/callbacks``."""

        # Loaded on first use, so importing sessions_client does not load the Harness.
        from mistralai.vibe_agents.sessions_client import api_models_v1  # noqa: PLC0415

        response = await self._request(HTTPMethod.GET, f"/sessions/{agent_session_id}/callbacks")
        callbacks: CallbacksTreeResponse = api_models_v1._SessionCallbacksResponse.model_validate(response.json())
        return callbacks

    async def stream_session_callbacks(
        self,
        *,
        agent_session_id: UUID,
        on_open: Callable[[], None] | None = None,
        on_activity: Callable[[], None] | None = None,
    ) -> AsyncIterator["CallbacksTreeResponse"]:
        """Follow ``/callbacks/stream``: the full list of open callbacks, again on each change.

        ``on_open`` and ``on_activity`` work as on ``stream_session_events``.
        """

        from mistralai.vibe_agents.sessions_client import api_models_v1  # noqa: PLC0415

        stream_ctx = await self.stream(HTTPMethod.GET, f"/sessions/{agent_session_id}/callbacks/stream")
        async with stream_ctx as response:
            await _raise_for_status(response)
            if on_open is not None:
                on_open()
            async for line in response.aiter_lines():
                if on_activity is not None:
                    on_activity()
                frame = _parse_sse_data_line(line, api_models_v1._SessionCallbacksResponse)
                if frame is not None:
                    yield frame

    @overload
    async def stream_until(
        self,
        *,
        agent_session_id: UUID,
        until: Callable[["RenderedSessionV1"], bool],
        timeout_seconds: float = ...,
        reconnect_delay_seconds: float = ...,
        renderer: None = None,
    ) -> "RenderedSessionV1": ...

    @overload
    async def stream_until(
        self,
        *,
        agent_session_id: UUID,
        until: Callable[[RendererT], bool],
        timeout_seconds: float = ...,
        reconnect_delay_seconds: float = ...,
        renderer: RendererT,
    ) -> RendererT: ...

    async def stream_until(
        self,
        *,
        agent_session_id: UUID,
        until: Callable[[Any], bool],
        timeout_seconds: float = 120.0,
        reconnect_delay_seconds: float = 1.0,
        renderer: SessionRenderer | None = None,
    ) -> SessionRenderer:
        """Fold ``/events`` into a rendered session until ``until`` holds.

        Observation only: the stream stays open between events, so this reads
        frames as they arrive and returns as soon as ``until`` is satisfied. To
        drive a session and answer its callbacks, use ``stream_until_waiting``.
        On a transient stream error within the deadline it reconnects, resuming
        the same rendered session from the last cursor.

        ``renderer`` defaults to a ``RenderedSessionV1``, matching the
        ``create_session`` default. Pass a legacy :class:`RenderedSession` for a
        session started with ``SessionProtocol.LEGACY_TASK_PROTOCOL``; the two
        event formats never mix on one session, so the renderer is chosen once
        alongside the protocol.
        """
        deadline = time.monotonic() + timeout_seconds
        rendered = renderer if renderer is not None else _default_renderer()
        cursor: str | None = None
        while time.monotonic() < deadline:
            try:
                async for observed in self.stream_session_events(agent_session_id=agent_session_id, cursor=cursor):
                    cursor = observed.sequence
                    rendered.apply_public_session_event(observed.event)
                    if until(rendered):
                        return rendered
                    if time.monotonic() >= deadline:
                        break
            except httpx.TransportError:
                pass
            except httpx.HTTPStatusError as error:
                # _raise_for_status fires inside stream_session_events; reconnect
                # on a transient open, surface anything else (e.g. 401/403).
                if not _is_transient_stream_status(error.response.status_code):
                    raise
            await asyncio.sleep(reconnect_delay_seconds)
        raise TimeoutError(f"session {agent_session_id} did not reach the awaited state within {timeout_seconds:g}s")

    @overload
    async def stream_until_waiting(
        self,
        *,
        agent_session_id: UUID,
        on_callback: Callable[[Callback], Awaitable[CallbackResultPayload | None]] | None = None,
        timeout_seconds: float = ...,
        reconnect_delay_seconds: float = ...,
        renderer: None = None,
    ) -> "RenderedSessionV1": ...

    @overload
    async def stream_until_waiting(
        self,
        *,
        agent_session_id: UUID,
        on_callback: Callable[[Callback], Awaitable[CallbackResultPayload | None]] | None = None,
        timeout_seconds: float = ...,
        reconnect_delay_seconds: float = ...,
        renderer: RendererT,
    ) -> RendererT: ...

    async def stream_until_waiting(
        self,
        *,
        agent_session_id: UUID,
        on_callback: Callable[[Callback], Awaitable[CallbackResultPayload | None]] | None = None,
        timeout_seconds: float = 120.0,
        reconnect_delay_seconds: float = 1.0,
        renderer: SessionRenderer | None = None,
    ) -> SessionRenderer:
        """Drive the session until it is waiting for user input.

        Returns once the session is blocked on the user, which is signaled two
        ways:

        - the agent handed control back, surfaced as ``waiting_for_input`` on the
          renderer (legacy: the ``workflow_status = waiting_for_input`` state row;
          Session v1: a waiting session status or a terminated turn). This is the
          ordinary between-turn wait; the next turn is delivered as a message via
          ``submit_message``.
        - an unanswered waiting callback (legacy ``ask_user_question``; Session v1
          ``user_input`` / ``approval`` / ``client_tool``), which does not flip the status, so the
          callback itself is the only signal. ``on_callback`` (when given) is
          offered each actionable callback and may answer it via the callback API;
          the wait returns once a waiting callback is left unanswered
          (``on_callback`` is absent or returned ``None``).

        ``renderer`` defaults to a ``RenderedSessionV1``; pass a legacy
        :class:`RenderedSession` for a ``SessionProtocol.LEGACY_TASK_PROTOCOL``
        session.
        """
        deadline = time.monotonic() + timeout_seconds
        rendered = renderer if renderer is not None else _default_renderer()
        cursor: str | None = None
        answered: set[UUID] = set()
        while time.monotonic() < deadline:
            try:
                async for observed in self.stream_session_events(agent_session_id=agent_session_id, cursor=cursor):
                    cursor = observed.sequence
                    rendered.apply_public_session_event(observed.event)
                    callback = await self._answer_callback(
                        agent_session_id=agent_session_id,
                        event=observed.event,
                        renderer=rendered,
                        on_callback=on_callback,
                        answered=answered,
                    )
                    if callback is not None and callback.is_waiting and callback.id not in answered:
                        return rendered
                    if rendered.waiting_for_input:
                        return rendered
                    if time.monotonic() >= deadline:
                        break
            except httpx.TransportError:
                pass
            except httpx.HTTPStatusError as error:
                # _raise_for_status fires inside stream_session_events; reconnect
                # on a transient open, surface anything else (e.g. 401/403).
                if not _is_transient_stream_status(error.response.status_code):
                    raise
            await asyncio.sleep(reconnect_delay_seconds)
        raise TimeoutError(f"session {agent_session_id} was not waiting for input within {timeout_seconds:g}s")

    async def _answer_callback(
        self,
        *,
        agent_session_id: UUID,
        event: dict[str, Any],
        renderer: SessionRenderer,
        on_callback: Callable[[Callback], Awaitable[CallbackResultPayload | None]] | None,
        answered: set[UUID],
    ) -> Callback | None:
        """Offer the event's callback (if any) to ``on_callback`` and submit a result.

        Returns the callback the event carried, answered or not, so callers can
        detect when the session is blocked waiting for input.
        """
        callback = renderer.callback_from_event(event)
        if callback is None or on_callback is None or callback.id in answered:
            return callback
        result = await on_callback(callback)
        if result is not None:
            await self.submit_callback_result(
                agent_session_id=agent_session_id,
                callback_id=callback.id,
                result=result,
            )
            answered.add(callback.id)
            # The renderer is re-read for ``waiting_for_input`` right after this
            # returns, so an answered callback has to stop counting as blocking.
            renderer.resolve_callback(callback.id)
        return callback

    async def cancel_session(
        self,
        *,
        agent_session_id: UUID,
        source: str = AGENTS_SDK_COMMAND_SOURCE,
        reason: str = "cancel requested",
        command_id: UUID | None = None,
    ) -> SubmitAgentMessageResponse:
        """Terminally cancel a Session and return its durable command receipt."""

        body = CancelAgentSessionRequest(
            command_id=command_id if command_id is not None else uuid4(),
            source=source,
            reason=reason,
        )
        response = await self._request(
            HTTPMethod.POST,
            f"/sessions/{agent_session_id}/commands",
            json=body.model_dump(mode="json"),
        )
        return SubmitAgentMessageResponse.model_validate(response.json())

    async def _request(
        self,
        method: HTTPMethod,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        response = await self.make_request(
            method,
            path,
            retries_codes=_RETRYABLE_STATUS_CODES,
            **kwargs,
        )
        await _raise_for_status(response)
        return response


__all__ = [
    "SessionCommandRejectedError",
    "SessionsAPIError",
    "SessionsClient",
]
