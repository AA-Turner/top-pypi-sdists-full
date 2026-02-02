""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/global_search
Category: monitor
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class GlobalSearchPayload(TypedDict, total=False):
    """Payload type for GlobalSearch operations."""
    search: str
    scope: Literal["vdom", "global"]
    search_tables: Literal["firewall.address", "firewall.address6"]
    skip_tables: Literal["firewall.address", "firewall.address6"]
    exact: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class GlobalSearchResponse(TypedDict, total=False):
    """Response type for GlobalSearch - use with .dict property for typed dict access."""
    mkey: int
    pathname: str
    weight: int
    matched_properties: list[str]


class GlobalSearchObject(FortiObject[GlobalSearchResponse]):
    """Typed FortiObject for GlobalSearch with field access."""
    mkey: int
    pathname: str
    weight: int
    matched_properties: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class GlobalSearch:
    """
    
    Endpoint: system/global_search
    Category: monitor
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        search: str,
        scope: Literal["vdom", "global"] | None = ...,
        search_tables: list[str] | None = ...,
        skip_tables: list[str] | None = ...,
        exact: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[GlobalSearchObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GlobalSearchPayload | None = ...,
        search: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        search_tables: Literal["firewall.address", "firewall.address6"] | None = ...,
        skip_tables: Literal["firewall.address", "firewall.address6"] | None = ...,
        exact: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GlobalSearchObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: GlobalSearchPayload | None = ...,
        search: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        search_tables: Literal["firewall.address", "firewall.address6"] | None = ...,
        skip_tables: Literal["firewall.address", "firewall.address6"] | None = ...,
        exact: bool | None = ...,
        vdom: str | bool | None = ...,
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
    "GlobalSearch",
    "GlobalSearchResponse",
    "GlobalSearchObject",
]