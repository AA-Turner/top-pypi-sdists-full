import os
import socket
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, Any, Self

import structlog
from mistralai.extra.workflows.encoding.config import (
    BlobStorageConfig as BlobStorageConfigBase,
)
from mistralai.extra.workflows.encoding.config import (
    PayloadCompressionConfig as PayloadCompressionConfigBase,
)
from mistralai.extra.workflows.encoding.config import (
    PayloadEncryptionConfig as PayloadEncryptionConfigBase,
)
from mistralai.extra.workflows.encoding.config import (
    PayloadOffloadingConfig as PayloadOffloadingConfigBase,
)
from pydantic import AliasChoices, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.main import PydanticBaseSettingsSource

from mistralai.workflows.core.logging import LogFormat, LoggerConfig, LogLevel, setup_logging
from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v1.workflow import DeploymentName, LocationType

logger = structlog.getLogger(__name__)

env_file = ".env" if os.environ.get("PYTEST_VERSION") is None else ".env.test"


class DetectEnvConflict:
    """Annotation marker to enable env/dotenv conflict detection on a field."""


def _mask_value(value: str | None) -> str | None:
    if value is None:
        return None
    if len(value) <= 4:
        return "..."
    return "..." + value[-4:]


class _EnvDotenvConflictDetector(PydanticBaseSettingsSource):
    """Detects conflicts between .env file values and environment variables for specific fields.

    For each monitored field, builds a list of possible source data keys (field name + validation
    aliases) and reports a conflict when any key appears in both sources with different values.
    """

    def __init__(self, settings_cls: type[BaseSettings], field_names: list[str]) -> None:
        super().__init__(settings_cls)
        self._field_groups = [self._derive_keys(settings_cls, name) for name in field_names]

    @staticmethod
    def _derive_keys(settings_cls: type[BaseSettings], field_name: str) -> list[str]:
        keys = [field_name]
        field_info = settings_cls.model_fields.get(field_name)
        if field_info is not None and isinstance(field_info.validation_alias, AliasChoices):
            for choice in field_info.validation_alias.choices:
                if isinstance(choice, str) and choice not in keys:
                    keys.append(choice)
        return keys

    def get_field_value(self, field: Any, field_name: str) -> tuple[Any, str, bool]:
        return None, field_name, False

    def _find_value(self, data: dict[str, Any], keys: list[str]) -> tuple[str | None, Any]:
        for key in keys:
            if key in data:
                return key, data[key]
        return None, None

    def __call__(self) -> dict[str, Any]:
        env_data = self.settings_sources_data.get("EnvSettingsSource", {})
        dotenv_data = self.settings_sources_data.get("DotEnvSettingsSource", {})
        for keys in self._field_groups:
            env_key, env_val = self._find_value(env_data, keys)
            dotenv_key, dotenv_val = self._find_value(dotenv_data, keys)
            if env_key is not None and dotenv_key is not None and env_val != dotenv_val:
                logger.warning(
                    "Value mismatch between .env file and environment variable, "
                    "the environment variable value will take precedence",
                    env_variable=env_key,
                    env_variable_value=_mask_value(env_val),
                    dotenv_variable=dotenv_key,
                    dotenv_variable_value=_mask_value(dotenv_val),
                    env_file=env_file,
                )
        return {}


class _ConflictDetectionMixin:
    @classmethod
    def _get_conflict_detection_fields(cls) -> list[str]:
        if not issubclass(cls, BaseSettings):
            raise TypeError(f"{cls.__name__} must be a subclass of BaseSettings")
        fields: list[str] = []
        for name, field_info in cls.model_fields.items():
            for meta in field_info.metadata:
                if isinstance(meta, DetectEnvConflict):
                    fields.append(name)
                    break
        return fields

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            _EnvDotenvConflictDetector(settings_cls, cls._get_conflict_detection_fields()),
        )


class OtelRedactionMode(StrEnum):
    """Client-side redaction policy applied to spans before OTLP export.

    - DEFAULT: content-oriented regex policy; scans string values and redacts
      matched secrets/PII substrings while preserving keys and structure.
    - STRICT: key-oriented policy; redacts whole values for sensitive keys and
      non-primitive values (destructive, high recall).
    - NONE: no redaction.
    """

    DEFAULT = auto()
    NONE = auto()
    STRICT = auto()


