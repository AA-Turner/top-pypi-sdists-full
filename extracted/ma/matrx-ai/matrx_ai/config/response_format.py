"""Unified LLM response_format wire shapes for LLMParams.

OpenAI Chat Completions–style discriminated union on ``type``. Translators in
``base_translator.build_openai_chat_response_format`` normalize all accepted
variants at the provider boundary.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from matrx_ai.config.json_schema_wire import JsonSchemaObjectDocument

STRUCTURED_OUTPUT_SATISFIED_KEY = "structured_output_contract_satisfied"


def is_clean_structured_output_completion(metadata: Any) -> bool:
    """Whether a terminal outcome may consume the one-answer JSON contract."""
    if not isinstance(metadata, dict):
        return False
    # Normal completion omits status today; accept an explicit completed value
    # as well. Every suspended, paused, cancelled, truncated, and failed status
    # is deliberately excluded even when its partial text happens to be valid.
    return metadata.get("status") in {None, "completed"}


class OutputSchemaEnvelope(BaseModel):
    """OpenAI ``json_schema`` inner envelope — matches ``agx_agent.output_schema``."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    name: str | None = None
    schema_: JsonSchemaObjectDocument | None = Field(default=None, alias="schema")
    strict: bool | None = None


class ResponseFormatText(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["text"]


class ResponseFormatJsonObject(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["json_object"]


class ResponseFormatJsonSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    type: Literal["json_schema"]
    json_schema: OutputSchemaEnvelope | None = None
    name: str | None = None
    schema_: JsonSchemaObjectDocument | None = Field(default=None, alias="schema")
    strict: bool | None = None

    @field_validator("json_schema", mode="before")
    @classmethod
    def _coerce_json_schema_body(cls, value: object) -> object:
        if value is None or isinstance(value, OutputSchemaEnvelope):
            return value
        if not isinstance(value, dict):
            return value
        if isinstance(value.get("schema"), dict) or "name" in value or "strict" in value:
            return OutputSchemaEnvelope.model_validate(value)
        if {"type", "properties", "items"} & value.keys():
            return OutputSchemaEnvelope(schema=JsonSchemaObjectDocument.model_validate(value))
        return OutputSchemaEnvelope.model_validate(value)

    @field_validator("schema_", mode="before")
    @classmethod
    def _coerce_flat_schema(cls, value: object) -> object:
        if value is None or isinstance(value, JsonSchemaObjectDocument):
            return value
        if isinstance(value, dict):
            return JsonSchemaObjectDocument.model_validate(value)
        return value


ResponseFormat = Annotated[
    ResponseFormatText | ResponseFormatJsonObject | ResponseFormatJsonSchema,
    Field(discriminator="type"),
]


def _explicit_response_format_override(overrides: Any) -> bool:
    """Whether this turn explicitly chose a response format.

    Conversation defaults are allowed to relax after their first successful
    structured answer. A caller that names ``response_format`` for THIS turn
    owns the contract and must never be second-guessed by the persisted
    conversation policy.
    """
    if overrides is None:
        return False
    if isinstance(overrides, dict):
        return overrides.get("response_format") is not None
    fields_set = getattr(overrides, "model_fields_set", set())
    return (
        "response_format" in fields_set and getattr(overrides, "response_format", None) is not None
    )


def _message_fully_satisfies_response_format(message: Any, response_format: dict[str, Any]) -> bool:
    """Validate a legacy, unmarked generated answer against the full contract."""
    output = message.get_output() if hasattr(message, "get_output") else ""
    if not output:
        return False

    from matrx_ai.agents.output import parse_agent_output, resolve_output_schema

    format_type = response_format.get("type")
    extraction = parse_agent_output(
        output,
        response_format if format_type == "json_schema" else None,
    )
    if not extraction.success or not isinstance(extraction.data, dict):
        return False
    if format_type == "json_object":
        return True

    schema = resolve_output_schema(response_format)
    if schema is None:
        return False
    from matrx_ai.schema.lint import check_sample_against_schema

    return not check_sample_against_schema(extraction.data, schema)


def _has_successful_generated_structured_answer(
    messages: Any,
    response_format: Any,
    *,
    prior_request_status: str | None = None,
) -> bool:
    """True after a provider-generated answer satisfied the active JSON contract.

    Authored/example assistant messages do not count. The orchestrator stamps
    every provider-produced assistant message with ``provider_iteration`` and
    stamps ``structured_output_contract_satisfied`` only after the completed
    request passes full JSON Schema validation. Those persisted facts keep
    authored examples and failed partial provider output from consuming the
    one enforced structured response; a separately gated compatibility check
    covers successful conversations that predate the marker.
    """
    if not isinstance(response_format, dict):
        return False
    format_type = response_format.get("type")
    if format_type not in {"json_schema", "json_object"}:
        return False

    try:
        candidates = list(messages)
    except TypeError:
        return False

    for message in reversed(candidates):
        role = getattr(message, "role", None)
        role_value = role.value if hasattr(role, "value") else role
        metadata = getattr(message, "metadata", None)
        if (
            role_value != "assistant"
            or getattr(message, "status", "active") == "failed"
            or not getattr(message, "is_visible_to_model", True)
            or not isinstance(metadata, dict)
            or not isinstance(metadata.get("provider_iteration"), int)
        ):
            continue
        if metadata.get(STRUCTURED_OUTPUT_SATISFIED_KEY) is True:
            return True
        # Backward compatibility for answers persisted before the success
        # marker existed. The durable conversation outcome proves the latest
        # request completed (so a failed partial cannot qualify), then the full
        # JSON Schema validator proves its generated answer met the contract.
        return prior_request_status == "completed" and _message_fully_satisfies_response_format(
            message, response_format
        )
    return False


def response_format_transition_after_first_structured_answer(
    config: Any,
    *,
    user_input: Any,
    config_overrides: Any = None,
    prior_request_status: str | None = None,
) -> dict[str, Any] | None:
    """Relax a persisted JSON contract for a natural follow-up turn.

    The first provider-generated answer must satisfy the saved structured
    contract. After that, a new user message defaults to ordinary text so the
    model can explain, revise, or naturally repeat JSON as appropriate. Retries
    (no new ``user_input``), authored assistant examples, failed/invalid output,
    and explicit per-turn response-format overrides retain enforcement.

    This function only decides the transition. The send boundary owns the
    actual wire-config mutation and observability so every shaping step remains
    behind one mechanically guarded entry point.
    """
    response_format = getattr(config, "response_format", None)
    if (
        user_input is None
        or _explicit_response_format_override(config_overrides)
        or not _has_successful_generated_structured_answer(
            getattr(config, "messages", None),
            response_format,
            prior_request_status=prior_request_status,
        )
    ):
        return None

    return {
        "code": "response_format_relaxed_after_first_structured_answer",
        "from": response_format["type"],
        "to": "text",
        "reason": "prior_successful_generated_structured_answer",
    }


def mark_structured_output_contract_satisfied(
    config: Any,
    *,
    result_start_position: int | None = None,
) -> bool:
    """Persist proof that this completed provider answer met its JSON contract.

    The lightweight extraction funnel locates the JSON candidate; JSON Schema
    then validates the complete contract (nested types, enums,
    ``additionalProperties``, and all other supported keywords). The marker is
    written only onto a provider-generated assistant message from this result
    window. Failed requests never call this helper.
    """
    response_format = getattr(config, "response_format", None)
    if not isinstance(response_format, dict):
        return False
    format_type = response_format.get("type")
    if format_type not in {"json_schema", "json_object"}:
        return False

    from matrx_ai.agents.output import parse_agent_output, resolve_output_schema

    output = config.get_last_output() if hasattr(config, "get_last_output") else ""
    extraction = parse_agent_output(
        output,
        response_format if format_type == "json_schema" else None,
    )
    if not extraction.success or not isinstance(extraction.data, dict):
        return False

    if format_type == "json_schema":
        schema = resolve_output_schema(response_format)
        if schema is None:
            return False
        from matrx_ai.schema.lint import check_sample_against_schema

        if check_sample_against_schema(extraction.data, schema):
            return False

    try:
        messages = list(config.messages)
    except (AttributeError, TypeError):
        return False
    lower_bound = max(result_start_position or 0, 0)
    for message in reversed(messages[lower_bound:]):
        role = getattr(message, "role", None)
        role_value = role.value if hasattr(role, "value") else role
        metadata = getattr(message, "metadata", None)
        if (
            role_value != "assistant"
            or getattr(message, "status", "active") == "failed"
            or not getattr(message, "is_visible_to_model", True)
            or not isinstance(metadata, dict)
            or not isinstance(metadata.get("provider_iteration"), int)
        ):
            continue
        message.metadata = {**metadata, STRUCTURED_OUTPUT_SATISFIED_KEY: True}
        return True
    return False


def response_format_for_schema(
    schema: dict[str, Any], *, name: str = "structured_output"
) -> ResponseFormatJsonSchema:
    """Build a provider-portable strict response format from a JSON Schema.

    Persisted agents carry their executable output contract as a JSON-schema
    dictionary, while code-authored agents often carry a Pydantic model.  Both
    representations must pass through the same linting boundary before a
    provider call.
    """
    from matrx_ai.schema.lint import lint_output_schema

    report = lint_output_schema(schema)
    portable_schema = report.portable_schema
    if portable_schema is None and report.ok:
        portable_schema = schema
    if portable_schema is None:
        errors = "; ".join(
            f"{finding.provider} {finding.path}: {finding.message}" for finding in report.errors
        )
        raise ValueError(
            f"{name} cannot be enforced as provider-native structured output. "
            f"Fix its JSON Schema before execution. {errors}"
        )

    return ResponseFormatJsonSchema(
        type="json_schema",
        json_schema=OutputSchemaEnvelope.model_validate(
            {"name": name, "schema": portable_schema, "strict": True}
        ),
    )


def response_format_for_model(model: type[BaseModel]) -> ResponseFormatJsonSchema:
    """Build a provider-portable strict response format from a Pydantic model.

    Typed programmatic agents use this instead of trusting a separately saved
    ``response_format`` placeholder. The Pydantic model is the executable
    contract, so the same schema constrains the provider response and validates
    the returned payload. An object-root schema that cannot be made portable
    fails before any model call rather than silently degrading to prompt-only
    JSON generation.
    """
    raw_schema = model.model_json_schema()
    return response_format_for_schema(raw_schema, name=model.__name__)
