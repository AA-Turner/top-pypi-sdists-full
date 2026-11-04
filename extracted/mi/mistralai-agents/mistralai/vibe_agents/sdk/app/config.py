from __future__ import annotations

import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import timedelta
from enum import StrEnum
from functools import cache, lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self, cast
from urllib.parse import urlsplit, urlunsplit

from pydantic import AliasChoices, Field, SecretStr, ValidationError, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from mistralai.client import SERVER_GLOBAL, SERVERS
from mistralai.vibe_agents.sdk.app._unused_env import check_environment

if TYPE_CHECKING:
    from mistralai.workflows.core.auth import TokenProvider

PROJECT_RUNTIME_KEY = "[tool.mistralai.agents].runtime"
PROJECT_ENTRYPOINT_KEY = "[tool.mistralai.agents].entrypoint"
# The Mistral API root, without /v1. MISTRAL_API_URL is canonical; the other two are deprecated aliases.
MISTRAL_API_URL_ENV_VARS = ("MISTRAL_API_URL", "MISTRAL_SERVER_URL", "SERVER_URL")
# OTel service.name for managed-agent Studio telemetry. The managed deployment does not set APP_NAME.
MANAGED_AGENT_SERVICE_NAME = "mistralai-agents"

DEFAULT_SESSION_LIFETIME_SECONDS = 86400
"""How long a Session may live by default, and so how long Koyeb keeps its sandbox."""

MANAGED_MAX_LIFETIME_LIMIT_SECONDS = 604800
"""The longest lifetime limit a worker Mistral operates may set: one week."""
MANAGED_MAX_IDLE_TIMEOUT_SECONDS = 86400
"""The longest idle limit a worker Mistral operates may set: 24 hours."""
SELF_HOSTED_MAX_SESSION_LIMIT_SECONDS = 31536000
"""The longest lifetime or idle limit a self-hosted worker may set: one year."""


def is_managed_worker(env: Mapping[str, str] | None = None) -> bool:
    """Whether Mistral operates this worker, as opposed to a self-hosted one."""
    # The aeon operator sets this sentinel on every managed worker; the Workflows SDK reads it the same way.
    from mistralai.workflows.protocol.v1.workflow import MANAGED_K8S_CLUSTER_SENTINEL  # noqa: PLC0415

    return (os.environ if env is None else env).get("DEPLOYMENT_LOCATION_K8S_CLUSTER") == MANAGED_K8S_CLUSTER_SENTINEL


def mistral_api_url(names: tuple[str, ...] = MISTRAL_API_URL_ENV_VARS) -> str | None:
    """Return the first non-empty Mistral API root URL among ``names``, without a trailing slash."""
    for name in names:
        if value := os.environ.get(name, "").strip():
            return value.rstrip("/")
    return None


def mistral_api_http_proxy() -> str | None:
    """The proxy for Mistral API requests, from ``MISTRAL_API_HTTP_PROXY``.

    A Sandbox Proxy sets it in a sandbox, where ``MISTRAL_API_KEY`` is a proxy credential that only
    this proxy exchanges for a real one. It is not ``HTTPS_PROXY``, so other traffic stays direct.
    """
    return os.environ.get("MISTRAL_API_HTTP_PROXY", "").strip() or None


class OtelRedactionMode(StrEnum):
    """Client-side redaction applied to Studio GenAI spans before export.

    - DEFAULT: content-oriented regex policy (redacts matched secrets/PII in values).
    - STRICT: key-oriented policy (redacts whole values for sensitive keys).
    - NONE: no redaction.

    Values mirror the Workflows OTel redaction modes so a shared env var parses either.
    """

    DEFAULT = "default"
    STRICT = "strict"
    NONE = "none"


@cache
def check_environment_once() -> None:
    """Warn once per process about ``AGENTS_SDK_`` variables no setting reads, or refuse them in strict mode.

    Not cached when it raises, so every later settings read refuses too.
    """

    check_environment(settings_classes())


