""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/timers
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

class TimersPayload(TypedDict, total=False):
    """Payload type for Timers operations."""
    echo_interval: int
    nat_session_keep_alive: int
    discovery_interval: int
    client_idle_timeout: int
    client_idle_rehome_timeout: int
    auth_timeout: int
    rogue_ap_log: int
    fake_ap_log: int
    sta_offline_cleanup: int
    sta_offline_ip2mac_cleanup: int
    sta_cap_cleanup: int
    rogue_ap_cleanup: int
    rogue_sta_cleanup: int
    wids_entry_cleanup: int
    ble_device_cleanup: int
    sta_stats_interval: int
    vap_stats_interval: int
    radio_stats_interval: int
    sta_capability_interval: int
    sta_locate_timer: int
    ipsec_intf_cleanup: int
    ble_scan_report_intv: int
    drma_interval: int
    ap_reboot_wait_interval1: int
    ap_reboot_wait_time: str
    ap_reboot_wait_interval2: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class TimersResponse(TypedDict, total=False):
    """Response type for Timers - use with .dict property for typed dict access."""
    echo_interval: int
    nat_session_keep_alive: int
    discovery_interval: int
    client_idle_timeout: int
    client_idle_rehome_timeout: int
    auth_timeout: int
    rogue_ap_log: int
    fake_ap_log: int
    sta_offline_cleanup: int
    sta_offline_ip2mac_cleanup: int
    sta_cap_cleanup: int
    rogue_ap_cleanup: int
    rogue_sta_cleanup: int
    wids_entry_cleanup: int
    ble_device_cleanup: int
    sta_stats_interval: int
    vap_stats_interval: int
    radio_stats_interval: int
    sta_capability_interval: int
    sta_locate_timer: int
    ipsec_intf_cleanup: int
    ble_scan_report_intv: int
    drma_interval: int
    ap_reboot_wait_interval1: int
    ap_reboot_wait_time: str
    ap_reboot_wait_interval2: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class TimersObject(FortiObject):
    """Typed FortiObject for Timers with field access."""
    echo_interval: int
    nat_session_keep_alive: int
    discovery_interval: int
    client_idle_timeout: int
    client_idle_rehome_timeout: int
    auth_timeout: int
    rogue_ap_log: int
    fake_ap_log: int
    sta_offline_cleanup: int
    sta_offline_ip2mac_cleanup: int
    sta_cap_cleanup: int
    rogue_ap_cleanup: int
    rogue_sta_cleanup: int
    wids_entry_cleanup: int
    ble_device_cleanup: int
    sta_stats_interval: int
    vap_stats_interval: int
    radio_stats_interval: int
    sta_capability_interval: int
    sta_locate_timer: int
    ipsec_intf_cleanup: int
    ble_scan_report_intv: int
    drma_interval: int
    ap_reboot_wait_interval1: int
    ap_reboot_wait_time: str
    ap_reboot_wait_interval2: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Timers:
    """
    
    Endpoint: wireless_controller/timers
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
    ) -> TimersObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TimersObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
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
    "Timers",
    "TimersPayload",
    "TimersResponse",
    "TimersObject",
]