"""Quota request metadata built from ambient SDK context."""

from functools import cache
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Literal

import structlog
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, ValidationError

from mistralai.vibe.sdk.observability.context import attributes_from_context

TelemetryCallType = Literal["main_call", "secondary_call"]
DEFAULT_CALL_SOURCE = "vibe_code"
logger = structlog.get_logger()


@cache
def _sdk_agent_version() -> str | None:
    try:
        return version("mistralai-vibe-sdk")
    except PackageNotFoundError:
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
    parent_session_id: str | None = None
    user_id: str | None = None
    workspace_id: str | None = None
    customer_id: str | None = None
    call_type: TelemetryCallType
    call_source: str = DEFAULT_CALL_SOURCE
    message_id: str | None = None

    @classmethod
    def build_from_context(cls) -> dict[str, Any]:
        context = attributes_from_context("entrypoint", *cls.model_fields)
        values = {key: value for key, value in context.items() if isinstance(value, str)}
        if "agent_entrypoint" in values:
            values.pop("entrypoint", None)

        try:
            return cls.model_validate(values).model_dump(exclude_none=True)
        except ValidationError as exc:
            invalid_fields = set(_validation_error_fields(exc))
            logger.warning(
                "request_metadata.invalid",
                fields=sorted(invalid_fields),
                error_types=_validation_error_types(exc),
            )
            metadata = {
                key: values[key]
                for key in cls.model_fields
                if key in values and key not in invalid_fields
            }
            if "entrypoint" in values:
                metadata.setdefault("agent_entrypoint", values["entrypoint"])
            if (
                "agent_version" not in metadata
                and (agent_version := _sdk_agent_version()) is not None
            ):
                metadata["agent_version"] = agent_version
            metadata["call_source"] = values.get("call_source", DEFAULT_CALL_SOURCE)
            return metadata


def _validation_error_fields(exc: ValidationError) -> list[str]:
    return sorted({str(error["loc"][0]) for error in exc.errors() if error["loc"]})


def _validation_error_types(exc: ValidationError) -> list[str]:
    return sorted({str(error["type"]) for error in exc.errors()})
