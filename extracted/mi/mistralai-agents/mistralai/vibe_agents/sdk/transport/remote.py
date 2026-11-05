"""Vibe Agents transport for deployment-backed Harness Session clients."""

import asyncio
import base64
import warnings
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping, Sequence, Set
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, cast
from uuid import UUID, uuid4

import httpx
import structlog
from pydantic import JsonValue

from mistralai.client import SERVER_GLOBAL, SERVERS
from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents._http import _header_api_key
from mistralai.vibe_agents._internal.caller_headers import internal_caller_headers
from mistralai.vibe_agents.agents_client import AgentsClient
from mistralai.vibe_agents.sdk.app.config import ControlPlaneSettings, SessionClientSettings, mistral_api_url
from mistralai.vibe_agents.sdk.authoring import errors as sdk_errors
from mistralai.vibe_agents.sdk.authoring.errors import (
    AgentsError,
    LegacySessionError,
    OutcomeUnknownError,
    RemoteAgentDeploymentNotFoundError,
    RemoteStreamLostError,
    SessionStartupTimeoutError,
    public_errors,
    public_iter_errors,
    sdk_runtime_error,
)
from mistralai.vibe_agents.session_workflow.command_ids import message_command_id, sdk_command_id
from mistralai.vibe_agents.sessions_client import (
    AgentSessionResponse,
    AgentSessionStatus,
    SessionCommandRejectedError,
    SessionProtocol,
    SessionsClient,
    StartAgentSessionResponse,
)
from mistralai.vibe_agents.sessions_client import api_models as session_api
from mistralai.vibe_agents.sessions_client import api_models_v1 as procedure_api
from mistralai.vibe_agents.sessions_client.client import ProcedureRoute

from .client_tools import NO_CLIENT_TOOLS, ClientToolRegistry, ClientToolSessionClient
from .event_ids import (
    _CURSOR_PREFIX,
    _EMPTY_CURSOR,
    _EMPTY_POSITION,
    _empty_cursor,
    _encode_base64url,
    _encode_event_id,
    _split_session,
)
from .procedures import SESSION_PROCEDURES, refuse_unlisted_procedure
from .product_session import build_session_from_product
from .projection_v1 import RelayedPayload, VibeAgentsSessionV1Projection

logger = structlog.get_logger(__name__)

# The x-internal-service identity this transport calls vibe-api with. It reads the same today as
# the application name it starts Sessions under, but the two are different contracts and each is
# free to move: keep them as separate literals.
_ORIGIN_SERVICE = "mistral-agents-sdk-unified-harness"
# Marks the event id of a Turn termination taken from the product row rather than a frame.
# `~` is outside the base64url alphabet the cursor is encoded in, so it cannot occur in one.
_RECONCILED_TURN_MARKER = "~turn"
_PAGE_CURSOR_PREFIX = "vibe-agents-page:"
# Also bounds send_message retries of an unknown outcome or a busy Session.
_OUTCOME_TIMEOUT_SECONDS = 30.0
# A 503 is the control plane's unknown outcome; a 504 is a gateway that gave up after forwarding. A
# 500 is a crash that may follow the commit, and its body cannot say where it happened.
_SEND_MESSAGE_UNKNOWN_OUTCOME_STATUSES = frozenset(
    {httpx.codes.INTERNAL_SERVER_ERROR, httpx.codes.SERVICE_UNAVAILABLE, httpx.codes.GATEWAY_TIMEOUT}
)
_RETRY_INITIAL_SECONDS = 0.05
_RETRY_MAX_SECONDS = 0.5
# How long the event reader keeps reconnecting a dropped event stream before it gives up and
# raises RemoteStreamLostError. The Session keeps running either way.
_STREAM_RECONNECT_BUDGET_SECONDS = 60.0
_STREAM_RECONNECT_INITIAL_SECONDS = 0.5
_STREAM_RECONNECT_MAX_SECONDS = 5.0
# A reopened stream with no event counts as reconnected only if it sent something (the server
# sends a heartbeat every 15 seconds) and stayed open this long. A server that accepts each stream
# and drops it at once, or accepts it and then sends nothing, still runs out the budget.
_STREAM_STABLE_OPEN_SECONDS = 10.0
# The `detail.code` of a 429 that applied nothing and clears on its own, so the same command is
# retried. A full Session Tree answers a 429 with another code, and waiting inside one call does
# not clear it. A 429 with no code comes from a gateway in front, which applied nothing either.
_RETRYABLE_BUSY_CODES = frozenset({"session_busy", "intake_overloaded", "session_continuing"})
# A Session start takes seconds, unlike a command acknowledgement, so it has its own slower
# schedule. The first readiness check is immediate. The next one comes _START_POLL_MIN_SECONDS
# later, and the wait doubles up to _START_POLL_MAX_SECONDS. A ready Session is noticed at most
# _START_POLL_MAX_SECONDS late. A slow start costs one history read and one status read per
# _START_POLL_MAX_SECONDS.
_START_POLL_MIN_SECONDS = 0.25
_START_POLL_MAX_SECONDS = 1.0
# The `detail.code` of the control plane's 403 for a client command on a subagent's Session.
_COMMAND_PROCEDURES = frozenset(
    {
        "app_server/session/message/send",
        "app_server/session/turn/start",
        "app_server/session/turn/steer",
        "app_server/session/turn/interrupt",
        "app_server/session/cancel",
        "app_server/session/callback/result",
    }
)
# A remote Session starts through its Agent Deployment, so `session/start` is the one SDK
# procedure this transport does not serve.
_REMOTE_PROCEDURES = tuple(method for method in SESSION_PROCEDURES if method != "app_server/session/start")
_TERMINAL_PRODUCT_STATUSES = frozenset(
    {AgentSessionStatus.COMPLETED, AgentSessionStatus.FAILED, AgentSessionStatus.TERMINATED}
)


class RemoteSessionConflictError(AgentsError, RuntimeError):
    """Raised when a compare-and-set Turn command targets stale state."""


def _invalid_event_cursor(
    event_id: str, session_id: UUID, *, owner: str | None = None
) -> sdk_errors.InvalidCursorError:
    """``InvalidCursorError``, as on a local session, still the ``RemoteSessionConflictError`` it was before."""
    return sdk_errors.invalid_cursor(event_id, session_id, owner=owner, host_class=RemoteSessionConflictError)


class _UndecodableEventCursorError(Exception):
    """The control plane answered 400 to the history read that sends the caller's cursor."""


class RemoteSessionTurnConflictError(RemoteSessionConflictError, harness_session.SessionTurnConflictError):
    """Raised when a steer or interrupt names a Turn that is not the active Turn.

    In-process sessions raise another ``SessionTurnConflictError`` for the same case.
    """


class _RemoteSessionTurnActiveError(sdk_errors.SessionBusyError, harness_session.SessionTurnActiveError):
    """Raised when the Session refused a Turn start because another Turn is running.

    Nothing was applied. ``active_turn_id`` is the running Turn. The same idempotency key starts a
    Turn once that Turn ends. In-process sessions raise ``LocalSessionBusyError`` for the same case.
    """


class RemoteSessionStartFailedError(AgentsError, RuntimeError):
    """Raised when a Session ends before it reports itself ready, with the failure Vibe Agents retained."""


