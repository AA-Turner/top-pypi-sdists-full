""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/device/query
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

class QueryPayload(TypedDict, total=False):
    """Payload type for Query operations."""
    timestamp_from: int
    timestamp_to: int
    filters: Literal["exact", "contains", "greaterThanEqualTo", "lessThanEqualTo"]
    query_type: Literal["latest", "unified_latest", "unified_history"]
    view_type: Literal["device", "fortiswitch_client", "forticlient", "iot_vuln_info"]
    query_id: int
    cache_query: bool
    key_only: bool
    filter_logic: Literal["and", "or"]
    total_only: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class QueryResponse(TypedDict, total=False):
    """Response type for Query - use with .dict property for typed dict access."""
    avatar_source: str
    avatar_fingerprint: str
    detected_interface: str
    detected_interface_fortitelemetry: str
    dhcp_lease_status: str
    dhcp_lease_expire: str
    dhcp_lease_reserved: str
    dhcp_server_id: str
    domain: str
    email: str
    fortiap_id: str
    fortiap_ssid: str
    fortiap_name: str
    forticlient_id: str
    forticlient_gateway_interface: str
    gateway_interface_name: str
    forticlient_username: str
    forticlient_version: str
    ems_sn: str
    ems_tenant_id: str
    tags: str
    is_fortiswitch_client: str
    fortiswitch_name: str
    fortiswitch_id: str
    fortiswitch_serial: str
    fortiswitch_port_id: str
    fortiswitch_vlan_id: str
    fortiswitch_port_name: str
    fortiswitch_last_seen: str
    generation: str
    hardware_family: str
    hardware_type: str
    hardware_vendor: str
    hardware_version: str
    hostname: str
    ipv4_address: str
    ipv6_address: str
    is_detected_interface_role_wan: str
    is_forticlient_endpoint: str
    is_ems_registered: str
    is_forticlient_unauth_user: bool
    is_master_device: str
    is_online: str
    last_seen: str
    active_start_time: str
    active_end_time: str
    mac: str
    mac_firewall_address: str
    master_mac: str
    online_interfaces: list[str]
    on_net: str
    os_name: str
    os_version: str
    other_macs: list[str]
    phone: str
    purdue_level: str
    quarantined_on_forticlient: bool
    server: str
    unauth_user: str
    unjoined_forticlient_endpoint: bool
    user_info: str
    vuln_count: int
    vuln_count_critical: int
    vuln_count_high: int
    vuln_count_info: int
    vuln_count_low: int
    vuln_count_medium: int
    host_src: str
    user_info_src: str
    vdom: str
    is_fortiguard_src: str
    ztna_connected: bool
    directly_connected: bool
    vpn_connected: bool
    out_of_sync: bool
    iot_info: list[str]
    iot_vuln_count: int
    iot_vuln_count_critical: int
    iot_vuln_count_high: int
    iot_vuln_count_info: int
    iot_vuln_count_low: int
    iot_vuln_count_medium: int
    iot_kev_count: int
    total_vuln_count: int
    max_vuln_level: str
    fortifone_name: str
    fortifone_extension: str
    fortivoice_managed_serial: str
    device_type: str


class QueryObject(FortiObject[QueryResponse]):
    """Typed FortiObject for Query with field access."""
    avatar_source: str
    avatar_fingerprint: str
    detected_interface: str
    detected_interface_fortitelemetry: str
    dhcp_lease_status: str
    dhcp_lease_expire: str
    dhcp_lease_reserved: str
    dhcp_server_id: str
    domain: str
    email: str
    fortiap_id: str
    fortiap_ssid: str
    fortiap_name: str
    forticlient_id: str
    forticlient_gateway_interface: str
    gateway_interface_name: str
    forticlient_username: str
    forticlient_version: str
    ems_sn: str
    ems_tenant_id: str
    tags: str
    is_fortiswitch_client: str
    fortiswitch_name: str
    fortiswitch_id: str
    fortiswitch_serial: str
    fortiswitch_port_id: str
    fortiswitch_vlan_id: str
    fortiswitch_port_name: str
    fortiswitch_last_seen: str
    generation: str
    hardware_family: str
    hardware_type: str
    hardware_vendor: str
    hardware_version: str
    hostname: str
    ipv4_address: str
    ipv6_address: str
    is_detected_interface_role_wan: str
    is_forticlient_endpoint: str
    is_ems_registered: str
    is_forticlient_unauth_user: bool
    is_master_device: str
    is_online: str
    last_seen: str
    active_start_time: str
    active_end_time: str
    mac: str
    mac_firewall_address: str
    master_mac: str
    online_interfaces: list[str]
    on_net: str
    os_name: str
    os_version: str
    other_macs: list[str]
    phone: str
    purdue_level: str
    quarantined_on_forticlient: bool
    server: str
    unauth_user: str
    unjoined_forticlient_endpoint: bool
    user_info: str
    vuln_count: int
    vuln_count_critical: int
    vuln_count_high: int
    vuln_count_info: int
    vuln_count_low: int
    vuln_count_medium: int
    host_src: str
    user_info_src: str
    vdom: str
    is_fortiguard_src: str
    ztna_connected: bool
    directly_connected: bool
    vpn_connected: bool
    out_of_sync: bool
    iot_info: list[str]
    iot_vuln_count: int
    iot_vuln_count_critical: int
    iot_vuln_count_high: int
    iot_vuln_count_info: int
    iot_vuln_count_low: int
    iot_vuln_count_medium: int
    iot_kev_count: int
    total_vuln_count: int
    max_vuln_level: str
    fortifone_name: str
    fortifone_extension: str
    fortivoice_managed_serial: str
    device_type: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Query:
    """
    
    Endpoint: user/device/query
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
        timestamp_from: int | None = ...,
        timestamp_to: int | None = ...,
        filters: list[str] | None = ...,
        query_type: Literal["latest", "unified_latest", "unified_history"] | None = ...,
        view_type: Literal["device", "fortiswitch_client", "forticlient", "iot_vuln_info"] | None = ...,
        query_id: int | None = ...,
        cache_query: bool | None = ...,
        key_only: bool | None = ...,
        filter_logic: Literal["and", "or"] | None = ...,
        total_only: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[QueryObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: QueryPayload | None = ...,
        timestamp_from: int | None = ...,
        timestamp_to: int | None = ...,
        filters: Literal["exact", "contains", "greaterThanEqualTo", "lessThanEqualTo"] | None = ...,
        query_type: Literal["latest", "unified_latest", "unified_history"] | None = ...,
        view_type: Literal["device", "fortiswitch_client", "forticlient", "iot_vuln_info"] | None = ...,
        query_id: int | None = ...,
        cache_query: bool | None = ...,
        key_only: bool | None = ...,
        filter_logic: Literal["and", "or"] | None = ...,
        total_only: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QueryObject: ...




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
        payload_dict: QueryPayload | None = ...,
        timestamp_from: int | None = ...,
        timestamp_to: int | None = ...,
        filters: Literal["exact", "contains", "greaterThanEqualTo", "lessThanEqualTo"] | None = ...,
        query_type: Literal["latest", "unified_latest", "unified_history"] | None = ...,
        view_type: Literal["device", "fortiswitch_client", "forticlient", "iot_vuln_info"] | None = ...,
        query_id: int | None = ...,
        cache_query: bool | None = ...,
        key_only: bool | None = ...,
        filter_logic: Literal["and", "or"] | None = ...,
        total_only: bool | None = ...,
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
    "Query",
    "QueryResponse",
    "QueryObject",
]