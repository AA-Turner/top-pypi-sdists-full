""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/sdn_connector_filters
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

class SdnConnectorFiltersPayload(TypedDict, total=False):
    """Payload type for SdnConnectorFilters operations."""
    connector: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SdnConnectorFiltersResponse(TypedDict, total=False):
    """Response type for SdnConnectorFilters - use with .dict property for typed dict access."""
    connector: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SdnConnectorFiltersObject(FortiObject):
    """Typed FortiObject for SdnConnectorFilters with field access."""
    connector: str


# ================================================================
# Main Endpoint Class
# ================================================================

class SdnConnectorFilters:
    """
    
    Endpoint: firewall/sdn_connector_filters
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
        connector: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SdnConnectorFiltersObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SdnConnectorFiltersPayload | None = ...,
        connector: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SdnConnectorFiltersObject: ...




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
        payload_dict: SdnConnectorFiltersPayload | None = ...,
        connector: str | None = ...,
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
    "SdnConnectorFilters",
    "SdnConnectorFiltersPayload",
    "SdnConnectorFiltersResponse",
    "SdnConnectorFiltersObject",
]