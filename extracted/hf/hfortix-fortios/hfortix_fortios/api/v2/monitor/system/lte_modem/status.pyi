""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/lte_modem/status
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

class StatusResponse(TypedDict, total=False):
    """Response type for Status - use with .dict property for typed dict access."""
    status: str
    manufacturer: str
    model: str
    revision: str
    msisdn: str
    esn: str
    imei: str
    meid: str
    cell_id: str
    hw_revision: str
    sw_revision: str
    sku: str
    fsn: str
    operating_mode: str
    billing_date: int
    gps_status: bool
    gps: str
    sim_auto_switch: bool
    sim_auto_switch_time: int
    roaming: bool
    signal: str
    data_limit: int
    data_usage_tracking: bool
    active_plan: str
    idle_plan: str
    active_sim: str
    connection_status_ipv4: str
    connection_status_ipv6: str
    interface: str
    ipv4: str
    ipv6: str
    profile: str


class StatusObject(FortiObject[StatusResponse]):
    """Typed FortiObject for Status with field access."""
    status: str
    manufacturer: str
    model: str
    revision: str
    msisdn: str
    esn: str
    imei: str
    meid: str
    cell_id: str
    hw_revision: str
    sw_revision: str
    sku: str
    fsn: str
    operating_mode: str
    billing_date: int
    gps_status: bool
    gps: str
    sim_auto_switch: bool
    sim_auto_switch_time: int
    roaming: bool
    signal: str
    data_limit: int
    data_usage_tracking: bool
    active_plan: str
    idle_plan: str
    active_sim: str
    connection_status_ipv4: str
    connection_status_ipv6: str
    interface: str
    ipv4: str
    ipv6: str
    profile: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Status:
    """
    
    Endpoint: system/lte_modem/status
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
    ) -> FortiObjectList[StatusObject]: ...
    


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
    "Status",
    "StatusResponse",
    "StatusObject",
]