class EventsApiVersion(StrEnum):
    """Which event route the worker publishes over.

    - V1: legacy event route.
    - V2: v2 event route, falling back to v1 when a v2 publish is not possible.
    - V2_ONLY: v2 event route with no fallback — any v1 emit raises (for v2 integration tests).
    """

    V1 = "v1"
    V2 = "v2"
    V2_ONLY = "v2-only"


class CommonConfig(_ConflictDetectionMixin, BaseSettings):
    app_name: str = "mistral-workflows"
    app_version: str = "0.0.0"
    log_format: LogFormat = LogFormat.CONSOLE
    log_level: LogLevel = LogLevel.INFO

    otel_enabled: bool = True
    # Independent per-signal OTLP export toggles, gated under the otel_enabled master switch.
    mistral_workflows_otel_traces_export: bool = True
    mistral_workflows_otel_metrics_export: bool = True
    mistral_workflows_otel_logs_export: bool = True
    # For backward compatibility; will be deprecated
    otel_endpoint: str | None = None
    otel_traces_endpoint: str | None = None
    otel_metrics_endpoint: str | None = None
    otel_logs_endpoint: str | None = None
    otel_sample_rate: float = 1.0
    otel_export_interval_ms: int = 30000
    temporal_runtime_metrics_buffer_size: int = 30000
    temporal_runtime_metrics_drain_interval_s: float = 5.0
    otel_tail_sampling: bool = False
    otel_local: bool = False
    otel_inject_logs: bool = True
    # Client-side redaction applied to all spans before OTLP export.
    otel_redaction: OtelRedactionMode = OtelRedactionMode.DEFAULT

    ca_bundle: str | None = Field(  # type: ignore[pydantic-alias]
        default=None,
        description="Path to the CA bundle file for TLS verification",
        validation_alias=AliasChoices("CA_BUNDLE", "CURL_CA_BUNDLE"),
    )

    mistral_api_key: Annotated[SecretStr | None, DetectEnvConflict()] = Field(default=None)
    mistral_sa_token_path: Annotated[str | None, DetectEnvConflict()] = Field(
        default=None,
        description=(
            "Path to a file holding a service-account bearer token, re-read periodically "
            "so rotated tokens are picked up."
        ),
    )

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )


# Hardcoded reserved workflow names that conflict with API endpoints
# This CANNOT be overridden via environment variables for security reasons
RESERVED_WORKFLOW_NAMES: frozenset[str] = frozenset(
    {"executions", "schedules", "definitions", "internal", "webhooks", "archive", "unarchive"}
)
RESERVED_UPDATE_NAMES: frozenset[str] = frozenset({"__submit_input"})

RESERVED_QUERY_NAMES: frozenset[str] = frozenset({"__get_pending_inputs"})

INTERNAL_ACTIVITY_PREFIX: str = "__internal__"

RESERVED_INPUT_ATTRIBUTE_PREFIX: str = "__internal_"

# Search-key size limits (RFC-402), shared by SDK validation/extraction and the abraxas API.
MAX_SEARCH_KEYS: int = 20
MAX_SEARCH_KEY_CHARS: int = 256
MAX_SEARCH_KEY_VALUE_CHARS: int = 8 * 1024  # 8 KiB


class ReservedExtraFieldsAttribute(StrEnum):
    """Reserved attribute names injected via extra_fields (pydantic extras).

    These attributes are injected by the system and should not be used by the user.
    All values must be prefixed with RESERVED_INPUT_ATTRIBUTE_PREFIX.
    """

    # TODO: once nuage-v1 is cleaned up, we can remove this
    EXPERIMENTAL_IDENTITY = f"{RESERVED_INPUT_ATTRIBUTE_PREFIX}experimental_identity"


