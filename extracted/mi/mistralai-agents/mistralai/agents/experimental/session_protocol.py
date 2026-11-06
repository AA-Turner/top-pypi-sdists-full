"""The raw Session protocol client: the advanced fallback under the session handles.

``attach(session)`` gives a ``SessionClient`` for an ``agents.Session`` handle. Its methods send
one Session protocol procedure each (``upload_file`` sends none: the client uploads), and return
the protocol's own models, which this module re-exports with the protocol's errors. Other errors
come from the host: on both hosts, an event cursor that is not valid raises ``agents.InvalidCursorError``,
and another request the host refuses (an invalid page, a ``write_config`` change a local session does
not allow) raises an ``agents.AgentsError``; a deployment-backed session also raises a
``LookupError`` for a session the server does not know, a ``RuntimeError`` when it cannot tell
whether a command took effect, and ``httpx.HTTPStatusError`` for another HTTP error. Use it for
what the handles do not do yet: answer a client tool, upload a file to a local session, rename
or archive a session, list its turns, read its history page by page, or change a local session's
configuration.

This module is experimental: a minor release may change it. Importing or using it gives no warning.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable, Collection
from contextlib import aclosing, asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Protocol, Self

import temporalio.workflow

from mistralai.agents import _silence

# A direct `import mistralai.agents.experimental.session_protocol` bypasses the parent packages'
# lazy `__getattr__`, so apply the same Temporal passthrough and log quieting here.
with temporalio.workflow.unsafe.imports_passed_through():
    _silence.presilence()
    try:
        from mistralai.vibe_agents.sdk.quiet import quiet_local_sdk_logs

        quiet_local_sdk_logs()
        from mistralai.vibe.harness.app_server import session as _protocol
        from mistralai.vibe.harness.app_server.session import (
            AgentConfig,
            ApprovalCallback,
            ArtifactCreatedEvent,
            AudioContentBlock,
            AuthCallback,
            AuthRequest,
            AuthResult,
            CallbackKind,
            CallbackOpenedEvent,
            CallbackResolvedEvent,
            CallbackResult,
            CallbackResultResponse,
            CatalogArchiveResponse,
            CatalogListResponse,
            CatalogRenameResponse,
            ChildSessionProcedureRefusedError,
            ClientEvent,
            ClientHookCallback,
            ClientToolCallback,
            ConfigReadResponse,
            ConfigWriteResponse,
            ContentBlock,
            DirectChildrenScope,
            EmbeddedResourceContentBlock,
            ErrorEvent,
            Event,
            EventBatch,
            EventId,
            EventsReadParams,
            ExecuteCodeCallback,
            HistoryEntryAddedEvent,
            HistoryEntryCompletedEvent,
            HistoryEntryPatchedEvent,
            ImageContentBlock,
            InfoParams,
            InfoResponse,
            ListPageRequest,
            MessageSendResponse,
            NoticeEvent,
            PageRequest,
            PromptSuggestedEvent,
            ResourceLinkContentBlock,
            RootsScope,
            SessionBusyError,
            SessionCallback,
            SessionCallbackRejectedError,
            SessionCallbackSettledError,
            SessionCancelResponse,
            SessionCatalogScope,
            SessionEventStreamLostError,
            SessionHistoryListResponse,
            SessionIdempotencyConflictError,
            SessionMessageRejectedError,
            SessionNotAttachedError,
            SessionReadResponse,
            SessionTerminatedError,
            SessionTerminatedEvent,
            SessionTransport,
            SessionTurnConflictError,
            SessionTurnsListResponse,
            SessionUpdatedEvent,
            StartSubagentCallback,
            SubagentsListResponse,
            TextContentBlock,
            TreeScope,
            TurnId,
            TurnInterruptResponse,
            TurnStartedEvent,
            TurnStartResponse,
            TurnSteerResponse,
            TurnTerminatedEvent,
            TurnUpdatedEvent,
            UnknownContentBlock,
            UnknownEventPayload,
            UnknownValue,
            UnsupportedSessionProcedureError,
            UserInputCallback,
        )
        from mistralai.vibe.harness.app_server.session import SessionClient as _HarnessSessionClient
        from mistralai.vibe.harness.app_server.session.file_upload import FileUploader as _FileUploader
        from mistralai.vibe.harness.app_server.session.local_record import (
            LocalSessionCallbackSettledError as _LocalSessionCallbackSettledError,
        )
        from mistralai.vibe.harness.app_server.session.local_record import (
            LocalSessionProcedureError as _LocalSessionProcedureError,
        )
        from mistralai.vibe.harness.app_server.session.models import AllowApproval, DenyApproval
        from mistralai.vibe.harness.app_server.session.models.base import SessionModel as _SessionModel
        from mistralai.vibe.harness.app_server.session.models.common import (
            DEFAULT_INTERRUPT_REASON as _DEFAULT_INTERRUPT_REASON,
        )
        from mistralai.vibe.harness.app_server.session.models.common import HistoryEntryId
        from mistralai.vibe_agents.sdk.authoring import errors as _errors
        from mistralai.vibe_agents.sdk.authoring.contracts import KeepCallbackOpen
        from mistralai.vibe_agents.sdk.authoring.errors import SdkError
        from mistralai.vibe_agents.sdk.authoring.errors import described_value as _described
        from mistralai.vibe_agents.sdk.client.handles import Session as _Session
    finally:
        _silence.restore_runtime_warning_levels()


__all__ = [
    # The client
    "SessionClient",
    "attach",
    # Arguments and results of its methods
    "AgentConfig",
    "ApprovalResult",
    "CallbackHandler",
    "CallbackKind",
    "CallbackResult",
    "CallbackResultResponse",
    "CatalogArchiveResponse",
    "CatalogListResponse",
    "CatalogRenameResponse",
    "ClientEvent",
    "ConfigReadResponse",
    "ConfigWriteResponse",
    "DirectChildrenScope",
    "EventId",
    "InfoParams",
    "InfoResponse",
    "ListPageRequest",
    "MessageSendResponse",
    "PageRequest",
    "RootsScope",
    "SessionCancelResponse",
    "SessionCatalogScope",
    "SessionHistoryListResponse",
    "SessionReadResponse",
    "SessionTurnsListResponse",
    "SubagentsListResponse",
    "TreeScope",
    "TurnId",
    "TurnInterruptResponse",
    "TurnStartResponse",
    "TurnSteerResponse",
    # A value a newer host added to a closed set, such as a status this client does not know
    "UnknownValue",
    # Content blocks
    "AudioContentBlock",
    "ContentBlock",
    "EmbeddedResourceContentBlock",
    "ImageContentBlock",
    "ResourceLinkContentBlock",
    "TextContentBlock",
    "UnknownContentBlock",
    # Callbacks
    "ApprovalCallback",
    "AuthCallback",
    "AuthRequest",
    "AuthResult",
    "ClientHookCallback",
    "ClientToolCallback",
    "ExecuteCodeCallback",
    "SessionCallback",
    "StartSubagentCallback",
    "UserInputCallback",
    # Event payloads
    "ArtifactCreatedEvent",
    "CallbackOpenedEvent",
    "CallbackResolvedEvent",
    "ErrorEvent",
    "HistoryEntryAddedEvent",
    "HistoryEntryCompletedEvent",
    "HistoryEntryPatchedEvent",
    "NoticeEvent",
    "PromptSuggestedEvent",
    "SessionTerminatedEvent",
    "SessionUpdatedEvent",
    "TurnStartedEvent",
    "TurnTerminatedEvent",
    "TurnUpdatedEvent",
    "UnknownEventPayload",
    # Errors of the client
    "ChildSessionProcedureRefusedError",
    "SessionCallbackRejectedError",
    "SessionCallbackSettledError",
    "SessionEventStreamLostError",
    "SessionNotAttachedError",
    "UnsupportedSessionProcedureError",
    # Errors of the turn commands
    "SessionBusyError",
    "SessionIdempotencyConflictError",
    "SessionMessageRejectedError",
    "SessionTerminatedError",
    "SessionTurnConflictError",
]


@dataclass(frozen=True, slots=True)
class ApprovalResult:
    """The answer to an approval: ``answer_callback`` sends it, and a ``provide_callbacks`` handler returns it.

    ``answer`` is ``agents.AllowApproval`` or ``agents.DenyApproval``. An approval takes no other
    answer: a ``CallbackResult`` sent to an approval raises ``agents.SdkError``.

    Raises:
        SdkError: ``answer`` is not ``AllowApproval`` or ``DenyApproval``: ``True``, a dict or ``None``.
    """

    callback_id: str
    answer: AllowApproval | DenyApproval

    def __post_init__(self) -> None:
        if not isinstance(self.answer, AllowApproval | DenyApproval):
            raise SdkError(
                "ApprovalResult takes agents.AllowApproval() or agents.DenyApproval() as its answer, "
                f"not {type(self.answer).__name__}"
            )

    def _callback_result(self) -> CallbackResult:
        return CallbackResult(callback_id=self.callback_id, output=self.answer.model_dump(mode="json"))


class CallbackHandler(Protocol):
    """What ``provide_callbacks`` calls for each open callback: an async function that returns its answer.

    ``agents.KeepCallbackOpen()`` keeps any callback open. An approval takes an ``ApprovalResult``;
    any other return for an approval, ``None`` or a ``CallbackResult`` included, raises
    ``agents.SdkError`` from the block. Any other callback takes a ``CallbackResult``; ``None``
    also keeps it open.
    """

    def __call__(
        self, callback: SessionCallback, /
    ) -> Awaitable[CallbackResult | ApprovalResult | KeepCallbackOpen | None]: ...


def _approval_refusal(callback_id: str) -> SdkError:
    return SdkError(
        f"Callback {callback_id} is an approval: answer it with "
        "session_protocol.ApprovalResult(callback_id, agents.AllowApproval() or agents.DenyApproval()), "
        "not a CallbackResult"
    )


def attach(session: _Session) -> SessionClient:
    """Return the raw protocol client of a session handle. Sends no request.

    The client reaches the session the way the handle does. Use it as ``async with attach(session)
    as client:``, which closes it at the end of the block, also after an exception, or close it
    with ``await client.close()`` when you are done. Closing it stops its event stream and callback
    handlers, and leaves the session running.

    Raises:
        TypeError: ``session`` is not an ``agents.Session``.
    """
    if not isinstance(session, _Session):
        raise TypeError(f"attach() takes an agents.Session, not {type(session).__name__}")
    try:
        transport = session._bind()
    except RuntimeError as error:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            # A local session is bound to the event loop it runs in.
            raise RuntimeError(
                "attach() needs a running event loop for a local session: call it from async code"
            ) from error
        raise
    client = SessionClient(session.id, transport)
    # Resolved on each upload, so that attaching still sends no request and reads nothing.
    client._uploads = session._uploader
    return client


class SessionClient:
    """The raw Session protocol client of one session. Get one with ``attach(session)``.

    ``async with attach(session) as client:`` closes the client at the end of the block, also after
    an exception. The session goes on running.

    Each method sends one Session protocol procedure, except ``upload_file``, which sends none.
    The session's host may refuse one with ``UnsupportedSessionProcedureError``: a
    deployment-backed session refuses ``read_config``, ``write_config`` and ``upload_file``. A
    subagent's session refuses commands and uploads with ``ChildSessionProcedureRefusedError``;
    its parent agent drives it.

    ``events()`` reads the session's event stream as the protocol sends it: from the session's
    start, or after a cursor. ``provide_callbacks`` reads the session once, to find the callbacks
    that are already open.
    """

    __slots__ = ("_attach_lock", "_closed", "_last_event_id", "_raw", "_session_id", "_transport", "_uploads")

    def __init__(self, session_id: str, transport: SessionTransport) -> None:
        self._session_id = session_id
        self._transport = transport
        self._raw = _HarnessSessionClient(transport)
        self._attach_lock = asyncio.Lock()
        self._last_event_id: EventId | None = None
        self._closed = False
        self._uploads: Callable[[], _FileUploader | None] | None = None

    @property
    def session_id(self) -> str:
        """The session's ID."""
        return self._session_id

    @property
    def last_event_id(self) -> EventId:
        """The ID of the last event ``events()`` yielded, or of the state ``read_session()`` read.

        Pass it as ``events(after=...)`` to read on from there.

        Raises:
            SessionNotAttachedError: The client has not read the session or its events yet.
        """
        if self._last_event_id is None:
            raise SessionNotAttachedError("The session client has read no event yet")
        return self._last_event_id

    async def info(self, params: InfoParams | None = None) -> InfoResponse:
        """Ask the host what it supports."""
        return await self._request("app_server/info", params or InfoParams(), InfoResponse)

    async def read_session(
        self,
        *,
        history: PageRequest | None = None,
        turns: PageRequest | None = None,
    ) -> SessionReadResponse:
        """Read the session's state: its status, active turn, open callbacks, history and turns.

        Without ``history`` or ``turns``, ``last_event_id`` moves to the state it read.
        """
        response = await self._request(
            "app_server/session/read",
            _protocol.SessionReadParams(session_id=self._session_id, history=history, turns=turns),
            SessionReadResponse,
        )
        if history is None and turns is None:
            await self._raw.adopt_session_snapshot(response.state, response.last_event_id)
            self._last_event_id = response.last_event_id
        return response

    async def list_history(
        self,
        *,
        turn_id: TurnId | None = None,
        page: PageRequest | None = None,
    ) -> SessionHistoryListResponse:
        """List the session's history entries, or one turn's, one page at a time."""
        return await self._request(
            "app_server/session/history/list",
            _protocol.SessionHistoryListParams(
                session_id=self._session_id, turn_id=turn_id, page=page or PageRequest()
            ),
            SessionHistoryListResponse,
        )

    async def list_turns(self, page: PageRequest | None = None) -> SessionTurnsListResponse:
        """List the session's turns, one page at a time."""
        return await self._request(
            "app_server/session/turns/list",
            _protocol.SessionTurnsListParams(session_id=self._session_id, page=page or PageRequest()),
            SessionTurnsListResponse,
        )

    async def list_subagents(self, *, page: ListPageRequest | None = None) -> SubagentsListResponse:
        """List the direct subagents of this session, newest first, one page at a time."""
        return await self._request(
            "app_server/subagents/list",
            _protocol.SubagentsListParams(parent_session_id=self._session_id, page=page or ListPageRequest()),
            SubagentsListResponse,
        )

    async def list_catalog(
        self,
        *,
        scope: SessionCatalogScope | None = None,
        include_archived: bool = False,
        page: ListPageRequest | None = None,
    ) -> CatalogListResponse:
        """List the host's sessions: root sessions by default, without archived ones."""
        return await self._request(
            "app_server/catalog/list",
            _protocol.CatalogListParams(
                scope=scope or RootsScope(), include_archived=include_archived, page=page or ListPageRequest()
            ),
            CatalogListResponse,
        )

    async def rename_session(self, title: str | None) -> CatalogRenameResponse:
        """Set the session's title, or clear it with ``None``."""
        return await self._request(
            "app_server/catalog/rename",
            _protocol.CatalogRenameParams(session_id=self._session_id, title=title),
            CatalogRenameResponse,
        )

    async def archive_session(self, archived: bool = True) -> CatalogArchiveResponse:
        """Archive the session, so that ``list_catalog`` leaves it out, or unarchive it with ``False``."""
        return await self._request(
            "app_server/catalog/archive",
            _protocol.CatalogArchiveParams(session_id=self._session_id, archived=archived),
            CatalogArchiveResponse,
        )

    @_errors.public_errors
    async def upload_file(
        self,
        source: str | Path | bytes | AsyncIterator[bytes],
        *,
        name: str | None = None,
        media_type: str | None = None,
    ) -> EmbeddedResourceContentBlock | ResourceLinkContentBlock:
        """Make a file on this machine available as a content block for the session's messages.

        Pass the block in the message of ``start_turn``, ``send_message`` or ``steer_turn``. The
        upload sends no message. ``source`` is a path, bytes or an async iterator of bytes; bytes
        and iterators need ``name=``. A local session without a sandbox embeds a snapshot of the
        file in the block. A local session whose sandbox has an input folder stores the file and
        returns a link to it, which a message copies into the sandbox; a link no message sends
        expires after an hour.

        Raises:
            UnsupportedSessionProcedureError: The host takes no uploads: a deployment-backed
                session, or a local sandbox without an input folder. Raised before reading
                ``source``.
            ChildSessionProcedureRefusedError: The session is a subagent's.
            SessionTerminatedError: The client or the session is closed.
        """
        self._refuse_if_closed()
        uploader = self._uploads() if self._uploads is not None else None
        if uploader is None:
            raise _errors.UnsupportedSessionProcedureError(
                method="upload_file",
                backend=type(self._transport).__name__,
                reason="File uploads are not available in the current configuration.",
            )
        return await uploader(self._session_id, source, name=name, media_type=media_type)

    async def send_message(
        self,
        message: list[ContentBlock],
        *,
        message_entry_id: HistoryEntryId | None = None,
        idempotency_key: str | None = None,
    ) -> MessageSendResponse:
        """Start a turn when none is active, else steer the active turn.

        The receipt is returned once the message is durably accepted. Its ``steered`` is ``True``
        when the message joined the running turn and ``False`` when it started one; an Agent or
        Agent Controller deployed before the field existed leaves it ``None``. The idempotency key
        defaults to ``message_entry_id``.
        """
        return await self._request(
            "app_server/session/message/send",
            _protocol.MessageSendParams(
                idempotency_key=idempotency_key or message_entry_id,
                session_id=self._session_id,
                message_entry_id=message_entry_id,
                message=message,
            ),
            MessageSendResponse,
        )

    async def start_turn(
        self,
        message: list[ContentBlock],
        *,
        message_entry_id: HistoryEntryId | None = None,
        idempotency_key: str | None = None,
    ) -> TurnStartResponse:
        """Start a turn. The idempotency key defaults to ``message_entry_id``."""
        return await self._request(
            "app_server/session/turn/start",
            _protocol.TurnStartParams(
                idempotency_key=idempotency_key or message_entry_id,
                session_id=self._session_id,
                message_entry_id=message_entry_id,
                message=message,
            ),
            TurnStartResponse,
        )

    async def steer_turn(
        self,
        expected_turn_id: TurnId,
        message: list[ContentBlock],
        *,
        message_entry_id: HistoryEntryId | None = None,
        idempotency_key: str | None = None,
    ) -> TurnSteerResponse:
        """Add a message to the running turn ``expected_turn_id``."""
        return await self._request(
            "app_server/session/turn/steer",
            _protocol.TurnSteerParams(
                idempotency_key=idempotency_key or message_entry_id,
                session_id=self._session_id,
                expected_turn_id=expected_turn_id,
                message_entry_id=message_entry_id,
                message=message,
            ),
            TurnSteerResponse,
        )

    async def interrupt_turn(
        self, expected_turn_id: TurnId, *, reason: str = _DEFAULT_INTERRUPT_REASON
    ) -> TurnInterruptResponse:
        """End the running turn ``expected_turn_id``, and leave the session usable."""
        return await self._request(
            "app_server/session/turn/interrupt",
            _protocol.TurnInterruptParams(
                session_id=self._session_id, expected_turn_id=expected_turn_id, reason=reason
            ),
            TurnInterruptResponse,
        )

    async def cancel_session(
        self,
        *,
        reason: str = "cancel requested",
        idempotency_key: str | None = None,
    ) -> SessionCancelResponse:
        """End the session and its subagents for good. A later command raises ``SessionTerminatedError``."""
        return await self._request(
            "app_server/session/cancel",
            _protocol.SessionCancelParams(idempotency_key=idempotency_key, session_id=self._session_id, reason=reason),
            SessionCancelResponse,
        )

    async def read_config(self) -> ConfigReadResponse:
        """Read a local session's configuration. A deployment-backed session refuses it."""
        return await self._request(
            "app_server/session/config/read",
            _protocol.ConfigReadParams(session_id=self._session_id),
            ConfigReadResponse,
        )

    async def write_config(self, config: AgentConfig) -> ConfigWriteResponse:
        """Replace a local session's configuration. A deployment-backed session refuses it.

        Only ``tools``, ``hooks``, ``mcps``, ``connectors`` and ``subagents`` can change, and only in
        a way that keeps the session's subagent policy. Any other change, such as the model or the
        instructions, raises an ``agents.AgentsError``.
        """
        return await self._request(
            "app_server/session/config/write",
            _protocol.ConfigWriteParams(session_id=self._session_id, config=config),
            ConfigWriteResponse,
        )

    async def answer_callback(
        self, result: CallbackResult | ApprovalResult, *, session_id: str | None = None
    ) -> CallbackResultResponse:
        """Answer one open callback, named by ``result.callback_id``, and return the protocol's receipt.

        An approval takes an ``ApprovalResult``, with ``agents.AllowApproval()`` or
        ``agents.DenyApproval()``; any other callback takes a ``CallbackResult``. Before it sends an
        answer, the client reads the open callbacks of its session and its subagents once: a
        ``CallbackResult`` for an approval the session has open, or an ``ApprovalResult`` for an
        open callback that is not an approval, raises ``agents.SdkError``, and nothing is sent.
        When that read fails, the answer is sent unchecked.

        ``session_id`` names the session that opened the callback, so a root client answers a
        callback of one of its subagents: pass the ``session_id`` of the callback that
        ``provide_callbacks`` handed to its handler. ``None`` means this client's session.

        Both hosts accept a second answer to a callback an answer already settled, and apply only
        the first. The receipt does not say whose answer the session applied: read the
        ``CallbackResolvedEvent`` of the callback from ``events()``. Its ``outcome`` says how the
        callback ended. For an approval, ``outcome.output`` holds the applied decision, such as
        ``{"decision": "allow", "scope": "once"}`` or ``{"decision": "deny"}``: compare it with
        your answer's ``model_dump(mode="json")``. A client tool's ``outcome.output`` is empty.

        Raises:
            SessionCallbackSettledError: The session has ended, or never opened the callback:
                answering a subagent's callback without its ``session_id`` raises it. Both hosts
                also raise it for a callback that timed out or was cancelled, which a deployed
                session on an older control plane or agent accepts with no effect.
            SessionCallbackRejectedError: The session refuses the answer: it does not fit the
                callback, such as an error answer to an approval, or an approval answer that
                neither allows nor denies. Nothing was applied and the callback stays open. It is
                also an ``agents.SdkError``, and its message says why the session refused it.
            SdkError: ``result`` is neither a ``CallbackResult`` nor an ``ApprovalResult``, it is
                a ``CallbackResult`` for an approval the session has open, or an ``ApprovalResult``
                for an open callback that is not an approval; nothing is sent.
            OutcomeUnknownError: A deployed session did not show the answer applied within 30
                seconds.
        """
        session_id = session_id or self._session_id
        if not isinstance(result, CallbackResult | ApprovalResult):
            raise SdkError(
                "answer_callback takes a CallbackResult, or an ApprovalResult for an approval, "
                f"not {type(result).__name__}"
            )
        kind = await self._open_callback_kind(session_id, result.callback_id)
        if isinstance(result, ApprovalResult):
            if kind is not None and kind != "approval":
                raise SdkError(
                    f"Callback {result.callback_id} is a {kind} callback, not an approval: answer it "
                    "with a CallbackResult, not an ApprovalResult"
                )
            result = result._callback_result()
        elif kind == "approval":
            raise _approval_refusal(result.callback_id)
        try:
            return await self._request(
                "app_server/session/callback/result",
                _protocol.CallbackResultParams(session_id=session_id, result=result),
                CallbackResultResponse,
            )
        except _LocalSessionProcedureError as error:
            # The local host reports a callback it never opened as a bare procedure error; the
            # deployed host reports it as settled. Raise the same error on both hosts.
            if isinstance(error, SessionCallbackSettledError) or not str(error).startswith(_LOCAL_UNKNOWN_CALLBACK):
                raise
            raise _LocalSessionCallbackSettledError(str(error)) from error

    @asynccontextmanager
    async def provide_callbacks(
        self,
        *,
        kinds: Collection[CallbackKind],
        handler: CallbackHandler,
    ) -> AsyncIterator[None]:
        """Answer the callbacks of ``kinds`` of this session and its subagents while the block is open.

        On a root session, one block also gets the callbacks its subagents open: the callback's
        ``session_id`` names the session that opened it, and the answer goes to that session. The
        handler gets each open callback once, and returns its answer: for an approval, an
        ``ApprovalResult``; for any other callback, a ``CallbackResult``. It returns
        ``agents.KeepCallbackOpen()`` to keep any callback open (``None`` also keeps a callback
        that is not an approval open). Answer it later with
        ``answer_callback(result, session_id=callback.session_id)``. Leaving the block stops
        answering, and leaves open callbacks open. An error the handler raises leaves the block, and
        so does ``agents.SdkError`` for a return that does not answer the callback's kind (for an
        approval: ``None`` or a ``CallbackResult``); the callback stays open. The first block reads
        the session once, to find the callbacks already open; that read does not move
        ``last_event_id``.
        """
        self._refuse_if_closed()
        raw = await self._attached()

        async def answer(callback: SessionCallback) -> CallbackResult | None:
            result = await handler(callback)
            if isinstance(result, KeepCallbackOpen):
                return None
            if isinstance(callback, ApprovalCallback):
                if isinstance(result, ApprovalResult):
                    return result._callback_result()
                if isinstance(result, CallbackResult):
                    raise _approval_refusal(callback.id)
                raise SdkError(
                    f"Callback {callback.id} is an approval: a provide_callbacks handler returns "
                    "session_protocol.ApprovalResult, or agents.KeepCallbackOpen() to keep it open, "
                    f"not {_described(result)}"
                )
            if result is None or isinstance(result, CallbackResult):
                return result
            raise SdkError(
                f"Callback {callback.id} is a {callback.kind} callback: a provide_callbacks handler returns "
                f"a CallbackResult, or agents.KeepCallbackOpen() to keep it open, not {_described(result)}"
            )

        async with raw.provide_callbacks(kinds=kinds, handler=answer):
            yield

    async def events(self, *, after: EventId | None = None, batch_size: int = 100) -> AsyncGenerator[ClientEvent, None]:
        """Yield the session's events, as the protocol sends them, until the session's stream ends.

        Without ``after``, the events start at the session's start. With ``after``, they start
        after that event. A turn's events start after its ``started_after_event_id``, which
        ``start_turn`` returns when the host gives it; ``last_event_id`` reads on from the last
        event read. Each call opens its own stream.

        Raises:
            SessionEventStreamLostError: The stream was lost; read again with ``after`` set to its
                ``after_event_id``.
        """
        self._refuse_if_closed()
        params = EventsReadParams(session_id=self._session_id, after_event_id=after, batch_size=batch_size)
        try:
            # Both transports return an async generator: close it when the reader stops.
            async with aclosing(self._transport.read_events(params)) as stream:  # type: ignore[type-var]
                async for item in stream:
                    match item:
                        case EventBatch(events=batch):
                            events = batch
                        case Event():
                            events = [item]
                        case _:
                            continue
                    for event in events:
                        client_event = _client_event(event)
                        self._last_event_id = client_event.event_id
                        yield client_event
        except Exception:
            # close() ends the streams it finds open; their transport may fail as it closes.
            if self._closed:
                return
            raise

    async def close(self) -> None:
        """End the client's event streams and callback handlers. The session goes on running."""
        self._closed = True
        await self._raw.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the client. A close that fails while the block raises becomes a note on that error."""
        try:
            await self.close()
        except BaseException as close_error:
            if exc_value is None:
                raise
            exc_value.add_note(f"Closing the session client failed: {close_error!r}")

    async def _request[ResultT: _SessionModel](
        self, method: str, params: _SessionModel, result_type: type[ResultT]
    ) -> ResultT:
        self._refuse_if_closed()
        return await self._raw.request(method, params, result_type)

    async def _open_callback_kind(self, session_id: str, callback_id: str) -> str | None:
        """The kind of ``callback_id`` if ``session_id`` has it open; ``None`` when it does not, or the read fails.

        It reads the open callbacks of this client's session and its subagents, as ``turn.answer``
        does, so a subagent's callback has its kind too: a read of the subagent's session would not
        show it on a deployed session.
        """
        try:
            tree = await self._request(
                "app_server/session/callbacks/tree",
                _protocol.CallbacksTreeParams(session_id=self._session_id),
                _protocol.CallbacksTreeResponse,
            )
        except SessionTerminatedError:
            raise
        except Exception:  # noqa: BLE001 - the answer goes unchecked; the host still refuses one it cannot read
            return None
        return next(
            (
                item.callback.kind
                for item in tree.callbacks
                if item.session_id == session_id and item.callback.id == callback_id
            ),
            None,
        )

    def _refuse_if_closed(self) -> None:
        # A closed local transport refuses with this error; a closed remote one raises a bare
        # RuntimeError. Refuse the same way on both hosts.
        if self._closed:
            raise SessionTerminatedError("The session client is closed")

    async def _attached(self) -> _HarnessSessionClient:
        # The harness client's callback handlers need the session's state, for the callbacks
        # already open. Read it on first need, once, without moving `last_event_id`.
        async with self._attach_lock:
            try:
                self._raw.state
            except SessionNotAttachedError:
                response = await self._request(
                    "app_server/session/read",
                    _protocol.SessionReadParams(session_id=self._session_id),
                    SessionReadResponse,
                )
                await self._raw.adopt_session_snapshot(response.state, response.last_event_id)
        return self._raw

    def __repr__(self) -> str:
        return f"SessionClient(session_id={self._session_id!r})"


# The message `local_execution._answer_callback` gives a callback the local session never opened.
_LOCAL_UNKNOWN_CALLBACK = "Unknown local Session callback "


def _client_event(event: Event) -> ClientEvent:
    if isinstance(event, ClientEvent):
        return event
    return ClientEvent.model_validate(event.model_dump(mode="json", by_alias=True))
