"""Compose process-local Agents SDK resources around Harness SessionTransport."""

import asyncio
import atexit
import concurrent.futures.thread  # noqa: F401  # registers the thread pools' exit hook first
import os
import threading
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable, Iterator, Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

import structlog
from pydantic import JsonValue

from mistralai.client import Mistral
from mistralai.vibe.harness.app_server.session import (
    CallbacksTreeParams,
    CallbacksTreeResponse,
    ClientTransportStreamItem,
    EmbeddedResourceContentBlock,
    EventsReadParams,
    HistoryImportEntry,
    InitialTurn,
    MaterializedSkillDefinition,
    SessionClient,
    SessionIdempotencyConflictError,
    SessionModel,
    SessionReadParams,
    SessionReadResponse,
    SessionStartParams,
    SessionStartResponse,
    SessionTerminatedError,
    SessionTransport,
)
from mistralai.vibe.harness.app_server.session.file_embedding import FileEmbedder
from mistralai.vibe.harness.app_server.session.file_upload import FileUploader
from mistralai.vibe.harness.app_server.session.local import (
    LocalManagerAttachment,
    LocalSessionClosedError,
    LocalSessionResource,
)
from mistralai.vibe.harness.app_server.session.local_event_log import JsonlSessionEventLog
from mistralai.vibe.harness.app_server.session.local_manager import (
    LocalSessionBinding,
    LocalSessionManager,
    LocalSessionWorkspace,
)
from mistralai.vibe.harness.app_server.session.models.state import ListPageRequest
from mistralai.vibe.harness.app_server.session.procedures.session import SubagentSession, SubagentsListParams
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.agents.control_plane import SessionControlPlaneError
from mistralai.vibe.harness.runtime.agents.policy import SubagentPolicy
from mistralai.vibe.harness.runtime.capabilities.skills import SkillHost
from mistralai.vibe.harness.runtime.completion import CompletionConfig, CompletionProvider
from mistralai.vibe.harness.runtime.completion.config import build_completion_provider
from mistralai.vibe.harness.runtime.configuration import build_capability_configuration_from_agent_config
from mistralai.vibe.harness.runtime.hosts.local.journal import JsonFileSessionJournal, in_memory_journal
from mistralai.vibe.harness.runtime.hosts.local.residency import (
    DEFAULT_LOCAL_SESSION_RESIDENCY_POLICY,
    LocalSessionResidencyPolicy,
)
from mistralai.vibe.harness.runtime.hosts.mcp_http import McpHttpCapabilityHost
from mistralai.vibe.harness.runtime.hosts.workflows import (
    WorkflowSandboxResource,
)
from mistralai.vibe.harness.runtime.session.configuration import BASH_MAX_TIMEOUT
from mistralai.vibe.harness.runtime.session.definition import SessionDefinition
from mistralai.vibe.harness.runtime.session.intake import DEFAULT_SESSION_INTAKE_LIMITS, SessionIntakeLimits
from mistralai.vibe.harness.runtime.session.model_wait import DEFAULT_MODEL_WAIT_POLICY, ModelWaitPolicy
from mistralai.vibe.harness.runtime.session.programs import DEFAULT_PROGRAM_EXECUTION_POLICY, ProgramExecutionPolicy
from mistralai.vibe.harness.runtime.session.turn_policy import DEFAULT_TURN_EXECUTION_POLICY, TurnExecutionPolicy
from mistralai.vibe.harness.runtime.tools.handler import BuiltinToolHandler
from mistralai.vibe.harness.runtime.tools.processes import (
    BUILTIN_PROCESS_TOOLS,
    BackgroundProcessToolHandler,
    build_background_process_tool_handlers,
)
from mistralai.vibe_agents.sdk.app import config as app_config
from mistralai.vibe_agents.sdk.assembly import assemble, capabilities, connectors, mcp, sandbox_skills
from mistralai.vibe_agents.sdk.assembly import sandbox as sandbox_assembly
from mistralai.vibe_agents.sdk.assembly import session_inputs as session_input_assembly
from mistralai.vibe_agents.sdk.assembly.local_mistral import local_mistral_client
from mistralai.vibe_agents.sdk.assembly.stateful import StateMap
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring.errors import (
    SdkError,
    SessionConfigMismatchError,
    SessionInUseError,
    SessionNotFoundError,
    public_errors,
    public_iter_errors,
)

from . import telemetry
from .client_tools import NO_CLIENT_TOOLS, ClientToolRegistry, ClientToolSessionClient
from .procedures import LOCAL_PROCEDURES, AllowlistedSessionTransport
from .session_file_manager import LocalSessionFileManager
from .session_file_stager import SessionFileStager
from .session_files import DEFAULT_SESSION_FILE_POLICY, SessionFilePolicy
from .session_journal import SessionJournals, harness_journals

logger = structlog.get_logger(__name__)


def _completion_provider_factory(
    provider: CompletionProvider | None,
) -> Callable[[CompletionConfig], CompletionProvider]:
    """Build each Session's provider from its config, unless one provider answers every Session."""
    if provider is None:
        return build_completion_provider
    return lambda _config: provider


def _validated_session_inputs(
    assembly: assemble.AgentAssembly,
    session_inputs: Mapping[str, contracts.SessionInput] | None,
) -> dict[str, JsonValue]:
    serialized_session_inputs = session_input_assembly.serialize_session_inputs(
        session_inputs,
        declared_classes=assembly.session_input_classes,
    )
    # Checked before the Sandbox is provisioned: a Session missing a declared
    # input can never run, so it must fail without side effects.
    try:
        session_input_assembly.bind_session_inputs(
            assembly.config, assembly.sandbox, serialized_session_inputs, sandbox_is_live=False
        )
    except ValueError as error:
        raise SdkError(str(error)) from error
    return serialized_session_inputs


class _LocalSessionInUseError(SessionInUseError, SessionControlPlaneError):
    """``SessionInUseError`` that keeps the Harness error's ``code`` for callers that read it."""

    def __init__(self, session_id: str, error: SessionControlPlaneError) -> None:
        SessionControlPlaneError.__init__(
            self, error.code, str(error), retryable=error.retryable, settled=error.settled
        )
        self.session_id = session_id


class _LocalSessionConfigMismatchError(SessionConfigMismatchError, SessionControlPlaneError):
    """``SessionConfigMismatchError`` that keeps the Harness error's ``code`` for callers that read it."""

    def __init__(self, session_id: str, error: SessionControlPlaneError) -> None:
        SessionControlPlaneError.__init__(
            self, error.code, str(error), retryable=error.retryable, settled=error.settled
        )
        self.session_id = session_id


def _reopen_error(session_id: str, error: SessionControlPlaneError) -> SessionControlPlaneError:
    """The SDK error for a reopen that the Harness refused, or the Harness error itself."""
    if error.code == "session_in_use":
        return _LocalSessionInUseError(session_id, error)
    if error.code == "session_config_mismatch":
        return _LocalSessionConfigMismatchError(session_id, error)
    return error


@dataclass(frozen=True, slots=True)
class _RootShare:
    """What a root lends the children that run in its sandbox."""

    hook_sandbox: contracts.HookSandbox
    skill_host: SkillHost | None
    sandbox: WorkflowSandboxResource
    skill_files: sandbox_skills.SandboxSkillFiles | None
    completion_provider_factory: Callable[[CompletionConfig], CompletionProvider] | None = None
    files: LocalSessionFileManager | None = None


@dataclass(frozen=True, slots=True)
class _RootStart:
    """What a root brings to its own binding while it starts."""

    assembly: assemble.AgentAssembly
    telemetry: telemetry.LocalSessionTelemetry
    skill_files: sandbox_skills.SandboxSkillFiles | None
    completion_provider_factory: Callable[[CompletionConfig], CompletionProvider] | None


