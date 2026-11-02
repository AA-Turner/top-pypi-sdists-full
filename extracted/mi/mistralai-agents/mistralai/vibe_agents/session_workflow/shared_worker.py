"""The Agents shared worker's routing names, and the definition each of its Sessions carries.

The shared worker is one platform deployment, in a reserved Workflows namespace, that runs the
data-only Agents of every workspace. The worker registers these Workflows on this deployment,
and the control plane routes a shared-worker Agent's Sessions to them, so both sides read the
names from here.

The control plane stores a shared-worker Agent in its own typed tables and builds a
``SharedWorkerAgentSpec`` from them for every Session; the worker compiles that spec. The spec is
language-neutral data, and it cannot express what a worker shared across tenants must refuse:
anything that reads the worker's environment, holds a secret, or acts with the platform's
authority. Parsing it is therefore the worker's validation.
"""

import re
from typing import Annotated, Final, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from mistralai.vibe_agents.session_workflow.commands import ReasoningEffort

SHARED_WORKER_DEPLOYMENT_NAME: Final = "shared-agents-worker"

# A reserved namespace only accepts Workflow names with this prefix.
SHARED_WORKFLOW_PREFIX: Final = "__shared-"

# `on_behalf_of` is fixed when a Workflow is registered, and the platform refuses an
# on-behalf-of execution that has no user identity. One Workflow per value lets an Agent that
# needs the executing user's credentials, and one that does not, share the same worker.
SHARED_WORKER_WORKFLOW_NAME: Final = f"{SHARED_WORKFLOW_PREFIX}agents-session"
SHARED_WORKER_ON_BEHALF_OF_WORKFLOW_NAME: Final = f"{SHARED_WORKFLOW_PREFIX}agents-session-obo"
SHARED_WORKER_WORKFLOW_NAMES: Final = frozenset({SHARED_WORKER_WORKFLOW_NAME, SHARED_WORKER_ON_BEHALF_OF_WORKFLOW_NAME})


def shared_worker_workflow_name(*, on_behalf_of: bool) -> str:
    return SHARED_WORKER_ON_BEHALF_OF_WORKFLOW_NAME if on_behalf_of else SHARED_WORKER_WORKFLOW_NAME


# The sandbox tools the model gets; None takes the sandbox's default.
type SandboxAccess = Literal["none", "files", "full"]


class _SpecModel(BaseModel):
    # A field this side does not know fails validation instead of being dropped: a definition
    # from a newer control plane must not run with part of it missing.
    model_config = ConfigDict(extra="forbid", frozen=True)


class SharedWorkerAgentConfig(_SpecModel):
    """The Agent's model and loop settings. The provider is always Mistral."""

    model: str = Field(min_length=1)
    instructions: str | None = None
    description: str | None = None
    temperature: float | None = None
    reasoning_effort: ReasoningEffort | None = None
    permission_mode: Literal["auto", "ask", "deny"] = "auto"
    auto_compact_threshold: int | None = Field(default=None, gt=0)
    max_iterations: int | None = None
    first_output_timeout_seconds: float | None = None
    # The SDK's `Builtins` and `PermissionPolicy`, as JSON: the worker validates them with those models.
    builtins: dict[str, JsonValue] | None = None
    permission_policy: dict[str, JsonValue] | None = None


class SharedWorkerNoSandbox(_SpecModel):
    kind: Literal["none"] = "none"


class SharedWorkerBashkitNetwork(_SpecModel):
    """Outbound network for a Bashkit sandbox. Private IPs stay blocked, and no credential is injected.

    ``allow`` lists exact ``host`` or ``host:port`` entries, as ``agents.Network.allow`` takes them.
    Specs from SDKs before that change listed URL patterns, which a worker now refuses.
    """

    allow: tuple[str, ...] = ()
    allow_all: bool = False

    @model_validator(mode="after")
    def _allow_list_or_all(self) -> Self:
        if self.allow and self.allow_all:
            raise ValueError("allow and allow_all are mutually exclusive")
        return self


class SharedWorkerBashkitSandbox(_SpecModel):
    """A Bashkit sandbox on the worker host. Its workspace is named after the Session."""

    kind: Literal["bashkit"] = "bashkit"
    access: SandboxAccess | None = None
    network: SharedWorkerBashkitNetwork | None = None


class SharedWorkerGitHubProxy(_SpecModel):
    type: Literal["github"] = "github"
    repo_whitelist: tuple[str, ...] = ()
    all_accessible_repos: bool = False
    ttl_seconds: int = 3600
    host: str = "github.com"


class SharedWorkerSandboxProxy(_SpecModel):
    integrations: tuple[SharedWorkerGitHubProxy, ...] = Field(min_length=1)


class SharedWorkerMistralSandbox(_SpecModel):
    """A managed Mistral sandbox. Unset values take the worker's defaults.

    It is never privileged, never runs a Docker daemon and never attaches to an existing
    sandbox: the worker creates it with the platform's sandbox account, for any tenant.
    """

    kind: Literal["mistral"] = "mistral"
    access: SandboxAccess | None = None
    image: str | None = None
    instance_type: str | None = None
    region: str | None = None
    name_prefix: str | None = None
    ttl_seconds: int | None = None
    idle_timeout_seconds: int | None = None
    default_exec_timeout_seconds: int | None = None
    enable_light_sleep: bool | None = None
    setup_script: str | None = None
    setup_script_timeout_seconds: int | None = None
    readiness_max_retries: int | None = None
    readiness_interval_seconds: float | None = None
    readiness_probe_timeout_seconds: int | None = None
    wait_ready_timeout_seconds: int | None = None
    enable_mesh: bool | None = None
    sandbox_proxy: SharedWorkerSandboxProxy | None = None


