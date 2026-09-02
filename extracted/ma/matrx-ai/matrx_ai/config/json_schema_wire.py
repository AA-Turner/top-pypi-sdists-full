"""Strict JSON Schema wire shapes for tool params and structured output."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

JsonSchemaType = Literal[
    "string",
    "number",
    "integer",
    "boolean",
    "array",
    "object",
    "null",
]


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

    @model_validator(mode="after")
    def _required_keys_exist(self) -> JsonSchemaObjectDocument:
        if not self.required:
            return self
        unknown = set(self.required) - set(self.properties.keys())
        if unknown:
            raise ValueError(f"required lists keys not present in properties: {sorted(unknown)}")
        return self


JsonSchemaProperty.model_rebuild()