class _RootShareRelease:
    def __init__(self, roots: dict[str, _RootShare], session_id: str) -> None:
        self._roots = roots
        self._session_id = session_id

    async def close(self) -> None:
        self._roots.pop(self._session_id, None)


class _StateRelease:
    """Forget a Session's saved values when the Session is disposed."""

    def __init__(self, values: dict[str, StateMap], session_id: str) -> None:
        self._values = values
        self._session_id = session_id

    async def close(self) -> None:
        self._values.pop(self._session_id, None)


@asynccontextmanager
async def _closing[ItemT](items: AsyncIterator[ItemT]) -> AsyncIterator[AsyncIterator[ItemT]]:
    """Close ``items`` on exit when it can be closed, as an async generator can."""
    try:
        yield items
    finally:
        aclose = getattr(items, "aclose", None)
        if aclose is not None:
            await aclose()


class _RuntimeOwningAttachment(SessionTransport):
    """Closing this attachment closes its runtime and every Session it started."""

    def __init__(self, attachment: SessionTransport, runtime: "_AgentsSdkLocalRuntime") -> None:
        self._attachment = attachment
        self._runtime = runtime

    async def request[ResultT: SessionModel](
        self, method: str, params: SessionModel, result_type: type[ResultT]
    ) -> ResultT:
        return await self._attachment.request(method, params, result_type)

    def read_events(self, params: EventsReadParams) -> AsyncIterator[ClientTransportStreamItem]:
        return self._attachment.read_events(params)

    def watch_callbacks_tree(self, params: CallbacksTreeParams) -> AsyncIterator[CallbacksTreeResponse]:
        return self._attachment.watch_callbacks_tree(params)

    async def close(self) -> None:
        try:
            await self._attachment.close()
        except BaseException as error:
            try:
                await self._runtime.close()
            except BaseException as cleanup_error:
                error.add_note(f"Runtime cleanup failed: {cleanup_error!r}")
            raise
        await self._runtime.close()


class _LocalSessionNotFoundError(SessionNotFoundError, SessionControlPlaneError):
    """A local session ID this runtime does not know. Still the Harness's ``session_not_found`` error."""

    def __init__(self, session_id: str, error: SessionControlPlaneError) -> None:
        SessionControlPlaneError.__init__(
            self,
            error.code,
            f"Session {session_id} was not found: no session with this ID ran in this process",
            retryable=error.retryable,
            settled=error.settled,
            session_loss=error.session_loss,
        )
        self.session_id = session_id


def _not_found(error: SessionControlPlaneError, session_id: object) -> SessionControlPlaneError:
    if error.code != "session_not_found" or not isinstance(session_id, str):
        return error
    return _LocalSessionNotFoundError(session_id, error)


class _TreeAttachment(LocalManagerAttachment):
    """Client attachment that lets its runtime know when the last client of a tree detaches.

    A session ID the runtime does not know raises ``SessionNotFoundError``, as on a deployment. As on a
    deployment's transport, the errors of its calls are ``AgentsError`` (see ``as_agents_error``).
    """

    def __init__(
        self,
        runtime: "_AgentsSdkLocalRuntime",
        *,
        session_id_factory: Callable[[], str] | None = None,
        definition: SessionDefinition | None = None,
        reopen: Callable[["_TreeAttachment"], Awaitable[None]] | None = None,
    ) -> None:
        super().__init__(runtime.manager, session_id_factory=session_id_factory, definition=definition)
        self._runtime = runtime
        self._root_session_id: str | None = None
        # Reopens a saved Session before the first use; kept until a reopen succeeds, so a use
        # after a failed one tries again.
        self._reopen = reopen
        self._reopen_lock = asyncio.Lock()

    def hold(self, root_session_id: str) -> None:
        self._root_session_id = root_session_id
        self._runtime._hold_tree(root_session_id)

    async def _reopen_first(self) -> None:
        if self._reopen is None:
            return
        async with self._reopen_lock:
            reopen = self._reopen
            if reopen is None:
                return
            await reopen(self)
            self._reopen = None

    @public_errors
    async def request[ResultT: SessionModel](
        self, method: str, params: SessionModel, result_type: type[ResultT]
    ) -> ResultT:
        await self._reopen_first()
        try:
            return await super().request(method, params, result_type)
        except SessionControlPlaneError as error:
            session_id = getattr(params, "session_id", None) or getattr(params, "parent_session_id", None)
            if (public := _not_found(error, session_id)) is error:
                raise
            raise public from error

    @public_iter_errors
    async def read_events(self, params: EventsReadParams) -> AsyncIterator[ClientTransportStreamItem]:
        await self._reopen_first()
        events = super().read_events(params)
        try:
            async for item in events:
                yield item
        except SessionControlPlaneError as error:
            if (public := _not_found(error, params.session_id)) is error:
                raise
            raise public from error
        finally:
            if isinstance(events, AsyncGenerator):
                await events.aclose()

    @public_iter_errors
    async def watch_callbacks_tree(self, params: CallbacksTreeParams) -> AsyncIterator[CallbacksTreeResponse]:
        await self._reopen_first()
        try:
            trees = super().watch_callbacks_tree(params)
        except SessionControlPlaneError as error:
            if (public := _not_found(error, params.session_id)) is error:
                raise
            raise public from error
        async with _closing(trees) as opened:
            async for tree in opened:
                yield tree

    async def close(self) -> None:
        try:
            await super().close()
        finally:
            root_session_id, self._root_session_id = self._root_session_id, None
            if root_session_id is not None:
                self._runtime._release_tree(root_session_id)


