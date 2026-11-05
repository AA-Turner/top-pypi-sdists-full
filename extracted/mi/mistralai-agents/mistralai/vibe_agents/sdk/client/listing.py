"""Listing: the sessions of a host, newest first.

``list_sessions()`` lists the sessions of the control plane, ``list_sessions(host="local")`` the
sessions of this event loop's local runtime. ``local_runtime()`` returns that runtime; its calls
work on local sessions only, and its ``async with`` block stops every local session at exit.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from datetime import UTC, datetime
from types import TracebackType
from typing import TYPE_CHECKING, Literal, Self, get_args
from uuid import UUID

import httpx

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session.local_record import LocalSessionProcedureError
from mistralai.vibe.harness.runtime.agents.control_plane import SessionControlPlaneError
from mistralai.vibe_agents.sdk.authoring import errors as sdk_errors
from mistralai.vibe_agents.sdk.authoring.experimental import warn_experimental
from mistralai.vibe_agents.sdk.client.records import (
    CancelledTermination,
    CompletedTermination,
    FailedTermination,
    SessionInfo,
    Termination,
    UnknownTermination,
)
from mistralai.vibe_agents.sdk.client.turn_reads import protocol_error
from mistralai.vibe_agents.sdk.client.unknown_values import read_value
from mistralai.vibe_agents.sdk.transport import local
from mistralai.vibe_agents.sdk.transport import remote as remote_transport
from mistralai.vibe_agents.sdk.transport.session_journal import JsonFileSessionJournal

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.client.api_client import Client

__all__ = ["LocalRuntime", "SessionScope", "SessionStatus", "list_sessions", "local_runtime"]

# The ``status=`` filter takes these; ``SessionInfo.status`` can also be an UnknownValue.
type SessionStatus = Literal["running", "waiting", "terminated"]
type SessionScope = Literal["roots", "children", "tree"]
type Host = Literal["deployed", "local"]

_STATUSES: frozenset[str] = frozenset(get_args(SessionStatus.__value__))
_SCOPES: frozenset[str] = frozenset(get_args(SessionScope.__value__))
_HOSTS: frozenset[str] = frozenset(get_args(Host.__value__))
# The control plane's largest page; the local runtime takes any size.
_PAGE_SIZE = 200

_ListPage = Callable[[harness_session.CatalogListParams], Awaitable[harness_session.CatalogListResponse]]


class LocalRuntime:
    """The local runtime of the running event loop: the one that ``agent.run`` and
    ``agent.start_session`` use for local agents.

    Getting it starts nothing. Each call reaches the runtime of the event loop it runs in, so it
    must run inside one. Two ``asyncio.run`` calls have two runtimes, which share no session.

    ``async with agents.local_runtime() as runtime:`` starts the runtime if it has not started, and
    its exit stops every session of that runtime: running turns, subagents and sandboxes. The
    sessions of an ``async with agent.local_runtime()`` block run in a runtime of their own and
    are not stopped.
    The exit frees the stopped sessions: a read or command on one then raises
    ``SessionTerminatedError``. With ``journal_factory``, a new block with the same journals
    continues them. The next local call starts a new runtime. In a nested block, only the outermost
    exit stops them.

    While the block is open, no session is closed for being idle: a session that no client holds,
    such as the session of an ``agent.run`` that returned, keeps its sandbox and can be driven
    again until the block exits or ``session.cancel()``. Outside a block, such a session ends once
    it is idle, and frees its sandbox.
    """

    __slots__ = ("_journals", "_program_policy")

    def __init__(
        self,
        *,
        program_timeout_seconds: float | None = None,
        journal_factory: Callable[[str], JsonFileSessionJournal] | None = None,
    ) -> None:
        self._program_policy = (
            local._program_policy(program_timeout_seconds) if program_timeout_seconds is not None else None
        )
        if journal_factory is not None:
            warn_experimental("journal_factory=", stacklevel=2)
        self._journals = journal_factory

    @property
    def program_timeout_seconds(self) -> float:
        """The time budget, in seconds, of each program that the model runs with ``run_typescript``
        in a local session of this event loop.

        It is the budget of the loop's runtime, or 60 seconds while it has not started, as the next
        local session would get. The ``program_timeout_seconds`` given to ``agents.local_runtime`` applies
        when the ``async with`` block is entered.
        """
        runtime = local._running_process_runtime()
        policy = runtime.program_policy if runtime is not None else local._program_policy(None)
        return policy.elapsed_budget_ms / 1000

    def list_sessions(
        self,
        *,
        scope: SessionScope = "roots",
        root: str | None = None,
        parent: str | None = None,
        status: SessionStatus | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[SessionInfo]:
        """Iterate over the sessions of this runtime, newest first.

        The arguments are those of ``agents.list_sessions``. An ended session is listed as
        ``"terminated"`` until the event loop stops. Listing starts nothing: before the runtime
        starts, it lists no session. The sessions of an ``async with agent.local_runtime()`` block
        run in a runtime of their own and are not listed.
        """
        params = _catalog_params(scope, root, parent, status, limit)
        return _iterate(self._page, params, status, limit)

    async def _page(self, params: harness_session.CatalogListParams) -> harness_session.CatalogListResponse:
        asyncio.get_running_loop()
        scope_session_id = _scope_session_id(params.scope)
        runtime = local._running_process_runtime()
        if runtime is None:
            if scope_session_id is not None:
                raise _not_in_local_runtime(scope_session_id)
            return harness_session.CatalogListResponse(items=[], next_cursor=None)
        manager = runtime.manager
        try:
            return manager.list_catalog(params)
        except SessionControlPlaneError as error:
            if error.code == "session_not_found" and scope_session_id is not None:
                raise _not_in_local_runtime(scope_session_id) from error
            raise
        except LocalSessionProcedureError as error:
            if not isinstance(params.scope, harness_session.TreeScope):
                raise
            # Not found as a tree root, as on the deployed host, which cannot tell a subagent apart.
            root = params.scope.root_session_id
            raise sdk_errors.local_session_not_found(
                root,
                f"it is a subagent, not a tree root; pass root={manager.record(root).root_session_id!r}, the root "
                "of its tree",
            ) from error

    async def __aenter__(self) -> Self:
        local._enter_process_runtime(program_policy=self._program_policy, journals=self._journals)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await local._exit_process_runtime()

    def __repr__(self) -> str:
        arguments = []
        if self._program_policy is not None:
            arguments.append(f"program_timeout_seconds={self._program_policy.elapsed_budget_ms / 1000:g}")
        if self._journals is not None:
            arguments.append(f"journal_factory={self._journals!r}")
        return f"LocalRuntime({', '.join(arguments)})"


def local_runtime(
    *,
    program_timeout_seconds: float | None = None,
    journal_factory: Callable[[str], JsonFileSessionJournal] | None = None,
) -> LocalRuntime:
    """Return the local runtime of the running event loop, for the calls on local sessions only.

    ``program_timeout_seconds`` sets the time budget of each program, the code the model runs with
    ``run_typescript``, in every local session of the event loop. It defaults to 60 seconds and
    must be greater than 0 and at most 4 hours (14400 seconds). It applies when the ``async
    with`` block is entered, and the budget is fixed when the loop's runtime starts, so enter the
    block before the first local session: ``async with
    agents.local_runtime(program_timeout_seconds=600):``. Entering the block while the runtime
    runs with another budget raises ``SdkError``; listing reads no budget.

    ``journal_factory`` is experimental: a minor release may change it, and passing it warns
    ``ExperimentalWarning`` once per process. It saves each root session that
    ``agent.start_session()`` starts in the block, so that a later process continues it with
    ``agent.session(session_id)``. An ``agent.run()`` in the block saves its session too, ended
    with the run. Use it as ``async with
    agents.local_runtime(journal_factory=experimental.JsonFileSessionJournal.in_directory("./sessions")):``,
    with ``from mistralai.agents import experimental``. It is fixed when the loop's runtime starts,
    as the budget is: entering the block while the runtime runs with another one raises
    ``SdkError``. Without it, sessions end with the process.
    """
    if journal_factory is not None:
        # Here as well, so the warning points at the caller's line; the constructor's is then silent.
        warn_experimental("journal_factory=", stacklevel=2)
    return LocalRuntime(program_timeout_seconds=program_timeout_seconds, journal_factory=journal_factory)


def list_sessions(
    *,
    host: Host = "deployed",
    scope: SessionScope = "roots",
    root: str | None = None,
    parent: str | None = None,
    status: SessionStatus | None = None,
    limit: int | None = None,
    client: Client | None = None,
) -> AsyncIterator[SessionInfo]:
    """Iterate over the sessions of a host, newest first, reading pages as they are needed.

    ``scope="roots"`` (the default) lists root sessions, ``scope="children", parent=id`` the
    direct subagents of a session, and ``scope="tree", root=id`` a root session and all its
    subagents. ``status=`` keeps only the sessions in that status. ``limit=`` stops after that
    many sessions. Archived sessions are not listed.

    ``host="deployed"`` (the default) lists the sessions that your API key started on the control
    plane, through ``client``. Without one, a default ``agents.Client()`` is used: the API key and
    URLs come from the environment, and a missing ``MISTRAL_API_KEY`` raises ``SdkError`` at the
    call. ``list_sessions(client=client)`` is ``client.list_sessions()``. ``host="local"`` lists the
    sessions of this event loop's local runtime, as ``agents.local_runtime().list_sessions()`` does, and
    takes no ``client``.

    A ``root=`` or ``parent=`` that is not a UUID raises ``SdkError`` at the call. One that names no
    session of the host raises ``SessionNotFoundError``, a ``LookupError``, whose ``session_id`` is that
    id, and so does a subagent as the ``root=`` of ``scope="tree"``, on both hosts. Any other wrong
    argument raises ``SdkError`` at the call too.
    """
    if host not in _HOSTS:
        raise sdk_errors.SdkError(f"host must be 'deployed' or 'local', got {host!r}")
    from mistralai.vibe_agents.sdk.client.api_client import Client  # noqa: PLC0415

    if client is not None and not isinstance(client, Client):
        raise sdk_errors.SdkError(f"client must be an agents.Client or None, got {type(client).__name__}")
    if host == "local":
        if client is not None:
            raise sdk_errors.SdkError('client= lists deployed sessions; host="local" takes no client')
        return local_runtime().list_sessions(scope=scope, root=root, parent=parent, status=status, limit=limit)
    # Without a client, the default agents.Client() without a pool: each page opens and closes its own.
    if client is None:
        # The arguments are checked before the environment, as a client checks them.
        _catalog_params(scope, root, parent, status, limit)
        client = Client._per_call()
    return client.list_sessions(scope=scope, root=root, parent=parent, status=status, limit=limit)


def _deployed_sessions(
    deployment: remote_transport.RemoteAgentDeployment,
    *,
    scope: SessionScope,
    root: str | None,
    parent: str | None,
    status: SessionStatus | None,
    limit: int | None,
) -> AsyncIterator[SessionInfo]:
    """The deployed listing of an ``agents.Client``, through its pool if it has one."""
    params = _catalog_params(scope, root, parent, status, limit)
    return _iterate(_DeployedPages(deployment, params.scope).page, params, status, limit)


class _DeployedPages:
    """Reads catalog pages from the control plane, each through a transport of its own. Without a
    pool on the deployment's client, each page opens and closes its own connection, so an iteration
    that stops early holds nothing open."""

    def __init__(
        self, deployment: remote_transport.RemoteAgentDeployment, scope: harness_session.SessionCatalogScope
    ) -> None:
        self._deployment = deployment
        self._scope_session_id = _scope_session_id(scope)
        # The control plane answers 404 for a subagent as a tree root too.
        self._not_found_detail = (
            'scope="tree" also takes only the root of a tree, not a subagent'
            if isinstance(scope, harness_session.TreeScope)
            else None
        )

    async def page(self, params: harness_session.CatalogListParams) -> harness_session.CatalogListResponse:
        transport = remote_transport._control_plane_transport(self._deployment)
        try:
            return await transport.request("app_server/catalog/list", params, harness_session.CatalogListResponse)
        except httpx.HTTPStatusError as error:
            # The control plane answers 404 for a root or a parent that the API key cannot read.
            if error.response.status_code == httpx.codes.NOT_FOUND and self._scope_session_id is not None:
                raise sdk_errors.SessionNotFoundError(self._scope_session_id, self._not_found_detail) from error
            raise
        finally:
            await transport.close()


def _catalog_params(
    scope: object, root: str | None, parent: str | None, status: object, limit: object
) -> harness_session.CatalogListParams:
    if status is not None and status not in _STATUSES:
        raise sdk_errors.SdkError(f"status must be 'running', 'waiting', 'terminated' or None, got {status!r}")
    if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit < 1):
        raise sdk_errors.SdkError(f"limit must be a positive integer or None, got {limit!r}")
    for name, session_id in (("root", root), ("parent", parent)):
        if session_id is not None and not isinstance(session_id, str):
            raise sdk_errors.SdkError(f"{name}= must be a session id string or None, got {session_id!r}")
    catalog_scope: harness_session.SessionCatalogScope
    match scope:
        case "roots" if root is None and parent is None:
            catalog_scope = harness_session.RootsScope()
        case "children" if parent is not None and root is None:
            catalog_scope = harness_session.DirectChildrenScope(parent_session_id=parent)
        case "tree" if root is not None and parent is None:
            catalog_scope = harness_session.TreeScope(root_session_id=root)
        case _ if scope not in _SCOPES:
            raise sdk_errors.SdkError(f"scope must be 'roots', 'children' or 'tree', got {scope!r}")
        case "roots":
            raise sdk_errors.SdkError('scope="roots" takes no root= or parent=: it lists the root sessions')
        case "children":
            raise sdk_errors.SdkError(
                'scope="children" takes parent=<session id> only, the session to list the subagents of'
            )
        case _:
            raise sdk_errors.SdkError('scope="tree" takes root=<session id> only, the root session of the tree to list')
    for name, session_id in (("root", root), ("parent", parent)):
        if session_id is not None:
            try:
                UUID(session_id)
            except ValueError as error:
                raise sdk_errors.SdkError(f"{name}= must be a UUID, the id of a session, got {session_id!r}") from error
    # Without a status filter, a page larger than the limit reads sessions that are never given.
    page_size = min(limit, _PAGE_SIZE) if limit is not None and status is None else _PAGE_SIZE
    return harness_session.CatalogListParams(scope=catalog_scope, page=harness_session.ListPageRequest(limit=page_size))


def _scope_session_id(scope: harness_session.SessionCatalogScope) -> str | None:
    match scope:
        case harness_session.TreeScope(root_session_id=session_id):
            return session_id
        case harness_session.DirectChildrenScope(parent_session_id=session_id):
            return session_id
        case _:
            return None


def _not_in_local_runtime(session_id: str) -> sdk_errors.SessionNotFoundError:
    return sdk_errors.local_session_not_found(session_id, "it is not a session of this event loop's local runtime")


async def _iterate(
    page: _ListPage,
    params: harness_session.CatalogListParams,
    status: SessionStatus | None,
    limit: int | None,
) -> AsyncIterator[SessionInfo]:
    given = 0
    cursor: str | None = None
    while True:
        response = await page(params.model_copy(update={"page": params.page.model_copy(update={"cursor": cursor})}))
        for item in response.items:
            if status is not None and item.status != status:
                continue
            yield _session_info(item)
            given += 1
            if limit is not None and given >= limit:
                return
        cursor = response.next_cursor
        if cursor is None:
            return


def _session_info(item: harness_session.Session) -> SessionInfo:
    return SessionInfo(
        id=str(item.id),
        parent_id=str(item.parent_session_id) if item.parent_session_id is not None else None,
        root_id=str(item.root_session_id),
        title=item.title,
        status=read_value(item.status, "SessionInfo.status"),
        created_at=_utc(item.created_at),
        updated_at=_utc(item.updated_at),
        archived_at=_utc(item.archived_at) if item.archived_at is not None else None,
        termination=_termination(item.termination) if item.termination is not None else None,
    )


def _termination(termination: harness_session.Termination) -> Termination:
    match termination:
        case harness_session.CompletedTermination(stop_reason=stop_reason):
            return CompletedTermination(stop_reason=read_value(stop_reason, "CompletedTermination.stop_reason"))
        case harness_session.CancelledTermination(cause=cause):
            return CancelledTermination(cause=cause)
        case harness_session.FailedTermination(error=error):
            return FailedTermination(error=protocol_error(error))
        case _:
            return UnknownTermination(outcome=termination.original_outcome, raw=termination.raw)


def _utc(unix_ms: int) -> datetime:
    return datetime.fromtimestamp(unix_ms / 1000, tz=UTC)
