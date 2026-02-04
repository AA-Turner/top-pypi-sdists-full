""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/settings
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

class SettingsGuidefaultpolicycolumnsItem(TypedDict, total=False):
    """Nested item for gui-default-policy-columns field."""
    name: str


class SettingsPayload(TypedDict, total=False):
    """Payload type for Settings operations."""
    comments: str
    vdom_type: Literal["traffic", "lan-extension", "admin"]
    lan_extension_controller_addr: str
    lan_extension_controller_port: int
    opmode: Literal["nat", "transparent"]
    ngfw_mode: Literal["profile-based", "policy-based"]
    http_external_dest: Literal["fortiweb", "forticache"]
    firewall_session_dirty: Literal["check-all", "check-new", "check-policy-option"]
    manageip: str
    gateway: str
    ip: str
    manageip6: str
    gateway6: str
    ip6: str
    device: str
    bfd: Literal["enable", "disable"]
    bfd_desired_min_tx: int
    bfd_required_min_rx: int
    bfd_detect_mult: int
    bfd_dont_enforce_src_port: Literal["enable", "disable"]
    utf8_spam_tagging: Literal["enable", "disable"]
    wccp_cache_engine: Literal["enable", "disable"]
    vpn_stats_log: str | list[str]
    vpn_stats_period: int
    v4_ecmp_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based"]
    mac_ttl: int
    fw_session_hairpin: Literal["enable", "disable"]
    prp_trailer_action: Literal["enable", "disable"]
    snat_hairpin_traffic: Literal["enable", "disable"]
    dhcp_proxy: Literal["enable", "disable"]
    dhcp_proxy_interface_select_method: Literal["auto", "sdwan", "specify"]
    dhcp_proxy_interface: str
    dhcp_proxy_vrf_select: int
    dhcp_server_ip: str | list[str]
    dhcp6_server_ip: str | list[str]
    central_nat: Literal["enable", "disable"]
    gui_default_policy_columns: str | list[str] | list[SettingsGuidefaultpolicycolumnsItem]
    lldp_reception: Literal["enable", "disable", "global"]
    lldp_transmission: Literal["enable", "disable", "global"]
    link_down_access: Literal["enable", "disable"]
    nat46_generate_ipv6_fragment_header: Literal["enable", "disable"]
    nat46_force_ipv4_packet_forwarding: Literal["enable", "disable"]
    nat64_force_ipv6_packet_forwarding: Literal["enable", "disable"]
    detect_unknown_esp: Literal["enable", "disable"]
    intree_ses_best_route: Literal["force", "disable"]
    auxiliary_session: Literal["enable", "disable"]
    asymroute: Literal["enable", "disable"]
    asymroute_icmp: Literal["enable", "disable"]
    tcp_session_without_syn: Literal["enable", "disable"]
    ses_denied_traffic: Literal["enable", "disable"]
    ses_denied_multicast_traffic: Literal["enable", "disable"]
    strict_src_check: Literal["enable", "disable"]
    allow_linkdown_path: Literal["enable", "disable"]
    asymroute6: Literal["enable", "disable"]
    asymroute6_icmp: Literal["enable", "disable"]
    sctp_session_without_init: Literal["enable", "disable"]
    sip_expectation: Literal["enable", "disable"]
    sip_nat_trace: Literal["enable", "disable"]
    h323_direct_model: Literal["disable", "enable"]
    status: Literal["enable", "disable"]
    sip_tcp_port: int | list[int]
    sip_udp_port: int | list[int]
    sip_ssl_port: int
    sccp_port: int
    multicast_forward: Literal["enable", "disable"]
    multicast_ttl_notchange: Literal["enable", "disable"]
    multicast_skip_policy: Literal["enable", "disable"]
    allow_subnet_overlap: Literal["enable", "disable"]
    deny_tcp_with_icmp: Literal["enable", "disable"]
    ecmp_max_paths: int
    discovered_device_timeout: int
    email_portal_check_dns: Literal["disable", "enable"]
    default_voip_alg_mode: Literal["proxy-based", "kernel-helper-based"]
    gui_icap: Literal["enable", "disable"]
    gui_implicit_policy: Literal["enable", "disable"]
    gui_dns_database: Literal["enable", "disable"]
    gui_load_balance: Literal["enable", "disable"]
    gui_multicast_policy: Literal["enable", "disable"]
    gui_dos_policy: Literal["enable", "disable"]
    gui_object_colors: Literal["enable", "disable"]
    gui_route_tag_address_creation: Literal["enable", "disable"]
    gui_voip_profile: Literal["enable", "disable"]
    gui_ap_profile: Literal["enable", "disable"]
    gui_security_profile_group: Literal["enable", "disable"]
    gui_local_in_policy: Literal["enable", "disable"]
    gui_wanopt_cache: Literal["enable", "disable"]
    gui_explicit_proxy: Literal["enable", "disable"]
    gui_dynamic_routing: Literal["enable", "disable"]
    gui_sslvpn_personal_bookmarks: Literal["enable", "disable"]
    gui_sslvpn_realms: Literal["enable", "disable"]
    gui_policy_based_ipsec: Literal["enable", "disable"]
    gui_threat_weight: Literal["enable", "disable"]
    gui_spamfilter: Literal["enable", "disable"]
    gui_file_filter: Literal["enable", "disable"]
    gui_application_control: Literal["enable", "disable"]
    gui_ips: Literal["enable", "disable"]
    gui_dhcp_advanced: Literal["enable", "disable"]
    gui_vpn: Literal["enable", "disable"]
    gui_sslvpn: Literal["enable", "disable"]
    gui_wireless_controller: Literal["enable", "disable"]
    gui_advanced_wireless_features: Literal["enable", "disable"]
    gui_switch_controller: Literal["enable", "disable"]
    gui_fortiap_split_tunneling: Literal["enable", "disable"]
    gui_webfilter_advanced: Literal["enable", "disable"]
    gui_traffic_shaping: Literal["enable", "disable"]
    gui_wan_load_balancing: Literal["enable", "disable"]
    gui_antivirus: Literal["enable", "disable"]
    gui_webfilter: Literal["enable", "disable"]
    gui_videofilter: Literal["enable", "disable"]
    gui_dnsfilter: Literal["enable", "disable"]
    gui_waf_profile: Literal["enable", "disable"]
    gui_dlp_profile: Literal["enable", "disable"]
    gui_dlp_advanced: Literal["enable", "disable"]
    gui_virtual_patch_profile: Literal["enable", "disable"]
    gui_casb: Literal["enable", "disable"]
    gui_fortiextender_controller: Literal["enable", "disable"]
    gui_advanced_policy: Literal["enable", "disable"]
    gui_allow_unnamed_policy: Literal["enable", "disable"]
    gui_email_collection: Literal["enable", "disable"]
    gui_multiple_interface_policy: Literal["enable", "disable"]
    gui_policy_disclaimer: Literal["enable", "disable"]
    gui_ztna: Literal["enable", "disable"]
    gui_ot: Literal["enable", "disable"]
    gui_dynamic_device_os_id: Literal["enable", "disable"]
    gui_gtp: Literal["enable", "disable"]
    location_id: str
    ike_session_resume: Literal["enable", "disable"]
    ike_quick_crash_detect: Literal["enable", "disable"]
    ike_dn_format: Literal["with-space", "no-space"]
    ike_port: int
    ike_tcp_port: int
    ike_policy_route: Literal["enable", "disable"]
    ike_detailed_event_logs: Literal["disable", "enable"]
    block_land_attack: Literal["disable", "enable"]
    default_app_port_as_service: Literal["enable", "disable"]
    fqdn_session_check: Literal["enable", "disable"]
    ext_resource_session_check: Literal["enable", "disable"]
    dyn_addr_session_check: Literal["enable", "disable"]
    default_policy_expiry_days: int
    gui_enforce_change_summary: Literal["disable", "require", "optional"]
    internet_service_database_cache: Literal["disable", "enable"]
    internet_service_app_ctrl_size: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingsResponse(TypedDict, total=False):
    """Response type for Settings - use with .dict property for typed dict access."""
    comments: str
    vdom_type: Literal["traffic", "lan-extension", "admin"]
    lan_extension_controller_addr: str
    lan_extension_controller_port: int
    opmode: Literal["nat", "transparent"]
    ngfw_mode: Literal["profile-based", "policy-based"]
    http_external_dest: Literal["fortiweb", "forticache"]
    firewall_session_dirty: Literal["check-all", "check-new", "check-policy-option"]
    manageip: str
    gateway: str
    ip: str
    manageip6: str
    gateway6: str
    ip6: str
    device: str
    bfd: Literal["enable", "disable"]
    bfd_desired_min_tx: int
    bfd_required_min_rx: int
    bfd_detect_mult: int
    bfd_dont_enforce_src_port: Literal["enable", "disable"]
    utf8_spam_tagging: Literal["enable", "disable"]
    wccp_cache_engine: Literal["enable", "disable"]
    vpn_stats_log: str
    vpn_stats_period: int
    v4_ecmp_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based"]
    mac_ttl: int
    fw_session_hairpin: Literal["enable", "disable"]
    prp_trailer_action: Literal["enable", "disable"]
    snat_hairpin_traffic: Literal["enable", "disable"]
    dhcp_proxy: Literal["enable", "disable"]
    dhcp_proxy_interface_select_method: Literal["auto", "sdwan", "specify"]
    dhcp_proxy_interface: str
    dhcp_proxy_vrf_select: int
    dhcp_server_ip: str | list[str]
    dhcp6_server_ip: str | list[str]
    central_nat: Literal["enable", "disable"]
    gui_default_policy_columns: list[SettingsGuidefaultpolicycolumnsItem]
    lldp_reception: Literal["enable", "disable", "global"]
    lldp_transmission: Literal["enable", "disable", "global"]
    link_down_access: Literal["enable", "disable"]
    nat46_generate_ipv6_fragment_header: Literal["enable", "disable"]
    nat46_force_ipv4_packet_forwarding: Literal["enable", "disable"]
    nat64_force_ipv6_packet_forwarding: Literal["enable", "disable"]
    detect_unknown_esp: Literal["enable", "disable"]
    intree_ses_best_route: Literal["force", "disable"]
    auxiliary_session: Literal["enable", "disable"]
    asymroute: Literal["enable", "disable"]
    asymroute_icmp: Literal["enable", "disable"]
    tcp_session_without_syn: Literal["enable", "disable"]
    ses_denied_traffic: Literal["enable", "disable"]
    ses_denied_multicast_traffic: Literal["enable", "disable"]
    strict_src_check: Literal["enable", "disable"]
    allow_linkdown_path: Literal["enable", "disable"]
    asymroute6: Literal["enable", "disable"]
    asymroute6_icmp: Literal["enable", "disable"]
    sctp_session_without_init: Literal["enable", "disable"]
    sip_expectation: Literal["enable", "disable"]
    sip_nat_trace: Literal["enable", "disable"]
    h323_direct_model: Literal["disable", "enable"]
    status: Literal["enable", "disable"]
    sip_tcp_port: int | list[int]
    sip_udp_port: int | list[int]
    sip_ssl_port: int
    sccp_port: int
    multicast_forward: Literal["enable", "disable"]
    multicast_ttl_notchange: Literal["enable", "disable"]
    multicast_skip_policy: Literal["enable", "disable"]
    allow_subnet_overlap: Literal["enable", "disable"]
    deny_tcp_with_icmp: Literal["enable", "disable"]
    ecmp_max_paths: int
    discovered_device_timeout: int
    email_portal_check_dns: Literal["disable", "enable"]
    default_voip_alg_mode: Literal["proxy-based", "kernel-helper-based"]
    gui_icap: Literal["enable", "disable"]
    gui_implicit_policy: Literal["enable", "disable"]
    gui_dns_database: Literal["enable", "disable"]
    gui_load_balance: Literal["enable", "disable"]
    gui_multicast_policy: Literal["enable", "disable"]
    gui_dos_policy: Literal["enable", "disable"]
    gui_object_colors: Literal["enable", "disable"]
    gui_route_tag_address_creation: Literal["enable", "disable"]
    gui_voip_profile: Literal["enable", "disable"]
    gui_ap_profile: Literal["enable", "disable"]
    gui_security_profile_group: Literal["enable", "disable"]
    gui_local_in_policy: Literal["enable", "disable"]
    gui_wanopt_cache: Literal["enable", "disable"]
    gui_explicit_proxy: Literal["enable", "disable"]
    gui_dynamic_routing: Literal["enable", "disable"]
    gui_sslvpn_personal_bookmarks: Literal["enable", "disable"]
    gui_sslvpn_realms: Literal["enable", "disable"]
    gui_policy_based_ipsec: Literal["enable", "disable"]
    gui_threat_weight: Literal["enable", "disable"]
    gui_spamfilter: Literal["enable", "disable"]
    gui_file_filter: Literal["enable", "disable"]
    gui_application_control: Literal["enable", "disable"]
    gui_ips: Literal["enable", "disable"]
    gui_dhcp_advanced: Literal["enable", "disable"]
    gui_vpn: Literal["enable", "disable"]
    gui_sslvpn: Literal["enable", "disable"]
    gui_wireless_controller: Literal["enable", "disable"]
    gui_advanced_wireless_features: Literal["enable", "disable"]
    gui_switch_controller: Literal["enable", "disable"]
    gui_fortiap_split_tunneling: Literal["enable", "disable"]
    gui_webfilter_advanced: Literal["enable", "disable"]
    gui_traffic_shaping: Literal["enable", "disable"]
    gui_wan_load_balancing: Literal["enable", "disable"]
    gui_antivirus: Literal["enable", "disable"]
    gui_webfilter: Literal["enable", "disable"]
    gui_videofilter: Literal["enable", "disable"]
    gui_dnsfilter: Literal["enable", "disable"]
    gui_waf_profile: Literal["enable", "disable"]
    gui_dlp_profile: Literal["enable", "disable"]
    gui_dlp_advanced: Literal["enable", "disable"]
    gui_virtual_patch_profile: Literal["enable", "disable"]
    gui_casb: Literal["enable", "disable"]
    gui_fortiextender_controller: Literal["enable", "disable"]
    gui_advanced_policy: Literal["enable", "disable"]
    gui_allow_unnamed_policy: Literal["enable", "disable"]
    gui_email_collection: Literal["enable", "disable"]
    gui_multiple_interface_policy: Literal["enable", "disable"]
    gui_policy_disclaimer: Literal["enable", "disable"]
    gui_ztna: Literal["enable", "disable"]
    gui_ot: Literal["enable", "disable"]
    gui_dynamic_device_os_id: Literal["enable", "disable"]
    gui_gtp: Literal["enable", "disable"]
    location_id: str
    ike_session_resume: Literal["enable", "disable"]
    ike_quick_crash_detect: Literal["enable", "disable"]
    ike_dn_format: Literal["with-space", "no-space"]
    ike_port: int
    ike_tcp_port: int
    ike_policy_route: Literal["enable", "disable"]
    ike_detailed_event_logs: Literal["disable", "enable"]
    block_land_attack: Literal["disable", "enable"]
    default_app_port_as_service: Literal["enable", "disable"]
    fqdn_session_check: Literal["enable", "disable"]
    ext_resource_session_check: Literal["enable", "disable"]
    dyn_addr_session_check: Literal["enable", "disable"]
    default_policy_expiry_days: int
    gui_enforce_change_summary: Literal["disable", "require", "optional"]
    internet_service_database_cache: Literal["disable", "enable"]
    internet_service_app_ctrl_size: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingsGuidefaultpolicycolumnsItemObject(FortiObject[SettingsGuidefaultpolicycolumnsItem]):
    """Typed object for gui-default-policy-columns table items with attribute access."""
    name: str


