""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/managed_switch/status
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

class StatusPayload(TypedDict, total=False):
    """Payload type for Status operations."""
    mkey: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class StatusResponse(TypedDict, total=False):
    """Response type for Status - use with .dict property for typed dict access."""
    serial: str
    switch_id: str
    fgt_peer_intf_name: str
    state: str
    status: str
    os_version: str
    connecting_from: str
    join_time: str
    ports: list[str]
    max_poe_budget: int
    igmp_snooping_supported: bool
    dhcp_snooping_supported: bool
    mc_lag_supported: bool
    led_blink_supported: bool
    vlan_segment_supported: bool
    vlan_segment_lite_supported: bool
    is_l3: bool
    faceplate_xml: str
    vdom: str
    image_download_progress: int
    type: str
    owner_vdom: str
    eos: bool
    eos_date: str
    forticare_registration_status: str
    ptp_capable: bool


class StatusObject(FortiObject[StatusResponse]):
    """Typed FortiObject for Status with field access."""
    serial: str
    switch_id: str
    fgt_peer_intf_name: str
    state: str
    status: str
    os_version: str
    connecting_from: str
    join_time: str
    ports: list[str]
    max_poe_budget: int
    igmp_snooping_supported: bool
    dhcp_snooping_supported: bool
    mc_lag_supported: bool
    led_blink_supported: bool
    vlan_segment_supported: bool
    vlan_segment_lite_supported: bool
    is_l3: bool
    faceplate_xml: str
    vdom: str
    image_download_progress: int
    type: str
    owner_vdom: str
    eos: bool
    eos_date: str
    forticare_registration_status: str
    ptp_capable: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class Status:
    """
    
    Endpoint: switch_controller/managed_switch/status
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
        mkey: str | None = ...,
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
        payload_dict: StatusPayload | None = ...,
        mkey: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StatusObject: ...




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
        payload_dict: StatusPayload | None = ...,
        mkey: str | None = ...,
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