"""Quota request metadata built from ambient SDK context."""

from collections.abc import Mapping
from contextlib import suppress
from functools import cache
from importlib.metadata import version
from typing import Any, Literal, get_args

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator

from mistralai.vibe.sdk.observability.context import attributes_from_context

TelemetryCallType = Literal["main_call", "secondary_call"]
CALL_TYPES = get_args(TelemetryCallType)
DEFAULT_CALL_TYPE: TelemetryCallType = "main_call"
DEFAULT_CALL_SOURCE = "vibe_code"


@cache
def _sdk_agent_version() -> str | None:
    with suppress(Exception):
        return version("mistralai-vibe-sdk")
    return None


class RequestMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    agent_entrypoint: str | None = Field(
        default=None,
        validation_alias=AliasChoices("agent_entrypoint", "entrypoint"),
    )
    agent_version: str | None = Field(default_factory=lambda: _sdk_agent_version())
    client_name: str | None = None
    client_version: str | None = None
    session_id: str | None = None
    conversation_id: str | None = None
    correlation_id: str | None = None
    parent_session_id: str | None = None
    user_id: str | None = None
    workspace_id: str | None = None
    customer_id: str | None = None
    call_type: TelemetryCallType | None = None
    call_source: str = DEFAULT_CALL_SOURCE
    surface: str | None = None
    message_id: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_values(cls, values: Any) -> dict[str, Any]:
        if not isinstance(values, Mapping):
            return {}

        metadata = {
            key: value
            for key, value in values.items()
            if key in cls.model_fields and isinstance(value, str)
        }
        if "agent_entrypoint" not in metadata and isinstance(values.get("entrypoint"), str):
            metadata["agent_entrypoint"] = values["entrypoint"]
        if metadata.get("call_type") not in CALL_TYPES:
            metadata["call_type"] = DEFAULT_CALL_TYPE
        metadata.setdefault("call_source", DEFAULT_CALL_SOURCE)
        return metadata

    @classmethod
    def build_from_context(cls) -> dict[str, Any]:
        context: dict[str, Any] = dict(attributes_from_context("entrypoint", *cls.model_fields))
        return cls(**context).model_dump(exclude_none=True)