class SettingsObject(FortiObject):
    """Typed FortiObject for Settings with field access."""
    comments: str
    vdom_type: Literal["traffic", "lan-extension", "admin"]
    lan_extension_controller_addr: str
    lan_extension_controller_port: int
    opmode: Literal["nat", "transparent"]
    ngfw_mode: Literal["profile-based", "policy-based"]
    http_external_dest: Literal["fortiweb", "forticache"]
    firewall_session_dirty: Literal["check-all", "check-new", "check-policy-option"]
    manageip: str
    gateway: str
    ip: str
    manageip6: str
    gateway6: str
    ip6: str
    device: str
    bfd: Literal["enable", "disable"]
    bfd_desired_min_tx: int
    bfd_required_min_rx: int
    bfd_detect_mult: int
    bfd_dont_enforce_src_port: Literal["enable", "disable"]
    utf8_spam_tagging: Literal["enable", "disable"]
    wccp_cache_engine: Literal["enable", "disable"]
    vpn_stats_log: str
    vpn_stats_period: int
    v4_ecmp_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based"]
    mac_ttl: int
    fw_session_hairpin: Literal["enable", "disable"]
    prp_trailer_action: Literal["enable", "disable"]
    snat_hairpin_traffic: Literal["enable", "disable"]
    dhcp_proxy: Literal["enable", "disable"]
    dhcp_proxy_interface_select_method: Literal["auto", "sdwan", "specify"]
    dhcp_proxy_interface: str
    dhcp_proxy_vrf_select: int
    dhcp_server_ip: str | list[str]
    dhcp6_server_ip: str | list[str]
    central_nat: Literal["enable", "disable"]
    gui_default_policy_columns: FortiObjectList[SettingsGuidefaultpolicycolumnsItemObject]
    lldp_reception: Literal["enable", "disable", "global"]
    lldp_transmission: Literal["enable", "disable", "global"]
    link_down_access: Literal["enable", "disable"]
    nat46_generate_ipv6_fragment_header: Literal["enable", "disable"]
    nat46_force_ipv4_packet_forwarding: Literal["enable", "disable"]
    nat64_force_ipv6_packet_forwarding: Literal["enable", "disable"]
    detect_unknown_esp: Literal["enable", "disable"]
    intree_ses_best_route: Literal["force", "disable"]
    auxiliary_session: Literal["enable", "disable"]
    asymroute: Literal["enable", "disable"]
    asymroute_icmp: Literal["enable", "disable"]
    tcp_session_without_syn: Literal["enable", "disable"]
    ses_denied_traffic: Literal["enable", "disable"]
    ses_denied_multicast_traffic: Literal["enable", "disable"]
    strict_src_check: Literal["enable", "disable"]
    allow_linkdown_path: Literal["enable", "disable"]
    asymroute6: Literal["enable", "disable"]
    asymroute6_icmp: Literal["enable", "disable"]
    sctp_session_without_init: Literal["enable", "disable"]
    sip_expectation: Literal["enable", "disable"]
    sip_nat_trace: Literal["enable", "disable"]
    h323_direct_model: Literal["disable", "enable"]
    status: Literal["enable", "disable"]
    sip_tcp_port: int | list[int]
    sip_udp_port: int | list[int]
    sip_ssl_port: int
    sccp_port: int
    multicast_forward: Literal["enable", "disable"]
    multicast_ttl_notchange: Literal["enable", "disable"]
    multicast_skip_policy: Literal["enable", "disable"]
    allow_subnet_overlap: Literal["enable", "disable"]
    deny_tcp_with_icmp: Literal["enable", "disable"]
    ecmp_max_paths: int
    discovered_device_timeout: int
    email_portal_check_dns: Literal["disable", "enable"]
    default_voip_alg_mode: Literal["proxy-based", "kernel-helper-based"]
    gui_icap: Literal["enable", "disable"]
    gui_implicit_policy: Literal["enable", "disable"]
    gui_dns_database: Literal["enable", "disable"]
    gui_load_balance: Literal["enable", "disable"]
    gui_multicast_policy: Literal["enable", "disable"]
    gui_dos_policy: Literal["enable", "disable"]
    gui_object_colors: Literal["enable", "disable"]
    gui_route_tag_address_creation: Literal["enable", "disable"]
    gui_voip_profile: Literal["enable", "disable"]
    gui_ap_profile: Literal["enable", "disable"]
    gui_security_profile_group: Literal["enable", "disable"]
    gui_local_in_policy: Literal["enable", "disable"]
    gui_wanopt_cache: Literal["enable", "disable"]
    gui_explicit_proxy: Literal["enable", "disable"]
    gui_dynamic_routing: Literal["enable", "disable"]
    gui_sslvpn_personal_bookmarks: Literal["enable", "disable"]
    gui_sslvpn_realms: Literal["enable", "disable"]
    gui_policy_based_ipsec: Literal["enable", "disable"]
    gui_threat_weight: Literal["enable", "disable"]
    gui_spamfilter: Literal["enable", "disable"]
    gui_file_filter: Literal["enable", "disable"]
    gui_application_control: Literal["enable", "disable"]
    gui_ips: Literal["enable", "disable"]
    gui_dhcp_advanced: Literal["enable", "disable"]
    gui_vpn: Literal["enable", "disable"]
    gui_sslvpn: Literal["enable", "disable"]
    gui_wireless_controller: Literal["enable", "disable"]
    gui_advanced_wireless_features: Literal["enable", "disable"]
    gui_switch_controller: Literal["enable", "disable"]
    gui_fortiap_split_tunneling: Literal["enable", "disable"]
    gui_webfilter_advanced: Literal["enable", "disable"]
    gui_traffic_shaping: Literal["enable", "disable"]
    gui_wan_load_balancing: Literal["enable", "disable"]
    gui_antivirus: Literal["enable", "disable"]
    gui_webfilter: Literal["enable", "disable"]
    gui_videofilter: Literal["enable", "disable"]
    gui_dnsfilter: Literal["enable", "disable"]
    gui_waf_profile: Literal["enable", "disable"]
    gui_dlp_profile: Literal["enable", "disable"]
    gui_dlp_advanced: Literal["enable", "disable"]
    gui_virtual_patch_profile: Literal["enable", "disable"]
    gui_casb: Literal["enable", "disable"]
    gui_fortiextender_controller: Literal["enable", "disable"]
    gui_advanced_policy: Literal["enable", "disable"]
    gui_allow_unnamed_policy: Literal["enable", "disable"]
    gui_email_collection: Literal["enable", "disable"]
    gui_multiple_interface_policy: Literal["enable", "disable"]
    gui_policy_disclaimer: Literal["enable", "disable"]
    gui_ztna: Literal["enable", "disable"]
    gui_ot: Literal["enable", "disable"]
    gui_dynamic_device_os_id: Literal["enable", "disable"]
    gui_gtp: Literal["enable", "disable"]
    location_id: str
    ike_session_resume: Literal["enable", "disable"]
    ike_quick_crash_detect: Literal["enable", "disable"]
    ike_dn_format: Literal["with-space", "no-space"]
    ike_port: int
    ike_tcp_port: int
    ike_policy_route: Literal["enable", "disable"]
    ike_detailed_event_logs: Literal["disable", "enable"]
    block_land_attack: Literal["disable", "enable"]
    default_app_port_as_service: Literal["enable", "disable"]
    fqdn_session_check: Literal["enable", "disable"]
    ext_resource_session_check: Literal["enable", "disable"]
    dyn_addr_session_check: Literal["enable", "disable"]
    default_policy_expiry_days: int
    gui_enforce_change_summary: Literal["disable", "require", "optional"]
    internet_service_database_cache: Literal["disable", "enable"]
    internet_service_app_ctrl_size: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Settings:
    """
    
    Endpoint: system/settings
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingsObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        comments: str | None = ...,
        vdom_type: Literal["traffic", "lan-extension", "admin"] | None = ...,
        lan_extension_controller_addr: str | None = ...,
        lan_extension_controller_port: int | None = ...,
        opmode: Literal["nat", "transparent"] | None = ...,
        ngfw_mode: Literal["profile-based", "policy-based"] | None = ...,
        http_external_dest: Literal["fortiweb", "forticache"] | None = ...,
        firewall_session_dirty: Literal["check-all", "check-new", "check-policy-option"] | None = ...,
        manageip: str | None = ...,
        gateway: str | None = ...,
        ip: str | None = ...,
        manageip6: str | None = ...,
        gateway6: str | None = ...,
        ip6: str | None = ...,
        device: str | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        bfd_desired_min_tx: int | None = ...,
        bfd_required_min_rx: int | None = ...,
        bfd_detect_mult: int | None = ...,
        bfd_dont_enforce_src_port: Literal["enable", "disable"] | None = ...,
        utf8_spam_tagging: Literal["enable", "disable"] | None = ...,
        wccp_cache_engine: Literal["enable", "disable"] | None = ...,
        vpn_stats_log: str | list[str] | None = ...,
        vpn_stats_period: int | None = ...,
        v4_ecmp_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based"] | None = ...,
        mac_ttl: int | None = ...,
        fw_session_hairpin: Literal["enable", "disable"] | None = ...,
        prp_trailer_action: Literal["enable", "disable"] | None = ...,
        snat_hairpin_traffic: Literal["enable", "disable"] | None = ...,
        dhcp_proxy: Literal["enable", "disable"] | None = ...,
        dhcp_proxy_interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        dhcp_proxy_interface: str | None = ...,
        dhcp_proxy_vrf_select: int | None = ...,
        dhcp_server_ip: str | list[str] | None = ...,
        dhcp6_server_ip: str | list[str] | None = ...,
        central_nat: Literal["enable", "disable"] | None = ...,
        gui_default_policy_columns: str | list[str] | list[SettingsGuidefaultpolicycolumnsItem] | None = ...,
        lldp_reception: Literal["enable", "disable", "global"] | None = ...,
        lldp_transmission: Literal["enable", "disable", "global"] | None = ...,
        link_down_access: Literal["enable", "disable"] | None = ...,
        nat46_generate_ipv6_fragment_header: Literal["enable", "disable"] | None = ...,
        nat46_force_ipv4_packet_forwarding: Literal["enable", "disable"] | None = ...,
        nat64_force_ipv6_packet_forwarding: Literal["enable", "disable"] | None = ...,
        detect_unknown_esp: Literal["enable", "disable"] | None = ...,
        intree_ses_best_route: Literal["force", "disable"] | None = ...,
        auxiliary_session: Literal["enable", "disable"] | None = ...,
        asymroute: Literal["enable", "disable"] | None = ...,
        asymroute_icmp: Literal["enable", "disable"] | None = ...,
        tcp_session_without_syn: Literal["enable", "disable"] | None = ...,
        ses_denied_traffic: Literal["enable", "disable"] | None = ...,
        ses_denied_multicast_traffic: Literal["enable", "disable"] | None = ...,
        strict_src_check: Literal["enable", "disable"] | None = ...,
        allow_linkdown_path: Literal["enable", "disable"] | None = ...,
        asymroute6: Literal["enable", "disable"] | None = ...,
        asymroute6_icmp: Literal["enable", "disable"] | None = ...,
        sctp_session_without_init: Literal["enable", "disable"] | None = ...,
        sip_expectation: Literal["enable", "disable"] | None = ...,
        sip_nat_trace: Literal["enable", "disable"] | None = ...,
        h323_direct_model: Literal["disable", "enable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        sip_tcp_port: int | list[int] | None = ...,
        sip_udp_port: int | list[int] | None = ...,
        sip_ssl_port: int | None = ...,
        sccp_port: int | None = ...,
        multicast_forward: Literal["enable", "disable"] | None = ...,
        multicast_ttl_notchange: Literal["enable", "disable"] | None = ...,
        multicast_skip_policy: Literal["enable", "disable"] | None = ...,
        allow_subnet_overlap: Literal["enable", "disable"] | None = ...,
        deny_tcp_with_icmp: Literal["enable", "disable"] | None = ...,
        ecmp_max_paths: int | None = ...,
        discovered_device_timeout: int | None = ...,
        email_portal_check_dns: Literal["disable", "enable"] | None = ...,
        default_voip_alg_mode: Literal["proxy-based", "kernel-helper-based"] | None = ...,
        gui_icap: Literal["enable", "disable"] | None = ...,
        gui_implicit_policy: Literal["enable", "disable"] | None = ...,
        gui_dns_database: Literal["enable", "disable"] | None = ...,
        gui_load_balance: Literal["enable", "disable"] | None = ...,
        gui_multicast_policy: Literal["enable", "disable"] | None = ...,
        gui_dos_policy: Literal["enable", "disable"] | None = ...,
        gui_object_colors: Literal["enable", "disable"] | None = ...,
        gui_route_tag_address_creation: Literal["enable", "disable"] | None = ...,
        gui_voip_profile: Literal["enable", "disable"] | None = ...,
        gui_ap_profile: Literal["enable", "disable"] | None = ...,
        gui_security_profile_group: Literal["enable", "disable"] | None = ...,
        gui_local_in_policy: Literal["enable", "disable"] | None = ...,
        gui_wanopt_cache: Literal["enable", "disable"] | None = ...,
        gui_explicit_proxy: Literal["enable", "disable"] | None = ...,
        gui_dynamic_routing: Literal["enable", "disable"] | None = ...,
        gui_sslvpn_personal_bookmarks: Literal["enable", "disable"] | None = ...,
        gui_sslvpn_realms: Literal["enable", "disable"] | None = ...,
        gui_policy_based_ipsec: Literal["enable", "disable"] | None = ...,
        gui_threat_weight: Literal["enable", "disable"] | None = ...,
        gui_spamfilter: Literal["enable", "disable"] | None = ...,
        gui_file_filter: Literal["enable", "disable"] | None = ...,
        gui_application_control: Literal["enable", "disable"] | None = ...,
        gui_ips: Literal["enable", "disable"] | None = ...,
        gui_dhcp_advanced: Literal["enable", "disable"] | None = ...,
        gui_vpn: Literal["enable", "disable"] | None = ...,
        gui_sslvpn: Literal["enable", "disable"] | None = ...,
        gui_wireless_controller: Literal["enable", "disable"] | None = ...,
        gui_advanced_wireless_features: Literal["enable", "disable"] | None = ...,
        gui_switch_controller: Literal["enable", "disable"] | None = ...,
        gui_fortiap_split_tunneling: Literal["enable", "disable"] | None = ...,
        gui_webfilter_advanced: Literal["enable", "disable"] | None = ...,
        gui_traffic_shaping: Literal["enable", "disable"] | None = ...,
        gui_wan_load_balancing: Literal["enable", "disable"] | None = ...,
        gui_antivirus: Literal["enable", "disable"] | None = ...,
        gui_webfilter: Literal["enable", "disable"] | None = ...,
        gui_videofilter: Literal["enable", "disable"] | None = ...,
        gui_dnsfilter: Literal["enable", "disable"] | None = ...,
        gui_waf_profile: Literal["enable", "disable"] | None = ...,
        gui_dlp_profile: Literal["enable", "disable"] | None = ...,
        gui_dlp_advanced: Literal["enable", "disable"] | None = ...,
        gui_virtual_patch_profile: Literal["enable", "disable"] | None = ...,
        gui_casb: Literal["enable", "disable"] | None = ...,
        gui_fortiextender_controller: Literal["enable", "disable"] | None = ...,
        gui_advanced_policy: Literal["enable", "disable"] | None = ...,
        gui_allow_unnamed_policy: Literal["enable", "disable"] | None = ...,
        gui_email_collection: Literal["enable", "disable"] | None = ...,
        gui_multiple_interface_policy: Literal["enable", "disable"] | None = ...,
        gui_policy_disclaimer: Literal["enable", "disable"] | None = ...,
        gui_ztna: Literal["enable", "disable"] | None = ...,
        gui_ot: Literal["enable", "disable"] | None = ...,
        gui_dynamic_device_os_id: Literal["enable", "disable"] | None = ...,
        gui_gtp: Literal["enable", "disable"] | None = ...,
        location_id: str | None = ...,
        ike_session_resume: Literal["enable", "disable"] | None = ...,
        ike_quick_crash_detect: Literal["enable", "disable"] | None = ...,
        ike_dn_format: Literal["with-space", "no-space"] | None = ...,
        ike_port: int | None = ...,
        ike_tcp_port: int | None = ...,
        ike_policy_route: Literal["enable", "disable"] | None = ...,
        ike_detailed_event_logs: Literal["disable", "enable"] | None = ...,
        block_land_attack: Literal["disable", "enable"] | None = ...,
        default_app_port_as_service: Literal["enable", "disable"] | None = ...,
        fqdn_session_check: Literal["enable", "disable"] | None = ...,
        ext_resource_session_check: Literal["enable", "disable"] | None = ...,
        dyn_addr_session_check: Literal["enable", "disable"] | None = ...,
        default_policy_expiry_days: int | None = ...,
        gui_enforce_change_summary: Literal["disable", "require", "optional"] | None = ...,
        internet_service_database_cache: Literal["disable", "enable"] | None = ...,
        internet_service_app_ctrl_size: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingsObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
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
        payload_dict: SettingsPayload | None = ...,
        comments: str | None = ...,
        vdom_type: Literal["traffic", "lan-extension", "admin"] | None = ...,
        lan_extension_controller_addr: str | None = ...,
        lan_extension_controller_port: int | None = ...,
        opmode: Literal["nat", "transparent"] | None = ...,
        ngfw_mode: Literal["profile-based", "policy-based"] | None = ...,
        http_external_dest: Literal["fortiweb", "forticache"] | None = ...,
        firewall_session_dirty: Literal["check-all", "check-new", "check-policy-option"] | None = ...,
        manageip: str | None = ...,
        gateway: str | None = ...,
        ip: str | None = ...,
        manageip6: str | None = ...,
        gateway6: str | None = ...,
        ip6: str | None = ...,
        device: str | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        bfd_desired_min_tx: int | None = ...,
        bfd_required_min_rx: int | None = ...,
        bfd_detect_mult: int | None = ...,
        bfd_dont_enforce_src_port: Literal["enable", "disable"] | None = ...,
        utf8_spam_tagging: Literal["enable", "disable"] | None = ...,
        wccp_cache_engine: Literal["enable", "disable"] | None = ...,
        vpn_stats_log: Literal["ipsec", "pptp", "l2tp", "ssl"] | list[str] | None = ...,
        vpn_stats_period: int | None = ...,
        v4_ecmp_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based"] | None = ...,
        mac_ttl: int | None = ...,
        fw_session_hairpin: Literal["enable", "disable"] | None = ...,
        prp_trailer_action: Literal["enable", "disable"] | None = ...,
        snat_hairpin_traffic: Literal["enable", "disable"] | None = ...,
        dhcp_proxy: Literal["enable", "disable"] | None = ...,
        dhcp_proxy_interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        dhcp_proxy_interface: str | None = ...,
        dhcp_proxy_vrf_select: int | None = ...,
        dhcp_server_ip: str | list[str] | None = ...,
        dhcp6_server_ip: str | list[str] | None = ...,
        central_nat: Literal["enable", "disable"] | None = ...,
        gui_default_policy_columns: str | list[str] | list[SettingsGuidefaultpolicycolumnsItem] | None = ...,
        lldp_reception: Literal["enable", "disable", "global"] | None = ...,
        lldp_transmission: Literal["enable", "disable", "global"] | None = ...,
        link_down_access: Literal["enable", "disable"] | None = ...,
        nat46_generate_ipv6_fragment_header: Literal["enable", "disable"] | None = ...,
        nat46_force_ipv4_packet_forwarding: Literal["enable", "disable"] | None = ...,
        nat64_force_ipv6_packet_forwarding: Literal["enable", "disable"] | None = ...,
        detect_unknown_esp: Literal["enable", "disable"] | None = ...,
        intree_ses_best_route: Literal["force", "disable"] | None = ...,
        auxiliary_session: Literal["enable", "disable"] | None = ...,
        asymroute: Literal["enable", "disable"] | None = ...,
        asymroute_icmp: Literal["enable", "disable"] | None = ...,
        tcp_session_without_syn: Literal["enable", "disable"] | None = ...,
        ses_denied_traffic: Literal["enable", "disable"] | None = ...,
        ses_denied_multicast_traffic: Literal["enable", "disable"] | None = ...,
        strict_src_check: Literal["enable", "disable"] | None = ...,
        allow_linkdown_path: Literal["enable", "disable"] | None = ...,
        asymroute6: Literal["enable", "disable"] | None = ...,
        asymroute6_icmp: Literal["enable", "disable"] | None = ...,
        sctp_session_without_init: Literal["enable", "disable"] | None = ...,
        sip_expectation: Literal["enable", "disable"] | None = ...,
        sip_nat_trace: Literal["enable", "disable"] | None = ...,
        h323_direct_model: Literal["disable", "enable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        sip_tcp_port: int | list[int] | None = ...,
        sip_udp_port: int | list[int] | None = ...,
        sip_ssl_port: int | None = ...,
        sccp_port: int | None = ...,
        multicast_forward: Literal["enable", "disable"] | None = ...,
        multicast_ttl_notchange: Literal["enable", "disable"] | None = ...,
        multicast_skip_policy: Literal["enable", "disable"] | None = ...,
        allow_subnet_overlap: Literal["enable", "disable"] | None = ...,
        deny_tcp_with_icmp: Literal["enable", "disable"] | None = ...,
        ecmp_max_paths: int | None = ...,
        discovered_device_timeout: int | None = ...,
        email_portal_check_dns: Literal["disable", "enable"] | None = ...,
        default_voip_alg_mode: Literal["proxy-based", "kernel-helper-based"] | None = ...,
        gui_icap: Literal["enable", "disable"] | None = ...,
        gui_implicit_policy: Literal["enable", "disable"] | None = ...,
        gui_dns_database: Literal["enable", "disable"] | None = ...,
        gui_load_balance: Literal["enable", "disable"] | None = ...,
        gui_multicast_policy: Literal["enable", "disable"] | None = ...,
        gui_dos_policy: Literal["enable", "disable"] | None = ...,
        gui_object_colors: Literal["enable", "disable"] | None = ...,
        gui_route_tag_address_creation: Literal["enable", "disable"] | None = ...,
        gui_voip_profile: Literal["enable", "disable"] | None = ...,
        gui_ap_profile: Literal["enable", "disable"] | None = ...,
        gui_security_profile_group: Literal["enable", "disable"] | None = ...,
        gui_local_in_policy: Literal["enable", "disable"] | None = ...,
        gui_wanopt_cache: Literal["enable", "disable"] | None = ...,
        gui_explicit_proxy: Literal["enable", "disable"] | None = ...,
        gui_dynamic_routing: Literal["enable", "disable"] | None = ...,
        gui_sslvpn_personal_bookmarks: Literal["enable", "disable"] | None = ...,
        gui_sslvpn_realms: Literal["enable", "disable"] | None = ...,
        gui_policy_based_ipsec: Literal["enable", "disable"] | None = ...,
        gui_threat_weight: Literal["enable", "disable"] | None = ...,
        gui_spamfilter: Literal["enable", "disable"] | None = ...,
        gui_file_filter: Literal["enable", "disable"] | None = ...,
        gui_application_control: Literal["enable", "disable"] | None = ...,
        gui_ips: Literal["enable", "disable"] | None = ...,
        gui_dhcp_advanced: Literal["enable", "disable"] | None = ...,
        gui_vpn: Literal["enable", "disable"] | None = ...,
        gui_sslvpn: Literal["enable", "disable"] | None = ...,
        gui_wireless_controller: Literal["enable", "disable"] | None = ...,
        gui_advanced_wireless_features: Literal["enable", "disable"] | None = ...,
        gui_switch_controller: Literal["enable", "disable"] | None = ...,
        gui_fortiap_split_tunneling: Literal["enable", "disable"] | None = ...,
        gui_webfilter_advanced: Literal["enable", "disable"] | None = ...,
        gui_traffic_shaping: Literal["enable", "disable"] | None = ...,
        gui_wan_load_balancing: Literal["enable", "disable"] | None = ...,
        gui_antivirus: Literal["enable", "disable"] | None = ...,
        gui_webfilter: Literal["enable", "disable"] | None = ...,
        gui_videofilter: Literal["enable", "disable"] | None = ...,
        gui_dnsfilter: Literal["enable", "disable"] | None = ...,
        gui_waf_profile: Literal["enable", "disable"] | None = ...,
        gui_dlp_profile: Literal["enable", "disable"] | None = ...,
        gui_dlp_advanced: Literal["enable", "disable"] | None = ...,
        gui_virtual_patch_profile: Literal["enable", "disable"] | None = ...,
        gui_casb: Literal["enable", "disable"] | None = ...,
        gui_fortiextender_controller: Literal["enable", "disable"] | None = ...,
        gui_advanced_policy: Literal["enable", "disable"] | None = ...,
        gui_allow_unnamed_policy: Literal["enable", "disable"] | None = ...,
        gui_email_collection: Literal["enable", "disable"] | None = ...,
        gui_multiple_interface_policy: Literal["enable", "disable"] | None = ...,
        gui_policy_disclaimer: Literal["enable", "disable"] | None = ...,
        gui_ztna: Literal["enable", "disable"] | None = ...,
        gui_ot: Literal["enable", "disable"] | None = ...,
        gui_dynamic_device_os_id: Literal["enable", "disable"] | None = ...,
        gui_gtp: Literal["enable", "disable"] | None = ...,
        location_id: str | None = ...,
        ike_session_resume: Literal["enable", "disable"] | None = ...,
        ike_quick_crash_detect: Literal["enable", "disable"] | None = ...,
        ike_dn_format: Literal["with-space", "no-space"] | None = ...,
        ike_port: int | None = ...,
        ike_tcp_port: int | None = ...,
        ike_policy_route: Literal["enable", "disable"] | None = ...,
        ike_detailed_event_logs: Literal["disable", "enable"] | None = ...,
        block_land_attack: Literal["disable", "enable"] | None = ...,
        default_app_port_as_service: Literal["enable", "disable"] | None = ...,
        fqdn_session_check: Literal["enable", "disable"] | None = ...,
        ext_resource_session_check: Literal["enable", "disable"] | None = ...,
        dyn_addr_session_check: Literal["enable", "disable"] | None = ...,
        default_policy_expiry_days: int | None = ...,
        gui_enforce_change_summary: Literal["disable", "require", "optional"] | None = ...,
        internet_service_database_cache: Literal["disable", "enable"] | None = ...,
        internet_service_app_ctrl_size: int | None = ...,
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
    "Settings",
    "SettingsPayload",
    "SettingsResponse",
    "SettingsObject",
]