class _CheckedSettings(BaseSettings):
    """Base of every SDK settings class, so whichever is built first checks the environment."""

    def __init__(self, *args: Any, **values: Any) -> None:
        # Before validation, so strict mode raises UnusedEnvironmentError itself, not a ValidationError.
        check_environment_once()
        super().__init__(*args, **values)


def _sandbox_alias(name: str) -> AliasChoices:
    return AliasChoices(f"AGENTS_SDK_KOYEB_SANDBOX_{name}", f"NUAGE_KOYEB_SANDBOX_{name}")


def _koyeb_runtime_alias(name: str, *fallbacks: str) -> AliasChoices:
    return AliasChoices(f"AGENTS_SDK_KOYEB_SANDBOX_{name}", f"NUAGE_KOYEB_SANDBOX_{name}", *fallbacks)


class MistralSandboxSettings(_CheckedSettings):
    """Environment defaults for the SDK-owned managed sandbox."""

    model_config = SettingsConfigDict(extra="ignore")

    # Mistral's public sandbox image (infra/docker/agents-sdk-public-sandbox), so that any Koyeb
    # organization can pull it without a registry secret. Pinned by digest, so the image changes
    # only with an SDK release.
    image: str = Field(  # type: ignore[pydantic-alias]
        default=(
            "europe-west4-docker.pkg.dev/mistral-ci/public/agents-sdk-sandbox:2026.10.23-main-48608-dc30038"
            "@sha256:27874779c5fa7cb7d3fa0a23a61a61fb6c367766c04c821077021295ac755e8a"
        ),
        validation_alias=_sandbox_alias("IMAGE"),
    )
    instance_type: str = Field(default="medium", validation_alias=_sandbox_alias("INSTANCE_TYPE"))  # type: ignore[pydantic-alias]
    region: str = Field(default="nl-north-1", validation_alias=_sandbox_alias("REGION"))  # type: ignore[pydantic-alias]
    name_prefix: str = Field(default="unknown", validation_alias=_sandbox_alias("NAME_PREFIX"))  # type: ignore[pydantic-alias]
    # Koyeb deletes the sandbox this long after it is created; a Session may live this long, so
    # Koyeb does not delete a sandbox under a Session that still runs.
    ttl_seconds: int = Field(  # type: ignore[pydantic-alias]
        default=DEFAULT_SESSION_LIFETIME_SECONDS, validation_alias=_sandbox_alias("TTL_SECONDS")
    )
    idle_timeout_seconds: int = Field(default=0, validation_alias=_sandbox_alias("IDLE_TIMEOUT_SECONDS"))  # type: ignore[pydantic-alias]
    default_exec_timeout_seconds: int = Field(  # type: ignore[pydantic-alias]
        default=30, validation_alias=_sandbox_alias("DEFAULT_EXEC_TIMEOUT_SECONDS")
    )
    privileged: bool = Field(default=False, validation_alias=_sandbox_alias("PRIVILEGED"))  # type: ignore[pydantic-alias]
    docker_daemon_enabled: bool = Field(default=False, validation_alias=_sandbox_alias("DOCKER_DAEMON_ENABLED"))  # type: ignore[pydantic-alias]
    docker_daemon_network_mode: str = Field(  # type: ignore[pydantic-alias]
        default="auto", validation_alias=_sandbox_alias("DOCKER_DAEMON_NETWORK_MODE")
    )
    enable_light_sleep: bool = Field(default=True, validation_alias=_sandbox_alias("ENABLE_LIGHT_SLEEP"))  # type: ignore[pydantic-alias]
    setup_script: str | None = Field(default=None, validation_alias=_sandbox_alias("SETUP_SCRIPT"))  # type: ignore[pydantic-alias]
    setup_script_timeout_seconds: int = Field(  # type: ignore[pydantic-alias]
        default=300, validation_alias=_sandbox_alias("SETUP_SCRIPT_TIMEOUT_SECONDS")
    )
    readiness_max_retries: int = Field(default=10, validation_alias=_sandbox_alias("READINESS_MAX_RETRIES"))  # type: ignore[pydantic-alias]
    readiness_interval_seconds: float = Field(  # type: ignore[pydantic-alias]
        default=2.0, validation_alias=_sandbox_alias("READINESS_INTERVAL_SECONDS")
    )
    readiness_probe_timeout_seconds: int = Field(  # type: ignore[pydantic-alias]
        default=5, validation_alias=_sandbox_alias("READINESS_PROBE_TIMEOUT_SECONDS")
    )
    wait_ready_timeout_seconds: int = Field(default=300, validation_alias=_sandbox_alias("WAIT_READY_TIMEOUT_SECONDS"))  # type: ignore[pydantic-alias]
    enable_mesh: bool = Field(default=False, validation_alias=_sandbox_alias("ENABLE_MESH"))  # type: ignore[pydantic-alias]
    pre_provisioned_sandbox_id: str | None = Field(  # type: ignore[pydantic-alias]
        default=None,
        validation_alias=_sandbox_alias("PRE_PROVISIONED_SANDBOX_ID"),
    )

    @field_validator("setup_script", "pre_provisioned_sandbox_id", mode="before")
    @classmethod
    def _empty_string_is_unset(cls, value: object) -> object:
        return None if value == "" else value


