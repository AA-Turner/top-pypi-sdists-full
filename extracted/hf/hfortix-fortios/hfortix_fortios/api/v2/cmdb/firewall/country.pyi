""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/country
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class CountryRegionItem(TypedDict, total=False):
    """Nested item for region field."""
    id: int


class CountryPayload(TypedDict, total=False):
    """Payload type for Country operations."""
    id: int
    name: str
    region: str | list[str] | list[CountryRegionItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CountryResponse(TypedDict, total=False):
    """Response type for Country - use with .dict property for typed dict access."""
    id: int
    name: str
    region: list[CountryRegionItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CountryRegionItemObject(FortiObject[CountryRegionItem]):
    """Typed object for region table items with attribute access."""
    id: int


class CountryObject(FortiObject):
    """Typed FortiObject for Country with field access."""
    id: int
    name: str
    region: FortiObjectList[CountryRegionItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Country:
    """
    
    Endpoint: firewall/country
    Category: cmdb
    MKey: id
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        id: int,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CountryObject: ...
    
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[CountryObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...




    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: CountryPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        region: str | list[str] | list[CountryRegionItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> list[str] | list[dict[str, Any]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> FortiObject[Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> FortiObject[Any]: ...
    
    @staticmethod
    def schema() -> FortiObject[Any]: ...


__all__ = [
    "Country",
    "CountryPayload",
    "CountryResponse",
    "CountryObject",
]