class TemporalConfig(_ConflictDetectionMixin, BaseSettings):
    server_url: str = Field(
        default="localhost:7233",
    )
    namespace: str = Field(
        default="mistral-workflows",
    )
    api_key: Annotated[SecretStr | None, DetectEnvConflict()] = Field(
        default=None,
    )
    task_queue: str = Field(default="default")  # Allow override
    tls: bool = False
    http_proxy_target_host: str | None = Field(
        default=None,
        description="Target host for the HTTP CONNECT proxy (e.g. 'proxy.example.com:8080')",
    )
    http_proxy_basic_auth_user: str | None = Field(
        default=None,
        description="Basic auth username for the HTTP CONNECT proxy",
    )
    http_proxy_basic_auth_pass: SecretStr | None = Field(
        default=None,
        description="Basic auth password for the HTTP CONNECT proxy",
    )

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="TEMPORAL_",
        env_parse_none_str="null",
    )


class BlobStorageConfig(BlobStorageConfigBase, BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )


class PayloadOffloadingConfig(PayloadOffloadingConfigBase, BaseSettings):
    storage_config: BlobStorageConfig | None = None


class PayloadEncryptionConfig(PayloadEncryptionConfigBase, BaseSettings):
    pass


class PayloadCompressionConfig(PayloadCompressionConfigBase, BaseSettings):
    pass


class AgentConfig(_ConflictDetectionMixin, BaseSettings):
    llm_rate_limit: RateLimit | None = None
    mistral_client_server: str | None = None
    mistral_client_server_url: str | None = None
    mistral_client_url_params: dict[str, str] | None = None
    mistral_client_timeout_ms: int | None = None
    mistral_client_api_key: Annotated[SecretStr | None, DetectEnvConflict()] = Field(
        default=None,
        description="API key for Mistral client",
    )
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
        env_nested_delimiter="__",
    )


class WorkerVersioningConfig(BaseSettings):
    enabled: bool = Field(default=False)
    # Temporal deployment name used for WorkerDeploymentVersion. This is the name that
    # Temporal uses to match pollers to registered versions. In controller mode it comes
    # from TEMPORAL_DEPLOYMENT_NAME ({namespace}/{resource-name}); in manual mode from
    # DEPLOYMENT_NAME. This is independent of WorkerConfig.deployment_name which is used
    # for the heartbeat/internal Workflows API.
    deployment_name: str | None = Field(default=None)
    build_id: str | None = Field(
        default=None,
        validation_alias="BUILD_ID",
    )
    auto_register_as_current: bool | None = Field(
        default=None,
        validation_alias="WORKER_AUTO_REGISTER_AS_CURRENT",
    )

    @model_validator(mode="after")
    def configure_versioning(self) -> "WorkerVersioningConfig":
        """Infer worker versioning behaviour from environment and config values."""
        controller_deployment = os.environ.get("TEMPORAL_DEPLOYMENT_NAME")
        controller_build_id = os.environ.get("TEMPORAL_WORKER_BUILD_ID")
        is_managed_by_controller = bool(controller_deployment and controller_build_id)

        auto_register_override = self.auto_register_as_current

        if is_managed_by_controller:
            # Use the controller's deployment name (TEMPORAL_DEPLOYMENT_NAME) for Temporal
            # versioning. The controller registers versions under this name, so the worker
            # must poll under the same name for Temporal to match pollers to versions.
            self.deployment_name = controller_deployment
            self.build_id = controller_build_id
            self.enabled = True
            if self.auto_register_as_current:
                logger.warning(
                    "Ignoring WORKER_AUTO_REGISTER_AS_CURRENT=true: controller manages version promotion",
                    deployment_name=self.deployment_name,
                )
            self.auto_register_as_current = False
            logger.info(
                "Worker managed by Temporal Worker Controller",
                deployment_name=self.deployment_name,
                build_id=self.build_id,
                auto_register=self.auto_register_as_current,
            )
            return self

        # manual / local mode
        if self.deployment_name and self.build_id:
            self.enabled = True
            if auto_register_override is not None:
                self.auto_register_as_current = auto_register_override
            else:
                self.auto_register_as_current = True

            logger.info(
                "Worker in manual mode with versioning enabled",
                deployment_name=self.deployment_name,
                build_id=self.build_id,
                auto_register=self.auto_register_as_current,
            )
            return self

        if self.enabled:
            logger.warning(
                "Worker versioning enabled but deployment name or build ID missing; disabling versioning",
                deployment_name=self.deployment_name,
                build_id=self.build_id,
            )

        self.enabled = False
        self.auto_register_as_current = False
        return self

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )


