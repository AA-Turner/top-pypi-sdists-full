""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/global_
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

class GlobalPayload(TypedDict, total=False):
    """Payload type for Global operations."""
    name: str
    location: str
    acd_process_count: int
    wpad_process_count: int
    image_download: Literal["enable", "disable"]
    rolling_wtp_upgrade: Literal["enable", "disable"]
    rolling_wtp_upgrade_threshold: str
    max_retransmit: int
    control_message_offload: str | list[str]
    data_ethernet_II: Literal["enable", "disable"]
    link_aggregation: Literal["enable", "disable"]
    mesh_eth_type: int
    fiapp_eth_type: int
    discovery_mc_addr: str
    discovery_mc_addr6: str
    max_clients: int
    rogue_scan_mac_adjacency: int
    ipsec_base_ip: str
    wtp_share: Literal["enable", "disable"]
    tunnel_mode: Literal["compatible", "strict"]
    nac_interval: int
    ap_log_server: Literal["enable", "disable"]
    ap_log_server_ip: str
    ap_log_server_port: int
    max_sta_offline: int
    max_sta_offline_ip2mac: int
    max_sta_cap: int
    max_sta_cap_wtp: int
    max_rogue_ap: int
    max_rogue_ap_wtp: int
    max_rogue_sta: int
    max_wids_entry: int
    max_ble_device: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GlobalResponse(TypedDict, total=False):
    """Response type for Global - use with .dict property for typed dict access."""
    name: str
    location: str
    acd_process_count: int
    wpad_process_count: int
    image_download: Literal["enable", "disable"]
    rolling_wtp_upgrade: Literal["enable", "disable"]
    rolling_wtp_upgrade_threshold: str
    max_retransmit: int
    control_message_offload: str
    data_ethernet_II: Literal["enable", "disable"]
    link_aggregation: Literal["enable", "disable"]
    mesh_eth_type: int
    fiapp_eth_type: int
    discovery_mc_addr: str
    discovery_mc_addr6: str
    max_clients: int
    rogue_scan_mac_adjacency: int
    ipsec_base_ip: str
    wtp_share: Literal["enable", "disable"]
    tunnel_mode: Literal["compatible", "strict"]
    nac_interval: int
    ap_log_server: Literal["enable", "disable"]
    ap_log_server_ip: str
    ap_log_server_port: int
    max_sta_offline: int
    max_sta_offline_ip2mac: int
    max_sta_cap: int
    max_sta_cap_wtp: int
    max_rogue_ap: int
    max_rogue_ap_wtp: int
    max_rogue_sta: int
    max_wids_entry: int
    max_ble_device: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GlobalObject(FortiObject):
    """Typed FortiObject for Global with field access."""
    name: str
    location: str
    acd_process_count: int
    wpad_process_count: int
    image_download: Literal["enable", "disable"]
    rolling_wtp_upgrade: Literal["enable", "disable"]
    rolling_wtp_upgrade_threshold: str
    max_retransmit: int
    control_message_offload: str
    data_ethernet_II: Literal["enable", "disable"]
    link_aggregation: Literal["enable", "disable"]
    mesh_eth_type: int
    fiapp_eth_type: int
    discovery_mc_addr: str
    discovery_mc_addr6: str
    max_clients: int
    rogue_scan_mac_adjacency: int
    ipsec_base_ip: str
    wtp_share: Literal["enable", "disable"]
    tunnel_mode: Literal["compatible", "strict"]
    nac_interval: int
    ap_log_server: Literal["enable", "disable"]
    ap_log_server_ip: str
    ap_log_server_port: int
    max_sta_offline: int
    max_sta_offline_ip2mac: int
    max_sta_cap: int
    max_sta_cap_wtp: int
    max_rogue_ap: int
    max_rogue_ap_wtp: int
    max_rogue_sta: int
    max_wids_entry: int
    max_ble_device: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Global:
    """
    
    Endpoint: wireless_controller/global_
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
    ) -> GlobalObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GlobalPayload | None = ...,
        name: str | None = ...,
        location: str | None = ...,
        acd_process_count: int | None = ...,
        wpad_process_count: int | None = ...,
        image_download: Literal["enable", "disable"] | None = ...,
        rolling_wtp_upgrade: Literal["enable", "disable"] | None = ...,
        rolling_wtp_upgrade_threshold: str | None = ...,
        max_retransmit: int | None = ...,
        control_message_offload: str | list[str] | None = ...,
        data_ethernet_II: Literal["enable", "disable"] | None = ...,
        link_aggregation: Literal["enable", "disable"] | None = ...,
        mesh_eth_type: int | None = ...,
        fiapp_eth_type: int | None = ...,
        discovery_mc_addr: str | None = ...,
        discovery_mc_addr6: str | None = ...,
        max_clients: int | None = ...,
        rogue_scan_mac_adjacency: int | None = ...,
        ipsec_base_ip: str | None = ...,
        wtp_share: Literal["enable", "disable"] | None = ...,
        tunnel_mode: Literal["compatible", "strict"] | None = ...,
        nac_interval: int | None = ...,
        ap_log_server: Literal["enable", "disable"] | None = ...,
        ap_log_server_ip: str | None = ...,
        ap_log_server_port: int | None = ...,
        max_sta_offline: int | None = ...,
        max_sta_offline_ip2mac: int | None = ...,
        max_sta_cap: int | None = ...,
        max_sta_cap_wtp: int | None = ...,
        max_rogue_ap: int | None = ...,
        max_rogue_ap_wtp: int | None = ...,
        max_rogue_sta: int | None = ...,
        max_wids_entry: int | None = ...,
        max_ble_device: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GlobalObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: GlobalPayload | None = ...,
        name: str | None = ...,
        location: str | None = ...,
        acd_process_count: int | None = ...,
        wpad_process_count: int | None = ...,
        image_download: Literal["enable", "disable"] | None = ...,
        rolling_wtp_upgrade: Literal["enable", "disable"] | None = ...,
        rolling_wtp_upgrade_threshold: str | None = ...,
        max_retransmit: int | None = ...,
        control_message_offload: Literal["ebp-frame", "aeroscout-tag", "ap-list", "sta-list", "sta-cap-list", "stats", "aeroscout-mu", "sta-health", "spectral-analysis"] | list[str] | None = ...,
        data_ethernet_II: Literal["enable", "disable"] | None = ...,
        link_aggregation: Literal["enable", "disable"] | None = ...,
        mesh_eth_type: int | None = ...,
        fiapp_eth_type: int | None = ...,
        discovery_mc_addr: str | None = ...,
        discovery_mc_addr6: str | None = ...,
        max_clients: int | None = ...,
        rogue_scan_mac_adjacency: int | None = ...,
        ipsec_base_ip: str | None = ...,
        wtp_share: Literal["enable", "disable"] | None = ...,
        tunnel_mode: Literal["compatible", "strict"] | None = ...,
        nac_interval: int | None = ...,
        ap_log_server: Literal["enable", "disable"] | None = ...,
        ap_log_server_ip: str | None = ...,
        ap_log_server_port: int | None = ...,
        max_sta_offline: int | None = ...,
        max_sta_offline_ip2mac: int | None = ...,
        max_sta_cap: int | None = ...,
        max_sta_cap_wtp: int | None = ...,
        max_rogue_ap: int | None = ...,
        max_rogue_ap_wtp: int | None = ...,
        max_rogue_sta: int | None = ...,
        max_wids_entry: int | None = ...,
        max_ble_device: int | None = ...,
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
    "Global",
    "GlobalPayload",
    "GlobalResponse",
    "GlobalObject",
]