@dataclass(frozen=True, slots=True)
class RemoteAgentDeployment:
    """Private routing and authentication for one Agent Deployment handle."""

    server_url: str
    api_key: str | None = None
    principal: wire.Principal | None = None
    agent_deployment_id: UUID | None = None
    agent_deployment_name: str | None = None
    # The connection pool of the agents.Client this handle came from, or None for a connection per request.
    pool: Callable[[], httpx.AsyncClient | None] | None = field(default=None, compare=False, repr=False)
    # FIXME: delete once MAIS 2026.11 is released
    # Procedure routes a Session answered 501 or a bare 404 to, keyed by the target Session since a
    # callback answer can target another Session of the tree. Held here rather than on a transport
    # because a handle binds a new transport for each call.
    unserved_routes: set[tuple[UUID, ProcedureRoute]] = field(
        default_factory=set, init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        # No identity is a handle that only reattaches: session requests are keyed by the session id.
        if self.agent_deployment_id is not None and self.agent_deployment_name is not None:
            raise ValueError("Remote Agent Deployment takes an id or a name, not both")
        if not self.server_url.strip():
            raise ValueError("Remote Agent Deployment server_url must not be blank")
        if (self.api_key is None) == (self.principal is None):
            raise ValueError("Remote Agent Deployment requires exactly one of api_key or principal")
        if self.api_key is not None and not self.api_key.strip():
            raise ValueError("Remote Agent Deployment api_key must not be blank")
        if self.agent_deployment_name is not None and not self.agent_deployment_name.strip():
            raise ValueError("Remote Agent Deployment name must not be blank")


def _sessions_client(
    deployment: RemoteAgentDeployment,
    http_transport: httpx.AsyncBaseTransport | None,
    http_client: httpx.AsyncClient | None = None,
    pool: Callable[[], httpx.AsyncClient | None] | None = None,
) -> SessionsClient:
    if deployment.principal is None:
        return SessionsClient(
            base_url=deployment.server_url,
            api_key=deployment.api_key,
            transport=http_transport,
            http_client=http_client,
            pool=pool,
        )
    return SessionsClient(
        base_url=deployment.server_url,
        extra_headers=internal_caller_headers(deployment.principal, origin_service=_ORIGIN_SERVICE),
        transport=http_transport,
        http_client=http_client,
        pool=pool,
    )


class VibeAgentsSessionTransport(harness_session.SessionTransport):
    """Adapt the existing Vibe Agents control plane to Harness SessionTransport."""

    def __init__(
        self,
        deployment: RemoteAgentDeployment,
        *,
        session_id: UUID | None = None,
        http_transport: httpx.AsyncBaseTransport | None = None,
        http_client: httpx.AsyncClient | None = None,
        sessions_client: SessionsClient | None = None,
        agents_client: AgentsClient | None = None,
    ) -> None:
        self._deployment = deployment
        self._session_id = session_id
        # A client's pool, asked again before each request: a closed client refuses, and a later event
        # loop gets its own pool. A pool comes with its own transport, so ``http_transport`` then goes unused.
        pool = deployment.pool
        if http_client is None and pool is not None:
            http_client = pool()
        self._sessions = sessions_client or _sessions_client(deployment, http_transport, http_client, pool)
        self._agents: AgentsClient | None
        if agents_client is not None:
            self._agents = agents_client
        elif deployment.agent_deployment_id is not None and deployment.api_key is not None:
            self._agents = AgentsClient(
                base_url=deployment.server_url,
                api_key=deployment.api_key,
                transport=http_transport,
                http_client=http_client,
                pool=pool,
            )
        else:
            self._agents = None
        self._owns_sessions_client = sessions_client is None
        self._owns_agents_client = agents_client is None and self._agents is not None
        self._resolved_deployment_name = deployment.agent_deployment_name
        # Set once the bound Session's row said it uses Session v1: a Session's protocol is fixed at creation.
        self._session_v1_checked = False
        self._read_projection: VibeAgentsSessionV1Projection | None = None
        self._read_projection_lock = asyncio.Lock()
        # Set once the control plane answered that it has no callbacks route: a wait reads the
        # Session's active Turn on every change, and each read would ask again.
        self._no_callbacks_tree = False
        # Turns of messages `send_message` was refused because the Session was stopping. The
        # Session may have published the message, naming the Turn, before refusing it.
        self._refused_turn_ids: set[str] = set()
        self._closed = False

    @public_errors
    async def request[ResultT: harness_session.SessionModel](
        self,
        method: str,
        params: harness_session.SessionModel,
        result_type: type[ResultT],
    ) -> ResultT:
        del result_type
        if self._closed:
            raise sdk_runtime_error("Remote Session transport is closed")
        refuse_unlisted_procedure(method, backend="vibe_agents")
        try:
            return cast(ResultT, await self._dispatch(method, params))
        except httpx.HTTPStatusError as error:
            if (refusal := _command_refusal(error, method=method)) is not None:
                raise refusal from error
            if error.response.status_code == httpx.codes.NOT_FOUND and method in _COMMAND_PROCEDURES:
                await self._raise_if_bound_session_missing()
            raise
        except harness_session.SessionCallbackSettledError as error:
            # A 404 to an answer can mean the callback closed or the Session is unknown.
            cause = error.__cause__
            if isinstance(cause, httpx.HTTPStatusError) and cause.response.status_code == httpx.codes.NOT_FOUND:
                await self._raise_if_bound_session_missing()
            raise

    async def _raise_if_bound_session_missing(self) -> None:
        """Raise ``SessionNotFoundError`` if the control plane does not know the bound Session.

        A command's 404 can name the Session or something in it, such as a callback that is no
        longer pending; the Session's row tells which. A read that fails otherwise tells nothing,
        so the caller keeps the command's own error.
        """
        if self._session_id is None:
            return
        try:
            await self._read_bound_session(self._session_id)
        except httpx.HTTPError:
            return

    async def _dispatch(self, method: str, params: harness_session.SessionModel) -> harness_session.SessionModel:
        if method == "app_server/info":
            return _build_info_response()
        if method == "app_server/subagents/list" and isinstance(params, harness_session.SubagentsListParams):
            return await self._list_subagents(params)
        if method == "app_server/catalog/list" and isinstance(params, harness_session.CatalogListParams):
            return await self._list_catalog(params)
        if method == "app_server/catalog/rename" and isinstance(params, harness_session.CatalogRenameParams):
            product = await self._sessions.rename_session(
                agent_session_id=self._require_session_id(params.session_id), title=params.title
            )
            return harness_session.CatalogRenameResponse(session=build_session_from_product(product))
        if method == "app_server/catalog/archive" and isinstance(params, harness_session.CatalogArchiveParams):
            product = await self._sessions.archive_session(
                agent_session_id=self._require_session_id(params.session_id), archived=params.archived
            )
            return harness_session.CatalogArchiveResponse(session=build_session_from_product(product))
        if method == "app_server/session/read" and isinstance(params, harness_session.SessionReadParams):
            return await self._read_session(params)
        if method == "app_server/session/history/list" and isinstance(
            params,
            harness_session.SessionHistoryListParams,
        ):
            return await self._list_history(params)
        if method == "app_server/session/turns/list" and isinstance(
            params,
            harness_session.SessionTurnsListParams,
        ):
            return await self._list_turns(params)
        if method == "app_server/session/message/send" and isinstance(params, harness_session.MessageSendParams):
            return await self._send_message(params)
        if method == "app_server/session/turn/start" and isinstance(params, harness_session.TurnStartParams):
            return await self._start_turn(params)
        if method == "app_server/session/turn/steer" and isinstance(params, harness_session.TurnSteerParams):
            return await self._steer_turn(params)
        if method == "app_server/session/turn/interrupt" and isinstance(
            params,
            harness_session.TurnInterruptParams,
        ):
            return await self._interrupt_turn(params)
        if method == "app_server/session/cancel" and isinstance(params, harness_session.SessionCancelParams):
            return await self._cancel_session(params)
        if method == "app_server/session/callback/result" and isinstance(
            params,
            harness_session.CallbackResultParams,
        ):
            return await self._answer_callback(params)
        if method == "app_server/session/callbacks/tree" and isinstance(params, harness_session.CallbacksTreeParams):
            session_id = self._require_session_id(params.session_id)
            # Before the route checks, so a legacy Session raises LegacySessionError on every host.
            await self._require_session_v1()
            if self._no_callbacks_tree:
                raise _tree_unsupported()
            try:
                return await self._sessions.read_session_callbacks(agent_session_id=session_id)
            except httpx.HTTPStatusError as error:
                if _route_missing(error):
                    self._no_callbacks_tree = True
                    raise _tree_unsupported() from error
                raise
        raise RemoteSessionProcedureUnsupportedError(
            method=method,
            backend="vibe_agents",
            reason=_remote_unsupported_reason(method),
        )

    async def _list_subagents(
        self, params: harness_session.SubagentsListParams
    ) -> harness_session.SubagentsListResponse:
        parent_id = self._require_session_id(params.parent_session_id)
        children = await self._sessions.list_sessions(
            scope=session_api.DirectChildrenScopeInput(parent_session_id=parent_id),
            include_archived=True,
            limit=params.page.limit,
            cursor=params.page.cursor,
        )
        return harness_session.SubagentsListResponse(
            items=[_subagent_session(child) for child in children.items],
            next_cursor=children.next_cursor,
        )

    async def _list_catalog(self, params: harness_session.CatalogListParams) -> harness_session.CatalogListResponse:
        scope: session_api.SessionCatalogScopeInput
        match params.scope:
            case harness_session.DirectChildrenScope(parent_session_id=parent_id):
                scope = session_api.DirectChildrenScopeInput(parent_session_id=UUID(parent_id))
            case harness_session.TreeScope(root_session_id=root_id):
                scope = session_api.TreeScopeInput(root_session_id=UUID(root_id))
            case harness_session.RootsScope():
                scope = session_api.RootsScopeInput()
        response = await self._sessions.list_sessions(
            scope=scope,
            include_archived=params.include_archived,
            limit=params.page.limit,
            cursor=params.page.cursor,
        )
        return harness_session.CatalogListResponse(
            items=[build_session_from_product(product) for product in response.items],
            next_cursor=response.next_cursor,
        )

    async def start_deployment_session(
        self,
        *,
        history: list[harness_session.HistoryImportEntry],
        timeout_seconds: float,
        idempotency_key: str | None = None,
        agent: wire.SessionAgentCustomization | None = None,
        session_inputs: Mapping[str, JsonValue] | None = None,
        until_started: bool = False,
        initial_turn: harness_session.InitialTurn | None = None,
    ) -> harness_session.SessionStartResponse:
        """Create the deployment-bound product Session and wait until it is ready.

        Without ``initial_turn``, ready is the retained idle state. With it, ready is the retained
        initial Turn, which the response names. The response names no initial Turn when the control
        plane or the Agent predates ``initial_turn``: the Session then starts idle.

        With ``until_started``, wait only while the Session is still starting. A repeated start
        with an idempotency key returns a Session that may be running a turn or have ended, and
        it may never be idle again.
        """

        if self._closed:
            raise sdk_runtime_error("Remote Session transport is closed")
        if self._session_id is not None:
            raise RemoteSessionConflictError("This transport is already attached to a Session")
        if history:
            raise RemoteSessionProcedureUnsupportedError(
                method="Agent.create_session(history=...)",
                backend="vibe_agents",
                reason="the current Vibe Agents start contract cannot import canonical history",
            )
        deployment_name = await self._resolve_deployment_name()
        # One throttle budget for every create call below.
        throttle_deadline = asyncio.get_running_loop().time() + _OUTCOME_TIMEOUT_SECONDS

        async def create(initial_turn: harness_session.InitialTurn | None) -> StartAgentSessionResponse:
            return await _retry_throttled_start(
                lambda: self._sessions.create_session(
                    agent_name=deployment_name,
                    agent=agent,
                    idempotency_key=idempotency_key,
                    session_inputs=dict(session_inputs) if session_inputs else None,
                    initial_turn=initial_turn,
                ),
                deadline=throttle_deadline,
            )

        try:
            started = await _create_with_initial_turn(create, initial_turn)
        except httpx.HTTPStatusError as error:
            if idempotency_key is not None and _is_idempotency_conflict(error):
                raise harness_session.SessionIdempotencyConflictError(idempotency_key=idempotency_key) from error
            # A 400 is a start request the control plane refused as invalid, such as a
            # missing session input: the same mistake an in-process start raises as SdkError.
            if error.response.status_code != httpx.codes.BAD_REQUEST:
                raise
            raise sdk_errors.SdkError(_detail_message(error, "The control plane refused the Session start")) from error
        self._session_id = started.agent_session.agent_session_id
        # A repeated start returns the Session its key first started, which a raw client may have started in
        # the legacy task protocol.
        _require_session_v1(started.agent_session)
        self._session_v1_checked = True
        if until_started and started.agent_session.status in _TERMINAL_PRODUCT_STATUSES:
            # Only a repeated start returns a Session that has already ended.
            projection = await self._build_projection(started.agent_session)
            ended_turn = projection.turns.get(started.initial_turn.id) if started.initial_turn else None
            # A retry of a start whose message was refused raises, as that start did.
            _raise_if_message_refused(ended_turn)
            return harness_session.SessionStartResponse(
                state=projection.state(),
                last_event_id=_last_event_id(projection),
                initial_turn=ended_turn,
            )
        turn_id: str | None = None
        description = "empty Session initialization"
        if started.initial_turn is not None:
            turn_id = started.initial_turn.id
            description = f"initial Turn {turn_id}"

        def ready(projection: VibeAgentsSessionV1Projection) -> bool:
            if turn_id is not None and turn_id in projection.turns:
                return True
            if until_started:
                return _left_starting(projection)
            # FIXME: once the control plane's minimum Agents SDK version runs initial_turn, wait only for the
            # Turn when the start names one. An Agent built with an older SDK drops the Turn and reports idle.
            return _started_idle(projection)

        readiness_timeout = asyncio.timeout(timeout_seconds)
        try:
            async with readiness_timeout:
                projection = await self._wait_for_projection(
                    ready,
                    description=description,
                    timeout_seconds=timeout_seconds,
                    product_session=started.agent_session,
                    session_start=True,
                )
        except TimeoutError as error:
            if not readiness_timeout.expired():
                raise
            raise SessionStartupTimeoutError(str(self._session_id), timeout_seconds) from error
        except OutcomeUnknownError as error:
            raise SessionStartupTimeoutError(str(self._session_id), timeout_seconds) from error
        turn: harness_session.TurnState | None = None
        if turn_id is not None:
            turn = projection.turns.get(turn_id)
        _raise_if_message_refused(turn)
        return harness_session.SessionStartResponse(
            state=projection.state(),
            last_event_id=_last_event_id(projection),
            initial_turn=turn,
        )

    @public_iter_errors
    async def read_events(
        self,
        params: harness_session.EventsReadParams,
        *,
        reconnect_budget_seconds: float | None = None,
        on_open: Callable[[], None] | None = None,
    ) -> AsyncIterator[harness_session.ClientTransportStreamItem]:
        """Read the Session's events after ``params.after_event_id``, then follow new ones.

        A dropped stream is reconnected for up to ``reconnect_budget_seconds``, by default
        ``_STREAM_RECONNECT_BUDGET_SECONDS``; with ``0``, its first failure raises
        ``RemoteStreamLostError``. ``on_open`` is called each time the server accepts the
        live stream, before its first frame.
        """
        session_id = self._require_session_id(params.session_id)
        after_event_id, reconciled_through = _split_reconciled_event_id(params.after_event_id, session_id)
        cursor, subevent_index = _decode_event_id(after_event_id, session_id, passed=params.after_event_id)
        product = await self._read_bound_session(session_id)
        try:
            projection, resume_payloads = await self._build_stream_projection(
                product,
                cursor=cursor,
                capture_cursor=cursor if subevent_index is not None else None,
            )
        except _UndecodableEventCursorError as error:
            raise _invalid_event_cursor(str(params.after_event_id), session_id) from error.__cause__
        resume_cursor: str | None = None

        if subevent_index is not None:
            if cursor is None or subevent_index >= len(resume_payloads) - 1:
                raise _invalid_event_cursor(str(params.after_event_id), session_id)
            resume_cursor = cursor

        yield harness_session.TransportStreamStarted()

        last_event_id = params.after_event_id
        if subevent_index is not None and resume_cursor is not None:
            for index, payload in enumerate(resume_payloads[subevent_index + 1 :], start=subevent_index + 1):
                last_event_id = _encode_event_id(
                    session_id,
                    resume_cursor,
                    subevent_index=index if index < len(resume_payloads) - 1 else None,
                )
                yield _relayed_event(
                    event_id=last_event_id,
                    emitted_at=projection.session.updated_at,
                    session_id=str(session_id),
                    root_session_id=projection.session.root_session_id,
                    payload=payload,
                )

        loop = asyncio.get_running_loop()
        reconnect_delay = _RETRY_INITIAL_SECONDS
        # A dropped connection is retried from the cursor of the last applied event until this
        # budget runs out. It restarts when an event arrives or a reopened stream sends something
        # and stays open, so only a lasting outage ends the stream.
        lost_stream = _LostStreamBudget(loop, session_id, budget_seconds=reconnect_budget_seconds)

        def opened() -> None:
            lost_stream.stream_opened()
            if on_open is not None:
                on_open()

        while not self._closed and projection.session.status != "terminated":
            attempt = lost_stream.start_attempt()
            stream_error: httpx.HTTPError | None = None
            try:
                async with attempt:
                    try:
                        async for observed in self._sessions.stream_session_events(
                            agent_session_id=session_id,
                            cursor=cursor,
                            on_open=opened,
                            on_activity=lost_stream.stream_active,
                        ):
                            # Remove the attempt limit before the yield below: it must not run while
                            # the caller handles the event.
                            lost_stream.stream_recovered()
                            reconnect_delay = _RETRY_INITIAL_SECONDS
                            repeated = projection.has_seen(observed.sequence)
                            payload = projection.apply(observed)
                            cursor = projection.product_cursor
                            payloads = ([] if payload is None else [payload]) + projection.take_pending_events()
                            if not payloads:
                                # A frame that carries no event still moves the reader's position:
                                # a session read's cursor can name it, and a reader waiting for that
                                # cursor would otherwise never see it. A repeated frame gave it already.
                                if not repeated:
                                    last_event_id = _encode_event_id(session_id, observed.sequence)
                                    yield harness_session.TransportHeartbeat(latest_event_id=last_event_id)
                                continue
                            emitted_at = _relayed_emitted_at(projection)
                            events = [
                                _relayed_event(
                                    event_id=_encode_event_id(
                                        session_id,
                                        observed.sequence,
                                        subevent_index=index if index < len(payloads) - 1 else None,
                                    ),
                                    emitted_at=emitted_at,
                                    session_id=str(session_id),
                                    root_session_id=projection.session.root_session_id,
                                    payload=event_payload,
                                )
                                for index, event_payload in enumerate(payloads)
                            ]
                            last_event_id = events[-1].event_id
                            yield events[0] if len(events) == 1 else harness_session.EventBatch(events=events)
                    except httpx.HTTPError as error:
                        # v1 publishes no terminal event, so a Session that ended while `/events`
                        # failed shows only on its row: read the row before reconnecting.
                        if self._closed or not _is_transient_read_failure(error):
                            raise
                        stream_error = error

                    if projection.session.status == "terminated" or self._closed:
                        break

                    product = await self._read_bound_session(session_id)
                    product_is_terminal = product.status in {
                        AgentSessionStatus.COMPLETED,
                        AgentSessionStatus.FAILED,
                        AgentSessionStatus.TERMINATED,
                    }
                    if stream_error is None:
                        lost_stream.stream_recovered()
                    elif not product_is_terminal:
                        raise stream_error
            except httpx.HTTPError as error:
                if self._closed or not _is_transient_read_failure(error):
                    raise
                # A v1 round can fail on `/events` and then on the lookup: report the stream error.
                remaining = lost_stream.record_failure(stream_error or error)
                if remaining <= 0:
                    raise lost_stream.lost_error(after_event_id=last_event_id) from error
                await lost_stream.wait_before_retry(remaining)
                continue
            except TimeoutError as error:
                if not attempt.expired():
                    raise
                # A new attempt hung until the budget ran out, for example a connect that waits
                # for the client's read timeout.
                raise lost_stream.lost_error(after_event_id=last_event_id) from error

            if product_is_terminal:
                # v1 excludes session_terminated from the read contract on purpose, so no
                # terminal event is coming. The product row is the signal: adopt it and let
                # the loop condition end the stream, rather than time out waiting. Relay the
                # Turns it terminates first, so a reader following one learns its outcome.
                events = _reconciled_turn_events(
                    projection,
                    projection.adopt_terminal_product(product),
                    session_id=session_id,
                    after_index=reconciled_through,
                )
                if events:
                    last_event_id = events[-1].event_id
                    yield events[0] if len(events) == 1 else harness_session.EventBatch(events=events)

            await asyncio.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, _RETRY_MAX_SECONDS)

        yield harness_session.TransportStreamEnded(
            reason="client_closed" if self._closed else "server_closed",
            latest_event_id=_last_event_id(projection),
        )

    @public_iter_errors
    async def watch_callbacks_tree(
        self,
        params: harness_session.CallbacksTreeParams,
    ) -> AsyncIterator[harness_session.CallbacksTreeResponse]:
        """Follow `/callbacks/stream`: the open callbacks of the Session and its descendants.

        The server sends the full list at once and again on each change. A dropped stream is
        reopened like the event stream; the list ends when the Session ends.
        """

        session_id = self._require_session_id(params.session_id)
        await self._require_session_v1()
        if self._no_callbacks_tree:
            raise _tree_unsupported()
        lost_stream = _LostStreamBudget(asyncio.get_running_loop(), session_id, stream="callbacks")
        reconnect_delay = _RETRY_INITIAL_SECONDS
        last: harness_session.CallbacksTreeResponse | None = None
        while not self._closed:
            attempt = lost_stream.start_attempt()
            try:
                async with attempt:
                    async for frame in self._sessions.stream_session_callbacks(
                        agent_session_id=session_id,
                        on_open=lost_stream.stream_opened,
                        on_activity=lost_stream.stream_active,
                    ):
                        # Remove the attempt limit before the yield below, as `read_events` does.
                        lost_stream.stream_recovered()
                        reconnect_delay = _RETRY_INITIAL_SECONDS
                        if frame == last:
                            continue
                        last = frame
                        yield frame
                    if self._closed:
                        return
                    # The server closed the stream: it ends with the Session, else reconnect.
                    product = await self._sessions.get_session(agent_session_id=session_id)
                    lost_stream.stream_recovered()
            except httpx.HTTPError as error:
                if isinstance(error, httpx.HTTPStatusError) and _route_missing(error):
                    self._no_callbacks_tree = True
                    raise _tree_unsupported() from error
                if self._closed or not _is_transient_read_failure(error):
                    raise
                remaining = lost_stream.record_failure(error)
                if remaining <= 0:
                    raise lost_stream.lost_error(after_event_id=None) from error
                await lost_stream.wait_before_retry(remaining)
                continue
            except TimeoutError as error:
                if not attempt.expired():
                    raise
                raise lost_stream.lost_error(after_event_id=None) from error
            if product.status in _TERMINAL_PRODUCT_STATUSES:
                return
            await asyncio.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, _RETRY_MAX_SECONDS)

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        cleanup_error: BaseException | None = None
        if self._owns_sessions_client:
            try:
                await self._sessions.aclose()
            except BaseException as error:
                cleanup_error = error
        if self._owns_agents_client and self._agents is not None:
            try:
                await self._agents.aclose()
            except BaseException as error:
                if cleanup_error is None:
                    cleanup_error = error
                else:
                    cleanup_error.add_note(f"Agents client cleanup failed: {error!r}")
        if cleanup_error is not None:
            raise cleanup_error

    async def _read_session(
        self,
        params: harness_session.SessionReadParams,
    ) -> harness_session.SessionReadResponse:
        session_id = self._require_session_id(params.session_id)
        async with self._read_projection_lock:
            # The product row is read before history, so the history read after it already holds
            # any terminal event behind a terminal row and the row only fills in a closure history
            # never retained. Both are read under the lock, so a read never reports an older row
            # than a read on this client that completed before it.
            product = await self._read_bound_session(session_id)
            projection = await self._advance_read_projection(product)
            last_event_id = _last_event_id(projection)
            state, ended_turns = projection.state_with_product(product)
            # A reader relays these Turns' ends after the last frame, each with an id of its
            # own: the read is at the last of them.
            relayed = _reconciled_turn_events(projection, ended_turns, session_id=session_id, after_index=None)
            if relayed:
                last_event_id = relayed[-1].event_id
        # Pages come from the returned state, not the projection, so a closure the product
        # row reported reaches the paged Turns too.
        if params.history is not None:
            state = state.model_copy(
                update={
                    "history": _build_page(
                        state.history.items,
                        params.history,
                        item_id=lambda entry: entry.id,
                    )
                }
            )
        if params.turns is not None:
            state = state.model_copy(
                update={
                    "turns": _build_page(
                        state.turns.items,
                        params.turns,
                        item_id=lambda turn: turn.id,
                    )
                }
            )
        return harness_session.SessionReadResponse(state=state, last_event_id=last_event_id)

    async def _list_history(
        self,
        params: harness_session.SessionHistoryListParams,
    ) -> harness_session.SessionHistoryListResponse:
        self._require_session_id(params.session_id)
        projection = await self._read_current_projection()
        entries = projection.history
        if params.turn_id is not None:
            entries = [entry for entry in entries if entry.turn_id == params.turn_id]
        return harness_session.SessionHistoryListResponse(
            page=_build_page(entries, params.page, item_id=lambda entry: entry.id)
        )

    async def _list_turns(
        self,
        params: harness_session.SessionTurnsListParams,
    ) -> harness_session.SessionTurnsListResponse:
        self._require_session_id(params.session_id)
        projection = await self._read_current_projection()
        return harness_session.SessionTurnsListResponse(
            page=_build_page(
                list(projection.turns.values()),
                params.page,
                item_id=lambda turn: turn.id,
            )
        )

    async def _send_message(
        self,
        params: harness_session.MessageSendParams,
    ) -> harness_session.MessageSendResponse:
        """Let the Session start a Turn or steer the running one, and report the Turn joined.

        The control plane answers on the call, so there is nothing to poll. A 500, a 503, a 504, a
        gateway 502, a lost connection or a busy 429 is retried with the same idempotency key
        until the outcome budget is spent: the Session deduplicates it and replays the original
        receipt. A ``Retry-After`` delays the next attempt. The budget bounds each attempt too, and
        this loop owns every retry because ``make_request`` does not retry a POST. An older Agent or an
        older control plane cannot serve it, and there is no fallback: nothing on ``/commands``
        starts or steers depending on the running Turn.
        """

        session_id = self._require_session_id(params.session_id)
        # One key for every attempt, so the Session deduplicates the retries.
        idempotency_key = params.idempotency_key or params.message_entry_id or uuid4().hex

        def refusal(error: httpx.HTTPStatusError) -> Exception | None:
            refused = _send_message_refusal(error, idempotency_key=idempotency_key)
            if isinstance(refused, harness_session.SessionTerminatedError):
                self._refused_turn_ids.add(message_command_id(str(session_id), idempotency_key))
            return refused

        # Not `_call_procedure`: there is no fallback to remember a 501 for, and a 501 can refuse
        # one message's format only, so every send asks the control plane.
        try:
            return await _retry_within_budget(
                lambda: self._sessions.send_message(
                    agent_session_id=session_id,
                    message=params.message,
                    idempotency_key=idempotency_key,
                    context_messages=params.context_messages,
                    message_entry_id=params.message_entry_id,
                    source=wire.AGENTS_SDK_COMMAND_SOURCE,
                ),
                classify=_refusing(refusal),
                outcome_unknown=lambda: _unconfirmed(f"message {idempotency_key}", idempotency_key=idempotency_key),
                # An attempt after the pause would be cut short during the Agent's busy wait.
                busy_wait_seconds=wire.SEND_MESSAGE_BUSY_WAIT_SECONDS,
            )
        except RemoteSessionProcedureUnsupportedError as unsupported:
            # The control plane refuses send_message on a legacy Session with a 501: name that cause.
            try:
                await self._require_session_v1()
            except httpx.HTTPError:
                # The Session could not be read: the refusal is still the clearest error.
                raise unsupported from None
            raise

    async def _start_turn(
        self,
        params: harness_session.TurnStartParams,
    ) -> harness_session.TurnStartResponse:
        """Start a Turn, retrying the submit while its outcome is unknown.

        Every attempt sends the same command id, and the control plane applies a command id
        once, so a retry cannot start a second Turn. A 500, a 503, a 504, a gateway 502, a lost
        connection or a busy 429 is retried until the outcome budget is spent, as in
        ``_send_message``. Then, or when the Turn is not confirmed after a taken submit,
        ``OutcomeUnknownError`` names the key that retries the same start safely,
        also when the caller passed none, unless another Turn ran (see below). The route, the
        submit retries and the wait for the Turn share one outcome budget. A start that was busy
        on every attempt applied nothing and raises ``SessionBusyError``, as ``_send_message``
        does. So does a start the Session refused because a Turn runs, on the route and on
        ``/commands``: ``_RemoteSessionTurnActiveError`` names that Turn.

        Only the Turn the start opened is returned. An agent deployed with an older SDK refuses a
        start while a Turn runs without saying so, and keeps refusing its key; that start never
        shows a Turn, and the wait ends in ``OutcomeUnknownError`` rather than in
        another caller's Turn. When another Turn ran during the wait, its message names that Turn
        and asks for a new key, also when that Turn has ended by then, and its ``idempotency_key``
        is ``None``.
        """

        session_id = self._require_session_id(params.session_id)
        _refuse_context_messages("app_server/session/turn/start", params.context_messages)
        # One key for every attempt, so the Session deduplicates the retries.
        idempotency_anchor = params.idempotency_key or params.message_entry_id or uuid4().hex
        command_id = sdk_command_id("turn", idempotency_anchor)

        # The other Turns seen running while the start waited, in order.
        other_turns_seen: list[str] = []

        def outcome_unknown(running_turn_id: str | None = None) -> OutcomeUnknownError:
            confirm = (
                f"Vibe Agents did not confirm the start of Turn {command_id} "
                f"within {_OUTCOME_TIMEOUT_SECONDS:g} seconds"
            )
            # An older agent refuses a start while a Turn runs without reporting it, and keeps
            # refusing that key: the same key would wait out the budget again, even once that
            # Turn has ended.
            older_agent = (
                "An agent deployed with an older Agents SDK refuses a start while a Turn runs without "
                "reporting it, and keeps refusing its key"
            )
            if running_turn_id is not None:
                message = (
                    f"{confirm}, and Turn {running_turn_id} is running. {older_agent}: "
                    f"once Turn {running_turn_id} ends, start the Turn again with a new idempotency key"
                )
            elif other_turns_seen:
                message = (
                    f"{confirm}, and Turn {other_turns_seen[-1]} was running. {older_agent}: "
                    "start the Turn again with a new idempotency key"
                )
            else:
                message = (
                    f"{confirm}; start the Turn again with idempotency_key={idempotency_anchor!r} "
                    "so that it cannot start twice"
                )
                return OutcomeUnknownError(message, idempotency_key=idempotency_anchor)
            # The refused key started nothing and would be refused again: no key to retry with.
            return OutcomeUnknownError(message, idempotency_key=None)

        def refusal(error: httpx.HTTPStatusError) -> Exception | None:
            return _turn_start_refusal(error, idempotency_key=idempotency_anchor)

        loop = asyncio.get_running_loop()
        deadline = loop.time() + _OUTCOME_TIMEOUT_SECONDS
        routed = await self._call_procedure(
            session_id,
            "turn/start",
            procedure_api.TurnStartRequest(
                message=params.message, idempotency_key=idempotency_anchor, source=wire.AGENTS_SDK_COMMAND_SOURCE
            ),
            harness_session.TurnStartResponse,
            refusal=refusal,
            outcome_unknown=outcome_unknown,
            deadline=deadline,
        )
        if routed is not None:
            return _with_route_cursor(routed, session_id)
        # FIXME: delete once MAIS 2026.11 is released
        await self._require_session_v1()

        async def submit() -> None:
            await self._sessions.submit_message(
                agent_session_id=session_id,
                source=wire.AGENTS_SDK_COMMAND_SOURCE,
                message=_build_message_input(params.message),
                command_id=command_id,
            )

        await _retry_within_budget(
            submit,
            classify=_refusing(refusal),
            outcome_unknown=outcome_unknown,
            deadline=deadline,
        )
        turn_id = str(command_id)
        # The wait still reads the Session once when the submit used the whole budget.
        remaining = max(deadline - loop.time(), 0.0)
        try:
            return await self._await_v1_turn_start(
                command_id=turn_id, timeout_seconds=remaining, other_turns_seen=other_turns_seen
            )
        except OutcomeUnknownError as error:
            # The submit was taken, so the Turn may have started. Only the same key retries it
            # safely, and the caller may not know it when the SDK generated it.
            raise outcome_unknown(await self._other_running_turn_id(turn_id)) from error

    async def _steer_turn(
        self,
        params: harness_session.TurnSteerParams,
    ) -> harness_session.TurnSteerResponse:
        session_id = self._require_session_id(params.session_id)
        _refuse_context_messages("app_server/session/turn/steer", params.context_messages)
        idempotency_anchor = params.idempotency_key or params.message_entry_id or uuid4().hex
        command_id = sdk_command_id("steer", idempotency_anchor)
        # The route, the fallback submit and the wait for its outcome share one outcome budget.
        deadline = asyncio.get_running_loop().time() + _OUTCOME_TIMEOUT_SECONDS
        routed = await self._call_procedure(
            session_id,
            "turn/steer",
            procedure_api.TurnSteerRequest(
                message=params.message,
                idempotency_key=idempotency_anchor,
                expected_turn_id=params.expected_turn_id,
                source=wire.AGENTS_SDK_COMMAND_SOURCE,
            ),
            harness_session.TurnSteerResponse,
            refusal=lambda error: _turn_steer_refusal(error, idempotency_key=idempotency_anchor),
            outcome_unknown=lambda: _unconfirmed(f"steer {command_id}", idempotency_key=idempotency_anchor),
            deadline=deadline,
        )
        if routed is not None:
            return _with_route_cursor(routed, session_id)
        # FIXME: delete once MAIS 2026.11 is released
        await self._require_session_v1()
        try:
            # The same command_id on every attempt, so a retry cannot steer twice.
            await _retry_busy_within_budget(
                lambda: self._sessions.submit_message(
                    agent_session_id=session_id,
                    source=wire.AGENTS_SDK_COMMAND_SOURCE,
                    message=_build_message_input(params.message),
                    command_id=command_id,
                    expected_turn_id=params.expected_turn_id,
                ),
                command_id=command_id,
                deadline=deadline,
            )
        except SessionCommandRejectedError as error:
            raise RemoteSessionTurnConflictError(str(error)) from error
        # The control plane answered the compare-and-set on the call itself, so reaching here
        # means the Session applied it.
        return harness_session.TurnSteerResponse(last_event_id=await self._current_last_event_id())

    async def _interrupt_turn(
        self,
        params: harness_session.TurnInterruptParams,
    ) -> harness_session.TurnInterruptResponse:
        session_id = self._require_session_id(params.session_id)
        command_id = sdk_command_id("interrupt", params.expected_turn_id)
        # The route, the fallback submit and the wait for its outcome share one outcome budget.
        deadline = asyncio.get_running_loop().time() + _OUTCOME_TIMEOUT_SECONDS
        routed = await self._call_procedure(
            session_id,
            "turn/interrupt",
            procedure_api.TurnInterruptRequest(
                expected_turn_id=params.expected_turn_id,
                reason=params.reason,
                source=wire.AGENTS_SDK_COMMAND_SOURCE,
            ),
            harness_session.TurnInterruptResponse,
            refusal=_turn_conflict,
            outcome_unknown=lambda: _unconfirmed(f"interrupt {command_id}"),
            deadline=deadline,
        )
        if routed is not None:
            return _with_route_cursor(routed, session_id)
        # FIXME: delete once MAIS 2026.11 is released
        await self._require_session_v1()
        try:
            await _retry_busy_within_budget(
                lambda: self._sessions.interrupt_session(
                    agent_session_id=session_id,
                    source=wire.AGENTS_SDK_COMMAND_SOURCE,
                    expected_turn_id=params.expected_turn_id,
                    command_id=command_id,
                    reason=params.reason,
                ),
                command_id=command_id,
                deadline=deadline,
            )
        except SessionCommandRejectedError as error:
            raise RemoteSessionTurnConflictError(str(error)) from error
        return harness_session.TurnInterruptResponse(last_event_id=await self._current_last_event_id())

    async def _cancel_session(
        self,
        params: harness_session.SessionCancelParams,
    ) -> harness_session.SessionCancelResponse:
        """Ensure the Session stops: a Session that already ended answers success.

        A Session whose Agent Deployment is gone raises ``SessionTerminatedError`` on both paths.
        """

        session_id = self._require_session_id(params.session_id)
        idempotency_key = params.idempotency_key or uuid4().hex
        command_id = sdk_command_id("cancel", idempotency_key)
        routed = await self._call_procedure(
            session_id,
            "cancel",
            procedure_api.SessionCancelRequest(
                idempotency_key=idempotency_key, reason=params.reason, source=wire.AGENTS_SDK_COMMAND_SOURCE
            ),
            harness_session.SessionCancelResponse,
            refusal=lambda _error: None,
            outcome_unknown=lambda: _unconfirmed(f"cancel {command_id}", idempotency_key=idempotency_key),
            deadline=asyncio.get_running_loop().time() + _OUTCOME_TIMEOUT_SECONDS,
        )
        if routed is not None:
            return routed
        # FIXME: delete once MAIS 2026.11 is released
        try:
            await self._sessions.cancel_session(
                agent_session_id=session_id,
                source=wire.AGENTS_SDK_COMMAND_SOURCE,
                command_id=command_id,
                reason=params.reason,
            )
        except httpx.HTTPStatusError as error:
            status_code = error.response.status_code
            if status_code == httpx.codes.GONE:
                # The Session already ended, which is what a cancel ensures.
                return harness_session.SessionCancelResponse()
            if status_code == httpx.codes.CONFLICT:
                # `/commands` answers 409 only when the Agent Deployment is gone; the route answers 410.
                raise harness_session.SessionTerminatedError(
                    _detail_message(error, "The Agent Deployment of the Session is gone")
                ) from error
            raise
        return harness_session.SessionCancelResponse()

    async def _answer_callback(
        self,
        params: harness_session.CallbackResultParams,
    ) -> harness_session.CallbackResultResponse:
        attached_id = self._require_session_id()
        try:
            session_id = UUID(params.session_id)
        except ValueError as error:
            raise sdk_errors.SdkError(f"Remote Session id must be a UUID: {params.session_id!r}") from error
        callback_id = _parse_remote_callback_id(params.result.callback_id)
        loop = asyncio.get_running_loop()
        # The route, the fallback submit and the wait for its acknowledgement share one outcome budget.
        deadline = loop.time() + _OUTCOME_TIMEOUT_SECONDS
        routed = await self._call_procedure(
            session_id,
            "callback/result",
            # The canonical id, as `/callbacks` sends it, so both paths name the same callback.
            procedure_api.CallbackResultRequest(
                result=params.result.model_copy(update={"callback_id": str(callback_id)})
            ),
            harness_session.CallbackResultResponse,
            refusal=lambda error: _callback_refusal(error, callback_id=callback_id),
            outcome_unknown=lambda: _unconfirmed(f"callback {callback_id}", idempotency_key=str(callback_id)),
            deadline=deadline,
        )
        if routed is not None:
            # The route answers once the control plane recorded the resolution, which its open
            # callbacks list reads too, so there is nothing left to wait for.
            if session_id != attached_id:
                # A callback of another Session of the tree: this transport follows the events of
                # its own Session only, and the cursor is the owner's.
                return harness_session.CallbackResultResponse(last_event_id=_empty_cursor(session_id))
            return _with_route_cursor(routed, session_id)
        # FIXME: delete once MAIS 2026.11 is released
        # A subagent's Session has its root's protocol, so checking the bound Session covers it.
        await self._require_session_v1()
        await self._submit_callback_result(
            session_id=session_id, callback_id=callback_id, result=params.result, deadline=deadline
        )
        if session_id != attached_id:
            # The open callbacks list acknowledges the answer, as the owner's event cursor is not known here.
            await self._wait_until_not_listed(session_id, callback_id, deadline=deadline)
            return harness_session.CallbackResultResponse(last_event_id=_empty_cursor(session_id))
        # `/callbacks` answers before the resolution, so wait until the Session shows it.
        try:
            acknowledged = await self._wait_for_projection(
                lambda candidate: str(callback_id) in candidate.resolved_callback_ids,
                description=f"callback {callback_id} result acknowledgement",
                # The wait still reads the Session once when the route or the submit used the whole budget.
                timeout_seconds=max(deadline - loop.time(), 0.0),
            )
        except OutcomeUnknownError as error:
            raise _unconfirmed(f"callback {callback_id}", idempotency_key=str(callback_id)) from error
        return harness_session.CallbackResultResponse(last_event_id=_last_event_id(acknowledged))

    # FIXME: delete once MAIS 2026.11 is released
    async def _wait_until_not_listed(self, session_id: UUID, callback_id: UUID, *, deadline: float) -> None:
        """Wait until the control plane's open callbacks of ``session_id`` no longer list ``callback_id``.

        `/callbacks` takes an answer before the control plane records its resolution, so a read
        right after the answer could still list the callback as open. A control plane without the
        list, or one that leaves the Session's callbacks out of it, has nothing to wait on. The
        wait shares the answer's outcome budget, which ends at ``deadline`` on the loop's clock; it
        still reads the list once when the answer used the whole budget.

        Raises:
            OutcomeUnknownError: The list still has the callback at ``deadline``.
        """

        loop = asyncio.get_running_loop()
        delay = _RETRY_INITIAL_SECONDS
        while not self._no_callbacks_tree:
            try:
                tree = await self._sessions.read_session_callbacks(agent_session_id=session_id)
            except httpx.HTTPError as error:
                if isinstance(error, httpx.HTTPStatusError) and _route_missing(error):
                    self._no_callbacks_tree = True
                    return
                if not _is_transient_read_failure(error):
                    raise
            else:
                if all(item.callback.id != str(callback_id) for item in tree.callbacks):
                    return
            if loop.time() >= deadline:
                raise _unconfirmed(f"callback {callback_id}", idempotency_key=str(callback_id))
            await asyncio.sleep(delay)
            delay = min(delay * 2, _RETRY_MAX_SECONDS)

    # FIXME: delete once MAIS 2026.11 is released
    async def _submit_callback_result(
        self,
        *,
        session_id: UUID,
        callback_id: UUID,
        result: harness_session.CallbackResult,
        deadline: float,
    ) -> None:
        """Submit a callback answer on ``/callbacks``, retrying an unknown outcome until ``deadline``.

        The callback id is the idempotency key: the control plane replays an answer it already
        took as accepted. A 500, a 503, a 504, a gateway 502 or a lost connection is retried, as
        in `_send_message`, and a ``Retry-After`` delays the next attempt.
        """

        if result.error is None:
            payload = wire.CallbackResultPayload.completed(task_id=callback_id, value=result.output)
            if result.content is not None or result.is_error or result.meta:
                task_state = payload.payload.result
                payload.payload.result = task_state.model_copy(
                    update={
                        "output": task_state.output.model_copy(
                            update={
                                "content": (
                                    None
                                    if result.content is None
                                    else [block.model_dump(mode="json") for block in result.content]
                                ),
                                "is_error": result.is_error,
                                "meta": result.meta,
                            }
                        )
                    }
                )
        else:
            payload = wire.CallbackResultPayload(
                payload=wire.CallbackResultEventPayload(
                    task_id=str(callback_id),
                    result=wire.CallbackResultTaskState(
                        id=str(callback_id),
                        output=wire.CallbackResultTaskOutput(status="failed", error=result.error.message),
                    ),
                )
            )
        try:
            await _retry_within_budget(
                lambda: self._sessions.submit_callback_result(
                    agent_session_id=session_id,
                    callback_id=callback_id,
                    result=payload,
                ),
                classify=lambda error: "unknown" if _send_message_outcome_unknown(error) else None,
                outcome_unknown=lambda: _unconfirmed(f"callback {callback_id}", idempotency_key=str(callback_id)),
                deadline=deadline,
            )
        except httpx.HTTPStatusError as error:
            if (refusal := _callback_refusal(error, callback_id=callback_id)) is not None:
                raise refusal from error
            raise

    async def _call_procedure[ResponseT: harness_session.SessionModel](
        self,
        session_id: UUID,
        route: ProcedureRoute,
        body: harness_session.SessionModel,
        response_type: type[ResponseT],
        *,
        refusal: Callable[[httpx.HTTPStatusError], Exception | None],
        outcome_unknown: Callable[[], Exception],
        deadline: float,
    ) -> ResponseT | None:
        """Call a Session protocol route, or return None when the caller must fall back.

        A 501 (this Session or its Worker cannot serve the procedure, and nothing was applied) or
        the framework's bare 404 (a control plane without the route) is remembered on the
        deployment for this Session and route, so later calls, from any transport bound to that
        deployment, go straight to the fallback. The fallback sends the same command id, so a
        command an earlier attempt applied is not applied twice, and gets the same ``deadline``,
        so both share one budget. ``refusal`` types the procedure's own
        refusals; a 403, a 410 and a named 404 reach ``request()``. Every attempt sends the same
        body and the server replays a command id it took, so a busy or unknown outcome is retried
        until ``deadline``, as ``_retry_within_budget`` describes.
        """

        if (session_id, route) in self._deployment.unserved_routes:
            return None
        try:
            return await _retry_within_budget(
                lambda: self._sessions._post_procedure(
                    agent_session_id=session_id, route=route, body=body, response_type=response_type
                ),
                classify=_refusing(refusal),
                outcome_unknown=outcome_unknown,
                deadline=deadline,
            )
        except httpx.HTTPStatusError as error:
            if error.response.status_code != httpx.codes.NOT_IMPLEMENTED and not _route_missing(error):
                raise
            self._deployment.unserved_routes.add((session_id, route))
            return None

    async def _resolve_deployment_name(self) -> str:
        if self._resolved_deployment_name is not None:
            return self._resolved_deployment_name
        deployment_id = self._deployment.agent_deployment_id
        if deployment_id is None:
            raise sdk_runtime_error("Remote Agent Deployment has no resolvable identity")
        if self._agents is None:
            raise sdk_runtime_error("Agent Deployment id lookup requires bearer authentication")
        try:
            product = await self._agents.get_agent(deployment_id)
        except httpx.HTTPStatusError as error:
            if error.response.status_code == httpx.codes.NOT_FOUND:
                raise RemoteAgentDeploymentNotFoundError(
                    f"Agent Deployment {deployment_id} no longer exists; it may have been shut down"
                ) from error
            raise
        self._resolved_deployment_name = product.agent_name
        return product.agent_name

    async def _read_current_projection(self) -> VibeAgentsSessionV1Projection:
        """Advance one transport-local projection for Session reads.

        Event readers and command polling use private projections because their
        cursors and lifetimes differ. Session reads and History and Turn pages
        share this guarded projection, so a caller that reads the same Session
        repeatedly fetches only the history retained since its last read instead
        of replaying it from the beginning every time.
        """

        async with self._read_projection_lock:
            return await self._advance_read_projection()

    async def _advance_read_projection(
        self, product: AgentSessionResponse | None = None
    ) -> VibeAgentsSessionV1Projection:
        """Advance the shared read projection; the caller holds ``_read_projection_lock``.

        ``product`` seeds the projection when the caller already holds a fresh product row.
        """

        if self._read_projection is None:
            if product is None:
                product = await self._read_bound_session(self._require_session_id())
            self._read_projection = _new_projection(product, self._refused_turn_ids)
        await self._advance_projection(self._read_projection)
        return self._read_projection

    async def _read_bound_session(self, session_id: UUID) -> AgentSessionResponse:
        """Read the row of the Session this transport is bound to.

        Binding never checked that the Session exists, so a 404 here means the control plane does
        not know it.
        """

        try:
            return await self._sessions.get_session(agent_session_id=session_id)
        except httpx.HTTPStatusError as error:
            if error.response.status_code != httpx.codes.NOT_FOUND:
                raise
            raise sdk_errors.SessionNotFoundError(str(session_id), _detail_message(error, "")) from error

    async def _build_projection(
        self,
        product: AgentSessionResponse,
    ) -> VibeAgentsSessionV1Projection:
        projection = _new_projection(product, self._refused_turn_ids)
        await self._advance_projection(projection)
        return projection

    async def _build_stream_projection(
        self,
        product: AgentSessionResponse,
        *,
        cursor: str | None,
        capture_cursor: str | None = None,
    ) -> tuple[VibeAgentsSessionV1Projection, list[RelayedPayload]]:
        """Reconstruct retained history through the SSE resume position.

        Command acknowledgements poll retained history and may replace the
        transport's cached read projection while an event reader is active.
        Each reader therefore owns a projection aligned with its own cursor;
        otherwise a reconnect can apply an append patch to incomplete history.
        A valid SSE cursor can identify a relay-only event that is absent from
        retained history, so reconstruction stops before the first retained
        event that follows the requested cursor.
        """

        projection = _new_projection(product, self._refused_turn_ids)
        if cursor is None:
            return projection, []
        captured_payloads: list[RelayedPayload] = []
        await self._advance_projection(
            projection,
            replay_through=cursor,
            capture_sequence=capture_cursor,
            captured_payloads=captured_payloads,
        )
        return projection, captured_payloads

    async def _next_retained_cursor_after(self, cursor: str) -> str | None:
        try:
            page = await self._sessions.read_session_events_history(
                agent_session_id=self._require_session_id(),
                limit=1,
                cursor=cursor,
            )
        except httpx.HTTPStatusError as error:
            # The one history read that sends the caller's cursor, not one the control plane gave:
            # it answers 400 for a cursor it cannot decode, such as a truncated stored cursor.
            if error.response.status_code != httpx.codes.BAD_REQUEST:
                raise
            raise _UndecodableEventCursorError from error
        if not page.events:
            return None
        return page.events[0].sequence

    async def _advance_projection(
        self,
        projection: VibeAgentsSessionV1Projection,
        *,
        replay_through: str | None = None,
        capture_sequence: str | None = None,
        captured_payloads: list[RelayedPayload] | None = None,
    ) -> bool:
        projection.drop_refused_turn()
        cursor = projection.product_cursor
        observed_new_event = False
        stop_before: str | None = None
        while True:
            page = await self._sessions.read_session_events_history(
                agent_session_id=projection.product_session.agent_session_id,
                limit=200,
                cursor=cursor,
            )
            # An empty successor read only bounds history already fetched. Read
            # each page first so later arrivals remain visible to the SSE reader.
            # Once found, the successor cannot change: retained history is append-only.
            if replay_through is not None and stop_before is None:
                stop_before = await self._next_retained_cursor_after(replay_through)
            for observed in page.events:
                if observed.sequence == stop_before:
                    return observed_new_event
                payload = projection.apply(observed)
                pending = projection.take_pending_events()
                if observed.sequence == capture_sequence and captured_payloads is not None:
                    if payload is not None:
                        captured_payloads.append(payload)
                    captured_payloads.extend(pending)
                observed_new_event = True
            if page.next_cursor is None:
                break
            cursor = page.next_cursor
        return observed_new_event

    # FIXME: delete once MAIS 2026.11 is released
    async def _other_running_turn_id(self, turn_id: str) -> str | None:
        """The running Turn if it is not ``turn_id``, or None, also when the read fails."""

        try:
            projection = await self._read_current_projection()
        except httpx.HTTPError:
            return None
        active_turn_id = projection.active_turn_id
        return active_turn_id if active_turn_id != turn_id else None

    # FIXME: delete once MAIS 2026.11 is released
    async def _await_v1_turn_start(
        self,
        *,
        command_id: str,
        timeout_seconds: float,
        other_turns_seen: list[str],
    ) -> harness_session.TurnStartResponse:
        """Report the Turn a Session v1 start opened.

        v1 publishes no command outcome, so the start's own Turn appearing in the stream is the
        whole acknowledgement. Each other Turn seen running meanwhile is added to
        ``other_turns_seen``, which tells a start an older agent refused from a lost one.
        """

        def opened(candidate: VibeAgentsSessionV1Projection) -> bool:
            active_turn_id = candidate.active_turn_id
            if active_turn_id is not None and active_turn_id not in (command_id, *other_turns_seen):
                other_turns_seen.append(active_turn_id)
            return _v1_started_turn(candidate, command_id) is not None

        started = await self._wait_for_projection(
            opened,
            description=f"the Turn opened for command {command_id}",
            timeout_seconds=timeout_seconds,
        )
        turn = _v1_started_turn(started, command_id)
        if turn is None:
            raise OutcomeUnknownError(f"Vibe Agents accepted command {command_id} but reported no Turn")
        return harness_session.TurnStartResponse(turn=turn, last_event_id=_last_event_id(started))

    async def _require_session_v1(self) -> None:
        """Raise ``LegacySessionError`` unless the bound Session uses Session v1, read once and remembered.

        A Session's protocol is fixed at creation, so only the first call reads its row. Calls that
        read the Session's events check its row anyway. The `/commands` and `/callbacks` fallbacks
        call this before they send; `message/send`, which the control plane refuses with a 501 on a
        legacy Session, calls it after that refusal.
        """

        if not self._session_v1_checked:
            _require_session_v1(await self._read_bound_session(self._require_session_id()))
            self._session_v1_checked = True

    # FIXME: delete once MAIS 2026.11 is released
    async def _current_last_event_id(self) -> str:
        """The resume cursor after a command the Session already confirmed applied."""

        projection = await self._read_current_projection()
        return _last_event_id(projection)

    async def _wait_for_projection(
        self,
        predicate: Callable[[VibeAgentsSessionV1Projection], bool],
        *,
        description: str,
        timeout_seconds: float,
        product_session: AgentSessionResponse | None = None,
        session_start: bool = False,
    ) -> VibeAgentsSessionV1Projection:
        """Poll the Session history until `predicate` holds, then return the projection.

        Raise `OutcomeUnknownError` if `predicate` still fails after `timeout_seconds`.
        The wait between reads doubles from _RETRY_INITIAL_SECONDS up to _RETRY_MAX_SECONDS. A read
        that finds new events resets it. A Session start (`session_start=True`) differs:
        - The wait doubles from _START_POLL_MIN_SECONDS up to _START_POLL_MAX_SECONDS.
        - New events do not reset the wait. A starting Session can publish events for its whole
          startup, so a reset would keep a slow start polling at the minimum.
        - After each read that does not meet `predicate`, it reads the Session status and raises
          `RemoteSessionStartFailedError` if the Session already ended. A rejected start ends
          before it publishes any initialization event, so the wait would otherwise run to the
          timeout.
        """
        session_id = self._require_session_id()
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout_seconds
        product = product_session or await self._read_bound_session(session_id)
        projection = await self._build_projection(product)
        if session_start:
            poll_min, poll_max = _START_POLL_MIN_SECONDS, _START_POLL_MAX_SECONDS
        else:
            poll_min, poll_max = _RETRY_INITIAL_SECONDS, _RETRY_MAX_SECONDS
        poll_interval = poll_min
        while True:
            if predicate(projection):
                return projection
            if loop.time() >= deadline:
                raise OutcomeUnknownError(
                    f"Vibe Agents did not retain {description} within {timeout_seconds:g} seconds"
                )
            await asyncio.sleep(poll_interval)
            try:
                advanced = await self._advance_projection(projection)
                if session_start and not predicate(projection):
                    await self._raise_if_product_terminal(session_id, projection, predicate)
            except httpx.HTTPError as error:
                if not _is_transient_read_failure(error):
                    raise
                advanced = False
            if advanced and not session_start:
                poll_interval = poll_min
            else:
                poll_interval = min(poll_interval * 2, poll_max)

    async def _raise_if_product_terminal(
        self,
        session_id: UUID,
        projection: VibeAgentsSessionV1Projection,
        predicate: Callable[[VibeAgentsSessionV1Projection], bool],
    ) -> None:
        """Fail fast if the Session already ended while we wait for it to become ready.

        A Session the worker rejects at startup (a missing session input, a sandbox error, ...) ends without
        ever being ready. Raise the failure the control plane kept, instead of polling until the timeout.
        """
        product = await self._read_bound_session(session_id)
        if product.status not in _TERMINAL_PRODUCT_STATUSES:
            return
        # A single-turn Session can end just after its Turn ends. Read the events again: the Session
        # published them all before its status changed.
        await self._advance_projection(projection)
        if predicate(projection):
            return
        raise RemoteSessionStartFailedError(
            f"Session {session_id} ended before it was ready ({product.status.value}): "
            f"{product.error or 'no failure was retained'}"
        )

    def _require_session_id(self, expected: str | None = None) -> UUID:
        if self._session_id is None:
            raise sdk_runtime_error("Remote Session transport is not attached")
        if expected is not None and expected != str(self._session_id):
            raise RemoteSessionConflictError(f"Transport is attached to {self._session_id}, not {expected}")
        return self._session_id