class _AgentsSdkLocalRuntime:
    """Local manager that hosts Session Trees; attachments borrow its execution lifetime.

    ``completion_provider`` answers the model calls of every Session that does not bring its own.
    With ``dispose_idle_trees``, a tree that has no client attached and no work left is closed
    and frees its sandbox; its Sessions stay readable but take no new command. ``keep_idle_trees``
    turns that off for the rest of the runtime's life.
    """

    def __init__(
        self,
        *,
        subagent_policy: SubagentPolicy | None = None,
        residency_policy: LocalSessionResidencyPolicy = DEFAULT_LOCAL_SESSION_RESIDENCY_POLICY,
        program_policy: ProgramExecutionPolicy = DEFAULT_PROGRAM_EXECUTION_POLICY,
        wait_policy: ModelWaitPolicy = DEFAULT_MODEL_WAIT_POLICY,
        turn_policy: TurnExecutionPolicy = DEFAULT_TURN_EXECUTION_POLICY,
        intake_limits: SessionIntakeLimits = DEFAULT_SESSION_INTAKE_LIMITS,
        callback_timeout: timedelta | None = None,
        completion_provider: CompletionProvider | None = None,
        dispose_idle_trees: bool = False,
        file_policy: SessionFilePolicy = DEFAULT_SESSION_FILE_POLICY,
        event_log_directory: Path | str | None = None,
        journal_factory: SessionJournals | None = None,
    ) -> None:
        if callback_timeout is not None and callback_timeout <= timedelta(0):
            raise ValueError("callback_timeout must be positive")
        self._closed = False
        self._dispose_idle_trees = dispose_idle_trees
        self._program_policy = program_policy
        # Attached clients per root, and the task that closes a tree once nothing holds it.
        self._attached: dict[str, int] = {}
        self._disposals: dict[str, asyncio.Task[None]] = {}
        self._disposing: set[str] = set()
        # Per Session kept by ``start_kept_session``: the task that lets its tree go once its root
        # fails or the tree ends.
        self._kept_tree_watches: dict[str, asyncio.Task[None]] = {}
        # The roots whose tree ``start_kept_session`` still holds.
        self._kept_roots: set[str] = set()
        # The roots of ``agent.run`` trees: they close once their Turns end, even with a
        # background process still running, which the close stops.
        self._run_roots: set[str] = set()
        self.capability_resolver = capabilities.WorkflowCapabilityResolver()
        self._file_policy = file_policy
        self._journals = journal_factory
        self._journal_factory = harness_journals(journal_factory) if journal_factory is not None else in_memory_journal
        # The reopen of each saved Session that is reopening, by Session ID; callers share it.
        self._reopens: dict[str, asyncio.Future[bool]] = {}
        self._starting: dict[str, _RootStart] = {}
        # Children run in their root's sandbox, so their Hooks reach the root's Hook sandbox
        # and their skills are read from the files the root wrote there.
        self._roots: dict[str, _RootShare] = {}
        # Root Sessions started with an idempotency key, by key: the start's request fingerprint and task.
        self._starts_by_key: dict[str, tuple[str, asyncio.Future[Any]]] = {}
        # The saved values of each subagent Session's stateful objects (a root Session's live in its
        # assembly). A Session that is unloaded and loaded again binds again, and keeps its values.
        self._values: dict[str, StateMap] = {}
        self.manager = LocalSessionManager(
            completion_provider_factory=_completion_provider_factory(completion_provider),
            binding_factory=self._bind,
            event_log_factory=(
                JsonlSessionEventLog.in_directory(event_log_directory) if event_log_directory is not None else None
            ),
            journal_factory=self._journal_factory,
            subagent_policy=subagent_policy,
            residency_policy=residency_policy,
            program_policy=program_policy,
            wait_policy=wait_policy,
            turn_policy=turn_policy,
            intake_limits=intake_limits,
            # The same setting as on a served or deployed worker, so approvals wait as long here.
            callback_timeout=(
                callback_timeout if callback_timeout is not None else app_config.get_app_settings().callback_timeout
            ),
        )

    def __deepcopy__(self, memo: dict[int, object]) -> "_AgentsSdkLocalRuntime":
        # Copying an authored Agent must preserve its live application binding.
        memo[id(self)] = self
        return self

    async def create_session(
        self,
        assembly: assemble.AgentAssembly,
        *,
        session_id: str,
        history: list[HistoryImportEntry] | None = None,
        session_inputs: Mapping[str, contracts.SessionInput] | None = None,
        completion_provider: CompletionProvider | None = None,
        close_runtime_with_client: bool = False,
        initial_turn: InitialTurn | None = None,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    ) -> SessionClient:
        """Start a root Session, with ``initial_turn`` as its first Turn when given, and attach a client.

        Closing the client only detaches it: the Session and its children run until this runtime
        closes, or until the tree is idle and unattached when ``dispose_idle_trees`` is set.
        With ``close_runtime_with_client``, closing the client also closes this runtime and every
        Session it started. ``completion_provider`` answers the model calls of the whole tree, in
        place of the runtime's own.
        """
        serialized_session_inputs = _validated_session_inputs(assembly, session_inputs)
        mcp.verify_tree_credentials(assembly.config)
        skill_files = _prepare_skill_files(assembly)
        session_telemetry = telemetry.LocalSessionTelemetry()
        self._starting[session_id] = _RootStart(
            assembly,
            session_telemetry,
            skill_files,
            _completion_provider_factory(completion_provider) if completion_provider is not None else None,
        )
        tree_attachment = _TreeAttachment(
            self, session_id_factory=lambda: session_id, definition=assembly.harness_definition
        )
        tree_attachment.hold(session_id)
        attachment: SessionTransport = tree_attachment
        if close_runtime_with_client:
            attachment = _RuntimeOwningAttachment(attachment, self)
        client: SessionClient | None = None
        try:
            response = await attachment.request(
                "app_server/session/start",
                SessionStartParams(
                    agent_config=assembly.config,
                    history=list(history or ()),
                    session_inputs=serialized_session_inputs,
                    initial_turn=initial_turn,
                ),
                SessionStartResponse,
            )
            client = ClientToolSessionClient(
                AllowlistedSessionTransport(attachment, backend="local", procedures=LOCAL_PROCEDURES),
                client_tools=client_tools,
                uploader=self._uploader_for(session_id),
            )
            await client.adopt_session_snapshot(response.state, response.last_event_id)
        except BaseException as error:
            try:
                if client is not None:
                    await client.close()
                else:
                    await attachment.close()
            except BaseException as cleanup_error:
                error.add_note(f"Session client cleanup failed: {cleanup_error!r}")
            raise
        finally:
            self._starting.pop(session_id, None)
        session_telemetry.session_started(session_id, agent_name=assembly.config.name)
        return client

    async def start_kept_session(
        self,
        assembly: assemble.AgentAssembly,
        *,
        session_id: str,
        history: list[HistoryImportEntry] | None = None,
        session_inputs: Mapping[str, contracts.SessionInput] | None = None,
        completion_provider: CompletionProvider | None = None,
        initial_turn: InitialTurn | None = None,
    ) -> str | None:
        """Start a root Session that runs until it is cancelled or this runtime closes, with no client attached.

        ``initial_turn`` starts the Session with that message as its first Turn, whose ID this
        returns; without it, this returns ``None``.

        A kept tree is never closed as idle: a program reaches it by its ID at any later time.
        If the root's worker fails, the root takes no command again, so the tree is let go: it
        closes as idle, sandbox included, once no client holds it and its subagents are idle,
        unless ``keep_idle_trees`` keeps it.
        A cancelled tree has already closed, and is let go too.
        """
        client = await self.create_session(
            assembly,
            session_id=session_id,
            history=history,
            session_inputs=session_inputs,
            completion_provider=completion_provider,
            initial_turn=initial_turn,
        )
        self._keep_tree(session_id)
        turns = client.state.turns.items if client.state.turns is not None else []
        await client.close()
        return turns[0].id if initial_turn is not None and turns else None

    def _keep_tree(self, root_session_id: str) -> None:
        # Released only once the root fails or the tree ends, so the tree stays held once its
        # clients detach.
        self._hold_tree(root_session_id)
        self._kept_roots.add(root_session_id)
        self._kept_tree_watches[root_session_id] = asyncio.get_running_loop().create_task(
            self._release_kept_tree_when_it_ends(root_session_id), name=f"agents-sdk-local-kept-tree:{root_session_id}"
        )

    async def _release_kept_tree_when_it_ends(self, root_session_id: str) -> None:
        try:
            record = self.manager.record(root_session_id)
            while True:
                # Take the signal before reading, so a change made after the read still wakes this.
                changed = record.tree_changes.changed()
                if record.closed or record.failure is not None:
                    break
                await changed.wait()
            self._kept_roots.discard(root_session_id)
            self._release_tree(root_session_id)
        finally:
            if self._kept_tree_watches.get(root_session_id) is asyncio.current_task():
                del self._kept_tree_watches[root_session_id]

    async def start_once[T](self, idempotency_key: str, start: Callable[[], Awaitable[T]], *, fingerprint: str) -> T:
        """Return what ``start`` returned for ``idempotency_key``, and call ``start`` on first use.

        ``fingerprint`` identifies the start's request. A later call with the key and the same
        fingerprint returns the first Session; one with another fingerprint raises
        ``SessionIdempotencyConflictError``. A start that fails or is cancelled frees its key. A caller
        that stops waiting does not stop the start, which other callers of the key share.
        """
        claimed = self._starts_by_key.get(idempotency_key)
        if claimed is not None:
            claimed_fingerprint, started = claimed
            if claimed_fingerprint != fingerprint:
                raise SessionIdempotencyConflictError(idempotency_key=idempotency_key)
        else:
            started = asyncio.ensure_future(start())
            self._starts_by_key[idempotency_key] = (fingerprint, started)

            def forget_failed_start(task: asyncio.Future[Any]) -> None:
                if (task.cancelled() or task.exception() is not None) and self._starts_by_key.get(
                    idempotency_key, (None, None)
                )[1] is task:
                    del self._starts_by_key[idempotency_key]

            started.add_done_callback(forget_failed_start)
        return await asyncio.shield(started)

    def bind_session(
        self,
        session_id: str,
        *,
        reassemble: Callable[[], assemble.AgentAssembly] | None = None,
        completion_provider: CompletionProvider | None = None,
    ) -> _TreeAttachment:
        """Return a transport to a Session of this runtime by its ID, without reading the Session.

        The transport keeps the Session's tree from being closed as idle until it closes. An ID
        this runtime does not know binds too: the first request for it fails as not found. An ID
        bound before its Session exists does not hold the Session's tree.

        With ``reassemble``, and a ``journal_factory`` on this runtime, the first use of the
        transport reopens the Session that an earlier process saved under an ID this runtime
        does not know, as ``reopen_saved`` does with ``completion_provider``, and holds its tree.
        """
        try:
            root_session_id = self.manager.record(session_id).root_session_id
        except SessionControlPlaneError as error:
            if error.code != "session_not_found":
                raise
        else:
            attachment = _TreeAttachment(self)
            attachment.hold(root_session_id)
            return attachment
        if reassemble is None or self._journals is None:
            return _TreeAttachment(self)

        async def reopen(attachment: _TreeAttachment) -> None:
            if await self.reopen_saved(session_id, reassemble, completion_provider=completion_provider):
                attachment.hold(session_id)

        return _TreeAttachment(self, reopen=reopen)

    async def reopen_saved(
        self,
        session_id: str,
        reassemble: Callable[[], assemble.AgentAssembly],
        *,
        completion_provider: CompletionProvider | None = None,
    ) -> bool:
        """Reopen the root Session that an earlier process saved under ``session_id``, and keep it.

        Return ``False``, and do nothing, when this runtime knows the ID already, or when nothing
        is saved under it. ``reassemble`` builds the Agent again; it runs only for a reopen.
        ``completion_provider`` answers the model calls of the reopened tree, in place of the
        runtime's own, as in ``create_session``. Calls for one ID share one reopen. The reopened
        tree is kept until this runtime closes, as ``start_kept_session`` keeps its own: closing
        it as idle would save it as ended.

        Raises ``SessionInUseError`` when another process holds the Session, and
        ``SessionConfigMismatchError`` when ``reassemble`` builds another Agent than the saved one.
        """
        if self._journals is None:
            return False
        if self._closed:
            raise SdkError(f"The local runtime closed, so it cannot reopen session {session_id}")
        if self._knows(session_id):
            return False
        reopening = self._reopens.get(session_id)
        if reopening is None:
            reopening = asyncio.ensure_future(self._reopen_saved(session_id, reassemble, completion_provider))
            self._reopens[session_id] = reopening

            def forget(task: asyncio.Future[bool]) -> None:
                if self._reopens.get(session_id) is task:
                    del self._reopens[session_id]

            reopening.add_done_callback(forget)
        try:
            return await asyncio.shield(reopening)
        except asyncio.CancelledError:
            # ``close()`` cancelled the shared reopen, not this caller's task: say why.
            if reopening.cancelled() and self._closed:
                current = asyncio.current_task()
                if current is None or not current.cancelling():
                    raise SdkError(f"The local runtime closed while it reopened session {session_id}") from None
            raise

    async def _reopen_saved(
        self,
        session_id: str,
        reassemble: Callable[[], assemble.AgentAssembly],
        completion_provider: CompletionProvider | None,
    ) -> bool:
        try:
            journal = self._journal_factory(session_id)
        except ValueError:
            # The ID cannot name a journal, so no Session is saved under it.
            return False
        saved = await journal.load()
        if saved is None:
            return False
        assembly = reassemble()
        # Session inputs are fixed for the Session's lifetime, so the new sandbox's
        # hooks get the saved values, as the restored Runtime's tools and hooks do.
        try:
            session_input_assembly.bind_session_inputs(
                assembly.config, assembly.sandbox, saved.session_inputs, sandbox_is_live=False
            )
        except ValueError as input_error:
            raise SdkError(str(input_error)) from input_error
        self._starting[session_id] = _RootStart(
            assembly,
            telemetry.LocalSessionTelemetry(),
            _prepare_skill_files(assembly),
            _completion_provider_factory(completion_provider) if completion_provider is not None else None,
        )
        try:
            await self.manager.reopen(session_id, assembly.harness_definition)
        except SessionControlPlaneError as error:
            mapped = _reopen_error(session_id, error)
            if mapped is error:
                raise
            raise mapped from error
        finally:
            self._starting.pop(session_id, None)
        # A Session saved as ended reopens closed: it serves reads, and has no tree to keep.
        if not self.manager.record(session_id).closed:
            self._keep_tree(session_id)
        return True

    def _knows(self, session_id: str) -> bool:
        try:
            self.manager.record(session_id)
        except SessionControlPlaneError as error:
            if error.code != "session_not_found":
                raise
            return False
        return True

    async def get_session(
        self,
        session_id: str,
        *,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
        reassemble: Callable[[], assemble.AgentAssembly] | None = None,
    ) -> SessionClient:
        """Attach to a Session of this runtime, or reopen one that an earlier process saved.

        ``reassemble`` builds the Agent again for ``session_id``; it runs only for a reopen.
        Without it, only a Session this runtime already holds can attach.
        """
        attachment = self.bind_session(session_id, reassemble=reassemble)
        client: SessionClient | None = None
        try:
            snapshot = await attachment.request(
                "app_server/session/read", SessionReadParams(session_id=session_id), SessionReadResponse
            )
            client = ClientToolSessionClient(
                AllowlistedSessionTransport(attachment, backend="local", procedures=LOCAL_PROCEDURES),
                client_tools=client_tools,
                uploader=self._uploader_for(session_id),
            )
            await client.adopt_session_snapshot(snapshot.state, snapshot.last_event_id)
        except BaseException:
            if client is not None:
                await client.close()
            else:
                await attachment.close()
            raise
        return client

    def _hold_tree(self, root_session_id: str) -> None:
        self._attached[root_session_id] = self._attached.get(root_session_id, 0) + 1
        # A tree already closing stays closed; the new client can still read it.
        if root_session_id not in self._disposing and (task := self._disposals.pop(root_session_id, None)):
            task.cancel()

    def _release_tree(self, root_session_id: str) -> None:
        remaining = self._attached.get(root_session_id, 0) - 1
        if remaining > 0:
            self._attached[root_session_id] = remaining
            return
        self._attached.pop(root_session_id, None)
        self._schedule_idle_disposal(root_session_id)

    def _schedule_idle_disposal(self, root_session_id: str) -> None:
        if (
            not self._dispose_idle_trees
            or self._closed
            or root_session_id in self._disposals
            or self._attached.get(root_session_id)
        ):
            return
        try:
            root = self.manager.record(root_session_id)
        except Exception:
            # The root never started, or the manager is closed.
            return
        if root.closed:
            self._run_roots.discard(root_session_id)
            return
        self._disposals[root_session_id] = asyncio.get_running_loop().create_task(
            self._dispose_when_idle(root_session_id), name=f"agents-sdk-local-tree-dispose:{root_session_id}"
        )

    def keep_idle_trees(self) -> None:
        """Close no tree as idle from now on, and stop the idle closes still waiting for a tree.

        An ``async with agents.local_runtime()`` block calls it on entry: its exit closes every
        tree, so until then a tree that no client holds can still be driven. A tree already
        closing stays closed.
        """
        self._dispose_idle_trees = False
        for root_session_id, task in list(self._disposals.items()):
            if root_session_id not in self._disposing:
                del self._disposals[root_session_id]
                task.cancel()

    async def _dispose_when_idle(self, root_session_id: str) -> None:
        task = asyncio.current_task()
        try:
            await self._close_tree(root_session_id, forget=False)
        except LocalSessionClosedError:
            return
        except Exception:
            logger.exception("agents_sdk_local_tree_dispose_failed", root_session_id=root_session_id)
        finally:
            if self._disposals.get(root_session_id) is task:
                del self._disposals[root_session_id]

    async def end_finished_tree(self, root_session_id: str) -> None:
        """Close a tree whose work ended now, sandbox included.

        Its Sessions stay readable until the event loop stops, as every ended local Session. A tree
        that a client still holds, that this runtime no longer knows, or that it keeps once idle
        (``keep_idle_trees``), is left as it is. An error closing the sandbox raises.
        """
        # Fast path: ``_close_tree`` checks ``_dispose_idle_trees`` again after its wait.
        if self._closed or not self._dispose_idle_trees or self._attached.get(root_session_id):
            return
        try:
            idle_disposal = self._disposals.pop(root_session_id, None)
            if idle_disposal is not None:
                if root_session_id in self._disposing:
                    # Already closing: let it finish; it logs its own errors.
                    await asyncio.shield(idle_disposal)
                else:
                    idle_disposal.cancel()
                    await asyncio.gather(idle_disposal, return_exceptions=True)
            try:
                self.manager.record(root_session_id)
            except SessionControlPlaneError as error:
                if error.code != "session_not_found":
                    raise
                return
            await self._close_tree(root_session_id, forget=False)
        except BaseException:
            # A caller that stops waiting before the tree closed leaves it to the idle disposal.
            self._schedule_idle_disposal(root_session_id)
            raise

    def close_after_turns(self, root_session_id: str) -> None:
        """Close this tree once its Turns end and no client holds it, even if work outlives them."""
        self._run_roots.add(root_session_id)

    async def _close_tree(self, root_session_id: str, *, forget: bool) -> None:
        """Close the tree once no client holds it, and with ``forget`` drop its Sessions.

        An ``agent.run`` tree closes once its Turns end; any other tree waits until it is idle.
        """
        if root_session_id in self._run_roots:
            await self.manager.wait_until_turns_end(root_session_id)
        else:
            await self.manager.wait_until_tree_idle(root_session_id)
        # A client may have attached meanwhile, or an agents.local_runtime() block opened.
        if self._attached.get(root_session_id) or not self._dispose_idle_trees:
            return
        self._disposing.add(root_session_id)
        try:
            await self.manager.dispose_tree(root_session_id)
            self._run_roots.discard(root_session_id)
            if forget:
                await self.manager.forget_tree(root_session_id)
                self.capability_resolver.unregister_provider(root_session_id)
        finally:
            self._disposing.discard(root_session_id)

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def journals(self) -> SessionJournals | None:
        """Where this runtime saves its root Sessions, fixed when it was built; ``None`` keeps them in memory."""
        return self._journals

    @property
    def program_policy(self) -> ProgramExecutionPolicy:
        """The program limits of every Session of this runtime, fixed when it was built."""
        return self._program_policy

    def open_sessions(self) -> dict[str, list[str]]:
        """Per open tree that still holds its sandbox for a reason, its Sessions not yet closed.

        A tree counts while a client holds it, while ``start_kept_session`` keeps it, or while one
        of its Sessions runs a Turn. An idle tree that nothing holds does not count: it is closing
        already, or ``keep_idle_trees`` keeps it until the runtime's close ends it. Keys are root
        Session IDs; each value lists the root first, then its open subagents.
        """
        trees: dict[str, list[str]] = {}
        for root_session_id in dict.fromkeys([*self._attached, *self._kept_roots, *self._roots]):
            if not self._session_is_open(root_session_id):
                continue
            links = list(self._subagent_links([root_session_id]))
            if (
                root_session_id not in self._attached
                and root_session_id not in self._kept_roots
                and not self._runs_a_turn(root_session_id)
                and not any(link.session.status == "running" for link in links)
            ):
                continue
            children = (str(link.session.id) for link in links)
            trees[root_session_id] = [
                root_session_id,
                *(session_id for session_id in children if self._session_is_open(session_id)),
            ]
        return trees

    def _runs_a_turn(self, session_id: str) -> bool:
        # A failed Session runs nothing more, even with its Turn left open: its tree closes as idle.
        record = self.manager.record(session_id)
        return (
            not record.closed
            and record.failure is None
            and record.state is not None
            and record.state.active_turn_id is not None
        )

    def _session_is_open(self, session_id: str) -> bool:
        try:
            return not self.manager.record(session_id).closed
        except Exception:
            # The Session never started, or the manager is closed.
            return False

    def running_subagents(self) -> list[SubagentSession]:
        """The subagents of this runtime's trees that still run a Turn, at any depth."""
        return [link for link in self._subagent_links(list(self._roots)) if link.session.status == "running"]

    def _subagent_links(self, parents: list[str]) -> Iterator[SubagentSession]:
        # Every subagent below ``parents``, at any depth.
        while parents:
            parent_id = parents.pop()
            cursor: str | None = None
            while True:
                page = self.manager.list_subagents(
                    SubagentsListParams(parent_session_id=parent_id, page=ListPageRequest(cursor=cursor))
                )
                for link in page.items:
                    parents.append(str(link.session.id))
                    yield link
                cursor = page.next_cursor
                if cursor is None:
                    break

    async def close(self) -> None:
        self._closed = True
        # A start whose callers stopped waiting still runs: stop it before the manager closes.
        stopping: list[asyncio.Future[str] | asyncio.Future[None] | asyncio.Future[bool]] = [
            *self._disposals.values(),
            *self._kept_tree_watches.values(),
            *(start for _, start in self._starts_by_key.values() if not start.done()),
            *(reopen for reopen in self._reopens.values() if not reopen.done()),
        ]
        # A task of a closed loop never runs again, so it cannot be cancelled or awaited.
        disposals = tuple(task for task in stopping if not task.get_loop().is_closed())
        self._disposals.clear()
        self._kept_tree_watches.clear()
        for task in disposals:
            task.cancel()
        await asyncio.gather(*disposals, return_exceptions=True)
        await self.manager.close()

    def _uploader_for(self, session_id: str) -> FileUploader | None:
        record = self.manager.record(session_id)
        share = self._roots.get(record.root_session_id)
        if share is None:
            return None
        if share.files is not None:
            return SessionFileStager(share.files, self._validate_session)
        if share.sandbox.config is not None:
            return None
        embedder = FileEmbedder()

        async def embed(
            session_id: str,
            source: str | Path | bytes | AsyncIterator[bytes],
            *,
            name: str | None,
            media_type: str | None,
        ) -> EmbeddedResourceContentBlock:
            self._validate_session(session_id)
            result = await embedder(session_id, source, name=name, media_type=media_type)
            self._validate_session(session_id)
            return result

        return embed

    def _validate_session(self, session_id: str) -> None:
        record = self.manager.record(session_id)
        record.validate_public_procedure("upload_file")
        if record.closed or record.failure is not None:
            raise SessionTerminatedError("The local Session is closed or failed")

    async def _bind(self, definition: SessionDefinition, root: LocalSessionWorkspace | None) -> LocalSessionBinding:
        owned: list[LocalSessionResource] = []
        session_resources: list[LocalSessionResource] = []
        handlers: Mapping[core_protocol.RuntimeBuiltinToolName, BuiltinToolHandler]
        if root is None:
            session_id = definition.session_id
            if session_id is None:
                raise ValueError("Local root definition requires a Session identity")
            start = self._starting[session_id]
            assembly, session_telemetry, skill_files = start.assembly, start.telemetry, start.skill_files
            completion_provider_factory = start.completion_provider_factory
            registrations = assembly.registrations
            sandbox = await sandbox_assembly.open_sandbox_resource(
                assembly.sandbox,
                bash_max_timeout=BASH_MAX_TIMEOUT,
            )
            # Local Sessions stay eager.
            await sandbox.provision_at_open()
            try:
                skills = await _serve_root_skills(skill_files, sandbox)
                journal = self._journal_factory(session_id)
                files = (
                    # A saved Session keeps its uploads beside its journal, so a reopen finds them.
                    await LocalSessionFileManager.for_saved_sandbox(
                        sandbox, journal.path.with_name(f"{journal.path.stem}.files"), self._file_policy
                    )
                    if isinstance(journal, JsonFileSessionJournal)
                    else LocalSessionFileManager.for_sandbox(sandbox, self._file_policy)
                )
            except BaseException as error:
                try:
                    await sandbox.close()
                except BaseException as cleanup_error:
                    error.add_note(f"Sandbox cleanup failed: {cleanup_error!r}")
                raise
            hook_sandbox = assembly.hook_sandbox
            hook_sandbox.bind(sandbox)
            session_skill_host = skills.host
            self._roots[session_id] = _RootShare(
                hook_sandbox, session_skill_host, sandbox, skill_files, completion_provider_factory, files
            )
            session_resources.extend((sandbox, session_telemetry, _RootShareRelease(self._roots, session_id)))
            if files is not None:
                session_resources.append(files)
            definition = definition.with_runtime_sandbox(sandbox=sandbox.config, workdir=sandbox.workspace)
            if skills.host is not None:
                definition = definition.model_copy(
                    update={"agent_config": sandbox_skills.with_skill_catalog(definition.agent_config, skills.catalog)}
                )
            process_composition = sandbox_assembly.compose_background_process_session(sandbox, assembly.sandbox)
            handlers = sandbox_skills.with_skill_file_hints(process_composition.runtime_builtin_tools, skills.catalog)
            environment = sandbox.command_environment
            large_output = sandbox_assembly.compose_large_output(
                sandbox,
                sandbox_assembly.default_large_output_policy(sandbox),
                session_id=session_id,
            )
            process_handler = process_composition.handler
        else:
            share = self._roots.get(root.definition.session_id) if root.definition.session_id is not None else None
            files = share.files if share is not None else None
            hook_sandbox = share.hook_sandbox if share is not None else contracts.HookSandbox()
            completion_provider_factory = share.completion_provider_factory if share is not None else None
            definition, session_skill_host = await _serve_child_skills(definition, share)
            registrations = (
                root.registrations
                if root.definition.session_id == definition.session_id
                else self.capability_resolver.build_capability_registrations(
                    definition, sandbox=hook_sandbox, values=self._session_values(definition, session_resources)
                )
            )
            definition = definition.with_runtime_sandbox(
                sandbox=root.definition.agent_config.sandbox, workdir=root.definition.agent_config.workdir
            )
            handlers = {
                name: handler
                for name, handler in root.runtime_builtin_tools.items()
                if name not in BUILTIN_PROCESS_TOOLS
            }
            environment = root.command_environment
            large_output = _child_large_output(definition, root, share)
            process_handler = (
                BackgroundProcessToolHandler(
                    root.process_gateway,
                    limit=root.process_limit,
                )
                if root.process_gateway is not None
                else None
            )
            if process_handler is not None:
                handlers = {**handlers, **build_background_process_tool_handlers(process_handler)}
        mcp_host = McpHttpCapabilityHost()
        connector_resource = None
        try:
            slots = self.capability_resolver.build_connector_slots(definition)
            discovery = self.capability_resolver.build_connector_discovery(definition)
            if slots or discovery is not None:
                connector_config = build_capability_configuration_from_agent_config(definition.agent_config).connectors
                if connector_config is None:
                    raise ValueError("Connector resources require connector configuration")
                connector_resource = connectors.AgentsSdkConnectorResource.from_local_environment(
                    slots, discovery=discovery, configuration=connector_config, http_mcp_host=mcp_host
                )
                owned.append(connector_resource)
            return LocalSessionBinding(
                definition=definition,
                message_files=files,
                registrations=registrations,
                runtime_builtin_tools=handlers,
                command_environment=environment,
                large_output=large_output.policy,
                filesystem=large_output.filesystem,
                mcp_host=connector_resource or mcp_host,
                connector_host=connector_resource,
                skill_host=session_skill_host,
                background_process_handler=process_handler,
                owned_resources=tuple(owned),
                session_resources=tuple(session_resources),
                completion_provider_factory=completion_provider_factory,
            )
        except BaseException as error:
            for resource in reversed([*session_resources, *owned]):
                try:
                    await resource.close()
                except BaseException as cleanup_error:
                    error.add_note(f"Local resource cleanup also failed: {cleanup_error!r}")
            raise

    def _session_values(self, definition: SessionDefinition, session_resources: list[LocalSessionResource]) -> StateMap:
        session_id = definition.session_id
        if session_id is None:
            return StateMap()
        values = self._values.get(session_id)
        if values is None:
            values = self._values[session_id] = StateMap()
            session_resources.append(_StateRelease(self._values, session_id))
        return values