@dataclass(frozen=True, slots=True)
class KoyebApiAccess:
    """The API host and bearer token one Koyeb SDK call uses."""

    host: str
    token: str


class KoyebSandboxRuntimeSettings(_CheckedSettings):
    """Worker-only credentials and environment for the SDK-owned Koyeb provider.

    A Koyeb API token, when set, talks to Koyeb directly. Without one, the same Koyeb API is reached
    through Mistral Cloud as the caller's Mistral identity: the worker's service account, or whoever
    holds MISTRAL_API_KEY.
    """

    model_config = SettingsConfigDict(extra="ignore", populate_by_name=True)

    mistral_cloud_api_url: str = Field(
        default="https://api.cloud.mistral.ai",
        validation_alias=AliasChoices("AGENTS_SDK_MISTRAL_CLOUD_API_URL"),
    )
    api_host: str = Field(
        default="https://app.koyeb.com",
        validation_alias=_koyeb_runtime_alias("API_HOST", "VIBE_HARNESS_KOYEB_SANDBOX_API_HOST"),
    )
    api_token: SecretStr | None = Field(
        default=None,
        validation_alias=_koyeb_runtime_alias(
            "API_TOKEN",
            "VIBE_HARNESS_KOYEB_SANDBOX_API_TOKEN",
            "KOYEB_API_TOKEN",
            "KOYEB_API_KEY",
        ),
    )
    registry_secret: str | None = Field(
        default=None,
        validation_alias=_koyeb_runtime_alias(
            "REGISTRY_SECRET",
            "VIBE_HARNESS_KOYEB_SANDBOX_REGISTRY_SECRET",
        ),
    )
    extra_env: dict[str, str] = Field(
        default_factory=dict,
        validation_alias=AliasChoices(
            "AGENTS_SDK_KOYEB_SANDBOX_EXTRA_ENV",
            "AGENTS_SDK_SANDBOX_EXTRA_ENV",
            "NUAGE_SANDBOX_EXTRA_ENV",
        ),
    )

    def has_credential(self) -> bool:
        return self._koyeb_token() is not None or _mistral_token_provider() is not None

    def api_access(self, host: str | None = None) -> KoyebApiAccess:
        """Select the backend from the credentials, or keep `host`, the backend an existing sandbox was created on."""
        cloud_host = self.mistral_cloud_api_url.rstrip("/")
        koyeb_token = self._koyeb_token()
        uses_koyeb = koyeb_token is not None if host is None else host != cloud_host
        if uses_koyeb:
            if koyeb_token is None:
                raise RuntimeError(
                    f"This sandbox was created through the Koyeb API at {host}; "
                    "set AGENTS_SDK_KOYEB_SANDBOX_API_TOKEN to reach it"
                )
            return KoyebApiAccess(host=host or self.api_host, token=koyeb_token)
        provider = _mistral_token_provider()
        if provider is None:
            raise RuntimeError(
                "MistralSandbox requires MISTRAL_API_KEY, a worker service-account token, "
                "or AGENTS_SDK_KOYEB_SANDBOX_API_TOKEN"
            )
        # Read on every call: a worker's service-account token rotates, and a sandbox outlives one token.
        return KoyebApiAccess(host=cloud_host, token=provider.get_token())

    def _koyeb_token(self) -> str | None:
        # An empty variable still parses as a SecretStr, and Koyeb then rejects every request.
        if self.api_token is None:
            return None
        return self.api_token.get_secret_value().strip() or None