def _is_transient_read_failure(error: httpx.HTTPError) -> bool:
    if isinstance(error, httpx.HTTPStatusError):
        status = error.response.status_code
        return status == httpx.codes.TOO_MANY_REQUESTS or status >= httpx.codes.INTERNAL_SERVER_ERROR
    return isinstance(error, httpx.TransportError)


async def _create_remote_session(
    deployment: RemoteAgentDeployment,
    *,
    history: list[harness_session.HistoryImportEntry] | None = None,
    idempotency_key: str | None = None,
    agent: wire.SessionAgentCustomization | None = None,
    session_inputs: Mapping[str, JsonValue] | None = None,
    initial_turn: harness_session.InitialTurn | None = None,
    client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
) -> harness_session.SessionClient:
    settings = SessionClientSettings()
    transport = VibeAgentsSessionTransport(deployment)
    client = ClientToolSessionClient(transport, client_tools=client_tools)
    try:
        response = await transport.start_deployment_session(
            history=history or [],
            idempotency_key=idempotency_key,
            agent=agent,
            timeout_seconds=settings.session_startup_timeout_seconds,
            session_inputs=session_inputs,
            initial_turn=initial_turn,
        )
        await client.adopt_session_snapshot(response.state, response.last_event_id)
    except BaseException as setup_error:
        if initial_turn is not None:
            _note_initial_turn_goes_on(setup_error, transport._session_id)
        await _close_client_after_setup_failure(client, setup_error)
        raise
    return client