def _detect_location_type() -> LocationType:
    if os.environ.get("KUBERNETES_SERVICE_HOST"):
        return LocationType.k8s
    return LocationType.local


def _detect_k8s_namespace() -> str | None:
    try:
        return Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read_text().strip()
    except OSError:
        return None


class DeploymentLocationConfig(BaseSettings):
    location_type: LocationType = Field(
        default_factory=_detect_location_type,
        description="Where this deployment is running: 'local', 'k8s', or 'managed'. "
        "Auto-detected from KUBERNETES_SERVICE_HOST.",
    )
    k8s_cluster: str | None = Field(
        default=None,
        description="K8s cluster name. Must be set explicitly via DEPLOYMENT_LOCATION_K8S_CLUSTER.",
    )
    k8s_namespace: str | None = Field(
        default_factory=_detect_k8s_namespace,
        description="K8s namespace. Auto-read from service account or DEPLOYMENT_LOCATION_K8S_NAMESPACE.",
    )

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="DEPLOYMENT_LOCATION_",
        env_parse_none_str="null",
    )


class GraphConfig(BaseSettings):
    upload_graph: bool = Field(
        default=False,
        description="If True, workflow graphs are generated and uploaded to the API after registration.",
    )
    graph_summarise_enabled: bool = Field(
        default=True,
        description="If True, LLM summaries are generated for workflow graph nodes during upload.",
    )
    graph_summarise_model: str = Field(
        default="mistral-small-latest",
        description="LLM model used to recursively summarise each node in the workflow's AST.",
    )

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )


class WorkerConfig(BaseSettings):
    retry_policy_max_attempts: int = 3
    retry_policy_backoff_coefficient: float = 2.0
    # - The workflow fails on any workflow-level error if set to True. Note: Workflow-level errors differ from
    # activity-level errors and typically result from bugs in the workflow code. By default, workflows do not fail
    #  on errors, enabling you to push code fixes without re-running workflows.
    # More information: https://community.temporal.io/t/workflow-retry-policy-seems-to-not-be-getting-respected/11203/2",
    dangerously_force_fail_workflow_on_error: bool = Field(
        default=False,
        description="☢️ DANGER ZONE ☢️",
        alias="DANGEROUSLY_FORCE_FAIL_WORKFLOW_ON_ERROR",
    )

    server_url: str = Field(  # type: ignore[pydantic-alias]
        default="https://api.mistral.ai",
        validation_alias=AliasChoices("SERVER_URL", "server_url"),
    )
    api_version: str = "v1"
    events_api_version: EventsApiVersion = EventsApiVersion.V1
    allow_multiple_workers: bool = True
    enable_config_discovery: bool = True
    mistral_api_headers: dict[str, str] | None = None

    temporal_payload_offloading: PayloadOffloadingConfig | None = None
    temporal_payload_encryption: PayloadEncryptionConfig | None = None
    temporal_payload_compression: PayloadCompressionConfig | None = None

    activity_attributes_offloading: PayloadOffloadingConfig | None = None

    blob_storage_configs: dict[str, BlobStorageConfig] = Field(default_factory=dict)

    agent: AgentConfig = Field(default_factory=AgentConfig)
    versioning: WorkerVersioningConfig = Field(default_factory=WorkerVersioningConfig)
    deployment_location: DeploymentLocationConfig = Field(default_factory=DeploymentLocationConfig)
    graph: GraphConfig = Field(default_factory=GraphConfig)

    workflow_name_prefix: str = Field(default="", description="If set, all workflows will be prefixed with this value.")
    default_enforce_determinism: bool = Field(
        default=True,
        description="If True, all workflows will be sandboxed by default to enforce deterministic execution.",
    )

    deployment_name: DeploymentName = None
    worker_name: str = Field(default_factory=socket.gethostname)

    max_workflow_task_pollers: int = Field(default=5, ge=2)
    max_activity_task_pollers: int = Field(default=5, ge=1)

    health_server_host: str = "localhost"
    health_server_port: int | None = None

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
        env_nested_delimiter="__",
    )

    @model_validator(mode="after")
    def default_agent_server_url(self) -> "WorkerConfig":
        if not self.agent.mistral_client_server_url:
            self.agent.mistral_client_server_url = self.server_url
        return self

    @model_validator(mode="after")
    def warn_determinism_disabled(self) -> "WorkerConfig":
        if not self.default_enforce_determinism:
            logger.warning(
                "Worker configured with default determinism enforcement disabled. "
                "This may lead to non-deterministic behavior and replay failures.",
            )
        return self


