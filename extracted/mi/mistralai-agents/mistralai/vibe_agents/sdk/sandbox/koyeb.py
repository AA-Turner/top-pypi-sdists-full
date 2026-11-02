"""Koyeb-backed Unified Harness sandbox driver and activities."""

import asyncio
import base64
import gzip
import hashlib
import math
import shlex
import time
import uuid
import warnings
from collections.abc import Mapping
from contextlib import suppress
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Annotated, Any, Literal, Protocol, Self, cast
from uuid import UUID

import httpx
import temporalio.workflow
from pydantic import BaseModel, Field, JsonValue, SecretStr, model_validator
from temporalio.exceptions import ApplicationError

import mistralai.workflows as workflows
from mistralai.vibe.harness.runtime.agents.models import RootSandboxReference
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox import (
    SANDBOX_EXECUTE_ACTIVITY_TIMEOUT,
    WorkflowSandboxExecuteRequest,
    WorkflowSandboxExecuteResult,
    WorkflowSandboxReadFileRequest,
    WorkflowSandboxReadFileResult,
    WorkflowSandboxUnavailableError,
    require_sandbox_execute_timeout,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_definitions import (
    DEFAULT_WORKSPACE,
    CustomSandboxDefinition,
    JsonObject,
    ReadySandbox,
    SandboxDriver,
    SandboxProvisioningIdentity,
    WorkflowSandboxContinuation,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import (
    FileSource,
    ResolvedFile,
    WorkflowSandboxWriteFilesRequest,
    WorkflowSandboxWriteFilesResult,
    files_to_tar,
    normalized_sandbox_root,
    resolve_file_source,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_resources import WorkflowSandboxResource
from mistralai.vibe.harness.runtime.http import build_ssl_context
from mistralai.vibe.harness.runtime.model import RuntimeModel
from mistralai.vibe.harness.runtime.session.configuration import DeclaredBashMaxTimeout
from mistralai.vibe_agents.sdk.app.config import (
    DEFAULT_SESSION_LIFETIME_SECONDS,
    KOYEB_SANDBOX_CREATE_ATTEMPT_TIMEOUT,
    KOYEB_SANDBOX_CREATE_MAX_ATTEMPTS,
    KOYEB_SANDBOX_SETUP_ACTIVITY_TIMEOUT,
    KoyebApiAccess,
    KoyebSandboxRuntimeSettings,
    SandboxProxySettings,
)
from mistralai.vibe_agents.sdk.app.worker.heartbeat import heartbeat_while_running
from mistralai.vibe_agents.sdk.authoring import contracts, determinism
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

from . import koyeb_secrets
from .bootstrap import (
    SandboxBootstrapError,
    SandboxProxyBootstrapClient,
)
from .file_materialization import FileMaterialization, file_materialization_from_source
from .koyeb_proxy import (
    build_github_proxy_sandbox_setup,
    build_github_proxy_token_renewal,
    build_github_proxy_token_renewal_command,
)
from .proxy_integrations import (
    GitHubProxyConfig,
    SandboxProxyIntegration,
    SecretInjectionProxyConfig,
    proxy_integrations,
)
from .proxy_lifecycle import (
    SandboxProxyEffects,
    SandboxProxyIdentity,
    SandboxProxyLifecycle,
)

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.assembly.sandbox import AgentsSdkSandbox

_PROXY_SETUP_TIMEOUT_SECONDS = 60
_SANDBOX_PROXY_BOOTSTRAP_ACTIVITY_PATCH = "agents-sdk-koyeb-sandbox-proxy-bootstrap-v2"
# This path is the producer contract defined by
# sandbox_proxy_protocol.bootstrap.secret_injection.SECRET_INJECTION_ENV_FILE.
_WORKSPACE_PROXY_ENV_FILE = "/tmp/sandbox-proxy/secret-injection.env"  # noqa: S108
# The file tools reach only the workspace and /tmp, so written files live under /tmp.
_FILES_ROOT = "/tmp/vibe-harness-files"  # noqa: S108
_KOYEB_API_NAME_MAX_LENGTH = 64
# The Koyeb SDK derives the app name from the sandbox name as
# f"sandbox-app-{name}-{int(time.time())}", so the name we pass must leave room for
# that wrapper or the API rejects the app name as too long.
_KOYEB_SDK_APP_NAME_OVERHEAD = len("sandbox-app-") + 1 + 10
_SANDBOX_NAME_MAX_LENGTH = _KOYEB_API_NAME_MAX_LENGTH - _KOYEB_SDK_APP_NAME_OVERHEAD
# Commands run in the workspace, which an arbitrary image does not provide.
_KOYEB_ENSURE_WORKSPACE_COMMAND = f"mkdir -p {shlex.quote(DEFAULT_WORKSPACE)}"
_KOYEB_BASIC_READINESS_PROBE = ("echo ok", "ok")
_KOYEB_DOCKER_READINESS_PROBE = (
    "test -S /var/run/docker.sock && docker info >/dev/null && echo docker-ok",
    "docker-ok",
)
_KOYEB_DOCKER_DAEMON_START_COMMAND = "sudo -n start-dockerd"
# Koyeb deployment states after which the sandbox never becomes ready.
_KOYEB_SETUP_SCRIPT_HEARTBEAT_TIMEOUT = timedelta(seconds=60)
_KOYEB_FAILED_DEPLOYMENT_STATUSES = frozenset({"ERROR", "ERRORING"})
_KOYEB_FILE_NOT_FOUND_EXIT_CODE = 44
_KOYEB_READ_FILE_PROGRAM = f"""
import base64, pathlib, sys
path = pathlib.Path(sys.argv[1])
limit = int(sys.argv[2])
try:
    data = path.read_bytes()
except FileNotFoundError:
    sys.exit({_KOYEB_FILE_NOT_FOUND_EXIT_CODE})
assert len(data) <= limit, 'file exceeds max_bytes'
print(base64.b64encode(data).decode('ascii'))
"""


class KoyebSandboxProxyDefinition(RuntimeModel):
    integrations: tuple[SandboxProxyIntegration, ...]

    @model_validator(mode="before")
    @classmethod
    def read_legacy_github_config(cls, data: object) -> object:
        """Accept proxy definitions persisted before integrations were introduced."""

        if not isinstance(data, Mapping) or "integrations" in data:
            return data
        legacy_fields = {
            "repo_whitelist",
            "all_accessible_repos",
            "ttl_seconds",
            "github_host",
        }
        if not any(field in data for field in legacy_fields):
            return data
        promoted = {key: value for key, value in data.items() if key not in legacy_fields}
        promoted["integrations"] = (
            {
                "type": "github",
                "repo_whitelist": data.get("repo_whitelist", ()),
                "all_accessible_repos": data.get("all_accessible_repos", False),
                "ttl_seconds": data.get("ttl_seconds", 3600),
                "host": data.get("github_host", "github.com"),
            },
        )
        return promoted


class _LegacyKoyebSandboxProxyDefinition(RuntimeModel):
    """Payload shape used by proxy activities scheduled before the bootstrap migration."""

    repo_whitelist: tuple[str, ...] = ()
    all_accessible_repos: bool = False
    ttl_seconds: Annotated[int, Field(gt=5 * 60)] = 3600
    github_host: str = "github.com"


_EGRESS_POLICY_REGIONS = frozenset({"nl-north-1"})


class KoyebSandboxDefinition(RuntimeModel):
    """Serializable Koyeb configuration derived from SDK-owned authoring."""

    type: Literal["koyeb"] = "koyeb"
    image: str
    instance_type: str
    region: str
    name_prefix: str
    ttl_seconds: Annotated[int, Field(ge=60)] = DEFAULT_SESSION_LIFETIME_SECONDS
    idle_timeout_seconds: Annotated[int, Field(ge=0)] = 0
    default_exec_timeout_seconds: Annotated[int, Field(ge=1)] = 30
    privileged: bool = False
    docker_daemon_enabled: bool = False
    docker_daemon_network_mode: str = "auto"
    enable_light_sleep: bool = True
    setup_script: str | None = None
    # The setup activity's deadline must outlast the script's own timeout.
    setup_script_timeout_seconds: Annotated[
        int, Field(ge=1, le=int(KOYEB_SANDBOX_SETUP_ACTIVITY_TIMEOUT.total_seconds()))
    ] = 300
    readiness_max_retries: Annotated[int, Field(ge=1)] = 10
    readiness_interval_seconds: Annotated[float, Field(gt=0)] = 2.0
    readiness_probe_timeout_seconds: Annotated[int, Field(ge=1)] = 5
    wait_ready_timeout_seconds: Annotated[int, Field(ge=1)] = 300
    enable_mesh: bool = False
    egress: contracts.EgressPolicy = contracts.EgressPolicy()
    pre_provisioned_sandbox_id: str | None = None
    proxy: KoyebSandboxProxyDefinition | None = None

    @model_validator(mode="after")
    def _validate_egress_region(self) -> Self:
        if self.egress.mode == "allow_all" or self.region in _EGRESS_POLICY_REGIONS:
            return self
        supported = ", ".join(sorted(_EGRESS_POLICY_REGIONS))
        raise ValueError(
            f"This network policy is not supported in region {self.region!r}; it is supported "
            f"only in {supported}. Pass network=Network.all() or a supported region."
        )

    @classmethod
    def from_authored(cls, authored: contracts.MistralSandbox) -> "KoyebSandboxDefinition":
        proxy = (
            KoyebSandboxProxyDefinition(integrations=proxy_integrations(authored.header_bindings))
            if authored.header_bindings
            else None
        )
        return cls(
            image=authored.image,
            instance_type=authored.instance_type,
            region=authored.region,
            name_prefix=authored.name_prefix,
            ttl_seconds=authored.ttl_seconds,
            idle_timeout_seconds=authored.idle_timeout_seconds,
            default_exec_timeout_seconds=authored.default_exec_timeout_seconds,
            privileged=authored.privileged,
            docker_daemon_enabled=authored.docker_daemon_enabled,
            docker_daemon_network_mode=authored.docker_daemon_network_mode,
            enable_light_sleep=authored.enable_light_sleep,
            setup_script=authored.setup_script,
            setup_script_timeout_seconds=authored.setup_script_timeout_seconds,
            readiness_max_retries=authored.readiness_max_retries,
            readiness_interval_seconds=authored.readiness_interval_seconds,
            readiness_probe_timeout_seconds=authored.readiness_probe_timeout_seconds,
            wait_ready_timeout_seconds=authored.wait_ready_timeout_seconds,
            enable_mesh=authored.enable_mesh,
            egress=authored.egress_policy,
            pre_provisioned_sandbox_id=authored.pre_provisioned_sandbox_id,
            proxy=proxy,
        )


class KoyebSandboxDriver(SandboxDriver):
    def __init__(
        self,
        authored: contracts.MistralSandbox | KoyebSandboxDefinition,
        restored_state: JsonObject | None,
        *,
        proxy_identity: Mapping[str, str] | None = None,
    ) -> None:
        self._definition = (
            authored if isinstance(authored, KoyebSandboxDefinition) else KoyebSandboxDefinition.from_authored(authored)
        )
        self._state = dict(restored_state or {})
        self._proxy_identity = (
            SandboxProxyIdentity.model_validate(proxy_identity) if proxy_identity is not None else None
        )
        self._proxy: KoyebProxyResource | None = None
        self._claimed = False

    @property
    def workspace(self) -> str:
        return DEFAULT_WORKSPACE

    @property
    def state(self) -> JsonObject:
        return dict(self._state)

    def root_reference(self) -> RootSandboxReference:
        """Name the created environment a child Session may borrow, never its credentials."""

        sandbox_id = self._state.get("sandbox_id")
        service_id = self._state.get("service_id")
        if not isinstance(sandbox_id, str) or not isinstance(service_id, str):
            raise RuntimeError("Created Koyeb Sandbox has no sandbox or service identity")
        return RootSandboxReference(sandbox_id=sandbox_id, service_id=UUID(service_id), workdir=self.workspace)

    async def create(self, identity: SandboxProvisioningIdentity) -> None:
        """Create the physical sandbox, or reattach to the one in restored state.

        Proxy configuration and ``setup_script`` are separate provisioning steps
        (``configure_new_proxy`` and ``run_setup_script``), so the resource orders and
        reports them.
        """

        if self._state.get("sandbox_id") is not None:
            await self.attach()
            return
        requested_at = determinism.now().timestamp()
        result = await _koyeb_create_v2(
            KoyebCreateRequest(
                # Sandbox creation does not use proxy configuration. Keeping it out of this
                # durable payload lets old and new workers process the same create activity
                # while proxy configuration models evolve independently.
                definition=self._definition.model_copy(update={"proxy": None, "setup_script": None}),
                name=_koyeb_sandbox_name(self._definition.name_prefix, identity),
            )
        )
        self._state = {**result.state, "lease_deadline": requested_at + self._definition.ttl_seconds}
        self._claimed = result.claimed

    async def attach(self) -> None:
        """Reconnect to the sandbox named in restored state; never creates one."""

        if self._state.get("sandbox_id") is None:
            raise RuntimeError("Koyeb Sandbox has no restored state to attach to")
        await self._open_proxy(configure=False)

    async def configure_new_proxy(self) -> None:
        """Recipe step: configure the Sandbox Proxy on a sandbox this driver just created."""

        await self._open_proxy(configure=True)

    async def run_setup_script(self) -> None:
        """Recipe step: run ``setup_script`` on a new sandbox; a claimed pool sandbox already ran it."""

        script = self._definition.setup_script
        if not script or self._claimed:
            return
        await _koyeb_run_setup_script(
            KoyebSetupScriptRequest(
                state=self._state,
                script=script,
                timeout_seconds=self._definition.setup_script_timeout_seconds,
            )
        )

    async def delete(self) -> None:
        sandbox_id = self._state.get("sandbox_id")
        if not isinstance(sandbox_id, str):
            return
        await _koyeb_delete(KoyebDeleteRequest(state=self._state))
        self._state = {}

    async def execute(self, request: WorkflowSandboxExecuteRequest) -> WorkflowSandboxExecuteResult:
        command = request.command
        if request.operation_name != "sandbox_proxy":
            await self.ensure_proxy_credentials()
            if self._proxy is not None:
                command = self._proxy.prepare_command(command)
        execute = _koyeb_execute_once if request.retry_mode == "at_most_once" else _koyeb_execute
        return await execute(
            KoyebExecuteRequest(
                state=self._state,
                command=command,
                cwd=request.cwd,
                timeout_seconds=require_sandbox_execute_timeout(
                    request.timeout_seconds or self._definition.default_exec_timeout_seconds
                ),
                env=request.env,
            )
        )

    async def ensure_proxy_credentials(self) -> None:
        if self._proxy is not None:
            await self._proxy.renew_if_needed()

    async def configure_proxy(
        self,
        integration: SandboxProxyIntegration,
    ) -> int:
        if not _use_sandbox_proxy_bootstrap_activity():
            result = await _koyeb_configure_proxy(
                KoyebProxyRequest(
                    operation="configure",
                    state=self._state,
                    definition=_legacy_proxy_definition(integration),
                    identity=self._require_proxy_identity(),
                    now=_epoch_seconds(),
                )
            )
            return result.expires_at
        result = await _koyeb_configure_proxy_v2(
            KoyebBootstrapProxyRequest(
                operation="setup",
                state=self._state,
                integration=integration,
            )
        )
        return result.expires_at

    async def renew_proxy(
        self,
        integration: SandboxProxyIntegration,
    ) -> int:
        if not _use_sandbox_proxy_bootstrap_activity():
            result = await _koyeb_configure_proxy(
                KoyebProxyRequest(
                    operation="renew",
                    state=self._state,
                    definition=_legacy_proxy_definition(integration),
                    identity=self._require_proxy_identity(),
                    now=_epoch_seconds(),
                )
            )
            return result.expires_at
        result = await _koyeb_configure_proxy_v2(
            KoyebBootstrapProxyRequest(
                operation="renewal",
                state=self._state,
                integration=integration,
            )
        )
        return result.expires_at

    def _require_proxy_identity(self) -> SandboxProxyIdentity:
        if self._proxy_identity is None:
            raise RuntimeError(
                "MistralSandbox(header_bindings=...) requires a caller identity to scope the legacy proxy token"
            )
        return self._proxy_identity

    def resolve_files_root(self, namespace: str) -> str:
        namespace = normalized_sandbox_root(namespace)
        name = namespace.strip("/").replace("/", "-")
        return f"{_FILES_ROOT}/{name}-{hashlib.sha256(namespace.encode()).hexdigest()[:8]}"

    async def write_files(self, request: WorkflowSandboxWriteFilesRequest) -> WorkflowSandboxWriteFilesResult:
        if not isinstance(self._state.get("sandbox_id"), str):
            raise RuntimeError("Koyeb sandbox is not created")
        root = self.resolve_files_root(request.root)
        result = await _koyeb_write_files(
            KoyebWriteFilesRequest(state=self._state, root=root, source=request.source, replace=request.replace)
        )
        return WorkflowSandboxWriteFilesResult(root=result.root, source_result=result.source_result)

    async def read_file(self, request: WorkflowSandboxReadFileRequest) -> WorkflowSandboxReadFileResult:
        command = shlex.join(
            [
                "python3",
                "-I",
                "-c",
                _KOYEB_READ_FILE_PROGRAM,
                request.path,
                str(request.max_bytes),
            ]
        )
        result = await self.execute(
            WorkflowSandboxExecuteRequest(
                command=command,
                operation_name="read_file",
                arguments={"path": request.path, "max_bytes": request.max_bytes},
                cwd=self.workspace,
                timeout_seconds=self._definition.default_exec_timeout_seconds,
                retry_mode="retry_safe",
            )
        )
        if result.exit_code == _KOYEB_FILE_NOT_FOUND_EXIT_CODE:
            raise FileNotFoundError(request.path)
        if result.exit_code != 0:
            raise RuntimeError(f"Koyeb read_file failed: {result.stderr or result.stdout}")
        content = result.stdout.strip()
        return WorkflowSandboxReadFileResult(
            content_base64=content,
            size_bytes=len(base64.b64decode(content.encode("ascii"), validate=True)),
        )

    async def _open_proxy(self, *, configure: bool) -> None:
        definition = self._definition.proxy
        if definition is None:
            return
        if not _use_sandbox_proxy_bootstrap_activity():
            if any(isinstance(integration, SecretInjectionProxyConfig) for integration in definition.integrations):
                raise SandboxBootstrapError(
                    "Sandbox Proxy secret injection requires authenticated bootstrap API access"
                )
            if not sandbox_proxy_is_configured():
                warnings.warn(
                    "MistralSandbox(header_bindings=...) is set but no sandbox-proxy config is "
                    "present in the environment, so Sandbox Proxy traffic will not be configured.",
                    stacklevel=3,
                )
                return
            self._require_proxy_identity()
        self._proxy = KoyebProxyResource(definition, self)
        if configure:
            await self._proxy.configure()
        else:
            self._proxy.attach_existing_sandbox()


async def open_borrowed_koyeb_sandbox(
    reference: RootSandboxReference,
    authored: contracts.Sandbox,
    host: "AgentsSdkSandbox",
    *,
    restored: WorkflowSandboxContinuation | None,
    bash_max_timeout: DeclaredBashMaxTimeout,
) -> WorkflowSandboxResource:
    """Open a child Session on its root's Koyeb Sandbox through the root's open path.

    The child gets the same driver, Sandbox Proxy and command preparation as the
    root, from the same authored binding. Only ownership differs: the child never
    runs the Sandbox's lifecycle hooks and never deletes it. A first open looks the
    Sandbox up once by its service identity; a continued child reopens from its own
    carried state, like a continued root.
    """

    if not isinstance(authored, contracts.MistralSandbox) or not isinstance(host.definition, CustomSandboxDefinition):
        raise ValueError("Borrowed Koyeb Sandbox requires a Koyeb worker binding")
    if restored is None or restored.provider_state is None:
        attached = await _koyeb_attach(KoyebAttachRequest(service_id=str(reference.service_id)))
        restored = WorkflowSandboxContinuation(
            sandbox=ReadySandbox(generation=1, attempt=1, provider_state=attached.state),
            session_started=True,
        )
    # Opening from a ready continuation reattaches the root's sandbox; the child never provisions.
    return await WorkflowSandboxResource.open(
        host.definition.model_copy(update={"hooks": (), "delete_on_cleanup": False}),
        config=host.config,
        restored=restored,
        host=host,
        bash_max_timeout=bash_max_timeout,
    )


class KoyebAttachRequest(RuntimeModel):
    service_id: str = Field(min_length=1)


class KoyebCreateRequest(RuntimeModel):
    definition: KoyebSandboxDefinition
    name: str


class KoyebCreateResult(RuntimeModel):
    state: JsonObject


class KoyebCreateV2Result(RuntimeModel):
    state: JsonObject
    claimed: bool = False
    """Whether the sandbox came from the pre-provisioned pool rather than a new deployment."""


class KoyebSetupScriptRequest(RuntimeModel):
    state: JsonObject
    script: str
    timeout_seconds: Annotated[int, Field(ge=1)]


class KoyebExecuteRequest(RuntimeModel):
    state: JsonObject
    command: str
    cwd: str
    timeout_seconds: Annotated[int, Field(ge=1)]
    env: dict[str, str] = Field(default_factory=dict)


class KoyebWriteFilesRequest(RuntimeModel):
    state: JsonObject
    root: str
    source: FileSource
    replace: bool = False


class KoyebWriteFilesResult(RuntimeModel):
    root: str
    source_result: JsonValue = None


class KoyebDeleteRequest(RuntimeModel):
    state: JsonObject


class KoyebProxyRequest(RuntimeModel):
    """Persisted request contract for the original proxy activity."""

    operation: Literal["configure", "renew"]
    state: JsonObject
    definition: _LegacyKoyebSandboxProxyDefinition
    identity: SandboxProxyIdentity
    now: int


class KoyebBootstrapProxyRequest(RuntimeModel):
    operation: Literal["setup", "renewal"]
    state: JsonObject
    integration: SandboxProxyIntegration


class KoyebProxyResult(RuntimeModel):
    expires_at: int


class _KoyebExecution(Protocol):
    exit_code: int | None
    duration: object | None
    stdout: str | None
    stderr: str | None


class _KoyebFilesystem(Protocol):
    async def write_file(self, path: str, content: str | bytes, encoding: str = "utf-8") -> None: ...


class _KoyebSandbox(Protocol):
    sandbox_id: str
    app_id: str
    service_id: str
    sandbox_secret: str | None
    _sandbox_url: tuple[str, str | None] | None

    async def exec(self, command: str, **kwargs: object) -> _KoyebExecution: ...

    async def delete(self) -> None: ...

    @property
    def filesystem(self) -> _KoyebFilesystem: ...

    async def update_lifecycle(self, *, delete_after_delay: int) -> None: ...


class KoyebProxyResource:
    def __init__(
        self,
        definition: KoyebSandboxProxyDefinition,
        driver: KoyebSandboxDriver,
    ) -> None:
        effects = tuple(
            _KoyebProxyIntegrationEffects(integration=integration, driver=driver)
            for integration in definition.integrations
        )
        self._lifecycle = SandboxProxyLifecycle(effects=effects, delete=driver.delete, now=_epoch_seconds)
        self._uses_secret_injection = any(
            isinstance(integration, SecretInjectionProxyConfig) for integration in definition.integrations
        )

    async def configure(self) -> None:
        await self._lifecycle.initialize_new_sandbox()

    def attach_existing_sandbox(self) -> None:
        self._lifecycle.attach_existing_sandbox()

    async def renew_if_needed(self) -> None:
        await self._lifecycle.before_execute()

    def prepare_command(self, command: str) -> str:
        if not self._uses_secret_injection:
            return command
        return f". {shlex.quote(_WORKSPACE_PROXY_ENV_FILE)} || exit $?\n{command}"


class _KoyebProxyIntegrationEffects(SandboxProxyEffects):
    def __init__(
        self,
        *,
        integration: SandboxProxyIntegration,
        driver: KoyebSandboxDriver,
    ) -> None:
        self._integration = integration
        self._driver = driver

    async def setup(self) -> int:
        return await self._driver.configure_proxy(self._integration)

    async def renew(self) -> int:
        return await self._driver.renew_proxy(self._integration)


def _legacy_proxy_definition(integration: SandboxProxyIntegration) -> _LegacyKoyebSandboxProxyDefinition:
    if not isinstance(integration, GitHubProxyConfig):
        raise SandboxBootstrapError("The legacy Sandbox Proxy activity supports only GitHub")
    return _LegacyKoyebSandboxProxyDefinition(
        repo_whitelist=integration.repo_whitelist,
        all_accessible_repos=integration.all_accessible_repos,
        ttl_seconds=integration.ttl_seconds,
        github_host=integration.host,
    )


def _use_sandbox_proxy_bootstrap_activity() -> bool:
    if not temporalio.workflow.in_workflow():
        return True
    context = retrieve_context()
    if context is not None and not context.on_behalf_of:
        return False
    return temporalio.workflow.patched(_SANDBOX_PROXY_BOOTSTRAP_ACTIVITY_PATCH)


def sandbox_proxy_is_configured() -> bool:
    return SandboxProxySettings().url is not None


def _koyeb_docker_daemon_start_command(definition: KoyebSandboxDefinition) -> str:
    return f"{_KOYEB_DOCKER_DAEMON_START_COMMAND} {shlex.quote(definition.docker_daemon_network_mode)}"


async def _ensure_koyeb_workspace(sandbox: _KoyebSandbox, definition: KoyebSandboxDefinition) -> None:
    result = await sandbox.exec(
        _KOYEB_ENSURE_WORKSPACE_COMMAND,
        timeout=definition.readiness_probe_timeout_seconds,
    )
    if result.exit_code != 0:
        output = (result.stderr or "").strip() or (result.stdout or "").strip() or "<empty output>"
        raise RuntimeError(f"Koyeb sandbox workspace setup failed: {output}")


async def _wait_until_koyeb_sandbox_ready(
    sandbox: _KoyebSandbox,
    definition: KoyebSandboxDefinition,
    *,
    include_docker_probe: bool,
) -> None:
    probes: list[tuple[str, str]] = [_KOYEB_BASIC_READINESS_PROBE]
    if include_docker_probe:
        probes.append(_KOYEB_DOCKER_READINESS_PROBE)

    for attempt in range(1, definition.readiness_max_retries + 1):
        for command, expected_output in probes:
            result = await sandbox.exec(command, timeout=definition.readiness_probe_timeout_seconds)
            if result.exit_code == 0 and (result.stdout or "").strip() == expected_output:
                continue
            break
        else:
            return

        if attempt < definition.readiness_max_retries:
            await asyncio.sleep(definition.readiness_interval_seconds)

    probe_name = "Docker readiness" if include_docker_probe else "Koyeb sandbox readiness"
    raise RuntimeError(f"{probe_name} probe failed")


def _koyeb_sandbox_state(sandbox: _KoyebSandbox, access: KoyebApiAccess) -> JsonObject:
    """Durable sandbox state. It enters Workflow history, so it never holds the sandbox secret.

    The secret plus the sandbox URL is enough to run commands in the sandbox, and any workspace
    member can read a Session's history. Workers look the secret up from Koyeb instead.

    The API host is kept so the sandbox stays on the backend that created it, whatever credential
    the worker holds later.
    """
    koyeb_secrets.put(sandbox)
    return {
        "sandbox_id": sandbox.sandbox_id,
        "app_id": sandbox.app_id,
        "service_id": sandbox.service_id,
        "sandbox_url": list(sandbox._sandbox_url) if sandbox._sandbox_url is not None else None,
        "api_host": access.host,
    }


async def _koyeb_sandbox_secret(service_id: str, access: KoyebApiAccess) -> SecretStr:
    cached = koyeb_secrets.get(service_id)
    if cached is not None:
        return cached
    AsyncSandbox = _require_koyeb_sdk()
    try:
        sandbox = cast(
            _KoyebSandbox,
            await AsyncSandbox.get_from_id(id=service_id, api_token=access.token, host=access.host),
        )
    except Exception as error:
        if _is_gone_koyeb_sandbox_error(error):
            raise WorkflowSandboxUnavailableError("Koyeb sandbox no longer exists") from error
        raise
    return koyeb_secrets.put(sandbox)


def _is_gone_koyeb_sandbox_error(error: Exception) -> bool:
    if isinstance(error, httpx.HTTPStatusError) and error.response.status_code == 404:
        return True
    message = str(error).lower()
    return "not found" in message or "no longer exist" in message


def _koyeb_delete_after_delay(
    ttl_seconds: int,
    created_at_epoch_seconds: float | None,
) -> int:
    if created_at_epoch_seconds is None:
        return ttl_seconds
    return max(0, math.ceil(time.time() - created_at_epoch_seconds)) + ttl_seconds


async def _koyeb_service_created_at_epoch_seconds(
    service_id: str,
    access: KoyebApiAccess,
) -> float | None:
    try:
        async with httpx.AsyncClient(timeout=10.0, verify=build_ssl_context()) as client:
            response = await client.get(
                f"{access.host}/v1/services/{service_id}",
                headers={"Authorization": f"Bearer {access.token}"},
            )
            response.raise_for_status()
    except httpx.HTTPError:
        return None

    try:
        body = response.json()
        created_at = body.get("service", {}).get("created_at")
        return datetime.fromisoformat(created_at.replace("Z", "+00:00")).timestamp()
    except (AttributeError, TypeError, ValueError):
        return None


class _KoyebDeployment(BaseModel):
    """The fields of a Koyeb `GET /v1/deployments/{id}` deployment that tell why it failed."""

    status: str | None = None
    messages: list[str] = Field(default_factory=list)


async def _raise_if_koyeb_deployment_failed(
    service_id: str, image: str, access: KoyebApiAccess, *, registry_secret: str | None
) -> None:
    """Stop sandbox creation for good when Koyeb reports that the deployment failed.

    Another attempt would create a new sandbox from the same image with the same token and fail
    the same way, so the error is not retryable and carries Koyeb's own reason.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0, verify=build_ssl_context()) as client:
            headers = {"Authorization": f"Bearer {access.token}"}
            service = await client.get(f"{access.host}/v1/services/{service_id}", headers=headers)
            service.raise_for_status()
            deployment_id = service.json().get("service", {}).get("latest_deployment_id")
            if not isinstance(deployment_id, str):
                return
            response = await client.get(f"{access.host}/v1/deployments/{deployment_id}", headers=headers)
            response.raise_for_status()
            deployment = _KoyebDeployment.model_validate(response.json().get("deployment"))
    except (httpx.HTTPError, AttributeError, ValueError):
        return
    if deployment.status not in _KOYEB_FAILED_DEPLOYMENT_STATUSES:
        return
    reason = "; ".join(deployment.messages) or "Koyeb gave no reason"
    message = f"Koyeb sandbox deployment failed with status {deployment.status}: {reason}."
    if registry_secret is None:
        message += (
            f" If Koyeb could not pull {image}, make the image public or set "
            "AGENTS_SDK_KOYEB_SANDBOX_REGISTRY_SECRET to a registry secret of your Koyeb organization that can pull it."
        )
    raise ApplicationError(
        message,
        type="KoyebSandboxDeploymentFailedError",
        non_retryable=True,
    )


class _KoyebInstanceTypeUsage(BaseModel):
    instance_type: str = ""
    used: int = 0
    limit: int = 0


class _KoyebQuotaUsage(BaseModel):
    """The fields of a Koyeb `GET /v1/quotas/organizations/{id}/usage` reply that a new sandbox counts against."""

    apps_used: int = 0
    apps_limit: int = 0
    services_used: int = 0
    services_limit: int = 0
    memory_mb_used: int = 0
    memory_mb_limit: int = 0
    instances_by_type: list[_KoyebInstanceTypeUsage] = Field(default_factory=list)

    def exhausted(self, instance_type: str, requested_memory_mb: int | None) -> list[str]:
        counts = [
            ("apps", self.apps_used, self.apps_limit),
            ("services", self.services_used, self.services_limit),
            *(
                (f"{usage.instance_type} instances", usage.used, usage.limit)
                for usage in self.instances_by_type
                if usage.instance_type == instance_type
            ),
        ]
        # A missing or zero limit says nothing about the organization's quota.
        exhausted = [f"{name} ({used} of {limit} used)" for name, used, limit in counts if 0 < limit <= used]
        # Memory runs out before it is fully used: a sandbox needs room for its whole instance. Without
        # the instance's size, only a full memory quota shows that it cannot fit.
        if 0 < self.memory_mb_limit < self.memory_mb_used + (requested_memory_mb or 1):
            needs = f", the sandbox needs {requested_memory_mb} MB" if requested_memory_mb else ""
            exhausted.append(f"memory ({self.memory_mb_used} of {self.memory_mb_limit} MB used{needs})")
        return exhausted


# Koyeb counts memory quota in decimal units: a "1GB" instance uses 1000 MB of it.
_KOYEB_CATALOG_MB_PER_UNIT = {"MB": 1, "GB": 1000}


class _KoyebCatalogInstance(BaseModel):
    """The field of a Koyeb `GET /v1/catalog/instances/{id}` instance that sizes its memory quota use."""

    memory: str

    def memory_mb(self) -> int | None:
        """The memory in MB, from the catalog's whole-number "512MB" or "2GB" form."""
        number, unit = self.memory[:-2], self.memory[-2:]
        if not number.isdigit() or unit not in _KOYEB_CATALOG_MB_PER_UNIT:
            return None
        return int(number) * _KOYEB_CATALOG_MB_PER_UNIT[unit]


async def _koyeb_instance_memory_mb(
    client: httpx.AsyncClient, access: KoyebApiAccess, headers: dict[str, str], instance_type: str
) -> int | None:
    try:
        response = await client.get(f"{access.host}/v1/catalog/instances/{instance_type}", headers=headers)
        response.raise_for_status()
        return _KoyebCatalogInstance.model_validate(response.json().get("instance")).memory_mb()
    except (httpx.HTTPError, AttributeError, ValueError):
        return None


def _koyeb_api_refusal_status(error: BaseException) -> int | None:
    """The 4xx status of a Koyeb API refusal, raised directly or wrapped in koyeb-sdk's SandboxError."""
    for candidate in (error, error.__cause__):
        status = getattr(candidate, "status", None)
        if isinstance(status, int) and 400 <= status < 500:
            return status
    return None


def _is_koyeb_api_refusal(error: BaseException) -> bool:
    """Whether the Koyeb API refused a request, as raised directly or wrapped in koyeb-sdk's SandboxError."""
    return _koyeb_api_refusal_status(error) is not None


def _raise_if_koyeb_access_denied(
    error: BaseException,
    access: KoyebApiAccess,
    settings: KoyebSandboxRuntimeSettings,
) -> None:
    """Stop sandbox creation for good when the credential may not create sandboxes.

    Another attempt sends the same credential and is refused the same way. Mistral Cloud refuses a
    Mistral identity without sandbox access with a bare 403, so the error names both ways to fix it.
    """
    status = _koyeb_api_refusal_status(error)
    if status not in (401, 403):
        return
    if access.host == settings.mistral_cloud_api_url.rstrip("/"):
        message = (
            f"Mistral Cloud refused to create the sandbox (HTTP {status}): the Mistral identity this process "
            "uses (MISTRAL_API_KEY, or the worker's service account) does not have access to Mistral Cloud "
            "sandboxes. Use a Mistral identity that has sandbox access, or set AGENTS_SDK_KOYEB_SANDBOX_API_TOKEN "
            "to an API token of your own Koyeb organization, then start the session again."
        )
    else:
        message = (
            f"Koyeb refused to create the sandbox (HTTP {status}): the Koyeb API token "
            "(AGENTS_SDK_KOYEB_SANDBOX_API_TOKEN, KOYEB_API_TOKEN or KOYEB_API_KEY) is invalid or may not create "
            "services in its organization. Check the token, then start the session again."
        )
    raise ApplicationError(message, type="MistralSandboxAccessDeniedError", non_retryable=True)


async def _raise_if_koyeb_quota_exhausted(
    error: BaseException,
    instance_type: str,
    access: KoyebApiAccess,
    settings: KoyebSandboxRuntimeSettings,
) -> None:
    """Stop sandbox creation for good when the organization has no quota left for another sandbox.

    Koyeb refuses an exhausted quota with a generic precondition failure that other refusals share,
    so the organization's quota usage, not the refusal, tells the two apart. It is read only after a
    refusal, so a healthy create costs nothing more.

    The organization is found through one of its apps: Mistral Cloud does not serve Koyeb's
    `/v1/account/organization`. An organization with no app has no full quota to report.
    """
    if not _is_koyeb_api_refusal(error):
        return
    try:
        async with httpx.AsyncClient(timeout=10.0, verify=build_ssl_context()) as client:
            headers = {"Authorization": f"Bearer {access.token}"}
            apps = await client.get(f"{access.host}/v1/apps", params={"limit": "1"}, headers=headers)
            apps.raise_for_status()
            organization_id = apps.json()["apps"][0]["organization_id"]
            response = await client.get(
                f"{access.host}/v1/quotas/organizations/{organization_id}/usage", headers=headers
            )
            response.raise_for_status()
            usage = _KoyebQuotaUsage.model_validate(response.json().get("usage"))
            requested_memory_mb = (
                await _koyeb_instance_memory_mb(client, access, headers, instance_type)
                if usage.memory_mb_limit > 0
                else None
            )
    except (httpx.HTTPError, AttributeError, IndexError, KeyError, TypeError, ValueError):
        return
    exhausted = usage.exhausted(instance_type, requested_memory_mb)
    if not exhausted:
        return
    backend = "Mistral Cloud" if access.host == settings.mistral_cloud_api_url.rstrip("/") else "Koyeb"
    raise ApplicationError(
        f"{backend} refused to create the sandbox: the organization has reached its quota of "
        f"{', '.join(exhausted)}. Delete the sandboxes and apps you no longer need, or ask for a "
        "higher quota, then start the session again.",
        type="MistralSandboxQuotaExceededError",
        non_retryable=True,
    )


def koyeb_sandbox_class() -> Any | None:
    """Return koyeb-sdk's AsyncSandbox, or None when koyeb-sdk is missing or too old to provide it.

    The one check of the Koyeb SDK contract: `agents serve` and the worker refuse to start on None, and
    sandbox creation fails on it, so a worker never starts with an SDK it cannot create sandboxes with.
    """
    try:
        from koyeb import AsyncSandbox  # type: ignore[import-untyped]  # noqa: PLC0415
    except ImportError as error:
        # name is "koyeb" both when the package is absent and when it lacks AsyncSandbox (an older
        # koyeb-sdk, or another package by that name). A dependency of koyeb failing to import is not
        # a missing extra, so it propagates.
        if error.name == "koyeb":
            return None
        raise
    return AsyncSandbox


def _require_koyeb_sdk() -> Any:
    sandbox_class = koyeb_sandbox_class()
    if sandbox_class is None:
        raise RuntimeError("MistralSandbox requires koyeb-sdk>=1.5.5; install mistralai-agents[koyeb]")
    return sandbox_class


async def _claim_koyeb_sandbox(
    definition: KoyebSandboxDefinition,
    access: KoyebApiAccess,
) -> KoyebCreateV2Result | None:
    sandbox_id = definition.pre_provisioned_sandbox_id
    if sandbox_id is None:
        return None

    AsyncSandbox = _require_koyeb_sdk()

    try:
        sandbox = cast(
            _KoyebSandbox,
            await AsyncSandbox.get_from_id(
                id=sandbox_id,
                api_token=access.token,
                host=access.host,
            ),
        )
        created_at_epoch_seconds = await _koyeb_service_created_at_epoch_seconds(
            sandbox.service_id,
            access,
        )
        await sandbox.update_lifecycle(
            delete_after_delay=_koyeb_delete_after_delay(
                definition.ttl_seconds,
                created_at_epoch_seconds,
            )
        )
    except Exception as error:
        if _is_gone_koyeb_sandbox_error(error):
            return None
        raise

    return KoyebCreateV2Result(state=_koyeb_sandbox_state(sandbox, access), claimed=True)


@workflows.activity(
    name="vibe_harness_koyeb_create",
    retry_policy_max_attempts=KOYEB_SANDBOX_CREATE_MAX_ATTEMPTS,
    start_to_close_timeout=KOYEB_SANDBOX_CREATE_ATTEMPT_TIMEOUT,
)
async def _koyeb_create(request: KoyebCreateRequest) -> KoyebCreateResult:
    """Complete create activities scheduled before setup became a separate step."""

    result = await _run_koyeb_create(request, run_setup_script=True)
    return KoyebCreateResult(state=result.state)


@workflows.activity(
    name="vibe_harness_koyeb_create_v2",
    retry_policy_max_attempts=KOYEB_SANDBOX_CREATE_MAX_ATTEMPTS,
    start_to_close_timeout=KOYEB_SANDBOX_CREATE_ATTEMPT_TIMEOUT,
)
async def _koyeb_create_v2(request: KoyebCreateRequest) -> KoyebCreateV2Result:
    """Create a sandbox whose setup script runs later as a provisioning step."""

    return await _run_koyeb_create(request, run_setup_script=False)


async def _run_koyeb_create(
    request: KoyebCreateRequest,
    *,
    run_setup_script: bool,
) -> KoyebCreateV2Result:
    AsyncSandbox = _require_koyeb_sdk()

    definition = request.definition
    settings = KoyebSandboxRuntimeSettings()
    access = settings.api_access()
    claimed = await _claim_koyeb_sandbox(definition, access)
    if claimed is not None:
        return claimed
    try:
        sandbox = await AsyncSandbox.create(
            image=definition.image,
            name=request.name,
            wait_ready=False,
            api_token=access.token,
            host=access.host,
            region=definition.region,
            instance_type=definition.instance_type,
            delete_after_delay=definition.ttl_seconds,
            idle_timeout=definition.idle_timeout_seconds,
            _experimental_enable_light_sleep=definition.enable_light_sleep,
            env=settings.extra_env or None,
            registry_secret=settings.registry_secret,
            enable_mesh=definition.enable_mesh,
            privileged=definition.privileged or definition.docker_daemon_enabled,
            block_network=definition.egress.mode == "block_all",
            outbound_allowlist=list(definition.egress.allow_cidrs) if definition.egress.mode == "custom" else None,
        )
    except Exception as error:
        _raise_if_koyeb_access_denied(error, access, settings)
        await _raise_if_koyeb_quota_exhausted(error, definition.instance_type, access, settings)
        raise
    try:
        try:
            ready = await sandbox.wait_ready(timeout=definition.wait_ready_timeout_seconds)
        except Exception:
            await _raise_if_koyeb_deployment_failed(
                sandbox.service_id, definition.image, access, registry_secret=settings.registry_secret
            )
            raise
        if not ready:
            await _raise_if_koyeb_deployment_failed(
                sandbox.service_id, definition.image, access, registry_secret=settings.registry_secret
            )
            raise RuntimeError("Koyeb sandbox wait_ready timed out")
        await _wait_until_koyeb_sandbox_ready(
            sandbox,
            definition,
            include_docker_probe=False,
        )
        await _ensure_koyeb_workspace(sandbox, definition)
        if definition.docker_daemon_enabled:
            result = await sandbox.exec(
                _koyeb_docker_daemon_start_command(definition),
                timeout=definition.setup_script_timeout_seconds,
            )
            if result.exit_code != 0:
                output = (result.stderr or "").strip() or (result.stdout or "").strip() or "<empty output>"
                raise RuntimeError(f"Koyeb Docker daemon startup failed: {output}")
            await _wait_until_koyeb_sandbox_ready(
                sandbox,
                definition,
                include_docker_probe=True,
            )
        if run_setup_script and definition.setup_script:
            result = await sandbox.exec(
                definition.setup_script,
                timeout=definition.setup_script_timeout_seconds,
            )
            if result.exit_code != 0:
                raise RuntimeError(f"Koyeb setup script failed: {result.stderr or result.stdout}")
    except BaseException:
        with suppress(Exception):
            await sandbox.delete()
        raise
    return KoyebCreateV2Result(state=_koyeb_sandbox_state(cast(_KoyebSandbox, sandbox), access))


@workflows.activity(
    name="vibe_harness_koyeb_attach",
    retry_policy_max_attempts=6,
)
async def _koyeb_attach(request: KoyebAttachRequest) -> KoyebCreateResult:
    """Look up a live Sandbox by its service identity for a Session that borrows it."""

    AsyncSandbox = _require_koyeb_sdk()
    try:
        access = KoyebSandboxRuntimeSettings().api_access()
        sandbox = await AsyncSandbox.get_from_id(
            id=request.service_id,
            api_token=access.token,
            host=access.host,
        )
    except Exception as error:
        if _is_gone_koyeb_sandbox_error(error):
            # A deleted Sandbox stays deleted: fail the attach now instead of retrying it.
            # The Workflow still sees the WorkflowSandboxUnavailableError type it matches on.
            raise ApplicationError(
                "Koyeb sandbox no longer exists",
                type=WorkflowSandboxUnavailableError.__name__,
                non_retryable=True,
            ) from error
        raise
    return KoyebCreateResult(state=_koyeb_sandbox_state(cast(_KoyebSandbox, sandbox), access))


async def _restore_koyeb_sandbox(state: JsonObject) -> _KoyebSandbox:
    AsyncSandbox = _require_koyeb_sdk()

    sandbox_id = state.get("sandbox_id")
    app_id = state.get("app_id")
    service_id = state.get("service_id")
    if not (isinstance(sandbox_id, str) and isinstance(app_id, str) and isinstance(service_id, str)):
        raise RuntimeError("Koyeb sandbox state is incomplete")
    api_host = state.get("api_host")
    access = KoyebSandboxRuntimeSettings().api_access(host=api_host if isinstance(api_host, str) else None)
    sandbox = AsyncSandbox(
        sandbox_id=sandbox_id,
        app_id=app_id,
        service_id=service_id,
        sandbox_secret=(await _koyeb_sandbox_secret(service_id, access)).get_secret_value(),
        api_token=access.token,
        host=access.host,
    )
    sandbox_url = state.get("sandbox_url")
    if isinstance(sandbox_url, list) and len(sandbox_url) == 2 and isinstance(sandbox_url[0], str):
        sandbox._sandbox_url = (
            sandbox_url[0],
            sandbox_url[1] if isinstance(sandbox_url[1], str) else None,
        )
    return cast(_KoyebSandbox, sandbox)


async def _execute_koyeb_sandbox_command(
    sandbox: _KoyebSandbox,
    command: str,
    *,
    cwd: str,
    env: dict[str, str] | None,
    timeout: int,
) -> _KoyebExecution:
    try:
        return await sandbox.exec(
            command,
            cwd=cwd,
            env=env,
            timeout=timeout,
        )
    except Exception as error:
        if _is_gone_koyeb_sandbox_error(error):
            raise WorkflowSandboxUnavailableError("Koyeb sandbox no longer exists") from error
        raise


@workflows.activity(
    name="vibe_harness_koyeb_setup_script",
    # Bounded by the script's own exec timeout; this ceiling only catches a hung connection.
    start_to_close_timeout=KOYEB_SANDBOX_SETUP_ACTIVITY_TIMEOUT,
    heartbeat_timeout=_KOYEB_SETUP_SCRIPT_HEARTBEAT_TIMEOUT,
    # A script is not known to be repeatable on the same sandbox, so it runs at most once.
    # The provisioning step retries it on a new sandbox instead.
    retry_policy_max_attempts=1,
)
async def _koyeb_run_setup_script(request: KoyebSetupScriptRequest) -> None:
    async with heartbeat_while_running():
        sandbox = await _restore_koyeb_sandbox(request.state)
        result = await sandbox.exec(request.script, timeout=request.timeout_seconds)
    if result.exit_code != 0:
        raise RuntimeError(f"Koyeb setup script failed: {result.stderr or result.stdout}")


@workflows.activity(name="vibe_harness_koyeb_execute", start_to_close_timeout=SANDBOX_EXECUTE_ACTIVITY_TIMEOUT)
async def _koyeb_execute(request: KoyebExecuteRequest) -> WorkflowSandboxExecuteResult:
    return await run_koyeb_execute(request)


@workflows.activity(
    name="vibe_harness_koyeb_execute_once",
    start_to_close_timeout=SANDBOX_EXECUTE_ACTIVITY_TIMEOUT,
    retry_policy_max_attempts=1,
)
async def _koyeb_execute_once(request: KoyebExecuteRequest) -> WorkflowSandboxExecuteResult:
    return await run_koyeb_execute(request)


async def run_koyeb_execute(request: KoyebExecuteRequest) -> WorkflowSandboxExecuteResult:
    """Run one command in the Koyeb sandbox described by the request state, from Activity code."""

    sandbox = await _restore_koyeb_sandbox(request.state)
    result = await _execute_koyeb_sandbox_command(
        sandbox,
        request.command,
        cwd=request.cwd,
        env=request.env or None,
        timeout=request.timeout_seconds,
    )
    if result.exit_code is None or result.duration is None:
        raise RuntimeError("Koyeb execution returned incomplete result")
    return WorkflowSandboxExecuteResult(
        stdout=result.stdout or "",
        stderr=result.stderr or "",
        exit_code=result.exit_code,
    )


_KOYEB_EXTRACT_FILES_PROGRAM = """
import base64, fcntl, io, os, shutil, sys, tarfile
prefix, count, target, replace = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4] == "1"
bundle_directory = sys.argv[5]
parts = [f"{prefix}.{index:05d}" for index in range(count)]
data = io.BytesIO()
for part in parts:
    with open(part, encoding="ascii") as handle:
        data.write(base64.b64decode(handle.read()))
    os.remove(part)
data.seek(0)
destination = os.path.join(target, bundle_directory) if bundle_directory else target
parent = os.path.dirname(destination)
os.makedirs(parent, exist_ok=True)
stage = None
if replace or bundle_directory:
    stage = os.path.join(parent, ".agents-sdk-files-" + os.urandom(8).hex())
    os.mkdir(stage)
extraction_root = stage if stage else target
os.makedirs(extraction_root, exist_ok=True)
try:
    with tarfile.open(fileobj=data, mode="r:gz") as archive:
        try:
            archive.extractall(extraction_root, filter="data")
        except TypeError:
            archive.extractall(extraction_root)
    if stage:
        prepared = os.path.join(stage, bundle_directory) if bundle_directory else stage
        lock_path = os.path.join(parent, "." + os.path.basename(destination) + ".agents-sdk-files.lock")
        with open(lock_path, "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if os.path.isdir(destination) and not os.path.islink(destination):
                shutil.rmtree(destination)
            elif os.path.lexists(destination):
                os.remove(destination)
            os.rename(prepared, destination)
            if bundle_directory:
                os.replace(prepared + ".complete", destination + ".complete")
finally:
    if stage and os.path.isdir(stage):
        shutil.rmtree(stage)
"""
# Parts of a few MiB keep each filesystem request small. The server stores the text as given, so the
# extract step decodes the base64 of each part.
_UPLOAD_PART_BYTES = 3 * 1024 * 1024
_UPLOAD_DIR = "/tmp"  # noqa: S108


@workflows.activity(name="vibe_harness_koyeb_write_files")
async def _koyeb_write_files(request: KoyebWriteFilesRequest) -> KoyebWriteFilesResult:
    publication = file_materialization_from_source(request.source)
    resolved = await resolve_file_source(request.source)
    if publication is not None and not resolved.files:
        return KoyebWriteFilesResult(root=request.root, source_result=None)
    sandbox = await _restore_koyeb_sandbox(request.state)
    await _upload_files(sandbox, request.root, resolved.files, replace=request.replace, publication=publication)
    return KoyebWriteFilesResult(root=request.root, source_result=resolved.result)


async def _upload_files(
    sandbox: _KoyebSandbox,
    root: str,
    files: tuple[ResolvedFile, ...],
    *,
    replace: bool,
    publication: FileMaterialization | None,
) -> None:
    if publication is not None and replace:
        raise ValueError("immutable materialization must not replace its shared namespace")
    # Resolved bundles have no size cap, so the archive is built off the event loop.
    data = await asyncio.to_thread(lambda: gzip.compress(files_to_tar(files)))
    # Each attempt has its own parts, so a retry never reads or deletes the parts of another one.
    prefix = f"{_UPLOAD_DIR}/agents-sdk-files-{uuid.uuid4().hex}"
    parts: list[str] = []
    try:
        # Each part is encoded and decoded on its own, so only one encoded part is in memory at a time.
        for start in range(0, len(data), _UPLOAD_PART_BYTES):
            part = f"{prefix}.{len(parts):05d}"
            # Listed before the write, so the cleanup also removes a part whose write timed out.
            parts.append(part)
            await sandbox.filesystem.write_file(
                part, base64.b64encode(data[start : start + _UPLOAD_PART_BYTES]).decode("ascii")
            )
        command = shlex.join(
            [
                "python3",
                "-I",
                "-c",
                _KOYEB_EXTRACT_FILES_PROGRAM,
                prefix,
                str(len(parts)),
                root,
                "1" if replace else "0",
                publication.directory if publication is not None else "",
            ]
        )
        result = await _execute_koyeb_sandbox_command(sandbox, command, cwd="/", env=None, timeout=120)
        if result.exit_code != 0:
            raise RuntimeError(f"Koyeb file extraction into {root} failed: {result.stderr or result.stdout}")
    except BaseException:
        if parts:
            with suppress(Exception):
                await _execute_koyeb_sandbox_command(
                    sandbox, shlex.join(["rm", "-f", "--", *parts]), cwd="/", env=None, timeout=60
                )
        raise


@workflows.activity(name="vibe_harness_koyeb_delete")
async def _koyeb_delete(request: KoyebDeleteRequest) -> None:
    service_id = request.state.get("service_id")
    try:
        sandbox = await _restore_koyeb_sandbox(request.state)
        await sandbox.delete()
    except WorkflowSandboxUnavailableError:
        pass
    except Exception as error:
        if "not found" not in str(error).lower():
            raise
    if isinstance(service_id, str):
        koyeb_secrets.evict(service_id)


@workflows.activity(name="vibe_harness_koyeb_configure_proxy")
async def _koyeb_configure_proxy(request: KoyebProxyRequest) -> KoyebProxyResult:
    """Complete proxy activities persisted before the bootstrap API migration."""

    proxy_url, ca_cert, signing_secret = SandboxProxySettings().require()
    sandbox = await _restore_koyeb_sandbox(request.state)

    if request.operation == "configure":
        env, command = build_github_proxy_sandbox_setup(
            identity=request.identity,
            repo_whitelist=list(request.definition.repo_whitelist),
            all_accessible_repos=request.definition.all_accessible_repos,
            proxy_url=proxy_url,
            ca_cert=ca_cert,
            signing_secret=signing_secret,
            ttl_seconds=request.definition.ttl_seconds,
            now=request.now,
            github_host=request.definition.github_host,
        )
        expires_at = request.now + request.definition.ttl_seconds
    else:
        renewal = build_github_proxy_token_renewal(
            identity=request.identity,
            proxy_url=proxy_url,
            signing_secret=signing_secret,
            repo_whitelist=list(request.definition.repo_whitelist),
            all_accessible_repos=request.definition.all_accessible_repos,
            ttl_seconds=request.definition.ttl_seconds,
            now=request.now,
            github_host=request.definition.github_host,
        )
        env = dict(renewal.env)
        command = build_github_proxy_token_renewal_command(github_host=request.definition.github_host)
        expires_at = renewal.expires_at

    result = await _execute_koyeb_sandbox_command(
        sandbox,
        command,
        cwd=DEFAULT_WORKSPACE,
        env=env,
        timeout=_PROXY_SETUP_TIMEOUT_SECONDS,
    )
    if result.exit_code != 0:
        raise RuntimeError(
            "Sandbox proxy setup failed: "
            f"{(result.stderr or '').strip() or (result.stdout or '').strip() or '<empty output>'}"
        )
    return KoyebProxyResult(expires_at=expires_at)


@workflows.activity(name="vibe_harness_koyeb_configure_proxy_v2")
async def _koyeb_configure_proxy_v2(request: KoyebBootstrapProxyRequest) -> KoyebProxyResult:
    try:
        async with SandboxProxyBootstrapClient.from_current_environment() as client:
            bootstrap = await client.bootstrap(request.integration)
        command = bootstrap.setup_command if request.operation == "setup" else bootstrap.renewal_command
        sandbox = await _restore_koyeb_sandbox(request.state)
        # Provider setup and renewal commands persist their runtime configuration in the sandbox.
        # Do not return runtime_env through the activity because it can contain short-lived credentials
        # that would then enter Workflow history.
        result = await _execute_koyeb_sandbox_command(
            sandbox,
            command,
            cwd=DEFAULT_WORKSPACE,
            env=bootstrap.setup_env,
            timeout=_PROXY_SETUP_TIMEOUT_SECONDS,
        )
        if result.exit_code != 0:
            raise SandboxBootstrapError(f"Sandbox Proxy {request.operation} command failed in the sandbox")
    except (SandboxBootstrapError, WorkflowSandboxUnavailableError):
        raise
    except Exception:
        raise SandboxBootstrapError("Sandbox Proxy activity failed") from None
    return KoyebProxyResult(expires_at=bootstrap.expires_at)


def _koyeb_sandbox_name(prefix: str, identity: SandboxProvisioningIdentity) -> str:
    execution_id = workflows.get_execution_id() or hashlib.sha256(str(time.time_ns()).encode()).hexdigest()
    # Hash the execution id so truncation cannot collapse distinct executions onto one name.
    root_session_hash = hashlib.sha256(execution_id.encode()).hexdigest()[:16]
    suffix = f"{root_session_hash}-g{identity.generation}-a{identity.attempt}"
    prefix_budget = _SANDBOX_NAME_MAX_LENGTH - len(suffix) - 1
    return f"{prefix[:prefix_budget].rstrip('-')}-{suffix}"


def _epoch_seconds() -> int:
    return int(determinism.now().timestamp())


def register_koyeb_sandbox_activities() -> None:
    """Load SDK-owned Koyeb activities before the worker registry snapshot."""
