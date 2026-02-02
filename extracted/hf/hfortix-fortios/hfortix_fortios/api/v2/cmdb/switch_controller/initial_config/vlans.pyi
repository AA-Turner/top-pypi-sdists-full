""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/initial_config/vlans
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

class VlansPayload(TypedDict, total=False):
    """Payload type for Vlans operations."""
    optional_vlans: Literal["enable", "disable"]
    default_vlan: str
    quarantine: str
    rspan: str
    voice: str
    video: str
    nac: str
    nac_segment: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VlansResponse(TypedDict, total=False):
    """Response type for Vlans - use with .dict property for typed dict access."""
    optional_vlans: Literal["enable", "disable"]
    default_vlan: str
    quarantine: str
    rspan: str
    voice: str
    video: str
    nac: str
    nac_segment: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VlansObject(FortiObject):
    """Typed FortiObject for Vlans with field access."""
    optional_vlans: Literal["enable", "disable"]
    default_vlan: str
    quarantine: str
    rspan: str
    voice: str
    video: str
    nac: str
    nac_segment: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Vlans:
    """
    
    Endpoint: switch_controller/initial_config/vlans
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
    ) -> VlansObject: ...
    
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
        payload_dict: VlansPayload | None = ...,
        optional_vlans: Literal["enable", "disable"] | None = ...,
        default_vlan: str | None = ...,
        quarantine: str | None = ...,
        rspan: str | None = ...,
        voice: str | None = ...,
        video: str | None = ...,
        nac: str | None = ...,
        nac_segment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VlansObject: ...


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
        payload_dict: VlansPayload | None = ...,
        optional_vlans: Literal["enable", "disable"] | None = ...,
        default_vlan: str | None = ...,
        quarantine: str | None = ...,
        rspan: str | None = ...,
        voice: str | None = ...,
        video: str | None = ...,
        nac: str | None = ...,
        nac_segment: str | None = ...,
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
    "Vlans",
    "VlansPayload",
    "VlansResponse",
    "VlansObject",
]