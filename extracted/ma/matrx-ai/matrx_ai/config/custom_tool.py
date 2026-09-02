"""Wire schema for inline / delegated custom tools (MCP-shaped).

Kept in ``config/`` (not ``tools/``) so ``LLMParams`` can reference
``CustomTool`` without importing the tools package. ``tools.models.CustomTool``
subclasses this type and adds provider formatting helpers.
"""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from matrx_ai.config.json_schema_wire import JsonSchemaProperty

# Internal-plane name rule: provider charset PLUS the namespace colon
# (``bundle:list_supabase``). Provider payloads never see a colon — the
# wire-name seam converts ':' → '__' at serialization and the executor
# reverses it at dispatch (see matrx_ai.config.wire_names).
_TOOL_NAME_RE = re.compile(r"^[a-zA-Z0-9_:-]{1,64}$")


class CustomToolInputSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["object"] = "object"
    properties: dict[str, JsonSchemaProperty] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _required_keys_exist(self) -> CustomToolInputSchema:
        unknown = set(self.required) - set(self.properties.keys())
        if unknown:
            raise ValueError(f"required lists keys not present in properties: {sorted(unknown)}")
        return self


class CustomTool(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        description="Unique tool name. Must match [a-zA-Z0-9_:-]{1,64}; a ':' "
        "namespace separator is serialized to '__' at the provider boundary."
    )
    description: str = Field(
        default="",
        description="Human-readable description shown to the model.",
    )
    input_schema: CustomToolInputSchema = Field(
        default_factory=CustomToolInputSchema,
        description="JSON Schema describing the tool's input parameters.",
    )

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        if not _TOOL_NAME_RE.match(value):
            raise ValueError(f"tool name {value!r} must match [a-zA-Z0-9_:-]{{1,64}}")
        # Each ':' gains one character at wire time (':' → '__'); a name whose
        # WIRE form exceeds the 64-char provider limit can never be declared —
        # the boundary would silently drop it while the request returns 200.
        # Fail fast here instead, where the caller sees the error.
        from matrx_ai.config.wire_names import to_wire_name

        if len(to_wire_name(value)) > 64:
            raise ValueError(
                f"tool name {value!r} exceeds the 64-char provider limit once "
                f"serialized to its wire form ({to_wire_name(value)!r}, "
                f"{len(to_wire_name(value))} chars) — shorten the name."
            )
        return value

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CustomTool:
        return cls.model_validate(data)