def _note_initial_turn_goes_on(start_error: BaseException, session_id: UUID | str | None) -> None:
    """Name the Session a start with an initial Turn stopped waiting for, when that Session goes on."""

    session_went_on = not isinstance(
        start_error,
        RemoteSessionStartFailedError | SessionStartupTimeoutError | harness_session.SessionMessageRejectedError,
    )
    if session_id is not None and session_went_on:
        # As agent.run() does for a Turn it stops waiting for: the Session goes on, so say which one.
        start_error.add_note(
            f"Session {session_id} is still starting with its initial Turn: the start stopped waiting for it. "
            "To stop it, cancel that Session."
        )


def _raise_if_message_refused(turn: harness_session.TurnState | None) -> None:
    """Raise ``SessionMessageRejectedError`` when ``turn`` is a first Turn whose message the Worker refused.

    The Worker publishes a refused first Turn as already terminated, and fails the Session.
    """
    if (
        turn is not None
        and isinstance(turn.termination, harness_session.FailedTermination)
        and turn.termination.error.code
        in {
            wire.SessionCommandVerdictReason.MESSAGE_TOO_LARGE.value,
            wire.SessionCommandVerdictReason.MESSAGE_REJECTED.value,
        }
    ):
        raise harness_session.SessionMessageRejectedError(turn.termination.error.message)


