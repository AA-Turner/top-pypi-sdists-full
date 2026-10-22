"""Strict JSON Schema wire shapes for tool params and structured output."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    SerializerFunctionWrapHandler,
    model_serializer,
    model_validator,
)

JsonSchemaType = Literal[
    "string",
    "number",
    "integer",
    "boolean",
    "array",
    "object",
    "null",
]


def _omit_absent(model: BaseModel, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
    """Serialize a schema node as the author wrote it: a typed field the caller never sent
    (``enum``, ``items``, ``properties``, ``required``…) is ABSENT from the wire, never
    ``null``/``[]``/``{}`` — a provider reads ``enum: null`` or ``properties: {}`` as a
    constraint (2026-10-22, /ai/manual). Extras (``const``, ``anyOf``, …) ride along."""
    dumped = handler(model)
    sent = model.model_fields_set
    out: dict[str, Any] = {}
    for key, value in dumped.items():
        field = type(model).model_fields.get(key)
        sent_key = field is None or key in sent or (field.alias or key) in sent
        if value is None or not sent_key:
            continue
        out[key] = value
    return out


class JsonSchemaProperty(BaseModel):
    """One property in a tool parameter schema or structured-output object."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: JsonSchemaType | list[JsonSchemaType] | None = None
    description: str | None = None
    enum: list[JsonValue] | None = None
    default: JsonValue | None = None
    items: JsonSchemaProperty | None = None
    properties: dict[str, JsonSchemaProperty] | None = None
    required: list[str] | None = None
    additional_properties: bool | JsonValue | None = Field(
        default=None,
        alias="additionalProperties",
    )

    @model_serializer(mode="wrap")
    def _serialize_as_sent(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        return _omit_absent(self, handler)


class JsonSchemaObjectDocument(BaseModel):
    """Object-root JSON Schema — agent ``output_schema.schema`` and tool roots."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: Literal["object"] | None = "object"
    properties: dict[str, JsonSchemaProperty] = Field(default_factory=dict)
    required: list[str] | None = None
    additional_properties: bool | JsonValue | None = Field(
        default=None,
        alias="additionalProperties",
    )

    @model_serializer(mode="wrap")
    def _serialize_as_sent(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        return _omit_absent(self, handler)

    @model_validator(mode="after")
    def _required_keys_exist(self) -> JsonSchemaObjectDocument:
        if not self.required:
            return self
        unknown = set(self.required) - set(self.properties.keys())
        if unknown:
            raise ValueError(f"required lists keys not present in properties: {sorted(unknown)}")
        return self


JsonSchemaProperty.model_rebuild()
