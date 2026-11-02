import re
from typing import Literal
from uuid import UUID

from pydantic import ConfigDict, Field, JsonValue, field_validator
from pydantic_core import PydanticCustomError

from mistralai.vibe.harness.app_server.session import PermissionPolicy
from mistralai.vibe_agents._internal.wire_models import ForwardCompatibleModel
from mistralai.vibe_agents.session_workflow.inputs import SubagentPolicy

# Session input ID -> JSON Schema of the value a caller must supply.
SessionInputSchemas = dict[str, dict[str, JsonValue]]


class _APIModel(ForwardCompatibleModel):
    model_config = ConfigDict(populate_by_name=True)


def _is_none(value: object) -> bool:
    return value is None


def _is_empty(value: list[object]) -> bool:
    return not value


class HarnessConfigInput(_APIModel):
    model_name: str
    instructions: str | None = None
    permission_mode: str = "auto"
    # Left out when unset: older control planes refuse it as an unknown field.
    permission_policy: PermissionPolicy | None = Field(default=None, exclude_if=_is_none)
    # None leaves the threshold to the model's profile. The server field is also
    # `int | None`, so the wire shape is unchanged.
    auto_compact_threshold: int | None = None
    max_iterations: int | None = None
    # Left out when unset: the control plane refuses a field it does not know, so an older one
    # still accepts a deploy that does not use them.
    temperature: float | None = Field(default=None, exclude_if=_is_none)
    thinking: str | None = Field(default=None, exclude_if=_is_none)
    first_output_timeout_seconds: float | None = Field(default=None, exclude_if=_is_none)
    # The Agent's `Builtins` as JSON; left out when the Agent keeps the defaults.
    builtins: dict[str, JsonValue] | None = Field(default=None, exclude_if=_is_none)

    @field_validator("permission_policy", mode="before")
    @classmethod
    def reject_unknown_permission_policy_fields(cls, value: object) -> object:
        if value is None:
            return None

        return PermissionPolicy.model_validate(value, extra="forbid")


class SkillInput(_APIModel):
    name: str
    body: str
    description: str = ""


class ConnectorInput(_APIModel):
    connector_name: str
    run_as: Literal["auto", "deployment"] = "auto"
    auto_auth: bool = True
    credentials_name: str | None = None
    allow_mcp_ui: bool = False


# The one place the secret-binding contract is written down. The CLI parser and the
# control plane's request schema both validate against these, so a binding rejected at
# deploy time is exactly the set the platform would reject, and neither side drifts.
ENV_VAR_NAME_PATTERN = r"^[A-Za-z_][A-Za-z0-9_]*$"
ENV_VAR_NAME_MAX_LENGTH = 256
# Only the workspace scope is offered: a deployed worker runs as a service account, whose
# user scope is empty. Dots and `@version` suffixes are refused because the platform's
# renderer cannot resolve them, so they must fail here rather than at boot.
SECRET_REFERENCE_PATTERN = r"^secret:workspace:[a-zA-Z0-9_][a-zA-Z0-9_-]*$"  # noqa: S105 - a grammar, not a secret
# Keys the platform sets on every worker, or that override one it sets (MISTRAL_API_URL and
# MISTRAL_SERVER_URL win over SERVER_URL). Binding one would either collide or silently lose to the
# platform's own value, so the platform refuses them.
RESERVED_ENV_VAR_NAMES = frozenset(
    {
        "DEPLOYMENT_NAME",
        "TEMPORAL_TASK_QUEUE",
        "TEMPORAL_DEPLOYMENT_NAME",
        "TEMPORAL_WORKER_BUILD_ID",
        "SERVER_URL",
        "MISTRAL_API_URL",
        "MISTRAL_SERVER_URL",
        "DEPLOYMENT_LOCATION_K8S_CLUSTER",
        "DEPLOYMENT_LOCATION_LOCATION_TYPE",
        "MISTRAL_SA_TOKEN_PATH",
        "MISTRAL_API_KEY",
        "ENTRYPOINT",
    }
)

_ENV_VAR_NAME_RE = re.compile(ENV_VAR_NAME_PATTERN)
_SECRET_REFERENCE_RE = re.compile(SECRET_REFERENCE_PATTERN)


def env_var_name_error(env_var_name: str) -> str | None:
    """Return why this env var name cannot be bound, or None when it can.

    Returns a message rather than raising so each caller can frame it: the CLI names the
    flag, the API returns a field error.
    """
    if len(env_var_name) > ENV_VAR_NAME_MAX_LENGTH:
        return f"must be at most {ENV_VAR_NAME_MAX_LENGTH} characters"
    if _ENV_VAR_NAME_RE.fullmatch(env_var_name) is None:
        return "must be a letter or '_' followed by letters, digits, or '_'"
    if env_var_name in RESERVED_ENV_VAR_NAMES:
        return f"is reserved by the platform: {', '.join(sorted(RESERVED_ENV_VAR_NAMES))}"
    return None


