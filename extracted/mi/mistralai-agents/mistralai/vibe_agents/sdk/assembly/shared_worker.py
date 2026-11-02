"""Turn an authored Agent into the spec the Agents shared worker runs, and that spec back into an Agent.

The shared worker runs the Agents of every workspace without any of their code, so a
shared-worker Agent keeps only the authoring that is plain data. Authoring that needs the
author's code is refused: tools, Hooks, Sandbox Hooks, custom Sandboxes and custom completion
configurations.

The worker is a platform process shared across tenants, so authoring that would act with the
worker's own authority is refused too. A value that names an environment variable reads the
worker's environment, which holds platform credentials. A connector that runs as the deployment
runs as the platform. A managed Sandbox that is privileged, runs a Docker daemon or attaches to
an existing Sandbox id is created with the platform's sandbox account. A Bashkit network that
injects credentials or reaches private IPs acts from inside the platform's network.

The spec (``SharedWorkerAgentSpec``) cannot express any of these, so the worker validates a
spec by parsing it. Skills are not supported yet: the shared worker will take AI Registry skill
references.
"""

from collections.abc import Iterator, Sequence
from typing import Any

from mistralai.vibe.harness.app_server.session import McpHttpSourceConfiguration
from mistralai.vibe.harness.runtime.hosts.workflows.harness_definition import WorkflowHarnessDefinition
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring import types as authoring_types
from mistralai.vibe_agents.sdk.authoring.agent import AgentAuthoring
from mistralai.vibe_agents.sdk.authoring.errors import SdkError
from mistralai.vibe_agents.sdk.authoring.permissions import PermissionPolicy
from mistralai.vibe_agents.sdk.authoring.sandbox_policy import Network
from mistralai.vibe_agents.sdk.authoring.secrets import SecretOrigin
from mistralai.workflows.plugins.mistralai.connectors import decorator as connector_decorator

from . import assemble
from .connectors import RunAs

_SUPPORTED_SANDBOXES: tuple[type[contracts.Sandbox], ...] = (
    contracts.NoSandbox,
    contracts.MistralSandbox,
    contracts.BashkitSandbox,
)
_MISTRAL_SANDBOX_FIELDS = tuple(
    name for name in wire.SharedWorkerMistralSandbox.model_fields if name not in ("kind", "access", "sandbox_proxy")
)
_DEFAULT_MCP = McpHttpSourceConfiguration(url="https://default.invalid")
# Compiling only to validate or to read derived properties binds no code, so any provider id works.
_CHECK_CAPABILITY_PROVIDER_ID = "shared-worker-check"


class SharedWorkerAgentError(ValueError):
    """Raised when an Agent cannot run on the shared worker. Lists every reason at once."""

    def __init__(self, issues: Sequence[str]) -> None:
        self.issues = tuple(issues)
        super().__init__("; ".join(self.issues))


def build_shared_worker_spec(agent: AgentAuthoring, harness: contracts.Harness) -> wire.SharedWorkerAgentSpec:
    """Turn an authored Agent into its shared-worker spec, or list every reason it cannot have one."""

    if issues := list(_authoring_issues(agent, harness)):
        raise SharedWorkerAgentError(issues)
    spec = wire.SharedWorkerAgentSpec(
        agent=_agent_config(agent),
        sandbox=_sandbox_spec(harness.sandbox),
        mcp_servers=tuple(_mcp_server(name, source) for name, source in harness.mcps.items()),
        connectors=tuple(_connector(slot) for slot in harness.connectors),
    )
    try:
        compile_shared_worker_spec(spec, agent_name=agent.name, capability_provider_id=_CHECK_CAPABILITY_PROVIDER_ID)
    except (SdkError, ValueError) as error:
        raise SharedWorkerAgentError([str(error)]) from error
    return spec


def compile_shared_worker_spec(
    spec: wire.SharedWorkerAgentSpec,
    *,
    agent_name: str,
    capability_provider_id: str,
    session_id: str | None = None,
) -> tuple[WorkflowHarnessDefinition, contracts.Sandbox]:
    """Compile a spec with the same compiler as a code-defined Agent, in the calling process."""

    agent, harness = to_authoring(spec, agent_name=agent_name, session_id=session_id)
    definition = assemble.compile_harness_definition(
        agent._to_agent_config(),
        harness,
        permission_mode=agent.permission_mode,
        capability_provider_id=capability_provider_id,
    )
    # A spec has no field that could name code; this keeps that true if the compiler ever
    # learns to produce a code-backed capability from data.
    if code_backed := [c.binding_id for c in definition.capabilities if c.kind in ("tool", "hook")]:
        raise SharedWorkerAgentError([f"the compiled Agent binds code capabilities {code_backed}"])
    return definition, harness.sandbox


