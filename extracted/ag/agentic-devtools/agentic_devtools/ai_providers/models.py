import re
from collections.abc import Mapping
from dataclasses import InitVar, dataclass, field
from datetime import datetime
from typing import Any, Literal, Optional, cast

from .serialization import JsonMapping, freeze_json, freeze_json_verbatim

_TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_VALIDATION_STATES = frozenset({"pending", "passed", "failed", "skipped"})
_FAILURE_CATEGORIES = frozenset(
    {
        "validation_error",
        "transport_error",
        "logic_error",
        "provider_error",
    }
)
_TASK_STATES = frozenset(
    {
        "queued",
        "in_progress",
        "completed",
        "failed",
        "idle",
        "waiting_for_user",
        "timed_out",
        "cancelled",
    }
)


def _freeze_mapping(value: Mapping[str, Any]) -> JsonMapping:
    frozen = freeze_json(value)
    if not isinstance(frozen, Mapping):  # pragma: no cover - freeze_json preserves mappings
        raise TypeError("Expected a mapping")
    return cast(JsonMapping, frozen)


def _freeze_mapping_verbatim(value: Mapping[str, Any]) -> JsonMapping:
    frozen = freeze_json_verbatim(value)
    if not isinstance(frozen, Mapping):  # pragma: no cover - freeze_json_verbatim preserves mappings
        raise TypeError(f"freeze_json_verbatim returned a non-Mapping for a Mapping input; got {type(frozen).__name__}")
    return cast(JsonMapping, frozen)


def _freeze_optional_mapping(value: Mapping[str, Any] | None) -> JsonMapping | None:
    if value is None:
        return None
    return _freeze_mapping(value)


def _require_iso8601_timestamp(field_name: str, value: str) -> datetime:
    if not isinstance(value, str) or "T" not in value:
        raise ValueError(f"{field_name} must be a valid ISO-8601 timestamp")

    normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid ISO-8601 timestamp") from exc


def _require_timezone_aware_iso8601_timestamp(field_name: str, value: str) -> None:
    parsed = _require_iso8601_timestamp(field_name, value)
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must be a timezone-aware ISO-8601 timestamp")


