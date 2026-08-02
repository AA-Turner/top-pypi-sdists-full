"""Ambient observability context helpers."""

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import cast

from pydantic import BaseModel, ConfigDict, JsonValue
from structlog.contextvars import bind_contextvars, clear_contextvars, get_contextvars

ObservabilityAttributes = Mapping[str, JsonValue]


class _HostObservabilityAttributes(BaseModel):
    """Host-supplied attributes allowed to enter SDK ambient context."""

    model_config = ConfigDict(extra="ignore")

    agent_entrypoint: str | None = None
    agent_version: str | None = None
    client_name: str | None = None
    client_version: str | None = None
    call_source: str | None = None
    entrypoint: str | None = None
    correlation_id: str | None = None
    application_id: str | None = None
    workflow_version: str | None = None
    surface: str | None = None
    parent_session_id: str | None = None
    workflow_name: str | None = None
    repo_id: str | None = None
    project_id: str | None = None
    user_id: str | None = None
    workspace_id: str | None = None
    organization_id: str | None = None
    customer_id: str | None = None
    started_from: str | None = None
    nb_models: int | None = None


SESSION_OBSERVABILITY_ATTRIBUTE_KEYS = tuple(_HostObservabilityAttributes.model_fields)

COMMON_CONTEXT_KEYS = (
    *SESSION_OBSERVABILITY_ATTRIBUTE_KEYS,
    "session_id",
    "conversation_id",
    "agent_name",
    "model",
    "provider",
)

SPAN_CONTEXT_KEYS = (
    "session_id",
    "conversation_id",
    "task_id",
    "agent_name",
    "model",
    "provider",
    "run_mode",
    "status",
    "history_length",
)


def validate_observability_attributes(
    attributes: ObservabilityAttributes | None,
) -> dict[str, JsonValue]:
    return cast(
        dict[str, JsonValue],
        _HostObservabilityAttributes.model_validate(attributes or {}).model_dump(exclude_none=True),
    )


@contextmanager
def observability_context(**attributes: JsonValue) -> Iterator[None]:
    """Bind observability attributes for this scope, then restore the prior context."""
    snapshot = get_contextvars()
    bind_contextvars(**attributes)
    try:
        yield
    finally:
        clear_contextvars()
        bind_contextvars(**snapshot)


def upsert_in_context(**attributes: JsonValue) -> None:
    bind_contextvars(**attributes)


def attributes_from_context(*keys: str) -> dict[str, JsonValue]:
    context = get_contextvars()
    return {
        key: cast(JsonValue, context[key])
        for key in keys
        if key in context and context[key] is not None
    }