# The largest program time budget a local runtime accepts.
_MAX_PROGRAM_TIMEOUT_SECONDS = 4 * 60 * 60


def _program_policy(timeout_seconds: float | None) -> ProgramExecutionPolicy:
    """Return the program limits for a ``program_timeout_seconds`` value, or the defaults for ``None``."""
    if timeout_seconds is None:
        return DEFAULT_PROGRAM_EXECUTION_POLICY
    # NaN fails both comparisons, and infinity is above the maximum.
    if isinstance(timeout_seconds, bool) or not 0 < timeout_seconds <= _MAX_PROGRAM_TIMEOUT_SECONDS:
        raise SdkError(
            f"program_timeout_seconds must be greater than 0 and at most {_MAX_PROGRAM_TIMEOUT_SECONDS} "
            f"(4 hours), got {timeout_seconds!r}"
        )
    return ProgramExecutionPolicy(elapsed_budget_ms=max(1, round(timeout_seconds * 1000)))


@dataclass(slots=True)
class _LoopRuntime:
    runtime: _AgentsSdkLocalRuntime
    # Closes the runtime when its loop shuts down. A loop keeps only weak references to its tasks.
    closer: asyncio.Task[None]
    # The thread that runs the loop.
    thread: threading.Thread
    # Resolved when the runtime is closed before its loop shuts down, so the closer ends quietly.
    released: asyncio.Future[None]
    # The open ``async with agents.local_runtime()`` blocks; the outermost one's exit closes the runtime.
    open_blocks: int = 0