async def _start_remote_run(
    deployment: RemoteAgentDeployment,
    *,
    idempotency_key: str | None = None,
    agent: wire.SessionAgentCustomization | None = None,
    session_inputs: Mapping[str, JsonValue] | None = None,
    initial_turn: harness_session.InitialTurn | None = None,
) -> tuple[str, str | None]:
    """Start a Session, with ``initial_turn`` as its first Turn when given, in one request.

    Waits only while the Session is starting, attaches no client, and returns the Session's ID and
    its initial Turn's ID. The Turn's ID is ``None`` when the control plane or the Agent predates
    ``initial_turn``: the Session then starts idle.
    """

    transport = VibeAgentsSessionTransport(deployment)
    try:
        started = await transport.start_deployment_session(
            history=[],
            idempotency_key=idempotency_key,
            agent=agent,
            session_inputs=session_inputs,
            timeout_seconds=SessionClientSettings().session_startup_timeout_seconds,
            until_started=True,
            initial_turn=initial_turn,
        )
    except BaseException as start_error:
        if initial_turn is not None:
            _note_initial_turn_goes_on(start_error, transport._session_id)
        try:
            await transport.close()
        except BaseException as cleanup_error:
            start_error.add_note(f"Remote Session cleanup failed: {cleanup_error!r}")
        raise
    session_id = str(transport._require_session_id())
    try:
        await transport.close()
    except Exception:
        # The Session started: losing its ID to a cleanup failure would orphan it.
        logger.warning("remote_session_start_cleanup_failed", session_id=session_id, exc_info=True)
    return session_id, started.initial_turn.id if started.initial_turn is not None else None