def to_authoring(
    spec: wire.SharedWorkerAgentSpec,
    *,
    agent_name: str,
    session_id: str | None = None,
) -> tuple[AgentAuthoring, contracts.Harness]:
    """The authoring objects a spec stands for, as the worker rebuilds them for one Session."""

    config = spec.agent
    agent = AgentAuthoring(
        model=config.model,
        name=agent_name,
        instructions=config.instructions,
        description=config.description,
        temperature=config.temperature,
        reasoning_effort=config.reasoning_effort,
        permission_mode=config.permission_mode,
        auto_compact_threshold=config.auto_compact_threshold,
        max_iterations=config.max_iterations,
        first_output_timeout_seconds=config.first_output_timeout_seconds,
        builtins=None if config.builtins is None else authoring_types.Builtins.model_validate(config.builtins),
        permission_policy=(
            None if config.permission_policy is None else PermissionPolicy.model_validate(config.permission_policy)
        ),
    )
    harness = contracts.Harness(
        sandbox=_sandbox(spec.sandbox, session_id=session_id),
        mcps={
            server.name: McpHttpSourceConfiguration(
                url=server.url,
                disabled_tools=list(server.disabled_tools),
                startup_timeout_seconds=server.startup_timeout_seconds,
                tool_timeout_seconds=server.tool_timeout_seconds,
            )
            for server in spec.mcp_servers
        },
        connectors=[
            connector_decorator.connector(
                connector.connector_name,
                auto_auth=connector.auto_auth,
                credentials_name=connector.credentials_name,
                allow_mcp_ui=connector.allow_mcp_ui,
            )
            for connector in spec.connectors
        ],
    )
    return agent, harness


def has_code(agent: AgentAuthoring, harness: contracts.Harness) -> bool:
    """Whether the Agent needs more than the control plane's typed configuration to run.

    True for the author's code (tools, Hooks, guardrails, subagents, a response format, a custom
    Sandbox), files (skills), and settings that configuration cannot carry (a custom completion,
    another provider, Bashkit credentials, an MCP server's auth environment variables). Settings it
    carries but the shared worker refuses, such as a privileged Sandbox, are the control plane's to check.
    """
    return any(_uncarried_issues(agent, harness))


def _authoring_issues(agent: AgentAuthoring, harness: contracts.Harness) -> Iterator[str]:
    yield from _uncarried_issues(agent, harness)
    yield from _platform_authority_issues(harness)


def _uncarried_issues(agent: AgentAuthoring, harness: contracts.Harness) -> Iterator[str]:
    if harness.tools:
        yield "custom tools need the author's code; expose them through a remote MCP server instead"
    if harness.hooks:
        yield "Hooks need the author's code"
    if harness.guardrails:
        yield "guardrails need the author's code"
    if agent.subagents or agent.subagent_policy is not None:
        yield "subagents need the author's code"
    if agent.response_format is not None:
        yield "response_format needs the author's code"
    if harness.skills or harness.skill_discovery is not None:
        yield "skills are not supported on the shared worker yet"
    if agent.completion is not None:
        yield "completion= is not supported; use the default Mistral provider"
    elif agent.provider != authoring_types.LLMProvider.MISTRAL:
        # Every other provider reads its API key from an environment variable.
        yield f"provider {str(agent.provider)!r} needs an API key secret; only the Mistral provider is supported"
    yield from _uncarried_sandbox_issues(harness.sandbox)
    yield from _uncarried_secret_issues(harness.secrets)
    for name, source in harness.mcps.items():
        yield from _mcp_issues(name, source)


def _platform_authority_issues(harness: contracts.Harness) -> Iterator[str]:
    # The control plane refuses these too: its typed configuration carries them.
    sandbox = harness.sandbox
    if isinstance(sandbox, contracts.MistralSandbox):
        # These would act with the platform's sandbox account, on behalf of any tenant.
        if sandbox.pre_provisioned_sandbox_id is not None:
            yield "MistralSandbox(pre_provisioned_sandbox_id=...) is not supported"
        if sandbox.privileged:
            yield "MistralSandbox(privileged=True) is not supported"
        if sandbox.docker_daemon_enabled:
            yield "MistralSandbox(docker_daemon_enabled=True) is not supported"
    if harness.connector_discovery is not None:
        # The spec names each connector; it has no field for a selection resolved per Session.
        yield "all_connectors() is not supported on the shared worker yet; name each connector"
    for slot in harness.connectors:
        if slot.run_as == RunAs.DEPLOYMENT:
            yield (
                f"connector {slot.connector_name!r} runs as the deployment, which on the shared worker is the "
                "platform; let it run as the executing user"
            )


def _uncarried_sandbox_issues(sandbox: contracts.Sandbox) -> Iterator[str]:
    if type(sandbox) not in _SUPPORTED_SANDBOXES:
        supported = ", ".join(sandbox_type.__name__ for sandbox_type in _SUPPORTED_SANDBOXES)
        yield f"{type(sandbox).__name__} is not supported; use one of {supported}"
        return
    if sandbox.hooks:
        yield "Sandbox Hooks need the author's code"
    if isinstance(sandbox, contracts.BashkitSandbox) and not sandbox.block_private_ips:
        yield "BashkitSandbox(block_private_ips=False) would reach the platform's private network"
    if isinstance(sandbox, contracts.MistralSandbox):
        # The worker opens no outbound network for a Mistral sandbox.
        if sandbox.network.mode != "none":
            yield f"MistralSandbox(network=Network.{sandbox.network.mode}()) is not supported"
        if sandbox.egress is not None:
            yield "MistralSandbox(egress=...) is not supported"
        # A header binding needs an open network, and the worker does not run Sandbox Proxy yet.
        for binding in sandbox.header_bindings:
            yield f"MistralSandbox(header_bindings=[{type(binding).__name__}(...)]) is not supported"