# One runtime per event loop: its Sessions, locks and tasks belong to the loop that started them.
# A forked child gets an empty registry: the parent's loops and Sessions do not run there.
_PROCESS_RUNTIMES: dict[asyncio.AbstractEventLoop, _LoopRuntime] = {}
_PROCESS_RUNTIMES_LOCK = threading.Lock()
# The runtimes that a block's exit took out of the registry and is closing; the lock guards it too.
_CLOSING_RUNTIMES: list[tuple[asyncio.AbstractEventLoop, _LoopRuntime]] = []
# How long the exit hook waits for a loop running in a daemon thread to close its runtime.
_EXIT_CLOSE_TIMEOUT_SECONDS = 10.0


def _process_runtime(
    *, program_policy: ProgramExecutionPolicy | None = None, journals: SessionJournals | None = None
) -> _AgentsSdkLocalRuntime:
    """Return the local runtime of the running event loop, and start it on first use.

    Its Session Trees run until the loop shuts down, as ``asyncio.run`` does when it returns, or
    until the process exits, or until ``_close_process_runtime`` closes it. Closing a client only
    detaches it; a tree with no client and no work left is closed and stays readable, except a tree
    that ``start_kept_session`` keeps, and except while an ``async with agents.local_runtime()`` block
    is open.

    ``program_policy`` starts the runtime with these program limits; a runtime that already runs
    with other limits raises ``SdkError``. Without it, the runtime starts with the defaults.
    ``journals`` starts the runtime saving its root Sessions there, with the same rule: a runtime
    that already runs with other journals, or none, raises ``SdkError``.
    """

    loop = asyncio.get_running_loop()
    with _PROCESS_RUNTIMES_LOCK:
        for closed_loop in [other for other in _PROCESS_RUNTIMES if other.is_closed()]:
            _let_go_of_closed_loop_runtime(_PROCESS_RUNTIMES.pop(closed_loop))
        for closing in [entry for entry in _CLOSING_RUNTIMES if entry[0].is_closed()]:
            _CLOSING_RUNTIMES.remove(closing)
            _let_go_of_closed_loop_runtime(closing[1])
        current = _PROCESS_RUNTIMES.get(loop)
        if current is not None and not current.runtime.closed:
            if program_policy is not None and program_policy != current.runtime.program_policy:
                raise SdkError(
                    "This event loop's local runtime already runs with program_timeout_seconds="
                    f"{_timeout_seconds(current.runtime.program_policy):g}; set program_timeout_seconds "
                    "before the loop's first local session, or leave the async with agents.local_runtime() "
                    f"block first to start a runtime with {_timeout_seconds(program_policy):g}"
                )
            if journals is not None and journals != current.runtime.journals:
                raise SdkError(
                    "This event loop's local runtime already runs with "
                    f"{_journals_text(current.runtime.journals)}; set journal_factory before the loop's first "
                    "local session, or leave the async with agents.local_runtime() block first to start a "
                    f"runtime with journal_factory={journals!r}"
                )
            return current.runtime
        runtime = _AgentsSdkLocalRuntime(
            dispose_idle_trees=True,
            program_policy=program_policy or DEFAULT_PROGRAM_EXECUTION_POLICY,
            journal_factory=journals,
        )
        released: asyncio.Future[None] = loop.create_future()
        closer = loop.create_task(
            _close_on_loop_shutdown(loop, runtime, released), name="agents-sdk-local-runtime-close"
        )
        _PROCESS_RUNTIMES[loop] = _LoopRuntime(runtime, closer, threading.current_thread(), released)
        return runtime