def _parse_remote_session_id(session_id: str) -> UUID:
    try:
        return UUID(session_id)
    except ValueError as error:
        raise sdk_errors.SdkError(f"Remote Session id must be a UUID: {session_id!r}") from error


def _parse_remote_callback_id(callback_id: str) -> UUID:
    try:
        return UUID(callback_id)
    except ValueError as error:
        raise sdk_errors.SdkError(f"Remote callback id must be a UUID: {callback_id!r}") from error


def _bind_remote_session(deployment: RemoteAgentDeployment, session_id: str) -> VibeAgentsSessionTransport:
    """Return a transport to a remote Session by its ID, without asking the control plane.

    An ID the control plane does not know binds too: the first read raises
    ``SessionNotFoundError``.
    """
    return VibeAgentsSessionTransport(deployment, session_id=_parse_remote_session_id(session_id))


def _client_urls(server_url: str | None, agents_url: str | None) -> tuple[str, str]:
    """Return the Mistral API root and the Agents control plane URL of an ``agents.Client``.

    ``server_url`` defaults to ``MISTRAL_API_URL``, else the public API root. ``agents_url``
    defaults to ``AGENTS_SDK_DEPLOY_CONTROL_PLANE_URL`` when ``server_url`` is not given, else to
    ``server_url`` + ``/v2/agents``.
    """
    for name, url in (("server_url", server_url), ("agents_url", agents_url)):
        if url is not None and (not isinstance(url, str) or not url.strip()):
            raise sdk_errors.SdkError(f"{name} must be a URL string or None, got {url!r}")
    root = (server_url or mistral_api_url() or SERVERS[SERVER_GLOBAL]).strip().rstrip("/")
    if agents_url is None:
        settings = ControlPlaneSettings()
        if server_url is None and "deploy_control_plane_url" in settings.model_fields_set:
            agents_url = settings.deploy_control_plane_url
        else:
            agents_url = f"{root}/v2/agents"
    return root, agents_url.strip().rstrip("/")


def _client_api_key(api_key: str | None) -> str:
    """Return the API key of an ``agents.Client``: ``api_key``, else ``MISTRAL_API_KEY``."""
    if api_key is not None and not isinstance(api_key, str):
        raise sdk_errors.SdkError(f"api_key must be a string or None, got {type(api_key).__name__}")
    if api_key is None:
        key = _header_api_key(ControlPlaneSettings().api_key, name="MISTRAL_API_KEY")
    else:
        key = _header_api_key(api_key, name="api_key")
    if not key:
        raise sdk_errors.SdkError(
            "The Agents control plane needs an API key: set MISTRAL_API_KEY or pass agents.Client(api_key=...)"
        )
    return key


