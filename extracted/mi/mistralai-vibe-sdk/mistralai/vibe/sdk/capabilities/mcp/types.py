"""Shared types for MCP capability adapters."""

from typing import Annotated, Any

from pydantic import AliasChoices, BaseModel, BeforeValidator, ConfigDict, Field

__all__ = [
    "McpToolDescriptor",
]


class McpToolDescriptor(BaseModel):
    """A tool advertised by an MCP server, parsed from a dict or generated SDK model."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: Annotated[str, BeforeValidator(lambda v: v if isinstance(v, str) else "")] = ""
    input_schema: Annotated[
        dict[str, Any] | None,
        BeforeValidator(lambda v: v if isinstance(v, dict) else None),
    ] = Field(
        default=None,
        validation_alias=AliasChoices("input_schema", "inputSchema", "jsonschema"),
    )
