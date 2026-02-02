""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/region
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

class RegionCityItem(TypedDict, total=False):
    """Nested item for city field."""
    id: int


class RegionPayload(TypedDict, total=False):
    """Payload type for Region operations."""
    id: int
    name: str
    city: str | list[str] | list[RegionCityItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RegionResponse(TypedDict, total=False):
    """Response type for Region - use with .dict property for typed dict access."""
    id: int
    name: str
    city: list[RegionCityItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RegionCityItemObject(FortiObject[RegionCityItem]):
    """Typed object for city table items with attribute access."""
    id: int


class RegionObject(FortiObject):
    """Typed FortiObject for Region with field access."""
    id: int
    name: str
    city: FortiObjectList[RegionCityItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Region:
    """
    
    Endpoint: firewall/region
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
    ) -> RegionObject: ...
    
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
    ) -> FortiObjectList[RegionObject]: ...
    
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
        payload_dict: RegionPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        city: str | list[str] | list[RegionCityItem] | None = ...,
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
    "Region",
    "RegionPayload",
    "RegionResponse",
    "RegionObject",
]