def _require_non_empty_string(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_string_or_none(field_name: str, value: object) -> None:
    if value is not None and not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string or None")


def _require_task_id_or_none(field_name: str, value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value or not _TASK_ID_PATTERN.fullmatch(value):
        raise ValueError(f"{field_name} must be a non-empty string matching ^[A-Za-z0-9_-]+$")
    return value


def _require_positive_integer(field_name: str, value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")


def _require_positive_optional_integer(field_name: str, value: object) -> None:
    if value is None:
        return
    _require_positive_integer(field_name, value)


def _require_boolean(field_name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean")


@dataclass(frozen=True)
class ModelRecord:
    name: str
    model_id: str
    provider: str
    context_window: int
    max_output_tokens: int | None
    supports_tools: bool
    raw_metadata: JsonMapping
    raw_metadata_verbatim: InitVar[bool] = False
    source: str = "acp-live"
    observed_at: str | None = None

    def __post_init__(self, raw_metadata_verbatim: bool) -> None:
        _require_non_empty_string("name", self.name)
        _require_non_empty_string("model_id", self.model_id)
        _require_non_empty_string("provider", self.provider)
        _require_positive_integer("context_window", self.context_window)
        _require_positive_optional_integer("max_output_tokens", self.max_output_tokens)
        _require_boolean("supports_tools", self.supports_tools)
        _require_boolean("raw_metadata_verbatim", raw_metadata_verbatim)
        _require_non_empty_string("source", self.source)
        if self.observed_at is not None:
            _require_non_empty_string("observed_at", self.observed_at)
            _require_timezone_aware_iso8601_timestamp("observed_at", self.observed_at)
        freeze = _freeze_mapping_verbatim if raw_metadata_verbatim else _freeze_mapping
        object.__setattr__(self, "raw_metadata", freeze(self.raw_metadata))


@dataclass(frozen=True)
class TaskRequest:
    model_id: str
    prompt: str
    context: str | None
    parameters: JsonMapping = field(repr=False)
    metadata: JsonMapping | None

    def __post_init__(self) -> None:
        _require_non_empty_string("model_id", self.model_id)
        if not isinstance(self.prompt, str):
            raise ValueError("prompt must be a string")
        _require_string_or_none("context", self.context)
        object.__setattr__(self, "parameters", _freeze_mapping_verbatim(self.parameters))
        object.__setattr__(self, "metadata", _freeze_optional_mapping(self.metadata))


@dataclass(frozen=True)
class AgentTaskSpec:
    task_id: str | None
    provider_name: str
    request: TaskRequest
    validation_state: Literal["pending", "passed", "failed", "skipped"]
    created_at: str
    metadata: JsonMapping

    def __post_init__(self) -> None:
        _require_task_id_or_none("task_id", self.task_id)
        _require_non_empty_string("provider_name", self.provider_name)
        if not isinstance(self.request, TaskRequest):
            raise ValueError("request must be a TaskRequest")
        if not isinstance(self.validation_state, str) or self.validation_state not in _VALIDATION_STATES:
            allowed = ", ".join(sorted(_VALIDATION_STATES))
            raise ValueError(f"validation_state must be one of: {allowed}")
        _require_iso8601_timestamp("created_at", self.created_at)
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))


@dataclass(frozen=True)
class FailureEnvelope:
    category: Literal["validation_error", "transport_error", "logic_error", "provider_error"]
    message: str
    details: JsonMapping | None
    retryable: bool

    def __post_init__(self) -> None:
        if not isinstance(self.category, str) or self.category not in _FAILURE_CATEGORIES:
            allowed = ", ".join(sorted(_FAILURE_CATEGORIES))
            raise ValueError(f"category must be one of: {allowed}")
        _require_non_empty_string("message", self.message)
        _require_boolean("retryable", self.retryable)
        object.__setattr__(self, "details", _freeze_optional_mapping(self.details))


@dataclass(frozen=True)
class TaskHandle:
    task_id: str | None
    state: Optional["TaskState"]
    failure: FailureEnvelope | None
    metadata: JsonMapping

    def __post_init__(self) -> None:
        _require_task_id_or_none("task_id", self.task_id)
        if self.state is not None and not isinstance(self.state, TaskState):
            raise ValueError("state must be a TaskState when provided")
        if self.failure is not None and not isinstance(self.failure, FailureEnvelope):
            raise ValueError("failure must be a FailureEnvelope when provided")
        if self.task_id is None and self.failure is None:
            raise ValueError("task_id is None requires failure is not None")
        if self.state is not None and self.failure is not None:
            raise ValueError("state and failure cannot both be non-None")
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))


@dataclass(frozen=True)
class TaskState:
    state: (
        Literal[
            "queued",
            "in_progress",
            "completed",
            "failed",
            "idle",
            "waiting_for_user",
            "timed_out",
            "cancelled",
        ]
        | None
    )
    failure: FailureEnvelope | None
    created_at: str
    metadata: JsonMapping

    def __post_init__(self) -> None:
        if self.state is not None and (not isinstance(self.state, str) or self.state not in _TASK_STATES):
            allowed = ", ".join(sorted(_TASK_STATES))
            raise ValueError(f"state must be one of: {allowed}")
        if self.failure is not None and not isinstance(self.failure, FailureEnvelope):
            raise ValueError("failure must be a FailureEnvelope when provided")

        if self.state is None:
            if self.failure is None:
                raise ValueError("state is None requires failure is not None")
        elif self.state == "failed":
            if self.failure is None:
                raise ValueError("If state == 'failed', then failure must not be None")
        else:
            if self.failure is not None:
                raise ValueError(f"If state is {self.state}, then failure must be None")
        _require_iso8601_timestamp("created_at", self.created_at)
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