def _mistral_token_provider() -> TokenProvider | None:
    from mistralai.workflows.core.auth import get_token_provider  # noqa: PLC0415

    return get_token_provider()


class SandboxProxyBootstrapSettings(_CheckedSettings):
    """Where a Workflow worker sends Sandbox Proxy bootstrap requests, when it differs from the Workflows API."""

    model_config = SettingsConfigDict(extra="ignore", populate_by_name=True)

    url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("AGENTS_SDK_SANDBOX_PROXY_BOOTSTRAP_URL", "MISTRAL_PUBLIC_API_URL"),
    )


class SandboxProxySettings(_CheckedSettings):
    """Legacy worker configuration retained while existing proxy activities drain."""

    model_config = SettingsConfigDict(extra="ignore", populate_by_name=True)

    url: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "AGENTS_SDK_SANDBOX_PROXY_URL",
            "VIBE_HARNESS_SANDBOX_PROXY_URL",
            "NUAGE_SANDBOX_PROXY_URL",
            "GITHUB_INTEGRATION_GIT_PROXY_PUBLIC_URL",
            "GIT_HTTP_PROXY_PUBLIC_URL",
        ),
    )
    ca_cert: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "AGENTS_SDK_SANDBOX_PROXY_CA_CERT",
            "VIBE_HARNESS_SANDBOX_PROXY_CA_CERT",
            "NUAGE_SANDBOX_PROXY_CA_CERT",
            "GITHUB_INTEGRATION_GIT_PROXY_CA_CERT",
            "GIT_HTTP_PROXY_CA_CERT",
        ),
    )
    signing_secret: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "AGENTS_SDK_SANDBOX_PROXY_TOKEN_SIGNING_SECRET",
            "VIBE_HARNESS_SANDBOX_PROXY_TOKEN_SIGNING_SECRET",
            "NUAGE_SANDBOX_PROXY_TOKEN_SIGNING_SECRET",
            "GITHUB_INTEGRATION_GIT_CREDENTIAL_TOKEN_SIGNING_SECRET",
            "GITHUB_INTEGRATION_GIT_PROXY_TOKEN_SIGNING_SECRET",
            "GIT_HTTP_PROXY_TOKEN_SIGNING_SECRET",
        ),
    )

    def require(self) -> tuple[str, str, str]:
        missing = [
            name
            for name, value in (
                ("URL", self.url),
                ("CA certificate", self.ca_cert),
                ("signing secret", self.signing_secret),
            )
            if value is None
        ]
        if missing:
            raise RuntimeError(f"Sandbox proxy is incomplete; missing: {', '.join(missing)}")
        return (
            cast(str, self.url),
            cast(SecretStr, self.ca_cert).get_secret_value(),
            cast(SecretStr, self.signing_secret).get_secret_value(),
        )


