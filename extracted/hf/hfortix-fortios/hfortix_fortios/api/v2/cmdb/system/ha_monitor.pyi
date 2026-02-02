""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ha_monitor
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

class HaMonitorPayload(TypedDict, total=False):
    """Payload type for HaMonitor operations."""
    monitor_vlan: Literal["enable", "disable"]
    vlan_hb_interval: int
    vlan_hb_lost_threshold: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class HaMonitorResponse(TypedDict, total=False):
    """Response type for HaMonitor - use with .dict property for typed dict access."""
    monitor_vlan: Literal["enable", "disable"]
    vlan_hb_interval: int
    vlan_hb_lost_threshold: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class HaMonitorObject(FortiObject):
    """Typed FortiObject for HaMonitor with field access."""
    monitor_vlan: Literal["enable", "disable"]
    vlan_hb_interval: int
    vlan_hb_lost_threshold: int


# ================================================================
# Main Endpoint Class
# ================================================================

class HaMonitor:
    """
    
    Endpoint: system/ha_monitor
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HaMonitorObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: HaMonitorPayload | None = ...,
        monitor_vlan: Literal["enable", "disable"] | None = ...,
        vlan_hb_interval: int | None = ...,
        vlan_hb_lost_threshold: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HaMonitorObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: HaMonitorPayload | None = ...,
        monitor_vlan: Literal["enable", "disable"] | None = ...,
        vlan_hb_interval: int | None = ...,
        vlan_hb_lost_threshold: int | None = ...,
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
    "HaMonitor",
    "HaMonitorPayload",
    "HaMonitorResponse",
    "HaMonitorObject",
]