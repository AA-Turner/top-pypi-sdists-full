""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wifi/managed_ap
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

class ManagedApPayload(TypedDict, total=False):
    """Payload type for ManagedAp operations."""
    wtp_id: str
    incl_local: bool
    skip_eos: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class ManagedApResponse(TypedDict, total=False):
    """Response type for ManagedAp - use with .dict property for typed dict access."""
    name: str
    auto_cert_proto: str
    wtp_id: str
    vdom: str
    serial: str
    is_local: bool
    ap_profile: str
    ble_profile: str
    lw_profile: str
    state: str
    mode: str
    connecting_from: str
    connecting_interface: str
    parent_wtp_id: str
    status: str
    region_code: str
    ap_group: str
    mgmt_vlanid: int
    mesh_uplink: str
    mesh_hop_count: int
    mesh_uplink_intf: str
    mesh_uplink_intf_speed: str
    clients: int
    os_version: str
    local_addr: str
    board_mac: str
    join_time: str
    join_time_raw: int
    last_reboot_time: str
    last_reboot_time_raw: int
    reboot_last_day: bool
    connection_state: str
    image_download_progress: int
    last_failure: str
    last_failure_code: int
    last_failure_param: str
    last_failure_time: str
    override_profile: bool
    eos: bool
    eos_date: str
    ssid: list[str]
    data_chan_sec: str
    dedicated_scan_enabled: bool
    indoor_outdoor: int
    subtype: int
    sensors_temperatures: list[str]
    radio: list[str]
    wanlan_mode: str
    health: str
    wired: list[str]
    wired_state_extension: list[str]
    wan_status: list[str]
    ac_poe_mode: str
    poe_mode: str
    poe_mode_oper: str
    country_code_conflict: int
    configured_country_name: str
    configured_country_code: int
    cli_enabled: bool
    region: str
    location: str
    comment: str
    wtp_mode: str
    lldp_enable: bool
    lldp: list[str]
    led_blink: bool
    led_blink_unlimited: bool
    led_blink_duration: int
    cpu_usage: int
    mem_free: int
    mem_total: int
    is_wpa3_supported: bool
    wan_port_auth: str
    wan_802_1x_method: str
    wan_802_1x_macsec: bool
    forticare_registration_status: str


class ManagedApObject(FortiObject[ManagedApResponse]):
    """Typed FortiObject for ManagedAp with field access."""
    name: str
    auto_cert_proto: str
    wtp_id: str
    vdom: str
    serial: str
    is_local: bool
    ap_profile: str
    ble_profile: str
    lw_profile: str
    state: str
    mode: str
    connecting_from: str
    connecting_interface: str
    parent_wtp_id: str
    status: str
    region_code: str
    ap_group: str
    mgmt_vlanid: int
    mesh_uplink: str
    mesh_hop_count: int
    mesh_uplink_intf: str
    mesh_uplink_intf_speed: str
    clients: int
    os_version: str
    local_addr: str
    board_mac: str
    join_time: str
    join_time_raw: int
    last_reboot_time: str
    last_reboot_time_raw: int
    reboot_last_day: bool
    connection_state: str
    image_download_progress: int
    last_failure: str
    last_failure_code: int
    last_failure_param: str
    last_failure_time: str
    override_profile: bool
    eos: bool
    eos_date: str
    ssid: list[str]
    data_chan_sec: str
    dedicated_scan_enabled: bool
    indoor_outdoor: int
    subtype: int
    sensors_temperatures: list[str]
    radio: list[str]
    wanlan_mode: str
    health: str
    wired: list[str]
    wired_state_extension: list[str]
    wan_status: list[str]
    ac_poe_mode: str
    poe_mode: str
    poe_mode_oper: str
    country_code_conflict: int
    configured_country_name: str
    configured_country_code: int
    cli_enabled: bool
    region: str
    location: str
    comment: str
    wtp_mode: str
    lldp_enable: bool
    lldp: list[str]
    led_blink: bool
    led_blink_unlimited: bool
    led_blink_duration: int
    cpu_usage: int
    mem_free: int
    mem_total: int
    is_wpa3_supported: bool
    wan_port_auth: str
    wan_802_1x_method: str
    wan_802_1x_macsec: bool
    forticare_registration_status: str



# ================================================================
# Main Endpoint Class
# ================================================================

class ManagedAp:
    """
    
    Endpoint: wifi/managed_ap
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
        wtp_id: str | None = ...,
        incl_local: bool | None = ...,
        skip_eos: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[ManagedApObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ManagedApPayload | None = ...,
        wtp_id: str | None = ...,
        incl_local: bool | None = ...,
        skip_eos: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ManagedApObject: ...


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
        payload_dict: ManagedApPayload | None = ...,
        wtp_id: str | None = ...,
        incl_local: bool | None = ...,
        skip_eos: bool | None = ...,
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
    "ManagedAp",
    "ManagedApResponse",
    "ManagedApObject",
]