# How long an approval or a client tool call waits for the app's answer, unless
# AGENTS_SDK_CALLBACK_TIMEOUT_SECONDS sets another value.
DEFAULT_CALLBACK_TIMEOUT = timedelta(hours=1)
# Koyeb create may consume its whole start-to-close window on every attempt. Setup then
# runs as its own activity. The provisioning budget must outlast both, plus proxy and hooks,
# or eager Session open fails while those provider operations would still succeed.
# Setup retries on a new sandbox share this budget.
KOYEB_SANDBOX_CREATE_ATTEMPT_TIMEOUT = timedelta(minutes=15)
KOYEB_SANDBOX_CREATE_MAX_ATTEMPTS = 6
KOYEB_SANDBOX_SETUP_ACTIVITY_TIMEOUT = timedelta(hours=1)
KOYEB_SANDBOX_SETUP_FRESH_SANDBOX_ATTEMPTS = 3
_SANDBOX_PROVISIONING_OTHER_STEPS_BUDGET = timedelta(minutes=15)
DEFAULT_SANDBOX_PROVISIONING_TIMEOUT = (
    KOYEB_SANDBOX_CREATE_ATTEMPT_TIMEOUT * KOYEB_SANDBOX_CREATE_MAX_ATTEMPTS
    + KOYEB_SANDBOX_SETUP_ACTIVITY_TIMEOUT
    + _SANDBOX_PROVISIONING_OTHER_STEPS_BUDGET
)


class TelemetrySettings(_CheckedSettings):
    # Kept apart from AppSettings so the HTTP clients can read the switch without AppSettings'
    # cross-field validation, which a client that never runs a session has no reason to satisfy.
    model_config = SettingsConfigDict(env_prefix="AGENTS_SDK_", extra="ignore")

    # Off means: emit no SDK telemetry, and ask the control plane to flag the events it emits for this
    # caller so they stay out of product analytics. Set it in tests and CI.
    telemetry_enabled: bool = True
    telemetry_server_url: str = Field(
        default_factory=lambda: mistral_api_url() or SERVERS[SERVER_GLOBAL],
        validation_alias="AGENTS_SDK_TELEMETRY_SERVER_URL",
    )


