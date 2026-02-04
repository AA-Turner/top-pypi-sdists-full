""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/device/stats
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

class StatsPayload(TypedDict, total=False):
    """Payload type for Stats operations."""
    stat_query_type: Literal["device", "fortiswitch_client", "forticlient"]
    stat_key: Literal["os_name", "hardware_type", "detected_interface", "is_online", "max_vuln_level", "fortiswitch_id", "fortiswitch_port_name"]
    timestamp_from: int
    timestamp_to: int
    filters: Literal["exact", "contains"]
    filter_logic: Literal["and", "or"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class StatsResponse(TypedDict, total=False):
    """Response type for Stats - use with .dict property for typed dict access."""
    chart_value: str
    chart_count: str


class StatsObject(FortiObject[StatsResponse]):
    """Typed FortiObject for Stats with field access."""
    chart_value: str
    chart_count: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Stats:
    """
    
    Endpoint: user/device/stats
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
        stat_query_type: Literal["device", "fortiswitch_client", "forticlient"] | None = ...,
        stat_key: Literal["os_name", "hardware_type", "detected_interface", "is_online", "max_vuln_level", "fortiswitch_id", "fortiswitch_port_name"],
        timestamp_from: int | None = ...,
        timestamp_to: int,
        filters: list[str] | None = ...,
        filter_logic: Literal["and", "or"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[StatsObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StatsPayload | None = ...,
        stat_query_type: Literal["device", "fortiswitch_client", "forticlient"] | None = ...,
        stat_key: Literal["os_name", "hardware_type", "detected_interface", "is_online", "max_vuln_level", "fortiswitch_id", "fortiswitch_port_name"] | None = ...,
        timestamp_from: int | None = ...,
        timestamp_to: int | None = ...,
        filters: Literal["exact", "contains"] | None = ...,
        filter_logic: Literal["and", "or"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StatsObject: ...




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
        payload_dict: StatsPayload | None = ...,
        stat_query_type: Literal["device", "fortiswitch_client", "forticlient"] | None = ...,
        stat_key: Literal["os_name", "hardware_type", "detected_interface", "is_online", "max_vuln_level", "fortiswitch_id", "fortiswitch_port_name"] | None = ...,
        timestamp_from: int | None = ...,
        timestamp_to: int | None = ...,
        filters: Literal["exact", "contains"] | None = ...,
        filter_logic: Literal["and", "or"] | None = ...,
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
    "Stats",
    "StatsResponse",
    "StatsObject",
]