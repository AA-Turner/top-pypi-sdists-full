"""Compile SDK-owned sandbox authoring into Vibe Workflow sandbox resources."""

from __future__ import annotations

import hashlib
import posixpath
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, cast, get_args
from uuid import uuid4

import structlog
import temporalio.exceptions
import temporalio.workflow
from pydantic import JsonValue, TypeAdapter

from mistralai.vibe.harness.app_server.session import SandboxConfig
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.hosts.processes import TransportBackgroundProcessGateway
from mistralai.vibe.harness.runtime.hosts.workflows import (
    BashkitNetworkDefinition,
    BashkitSandboxDefinition,
    CustomSandboxDefinition,
    LocalDockerSandboxDefinition,
    LocalHostSandboxDefinition,
    NoSandboxDefinition,
    SandboxHookDefinition,
    SandboxProvisioningStep,
    WorkflowBackgroundProcessTransport,
    WorkflowSandboxContinuation,
    WorkflowSandboxDefinition,
    WorkflowSandboxHostPort,
    WorkflowSandboxResource,
    workflow_is_replaying,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox import (
    WorkflowSandboxExecuteRequest,
    WorkflowSandboxExecuteResult,
    WorkflowSandboxReadFileRequest,
    WorkflowSandboxReadFileResult,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_definitions import (
    SandboxDriver,
    SandboxProvisioningIdentity,
    WorkflowSandboxHookPort,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import (
    HARNESS_FILES_ROOT,
    SandboxFilesFilesystemHandler,
    WorkflowSandboxWriteFilesRequest,
    WorkflowSandboxWriteFilesResult,
    normalized_sandbox_root,
)
from mistralai.vibe.harness.runtime.session.configuration import DeclaredBashMaxTimeout
from mistralai.vibe.harness.runtime.tools import (
    BackgroundProcessToolHandler,
    BuiltinToolHandler,
    build_background_process_tool_handlers,
)
from mistralai.vibe.harness.runtime.tools.handler import FilesystemHandler
from mistralai.vibe_agents.sdk.app.config import KOYEB_SANDBOX_SETUP_FRESH_SANDBOX_ATTEMPTS
from mistralai.vibe_agents.sdk.authoring import contracts, session_input

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.app.worker.sandbox_lifecycle import SandboxLifecycle
    from mistralai.vibe_agents.sdk.sandbox.koyeb import KoyebSandboxDriver

logger = structlog.get_logger(__name__)
_JSON_OBJECT = TypeAdapter(dict[str, JsonValue])

type _SandboxHookPoint = Literal["on_create", "on_destroy"]
_SANDBOX_HOOK_POINTS: tuple[_SandboxHookPoint, ...] = get_args(_SandboxHookPoint.__value__)


class SandboxHookFailedError(RuntimeError):
    """A sandbox hook's on_create raised in a Workflow-hosted Session, which must fail rather than retry."""


@dataclass(frozen=True, slots=True)
class BackgroundProcessSessionComposition:
    handler: BackgroundProcessToolHandler | None
    runtime_builtin_tools: dict[core_protocol.RuntimeBuiltinToolName, BuiltinToolHandler]


@dataclass(frozen=True, slots=True)
class LargeOutputComposition:
    policy: core_protocol.LargeOutputPolicy
    filesystem: FilesystemHandler | None


class AgentsSdkSandbox(WorkflowSandboxHostPort):
    """Bridge SDK-owned authoring into Vibe-owned sandbox resources."""

    def __init__(
        self,
        definition: WorkflowSandboxDefinition,
        authored: contracts.Sandbox,
        *,
        config: SandboxConfig | None,
        proxy_identity: dict[str, str] | None = None,
        terminal_hook_failures: bool = False,
        lifecycle: SandboxLifecycle | None = None,
    ) -> None:
        self.definition = definition
        self.config = config
        self._authored = authored
        self._proxy_identity = proxy_identity
        self._terminal_hook_failures = terminal_hook_failures
        self._lifecycle = lifecycle
        self._custom: contracts.CustomSandbox | None = None
        self._koyeb_driver: KoyebSandboxDriver | None = None
        self._session_inputs: Mapping[str, JsonValue] = {}

    def bind_session_inputs(self, session_inputs: Mapping[str, JsonValue], *, sandbox_is_live: bool) -> None:
        """Bind the inputs sandbox hooks receive, checking them against every declaration.

        Raises ``ValueError`` when a declared input is missing or does not rebuild into
        its class: sandbox hooks are SDK-owned and absent from the Agent Configuration
        the Harness validates. A live sandbox already ran ``on_create``, so its inputs
        are not checked again: checking them against changed classes could strand it.
        """

        if not sandbox_is_live:
            for consumer, declarations in sandbox_hook_session_input_consumers(self._authored):
                session_input.rebuild_session_inputs(consumer, declarations, session_inputs)
        self._session_inputs = session_inputs

    @property
    def supports_background_processes(self) -> bool:
        """Whether the provider can run the bundled process helper without restrictions."""

        return self._authored.supports_background_processes

    async def on_session_start(self) -> None:
        if isinstance(self._authored, contracts.CustomSandbox):
            await self._authored.on_session_start()

    async def on_session_end(self) -> None:
        if isinstance(self._authored, contracts.CustomSandbox):
            await (self._custom or self._authored).on_session_end()

    async def open(
        self,
        definition: CustomSandboxDefinition,
        restored_state: dict[str, JsonValue] | None,
    ) -> SandboxDriver | None:
        del definition
        if isinstance(self._authored, contracts.MistralSandbox):
            from mistralai.vibe_agents.sdk.sandbox.koyeb import KoyebSandboxDriver  # noqa: PLC0415

            self._koyeb_driver = KoyebSandboxDriver(
                self._authored,
                restored_state,
                proxy_identity=self._proxy_identity,
            )
            if restored_state is not None and self._lifecycle is not None:
                self._lifecycle.reattach(self._koyeb_driver)
            return self._koyeb_driver
        if not isinstance(self._authored, contracts.CustomSandbox):
            return None
        custom = (
            self._authored
            if restored_state is None
            else cast(
                contracts.CustomSandbox,
                contracts.deserialize_unified(
                    restored_state,
                    expected=contracts.CustomSandbox,
                    default_sandbox_policy=self._authored.policy,
                ),
            )
        )
        self._custom = custom
        return _ExecutableSandboxDriver(custom) if custom.is_executable else None

    async def prepare_capability_sandbox_access(self) -> None:
        if self._koyeb_driver is not None:
            await self._koyeb_driver.ensure_proxy_credentials()

    def provisioning_steps(self) -> tuple[SandboxProvisioningStep, ...]:
        """Build the provider steps that complete a new managed sandbox."""

        if not isinstance(self._authored, contracts.MistralSandbox):
            return ()
        steps: list[SandboxProvisioningStep] = []
        if self._authored.header_bindings:

            async def configure_proxy(sandbox: WorkflowSandboxHookPort) -> None:
                del sandbox
                current = self._koyeb_driver
                if current is None:
                    raise RuntimeError("Koyeb provisioning driver is unavailable")
                await current.configure_new_proxy()

            steps.append(SandboxProvisioningStep(stage="proxy", run=configure_proxy))
        if self._authored.setup_script:

            async def run_setup_script(sandbox: WorkflowSandboxHookPort) -> None:
                del sandbox
                current = self._koyeb_driver
                if current is None:
                    raise RuntimeError("Koyeb provisioning driver is unavailable")
                await current.run_setup_script()

            steps.append(
                SandboxProvisioningStep(
                    stage="setup",
                    run=run_setup_script,
                    fresh_sandbox_attempts=KOYEB_SANDBOX_SETUP_FRESH_SANDBOX_ATTEMPTS,
                )
            )
        lifecycle = self._lifecycle
        if lifecycle is not None:

            async def provision_workspace(sandbox: WorkflowSandboxHookPort) -> None:
                del sandbox
                current = self._koyeb_driver
                if current is None:
                    raise RuntimeError("Koyeb provisioning driver is unavailable")
                await lifecycle.provision(current)

            steps.append(
                SandboxProvisioningStep(
                    stage="workspace",
                    run=provision_workspace,
                    fresh_sandbox_attempts=lifecycle.workspace_attempts,
                )
            )
        return tuple(steps)

    async def on_hooks_create(
        self,
        hooks: tuple[SandboxHookDefinition, ...],
        sandbox: WorkflowSandboxHookPort,
    ) -> None:
        context = _sandbox_callback_context(sandbox)
        for hook in _hooks_from_definitions(hooks):
            try:
                await hook.on_create(context, **self._hook_session_inputs(hook, "on_create"))
            except Exception as error:
                # A local Session raises the hook's own exception.
                if not self._terminal_hook_failures:
                    raise
                # A cancel must still cancel the Workflow. A nondeterminism error is
                # recoverable by redeploying, so the Workflow task must retry.
                if temporalio.exceptions.is_cancelled_exception(error):
                    raise
                if isinstance(error, temporalio.workflow.NondeterminismError):
                    raise
                # The message reaches the Workflow output and the control plane, so it names only
                # identifiers; the worker logs the full error when it ends the Session.
                raise SandboxHookFailedError(
                    f"Sandbox hook {type(hook).__name__}.on_create failed with {type(error).__name__}"
                ) from error

    async def on_hooks_destroy(
        self,
        hooks: tuple[SandboxHookDefinition, ...],
        sandbox: WorkflowSandboxHookPort,
    ) -> None:
        context = _sandbox_callback_context(sandbox)
        for hook in reversed(_hooks_from_definitions(hooks)):
            try:
                await hook.on_destroy(context, **self._hook_session_inputs(hook, "on_destroy"))
            except Exception as error:
                # Cleanup continues for the other hooks. Hooks may run in Workflow code, which replays.
                if not workflow_is_replaying():
                    logger.warning("Sandbox hook on_destroy failed", hook=type(hook).__name__, exc_info=error)

    def _hook_session_inputs(self, hook: contracts.SandboxHook, point: _SandboxHookPoint) -> dict[str, object]:
        declarations = _sandbox_hook_declarations(hook, point)
        if not declarations:
            return {}
        return session_input.rebuild_session_inputs(
            _sandbox_hook_label(hook, point), declarations, self._session_inputs
        )


class _ExecutableSandboxDriver(SandboxDriver):
    def __init__(self, sandbox: contracts.CustomSandbox) -> None:
        self._sandbox = sandbox
        self._workspace = sandbox.workspace

    @property
    def workspace(self) -> str:
        return self._workspace

    @property
    def state(self) -> dict[str, JsonValue]:
        return _JSON_OBJECT.validate_python(self._sandbox.serialize_unified())

    async def create(self, identity: SandboxProvisioningIdentity) -> None:
        del identity
        self._workspace = await self._sandbox.create()

    async def delete(self) -> None:
        await self._sandbox.delete()

    async def execute(
        self,
        request: WorkflowSandboxExecuteRequest,
    ) -> WorkflowSandboxExecuteResult:
        return await self._sandbox.execute(request)

    async def read_file(
        self,
        request: WorkflowSandboxReadFileRequest,
    ) -> WorkflowSandboxReadFileResult:
        return await self._sandbox.read_file(request)

    def resolve_files_root(self, namespace: str) -> None:
        normalized_sandbox_root(namespace)
        return None

    async def write_files(self, request: WorkflowSandboxWriteFilesRequest) -> WorkflowSandboxWriteFilesResult:
        written = await self._sandbox.write_files(request)
        # Skill and hook paths are joined to this root, so author code must return a real sandbox folder.
        return written.model_copy(update={"root": normalized_sandbox_root(written.root)})


def _sandbox_callback_context(sandbox: WorkflowSandboxHookPort) -> contracts.SandboxCallbackContext:
    """Give lifecycle hooks the sandbox API an authored Hook gets."""

    hook_sandbox = contracts.HookSandbox()
    hook_sandbox.bind(sandbox, inline_writes=temporalio.workflow.in_workflow())
    return contracts.SandboxCallbackContext(hook_sandbox)


def compile_sandbox(
    authored: contracts.Sandbox,
    *,
    proxy_identity: dict[str, str] | None = None,
    session_id: str | None = None,
    terminal_hook_failures: bool = False,
    lifecycle: SandboxLifecycle | None = None,
) -> AgentsSdkSandbox:
    """Compile SDK-owned sandbox authoring into one Vibe resource definition.

    ``terminal_hook_failures`` turns an ``on_create`` error into ``SandboxHookFailedError``,
    which a Workflow-hosted Session maps to a terminal failure instead of retrying its
    Workflow task. Without it, the hook's own exception propagates.
    """

    hooks = tuple(
        SandboxHookDefinition(state=_JSON_OBJECT.validate_python(hook.serialize_unified())) for hook in authored.hooks
    )
    match authored:
        case contracts.NoSandbox():
            definition: WorkflowSandboxDefinition = NoSandboxDefinition()
        case contracts.MistralSandbox():
            definition = CustomSandboxDefinition(
                state=_JSON_OBJECT.validate_python(authored.serialize_unified()),
                executable=True,
                hooks=hooks,
            )
        case contracts.LocalDockerSandbox():
            definition = LocalDockerSandboxDefinition(
                network="none" if authored.network.mode == "none" else "all",
                image=authored.image,
                shell=authored.shell,
                default_exec_timeout_seconds=authored.default_exec_timeout_seconds,
                setup_script=authored.setup_script,
                setup_script_timeout_seconds=authored.setup_script_timeout_seconds,
                hooks=hooks,
            )
        case contracts.DangerousLocalSandbox():
            definition = LocalHostSandboxDefinition(
                shell=authored.shell,
                default_exec_timeout_seconds=authored.default_exec_timeout_seconds,
                workspace=authored.workspace,
                delete_on_cleanup=authored.delete_on_cleanup,
                # A Session's served files keep their paths when a new process reopens it.
                instance_id=None if session_id is None else hashlib.sha256(session_id.encode()).hexdigest()[:20],
                hooks=hooks,
            )
        case contracts.BashkitSandbox():
            definition = BashkitSandboxDefinition(
                instance_id=_session_instance_id(authored.instance_id, session_id),
                network=_bashkit_network(authored),
                hooks=hooks,
            )
        case contracts.CustomSandbox():
            definition = CustomSandboxDefinition(
                state=_JSON_OBJECT.validate_python(authored.serialize_unified()),
                executable=authored.is_executable,
                delete_on_cleanup=authored.delete_on_cleanup,
                hooks=hooks,
            )
        case _:
            raise TypeError(f"Unified Harness does not support sandbox {type(authored).__name__}")
    config = (
        None
        if isinstance(authored, contracts.NoSandbox)
        else SandboxConfig(
            type="managed" if authored.is_executable else "local",
            options={"agents_sdk_state": _JSON_OBJECT.validate_python(authored.serialize_unified())},
        )
    )
    return AgentsSdkSandbox(
        definition,
        authored,
        config=config,
        proxy_identity=proxy_identity,
        terminal_hook_failures=terminal_hook_failures,
        lifecycle=lifecycle,
    )


def needs_sandbox_at_open(authored: contracts.Sandbox) -> bool:
    """Whether a Session must create its sandbox before the first model completion.

    Reads only the authored configuration, so it answers the same on every replay
    and after Continue-As-New. Every Session is eager until lazy creation ships
    with a provisioning progress surface.
    """

    del authored
    return True


async def open_sandbox_resource(
    sandbox_host: AgentsSdkSandbox,
    *,
    bash_max_timeout: DeclaredBashMaxTimeout,
    restored: WorkflowSandboxContinuation | None = None,
    provisioning_timeout_seconds: float | None = None,
) -> WorkflowSandboxResource:
    """Compose a root resource with its provider steps, without provisioning it."""

    return await WorkflowSandboxResource.compose(
        sandbox_host.definition,
        config=sandbox_host.config,
        restored=restored,
        host=sandbox_host,
        bash_max_timeout=bash_max_timeout,
        provisioning_timeout_seconds=provisioning_timeout_seconds,
        provisioning_steps=sandbox_host.provisioning_steps(),
    )


def sandbox_hook_session_input_consumers(
    authored: contracts.Sandbox,
) -> list[tuple[str, Mapping[str, type[session_input.SessionInput]]]]:
    """Name each sandbox hook point with the Session inputs its signature declares."""

    # Hooks run only once a sandbox is provisioned: NoSandbox and a non-executable
    # CustomSandbox never fire them, so their declarations require nothing.
    if not authored.is_executable:
        return []
    return [
        (
            _sandbox_hook_label(hook, point),
            _sandbox_hook_declarations(hook, point),
        )
        for hook in authored.hooks
        for point in _SANDBOX_HOOK_POINTS
    ]


def _sandbox_hook_declarations(
    hook: contracts.SandboxHook, point: _SandboxHookPoint
) -> Mapping[str, type[session_input.SessionInput]]:
    return session_input.method_session_inputs(contracts.SandboxHook, hook, point)


def _sandbox_hook_label(hook: contracts.SandboxHook, point: _SandboxHookPoint) -> str:
    return f"sandbox hook {type(hook).__name__}.{point}"


def build_background_process_handler(
    sandbox: WorkflowSandboxResource,
) -> BackgroundProcessToolHandler | None:
    """Build process tooling only for sandboxes with an operating-system shell."""

    if isinstance(
        sandbox.command_environment,
        (
            core_protocol.DisabledCommandEnvironment,
            core_protocol.InMemoryBashCommandEnvironment,
        ),
    ):
        return None
    return BackgroundProcessToolHandler(TransportBackgroundProcessGateway(WorkflowBackgroundProcessTransport(sandbox)))


def compose_background_process_session(
    sandbox: WorkflowSandboxResource,
    sandbox_host: AgentsSdkSandbox,
    *,
    enabled: bool = True,
) -> BackgroundProcessSessionComposition:
    """Compose sandbox tools with process support when the Session permits it."""

    handler = (
        build_background_process_handler(sandbox) if enabled and sandbox_host.supports_background_processes else None
    )
    runtime_builtin_tools = dict(sandbox.handlers)
    if handler is not None:
        runtime_builtin_tools.update(build_background_process_tool_handlers(handler))
    return BackgroundProcessSessionComposition(
        handler=handler,
        runtime_builtin_tools=runtime_builtin_tools,
    )


def default_large_output_policy(sandbox: WorkflowSandboxResource) -> core_protocol.LargeOutputPolicy:
    """Save an oversized tool result as a sandbox file the model can read back.

    A sandbox that cannot hold files keeps the Harness default: the result is truncated in place.
    """

    if sandbox.resolve_files_root(HARNESS_FILES_ROOT) is None:
        return core_protocol.DisabledLargeOutputPolicy()
    return core_protocol.FilesystemLargeOutputPolicy()


def compose_large_output(
    sandbox: WorkflowSandboxResource,
    policy: core_protocol.LargeOutputPolicy,
    *,
    session_id: str,
) -> LargeOutputComposition:
    """Bind ``policy`` to a writer that keeps each Session's files apart in a shared sandbox."""

    if policy.mode != "filesystem":
        return LargeOutputComposition(policy=policy, filesystem=None)
    return LargeOutputComposition(
        policy=policy,
        filesystem=SandboxFilesFilesystemHandler(sandbox, root=posixpath.join(HARNESS_FILES_ROOT, session_id)),
    )


def _hooks_from_definitions(
    hooks: tuple[SandboxHookDefinition, ...],
) -> list[contracts.SandboxHook]:
    return [
        cast(
            contracts.SandboxHook,
            contracts.deserialize_unified(
                cast(dict[str, object], definition.state),
                expected=contracts.SandboxHook,
            ),
        )
        for definition in hooks
    ]


def _bashkit_network(authored: contracts.BashkitSandbox) -> BashkitNetworkDefinition | None:
    # Bashkit refuses every connection when it gets no network, and matches each allowed entry as
    # a URL prefix, scheme included. An allowed host is reached over HTTPS only, so nothing the
    # sandbox sends to it, a bound header included, travels in clear text.
    network = authored.network
    if network.mode == "none":
        return None
    if network.mode == "all":
        return BashkitNetworkDefinition(allow_all=True, block_private_ips=authored.block_private_ips)
    return BashkitNetworkDefinition(
        allow=tuple(f"https://{host}" for host in network.hosts),
        block_private_ips=authored.block_private_ips,
    )


def _session_instance_id(instance_id: str | None, session_id: str | None) -> str:
    # One authored sandbox serves every Session of its agent. Bashkit keys its host folders by
    # instance, so each Session gets its own: otherwise one Session's close deletes another's files.
    if session_id is None:
        return instance_id or str(uuid4())
    session_key = hashlib.sha256(session_id.encode()).hexdigest()
    if instance_id is None:
        # Named after the Session alone, so a new process that reopens it gets the same folders.
        return session_key[:20]
    return f"{instance_id}-{session_key[:12]}"


__all__ = [
    "AgentsSdkSandbox",
    "BackgroundProcessSessionComposition",
    "SandboxHookFailedError",
    "build_background_process_handler",
    "compile_sandbox",
    "compose_background_process_session",
    "needs_sandbox_at_open",
    "open_sandbox_resource",
    "sandbox_hook_session_input_consumers",
]