class AppSettings(TelemetrySettings):
    # Config for the file-defined-agent runtime, owned by this SDK (env prefix AGENTS_SDK_). Kept
    # separate from the internal Nuage settings so the SDK does not depend on Nuage config surface.
    model_config = SettingsConfigDict(env_prefix="AGENTS_SDK_", extra="ignore")

    # Temporal's execution timeout, across every Continue-As-New run. A backstop only: the
    # lifetime and idle limits below end the Session first, through its normal terminal path.
    execution_timeout_seconds: float = Field(default=604800.0, gt=0.0)
    # Longest a Session may live, counted from its first run: at most one week on a managed worker,
    # one year on a self-hosted one, whatever the execution timeout.
    lifetime_limit_seconds: float = Field(
        default=float(DEFAULT_SESSION_LIFETIME_SECONDS), gt=0.0, le=float(SELF_HOSTED_MAX_SESSION_LIMIT_SECONDS)
    )
    # Longest a Session may stay idle; deployment configuration only, never set per Session. Idle
    # means no Turn runs or waits to run, or every unfinished Action of the running Turn waits for
    # the user or the app. A Session is never idle while one of its direct children is starting or
    # running a Turn. At most 24 hours on a managed worker, one year on a self-hosted one.
    idle_timeout_seconds: float = Field(default=14400.0, gt=0.0, le=float(SELF_HOSTED_MAX_SESSION_LIMIT_SECONDS))
    # How long a Session stopped at a limit may take to end before it is force-ended.
    limit_grace_seconds: float = Field(default=300.0, gt=0.0)
    # How long an approval or a client tool call waits for the app's answer before the call fails.
    # Must stay strictly below execution_timeout so the wait ends here, not at the Temporal timeout.
    callback_timeout_seconds: float = Field(default=DEFAULT_CALLBACK_TIMEOUT.total_seconds(), gt=0.0)
    # Bounds the whole sandbox provisioning sequence (create, proxy, setup, hooks) across
    # provider retries. The default outlasts every Koyeb create attempt and the setup
    # activity. Exceeding it fails provisioning like any other setup error.
    sandbox_provisioning_timeout_seconds: float = Field(
        default=DEFAULT_SANDBOX_PROVISIONING_TIMEOUT.total_seconds(), gt=0.0
    )
    steer_input_enabled: bool = Field(default=True)
    # Only workers Mistral operates export to the internal Mimir the agent-runtime alerts read.
    runtime_metrics_enabled: bool = False
    # Match the gateway settings used by the Nuage worker without importing Nuage configuration.
    completion_gateway_api_base: str = Field(  # type: ignore[pydantic-alias]
        default_factory=lambda: mistral_api_url() or "",
        validation_alias=AliasChoices("AGENTS_SDK_COMPLETION_GATEWAY_API_BASE", "MISTRAL_PROVIDER_API_BASE"),
    )
    completion_gateway_api_key_env_var: str = Field(  # type: ignore[pydantic-alias]
        default="MISTRAL_API_KEY",
        validation_alias=AliasChoices(
            "AGENTS_SDK_COMPLETION_GATEWAY_API_KEY_ENV_VAR",
            "MISTRAL_PROVIDER_API_KEY_ENV_VAR",
        ),
    )
    # Authenticate completions as the Session's caller via identity headers rather than with an API
    # key of the worker's own. Only the internal completion gateway honours those headers, so this
    # stays off by default for `agents serve`, which runs against a personal key and no gateway.
    # Aliased to the name the Nuage worker already uses, so one deployment-level switch covers both
    # backends without this SDK reading Nuage settings.
    use_identity_headers: bool = Field(  # type: ignore[pydantic-alias]
        default=False,
        validation_alias=AliasChoices("AGENTS_SDK_USE_IDENTITY_HEADERS", "MISTRAL_USE_IDENTITY_HEADERS"),
    )
    albe_api_url: str = Field(  # type: ignore[pydantic-alias]
        default="http://albe",
        validation_alias=AliasChoices("AGENTS_SDK_ALBE_API_URL", "ALBE_API_URL"),
    )
    albe_internal_service_name: str = Field(  # type: ignore[pydantic-alias]
        default="nuage-workflow",
        validation_alias=AliasChoices("AGENTS_SDK_ALBE_INTERNAL_SERVICE_NAME", "ALBE_INTERNAL_SERVICE_NAME"),
    )
    # Kill-switch for Studio GenAI tracing, on by default like Workflows telemetry.
    studio_tracing_enabled: bool = True
    # Whether GenAI spans carry prompt/response content (redaction still applies).
    studio_tracing_include_content: bool = True
    studio_tracing_redaction: OtelRedactionMode = OtelRedactionMode.DEFAULT
    # The shared worker serves every workspace, so a rollout without Temporal worker versioning
    # would replay all running Sessions on new code. Its deployment sets this, and the worker then
    # refuses to start unversioned.
    require_worker_versioning: bool = False

    @model_validator(mode="after")
    def _validate_limits_end_before_temporal(self) -> Self:
        # Temporal must never be the one to end a Session, even once a stop at a limit takes its
        # whole grace period.
        if self.lifetime_limit_seconds + self.limit_grace_seconds >= self.execution_timeout_seconds:
            raise ValueError(
                "AGENTS_SDK_LIFETIME_LIMIT_SECONDS plus AGENTS_SDK_LIMIT_GRACE_SECONDS must be strictly less than "
                "AGENTS_SDK_EXECUTION_TIMEOUT_SECONDS: set AGENTS_SDK_EXECUTION_TIMEOUT_SECONDS above "
                f"{self.lifetime_limit_seconds + self.limit_grace_seconds:.0f}"
            )
        return self

    @model_validator(mode="after")
    def _validate_managed_worker_limits(self) -> Self:
        # A self-hosted worker may keep Sessions up to a year; Mistral's workers keep the product limits.
        if not is_managed_worker():
            return self
        if self.lifetime_limit_seconds > MANAGED_MAX_LIFETIME_LIMIT_SECONDS:
            raise ValueError(
                f"AGENTS_SDK_LIFETIME_LIMIT_SECONDS is at most {MANAGED_MAX_LIFETIME_LIMIT_SECONDS} on a managed worker"
            )
        if self.idle_timeout_seconds > MANAGED_MAX_IDLE_TIMEOUT_SECONDS:
            raise ValueError(
                f"AGENTS_SDK_IDLE_TIMEOUT_SECONDS is at most {MANAGED_MAX_IDLE_TIMEOUT_SECONDS} on a managed worker"
            )
        return self

    @model_validator(mode="after")
    def _validate_callback_wait_below_execution(self) -> Self:
        if self.callback_timeout_seconds >= self.execution_timeout_seconds:
            raise ValueError("callback_timeout_seconds must be strictly less than execution_timeout_seconds")
        return self

    @model_validator(mode="after")
    def _validate_sandbox_provisioning_below_execution(self) -> Self:
        if self.sandbox_provisioning_timeout_seconds >= self.execution_timeout_seconds:
            raise ValueError(
                "sandbox_provisioning_timeout_seconds must be strictly less than execution_timeout_seconds"
            )
        return self

    @model_validator(mode="after")
    def _validate_identity_headers_name_a_gateway(self) -> Self:
        if self.use_identity_headers and not self.completion_gateway_api_base.strip():
            raise ValueError(
                "AGENTS_SDK_USE_IDENTITY_HEADERS requires AGENTS_SDK_COMPLETION_GATEWAY_API_BASE "
                "(or MISTRAL_PROVIDER_API_BASE, or MISTRAL_API_URL): identity headers replace the completion API key, "
                "and only the internal completion gateway honours them"
            )
        return self

    @property
    def execution_timeout(self) -> timedelta:
        return timedelta(seconds=self.execution_timeout_seconds)

    @property
    def callback_timeout(self) -> timedelta:
        return timedelta(seconds=self.callback_timeout_seconds)

    @property
    def completion_gateway_server_url(self) -> str | None:
        if not self.completion_gateway_api_base:
            return None
        parsed = urlsplit(self.completion_gateway_api_base)
        if not parsed.scheme or not parsed.netloc:
            return self.completion_gateway_api_base.rstrip("/")
        return urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))


