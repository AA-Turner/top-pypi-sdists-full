# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_list_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class ItemDeprecatedToolkit(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    logo: str
    "URL to the toolkit logo image"


class ItemDeprecated(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    available_versions: list[str]
    "List of all available versions for this tool"
    display_name: str = Field(alias="displayName")
    "The display name of the tool"
    is_deprecated: bool
    "Indicates if this tool is deprecated and may be removed in the future"
    toolkit: ItemDeprecatedToolkit
    version: str
    "Current version identifier of the tool"


class ItemScopeRequirementsAllOfAnyOf(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    any_of: list[str]
    when: dict[str, list[str]] | None = None
    source: list[str] | None = None


class ItemScopeRequirements(BaseModel):
    "Structured scope requirements for the tool.\n\nNull means the tool is legacy and only exposes flat scopes."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    all_of: list[Union[str, ItemScopeRequirementsAllOfAnyOf]]
    source: list[str] | None = None


class ItemToolkit(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    logo: str
    "URL to the toolkit logo image"
    name: str
    "Human-readable name of the parent toolkit"
    slug: str
    "Unique identifier of the parent toolkit"


class CurrentItemInstantPrice(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    description: str | None = None
    discount: str | None = None


class CurrentItemInstant(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    supported: Literal[True]
    price: CurrentItemInstantPrice | None = None


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    available_versions: list[str]
    "List of all available versions for this tool"
    deprecated: ItemDeprecated
    description: str
    "Detailed explanation of the tool's functionality and purpose"
    human_description: Optional[str] = None
    "Human-friendly description of the tool, if available"
    input_parameters: Dict[str, Optional[object]]
    "Schema definition of required input parameters for the tool"
    is_deprecated: bool
    "Indicates if this tool is deprecated and may be removed in the future"
    name: str
    "Human-readable display name of the tool"
    no_auth: bool
    "Indicates if the tool can be used without authentication"
    output_parameters: Dict[str, Optional[object]]
    "Schema definition of return values from the tool"
    scope_requirements: Optional[ItemScopeRequirements] = None
    "Structured scope requirements for the tool.\n\nNull means the tool is legacy and only exposes flat scopes."
    scopes: list[str]
    "List of scopes associated with the tool"
    slug: str
    "Unique identifier for the tool"
    tags: list[str]
    "List of tags associated with the tool for categorization and filtering"
    toolkit: ItemToolkit
    version: str
    "Current version of the tool"
    instant: CurrentItemInstant | None = None


class ToolListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


ItemScopeRequirementsAllOf: TypeAlias = Union[str, ItemScopeRequirementsAllOfAnyOf]

__all__ = [
    "ToolListResponse",
    "Item",
    "ItemDeprecated",
    "ItemDeprecatedToolkit",
    "ItemScopeRequirements",
    "ItemScopeRequirementsAllOf",
    "ItemScopeRequirementsAllOfAnyOf",
    "ItemToolkit",
    "CurrentItemInstantPrice",
    "CurrentItemInstant",
]