def _uncarried_secret_issues(secrets: dict[str, SecretOrigin]) -> Iterator[str]:
    # The spec has no secret bindings.
    for name in secrets:
        yield f"secret {name!r} is an agents.MistralSecret, which needs a secret binding"


def _mcp_issues(name: str, source: McpHttpSourceConfiguration) -> Iterator[str]:
    if source.auth_header_env_vars:
        yield f"MCP server {name!r} reads auth headers from environment variables, which needs a secret"
    unsupported = [
        field
        for field in ("id", "name", "namespace", "model_access")
        if getattr(source, field) != getattr(_DEFAULT_MCP, field)
    ]
    if unsupported:
        yield f"MCP server {name!r} sets {', '.join(unsupported)}, which the shared worker does not support yet"


def _agent_config(agent: AgentAuthoring) -> wire.SharedWorkerAgentConfig:
    return wire.SharedWorkerAgentConfig(
        model=agent.model,
        instructions=agent.instructions,
        description=agent.description,
        temperature=agent.temperature,
        reasoning_effort=agent.reasoning_effort,
        permission_mode=agent.permission_mode,
        auto_compact_threshold=agent.auto_compact_threshold,
        max_iterations=agent.max_iterations,
        first_output_timeout_seconds=agent.first_output_timeout_seconds,
        # Left out when default, so the spec stays the same for every Agent that does not change them.
        builtins=None if agent.builtins == authoring_types.Builtins() else agent.builtins.model_dump(mode="json"),
        permission_policy=None if agent.permission_policy is None else agent.permission_policy.model_dump(mode="json"),
    )


def _sandbox_spec(sandbox: contracts.Sandbox) -> wire.SharedWorkerSandbox:
    if isinstance(sandbox, contracts.BashkitSandbox):
        # The authored instance id is not kept: the worker names each workspace after its Session.
        network = sandbox.network
        return wire.SharedWorkerBashkitSandbox(
            access=sandbox.access,
            network=(
                None
                if network.mode == "none"
                else wire.SharedWorkerBashkitNetwork(allow=network.hosts, allow_all=network.mode == "all")
            ),
        )
    if isinstance(sandbox, contracts.MistralSandbox):
        return wire.SharedWorkerMistralSandbox(access=sandbox.access, **_explicit_mistral_sandbox_values(sandbox))
    return wire.SharedWorkerNoSandbox()


def _explicit_mistral_sandbox_values(sandbox: contracts.MistralSandbox) -> dict[str, Any]:
    # A MistralSandbox resolves every value the author left out from the settings of the process
    # that builds it, here the deploy machine. The spec leaves those out, so the worker applies its own.
    return {name: value for name, value in sandbox.authored_settings.items() if name in _MISTRAL_SANDBOX_FIELDS}


def _mcp_server(name: str, source: McpHttpSourceConfiguration) -> wire.SharedWorkerMcpServer:
    return wire.SharedWorkerMcpServer(
        name=name,
        url=source.url,
        disabled_tools=tuple(source.disabled_tools),
        startup_timeout_seconds=source.startup_timeout_seconds,
        tool_timeout_seconds=source.tool_timeout_seconds,
    )


def _connector(slot: connector_decorator.ConnectorSlot) -> wire.SharedWorkerConnector:
    return wire.SharedWorkerConnector(
        connector_name=slot.connector_name,
        auto_auth=slot.auto_auth,
        credentials_name=slot.credentials_name,
        allow_mcp_ui=slot.allow_mcp_ui,
    )


def _sandbox(spec: wire.SharedWorkerSandbox, *, session_id: str | None) -> contracts.Sandbox:
    if isinstance(spec, wire.SharedWorkerBashkitSandbox):
        # A Bashkit workspace is a directory on the worker host named after the instance id. On a
        # worker shared across tenants, each Session gets its own.
        network = (
            None
            if spec.network is None
            else Network.all()
            if spec.network.allow_all
            else Network.allow(hosts=spec.network.allow)
        )
        return contracts.BashkitSandbox(instance_id=session_id, access=spec.access, network=network)
    if isinstance(spec, wire.SharedWorkerMistralSandbox):
        if spec.sandbox_proxy is not None:
            raise ValueError("the shared worker does not run Sandbox Proxy yet")
        return contracts.MistralSandbox(**spec.model_dump(exclude={"kind", "sandbox_proxy"}, exclude_none=True))
    return contracts.NoSandbox()


__all__ = [
    "SharedWorkerAgentError",
    "build_shared_worker_spec",
    "compile_shared_worker_spec",
    "to_authoring",
]