class ControlPlaneSettings(_CheckedSettings):
    # Split out of DeploySettings so `serve` can read these without tripping the api-key validator: a
    # Mistral Cloud worker has no API key, and does not register itself.
    model_config = SettingsConfigDict(env_prefix="AGENTS_SDK_", extra="ignore")

    # The public Agents API route, so the SDK works from any network. The same service is also
    # reachable in-cluster on a root-mounted private route; point this at that one only for QA.
    deploy_control_plane_url: str = Field(default="https://api.mistral.ai/v2/agents")
    mistral_api_key: str = Field(  # type: ignore[pydantic-alias]
        default="", validation_alias=AliasChoices("MISTRAL_API_KEY", "PROD_MISTRAL_API_KEY")
    )
    # The release of the code `agents serve` runs, such as the commit an image was built from. A restart
    # with the same configuration and code version keeps its agent. Unset, the SDK hashes the project.
    code_version: str = ""

    @property
    def api_key(self) -> str:
        return self.mistral_api_key.strip()


class AuthenticatedControlPlaneSettings(ControlPlaneSettings):
    """Control plane settings for a command that calls the Agents API, so both values must be set."""

    @model_validator(mode="after")
    def _validate_required_control_plane_settings(self) -> Self:
        if not self.deploy_control_plane_url.strip():
            raise ValueError("AGENTS_SDK_DEPLOY_CONTROL_PLANE_URL must be set")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY must be set")
        return self


class DeploySettings(AuthenticatedControlPlaneSettings):
    deploy_wait_timeout_seconds: float = Field(default=300.0, gt=0.0)
    deploy_poll_interval_seconds: float = Field(default=3.0, gt=0.0)
    # The Runtime API route serving a managed worker's stdout and stderr, read when a deploy fails.
    deploy_runtime_logs_url: str = Field(default=f"{SERVERS[SERVER_GLOBAL]}/v1/runtime/logs")


