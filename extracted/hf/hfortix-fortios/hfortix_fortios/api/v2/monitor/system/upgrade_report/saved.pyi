""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/upgrade_report/saved
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
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class SavedResponse(TypedDict, total=False):
    """Response type for Saved - use with .dict property for typed dict access."""
    ipv4_sessions: int
    ipv6_sessions: int
    sslvpn_tunnels: int
    ipsec_tunnels: int
    cpu_usage: int
    memory_usage: int
    total_routes: int
    total_ospf_routes: int
    total_bgp_routes: int
    fortigate_stats: str
    fortiap_stats: str
    fortiswitch_stats: str
    fortiextender_stats: str
    endpoint_device_stats: str
    config_revision_id: int
    version: str
    admin: str
    created: int


class SavedObject(FortiObject[SavedResponse]):
    """Typed FortiObject for Saved with field access."""
    ipv4_sessions: int
    ipv6_sessions: int
    sslvpn_tunnels: int
    ipsec_tunnels: int
    cpu_usage: int
    memory_usage: int
    total_routes: int
    total_ospf_routes: int
    total_bgp_routes: int
    fortigate_stats: str
    fortiap_stats: str
    fortiswitch_stats: str
    fortiextender_stats: str
    endpoint_device_stats: str
    config_revision_id: int
    version: str
    admin: str
    created: int



# ================================================================
# Main Endpoint Class
# ================================================================

class Saved:
    """
    
    Endpoint: system/upgrade_report/saved
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
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[SavedObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...


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
        payload_dict: dict[str, Any] | None = ...,
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
    "Saved",
    "SavedResponse",
    "SavedObject",
]