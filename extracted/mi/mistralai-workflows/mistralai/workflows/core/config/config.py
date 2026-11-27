import logging
import os
import socket
from collections.abc import Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import StrEnum, auto
from pathlib import Path
from threading import Lock
from types import MappingProxyType
from typing import Annotated, Any, Callable, Iterator, Self, TypedDict, cast
from urllib.parse import urlsplit, urlunsplit

import structlog
import temporalio.exceptions
import temporalio.workflow
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
    PayloadEncryptionMode,
)
from mistralai.extra.workflows.encoding.config import (
    PayloadOffloadingConfig as PayloadOffloadingConfigBase,
)
from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    Field,
    SecretStr,
    ValidatorFunctionWrapHandler,
    field_validator,
    model_validator,
)
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, EnvSettingsSource, InitSettingsSource, NoDecode, SettingsConfigDict
from pydantic_settings.main import PydanticBaseSettingsSource

from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.logging import (
    LogFormat,
    LoggerConfig,
    LogLevel,
    route_logs_to_host_logging,
    setup_logging,
)
from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v1.events import WorkflowEventCategory
from mistralai.workflows.protocol.v1.worker import PayloadEncryptionLevel
from mistralai.workflows.protocol.v1.workflow import DeploymentName, LocationType

logger = get_logger(__name__)

env_file = ".env" if os.environ.get("PYTEST_VERSION") is None else ".env.test"


def _split_comma_separated(value: object) -> object:
    if not isinstance(value, str):
        return value
    items = [item.strip() for item in value.split(",") if item.strip()]
    # An empty value is usually a template that rendered to "", not a request for an empty list.
    if not items:
        raise ValueError("must list at least one value")
    return items


# Pair with NoDecode, so pydantic-settings hands over the raw environment string instead of parsing it as JSON.
CommaSeparated = BeforeValidator(_split_comma_separated)


class _DelegatingSettingsSource(PydanticBaseSettingsSource):
    """Wrap a settings source while keeping the name and state pydantic-settings records for it."""

    def __init__(self, source: PydanticBaseSettingsSource) -> None:
        super().__init__(source.settings_cls)
        self.source = source
        self.__name__ = getattr(source, "__name__", type(source).__name__)

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        return self.source.get_field_value(field, field_name)

    def _read_source(self) -> dict[str, Any]:
        self.source._set_current_state(self.current_state)
        self.source._set_settings_sources_data(self.settings_sources_data)
        return self.source()

    def __call__(self) -> dict[str, Any]:
        return self._read_source()


class _FieldNameInitSource(_DelegatingSettingsSource):
    """Accept a field's Python name in code without making it an environment variable name.

    Adding the name to ``AliasChoices`` would also read a bare environment variable of that name.
    """

    def __init__(self, source: PydanticBaseSettingsSource, aliases: Mapping[str, str]) -> None:
        super().__init__(source)
        self._aliases = aliases

    def __call__(self) -> dict[str, Any]:
        data = self._read_source()
        renamed = {name: alias for name, alias in self._aliases.items() if name in data and alias not in data}
        if not renamed:
            return data
        return {renamed.get(key, key): value for key, value in data.items()}


_ignored_foreign_env_vars: set[str] = set()


def _ignore_foreign_bare_model_values(source: PydanticBaseSettingsSource) -> PydanticBaseSettingsSource:
    """Drop a bare variable named after a non-optional nested model unless its value is a JSON object.

    Other software exports such names: coding agents set ``AGENT=claude-code``, which would otherwise fail
    ``WorkerConfig`` with a ``SettingsError``. ``AGENT__<FIELD>`` is a separate key and still applies, and a
    value starting with ``{`` is meant as configuration, so a malformed one still fails. Optional models such
    as ``TEMPORAL_PAYLOAD_ENCRYPTION`` are left alone, so a mistyped encryption setting keeps failing.
    Classes with an env prefix never read bare names.
    """
    if not isinstance(source, EnvSettingsSource) or source.env_prefix:
        return source
    env_vars = dict(source.env_vars)
    for name, field in source.settings_cls.model_fields.items():
        if not (isinstance(field.annotation, type) and issubclass(field.annotation, BaseModel)):
            continue
        key = name if source.case_sensitive else name.lower()
        value = env_vars.get(key)
        if value is None or value.lstrip().startswith("{"):
            continue
        del env_vars[key]
        if key not in _ignored_foreign_env_vars:
            _ignored_foreign_env_vars.add(key)
            logger.warning(
                "Ignoring an environment variable that is not a JSON object, set nested fields as <VARIABLE>__<FIELD>",
                env_variable=key.upper(),
            )
    source.env_vars = env_vars
    return source


class _SdkSettings(BaseSettings):
    """Base for SDK settings classes that adjust their settings sources.

    Override ``_wrap_init_source`` or ``_extra_sources`` rather than ``settings_customise_sources``.
    """

    @classmethod
    def _wrap_init_source(cls, source: PydanticBaseSettingsSource) -> PydanticBaseSettingsSource:
        return source

    @classmethod
    def _extra_sources(cls, settings_cls: type[BaseSettings]) -> tuple[PydanticBaseSettingsSource, ...]:
        return ()

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
            cls._wrap_init_source(init_settings),
            _ignore_foreign_bare_model_values(env_settings),
            _ignore_foreign_bare_model_values(dotenv_settings),
            file_secret_settings,
            *cls._extra_sources(settings_cls),
        )