class AppConfig(BaseSettings):
    common: CommonConfig = Field(default_factory=CommonConfig)
    worker: WorkerConfig = Field(default_factory=WorkerConfig)
    temporal: TemporalConfig = Field(default_factory=TemporalConfig)

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )

    @property
    def otel_headers(self) -> str | None:
        """Generate OTEL headers with Mistral API key as bearer token if available."""
        if self.common.mistral_api_key and self.common.mistral_api_key.get_secret_value():
            return f"Authorization=Bearer {self.common.mistral_api_key.get_secret_value()}"
        return None

    def validate_for_worker_startup(self) -> None:
        if not self.worker.deployment_name and self.get_effective_task_queue() == "default":
            raise ValueError(
                "DEPLOYMENT_NAME is required. "
                "Set it to a stable identifier for this deployment (e.g. 'invoice-parser')."
            )
        if self.worker.deployment_name == "default":
            logger.warning(
                "DEPLOYMENT_NAME is set to 'default'; this is valid but may conflict with other "
                "deployments that rely on the default task queue"
            )

    def get_effective_task_queue(self, raise_on_conflict: bool = False) -> str:
        deployment_name = self.worker.deployment_name
        task_queue = self.temporal.task_queue

        if not deployment_name:
            return task_queue
        if task_queue == "default" or task_queue == deployment_name:
            return deployment_name
        if not raise_on_conflict:
            return deployment_name
        raise WorkflowsException(
            code=ErrorCode.WORKER_RUNTIME_CONFIG_ERROR,
            message=(
                f"TEMPORAL_TASK_QUEUE ({task_queue!r}) conflicts with DEPLOYMENT_NAME ({deployment_name!r}). "
                "They must be the same value, or leave TEMPORAL_TASK_QUEUE unset "
                "to let it be derived from DEPLOYMENT_NAME."
            ),
        )

    @model_validator(mode="after")
    def inject_defaults(self) -> Self:
        has_temporal_key = self.temporal.api_key and self.temporal.api_key.get_secret_value()
        has_mistral_key = self.common.mistral_api_key and self.common.mistral_api_key.get_secret_value()
        if not has_temporal_key and has_mistral_key:
            self.temporal.api_key = self.common.mistral_api_key
        if not self.worker.agent.mistral_client_api_key and has_mistral_key:
            self.worker.agent.mistral_client_api_key = self.common.mistral_api_key
        return self


def _get_or_load_config() -> AppConfig:
    """Read and initialize the application configuration."""
    # Load configuration from environment/file
    config = AppConfig()

    # Set OTEL_EXPORTER_OTLP_CERTIFICATE if CA_BUNDLE is set to enable TLS verification for OpenTelemetry
    if config.common.ca_bundle is not None:
        os.environ["OTEL_EXPORTER_OTLP_CERTIFICATE"] = config.common.ca_bundle

    # Set OTEL_EXPORTER_OTLP_HEADERS if Mistral API key is available
    if config.otel_headers is not None:
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = config.otel_headers

    # Set up structured logging with OpenTelemetry trace injection if enabled
    if not structlog.is_configured():
        setup_logging(
            log_level=config.common.log_level,
            log_format=config.common.log_format,
            app_version=config.common.app_version,
            inject_otel_trace=config.common.otel_enabled and config.common.otel_inject_logs,
            extra_config=[
                # noisy
                LoggerConfig(
                    name="httpx",
                    level=LogLevel.WARNING,
                ),
                LoggerConfig(
                    name="httpcore",
                    level=LogLevel.WARNING,
                ),
                LoggerConfig(
                    name="asyncio",
                    level=LogLevel.WARNING,
                ),
                LoggerConfig(
                    name="aiocache",
                    level=LogLevel.WARNING,
                ),
                LoggerConfig(
                    name="urllib3",
                    level=LogLevel.WARNING,
                ),
            ],
        )

    logger.info("Configuration loaded", config=config.model_dump())
    return config


config = _get_or_load_config()