def is_valid_secret_reference(reference: str) -> bool:
    return _SECRET_REFERENCE_RE.fullmatch(reference) is not None


# The platform names its own agents in a dotted namespace, such as `vibe.code`: the namespace is
# the product surface that owns the agent. The Agent constructor and the control plane both refuse
# a dotted name, so a name is refused while the agent is written, and again by the platform for a
# client that skips the SDK. The namespace holds because the separator is a character no user
# agent name can contain, so it needs no list of names.
PLATFORM_AGENT_NAMESPACE_SEPARATOR = "."


def is_reserved_agent_name(agent_name: str) -> bool:
    return PLATFORM_AGENT_NAMESPACE_SEPARATOR in agent_name


def reserved_agent_name_message(agent_name: str) -> str:
    return (
        f"Agent name {agent_name!r} is reserved by the platform: "
        f"names that contain {PLATFORM_AGENT_NAMESPACE_SEPARATOR!r} belong to platform agents"
    )


# Never interpolates the rejected value: it may be a secret pasted by mistake, and this
# text reaches terminals, CI logs, and API error bodies.
SECRET_REFERENCE_ERROR = (
    "must point at a secret reference, written as 'secret:workspace:<NAME>', not at a "  # noqa: S105 - an error message, not a secret
    "secret value. <NAME> starts with a letter, digit, or '_' and continues with letters, "
    "digits, '_', or '-'; dots and '@version' suffixes are not supported. If you passed "
    "the secret's name on its own, prefix it with 'secret:workspace:'."
)


class SecretBindingInput(_APIModel):
    """One env var on the deployed worker, bound to a workspace secret.

    Only the reference crosses the wire. The platform resolves it at boot, in the pod, so
    the secret's value never reaches the control plane or this client.
    """

    env_var_name: str
    reference: str

    @field_validator("env_var_name")
    @classmethod
    def _check_env_var_name(cls, value: str) -> str:
        problem = env_var_name_error(value)
        if problem is not None:
            raise PydanticCustomError("secret_binding_env_var_name", f"env_var_name {problem}.")
        return value

    @field_validator("reference")
    @classmethod
    def _check_reference(cls, value: str) -> str:
        if not is_valid_secret_reference(value):
            raise PydanticCustomError("secret_binding_reference", f"reference {SECRET_REFERENCE_ERROR}")
        return value


class ConnectorSelectionInput(_APIModel):
    """The connector set the agent asks for when it names no connectors.

    Sent so that the deployment records what ``all_connectors()`` requests. Without it
    an administrator reading the deployment would see no connectors at all.
    """

    type: Literal["all"] = "all"
    exclude: list[str] = []
    max_connectors: int | None = None
    auto_auth: bool = True
    allow_mcp_ui: bool = False


class AgentConfigurationRequest(_APIModel):
    """The agent's configuration, the same fields in a deploy and in a registration.

    Each field is left out when unused, so a request that does not use it reaches an older control
    plane, which refuses a field it does not know.
    """

    description: str | None = Field(default=None, exclude_if=_is_none)
    harness_config: HarnessConfigInput | None = Field(default=None, exclude_if=_is_none)
    sandbox_config: "SandboxConfigInput | None" = Field(default=None, exclude_if=_is_none)
    skills: list[SkillInput] = Field(default=[], exclude_if=_is_empty)
    connectors: list[ConnectorInput] = Field(default=[], exclude_if=_is_empty)
    connector_selection: ConnectorSelectionInput | None = Field(default=None, exclude_if=_is_none)
    mcp_servers: list["PlainMCPServerInput"] = Field(default=[], exclude_if=_is_empty)


class CreateManagedAgentRequest(AgentConfigurationRequest):
    agent_name: str
    workflow_name: str
    github_url: str
    revision: str | None = None
    working_dir: str | None = None
    dockerfile_path: str | None = None
    is_hardened: bool = True
    secret_bindings: list[SecretBindingInput] = []
    required_session_inputs: SessionInputSchemas | None = None
    # The policy of a Session that starts without its own; None leaves such Sessions without
    # subagents. Left out when None, so an agent without subagents deploys to an older control plane.
    default_subagent_policy: SubagentPolicy | None = Field(default=None, exclude_if=lambda value: value is None)


class ManagedAgentResponse(_APIModel):
    agent_id: UUID
    agent_name: str
    service_id: str
    chat_url: str | None = None
    console_url: str | None = None


class SandboxImageInput(_APIModel):
    image: str | None = None
    instance_type: str | None = None
    region: str | None = None
    name_prefix: str | None = None


class BashkitNetworkInput(_APIModel):
    allow: list[str] = []
    allow_all: bool = False


class GitHubProxyInput(_APIModel):
    type: Literal["github"] = "github"
    repo_whitelist: list[str] = []
    all_accessible_repos: bool = False
    ttl_seconds: int = 3600
    host: str = "github.com"