class _NestedSettings(_SdkSettings):
    """Settings that take values only from code or from the parent's nested names, such as
    ``TEMPORAL_PAYLOAD_ENCRYPTION__MAIN_KEY``.

    These classes have no env prefix, so their own sources would read bare names like ``MAIN_KEY`` or
    ``BUCKET_NAME`` and fill fields the parent left unset.
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (cls._wrap_init_source(init_settings), *cls._extra_sources(settings_cls))


class DetectEnvConflict:
    """Annotation marker to enable env/dotenv conflict detection on a field."""


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
                    dotenv_variable=dotenv_key,
                    env_file=env_file,
                )
        return {}


class _ConflictDetectionMixin(_SdkSettings):
    @classmethod
    def _get_conflict_detection_fields(cls) -> list[str]:
        fields: list[str] = []
        for name, field_info in cls.model_fields.items():
            for meta in field_info.metadata:
                if isinstance(meta, DetectEnvConflict):
                    fields.append(name)
                    break
        return fields

    @classmethod
    def _extra_sources(cls, settings_cls: type[BaseSettings]) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            *super()._extra_sources(settings_cls),
            _EnvDotenvConflictDetector(settings_cls, cls._get_conflict_detection_fields()),
        )


class OtelRedactionMode(StrEnum):
    """Client-side redaction policy applied to spans and log records before OTLP export.

    - DEFAULT: content-oriented regex policy; scans string values (including log
      bodies) and redacts matched secrets/PII substrings while preserving keys
      and structure.
    - STRICT: key-oriented policy; redacts whole values for sensitive keys
      (including `wf.arguments` and `wf.result`), non-primitive values and whole
      log bodies (destructive, high recall).
    - NONE: no redaction.
    """

    DEFAULT = auto()
    NONE = auto()
    STRICT = auto()


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
    otel_traces_endpoint: str | None = None
    otel_metrics_endpoint: str | None = None
    otel_logs_endpoint: str | None = None
    otel_sample_rate: float = 1.0
    otel_export_interval_ms: int = 30000
    temporal_runtime_metrics_buffer_size: int = 30000
    temporal_runtime_metrics_drain_interval_s: float = 5.0
    otel_local: bool = False
    otel_inject_logs: bool = True
    # Client-side redaction applied to all spans and log records before OTLP export.
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

    mtls_client_cert_path: str | None = Field(
        default=None,
        description=(
            "Path to a PEM client certificate chain the worker presents for mTLS on the transport "
            "layer of all worker traffic -- control-plane HTTP, the SDK Mistral clients, and the "
            "Temporal connection. This is independent of the bearer/API-key sent on top of it. Must "
            "be set together with mtls_client_key_path."
        ),
    )
    mtls_client_key_path: str | None = Field(
        default=None,
        description=(
            "Path to the unencrypted PEM private key for mtls_client_cert_path. Temporal's TLSConfig "
            "takes raw key bytes with no passphrase, so an encrypted key is not supported. Must be "
            "set together with mtls_client_cert_path."
        ),
    )

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )

    @model_validator(mode="after")
    def _validate_mtls_client_pair(self) -> Self:
        if bool(self.mtls_client_cert_path) != bool(self.mtls_client_key_path):
            raise ValueError(
                "mtls_client_cert_path and mtls_client_key_path must be set together "
                "(a client certificate is useless without its private key, and vice versa)"
            )
        return self

    @property
    def mtls_client_identity(self) -> tuple[str, str] | None:
        """The (cert, key) pair the worker presents for mTLS, or None when mTLS is off."""
        if self.mtls_client_cert_path and self.mtls_client_key_path:
            return self.mtls_client_cert_path, self.mtls_client_key_path
        return None


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
    tls: bool = False
    tls_server_root_ca_cert_path: str | None = Field(
        default=None,
        description=(
            "Path to a PEM CA certificate used to verify the Temporal server. It supplies a trust "
            "root but does not by itself enable TLS: setting it while tls=False is an error. The CA replaces the "
            "default trust roots rather than adding to them, so it must be the CA that issued the "
            "certificate this client actually sees -- typically a TLS-intercepting proxy's CA."
        ),
    )
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


class BlobStorageConfig(BlobStorageConfigBase, _NestedSettings):
    model_config = SettingsConfigDict(extra="ignore")


class PayloadOffloadingConfig(PayloadOffloadingConfigBase, _NestedSettings):
    storage_config: BlobStorageConfig | None = None


class PayloadEncryptionConfig(PayloadEncryptionConfigBase, _NestedSettings):
    # Event payloads use `mode` by default. `custom_event_mode` overrides it for custom task events only,
    # e.g. `partial` on top of `mode=full` so readers without the key can still read their unmarked fields.
    custom_event_mode: PayloadEncryptionMode | None = None

    @property
    def custom_event_config(self) -> Self:
        """The encryption config to apply to custom task events."""
        if self.custom_event_mode is None:
            return self
        return self.model_copy(update={"mode": self.custom_event_mode, "custom_event_mode": None})


class PayloadCompressionConfig(PayloadCompressionConfigBase, _NestedSettings):
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


class WorkerVersioningConfig(_SdkSettings):
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

    @classmethod
    def _wrap_init_source(cls, source: PydanticBaseSettingsSource) -> PydanticBaseSettingsSource:
        source = super()._wrap_init_source(source)
        return _FieldNameInitSource(source, {"auto_register_as_current": "WORKER_AUTO_REGISTER_AS_CURRENT"})

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


class WorkflowDecoratorConfig(BaseSettings):
    """SDK defaults for workflow definitions before a worker resolves its configuration.

    Only the module-level instance below is used, built without reading the environment. The class
    keeps its settings base because it is part of the public API surface.
    """

    workflow_name_prefix: str = ""
    default_enforce_determinism: bool = True
    versioning: WorkerVersioningConfig = Field(default_factory=WorkerVersioningConfig)

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
        env_nested_delimiter="__",
    )


_workflow_decorator_config = WorkflowDecoratorConfig.model_construct(
    versioning=WorkerVersioningConfig.model_construct(
        enabled=False, deployment_name=None, build_id=None, auto_register_as_current=False
    ),
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


class DeploymentLocationConfig(_SdkSettings):
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


class RemotelyOverridable:
    """Annotation marker: the server may supply this field's default at worker startup.

    The field name doubles as the feature-flag name the server sends, so it must be unique across
    the settings tree.
    """


def _collect_remotely_overridable(root: BaseSettings) -> dict[str, BaseSettings]:
    """Map each remotely overridable field name to the settings instance holding it."""
    targets: dict[str, BaseSettings] = {}
    pending = [root]
    while pending:
        settings = pending.pop()
        for name, field_info in type(settings).model_fields.items():
            value = getattr(settings, name)
            if isinstance(value, BaseSettings):
                pending.append(value)
            if not any(isinstance(meta, RemotelyOverridable) for meta in field_info.metadata):
                continue
            if name in targets:
                raise WorkflowsException(
                    code=ErrorCode.WORKER_RUNTIME_CONFIG_ERROR,
                    message=f"Feature flag {name!r} is declared on more than one settings field",
                )
            targets[name] = settings
    return targets


def adopt_remote_default(settings: BaseSettings, field: str, value: Any) -> None:
    """Write a server-supplied default, unless local configuration already set the field."""
    if field not in settings.model_fields_set:
        setattr(settings, field, value)


def apply_remote_defaults(root: BaseSettings, values: Mapping[str, Any]) -> dict[str, Any]:
    """Apply server-resolved defaults to the marked fields, returning the values that won.

    A `None` value is the server declining to have an opinion, which leaves the SDK default in
    place. Otherwise `model_fields_set` separates a value an environment variable or dotenv entry
    populated from one that fell through to the SDK default, giving the precedence order: explicit
    local configuration, then the server value, then the SDK default.

    Any write marks a field as set, including one from a `model_validator(mode="after")` that
    assigns to `self`. A settings class holding a `RemotelyOverridable` field must therefore never
    self-assign it, or the server value becomes permanently inert.
    """
    if not isinstance(root, BaseSettings):
        root = cast(Any, root).get()
    targets = _collect_remotely_overridable(root)
    effective: dict[str, Any] = {}
    for field, value in values.items():
        settings = targets.get(field)
        if settings is None:
            raise WorkflowsException(
                code=ErrorCode.WORKER_RUNTIME_CONFIG_ERROR,
                message=f"Feature flag {field!r} has no field marked `RemotelyOverridable`",
            )
        if value is not None:
            adopt_remote_default(settings, field, value)
        effective[field] = getattr(settings, field)
    return effective


class GraphConfig(_SdkSettings):
    # upload_graph is remotely defaulted: never assign it in a validator.
    upload_graph: Annotated[bool, RemotelyOverridable()] = Field(
        default=False,
        description="If True, workflow graphs are generated and uploaded to the API after registration.",
    )
    graph_summarise_enabled: bool = Field(
        default=True,
        description="If True, LLM summaries are generated for workflow graph nodes during upload.",
    )
    # Remotely defaulted like upload_graph: this runs a CST parse over customer
    # source in customer-deployed workers, so it must be disableable without a
    # customer redeploy. Never assign it in a validator.
    dataflow_views_enabled: Annotated[bool, RemotelyOverridable()] = Field(
        default=True,
        description="If True, data-flow graph views are generated and uploaded alongside the control-flow view.",
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


_EXPLICIT_HEADER_FIELDS = ("mistral_api_headers", "mistral_api_header_files")
_INIT_SOURCE_NAME = InitSettingsSource.__name__
# Set while AppConfig validates its worker: the parent has already marked which header mappings came
# from code, and the nested WorkerConfig cannot tell them apart from mappings inherited through WORKER.
_resolving_nested_worker_config: ContextVar[bool] = ContextVar("resolving_nested_worker_config", default=False)


def _mark_explicit_headers(values: Mapping[str, Any]) -> dict[str, Any]:
    """Mark header mappings set in code so lower-priority sources replace them instead of merging.

    Pydantic-settings deep-merges plain dictionaries only. Validation turns the proxies back into dictionaries.
    """
    return {
        key: MappingProxyType(value) if key in _EXPLICIT_HEADER_FIELDS and isinstance(value, dict) else value
        for key, value in values.items()
    }


def _section(data: Mapping[str, Any], key: str | None) -> Mapping[str, Any] | None:
    values = data if key is None else data.get(key)
    return values if isinstance(values, Mapping) else None


class _ExplicitHeadersSource(_DelegatingSettingsSource):
    """Mark the header mappings set in code, at the top level or under ``key``."""

    def __init__(self, source: PydanticBaseSettingsSource, key: str | None = None) -> None:
        super().__init__(source)
        self._key = key

    def __call__(self) -> dict[str, Any]:
        data = self._read_source()
        values = _section(data, self._key)
        if values is None:
            return data
        if self._key is None:
            return _mark_explicit_headers(values)
        return {**data, self._key: _mark_explicit_headers(values)}


class _DroppedHeadersWarningSource(PydanticBaseSettingsSource):
    """Log the inherited header names that a mapping set in code drops, at the top level or under ``key``."""

    def __init__(self, settings_cls: type[BaseSettings], key: str | None = None) -> None:
        super().__init__(settings_cls)
        self._key = key

    def get_field_value(self, field: Any, field_name: str) -> tuple[Any, str, bool]:
        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        explicit_values = _section(self.settings_sources_data.get(_INIT_SOURCE_NAME, {}), self._key) or {}
        for field_name in _EXPLICIT_HEADER_FIELDS:
            # A plain dictionary here was inherited through WORKER rather than set in code.
            if field_name not in explicit_values or isinstance(explicit_values[field_name], dict):
                continue
            explicit = explicit_values[field_name] or {}
            inherited = set()
            for source_name, data in self.settings_sources_data.items():
                values = _section(data, self._key) if source_name != _INIT_SOURCE_NAME else None
                if values is not None and isinstance(values.get(field_name), Mapping):
                    inherited.update(values[field_name])
            dropped = sorted(inherited - set(explicit))
            if dropped:
                logger.warning(
                    "Headers set in code replace inherited headers; these inherited headers are not sent",
                    field=field_name,
                    discarded_headers=dropped,
                )
        return {}


class WorkerConfig(_SdkSettings):
    retry_policy_max_attempts: int = 3
    retry_policy_backoff_coefficient: float = 2.0
    # Wait multiplier for the client-side retry `@activity` applies outside a workflow; `None`
    # follows the coefficient above. Separate because Temporal rejects a coefficient below 1.
    local_retry_backoff_coefficient: float | None = None
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
    allow_multiple_workers: bool = True
    enable_config_discovery: bool = True
    mistral_api_headers: dict[str, str] | None = None
    mistral_api_header_files: dict[str, str] | None = Field(
        default=None,
        description=(
            "Like mistral_api_headers, but each value is read from a file, as {header name: file path}. The "
            "files are re-read so rotated values are picked up. Both are the worker's own identity: sent on every "
            "Workflows API and Temporal call it makes as itself, never with an executor's identity."
        ),
    )

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
    # Concurrent gRPC streams the network path to Temporal allows per connection (100 at Cloudflare's
    # edge). Workers warn when their poll streams approach it; set to null where no such limit applies.
    connection_stream_limit: int | None = Field(default=100, gt=0)
    max_concurrent_activities: int = Field(default=100, gt=0)
    # 0 would disable the cache and replay every workflow from history on each task.
    max_cached_workflows: int = Field(default=1000, gt=0)
    # On shutdown the worker stops polling, then gives running activities this long to finish before it
    # cancels them; 0 cancels them at once. Keep it below the platform's SIGTERM-to-SIGKILL delay (30 s
    # by default on Kubernetes), leaving room for the telemetry flush.
    graceful_shutdown_timeout_seconds: float = Field(default=25, ge=0)

    # Comma-separated in the environment, e.g. EMITTED_EVENT_CATEGORIES=WORKFLOW,CUSTOM_TASK,ACTIVITY. The list is
    # exactly what the worker sends, so it must name CUSTOM_TASK. An empty value is rejected rather than read as
    # "no category", which would silently turn WORKFLOW events off.
    emitted_event_categories: Annotated[list[WorkflowEventCategory], NoDecode, CommaSeparated] = Field(
        default_factory=lambda: [WorkflowEventCategory.WORKFLOW, WorkflowEventCategory.CUSTOM_TASK],
        description=(
            "Event categories the worker sends to the Workflows API. CUSTOM_TASK is always sent: consumers such as "
            "Vibe rely on it. ACTIVITY is off by default: its events make every activity wait on publish calls, "
            "and no internal consumer reads them."
        ),
    )

    health_server_host: str = "localhost"
    health_server_port: int | None = None

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
        env_nested_delimiter="__",
    )

    @classmethod
    def _wrap_init_source(cls, source: PydanticBaseSettingsSource) -> PydanticBaseSettingsSource:
        source = super()._wrap_init_source(source)
        return source if _resolving_nested_worker_config.get() else _ExplicitHeadersSource(source)

    @classmethod
    def _extra_sources(cls, settings_cls: type[BaseSettings]) -> tuple[PydanticBaseSettingsSource, ...]:
        return (*super()._extra_sources(settings_cls), _DroppedHeadersWarningSource(settings_cls))

    @model_validator(mode="after")
    def default_agent_server_url(self) -> "WorkerConfig":
        if not self.agent.mistral_client_server_url:
            self.agent.mistral_client_server_url = self.server_url
        return self

    @property
    def payload_encryption_level(self) -> PayloadEncryptionLevel:
        if self.temporal_payload_encryption is None:
            return PayloadEncryptionLevel.NONE
        return PayloadEncryptionLevel(self.temporal_payload_encryption.mode.value)

    @property
    def encrypts_payloads_fully(self) -> bool:
        return (
            self.temporal_payload_encryption is not None
            and self.temporal_payload_encryption.mode == PayloadEncryptionMode.FULL
        )

    @model_validator(mode="after")
    def always_emit_custom_task_events(self) -> "WorkerConfig":
        # Rejected rather than added, so the setting reads as exactly what the worker sends.
        if WorkflowEventCategory.CUSTOM_TASK not in self.emitted_event_categories:
            raise ValueError(
                "emitted_event_categories must include CUSTOM_TASK: consumers such as Vibe rely on its events"
            )
        return self

    @model_validator(mode="after")
    def warn_determinism_disabled(self) -> "WorkerConfig":
        if not self.default_enforce_determinism:
            logger.warning(
                "Worker configured with default determinism enforcement disabled. "
                "This may lead to non-deterministic behavior and replay failures.",
            )
        return self


class HttpRoute(TypedDict, total=False):
    """Per-pattern override of `HttpConfig`."""

    proxy: str | None
    verify: bool | None


class HttpConfig(_SdkSettings):
    """Settings for the httpx clients the SDK builds."""

    proxy: str | None = Field(
        default=None,
        description="Proxy every SDK HTTP client routes through, e.g. 'http://corp-proxy:3128'",
    )
    verify: bool = Field(
        default=True,
        description="Whether to check TLS certificates; ☢️ False checks nothing. The bundle is `common.ca_bundle`",
    )
    routes: dict[str, HttpRoute | None] = Field(
        default_factory=dict,
        description="Overrides of the above per httpx URL pattern, e.g. 'all://*.eu.corp'. None connects directly",
    )
    timeout: float = Field(
        default=60.0,
        gt=0,
        description="Default timeout in seconds for the SDK HTTP clients",
    )
    retries: int = Field(
        default=0,
        ge=0,
        description="Retries when the connection could not be established; httpx ignores it through a proxy",
    )
    max_connections: int | None = Field(
        default=100,
        description="Cap on concurrent connections per client; None is unlimited",
    )
    max_keepalive_connections: int | None = Field(
        default=20,
        description="Cap on idle keep-alive connections per client; None is unlimited",
    )
    transport_factory: Callable[[type], Any] | None = Field(
        default=None,
        exclude=True,
        repr=False,
        description=(
            "Builds the transport for a given client class, replacing the one derived above. The factory owns "
            "TLS: common.ca_bundle and the mTLS client identity are not applied to the transport it returns"
        ),
    )

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="MISTRAL_WORKFLOWS_HTTP_",
        env_parse_none_str="null",
    )

    def route_verify(self, route: "HttpRoute | None" = None) -> bool:
        route_value = route.get("verify") if route is not None else None
        if route_value is not None:
            return route_value
        return self.verify

    def route_proxy(self, route: "HttpRoute | None" = None) -> str | None:
        if route is None:
            return None
        return route.get("proxy", self.proxy)

    @model_validator(mode="after")
    def warn_tls_verification_disabled(self) -> Self:
        unverified = [p for p, route in self.routes.items() if self.route_verify(route) is False]
        if self.verify is False:
            unverified.append("all://")
        if unverified:
            logger.warning(
                "TLS certificate verification is disabled, traffic to these destinations can be "
                "read and altered in transit",
                patterns=sorted(set(unverified)),
            )
        return self


class AppConfig(_SdkSettings):
    common: CommonConfig = Field(default_factory=CommonConfig)
    worker: WorkerConfig = Field(default_factory=WorkerConfig)
    temporal: TemporalConfig = Field(default_factory=TemporalConfig)
    http: HttpConfig = Field(default_factory=HttpConfig)

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )

    @classmethod
    def _wrap_init_source(cls, source: PydanticBaseSettingsSource) -> PydanticBaseSettingsSource:
        return _ExplicitHeadersSource(super()._wrap_init_source(source), key="worker")

    @classmethod
    def _extra_sources(cls, settings_cls: type[BaseSettings]) -> tuple[PydanticBaseSettingsSource, ...]:
        return (*super()._extra_sources(settings_cls), _DroppedHeadersWarningSource(settings_cls, key="worker"))

    @field_validator("worker", mode="wrap")
    @classmethod
    def _resolve_nested_worker(cls, value: Any, handler: ValidatorFunctionWrapHandler) -> Any:
        token = _resolving_nested_worker_config.set(True)
        try:
            return handler(value)
        finally:
            _resolving_nested_worker_config.reset(token)

    @property
    def otel_headers(self) -> str | None:
        """Generate OTEL headers with Mistral API key as bearer token if available."""
        if self.common.mistral_api_key and self.common.mistral_api_key.get_secret_value():
            return f"Authorization=Bearer {self.common.mistral_api_key.get_secret_value()}"
        return None

    def validate_for_worker_startup(self) -> None:
        if not self.worker.deployment_name:
            raise ValueError(
                "DEPLOYMENT_NAME is required. "
                "Set it to a stable identifier for this deployment (e.g. 'invoice-parser')."
            )
        if self.worker.deployment_name == "default":
            logger.warning(
                "DEPLOYMENT_NAME is set to 'default'; this is valid but may conflict with other "
                "deployments using the same name"
            )

    def get_effective_task_queue(self) -> str:
        return self.worker.deployment_name or "default"

    @model_validator(mode="after")
    def inject_defaults(self) -> Self:
        has_mistral_key = self.common.mistral_api_key and self.common.mistral_api_key.get_secret_value()
        if not self.worker.agent.mistral_client_api_key and has_mistral_key:
            self.worker.agent.mistral_client_api_key = self.common.mistral_api_key
        return self


def _redact_proxy_url(url: str) -> str:
    """Strip any user:password from a proxy URL so credentials never reach the logs."""
    parts = urlsplit(url)
    if not (parts.username or parts.password):
        return url
    host = parts.hostname or ""
    netloc = f"***@{host}:{parts.port}" if parts.port else f"***@{host}"
    return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


def _loggable_config(config: AppConfig) -> dict[str, Any]:
    """A config dump safe to log: proxy credentials are stripped. ``SecretStr`` fields are already
    masked by ``model_dump``."""
    data = config.model_dump()
    worker = data.get("worker") or {}
    if worker.get("mistral_api_headers"):
        worker["mistral_api_headers"] = {name: "***" for name in worker["mistral_api_headers"]}
    http = data.get("http") or {}
    if http.get("proxy"):
        http["proxy"] = _redact_proxy_url(http["proxy"])
    for route in (http.get("routes") or {}).values():
        if isinstance(route, dict) and route.get("proxy"):
            route["proxy"] = _redact_proxy_url(route["proxy"])
    return data


def get_config_from_env() -> AppConfig:
    """Resolve a fresh workflow configuration from environment variables and dotenv."""
    return AppConfig()


_active_config: ContextVar[AppConfig | None] = ContextVar("mistral_workflows_config", default=None)
# Temporal workflow activations and Replayer executions run in executor contexts that do not inherit
# the worker's ContextVar. This module is passed through the sandbox, so workflow code can safely select
# the snapshot registered before polling starts without touching Temporal's internal workflow definition.


@dataclass
class _WorkflowConfigRegistration:
    task_queue: str
    deployment_version: tuple[str, str] | None
    config: AppConfig
    reference_count: int = 1
    replay_namespaces: dict[str, int] = dataclass_field(default_factory=dict)


_WorkflowConfigKey = tuple[str, str, tuple[str, str] | None]
_WorkflowConfigReadCacheKey = tuple[str | None, str | None, _WorkflowConfigKey]


@dataclass(frozen=True)
class _WorkflowConfigRegistrySnapshot:
    registrations: Mapping[_WorkflowConfigKey, _WorkflowConfigRegistration]
    queue_fallbacks: Mapping[tuple[str, str], _WorkflowConfigRegistration | None]
    workflow_fallbacks: Mapping[str, _WorkflowConfigRegistration | None]
    replay_fallbacks: Mapping[tuple[str, str], _WorkflowConfigRegistration | None]
    managed_workflow_types: frozenset[str]


_workflow_configs: dict[_WorkflowConfigKey, _WorkflowConfigRegistration] = {}
_workflow_config_queue_fallbacks: dict[tuple[str, str], _WorkflowConfigRegistration | None] = {}
_workflow_config_fallbacks: dict[str, _WorkflowConfigRegistration | None] = {}
_workflow_config_replay_fallbacks: dict[tuple[str, str], _WorkflowConfigRegistration | None] = {}
_workflow_config_registry_snapshot = _WorkflowConfigRegistrySnapshot(
    registrations=MappingProxyType({}),
    queue_fallbacks=MappingProxyType({}),
    workflow_fallbacks=MappingProxyType({}),
    replay_fallbacks=MappingProxyType({}),
    managed_workflow_types=frozenset(),
)
# Keep configured names after their registration closes so an SDK workflow cannot silently
# fall back to environment config, while raw Temporal workflows retain their legacy fallback.
_managed_workflow_types: set[str] = set()
_workflow_configs_lock = Lock()
_workflow_config_read_cache: ContextVar[tuple[_WorkflowConfigReadCacheKey, AppConfig] | None] = ContextVar(
    "mistral_workflows_config_read_cache",
    default=None,
)


def _publish_workflow_config_registry_snapshot() -> None:
    global _workflow_config_registry_snapshot
    _workflow_config_registry_snapshot = _WorkflowConfigRegistrySnapshot(
        registrations=MappingProxyType(dict(_workflow_configs)),
        queue_fallbacks=MappingProxyType(dict(_workflow_config_queue_fallbacks)),
        workflow_fallbacks=MappingProxyType(dict(_workflow_config_fallbacks)),
        replay_fallbacks=MappingProxyType(dict(_workflow_config_replay_fallbacks)),
        managed_workflow_types=frozenset(_managed_workflow_types),
    )


def _single_config_registration(
    registrations: list[_WorkflowConfigRegistration],
) -> _WorkflowConfigRegistration | None:
    """Return a registration when every candidate carries the same config, else None.

    An unversioned worker registers its config twice (without a version and under its synthetic
    version), so counting registrations would wrongly treat one config as ambiguous.
    """
    if not registrations:
        return None
    first = registrations[0]
    first_dump = first.config.model_dump(round_trip=True)
    if all(registration.config.model_dump(round_trip=True) == first_dump for registration in registrations[1:]):
        return first
    return None


def _refresh_workflow_config_fallbacks(workflow_type: str, task_queue: str) -> None:
    matching_registrations = [
        registration
        for (registered_workflow_type, _, _), registration in _workflow_configs.items()
        if registered_workflow_type == workflow_type
    ]
    _workflow_config_fallbacks[workflow_type] = _single_config_registration(matching_registrations)
    matching_queue_registrations = [
        registration
        for (registered_workflow_type, registered_task_queue, _), registration in _workflow_configs.items()
        if registered_workflow_type == workflow_type and registered_task_queue == task_queue
    ]
    _workflow_config_queue_fallbacks[(workflow_type, task_queue)] = _single_config_registration(
        matching_queue_registrations
    )
    for key in [key for key in _workflow_config_replay_fallbacks if key[0] == workflow_type]:
        del _workflow_config_replay_fallbacks[key]
    replay_namespaces = {
        namespace
        for registration in matching_registrations
        for namespace, reference_count in registration.replay_namespaces.items()
        if reference_count > 0
    }
    for namespace in replay_namespaces:
        replay_registrations = [
            registration
            for registration in matching_registrations
            if registration.replay_namespaces.get(namespace, 0) > 0
        ]
        _workflow_config_replay_fallbacks[(workflow_type, namespace)] = (
            replay_registrations[0] if len(replay_registrations) == 1 else None
        )


def _workflow_deployment_version(config: AppConfig) -> tuple[str, str] | None:
    versioning = config.worker.versioning
    if not versioning.enabled or not versioning.deployment_name or not versioning.build_id:
        return None
    return versioning.deployment_name, versioning.build_id


def _register_workflow_config(
    workflow_type: str,
    task_queue: str,
    config: AppConfig,
    *,
    replay_namespace: str | None = None,
    deployment_version_override: tuple[str, str] | None = None,
) -> _WorkflowConfigKey:
    """Register an isolated config snapshot visible to one Temporal workflow definition."""
    config_snapshot = config.model_copy(deep=True)
    deployment_version = deployment_version_override or _workflow_deployment_version(config_snapshot)
    registration_key = (workflow_type, task_queue, deployment_version)
    with _workflow_configs_lock:
        _managed_workflow_types.add(workflow_type)
        existing = _workflow_configs.get(registration_key)
        if existing is not None:
            if existing.config.model_dump(round_trip=True) != config_snapshot.model_dump(round_trip=True):
                raise WorkflowsException(
                    code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
                    message=(
                        f"Workflow type {workflow_type!r} is already configured on task queue {task_queue!r} "
                        f"for deployment version {deployment_version!r} with a different workflow configuration. "
                        "A workflow type, task queue, and deployment version can only have one complete "
                        "workflow-visible configuration per process. Use a different task queue or deployment "
                        "version, or run differently configured workers in separate processes."
                    ),
                )
            existing.reference_count += 1
            if replay_namespace is not None:
                existing.replay_namespaces[replay_namespace] = existing.replay_namespaces.get(replay_namespace, 0) + 1
                _refresh_workflow_config_fallbacks(workflow_type, task_queue)
                _publish_workflow_config_registry_snapshot()
            return registration_key
        _workflow_configs[registration_key] = _WorkflowConfigRegistration(
            task_queue,
            deployment_version,
            config_snapshot,
            replay_namespaces={replay_namespace: 1} if replay_namespace is not None else {},
        )
        _refresh_workflow_config_fallbacks(workflow_type, task_queue)
        _publish_workflow_config_registry_snapshot()
        return registration_key


def _unregister_workflow_config(
    registration_key: _WorkflowConfigKey,
    *,
    replay_namespace: str | None = None,
) -> None:
    """Release one matching workflow config registration."""
    with _workflow_configs_lock:
        existing = _workflow_configs.get(registration_key)
        if existing is None:
            return
        if existing.reference_count == 1:
            del _workflow_configs[registration_key]
            _refresh_workflow_config_fallbacks(registration_key[0], registration_key[1])
            _publish_workflow_config_registry_snapshot()
        else:
            existing.reference_count -= 1
            if replay_namespace is not None:
                replay_reference_count = existing.replay_namespaces[replay_namespace]
                if replay_reference_count == 1:
                    del existing.replay_namespaces[replay_namespace]
                else:
                    existing.replay_namespaces[replay_namespace] = replay_reference_count - 1
                _refresh_workflow_config_fallbacks(registration_key[0], registration_key[1])
                _publish_workflow_config_registry_snapshot()


@contextmanager
def _use_workflow_config(
    workflow_type: str,
    task_queue: str,
    config: AppConfig,
    *,
    replay_namespace: str | None = None,
    deployment_version_override: tuple[str, str] | None = None,
) -> Iterator[None]:
    registration_key = _register_workflow_config(
        workflow_type,
        task_queue,
        config,
        replay_namespace=replay_namespace,
        deployment_version_override=deployment_version_override,
    )
    try:
        yield
    finally:
        _unregister_workflow_config(registration_key, replay_namespace=replay_namespace)


def _get_registered_workflow_config() -> AppConfig | None:
    if not temporalio.workflow.in_workflow():
        return None

    try:
        info = temporalio.workflow.info()
    except (RuntimeError, temporalio.exceptions.TemporalError):
        return None
    deployment = info.get_current_deployment_version()
    deployment_version = (
        (deployment.deployment_name, deployment.build_id)
        if deployment is not None and deployment.deployment_name
        else None
    )
    registry = _workflow_config_registry_snapshot
    registered = None
    workflow_namespace = getattr(info, "namespace", None)
    if workflow_namespace is not None:
        # A Replayer runs under its own namespace. Prefer the config prepared for that replay,
        # even when a live worker in this process serves the same workflow and task queue.
        registered = registry.replay_fallbacks.get((info.workflow_type, workflow_namespace))
    if registered is None:
        registered = registry.registrations.get((info.workflow_type, info.task_queue, deployment_version))
    if registered is None:
        # A run can report a deployment version this worker did not register: a v2 worker continuing
        # a v1 run after an upgrade, recovery, or versioning override. When the task queue has exactly
        # one config, that config is the only one this worker can run the workflow with.
        registered = registry.queue_fallbacks.get((info.workflow_type, info.task_queue))
    if registered is None and deployment_version is None:
        registered = registry.workflow_fallbacks.get(info.workflow_type)
    if registered is None:
        if info.workflow_type not in registry.managed_workflow_types:
            return None
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message=(
                f"No workflow configuration is registered for workflow type {info.workflow_type!r} "
                f"on task queue {info.task_queue!r} for deployment version {deployment_version!r}. "
                "Start it with run_worker() or keep prepare_workflows() open while running a Temporal "
                "Worker or Replayer."
            ),
        )
    registration_key = (info.workflow_type, registered.task_queue, registered.deployment_version)
    cache_key = (
        getattr(info, "workflow_id", None),
        getattr(info, "run_id", None),
        registration_key,
    )
    cached = _workflow_config_read_cache.get()
    if cached is not None and cached[0] == cache_key:
        return cached[1]
    workflow_config = registered.config.model_copy(deep=True)
    _workflow_config_read_cache.set((cache_key, workflow_config))
    return workflow_config


@contextmanager
def use_config(config: AppConfig) -> Iterator[None]:
    """Make a resolved config available to legacy runtime dependencies in this async context."""
    token = _active_config.set(config)
    try:
        yield
    finally:
        _active_config.reset(token)


class _LazyConfig:
    """Backward-compatible lazy facade for the deprecated mutable config singleton."""

    def __init__(self) -> None:
        object.__setattr__(self, "_value", None)
        object.__setattr__(self, "_lock", Lock())

    def get(self) -> AppConfig:
        if workflow_config := _get_registered_workflow_config():
            return workflow_config
        if active_config := _active_config.get():
            return active_config

        value = cast(AppConfig | None, object.__getattribute__(self, "_value"))
        if value is not None:
            return value

        lock = cast(Lock, object.__getattribute__(self, "_lock"))
        with lock:
            value = cast(AppConfig | None, object.__getattribute__(self, "_value"))
            if value is None:
                value = get_config_from_env()
                object.__setattr__(self, "_value", value)
        return value

    def get_if_loaded(self) -> AppConfig | None:
        return cast(AppConfig | None, object.__getattribute__(self, "_value"))

    def __getattr__(self, name: str) -> Any:
        return getattr(self.get(), name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self.get(), name, value)


_lazy_config = _LazyConfig()


def _get_or_load_config() -> AppConfig:
    """Return the lazy compatibility facade without resolving its environment."""
    return cast(AppConfig, _lazy_config)


config = _get_or_load_config()


def setup_default_logging(app_config: AppConfig | None = None) -> None:
    """Set up the SDK's console logging for a process the SDK runs, such as a worker or the SDK CLIs.

    The host's own logging setup wins. If the host configured structlog, this does nothing, and
    the host owns every logger level. If the host only set up stdlib logging (the root logger has
    handlers), the SDK logs through those handlers and leaves the root logger, its handlers and
    the logger levels as they are. Otherwise it installs the SDK's console handler and quiets the
    noisy libraries. Importing the SDK never sets up logging; entry points that own the process
    call this instead.
    """
    if structlog.is_configured():
        return
    resolved_config = app_config if app_config is not None else config
    inject_otel_trace = resolved_config.common.otel_enabled and resolved_config.common.otel_inject_logs
    if logging.getLogger().handlers:
        route_logs_to_host_logging(inject_otel_trace=inject_otel_trace)
        return
    setup_logging(
        log_level=resolved_config.common.log_level,
        log_format=resolved_config.common.log_format,
        app_version=resolved_config.common.app_version,
        inject_otel_trace=inject_otel_trace,
        extra_config=[
            # noisy
            LoggerConfig(name="httpx", level=LogLevel.WARNING),
            LoggerConfig(name="httpcore", level=LogLevel.WARNING),
            LoggerConfig(name="asyncio", level=LogLevel.WARNING),
            LoggerConfig(name="aiocache", level=LogLevel.WARNING),
            LoggerConfig(name="urllib3", level=LogLevel.WARNING),
        ],
    )


def log_configuration(app_config: AppConfig | None = None) -> None:
    """Log the loaded configuration, with secrets masked. Called when a worker starts."""
    resolved_config = app_config if app_config is not None else config
    logger.info("Configuration loaded", config=_loggable_config(resolved_config))


class _DeploymentNameEnvironment(BaseSettings):
    deployment_name: str | None = None

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
        env_parse_none_str="null",
    )


def resolve_worker_config(explicit_config: AppConfig | None) -> AppConfig:
    """Resolve configuration for one worker startup.

    Explicit configuration is copied so the caller's object remains isolated. Without an explicit
    configuration, environment and dotenv values are resolved fresh for every worker startup unless
    the deprecated mutable ``config`` facade was already loaded, in which case its compatibility
    value remains authoritative.
    """
    if explicit_config is not None:
        environment_deployment_name = _DeploymentNameEnvironment().deployment_name
        explicit_deployment_name = explicit_config.worker.deployment_name
        if environment_deployment_name is not None and explicit_deployment_name != environment_deployment_name:
            logger.warning(
                "Explicit worker deployment name overrides DEPLOYMENT_NAME from the environment",
                explicit_deployment_name=explicit_deployment_name,
                environment_deployment_name=environment_deployment_name,
            )
        resolved = explicit_config.model_copy(deep=True)
    else:
        resolved = _lazy_config.get_if_loaded() or get_config_from_env()
    return resolved


def get_workflow_decorator_config() -> WorkerConfig | WorkflowDecoratorConfig:
    """Resolve only settings that affect class decoration.

    A worker being prepared or running takes precedence, so Temporal sandbox re-imports reproduce the
    definitions registered by that worker. Otherwise decoration uses SDK defaults, without reading the
    environment or the legacy ``config`` facade, so a definition never depends on import order.
    """
    if workflow_config := _get_registered_workflow_config():
        return workflow_config.worker
    if active_config := _active_config.get():
        return active_config.worker
    return _workflow_decorator_config
