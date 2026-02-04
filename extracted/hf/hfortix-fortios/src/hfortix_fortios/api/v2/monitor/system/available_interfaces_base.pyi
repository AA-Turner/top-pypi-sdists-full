""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/available_interfaces
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

class AvailableInterfacesPayload(TypedDict, total=False):
    """Payload type for AvailableInterfaces operations."""
    mkey: str
    include_ha: bool
    view_type: str
    scope: Literal["vdom", "global"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class AvailableInterfacesResponse(TypedDict, total=False):
    """Response type for AvailableInterfaces - use with .dict property for typed dict access."""
    vlan_protocol: str
    vrf: str
    supports_fctrl_trunk: bool
    supports_fortiextender: bool
    supports_extension: bool
    is_used: bool
    is_zone: bool
    is_sdwan_zone: bool
    is_modem: bool
    is_modem_hidden: bool
    is_l2tp_enabled: bool
    is_l2tp_tunnel: bool
    is_used_by_aggregate: bool
    is_used_by_hw_composite: bool
    used_by_composite: bool
    is_used_by_switch: bool
    is_used_by_redundant: bool
    is_used_by_ha: bool
    is_used_by_vlan: bool
    is_used_by_emac_vlan: bool
    is_used_by_bypass: bool
    is_wifi: bool
    is_mesh_backhaul: bool
    is_local_bridge: bool
    supports_vap_security_exempt_list: bool
    is_usb_lte: bool
    is_usb_wwan: bool
    is_wwan: bool
    is_tunnel: bool
    is_nat_tunnel: bool
    is_sit_tunnel: bool
    is_ipsec_manualkey: bool
    is_ipsec_static: bool
    is_ipsec_dialup: bool
    is_ipsec_dialup_netdevice: bool
    is_ipsec_ddns: bool
    is_ipsec_aggregate: bool
    is_virtual_wire_pair_member: bool
    is_virtual_wire_pair_used: bool
    does_support_virtual_wire_pair: bool
    is_backplane: bool
    is_backplane_hidden: bool
    is_elbc: bool
    is_elbc_heartbeat: bool
    is_fortiextender: bool
    used_as_ip6_prefix_delegate: bool
    is_loopback: bool
    is_hdlc: bool
    is_vlan: bool
    is_wifi_vlan: bool
    is_fortilink_vlan: bool
    is_emac_vlan: bool
    is_vxlan: bool
    is_wifi_mesh: bool
    is_wifi_client: bool
    is_hardware_switch: bool
    is_software_switch: bool
    is_physical: bool
    is_vdom_link: bool
    is_fctrl_trunk: bool
    is_geneve: bool
    is_switchctl_interface_mode: bool
    is_switchctl_iot_scanning: bool
    has_switchctl_split_interface: bool
    is_ha_mgmt_intf: bool
    is_dedicated_mgmt: bool
    is_used_by_fctrl_trunk: bool
    is_npu_vdom_link: bool
    is_lan_extension: bool
    dynamic_addressing: bool
    pppoe_interface: bool
    dhcp_interface: bool
    device_id_enabled: bool
    valid_in_policy: bool
    valid_in_local_in_policy: bool
    dns_server_enabled: bool
    is_sslvpn: bool
    used_by_aggregate_or_switch: bool
    is_split_port: bool
    is_ethernet_trunk: bool
    is_aggregate: bool
    is_redundant: bool
    is_hard_switch_vlan: bool
    is_available_for_acl: bool
    explicit_web_proxy_enabled: bool
    explicit_ftp_proxy_enabled: bool
    is_hardware_switch_member: bool
    is_zone_member: bool
    is_zone_usable: bool
    is_virtual_wan_link_member: bool
    is_virtual_wan_link_capable: bool
    is_dhcp6_prefix_delegation: bool
    is_aggregatable: bool
    is_switch_capable: bool
    is_hard_switch_capable: bool
    is_explicit_proxyable: bool
    is_ftp_proxyable: bool
    is_dedicate_capable: bool
    is_ipsecable: bool
    is_routable: bool
    is_ha_heartbeatable: bool
    is_ha_monitorable: bool
    is_ha_mgmt_candidate: bool
    is_ha_heartbeat: bool
    is_onearm_sniffer: bool
    supports_fortilink: bool
    supports_onearm: bool
    supports_ieee802_1x: bool
    supports_poe: bool
    supports_poe_members: bool
    supports_stp: bool
    supports_dhcp: bool
    supports_device_id: bool
    supports_fortitelemetry: bool
    supports_vlan: bool
    supports_emac_vlan: bool
    supports_elbc_confsync: bool
    supports_pppoe: bool
    supports_secondary_ip: bool
    supports_dhcp_client: bool
    supports_ssid: bool
    supports_non_manual_addressing: bool
    supports_transceiver: bool
    used_by_policy: bool
    used_by_explicit_policy: bool
    used_by_route: bool
    used_by_shaping_policy: bool
    chip_id: int
    name: str
    port_group_number: int
    port_speed_opts: list[str]
    port_speed: str
    type: str
    icon: str
    out_of_scope: bool
    real_interface_name: str
    vdom: str
    is_system_interface: bool
    status: str
    is_vne_tunnel: bool
    alias: str
    in_bandwidth_limit: int
    out_bandwidth_limit: int
    dhcp4_client_count: int
    dhcp6_client_count: int
    role: str
    estimated_upstream_bandwidth: int
    estimated_downstream_bandwidth: int
    monitor_bandwidth: bool
    measured_upstream_bandwidth: int
    measured_downstream_bandwidth: int
    measure_time: int
    ipv4_addresses: list[str]
    ipv6_addresses: list[str]
    mac_address: str
    vlan_id: str
    is_nac_lan_primary_interface: bool
    nac_lan_primary_interface: str
    is_nac_lan_segment: bool
    link: str
    duplex: str
    speed: int
    members: list[str]
    ssid: str
    media: str
    poe_capable: bool
    poe_enabled: bool
    poe_status: str
    adsl: str
    fortiextender_id: str
    physical_switch: str
    description: str
    sdwan_zone: str
    vlan_interface: str
    tunnel_interface: str
    outgoing_interface: str
    vdom_link: str
    npu_vdom_link: str
    physical_interface: str
    zone: str
    virtual_wire_pair: str
    hardware_switch: str
    will_https_port_conflict_with_sslvpn: bool
    will_sslvpn_take_precedence_over_https: bool
    tx_packets: int
    rx_packets: int
    tx_bytes: int
    rx_bytes: int
    tx_errors: int
    rx_errors: int
    _performance: str
    is_dsl_lantiq: bool
    dsl: str
    allow_fabric_heartbeat: bool
    allow_ftm_push: bool
    supports_lldp_reception: bool
    has_lldp_reception_enabled: bool
    used_in_policy: bool
    is_shared_port: bool
    shared_port_medium: str


class AvailableInterfacesObject(FortiObject[AvailableInterfacesResponse]):
    """Typed FortiObject for AvailableInterfaces with field access."""
    vlan_protocol: str
    vrf: str
    supports_fctrl_trunk: bool
    supports_fortiextender: bool
    supports_extension: bool
    is_used: bool
    is_zone: bool
    is_sdwan_zone: bool
    is_modem: bool
    is_modem_hidden: bool
    is_l2tp_enabled: bool
    is_l2tp_tunnel: bool
    is_used_by_aggregate: bool
    is_used_by_hw_composite: bool
    used_by_composite: bool
    is_used_by_switch: bool
    is_used_by_redundant: bool
    is_used_by_ha: bool
    is_used_by_vlan: bool
    is_used_by_emac_vlan: bool
    is_used_by_bypass: bool
    is_wifi: bool
    is_mesh_backhaul: bool
    is_local_bridge: bool
    supports_vap_security_exempt_list: bool
    is_usb_lte: bool
    is_usb_wwan: bool
    is_wwan: bool
    is_tunnel: bool
    is_nat_tunnel: bool
    is_sit_tunnel: bool
    is_ipsec_manualkey: bool
    is_ipsec_static: bool
    is_ipsec_dialup: bool
    is_ipsec_dialup_netdevice: bool
    is_ipsec_ddns: bool
    is_ipsec_aggregate: bool
    is_virtual_wire_pair_member: bool
    is_virtual_wire_pair_used: bool
    does_support_virtual_wire_pair: bool
    is_backplane: bool
    is_backplane_hidden: bool
    is_elbc: bool
    is_elbc_heartbeat: bool
    is_fortiextender: bool
    used_as_ip6_prefix_delegate: bool
    is_loopback: bool
    is_hdlc: bool
    is_vlan: bool
    is_wifi_vlan: bool
    is_fortilink_vlan: bool
    is_emac_vlan: bool
    is_vxlan: bool
    is_wifi_mesh: bool
    is_wifi_client: bool
    is_hardware_switch: bool
    is_software_switch: bool
    is_physical: bool
    is_vdom_link: bool
    is_fctrl_trunk: bool
    is_geneve: bool
    is_switchctl_interface_mode: bool
    is_switchctl_iot_scanning: bool
    has_switchctl_split_interface: bool
    is_ha_mgmt_intf: bool
    is_dedicated_mgmt: bool
    is_used_by_fctrl_trunk: bool
    is_npu_vdom_link: bool
    is_lan_extension: bool
    dynamic_addressing: bool
    pppoe_interface: bool
    dhcp_interface: bool
    device_id_enabled: bool
    valid_in_policy: bool
    valid_in_local_in_policy: bool
    dns_server_enabled: bool
    is_sslvpn: bool
    used_by_aggregate_or_switch: bool
    is_split_port: bool
    is_ethernet_trunk: bool
    is_aggregate: bool
    is_redundant: bool
    is_hard_switch_vlan: bool
    is_available_for_acl: bool
    explicit_web_proxy_enabled: bool
    explicit_ftp_proxy_enabled: bool
    is_hardware_switch_member: bool
    is_zone_member: bool
    is_zone_usable: bool
    is_virtual_wan_link_member: bool
    is_virtual_wan_link_capable: bool
    is_dhcp6_prefix_delegation: bool
    is_aggregatable: bool
    is_switch_capable: bool
    is_hard_switch_capable: bool
    is_explicit_proxyable: bool
    is_ftp_proxyable: bool
    is_dedicate_capable: bool
    is_ipsecable: bool
    is_routable: bool
    is_ha_heartbeatable: bool
    is_ha_monitorable: bool
    is_ha_mgmt_candidate: bool
    is_ha_heartbeat: bool
    is_onearm_sniffer: bool
    supports_fortilink: bool
    supports_onearm: bool
    supports_ieee802_1x: bool
    supports_poe: bool
    supports_poe_members: bool
    supports_stp: bool
    supports_dhcp: bool
    supports_device_id: bool
    supports_fortitelemetry: bool
    supports_vlan: bool
    supports_emac_vlan: bool
    supports_elbc_confsync: bool
    supports_pppoe: bool
    supports_secondary_ip: bool
    supports_dhcp_client: bool
    supports_ssid: bool
    supports_non_manual_addressing: bool
    supports_transceiver: bool
    used_by_policy: bool
    used_by_explicit_policy: bool
    used_by_route: bool
    used_by_shaping_policy: bool
    chip_id: int
    name: str
    port_group_number: int
    port_speed_opts: list[str]
    port_speed: str
    type: str
    icon: str
    out_of_scope: bool
    real_interface_name: str
    vdom: str
    is_system_interface: bool
    status: str
    is_vne_tunnel: bool
    alias: str
    in_bandwidth_limit: int
    out_bandwidth_limit: int
    dhcp4_client_count: int
    dhcp6_client_count: int
    role: str
    estimated_upstream_bandwidth: int
    estimated_downstream_bandwidth: int
    monitor_bandwidth: bool
    measured_upstream_bandwidth: int
    measured_downstream_bandwidth: int
    measure_time: int
    ipv4_addresses: list[str]
    ipv6_addresses: list[str]
    mac_address: str
    vlan_id: str
    is_nac_lan_primary_interface: bool
    nac_lan_primary_interface: str
    is_nac_lan_segment: bool
    link: str
    duplex: str
    speed: int
    members: list[str]
    ssid: str
    media: str
    poe_capable: bool
    poe_enabled: bool
    poe_status: str
    adsl: str
    fortiextender_id: str
    physical_switch: str
    description: str
    sdwan_zone: str
    vlan_interface: str
    tunnel_interface: str
    outgoing_interface: str
    vdom_link: str
    npu_vdom_link: str
    physical_interface: str
    zone: str
    virtual_wire_pair: str
    hardware_switch: str
    will_https_port_conflict_with_sslvpn: bool
    will_sslvpn_take_precedence_over_https: bool
    tx_packets: int
    rx_packets: int
    tx_bytes: int
    rx_bytes: int
    tx_errors: int
    rx_errors: int
    _performance: str
    is_dsl_lantiq: bool
    dsl: str
    allow_fabric_heartbeat: bool
    allow_ftm_push: bool
    supports_lldp_reception: bool
    has_lldp_reception_enabled: bool
    used_in_policy: bool
    is_shared_port: bool
    shared_port_medium: str



# ================================================================
# Main Endpoint Class
# ================================================================

class AvailableInterfaces:
    """
    
    Endpoint: system/available_interfaces
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
        include_ha: bool | None = ...,
        view_type: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[AvailableInterfacesObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AvailableInterfacesPayload | None = ...,
        mkey: str | None = ...,
        include_ha: bool | None = ...,
        view_type: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AvailableInterfacesObject: ...




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
        payload_dict: AvailableInterfacesPayload | None = ...,
        mkey: str | None = ...,
        include_ha: bool | None = ...,
        view_type: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
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
    "AvailableInterfaces",
    "AvailableInterfacesResponse",
    "AvailableInterfacesObject",
]