class SandboxProxyInput(_APIModel):
    integrations: list[GitHubProxyInput]


class SandboxConfigInput(_APIModel):
    """The Agent's sandbox. Unset values take the defaults of the worker that makes the sandbox."""

    # Left out at their defaults: an older control plane refuses a field it does not know.
    kind: Literal["mistral", "bashkit"] = Field(default="mistral", exclude_if=lambda kind: kind == "mistral")
    image: SandboxImageInput | None = None
    pre_provisioned_sandbox_id: str | None = None
    privileged: bool | None = None
    docker_daemon_enabled: bool | None = None
    docker_daemon_network_mode: str | None = None
    ttl_seconds: int | None = None
    idle_timeout_seconds: int | None = None
    default_exec_timeout_seconds: int | None = None
    enable_light_sleep: bool | None = None
    setup_script: str | None = None
    setup_script_timeout_seconds: int | None = None
    readiness_max_retries: int | None = None
    readiness_interval_seconds: float | None = None
    readiness_probe_timeout_seconds: float | None = None
    wait_ready_timeout_seconds: float | None = None
    enable_mesh: bool | None = None
    sandbox_proxy: SandboxProxyInput | None = Field(default=None, exclude_if=_is_none)
    bashkit_network: BashkitNetworkInput | None = Field(default=None, exclude_if=_is_none)
    access: Literal["none", "files", "full"] | None = Field(default=None, exclude_if=_is_none)


class PlainMCPServerInput(_APIModel):
    """A remote MCP server reached without authentication."""

    name: str
    url: str
    disabled_tools: list[str] = []
    startup_timeout_sec: float
    tool_timeout_sec: float


class AgentDetailResponse(_APIModel):
    """One catalog agent plus the live status of its deployment.

    ``is_active`` means a worker is polling the deployment. The rollout and build
    fields are only populated for deployments built from a repository, and the
    server resolves them fail-open, so ``None`` means "not known" rather than
    "not happening".
    """

    agent_id: UUID
    agent_name: str
    deployment_name: str
    source: Literal["workspace", "builtin"] = "workspace"
    is_active: bool
    managed: bool
    rollout_status: str | None = None
    message: str | None = None
    build_phase: str | None = None
    build_message: str | None = None
    chat_url: str | None = None
    console_url: str | None = None
    # None means the worker never reported its declarations.
    required_session_inputs: SessionInputSchemas | None = None
    # The managed deployment's Mistral Cloud service, whose logs the Runtime API serves. Only
    # `GET /agents/{agent_id}` returns it; the by-name lookup leaves it None.
    service_id: str | None = None


class RegisterAgentRequest(AgentConfigurationRequest):
    agent_name: str
    workflow_name: str
    # None lets the control plane choose the task queue, and the response carries its choice.
    deployment_name: str | None = None
    required_session_inputs: SessionInputSchemas | None = None
    # The policy of a Session that starts without its own; None leaves such Sessions without
    # subagents. Left out when None, so an agent without subagents registers with an older control plane.
    default_subagent_policy: SubagentPolicy | None = Field(default=None, exclude_if=lambda value: value is None)
    # The worker makes its own sandbox from its code, so the control plane makes none from the sandbox
    # configuration it stores. Left out when false, so a registration without configuration still
    # reaches an older control plane, which refuses the field as unknown.
    makes_own_sandbox: bool = Field(default=False, exclude_if=lambda value: not value)


class AgentResponse(_APIModel):
    """An agent with its task queue, and links to it in the public UIs when the control plane has them."""

    agent_id: UUID
    agent_name: str
    workflow_name: str
    deployment_name: str
    # A plain string: a source a newer control plane adds must not fail the whole list page.
    source: str = "workspace"
    is_active: bool
    managed: bool
    chat_url: str | None = None
    console_url: str | None = None


class ListAgentsResponse(_APIModel):
    items: list[AgentResponse]
    next_cursor: str | None = Field(default=None, validation_alias="nextCursor")


__all__ = [
    "AgentDetailResponse",
    "AgentResponse",
    "BashkitNetworkInput",
    "ConnectorInput",
    "CreateManagedAgentRequest",
    "GitHubProxyInput",
    "HarnessConfigInput",
    "ListAgentsResponse",
    "ManagedAgentResponse",
    "PlainMCPServerInput",
    "PLATFORM_AGENT_NAMESPACE_SEPARATOR",
    "RegisterAgentRequest",
    "SandboxConfigInput",
    "SandboxImageInput",
    "SandboxProxyInput",
    "SecretBindingInput",
    "SessionInputSchemas",
    "SECRET_REFERENCE_PATTERN",
    "ENV_VAR_NAME_PATTERN",
    "SkillInput",
    "is_reserved_agent_name",
    "reserved_agent_name_message",
]