def _running_process_runtime() -> _AgentsSdkLocalRuntime | None:
    """Return the local runtime of the running event loop if it has one, without starting it.

    Outside an event loop, return ``None``.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return None
    with _PROCESS_RUNTIMES_LOCK:
        current = _PROCESS_RUNTIMES.get(loop)
    return current.runtime if current is not None and not current.runtime.closed else None


def _enter_process_runtime(
    *, program_policy: ProgramExecutionPolicy | None = None, journals: SessionJournals | None = None
) -> _AgentsSdkLocalRuntime:
    """Return the running event loop's local runtime as ``_process_runtime`` does, and count one more
    open ``async with agents.local_runtime()`` block on it.

    From then on the runtime closes no idle tree: the outermost block's exit closes them all.
    """
    runtime = _process_runtime(program_policy=program_policy, journals=journals)
    runtime.keep_idle_trees()
    loop = asyncio.get_running_loop()
    with _PROCESS_RUNTIMES_LOCK:
        _PROCESS_RUNTIMES[loop].open_blocks += 1
    return runtime


async def _exit_process_runtime() -> None:
    """Count one open block less, and close the runtime when the outermost block exits."""
    loop = asyncio.get_running_loop()
    with _PROCESS_RUNTIMES_LOCK:
        current = _PROCESS_RUNTIMES.get(loop)
        if current is not None and current.open_blocks > 1:
            current.open_blocks -= 1
            return
    await _close_process_runtime()


async def _close_process_runtime() -> None:
    """Close the running event loop's local runtime: every Session it holds, their subagents and
    their sandboxes. The next ``_process_runtime`` call starts a new runtime.
    """
    loop = asyncio.get_running_loop()
    with _PROCESS_RUNTIMES_LOCK:
        current = _PROCESS_RUNTIMES.pop(loop, None)
        if current is None:
            return
        entry = (loop, current)
        _CLOSING_RUNTIMES.append(entry)
    # Out of the registry before the close starts: a block entered while it runs starts a new runtime
    # instead of joining this one. Until the close ends, its closer still waits for ``released`` and the
    # exit hook still finds it in ``_CLOSING_RUNTIMES``, so loop shutdown and process exit close it.
    # A cancel of the block's exit (a second Ctrl-C, a timeout, a failing TaskGroup sibling) must not
    # stop the close partway: the close runs in its own task and is awaited to the end, then the cancel
    # goes on.
    closing = asyncio.ensure_future(current.runtime.close())
    cancel: asyncio.CancelledError | None = None
    try:
        while not closing.done():
            try:
                await asyncio.wait((closing,))
            except asyncio.CancelledError as error:
                cancel = error
    finally:
        with _PROCESS_RUNTIMES_LOCK:
            # The exit hook, or a reset after fork, may have taken it already.
            _CLOSING_RUNTIMES[:] = [other for other in _CLOSING_RUNTIMES if other is not entry]
        if not current.released.done():
            current.released.set_result(None)
    if cancel is not None:
        # The cancel goes on; an error of the close is kept as its cause.
        raise cancel from (None if closing.cancelled() else closing.exception())
    closing.result()


def _journals_text(journals: SessionJournals | None) -> str:
    return "no journal_factory, so its sessions are not saved" if journals is None else f"journal_factory={journals!r}"


def _timeout_seconds(policy: ProgramExecutionPolicy) -> float:
    return policy.elapsed_budget_ms / 1000


async def _close_on_loop_shutdown(
    loop: asyncio.AbstractEventLoop, runtime: _AgentsSdkLocalRuntime, released: asyncio.Future[None]
) -> None:
    # Shutting a loop down cancels its pending tasks. This one then closes the runtime's Sessions
    # and their sandboxes while the loop still runs. When the runtime is closed before that, it
    # ends without doing anything.
    # A loop closed without shutting down never cancels this task, and never runs it again.
    try:
        await released
    except asyncio.CancelledError:
        with _PROCESS_RUNTIMES_LOCK:
            current = _PROCESS_RUNTIMES.get(loop)
            if current is not None and current.runtime is runtime:
                del _PROCESS_RUNTIMES[loop]
        _warn_about_open_sessions(runtime)
        _warn_about_stopped_subagents(runtime)
        await _close_quietly(runtime)
        raise


def _warn_about_open_sessions(runtime: _AgentsSdkLocalRuntime) -> None:
    # A session left open, with a client or from `agent.start_session()`, or one still running a
    # turn nobody waits for, keeps its tree's sandbox until the loop shuts down.
    try:
        trees = runtime.open_sessions()
    except Exception:
        logger.exception("agents_sdk_local_runtime_sessions_unreadable")
        return
    if not trees:
        return
    session_ids = [session_id for tree in trees.values() for session_id in tree]
    logger.warning(
        "agents_sdk_local_runtime_closed_open_sessions",
        open_trees=len(trees),
        root_session_ids=list(trees),
        session_ids=session_ids,
        detail=f"the event loop shut down while {len(session_ids)} session(s) still had a sandbox, because a client "
        "or `agent.start_session()` held them or a turn still ran, so they were closed with it: "
        f"{', '.join(session_ids)}. Cancel each root session when you are done with it, with "
        "`await session.cancel()`, which ends its subagents too, and close each session client you opened",
    )


def _warn_about_stopped_subagents(runtime: _AgentsSdkLocalRuntime) -> None:
    # `agent.run` returns without waiting for subagents, so a script can end while one still works.
    try:
        running = runtime.running_subagents()
    except Exception:
        logger.exception("agents_sdk_local_runtime_subagents_unreadable")
        return
    if not running:
        return
    logger.warning(
        "agents_sdk_local_runtime_stopped_running_subagents",
        subagents=[
            {"name": link.name, "agent_path": link.agent_path, "session_id": str(link.session.id)} for link in running
        ],
        detail="the event loop shut down while these subagents still ran a turn, so they were stopped mid-turn. "
        "agent.run(...) does not wait for subagents: tell the root model to wait for the results it needs "
        "(its `wait` tool), or keep the event loop running until they finish",
    )


async def _close_quietly(runtime: _AgentsSdkLocalRuntime) -> None:
    try:
        await runtime.close()
    except Exception:
        logger.exception("agents_sdk_local_runtime_close_failed")


def _let_go_of_closed_loop_runtime(current: _LoopRuntime) -> None:
    # A loop closed without shutting down never ran its closer. The runtime's tasks belong to that
    # loop and never run again, so no other loop can close its Sessions; the registry lets it go.
    # The closer is then collected while pending, which the warning already reports.
    current.closer._log_destroy_pending = False  # type: ignore[attr-defined]
    logger.warning(
        "agents_sdk_local_runtime_loop_closed",
        detail="an event loop closed without shutting down; its local Sessions were not closed. "
        "Use asyncio.run, or cancel the loop's tasks before closing it",
    )


def _reset_after_fork() -> None:
    global _PROCESS_RUNTIMES_LOCK
    # The parent may have held the lock while it forked.
    _PROCESS_RUNTIMES_LOCK = threading.Lock()
    _PROCESS_RUNTIMES.clear()
    _CLOSING_RUNTIMES.clear()


def _close_process_runtimes_at_exit() -> None:
    # A loop that is never shut down, such as a notebook's, still holds its runtime at exit.
    with _PROCESS_RUNTIMES_LOCK:
        runtimes = [*_PROCESS_RUNTIMES.items(), *_CLOSING_RUNTIMES]
        _PROCESS_RUNTIMES.clear()
        _CLOSING_RUNTIMES.clear()
    for loop, current in runtimes:
        try:
            if loop.is_running():
                _close_on_running_loop_at_exit(loop, current)
                continue
            if loop.is_closed():
                _let_go_of_closed_loop_runtime(current)
                continue
            current.closer.cancel()
            loop.run_until_complete(asyncio.gather(current.closer, return_exceptions=True))
        except Exception:
            logger.exception("agents_sdk_local_runtime_close_failed")


def _close_on_running_loop_at_exit(loop: asyncio.AbstractEventLoop, current: _LoopRuntime) -> None:
    # A daemon thread stops with the process, so its loop closes the runtime now. A loop in a
    # non-daemon thread may still have work to do: it keeps its runtime and closes it when it shuts
    # down, though a close that needs a worker thread then fails, logged, as the pools have stopped.
    if not current.thread.daemon:
        return
    closing = asyncio.run_coroutine_threadsafe(_cancel_closer(current.closer), loop)
    try:
        closing.result(timeout=_EXIT_CLOSE_TIMEOUT_SECONDS)
    except TimeoutError:
        closing.cancel()
        logger.warning(
            "agents_sdk_local_runtime_loop_running_at_exit",
            thread=current.thread.name,
            detail="the process exited while an event loop still ran in a daemon thread, and its local Sessions "
            f"did not close within {_EXIT_CLOSE_TIMEOUT_SECONDS:g} s. Shut the loop down before the process exits",
        )


async def _cancel_closer(closer: asyncio.Task[None]) -> None:
    closer.cancel()
    await asyncio.gather(closer, return_exceptions=True)


def _register_exit_close() -> None:
    # Closing a sandbox can use worker threads, and the thread pools stop before ``atexit``
    # handlers run. Threading's own exit hooks run before that, last registered first, so this
    # hook must come after the thread pools' own, which their module registers on import.
    register = getattr(threading, "_register_atexit", None)
    if register is None:
        atexit.register(_close_process_runtimes_at_exit)
        return
    try:
        register(_close_process_runtimes_at_exit)
    except RuntimeError:
        # The interpreter is already shutting down.
        atexit.register(_close_process_runtimes_at_exit)


_register_exit_close()
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_after_fork)


async def _create_local_session(
    assembly: assemble.AgentAssembly,
    *,
    history: list[HistoryImportEntry] | None = None,
    session_id: str,
    session_inputs: Mapping[str, contracts.SessionInput] | None = None,
    completion_provider: CompletionProvider | None = None,
    file_policy: SessionFilePolicy = DEFAULT_SESSION_FILE_POLICY,
    initial_turn: InitialTurn | None = None,
    client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
) -> SessionClient:
    """Start a Session whose client owns the manager and shared resource lifetime.

    Its program time budget is that of the event loop's runtime once it has started, else the default.
    """
    loop_runtime = _running_process_runtime()
    runtime = _AgentsSdkLocalRuntime(
        completion_provider=completion_provider,
        file_policy=file_policy,
        program_policy=loop_runtime.program_policy if loop_runtime is not None else DEFAULT_PROGRAM_EXECUTION_POLICY,
    )
    try:
        return await runtime.create_session(
            assembly,
            session_id=session_id,
            history=history,
            session_inputs=session_inputs,
            close_runtime_with_client=True,
            initial_turn=initial_turn,
            client_tools=client_tools,
        )
    except BaseException:
        await runtime.close()
        raise


@dataclass(frozen=True, slots=True)
class _ServedSkills:
    catalog: list[MaterializedSkillDefinition]
    host: SkillHost | None


def _prepare_skill_files(assembly: assemble.AgentAssembly) -> sandbox_skills.SandboxSkillFiles | None:
    """Prepare the tree's skill files before anything opens, or ``None`` when the tree has no skills.

    Local skills are validated here. Registry skills are fetched by the sandbox write itself.
    """

    if assembly.skills is None:
        return None
    return sandbox_skills.SandboxSkillFiles.prepare(
        assembly.skills.skills,
        resolver=_SKILL_FILE_RESOLVER,
        subagent_skills=assembly.skills.subagents,
        workspace=assembly.skills.workspace,
        discovery=assembly.skills.discovery is not None,
    )


async def _serve_root_skills(
    files: sandbox_skills.SandboxSkillFiles | None, sandbox: WorkflowSandboxResource
) -> _ServedSkills:
    if files is None:
        return _ServedSkills(catalog=[], host=None)
    catalog = await files.provision(sandbox)
    return _ServedSkills(
        catalog=catalog,
        host=sandbox_skills.SandboxSkillHost(sandbox, resolver=files.resolver, catalog=catalog, writer=sandbox),
    )


def _child_large_output(
    definition: SessionDefinition, root: LocalSessionWorkspace, share: _RootShare | None
) -> sandbox_assembly.LargeOutputComposition:
    """Keep the root's policy, and write a child's large tool results into a folder of its own."""

    if share is None or root.large_output.mode != "filesystem":
        return sandbox_assembly.LargeOutputComposition(policy=root.large_output, filesystem=None)
    if definition.session_id is None:
        raise ValueError("Local child definition requires a Session identity")
    return sandbox_assembly.compose_large_output(share.sandbox, root.large_output, session_id=definition.session_id)


async def _serve_child_skills(
    definition: SessionDefinition, share: _RootShare | None
) -> tuple[SessionDefinition, SkillHost | None]:
    """Serve a child's skills from its root's sandbox.

    A child that inherits already has its parent's catalog and reads through the root's host. A
    child with its own skills writes them into a folder of its own in the root's sandbox. A tree
    without skills has no skill host, and the Harness refuses skill sources without one.
    """

    sources = definition.agent_config.skill_sources
    if share is None:
        return definition, None
    if not sources or share.skill_files is None:
        return definition, share.skill_host
    if definition.session_id is None:
        raise ValueError("Local child definition requires a Session identity")
    catalog = await share.skill_files.write_declared(share.sandbox, sources, session_id=definition.session_id)
    definition = definition.model_copy(
        update={"agent_config": sandbox_skills.with_skill_catalog(definition.agent_config, catalog)}
    )
    return definition, share.skill_host


@asynccontextmanager
async def _local_registry_client() -> AsyncIterator[Mistral]:
    registry = local_mistral_client("AI Registry skills")
    try:
        yield registry.client
    finally:
        await registry.http.aclose()


# One resolver for the process: its name keeps it, so every Session registers this same object.
_SKILL_FILE_RESOLVER = sandbox_skills.SkillFileResolver(
    sandbox_skills.LOCAL_SKILL_FILE_RESOLVER, _local_registry_client
)


__all__: list[str] = []
