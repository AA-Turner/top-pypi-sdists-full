"""Unified LLM response_format wire shapes for LLMParams.

OpenAI Chat Completions–style discriminated union on ``type``. Translators in
``base_translator.build_openai_chat_response_format`` normalize all accepted
variants at the provider boundary.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from matrx_ai.config.json_schema_wire import JsonSchemaObjectDocument


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