type SharedWorkerSandbox = Annotated[
    SharedWorkerNoSandbox | SharedWorkerBashkitSandbox | SharedWorkerMistralSandbox,
    Field(discriminator="kind"),
]


class SharedWorkerMcpServer(_SpecModel):
    """A remote MCP server, reached without authentication."""

    name: str = Field(min_length=1)
    url: str = Field(min_length=1)
    disabled_tools: tuple[str, ...] = ()
    startup_timeout_seconds: float = Field(default=30.0, gt=0)
    tool_timeout_seconds: float = Field(default=300.0, gt=0)


class SharedWorkerConnector(_SpecModel):
    """A Mistral connector. It always runs as the executing user."""

    connector_name: str = Field(min_length=1)
    auto_auth: bool = True
    credentials_name: str | None = None
    allow_mcp_ui: bool = False


class SharedWorkerAgentSpec(_SpecModel):
    """Everything the shared worker needs to run one Agent, as language-neutral data."""

    agent: SharedWorkerAgentConfig
    sandbox: SharedWorkerSandbox = Field(default_factory=SharedWorkerNoSandbox)
    mcp_servers: tuple[SharedWorkerMcpServer, ...] = ()
    connectors: tuple[SharedWorkerConnector, ...] = ()

    @model_validator(mode="after")
    def _unique_names(self) -> Self:
        if len({server.name for server in self.mcp_servers}) != len(self.mcp_servers):
            raise ValueError("MCP server names must be unique")
        if len({connector.connector_name for connector in self.connectors}) != len(self.connectors):
            raise ValueError("connector names must be unique")
        return self

    def requires_on_behalf_of(self) -> bool:
        """Whether the Agent needs the executing user's credentials, so routes to the on-behalf-of Workflow."""

        if self.connectors:
            return True
        return isinstance(self.sandbox, SharedWorkerMistralSandbox) and self.sandbox.sandbox_proxy is not None


# A connector or credentials name goes unencoded into a URL path on the platform's API host, so a
# `/`, `?` or `..` would reach another route on it with the executing user's token.
_URL_PATH_SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")


def shared_worker_egress_issues(spec: SharedWorkerAgentSpec) -> list[str]:
    """Every part of the spec that would let a tenant or the model choose where the shared worker connects.

    The shared worker runs inside the platform's network, with platform credentials. Until its
    egress is enforced at the network layer (AGE-1842), it runs only Agents whose connections all
    go to platform-fixed hosts: the completion gateway, the Mistral API for connectors, and Koyeb.
    The worker refuses any other spec, whoever started the Session, and the control plane refuses
    it at deploy, so such an Agent gets a deployment of its own instead. Remote MCP servers and
    Bashkit come back with that network policy.
    """

    issues = [
        f"MCP server {server.name!r}: the shared worker does not call remote MCP servers yet, "
        "since it would call a tenant-chosen URL from inside the platform's network"
        for server in spec.mcp_servers
    ]
    sandbox = spec.sandbox
    if isinstance(sandbox, SharedWorkerBashkitSandbox):
        issues.append(
            "the shared worker does not run a Bashkit sandbox yet: it runs in the worker process, "
            "inside the platform's network"
        )
    if isinstance(sandbox, SharedWorkerMistralSandbox):
        if sandbox.image is not None:
            issues.append(
                "the shared worker runs only its default sandbox image: another image would be pulled "
                "with the platform's registry credentials"
            )
        if sandbox.enable_mesh:
            issues.append("enable_mesh would join the platform's private sandbox network")
    for connector in spec.connectors:
        for name in (connector.connector_name, connector.credentials_name):
            if name is not None and not _URL_PATH_SAFE_NAME.fullmatch(name):
                issues.append(f"connector name {name!r} may use only letters, digits, '_', '.' and '-'")
    return issues


__all__ = [
    "SHARED_WORKER_DEPLOYMENT_NAME",
    "SandboxAccess",
    "SHARED_WORKER_ON_BEHALF_OF_WORKFLOW_NAME",
    "SHARED_WORKER_WORKFLOW_NAME",
    "SHARED_WORKER_WORKFLOW_NAMES",
    "SHARED_WORKFLOW_PREFIX",
    "SharedWorkerAgentConfig",
    "SharedWorkerAgentSpec",
    "SharedWorkerBashkitNetwork",
    "SharedWorkerBashkitSandbox",
    "SharedWorkerConnector",
    "SharedWorkerGitHubProxy",
    "SharedWorkerMcpServer",
    "SharedWorkerMistralSandbox",
    "SharedWorkerNoSandbox",
    "SharedWorkerSandbox",
    "SharedWorkerSandboxProxy",
    "shared_worker_egress_issues",
    "shared_worker_workflow_name",
]
