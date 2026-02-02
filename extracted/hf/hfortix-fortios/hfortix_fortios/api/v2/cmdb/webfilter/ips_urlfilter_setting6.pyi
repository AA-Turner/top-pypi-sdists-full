""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: webfilter/ips_urlfilter_setting6
Category: cmdb
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

class IpsUrlfilterSetting6Payload(TypedDict, total=False):
    """Payload type for IpsUrlfilterSetting6 operations."""
    device: str
    distance: int
    gateway6: str
    geo_filter: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IpsUrlfilterSetting6Response(TypedDict, total=False):
    """Response type for IpsUrlfilterSetting6 - use with .dict property for typed dict access."""
    device: str
    distance: int
    gateway6: str
    geo_filter: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IpsUrlfilterSetting6Object(FortiObject):
    """Typed FortiObject for IpsUrlfilterSetting6 with field access."""
    device: str
    distance: int
    gateway6: str
    geo_filter: str


# ================================================================
# Main Endpoint Class
# ================================================================

class IpsUrlfilterSetting6:
    """
    
    Endpoint: webfilter/ips_urlfilter_setting6
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IpsUrlfilterSetting6Object: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IpsUrlfilterSetting6Payload | None = ...,
        device: str | None = ...,
        distance: int | None = ...,
        gateway6: str | None = ...,
        geo_filter: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IpsUrlfilterSetting6Object: ...


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
        payload_dict: IpsUrlfilterSetting6Payload | None = ...,
        device: str | None = ...,
        distance: int | None = ...,
        gateway6: str | None = ...,
        geo_filter: str | None = ...,
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
    "IpsUrlfilterSetting6",
    "IpsUrlfilterSetting6Payload",
    "IpsUrlfilterSetting6Response",
    "IpsUrlfilterSetting6Object",
]