class SettingsError(ValueError):
    """Raised when the environment does not configure a command; the message names what to set."""


def _load[T: BaseSettings](settings_type: type[T]) -> T:
    try:
        return settings_type()
    except ValidationError as exc:
        raise SettingsError("; ".join(str(item["msg"]).removeprefix("Value error, ") for item in exc.errors())) from exc


def load_control_plane_settings() -> AuthenticatedControlPlaneSettings:
    """The control plane URL and API key, for commands that only call the Agents API.

    Unlike ``load_deploy_settings`` this leaves the deploy-only values unvalidated, so a bad deploy
    timeout does not block a command that never waits on a deploy.
    """
    return _load(AuthenticatedControlPlaneSettings)


def load_deploy_settings() -> DeploySettings:
    return _load(DeploySettings)


class SessionClientSettings(_CheckedSettings):
    """Client-side readiness budget, separate from Workflow and HTTP timeouts."""

    model_config = SettingsConfigDict(env_prefix="AGENTS_SDK_", extra="ignore")

    session_startup_timeout_seconds: float = Field(default=900.0, gt=0.0, allow_inf_nan=False)


class WorkflowsClientSettings(_CheckedSettings):
    # Retry policy the SDK applies to its Workflows API client. get_mistral_client() ships without one,
    # so without this a single transient transport error fails a serve-registration or execution read.
    model_config = SettingsConfigDict(env_prefix="AGENTS_SDK_", extra="ignore")

    retry_initial_interval_ms: int = Field(default=500, gt=0)
    retry_max_interval_ms: int = Field(default=10000, gt=0)
    retry_exponent: float = Field(default=1.5, gt=0.0)
    retry_max_elapsed_time_ms: int = Field(default=60000, gt=0)


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()


def settings_classes() -> tuple[type[BaseSettings], ...]:
    """Every settings class here, so each environment variable they read counts as used."""

    return tuple(
        value
        for value in globals().values()
        if isinstance(value, type) and issubclass(value, BaseSettings) and value.__module__ == __name__
    )


def _read_agents_table(root: Path) -> tuple[dict[str, object], Path] | None:
    pyproject = Path(root) / "pyproject.toml"
    if not pyproject.is_file():
        return None
    try:
        parsed = tomllib.loads(pyproject.read_text())
    except (OSError, tomllib.TOMLDecodeError) as exc:
        # Not ignorable: the unreadable file may be the one declaring the backend or the entrypoint.
        raise ValueError(f"Cannot read {pyproject}: {exc}") from exc
    tool = parsed.get("tool")
    mistralai = tool.get("mistralai") if isinstance(tool, dict) else None
    agents = mistralai.get("agents") if isinstance(mistralai, dict) else None
    if not isinstance(agents, dict):
        return None
    return agents, pyproject


def read_project_entrypoint_from_pyproject(root: Path) -> str | None:
    """Read the ``module:attr`` entrypoint a project declares, or None if it declares none.

    Raises ValueError for an unreadable file or a non-string value; callers choose how to report it.
    """

    table = _read_agents_table(root)
    if table is None:
        return None
    agents, pyproject = table
    declared = agents.get("entrypoint")
    if declared is None:
        return None
    if not isinstance(declared, str) or not declared.strip():
        raise ValueError(f"{PROJECT_ENTRYPOINT_KEY} in {pyproject} must be a non-empty string.")
    return declared.strip()


def reject_project_runtime_declaration(root: Path) -> None:
    """Raise if an agent project still declares a backend to run on.

    There is one runtime, so the key selects nothing. It is an error rather than an ignored leftover
    because a project pinned to the retired `"nuage"` would otherwise come up on the Harness and
    behave unlike what it declares.
    """

    table = _read_agents_table(root)
    if table is None:
        return
    agents, pyproject = table
    if "runtime" not in agents:
        return
    raise ValueError(
        f"{PROJECT_RUNTIME_KEY} in {pyproject} is no longer supported: the SDK runs on the Unified "
        "Harness and there is nothing to select. Remove the key."
    )