def _control_plane_transport(
    deployment: RemoteAgentDeployment,
    *,
    http_transport: httpx.AsyncBaseTransport | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> VibeAgentsSessionTransport:
    """Return a transport to the control plane of ``deployment``, bound to no Session.

    It serves the catalog procedures. With ``http_client``, it borrows that connection pool.
    """
    return VibeAgentsSessionTransport(deployment, http_transport=http_transport, http_client=http_client)


async def _get_remote_session(
    deployment: RemoteAgentDeployment,
    session_id: str,
    *,
    client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
) -> harness_session.SessionClient:
    transport = _bind_remote_session(deployment, session_id)
    client = ClientToolSessionClient(transport, client_tools=client_tools)
    try:
        response = await transport.request(
            "app_server/session/read",
            harness_session.SessionReadParams(session_id=session_id),
            harness_session.SessionReadResponse,
        )
        await client.adopt_session_snapshot(response.state, response.last_event_id)
    except BaseException as setup_error:
        await _close_client_after_setup_failure(client, setup_error)
        raise
    return client


async def _close_client_after_setup_failure(
    client: harness_session.SessionClient,
    setup_error: BaseException,
) -> None:
    try:
        await client.close()
    except BaseException as cleanup_error:
        setup_error.add_note(f"Remote Session cleanup failed: {cleanup_error!r}")


class _LostStreamBudget:
    """Time limit for getting a dropped event or callbacks stream back.

    The limit starts at the first failed read. It ends when an event arrives, or when a reopened
    stream sends something and stays open for `_STREAM_STABLE_OPEN_SECONDS`: an open stream can
    stay quiet for minutes while the Session works, because the server sends only SSE heartbeat
    comments, which the client does not report as events. A stream that the server accepts and
    drops at once, or accepts and then leaves silent until the read timeout, does not end it. While
    the limit runs, each new attempt is bounded by what is left of it, so an attempt that hangs
    before the server accepts it cannot take the reader past it. An accepted stream is bounded by
    the read timeout instead, so the reader gives up at most one read timeout after the limit.

    It logs one warning when an outage starts and one info line when it ends, not one per attempt.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        session_id: UUID,
        *,
        stream: str = "event",
        budget_seconds: float | None = None,
    ) -> None:
        self._loop = loop
        self._budget_seconds = _STREAM_RECONNECT_BUDGET_SECONDS if budget_seconds is None else budget_seconds
        self._session_id = str(session_id)
        self._stream = stream
        self._lost_since: float | None = None
        self._failed_attempts = 0
        self._opened_at: float | None = None
        self._active = False
        self._delay = _STREAM_RECONNECT_INITIAL_SECONDS
        self._attempt: asyncio.Timeout | None = None
        self._last_error: httpx.HTTPError | None = None

    def start_attempt(self) -> asyncio.Timeout:
        """Return the time limit of the next connection attempt. It has no limit while no stream is lost."""
        self._opened_at = None
        self._active = False
        deadline = None if self._lost_since is None else self._lost_since + self._budget_seconds
        self._attempt = asyncio.timeout_at(deadline)
        return self._attempt

    def stream_opened(self) -> None:
        """Record that the server accepted a stream. An open stream is not bounded by the budget."""
        self._opened_at = self._loop.time()
        if self._attempt is not None:
            self._attempt.reschedule(None)

    def stream_active(self) -> None:
        """Record that the open stream sent a line, a heartbeat or an event."""
        self._active = True

    def stream_recovered(self) -> None:
        """Record that an event or an answer arrived: the stream is back."""
        self._restart()
        if self._attempt is not None:
            self._attempt.reschedule(None)

    def _restart(self) -> None:
        if self._lost_since is not None:
            logger.info(
                f"Remote Session {self._stream} stream recovered",
                session_id=self._session_id,
                reconnect_attempts=self._failed_attempts,
                down_seconds=round(self._loop.time() - self._lost_since, 1),
            )
        self._lost_since = None
        self._failed_attempts = 0
        self._delay = _STREAM_RECONNECT_INITIAL_SECONDS
        self._last_error = None

    def record_failure(self, error: httpx.HTTPError) -> float:
        """Record a failed read and return the seconds left in the budget."""
        now = self._loop.time()
        if self._active and self._opened_at is not None and now - self._opened_at >= _STREAM_STABLE_OPEN_SECONDS:
            # The stream that just dropped was a working one: this is a new outage.
            self._restart()
        if self._lost_since is None:
            self._lost_since = now
            logger.warning(
                f"Remote Session {self._stream} stream dropped, reconnecting",
                session_id=self._session_id,
                error=type(error).__name__,
                status_code=error.response.status_code if isinstance(error, httpx.HTTPStatusError) else None,
            )
        self._failed_attempts += 1
        self._last_error = error
        return self._lost_since + self._budget_seconds - now

    async def wait_before_retry(self, remaining: float) -> None:
        await asyncio.sleep(min(self._delay, remaining))
        self._delay = min(self._delay * 2, _STREAM_RECONNECT_MAX_SECONDS)

    def lost_error(self, *, after_event_id: str | None) -> RemoteStreamLostError:
        elapsed = 0.0 if self._lost_since is None else self._loop.time() - self._lost_since
        error = self._last_error
        last_error = "none" if error is None else f"{type(error).__name__}: {error}"
        return RemoteStreamLostError(
            session_id=self._session_id,
            after_event_id=after_event_id,
            reason=f"reconnecting failed for {elapsed:.0f} seconds, last error: {last_error}",
        )


def _build_info_response() -> harness_session.InfoResponse:
    return harness_session.InfoResponse(
        server_info=harness_session.ServerInfo(
            name="vibe_agents",
            version="session-v1-transport",
        ),
        capabilities={
            "app_server/session": harness_session.app_server_capability(_REMOTE_PROCEDURES),
            "app_server/subagents": harness_session.app_server_capability(("app_server/subagents/list",)),
            "app_server/catalog": harness_session.app_server_capability(
                ("app_server/catalog/list", "app_server/catalog/rename", "app_server/catalog/archive")
            ),
        },
    )


def _refuse_context_messages(method: str, context_messages: Sequence[harness_session.ContextMessage]) -> None:
    if context_messages:
        raise RemoteSessionProcedureUnsupportedError(
            method=method,
            backend="vibe_agents",
            reason="no control-plane route takes this procedure, and /commands cannot carry context messages",
        )


# FIXME: delete once MAIS 2026.11 is released
def _build_message_input(content: Sequence[harness_session.ContentBlock]) -> wire.MessageInput:
    try:
        return wire.MessageInput.from_content(content)
    except TypeError as error:
        raise RemoteSessionProcedureUnsupportedError(
            method="app_server/session/turn/start",
            backend="vibe_agents",
            reason=str(error),
        ) from error


def _subagent_session(child: AgentSessionResponse) -> harness_session.SubagentSession:
    if child.agent_path is None:
        raise RemoteSessionProcedureUnsupportedError(
            method="app_server/subagents/list",
            backend="vibe_agents",
            reason="the Vibe Agents server does not report child agent paths",
        )
    return harness_session.SubagentSession(
        session=build_session_from_product(child),
        name=child.agent_path.rsplit("/", 1)[-1],
        config_name=child.config_name,
        agent_path=child.agent_path,
    )


def _response_detail(error: httpx.HTTPStatusError) -> object:
    try:
        body = error.response.json()
    except ValueError:
        return None
    if not isinstance(body, dict):
        return None
    return body.get("detail")


type _RetryKind = Literal["busy", "unknown"]


def _session_busy(error: httpx.HTTPStatusError) -> sdk_errors.SessionBusyError:
    busy = sdk_errors.SessionBusyError(_detail_message(error, "The Session is busy"))
    busy.retry_after = sdk_errors.retry_after_seconds(error.response)
    return busy


async def _retry_within_budget[ResultT](
    attempt: Callable[[], Awaitable[ResultT]],
    *,
    classify: Callable[[httpx.HTTPStatusError], _RetryKind | None],
    outcome_unknown: Callable[[], Exception],
    retry_lost_attempts: bool = True,
    busy_wait_seconds: float = 0.0,
    deadline: float | None = None,
) -> ResultT:
    """Run one idempotent command, retrying until it answers or the outcome budget is spent.

    Every attempt must carry the same idempotency key, so the Session replays a command it already
    took instead of applying it twice. ``classify`` names an HTTP error ``"busy"`` (the Session
    applied nothing), ``"unknown"`` (it may have applied the command) or None (raise it), and may
    raise a typed refusal itself. ``make_request`` does not retry a POST, so this loop owns every
    retry. A ``Retry-After`` delays the next attempt. With ``retry_lost_attempts``, a lost
    connection is an unknown outcome and the budget bounds each attempt too; without it, both
    reach the caller as they are, and an attempt is never cut short.

    The call raises ``SessionBusyError`` only while every attempt was busy, which committed nothing, and
    ``outcome_unknown`` otherwise. It gives up early on busy when what is left of the budget is
    shorter than ``busy_wait_seconds``, the time the server may wait before it answers busy.
    ``deadline`` (event loop time) ends the budget early when the caller shares it with later steps.
    """

    loop = asyncio.get_running_loop()
    if deadline is None:
        deadline = loop.time() + _OUTCOME_TIMEOUT_SECONDS
    delay = _RETRY_INITIAL_SECONDS
    unknown_error: Exception | None = None
    busy_cause: httpx.HTTPStatusError | None = None
    while True:
        server_delay = 0.0
        try:
            if not retry_lost_attempts:
                return await attempt()
            async with asyncio.timeout_at(deadline):
                return await attempt()
        except httpx.HTTPStatusError as error:
            kind = classify(error)
            if kind is None:
                raise
            server_delay = sdk_errors.retry_after_seconds(error.response) or 0.0
            if kind == "busy":
                busy_cause = error
            else:
                unknown_error = error
        except (httpx.TransportError, TimeoutError) as error:
            if not retry_lost_attempts:
                raise
            unknown_error = error
        remaining = deadline - loop.time()
        pause = min(max(delay, server_delay), remaining)
        # After an unknown outcome, that attempt may still commit, so the loop keeps the full
        # budget and reports the outcome unknown.
        if busy_cause is not None and unknown_error is None and remaining - pause <= busy_wait_seconds:
            raise _session_busy(busy_cause) from busy_cause
        # An attempt that starts at the deadline cannot answer.
        if remaining - pause <= 0:
            raise outcome_unknown() from unknown_error
        await asyncio.sleep(pause)
        delay = min(delay * 2, _RETRY_MAX_SECONDS)


async def _retry_throttled_start[ResultT](attempt: Callable[[], Awaitable[ResultT]], *, deadline: float) -> ResultT:
    """Resend a Session start the control plane throttled, once its ``Retry-After`` has passed.

    A 429 applied nothing, so the same start is resent. A 429 with no ``Retry-After``, or one that
    ends after ``deadline`` (event loop time), such as a spent daily quota, is raised at once.
    """

    loop = asyncio.get_running_loop()
    while True:
        try:
            return await attempt()
        except httpx.HTTPStatusError as error:
            delay = sdk_errors.retry_after_seconds(error.response)
            if error.response.status_code != httpx.codes.TOO_MANY_REQUESTS or delay is None:
                raise
            if loop.time() + delay > deadline:
                raise
            logger.info("Session start throttled (429), retrying", retry_after_seconds=delay)
        await asyncio.sleep(delay)


# FIXME: delete once MAIS 2026.11 is released
async def _retry_busy_within_budget[ResultT](
    attempt: Callable[[], Awaitable[ResultT]], *, command_id: UUID, deadline: float
) -> ResultT:
    """Retry a compare-and-set command only while the Session answers a busy 429.

    Any other answer, including an unknown outcome, reaches the caller as before. Once the budget
    is spent ``SessionBusyError`` is raised, since nothing was applied.
    """

    return await _retry_within_budget(
        attempt,
        classify=lambda error: "busy" if _is_retryable_busy(error) else None,
        # Unreachable: only busy answers are retried, and they raise ``SessionBusyError``.
        outcome_unknown=lambda: _unconfirmed(f"command {command_id}", idempotency_key=str(command_id)),
        retry_lost_attempts=False,
        deadline=deadline,
    )


def _submit_retry_kind(error: httpx.HTTPStatusError) -> _RetryKind | None:
    """Classify a refused message submit: busy applied nothing, unknown may have applied it."""

    if _is_retryable_busy(error):
        return "busy"
    return "unknown" if _send_message_outcome_unknown(error) else None


def _refusing(
    refusal: Callable[[httpx.HTTPStatusError], Exception | None],
) -> Callable[[httpx.HTTPStatusError], _RetryKind | None]:
    """Classify a submit like ``_submit_retry_kind``, raising the typed refusal ``refusal`` finds otherwise."""

    def classify(error: httpx.HTTPStatusError) -> _RetryKind | None:
        kind = _submit_retry_kind(error)
        # Busy first: `send_message`'s refusal types every 429, and only a busy one clears by waiting.
        if kind == "busy":
            return kind
        typed = refusal(error)
        if typed is not None:
            raise typed from error
        return kind

    return classify


def _turn_conflict(error: httpx.HTTPStatusError) -> RemoteSessionTurnConflictError | None:
    """Type the 409 of a steer or interrupt route: the expected Turn is not the active Turn."""

    if error.response.status_code != httpx.codes.CONFLICT:
        return None
    return RemoteSessionTurnConflictError(_detail_message(error, "The expected Turn is not the active Turn"))


def _turn_steer_refusal(error: httpx.HTTPStatusError, *, idempotency_key: str) -> Exception | None:
    # A steer carries a key, so a 409 for a key reused with another message is not a stale Turn.
    if _is_idempotency_conflict(error):
        return harness_session.SessionIdempotencyConflictError(idempotency_key=idempotency_key)
    conflict = _turn_conflict(error)
    if conflict is not None:
        return conflict
    return _message_rejection(error)


def _unconfirmed(what: str, *, idempotency_key: str | None = None) -> OutcomeUnknownError:
    return OutcomeUnknownError(
        f"Vibe Agents did not confirm {what} within {_OUTCOME_TIMEOUT_SECONDS:g} seconds",
        idempotency_key=idempotency_key,
    )


type _RouteCursorResponse = (
    harness_session.TurnStartResponse
    | harness_session.TurnSteerResponse
    | harness_session.TurnInterruptResponse
    | harness_session.CallbackResultResponse
)


def _with_route_cursor[ResponseT: _RouteCursorResponse](response: ResponseT, session_id: UUID) -> ResponseT:
    """Wrap the controller ``/events`` cursor a route returns as this transport's event id."""

    return response.model_copy(update={"last_event_id": _encode_event_id(session_id, response.last_event_id)})


def _is_retryable_busy(error: httpx.HTTPStatusError) -> bool:
    """Whether a 429 applied nothing and should clear shortly: a busy code, or no code at all.

    The quota 429 is only on a Session start, which ``_retry_throttled_start`` retries by its
    ``Retry-After`` alone.
    """

    if error.response.status_code != httpx.codes.TOO_MANY_REQUESTS:
        return False
    detail = _response_detail(error)
    return not isinstance(detail, dict) or detail.get("code") in _RETRYABLE_BUSY_CODES


def _detail_message(error: httpx.HTTPStatusError, default: str) -> str:
    """The human message of an error's ``detail``, which is a string or a coded object."""

    detail = _response_detail(error)
    if isinstance(detail, dict):
        detail = detail.get("message")
    return str(detail) if detail else default


def _send_message_outcome_unknown(error: httpx.HTTPStatusError) -> bool:
    status_code = error.response.status_code
    if status_code in _SEND_MESSAGE_UNKNOWN_OUTCOME_STATUSES:
        return True
    # A gateway answers 502 when the control plane died mid-request, which may hide a commit. The
    # control plane's own 502 carries a `detail` and repeats for the same request.
    return status_code == httpx.codes.BAD_GATEWAY and _response_detail(error) is None


def _refusal_detail(error: httpx.HTTPStatusError) -> str | None:
    """The ``detail`` of the control plane's own 422 refusal of a command's content, or None.

    That refusal's ``detail`` is a string. Request validation answers a list, which is a caller bug.
    """

    detail = _response_detail(error)
    if error.response.status_code != httpx.codes.UNPROCESSABLE_ENTITY or not isinstance(detail, str):
        return None
    return detail


def _message_rejection(error: httpx.HTTPStatusError) -> harness_session.SessionMessageRejectedError | None:
    """Type the control plane's own refusal of a rejected or too large message, or return None."""

    detail = _refusal_detail(error)
    if detail is None:
        return None
    return harness_session.SessionMessageRejectedError(detail or "The Session rejected the message")


def _send_message_refusal(error: httpx.HTTPStatusError, *, idempotency_key: str) -> Exception | None:
    """Return the typed Session error for a ``send_message`` refusal, or None for any other status.

    A 409 is typed only when it carries a ``detail.code`` this SDK knows; any other 409 stays
    an HTTP error rather than reading as a refusal of this message.
    """

    detail = _response_detail(error)
    status_code = error.response.status_code
    if status_code == httpx.codes.TOO_MANY_REQUESTS:
        # Applied nothing, but the code says waiting does not clear it.
        return _session_busy(error)
    if status_code == httpx.codes.GONE:
        return harness_session.SessionTerminatedError(str(detail or "The Session accepts no commands"))
    if (rejection := _message_rejection(error)) is not None:
        return rejection
    if status_code == httpx.codes.NOT_IMPLEMENTED:
        return RemoteSessionProcedureUnsupportedError(
            method="app_server/session/message/send",
            backend="vibe_agents",
            reason=str(detail or "the Session cannot serve send_message"),
        )
    # The framework's bare 404 for an unknown route; a missing Session names itself in the detail.
    if status_code == httpx.codes.NOT_FOUND and detail == "Not Found":
        return RemoteSessionProcedureUnsupportedError(
            method="app_server/session/message/send",
            backend="vibe_agents",
            reason="the control plane predates send_message; upgrade it",
        )
    if _is_idempotency_conflict(error):
        return harness_session.SessionIdempotencyConflictError(idempotency_key=idempotency_key)
    return None


def _turn_start_refusal(error: httpx.HTTPStatusError, *, idempotency_key: str) -> Exception | None:
    """Return the typed Session error for a Turn start the control plane refused, or None.

    The route and ``/commands`` refuse a start the same way. A 429 that waiting does not clear (a
    child limit) is busy, as for ``send_message``, and a 409 ``idempotency_conflict`` is a key
    reused for another message. A 409 ``turn_active`` is a start the Session refused because a
    Turn runs. When it names no running Turn, the Session refused this key earlier, while a Turn
    ran, and kept that refusal: the same key cannot start a Turn, so it is not reported as busy.
    A 422 string is a message the Session never takes.
    """

    if error.response.status_code == httpx.codes.TOO_MANY_REQUESTS and not _is_retryable_busy(error):
        return _session_busy(error)
    if _is_idempotency_conflict(error):
        return harness_session.SessionIdempotencyConflictError(idempotency_key=idempotency_key)
    detail = _response_detail(error)
    if (
        error.response.status_code == httpx.codes.CONFLICT
        and isinstance(detail, dict)
        and detail.get("code") == wire.SessionCommandVerdictReason.TURN_ACTIVE
    ):
        active_turn_id = detail.get("active_turn_id")
        if not active_turn_id:
            return harness_session.SessionMessageRejectedError(
                f"The Session refused the start with idempotency key {idempotency_key!r} while a Turn ran, "
                "and still refuses that key with no Turn running; start the Turn again with a new key"
            )
        return _RemoteSessionTurnActiveError(
            _detail_message(error, "A Turn is already running"), active_turn_id=str(active_turn_id)
        )
    return _message_rejection(error)


def _route_missing(error: httpx.HTTPStatusError) -> bool:
    """Whether the error says this control plane has no route for the request.

    The framework answers a bare 404 for an unknown path, and a 405 for a path that only matches a
    route of another method: without the stream route, `GET .../callbacks/stream` matches
    `POST .../callbacks/{callback_id}`. A missing or foreign Session names itself in a 404 detail.
    """

    status_code = error.response.status_code
    if status_code == httpx.codes.METHOD_NOT_ALLOWED:
        return True
    return status_code == httpx.codes.NOT_FOUND and _response_detail(error) == "Not Found"


def _tree_unsupported() -> harness_session.UnsupportedSessionProcedureError:
    return RemoteSessionProcedureUnsupportedError(
        method="app_server/session/callbacks/tree",
        backend="vibe_agents",
        reason="the control plane predates the callbacks tree; upgrade it",
    )


def _callback_refusal(
    error: httpx.HTTPStatusError, *, callback_id: UUID
) -> harness_session.SessionCallbackSettledError | harness_session.SessionCallbackRejectedError | None:
    """Return the in-process host's error for an answer the control plane refused, or None.

    The control plane answers 404 when the callback is no longer open (its turn ended, or its
    Session takes no more commands) and 410 when the Session is gone: the callback is settled. It
    answers a 422 string for an answer the Session refused (it does not fit the callback, or is
    too large): the callback stays open. Either way the answer changed nothing. The framework's
    bare 404 for an unknown route stays an HTTP error.
    """

    status_code = error.response.status_code
    if status_code == httpx.codes.GONE or (status_code == httpx.codes.NOT_FOUND and not _route_missing(error)):
        return harness_session.SessionCallbackSettledError(
            f"Callback {callback_id} is no longer open: {_detail_message(error, 'its Session ended')}"
        )
    detail = _refusal_detail(error)
    if detail is None:
        return None
    return harness_session.SessionCallbackRejectedError(
        f"The Session refused the answer to callback {callback_id}: {detail or 'it does not fit the callback'}"
    )


def _is_idempotency_conflict(error: httpx.HTTPStatusError) -> bool:
    """Whether the control plane refused a reused idempotency key; any other 409 stays an HTTP error."""

    if error.response.status_code != httpx.codes.CONFLICT:
        return False
    detail = _response_detail(error)
    return isinstance(detail, dict) and detail.get("code") == "idempotency_conflict"


def _command_refusal(error: httpx.HTTPStatusError, *, method: str) -> Exception | None:
    """Return the typed error for a command the control plane refused outright, or None.

    A 403 coded ``child_session_command_refused`` is a client command on a subagent's Session,
    which only its parent agent may drive: the same error the in-process host raises. A 410 is a
    Session that accepts no more commands.
    """

    status_code = error.response.status_code
    detail = _response_detail(error)
    if (
        status_code == httpx.codes.FORBIDDEN
        and isinstance(detail, dict)
        and detail.get("code") == harness_session.CHILD_SESSION_COMMAND_REFUSED
    ):
        return harness_session.ChildSessionProcedureRefusedError(method=method, backend="vibe_agents")
    if status_code == httpx.codes.GONE and method in _COMMAND_PROCEDURES:
        return harness_session.SessionTerminatedError(_detail_message(error, "The Session accepts no commands"))
    return None


def _remote_unsupported_reason(method: str) -> str:
    if method == "app_server/session/start":
        return "remote creation is deployment-bound; use Agent.start_session()"
    return "the Vibe Agents adapter does not implement this App Server procedure"


def _decode_base64url(value: str) -> str:
    return base64.b64decode(
        value + "=" * (-len(value) % 4),
        altchars=b"-_",
        validate=True,
    ).decode()


def _decode_event_id(
    event_id: str | None, session_id: UUID, *, passed: str | None = None
) -> tuple[str | None, int | None]:
    """The product cursor and the sub-index ``event_id`` names, ``None`` for the session's start.

    An id without a session id, as the transport gave before, is taken as ``session_id``'s.
    ``passed`` is the id as the caller gave it, which the error shows, if it differs.

    Raises:
        InvalidCursorError: The id is not one this transport gives, or is of another session.
    """
    if event_id is None or event_id == _EMPTY_CURSOR:
        return None, None
    if not event_id.startswith(_CURSOR_PREFIX):
        raise _invalid_event_cursor(passed or event_id, session_id)
    owner, position = _split_session(event_id, _CURSOR_PREFIX)
    if owner is not None and owner != str(session_id):
        # Its position can be one of this session's too: read by it, the cursor would skip or
        # repeat events.
        raise _invalid_event_cursor(passed or event_id, session_id, owner=owner)
    if position == _EMPTY_POSITION:
        return None, None
    encoded, separator, subevent_index = position.partition(".")
    try:
        if separator and not subevent_index.isdigit():
            raise ValueError("Event sub-index is invalid")
        product_cursor = _decode_base64url(encoded)
        if not product_cursor:
            raise ValueError("Event cursor decoded to an empty product cursor")
        return product_cursor, int(subevent_index) if separator else None
    except (ValueError, UnicodeDecodeError) as error:
        raise _invalid_event_cursor(passed or event_id, session_id) from error


def _new_projection(product: AgentSessionResponse, refused_turn_ids: Set[str]) -> VibeAgentsSessionV1Projection:
    """Start a projection of the Session's events, refusing a Session in the legacy task protocol.

    Checked on the product row rather than remembered from the create call, so a transport
    that attached to a session it did not open refuses it the same way.
    """

    _require_session_v1(product)
    return VibeAgentsSessionV1Projection(product, refused_turn_ids=refused_turn_ids)


def _require_session_v1(product: AgentSessionResponse) -> None:
    if product.session_protocol is not SessionProtocol.SESSION_V1:
        raise LegacySessionError(str(product.agent_session_id))


def _reconciled_turn_events(
    projection: VibeAgentsSessionV1Projection,
    terminated_turns: Sequence[harness_session.TurnTerminatedEvent],
    *,
    session_id: UUID,
    after_index: int | None,
) -> list[harness_session.Event]:
    """Relay the Turn terminations the product row produced after the last frame.

    No frame carries them, so each gets an id of its own after the projection's cursor. A
    reader that resumes from one rebuilds the same terminations and is sent only the ones after
    it; `after_index` is that position.
    """

    cursor = projection.product_cursor
    if cursor is None:
        # No frame was relayed, so there is no Turn the reader could be following.
        return []
    return [
        harness_session.Event(
            event_id=_encode_reconciled_event_id(session_id, cursor, index),
            emitted_at=projection.session.updated_at,
            session_id=str(session_id),
            root_session_id=projection.session.root_session_id,
            payload=payload,
        )
        for index, payload in enumerate(terminated_turns)
        if after_index is None or index > after_index
    ]


def _encode_reconciled_event_id(session_id: UUID, product_cursor: str, index: int) -> str:
    return f"{_encode_event_id(session_id, product_cursor)}{_RECONCILED_TURN_MARKER}{index}"


def _split_reconciled_event_id(event_id: str | None, session_id: UUID) -> tuple[str | None, int | None]:
    """Separate a reconciled Turn termination's position from the cursor it follows."""

    if event_id is None or _RECONCILED_TURN_MARKER not in event_id:
        return event_id, None
    cursor_event_id, _marker, index = event_id.rpartition(_RECONCILED_TURN_MARKER)
    if not index.isdigit():
        raise _invalid_event_cursor(event_id, session_id)
    return cursor_event_id, int(index)


def _relayed_event(
    *, event_id: str, emitted_at: int, session_id: str, root_session_id: str | None, payload: RelayedPayload
) -> harness_session.Event:
    """The event that carries ``payload``: a client event for one this SDK has no model for."""

    event_type = (
        harness_session.ClientEvent
        if isinstance(payload, harness_session.UnknownEventPayload)
        else harness_session.Event
    )
    return event_type(
        event_id=event_id,
        emitted_at=emitted_at,
        session_id=session_id,
        root_session_id=root_session_id,
        payload=payload,
    )


def _relayed_emitted_at(projection: VibeAgentsSessionV1Projection) -> int:
    """When to say a relayed event happened: the frame's own `emittedAt`, else the session snapshot's time."""

    if projection.last_emitted_at is not None:
        return projection.last_emitted_at
    return projection.session.updated_at


# FIXME: delete once MAIS 2026.11 is released
def _v1_started_turn(projection: VibeAgentsSessionV1Projection, command_id: str) -> harness_session.TurnState | None:
    """The Turn a Session v1 start opened, or None while it has not appeared.

    The Turn a start opens carries the command's own id: the worker names it after the command
    id, and this transport always sends one. So the lookup also answers a retry whose Turn has
    already finished. A Turn with another id is never this start's: the Session refuses a start
    while a Turn runs, it does not add the message to that Turn.
    """

    return projection.turns.get(command_id)


def _left_starting(projection: VibeAgentsSessionV1Projection) -> bool:
    """Whether a Session has been up at least once: idle now, or it has started a turn."""

    return _started_idle(projection) or bool(projection.turns)


async def _create_with_initial_turn(
    create: Callable[[harness_session.InitialTurn | None], Awaitable[StartAgentSessionResponse]],
    initial_turn: harness_session.InitialTurn | None,
) -> StartAgentSessionResponse:
    """Create the product Session, and type the control plane's refusal of the initial Turn."""

    if initial_turn is None:
        return await create(None)
    try:
        return await create(initial_turn)
    except httpx.HTTPStatusError as error:
        # A string-detail 422 refuses the message, or a start input too large to send. The second is rare:
        # the control plane caps the message well below that limit.
        if (rejection := _message_rejection(error)) is not None:
            raise rejection from error
        if not _refuses_initial_turn_field(error):
            raise
    # FIXME: delete once MAIS 2026.11 is released
    # A control plane that predates initial_turn refuses it before it creates anything.
    return await create(None)


# FIXME: delete once MAIS 2026.11 is released
def _refuses_initial_turn_field(error: httpx.HTTPStatusError) -> bool:
    if error.response.status_code != httpx.codes.UNPROCESSABLE_ENTITY:
        return False
    detail = _response_detail(error)
    if not isinstance(detail, list):
        return False
    return any(
        isinstance(item, dict) and item.get("type") == "extra_forbidden" and item.get("loc") == ["body", "initial_turn"]
        for item in detail
    )


def _started_idle(projection: VibeAgentsSessionV1Projection) -> bool:
    """Whether a freshly created Session has reported itself up and waiting.

    Session v1 has no initialized entry kind, so its retained waiting status is the whole signal.
    """

    return projection.session.status == "waiting"


def _last_event_id(projection: VibeAgentsSessionV1Projection) -> str:
    # The session the transport read, not the id its stream reports: a cursor is of that session.
    session_id = projection.product_session.agent_session_id
    if projection.product_cursor is None:
        return _empty_cursor(session_id)
    return _encode_event_id(session_id, projection.product_cursor)


def _encode_page_cursor(
    direction: harness_session.SortDirection,
    after_item_id: str | None,
) -> str:
    direction_marker = "f" if direction == "forward" else "b"
    payload = f"{direction_marker}:start" if after_item_id is None else f"{direction_marker}:after:{after_item_id}"
    return f"{_PAGE_CURSOR_PREFIX}{_encode_base64url(payload)}"


def _decode_page_cursor(
    cursor: str | None,
    direction: harness_session.SortDirection,
) -> str | None:
    if cursor is None:
        return None
    if not cursor.startswith(_PAGE_CURSOR_PREFIX):
        raise RemoteSessionConflictError(f"Invalid page cursor: {cursor!r}")
    encoded = cursor.removeprefix(_PAGE_CURSOR_PREFIX)
    try:
        payload = _decode_base64url(encoded)
    except (ValueError, UnicodeDecodeError) as error:
        raise RemoteSessionConflictError(f"Invalid page cursor: {cursor!r}") from error
    parts = payload.split(":", maxsplit=2)
    expected_marker = "f" if direction == "forward" else "b"
    if parts == [expected_marker, "start"]:
        return None
    if len(parts) == 3 and parts[0] == expected_marker and parts[1] == "after" and parts[2]:
        return parts[2]
    raise RemoteSessionConflictError(f"Invalid page cursor: {cursor!r}")


def _build_page[ItemT](
    items: list[ItemT],
    request: harness_session.PageRequest,
    *,
    item_id: Callable[[ItemT], str],
) -> harness_session.Page[ItemT]:
    """Page append-only items relative to stable ids instead of mutable offsets."""

    ordered = items if request.direction == "forward" else list(reversed(items))
    after_item_id = _decode_page_cursor(request.cursor, request.direction)
    start = 0
    if after_item_id is not None:
        try:
            start = next(index for index, item in enumerate(ordered) if item_id(item) == after_item_id) + 1
        except StopIteration as error:
            raise RemoteSessionConflictError(f"Stale page cursor: {request.cursor!r}") from error

    selected = ordered[start : start + request.limit]
    next_index = start + len(selected)
    next_cursor = None
    if selected and next_index < len(ordered):
        next_cursor = _encode_page_cursor(request.direction, item_id(selected[-1]))

    previous_cursor = None
    if start > 0:
        previous_start = max(0, start - request.limit)
        previous_item_id = item_id(ordered[previous_start - 1]) if previous_start > 0 else None
        previous_cursor = _encode_page_cursor(request.direction, previous_item_id)

    return harness_session.Page(
        items=selected,
        next_cursor=next_cursor,
        previous_cursor=previous_cursor,
    )


RemoteSessionProcedureUnsupportedError = sdk_errors.UnsupportedSessionProcedureError

if TYPE_CHECKING:
    RemoteSessionOutcomeUnknownError = OutcomeUnknownError
    RemoteSessionStartupTimeoutError = SessionStartupTimeoutError
    RemoteSessionStreamLostError = RemoteStreamLostError

# The 1.1.0rc12 error names this module exported, still readable with a `DeprecationWarning`.
_RENAMED = frozenset(
    {"RemoteSessionOutcomeUnknownError", "RemoteSessionStartupTimeoutError", "RemoteSessionStreamLostError"}
)


def __getattr__(name: str) -> object:
    if name in _RENAMED:
        warnings.warn(sdk_errors._renamed_warning(name), DeprecationWarning, stacklevel=2)
        return sdk_errors._renamed_class(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "RemoteAgentDeployment",
    "RemoteAgentDeploymentNotFoundError",
    "RemoteSessionConflictError",
    "RemoteSessionProcedureUnsupportedError",
    "RemoteSessionStartFailedError",
    "RemoteSessionTurnConflictError",
    "VibeAgentsSessionTransport",
]
