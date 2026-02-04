""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/interface
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class InterfaceVrrpProxyarpItem(TypedDict, total=False):
    """Nested item for vrrp.proxy-arp field."""
    id: int
    ip: str


class InterfaceTaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class InterfaceIpv6ClientoptionsItem(TypedDict, total=False):
    """Nested item for ipv6.client-options field."""
    id: int
    code: int
    type: Literal["hex", "string", "ip6", "fqdn"]
    value: str
    ip6: str | list[str]


class InterfaceIpv6Ip6extraaddrItem(TypedDict, total=False):
    """Nested item for ipv6.ip6-extra-addr field."""
    prefix: str


class InterfaceIpv6Ip6routelistItem(TypedDict, total=False):
    """Nested item for ipv6.ip6-route-list field."""
    route: str
    route_pref: Literal["medium", "high", "low"]
    route_life_time: int


class InterfaceIpv6Ip6prefixlistItem(TypedDict, total=False):
    """Nested item for ipv6.ip6-prefix-list field."""
    prefix: str
    autonomous_flag: Literal["enable", "disable"]
    onlink_flag: Literal["enable", "disable"]
    valid_life_time: int
    preferred_life_time: int


class InterfaceIpv6Ip6rdnsslistItem(TypedDict, total=False):
    """Nested item for ipv6.ip6-rdnss-list field."""
    rdnss: str
    rdnss_life_time: int


class InterfaceIpv6Ip6dnssllistItem(TypedDict, total=False):
    """Nested item for ipv6.ip6-dnssl-list field."""
    domain: str
    dnssl_life_time: int


class InterfaceIpv6Ip6delegatedprefixlistItem(TypedDict, total=False):
    """Nested item for ipv6.ip6-delegated-prefix-list field."""
    prefix_id: int
    upstream_interface: str
    delegated_prefix_iaid: int
    autonomous_flag: Literal["enable", "disable"]
    onlink_flag: Literal["enable", "disable"]
    subnet: str
    rdnss_service: Literal["delegated", "default", "specify"]
    rdnss: str | list[str]
    dnssl_service: Literal["enable", "disable"]


class InterfaceIpv6Dhcp6iapdlistItem(TypedDict, total=False):
    """Nested item for ipv6.dhcp6-iapd-list field."""
    iaid: int
    prefix_hint: str
    prefix_hint_plt: int
    prefix_hint_vlt: int


class InterfaceIpv6Vrrp6Item(TypedDict, total=False):
    """Nested item for ipv6.vrrp6 field."""
    vrid: int
    vrgrp: int
    vrip6: str
    priority: int
    adv_interval: int
    start_time: int
    preempt: Literal["enable", "disable"]
    accept_mode: Literal["enable", "disable"]
    vrdst6: str | list[str]
    vrdst_priority: int
    ignore_default_route: Literal["enable", "disable"]
    status: Literal["enable", "disable"]


class InterfaceClientoptionsItem(TypedDict, total=False):
    """Nested item for client-options field."""
    id: int
    code: int
    type: Literal["hex", "string", "ip", "fqdn"]
    value: str
    ip: str | list[str]


class InterfaceFailalertinterfacesItem(TypedDict, total=False):
    """Nested item for fail-alert-interfaces field."""
    name: str


class InterfaceMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    interface_name: str


class InterfaceSecuritygroupsItem(TypedDict, total=False):
    """Nested item for security-groups field."""
    name: str


class InterfaceVrrpItem(TypedDict, total=False):
    """Nested item for vrrp field."""
    vrid: int
    version: Literal["2", "3"]
    vrgrp: int
    vrip: str
    priority: int
    adv_interval: int
    start_time: int
    preempt: Literal["enable", "disable"]
    accept_mode: Literal["enable", "disable"]
    vrdst: str | list[str]
    vrdst_priority: int
    ignore_default_route: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    proxy_arp: str | list[str] | list[InterfaceVrrpProxyarpItem]


class InterfacePhysettingDict(TypedDict, total=False):
    """Nested object type for phy-setting field."""
    signal_ok_threshold: int


class InterfaceSecondaryipItem(TypedDict, total=False):
    """Nested item for secondaryip field."""
    id: int
    ip: str
    secip_relay_ip: str | list[str]
    allowaccess: Literal["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "radius-acct", "probe-response", "fabric", "ftm", "speed-test", "scim"]
    gwdetect: Literal["enable", "disable"]
    ping_serv_status: int
    detectserver: str
    detectprotocol: Literal["ping", "tcp-echo", "udp-echo"]
    ha_priority: int


class InterfaceDhcpsnoopingserverlistItem(TypedDict, total=False):
    """Nested item for dhcp-snooping-server-list field."""
    name: str
    server_ip: str


class InterfaceTaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[InterfaceTaggingTagsItem]


class InterfaceIpv6Dict(TypedDict, total=False):
    """Nested object type for ipv6 field."""
    ip6_mode: Literal["static", "dhcp", "pppoe", "delegated"]
    client_options: str | list[str] | list[InterfaceIpv6ClientoptionsItem]
    nd_mode: Literal["basic", "SEND-compatible"]
    nd_cert: str
    nd_security_level: int
    nd_timestamp_delta: int
    nd_timestamp_fuzz: int
    nd_cga_modifier: str
    ip6_dns_server_override: Literal["enable", "disable"]
    ip6_address: str
    ip6_extra_addr: str | list[str] | list[InterfaceIpv6Ip6extraaddrItem]
    ip6_allowaccess: Literal["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "fabric", "scim", "probe-response"]
    ip6_send_adv: Literal["enable", "disable"]
    icmp6_send_redirect: Literal["enable", "disable"]
    ip6_manage_flag: Literal["enable", "disable"]
    ip6_other_flag: Literal["enable", "disable"]
    ip6_max_interval: int
    ip6_min_interval: int
    ip6_link_mtu: int
    ra_send_mtu: Literal["enable", "disable"]
    ip6_reachable_time: int
    ip6_retrans_time: int
    ip6_default_life: int
    ip6_hop_limit: int
    ip6_adv_rio: Literal["enable", "disable"]
    ip6_route_pref: Literal["medium", "high", "low"]
    ip6_route_list: str | list[str] | list[InterfaceIpv6Ip6routelistItem]
    autoconf: Literal["enable", "disable"]
    unique_autoconf_addr: Literal["enable", "disable"]
    interface_identifier: str
    ip6_prefix_mode: Literal["dhcp6", "ra"]
    ip6_delegated_prefix_iaid: int
    ip6_upstream_interface: str
    ip6_subnet: str
    ip6_prefix_list: str | list[str] | list[InterfaceIpv6Ip6prefixlistItem]
    ip6_rdnss_list: str | list[str] | list[InterfaceIpv6Ip6rdnsslistItem]
    ip6_dnssl_list: str | list[str] | list[InterfaceIpv6Ip6dnssllistItem]
    ip6_delegated_prefix_list: str | list[str] | list[InterfaceIpv6Ip6delegatedprefixlistItem]
    dhcp6_relay_service: Literal["disable", "enable"]
    dhcp6_relay_type: Literal["regular"]
    dhcp6_relay_source_interface: Literal["disable", "enable"]
    dhcp6_relay_ip: str | list[str]
    dhcp6_relay_source_ip: str
    dhcp6_relay_interface_id: str
    dhcp6_client_options: Literal["rapid", "iapd", "iana"]
    dhcp6_prefix_delegation: Literal["enable", "disable"]
    dhcp6_information_request: Literal["enable", "disable"]
    dhcp6_iapd_list: str | list[str] | list[InterfaceIpv6Dhcp6iapdlistItem]
    cli_conn6_status: int
    vrrp_virtual_mac6: Literal["enable", "disable"]
    vrip6_link_local: str
    vrrp6: str | list[str] | list[InterfaceIpv6Vrrp6Item]


class InterfacePayload(TypedDict, total=False):
    """Payload type for Interface operations."""
    name: str
    vdom: str
    vrf: int
    cli_conn_status: int
    fortilink: Literal["enable", "disable"]
    switch_controller_source_ip: Literal["outbound", "fixed"]
    mode: Literal["static", "dhcp", "pppoe"]
    client_options: str | list[str] | list[InterfaceClientoptionsItem]
    distance: int
    priority: int
    dhcp_relay_interface_select_method: Literal["auto", "sdwan", "specify"]
    dhcp_relay_interface: str
    dhcp_relay_vrf_select: int
    dhcp_broadcast_flag: Literal["disable", "enable"]
    dhcp_relay_service: Literal["disable", "enable"]
    dhcp_relay_ip: str | list[str]
    dhcp_relay_source_ip: str
    dhcp_relay_circuit_id: str
    dhcp_relay_link_selection: str
    dhcp_relay_request_all_server: Literal["disable", "enable"]
    dhcp_relay_allow_no_end_option: Literal["disable", "enable"]
    dhcp_relay_type: Literal["regular", "ipsec"]
    dhcp_smart_relay: Literal["disable", "enable"]
    dhcp_relay_agent_option: Literal["enable", "disable"]
    dhcp_classless_route_addition: Literal["enable", "disable"]
    management_ip: str
    ip: str
    allowaccess: str | list[str]
    gwdetect: Literal["enable", "disable"]
    ping_serv_status: int
    detectserver: str
    detectprotocol: str | list[str]
    ha_priority: int
    fail_detect: Literal["enable", "disable"]
    fail_detect_option: str | list[str]
    fail_alert_method: Literal["link-failed-signal", "link-down"]
    fail_action_on_extender: Literal["soft-restart", "hard-restart", "reboot"]
    fail_alert_interfaces: str | list[str] | list[InterfaceFailalertinterfacesItem]
    dhcp_client_identifier: str
    dhcp_renew_time: int
    ipunnumbered: str
    username: str
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]
    password: str
    idle_timeout: int
    multilink: Literal["enable", "disable"]
    mrru: int
    detected_peer_mtu: int
    disc_retry_timeout: int
    padt_retry_timeout: int
    service_name: str
    ac_name: str
    lcp_echo_interval: int
    lcp_max_echo_fails: int
    defaultgw: Literal["enable", "disable"]
    dns_server_override: Literal["enable", "disable"]
    dns_server_protocol: str | list[str]
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    pptp_client: Literal["enable", "disable"]
    pptp_user: str
    pptp_password: str
    pptp_server_ip: str
    pptp_auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    pptp_timeout: int
    arpforward: Literal["enable", "disable"]
    ndiscforward: Literal["enable", "disable"]
    broadcast_forward: Literal["enable", "disable"]
    bfd: Literal["global", "enable", "disable"]
    bfd_desired_min_tx: int
    bfd_detect_mult: int
    bfd_required_min_rx: int
    l2forward: Literal["enable", "disable"]
    icmp_send_redirect: Literal["enable", "disable"]
    icmp_accept_redirect: Literal["enable", "disable"]
    reachable_time: int
    vlanforward: Literal["enable", "disable"]
    stpforward: Literal["enable", "disable"]
    stpforward_mode: Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"]
    ips_sniffer_mode: Literal["enable", "disable"]
    ident_accept: Literal["enable", "disable"]
    ipmac: Literal["enable", "disable"]
    subst: Literal["enable", "disable"]
    macaddr: str
    virtual_mac: str
    substitute_dst_mac: str
    speed: Literal["auto", "10full", "10half", "100full", "100half", "100auto", "1000full", "1000auto"]
    status: Literal["up", "down"]
    netbios_forward: Literal["disable", "enable"]
    wins_ip: str
    type: Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "vdom-link", "loopback", "switch", "vap-switch", "wl-mesh", "fext-wan", "vxlan", "geneve", "switch-vlan", "emac-vlan", "lan-extension"]
    dedicated_to: Literal["none", "management"]
    trust_ip_1: str
    trust_ip_2: str
    trust_ip_3: str
    trust_ip6_1: str
    trust_ip6_2: str
    trust_ip6_3: str
    ring_rx: int
    ring_tx: int
    wccp: Literal["enable", "disable"]
    netflow_sampler: Literal["disable", "tx", "rx", "both"]
    netflow_sample_rate: int
    netflow_sampler_id: int
    sflow_sampler: Literal["enable", "disable"]
    drop_fragment: Literal["enable", "disable"]
    src_check: Literal["enable", "disable"]
    sample_rate: int
    polling_interval: int
    sample_direction: Literal["tx", "rx", "both"]
    explicit_web_proxy: Literal["enable", "disable"]
    explicit_ftp_proxy: Literal["enable", "disable"]
    proxy_captive_portal: Literal["enable", "disable"]
    tcp_mss: int
    inbandwidth: int
    outbandwidth: int
    egress_shaping_profile: str
    ingress_shaping_profile: str
    spillover_threshold: int
    ingress_spillover_threshold: int
    weight: int
    interface: str
    external: Literal["enable", "disable"]
    mtu_override: Literal["enable", "disable"]
    mtu: int
    vlan_protocol: Literal["8021q", "8021ad"]
    vlanid: int
    forward_domain: int
    remote_ip: str
    member: str | list[str] | list[InterfaceMemberItem]
    lacp_mode: Literal["static", "passive", "active"]
    lacp_ha_secondary: Literal["enable", "disable"]
    system_id_type: Literal["auto", "user"]
    system_id: str
    lacp_speed: Literal["slow", "fast"]
    min_links: int
    min_links_down: Literal["operational", "administrative"]
    algorithm: Literal["L2", "L3", "L4", "NPU-GRE", "Source-MAC"]
    link_up_delay: int
    aggregate_type: Literal["physical", "vxlan"]
    priority_override: Literal["enable", "disable"]
    aggregate: str
    redundant_interface: str
    devindex: int
    vindex: int
    switch: str
    description: str
    alias: str
    security_mode: Literal["none", "captive-portal", "802.1X"]
    security_mac_auth_bypass: Literal["mac-auth-only", "enable", "disable"]
    security_ip_auth_bypass: Literal["enable", "disable"]
    security_external_web: str
    security_external_logout: str
    replacemsg_override_group: str
    security_redirect_url: str
    auth_cert: str
    auth_portal_addr: str
    security_exempt_list: str
    security_groups: str | list[str] | list[InterfaceSecuritygroupsItem]
    ike_saml_server: str
    device_identification: Literal["enable", "disable"]
    exclude_signatures: str | list[str]
    device_user_identification: Literal["enable", "disable"]
    lldp_reception: Literal["enable", "disable", "vdom"]
    lldp_transmission: Literal["enable", "disable", "vdom"]
    lldp_network_policy: str
    estimated_upstream_bandwidth: int
    estimated_downstream_bandwidth: int
    measured_upstream_bandwidth: int
    measured_downstream_bandwidth: int
    bandwidth_measure_time: int
    monitor_bandwidth: Literal["enable", "disable"]
    vrrp_virtual_mac: Literal["enable", "disable"]
    vrrp: str | list[str] | list[InterfaceVrrpItem]
    phy_setting: InterfacePhysettingDict
    role: Literal["lan", "wan", "dmz", "undefined"]
    snmp_index: int
    secondary_IP: Literal["enable", "disable"]
    secondaryip: str | list[str] | list[InterfaceSecondaryipItem]
    preserve_session_route: Literal["enable", "disable"]
    auto_auth_extension_device: Literal["enable", "disable"]
    ap_discover: Literal["enable", "disable"]
    fortilink_neighbor_detect: Literal["lldp", "fortilink"]
    ip_managed_by_fortiipam: Literal["inherit-global", "enable", "disable"]
    managed_subnetwork_size: Literal["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216"]
    fortilink_split_interface: Literal["enable", "disable"]
    internal: int
    fortilink_backup_link: int
    switch_controller_access_vlan: Literal["enable", "disable"]
    switch_controller_traffic_policy: str
    switch_controller_rspan_mode: Literal["disable", "enable"]
    switch_controller_netflow_collect: Literal["disable", "enable"]
    switch_controller_mgmt_vlan: int
    switch_controller_igmp_snooping: Literal["enable", "disable"]
    switch_controller_igmp_snooping_proxy: Literal["enable", "disable"]
    switch_controller_igmp_snooping_fast_leave: Literal["enable", "disable"]
    switch_controller_dhcp_snooping: Literal["enable", "disable"]
    switch_controller_dhcp_snooping_verify_mac: Literal["enable", "disable"]
    switch_controller_dhcp_snooping_option82: Literal["enable", "disable"]
    dhcp_snooping_server_list: str | list[str] | list[InterfaceDhcpsnoopingserverlistItem]
    switch_controller_arp_inspection: Literal["enable", "disable", "monitor"]
    switch_controller_learning_limit: int
    switch_controller_nac: str
    switch_controller_dynamic: str
    switch_controller_feature: Literal["none", "default-vlan", "quarantine", "rspan", "voice", "video", "nac", "nac-segment"]
    switch_controller_iot_scanning: Literal["enable", "disable"]
    switch_controller_offload: Literal["enable", "disable"]
    switch_controller_offload_ip: str
    switch_controller_offload_gw: Literal["enable", "disable"]
    swc_vlan: int
    swc_first_create: int
    color: int
    tagging: str | list[str] | list[InterfaceTaggingItem]
    eap_supplicant: Literal["enable", "disable"]
    eap_method: Literal["tls", "peap"]
    eap_identity: str
    eap_password: str
    eap_ca_cert: str
    eap_user_cert: str
    default_purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    ipv6: InterfaceIpv6Dict
    physical: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InterfaceResponse(TypedDict, total=False):
    """Response type for Interface - use with .dict property for typed dict access."""
    name: str
    vdom: str
    vrf: int
    cli_conn_status: int
    fortilink: Literal["enable", "disable"]
    switch_controller_source_ip: Literal["outbound", "fixed"]
    mode: Literal["static", "dhcp", "pppoe"]
    client_options: list[InterfaceClientoptionsItem]
    distance: int
    priority: int
    dhcp_relay_interface_select_method: Literal["auto", "sdwan", "specify"]
    dhcp_relay_interface: str
    dhcp_relay_vrf_select: int
    dhcp_broadcast_flag: Literal["disable", "enable"]
    dhcp_relay_service: Literal["disable", "enable"]
    dhcp_relay_ip: str | list[str]
    dhcp_relay_source_ip: str
    dhcp_relay_circuit_id: str
    dhcp_relay_link_selection: str
    dhcp_relay_request_all_server: Literal["disable", "enable"]
    dhcp_relay_allow_no_end_option: Literal["disable", "enable"]
    dhcp_relay_type: Literal["regular", "ipsec"]
    dhcp_smart_relay: Literal["disable", "enable"]
    dhcp_relay_agent_option: Literal["enable", "disable"]
    dhcp_classless_route_addition: Literal["enable", "disable"]
    management_ip: str
    ip: str
    allowaccess: str
    gwdetect: Literal["enable", "disable"]
    ping_serv_status: int
    detectserver: str
    detectprotocol: str
    ha_priority: int
    fail_detect: Literal["enable", "disable"]
    fail_detect_option: str
    fail_alert_method: Literal["link-failed-signal", "link-down"]
    fail_action_on_extender: Literal["soft-restart", "hard-restart", "reboot"]
    fail_alert_interfaces: list[InterfaceFailalertinterfacesItem]
    dhcp_client_identifier: str
    dhcp_renew_time: int
    ipunnumbered: str
    username: str
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]
    password: str
    idle_timeout: int
    multilink: Literal["enable", "disable"]
    mrru: int
    detected_peer_mtu: int
    disc_retry_timeout: int
    padt_retry_timeout: int
    service_name: str
    ac_name: str
    lcp_echo_interval: int
    lcp_max_echo_fails: int
    defaultgw: Literal["enable", "disable"]
    dns_server_override: Literal["enable", "disable"]
    dns_server_protocol: str
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    pptp_client: Literal["enable", "disable"]
    pptp_user: str
    pptp_password: str
    pptp_server_ip: str
    pptp_auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    pptp_timeout: int
    arpforward: Literal["enable", "disable"]
    ndiscforward: Literal["enable", "disable"]
    broadcast_forward: Literal["enable", "disable"]
    bfd: Literal["global", "enable", "disable"]
    bfd_desired_min_tx: int
    bfd_detect_mult: int
    bfd_required_min_rx: int
    l2forward: Literal["enable", "disable"]
    icmp_send_redirect: Literal["enable", "disable"]
    icmp_accept_redirect: Literal["enable", "disable"]
    reachable_time: int
    vlanforward: Literal["enable", "disable"]
    stpforward: Literal["enable", "disable"]
    stpforward_mode: Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"]
    ips_sniffer_mode: Literal["enable", "disable"]
    ident_accept: Literal["enable", "disable"]
    ipmac: Literal["enable", "disable"]
    subst: Literal["enable", "disable"]
    macaddr: str
    virtual_mac: str
    substitute_dst_mac: str
    speed: Literal["auto", "10full", "10half", "100full", "100half", "100auto", "1000full", "1000auto"]
    status: Literal["up", "down"]
    netbios_forward: Literal["disable", "enable"]
    wins_ip: str
    type: Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "vdom-link", "loopback", "switch", "vap-switch", "wl-mesh", "fext-wan", "vxlan", "geneve", "switch-vlan", "emac-vlan", "lan-extension"]
    dedicated_to: Literal["none", "management"]
    trust_ip_1: str
    trust_ip_2: str
    trust_ip_3: str
    trust_ip6_1: str
    trust_ip6_2: str
    trust_ip6_3: str
    ring_rx: int
    ring_tx: int
    wccp: Literal["enable", "disable"]
    netflow_sampler: Literal["disable", "tx", "rx", "both"]
    netflow_sample_rate: int
    netflow_sampler_id: int
    sflow_sampler: Literal["enable", "disable"]
    drop_fragment: Literal["enable", "disable"]
    src_check: Literal["enable", "disable"]
    sample_rate: int
    polling_interval: int
    sample_direction: Literal["tx", "rx", "both"]
    explicit_web_proxy: Literal["enable", "disable"]
    explicit_ftp_proxy: Literal["enable", "disable"]
    proxy_captive_portal: Literal["enable", "disable"]
    tcp_mss: int
    inbandwidth: int
    outbandwidth: int
    egress_shaping_profile: str
    ingress_shaping_profile: str
    spillover_threshold: int
    ingress_spillover_threshold: int
    weight: int
    interface: str
    external: Literal["enable", "disable"]
    mtu_override: Literal["enable", "disable"]
    mtu: int
    vlan_protocol: Literal["8021q", "8021ad"]
    vlanid: int
    forward_domain: int
    remote_ip: str
    member: list[InterfaceMemberItem]
    lacp_mode: Literal["static", "passive", "active"]
    lacp_ha_secondary: Literal["enable", "disable"]
    system_id_type: Literal["auto", "user"]
    system_id: str
    lacp_speed: Literal["slow", "fast"]
    min_links: int
    min_links_down: Literal["operational", "administrative"]
    algorithm: Literal["L2", "L3", "L4", "NPU-GRE", "Source-MAC"]
    link_up_delay: int
    aggregate_type: Literal["physical", "vxlan"]
    priority_override: Literal["enable", "disable"]
    aggregate: str
    redundant_interface: str
    devindex: int
    vindex: int
    switch: str
    description: str
    alias: str
    security_mode: Literal["none", "captive-portal", "802.1X"]
    security_mac_auth_bypass: Literal["mac-auth-only", "enable", "disable"]
    security_ip_auth_bypass: Literal["enable", "disable"]
    security_external_web: str
    security_external_logout: str
    replacemsg_override_group: str
    security_redirect_url: str
    auth_cert: str
    auth_portal_addr: str
    security_exempt_list: str
    security_groups: list[InterfaceSecuritygroupsItem]
    ike_saml_server: str
    device_identification: Literal["enable", "disable"]
    exclude_signatures: str
    device_user_identification: Literal["enable", "disable"]
    lldp_reception: Literal["enable", "disable", "vdom"]
    lldp_transmission: Literal["enable", "disable", "vdom"]
    lldp_network_policy: str
    estimated_upstream_bandwidth: int
    estimated_downstream_bandwidth: int
    measured_upstream_bandwidth: int
    measured_downstream_bandwidth: int
    bandwidth_measure_time: int
    monitor_bandwidth: Literal["enable", "disable"]
    vrrp_virtual_mac: Literal["enable", "disable"]
    vrrp: list[InterfaceVrrpItem]
    phy_setting: InterfacePhysettingDict
    role: Literal["lan", "wan", "dmz", "undefined"]
    snmp_index: int
    secondary_IP: Literal["enable", "disable"]
    secondaryip: list[InterfaceSecondaryipItem]
    preserve_session_route: Literal["enable", "disable"]
    auto_auth_extension_device: Literal["enable", "disable"]
    ap_discover: Literal["enable", "disable"]
    fortilink_neighbor_detect: Literal["lldp", "fortilink"]
    ip_managed_by_fortiipam: Literal["inherit-global", "enable", "disable"]
    managed_subnetwork_size: Literal["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216"]
    fortilink_split_interface: Literal["enable", "disable"]
    internal: int
    fortilink_backup_link: int
    switch_controller_access_vlan: Literal["enable", "disable"]
    switch_controller_traffic_policy: str
    switch_controller_rspan_mode: Literal["disable", "enable"]
    switch_controller_netflow_collect: Literal["disable", "enable"]
    switch_controller_mgmt_vlan: int
    switch_controller_igmp_snooping: Literal["enable", "disable"]
    switch_controller_igmp_snooping_proxy: Literal["enable", "disable"]
    switch_controller_igmp_snooping_fast_leave: Literal["enable", "disable"]
    switch_controller_dhcp_snooping: Literal["enable", "disable"]
    switch_controller_dhcp_snooping_verify_mac: Literal["enable", "disable"]
    switch_controller_dhcp_snooping_option82: Literal["enable", "disable"]
    dhcp_snooping_server_list: list[InterfaceDhcpsnoopingserverlistItem]
    switch_controller_arp_inspection: Literal["enable", "disable", "monitor"]
    switch_controller_learning_limit: int
    switch_controller_nac: str
    switch_controller_dynamic: str
    switch_controller_feature: Literal["none", "default-vlan", "quarantine", "rspan", "voice", "video", "nac", "nac-segment"]
    switch_controller_iot_scanning: Literal["enable", "disable"]
    switch_controller_offload: Literal["enable", "disable"]
    switch_controller_offload_ip: str
    switch_controller_offload_gw: Literal["enable", "disable"]
    swc_vlan: int
    swc_first_create: int
    color: int
    tagging: list[InterfaceTaggingItem]
    eap_supplicant: Literal["enable", "disable"]
    eap_method: Literal["tls", "peap"]
    eap_identity: str
    eap_password: str
    eap_ca_cert: str
    eap_user_cert: str
    default_purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    ipv6: InterfaceIpv6Dict
    physical: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InterfaceVrrpProxyarpItemObject(FortiObject[InterfaceVrrpProxyarpItem]):
    """Typed object for vrrp.proxy-arp table items with attribute access."""
    id: int
    ip: str


class InterfaceTaggingTagsItemObject(FortiObject[InterfaceTaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class InterfaceClientoptionsItemObject(FortiObject[InterfaceClientoptionsItem]):
    """Typed object for client-options table items with attribute access."""
    id: int
    code: int
    type: Literal["hex", "string", "ip", "fqdn"]
    value: str
    ip: str | list[str]


class InterfaceFailalertinterfacesItemObject(FortiObject[InterfaceFailalertinterfacesItem]):
    """Typed object for fail-alert-interfaces table items with attribute access."""
    name: str


class InterfaceMemberItemObject(FortiObject[InterfaceMemberItem]):
    """Typed object for member table items with attribute access."""
    interface_name: str


class InterfaceSecuritygroupsItemObject(FortiObject[InterfaceSecuritygroupsItem]):
    """Typed object for security-groups table items with attribute access."""
    name: str


class InterfaceVrrpItemObject(FortiObject[InterfaceVrrpItem]):
    """Typed object for vrrp table items with attribute access."""
    vrid: int
    version: Literal["2", "3"]
    vrgrp: int
    vrip: str
    priority: int
    adv_interval: int
    start_time: int
    preempt: Literal["enable", "disable"]
    accept_mode: Literal["enable", "disable"]
    vrdst: str | list[str]
    vrdst_priority: int
    ignore_default_route: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    proxy_arp: FortiObjectList[InterfaceVrrpProxyarpItemObject]


class InterfaceSecondaryipItemObject(FortiObject[InterfaceSecondaryipItem]):
    """Typed object for secondaryip table items with attribute access."""
    id: int
    ip: str
    secip_relay_ip: str | list[str]
    allowaccess: Literal["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "radius-acct", "probe-response", "fabric", "ftm", "speed-test", "scim"]
    gwdetect: Literal["enable", "disable"]
    ping_serv_status: int
    detectserver: str
    detectprotocol: Literal["ping", "tcp-echo", "udp-echo"]
    ha_priority: int


class InterfaceDhcpsnoopingserverlistItemObject(FortiObject[InterfaceDhcpsnoopingserverlistItem]):
    """Typed object for dhcp-snooping-server-list table items with attribute access."""
    name: str
    server_ip: str


class InterfaceTaggingItemObject(FortiObject[InterfaceTaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[InterfaceTaggingTagsItemObject]


class InterfaceIpv6ClientoptionsItemObject(FortiObject[InterfaceIpv6ClientoptionsItem]):
    """Typed object for ipv6.client-options table items with attribute access."""
    id: int
    code: int
    type: Literal["hex", "string", "ip6", "fqdn"]
    value: str
    ip6: str | list[str]


class InterfaceIpv6Ip6extraaddrItemObject(FortiObject[InterfaceIpv6Ip6extraaddrItem]):
    """Typed object for ipv6.ip6-extra-addr table items with attribute access."""
    prefix: str


class InterfaceIpv6Ip6routelistItemObject(FortiObject[InterfaceIpv6Ip6routelistItem]):
    """Typed object for ipv6.ip6-route-list table items with attribute access."""
    route: str
    route_pref: Literal["medium", "high", "low"]
    route_life_time: int


class InterfaceIpv6Ip6prefixlistItemObject(FortiObject[InterfaceIpv6Ip6prefixlistItem]):
    """Typed object for ipv6.ip6-prefix-list table items with attribute access."""
    prefix: str
    autonomous_flag: Literal["enable", "disable"]
    onlink_flag: Literal["enable", "disable"]
    valid_life_time: int
    preferred_life_time: int


class InterfaceIpv6Ip6rdnsslistItemObject(FortiObject[InterfaceIpv6Ip6rdnsslistItem]):
    """Typed object for ipv6.ip6-rdnss-list table items with attribute access."""
    rdnss: str
    rdnss_life_time: int


class InterfaceIpv6Ip6dnssllistItemObject(FortiObject[InterfaceIpv6Ip6dnssllistItem]):
    """Typed object for ipv6.ip6-dnssl-list table items with attribute access."""
    domain: str
    dnssl_life_time: int


class InterfaceIpv6Ip6delegatedprefixlistItemObject(FortiObject[InterfaceIpv6Ip6delegatedprefixlistItem]):
    """Typed object for ipv6.ip6-delegated-prefix-list table items with attribute access."""
    prefix_id: int
    upstream_interface: str
    delegated_prefix_iaid: int
    autonomous_flag: Literal["enable", "disable"]
    onlink_flag: Literal["enable", "disable"]
    subnet: str
    rdnss_service: Literal["delegated", "default", "specify"]
    rdnss: str | list[str]
    dnssl_service: Literal["enable", "disable"]


class InterfaceIpv6Dhcp6iapdlistItemObject(FortiObject[InterfaceIpv6Dhcp6iapdlistItem]):
    """Typed object for ipv6.dhcp6-iapd-list table items with attribute access."""
    iaid: int
    prefix_hint: str
    prefix_hint_plt: int
    prefix_hint_vlt: int


class InterfaceIpv6Vrrp6ItemObject(FortiObject[InterfaceIpv6Vrrp6Item]):
    """Typed object for ipv6.vrrp6 table items with attribute access."""
    vrid: int
    vrgrp: int
    vrip6: str
    priority: int
    adv_interval: int
    start_time: int
    preempt: Literal["enable", "disable"]
    accept_mode: Literal["enable", "disable"]
    vrdst6: str | list[str]
    vrdst_priority: int
    ignore_default_route: Literal["enable", "disable"]
    status: Literal["enable", "disable"]


class InterfacePhysettingObject(FortiObject):
    """Nested object for phy-setting field with attribute access."""
    signal_ok_threshold: int


class InterfaceIpv6Object(FortiObject):
    """Nested object for ipv6 field with attribute access."""
    ip6_mode: Literal["static", "dhcp", "pppoe", "delegated"]
    client_options: str | list[str]
    nd_mode: Literal["basic", "SEND-compatible"]
    nd_cert: str
    nd_security_level: int
    nd_timestamp_delta: int
    nd_timestamp_fuzz: int
    nd_cga_modifier: str
    ip6_dns_server_override: Literal["enable", "disable"]
    ip6_address: str
    ip6_extra_addr: str | list[str]
    ip6_allowaccess: Literal["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "fabric", "scim", "probe-response"]
    ip6_send_adv: Literal["enable", "disable"]
    icmp6_send_redirect: Literal["enable", "disable"]
    ip6_manage_flag: Literal["enable", "disable"]
    ip6_other_flag: Literal["enable", "disable"]
    ip6_max_interval: int
    ip6_min_interval: int
    ip6_link_mtu: int
    ra_send_mtu: Literal["enable", "disable"]
    ip6_reachable_time: int
    ip6_retrans_time: int
    ip6_default_life: int
    ip6_hop_limit: int
    ip6_adv_rio: Literal["enable", "disable"]
    ip6_route_pref: Literal["medium", "high", "low"]
    ip6_route_list: str | list[str]
    autoconf: Literal["enable", "disable"]
    unique_autoconf_addr: Literal["enable", "disable"]
    interface_identifier: str
    ip6_prefix_mode: Literal["dhcp6", "ra"]
    ip6_delegated_prefix_iaid: int
    ip6_upstream_interface: str
    ip6_subnet: str
    ip6_prefix_list: str | list[str]
    ip6_rdnss_list: str | list[str]
    ip6_dnssl_list: str | list[str]
    ip6_delegated_prefix_list: str | list[str]
    dhcp6_relay_service: Literal["disable", "enable"]
    dhcp6_relay_type: Literal["regular"]
    dhcp6_relay_source_interface: Literal["disable", "enable"]
    dhcp6_relay_ip: str | list[str]
    dhcp6_relay_source_ip: str
    dhcp6_relay_interface_id: str
    dhcp6_client_options: Literal["rapid", "iapd", "iana"]
    dhcp6_prefix_delegation: Literal["enable", "disable"]
    dhcp6_information_request: Literal["enable", "disable"]
    dhcp6_iapd_list: str | list[str]
    cli_conn6_status: int
    vrrp_virtual_mac6: Literal["enable", "disable"]
    vrip6_link_local: str
    vrrp6: str | list[str]


class InterfaceObject(FortiObject):
    """Typed FortiObject for Interface with field access."""
    name: str
    vrf: int
    cli_conn_status: int
    fortilink: Literal["enable", "disable"]
    switch_controller_source_ip: Literal["outbound", "fixed"]
    mode: Literal["static", "dhcp", "pppoe"]
    client_options: FortiObjectList[InterfaceClientoptionsItemObject]
    distance: int
    priority: int
    dhcp_relay_interface_select_method: Literal["auto", "sdwan", "specify"]
    dhcp_relay_interface: str
    dhcp_relay_vrf_select: int
    dhcp_broadcast_flag: Literal["disable", "enable"]
    dhcp_relay_service: Literal["disable", "enable"]
    dhcp_relay_ip: str | list[str]
    dhcp_relay_source_ip: str
    dhcp_relay_circuit_id: str
    dhcp_relay_link_selection: str
    dhcp_relay_request_all_server: Literal["disable", "enable"]
    dhcp_relay_allow_no_end_option: Literal["disable", "enable"]
    dhcp_relay_type: Literal["regular", "ipsec"]
    dhcp_smart_relay: Literal["disable", "enable"]
    dhcp_relay_agent_option: Literal["enable", "disable"]
    dhcp_classless_route_addition: Literal["enable", "disable"]
    management_ip: str
    ip: str
    allowaccess: str
    gwdetect: Literal["enable", "disable"]
    ping_serv_status: int
    detectserver: str
    detectprotocol: str
    ha_priority: int
    fail_detect: Literal["enable", "disable"]
    fail_detect_option: str
    fail_alert_method: Literal["link-failed-signal", "link-down"]
    fail_action_on_extender: Literal["soft-restart", "hard-restart", "reboot"]
    fail_alert_interfaces: FortiObjectList[InterfaceFailalertinterfacesItemObject]
    dhcp_client_identifier: str
    dhcp_renew_time: int
    ipunnumbered: str
    username: str
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]
    password: str
    idle_timeout: int
    multilink: Literal["enable", "disable"]
    mrru: int
    detected_peer_mtu: int
    disc_retry_timeout: int
    padt_retry_timeout: int
    service_name: str
    ac_name: str
    lcp_echo_interval: int
    lcp_max_echo_fails: int
    defaultgw: Literal["enable", "disable"]
    dns_server_override: Literal["enable", "disable"]
    dns_server_protocol: str
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    pptp_client: Literal["enable", "disable"]
    pptp_user: str
    pptp_password: str
    pptp_server_ip: str
    pptp_auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    pptp_timeout: int
    arpforward: Literal["enable", "disable"]
    ndiscforward: Literal["enable", "disable"]
    broadcast_forward: Literal["enable", "disable"]
    bfd: Literal["global", "enable", "disable"]
    bfd_desired_min_tx: int
    bfd_detect_mult: int
    bfd_required_min_rx: int
    l2forward: Literal["enable", "disable"]
    icmp_send_redirect: Literal["enable", "disable"]
    icmp_accept_redirect: Literal["enable", "disable"]
    reachable_time: int
    vlanforward: Literal["enable", "disable"]
    stpforward: Literal["enable", "disable"]
    stpforward_mode: Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"]
    ips_sniffer_mode: Literal["enable", "disable"]
    ident_accept: Literal["enable", "disable"]
    ipmac: Literal["enable", "disable"]
    subst: Literal["enable", "disable"]
    macaddr: str
    virtual_mac: str
    substitute_dst_mac: str
    speed: Literal["auto", "10full", "10half", "100full", "100half", "100auto", "1000full", "1000auto"]
    status: Literal["up", "down"]
    netbios_forward: Literal["disable", "enable"]
    wins_ip: str
    type: Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "vdom-link", "loopback", "switch", "vap-switch", "wl-mesh", "fext-wan", "vxlan", "geneve", "switch-vlan", "emac-vlan", "lan-extension"]
    dedicated_to: Literal["none", "management"]
    trust_ip_1: str
    trust_ip_2: str
    trust_ip_3: str
    trust_ip6_1: str
    trust_ip6_2: str
    trust_ip6_3: str
    ring_rx: int
    ring_tx: int
    wccp: Literal["enable", "disable"]
    netflow_sampler: Literal["disable", "tx", "rx", "both"]
    netflow_sample_rate: int
    netflow_sampler_id: int
    sflow_sampler: Literal["enable", "disable"]
    drop_fragment: Literal["enable", "disable"]
    src_check: Literal["enable", "disable"]
    sample_rate: int
    polling_interval: int
    sample_direction: Literal["tx", "rx", "both"]
    explicit_web_proxy: Literal["enable", "disable"]
    explicit_ftp_proxy: Literal["enable", "disable"]
    proxy_captive_portal: Literal["enable", "disable"]
    tcp_mss: int
    inbandwidth: int
    outbandwidth: int
    egress_shaping_profile: str
    ingress_shaping_profile: str
    spillover_threshold: int
    ingress_spillover_threshold: int
    weight: int
    interface: str
    external: Literal["enable", "disable"]
    mtu_override: Literal["enable", "disable"]
    mtu: int
    vlan_protocol: Literal["8021q", "8021ad"]
    vlanid: int
    forward_domain: int
    remote_ip: str
    member: FortiObjectList[InterfaceMemberItemObject]
    lacp_mode: Literal["static", "passive", "active"]
    lacp_ha_secondary: Literal["enable", "disable"]
    system_id_type: Literal["auto", "user"]
    system_id: str
    lacp_speed: Literal["slow", "fast"]
    min_links: int
    min_links_down: Literal["operational", "administrative"]
    algorithm: Literal["L2", "L3", "L4", "NPU-GRE", "Source-MAC"]
    link_up_delay: int
    aggregate_type: Literal["physical", "vxlan"]
    priority_override: Literal["enable", "disable"]
    aggregate: str
    redundant_interface: str
    devindex: int
    vindex: int
    switch: str
    description: str
    alias: str
    security_mode: Literal["none", "captive-portal", "802.1X"]
    security_mac_auth_bypass: Literal["mac-auth-only", "enable", "disable"]
    security_ip_auth_bypass: Literal["enable", "disable"]
    security_external_web: str
    security_external_logout: str
    replacemsg_override_group: str
    security_redirect_url: str
    auth_cert: str
    auth_portal_addr: str
    security_exempt_list: str
    security_groups: FortiObjectList[InterfaceSecuritygroupsItemObject]
    ike_saml_server: str
    device_identification: Literal["enable", "disable"]
    exclude_signatures: str
    device_user_identification: Literal["enable", "disable"]
    lldp_reception: Literal["enable", "disable", "vdom"]
    lldp_transmission: Literal["enable", "disable", "vdom"]
    lldp_network_policy: str
    estimated_upstream_bandwidth: int
    estimated_downstream_bandwidth: int
    measured_upstream_bandwidth: int
    measured_downstream_bandwidth: int
    bandwidth_measure_time: int
    monitor_bandwidth: Literal["enable", "disable"]
    vrrp_virtual_mac: Literal["enable", "disable"]
    vrrp: FortiObjectList[InterfaceVrrpItemObject]
    phy_setting: InterfacePhysettingObject
    role: Literal["lan", "wan", "dmz", "undefined"]
    snmp_index: int
    secondary_IP: Literal["enable", "disable"]
    secondaryip: FortiObjectList[InterfaceSecondaryipItemObject]
    preserve_session_route: Literal["enable", "disable"]
    auto_auth_extension_device: Literal["enable", "disable"]
    ap_discover: Literal["enable", "disable"]
    fortilink_neighbor_detect: Literal["lldp", "fortilink"]
    ip_managed_by_fortiipam: Literal["inherit-global", "enable", "disable"]
    managed_subnetwork_size: Literal["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216"]
    fortilink_split_interface: Literal["enable", "disable"]
    internal: int
    fortilink_backup_link: int
    switch_controller_access_vlan: Literal["enable", "disable"]
    switch_controller_traffic_policy: str
    switch_controller_rspan_mode: Literal["disable", "enable"]
    switch_controller_netflow_collect: Literal["disable", "enable"]
    switch_controller_mgmt_vlan: int
    switch_controller_igmp_snooping: Literal["enable", "disable"]
    switch_controller_igmp_snooping_proxy: Literal["enable", "disable"]
    switch_controller_igmp_snooping_fast_leave: Literal["enable", "disable"]
    switch_controller_dhcp_snooping: Literal["enable", "disable"]
    switch_controller_dhcp_snooping_verify_mac: Literal["enable", "disable"]
    switch_controller_dhcp_snooping_option82: Literal["enable", "disable"]
    dhcp_snooping_server_list: FortiObjectList[InterfaceDhcpsnoopingserverlistItemObject]
    switch_controller_arp_inspection: Literal["enable", "disable", "monitor"]
    switch_controller_learning_limit: int
    switch_controller_nac: str
    switch_controller_dynamic: str
    switch_controller_feature: Literal["none", "default-vlan", "quarantine", "rspan", "voice", "video", "nac", "nac-segment"]
    switch_controller_iot_scanning: Literal["enable", "disable"]
    switch_controller_offload: Literal["enable", "disable"]
    switch_controller_offload_ip: str
    switch_controller_offload_gw: Literal["enable", "disable"]
    swc_vlan: int
    swc_first_create: int
    color: int
    tagging: FortiObjectList[InterfaceTaggingItemObject]
    eap_supplicant: Literal["enable", "disable"]
    eap_method: Literal["tls", "peap"]
    eap_identity: str
    eap_password: str
    eap_ca_cert: str
    eap_user_cert: str
    default_purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    ipv6: InterfaceIpv6Object
    physical: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Interface:
    """
    
    Endpoint: system/interface
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
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
    ) -> InterfaceObject: ...
    
    @overload
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
    ) -> FortiObjectList[InterfaceObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: InterfacePayload | None = ...,
        name: str | None = ...,
        vrf: int | None = ...,
        cli_conn_status: int | None = ...,
        fortilink: Literal["enable", "disable"] | None = ...,
        switch_controller_source_ip: Literal["outbound", "fixed"] | None = ...,
        mode: Literal["static", "dhcp", "pppoe"] | None = ...,
        client_options: str | list[str] | list[InterfaceClientoptionsItem] | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
        dhcp_relay_interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        dhcp_relay_interface: str | None = ...,
        dhcp_relay_vrf_select: int | None = ...,
        dhcp_broadcast_flag: Literal["disable", "enable"] | None = ...,
        dhcp_relay_service: Literal["disable", "enable"] | None = ...,
        dhcp_relay_ip: str | list[str] | None = ...,
        dhcp_relay_source_ip: str | None = ...,
        dhcp_relay_circuit_id: str | None = ...,
        dhcp_relay_link_selection: str | None = ...,
        dhcp_relay_request_all_server: Literal["disable", "enable"] | None = ...,
        dhcp_relay_allow_no_end_option: Literal["disable", "enable"] | None = ...,
        dhcp_relay_type: Literal["regular", "ipsec"] | None = ...,
        dhcp_smart_relay: Literal["disable", "enable"] | None = ...,
        dhcp_relay_agent_option: Literal["enable", "disable"] | None = ...,
        dhcp_classless_route_addition: Literal["enable", "disable"] | None = ...,
        management_ip: str | None = ...,
        ip: str | None = ...,
        allowaccess: str | list[str] | None = ...,
        gwdetect: Literal["enable", "disable"] | None = ...,
        ping_serv_status: int | None = ...,
        detectserver: str | None = ...,
        detectprotocol: str | list[str] | None = ...,
        ha_priority: int | None = ...,
        fail_detect: Literal["enable", "disable"] | None = ...,
        fail_detect_option: str | list[str] | None = ...,
        fail_alert_method: Literal["link-failed-signal", "link-down"] | None = ...,
        fail_action_on_extender: Literal["soft-restart", "hard-restart", "reboot"] | None = ...,
        fail_alert_interfaces: str | list[str] | list[InterfaceFailalertinterfacesItem] | None = ...,
        dhcp_client_identifier: str | None = ...,
        dhcp_renew_time: int | None = ...,
        ipunnumbered: str | None = ...,
        username: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        detected_peer_mtu: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        defaultgw: Literal["enable", "disable"] | None = ...,
        dns_server_override: Literal["enable", "disable"] | None = ...,
        dns_server_protocol: str | list[str] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        pptp_client: Literal["enable", "disable"] | None = ...,
        pptp_user: str | None = ...,
        pptp_password: str | None = ...,
        pptp_server_ip: str | None = ...,
        pptp_auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        pptp_timeout: int | None = ...,
        arpforward: Literal["enable", "disable"] | None = ...,
        ndiscforward: Literal["enable", "disable"] | None = ...,
        broadcast_forward: Literal["enable", "disable"] | None = ...,
        bfd: Literal["global", "enable", "disable"] | None = ...,
        bfd_desired_min_tx: int | None = ...,
        bfd_detect_mult: int | None = ...,
        bfd_required_min_rx: int | None = ...,
        l2forward: Literal["enable", "disable"] | None = ...,
        icmp_send_redirect: Literal["enable", "disable"] | None = ...,
        icmp_accept_redirect: Literal["enable", "disable"] | None = ...,
        reachable_time: int | None = ...,
        vlanforward: Literal["enable", "disable"] | None = ...,
        stpforward: Literal["enable", "disable"] | None = ...,
        stpforward_mode: Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"] | None = ...,
        ips_sniffer_mode: Literal["enable", "disable"] | None = ...,
        ident_accept: Literal["enable", "disable"] | None = ...,
        ipmac: Literal["enable", "disable"] | None = ...,
        subst: Literal["enable", "disable"] | None = ...,
        macaddr: str | None = ...,
        virtual_mac: str | None = ...,
        substitute_dst_mac: str | None = ...,
        speed: Literal["auto", "10full", "10half", "100full", "100half", "100auto", "1000full", "1000auto"] | None = ...,
        status: Literal["up", "down"] | None = ...,
        netbios_forward: Literal["disable", "enable"] | None = ...,
        wins_ip: str | None = ...,
        type: Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "vdom-link", "loopback", "switch", "vap-switch", "wl-mesh", "fext-wan", "vxlan", "geneve", "switch-vlan", "emac-vlan", "lan-extension"] | None = ...,
        dedicated_to: Literal["none", "management"] | None = ...,
        trust_ip_1: str | None = ...,
        trust_ip_2: str | None = ...,
        trust_ip_3: str | None = ...,
        trust_ip6_1: str | None = ...,
        trust_ip6_2: str | None = ...,
        trust_ip6_3: str | None = ...,
        ring_rx: int | None = ...,
        ring_tx: int | None = ...,
        wccp: Literal["enable", "disable"] | None = ...,
        netflow_sampler: Literal["disable", "tx", "rx", "both"] | None = ...,
        netflow_sample_rate: int | None = ...,
        netflow_sampler_id: int | None = ...,
        sflow_sampler: Literal["enable", "disable"] | None = ...,
        drop_fragment: Literal["enable", "disable"] | None = ...,
        src_check: Literal["enable", "disable"] | None = ...,
        sample_rate: int | None = ...,
        polling_interval: int | None = ...,
        sample_direction: Literal["tx", "rx", "both"] | None = ...,
        explicit_web_proxy: Literal["enable", "disable"] | None = ...,
        explicit_ftp_proxy: Literal["enable", "disable"] | None = ...,
        proxy_captive_portal: Literal["enable", "disable"] | None = ...,
        tcp_mss: int | None = ...,
        inbandwidth: int | None = ...,
        outbandwidth: int | None = ...,
        egress_shaping_profile: str | None = ...,
        ingress_shaping_profile: str | None = ...,
        spillover_threshold: int | None = ...,
        ingress_spillover_threshold: int | None = ...,
        weight: int | None = ...,
        interface: str | None = ...,
        external: Literal["enable", "disable"] | None = ...,
        mtu_override: Literal["enable", "disable"] | None = ...,
        mtu: int | None = ...,
        vlan_protocol: Literal["8021q", "8021ad"] | None = ...,
        vlanid: int | None = ...,
        forward_domain: int | None = ...,
        remote_ip: str | None = ...,
        member: str | list[str] | list[InterfaceMemberItem] | None = ...,
        lacp_mode: Literal["static", "passive", "active"] | None = ...,
        lacp_ha_secondary: Literal["enable", "disable"] | None = ...,
        system_id_type: Literal["auto", "user"] | None = ...,
        system_id: str | None = ...,
        lacp_speed: Literal["slow", "fast"] | None = ...,
        min_links: int | None = ...,
        min_links_down: Literal["operational", "administrative"] | None = ...,
        algorithm: Literal["L2", "L3", "L4", "NPU-GRE", "Source-MAC"] | None = ...,
        link_up_delay: int | None = ...,
        aggregate_type: Literal["physical", "vxlan"] | None = ...,
        priority_override: Literal["enable", "disable"] | None = ...,
        aggregate: str | None = ...,
        redundant_interface: str | None = ...,
        devindex: int | None = ...,
        vindex: int | None = ...,
        switch: str | None = ...,
        description: str | None = ...,
        alias: str | None = ...,
        security_mode: Literal["none", "captive-portal", "802.1X"] | None = ...,
        security_mac_auth_bypass: Literal["mac-auth-only", "enable", "disable"] | None = ...,
        security_ip_auth_bypass: Literal["enable", "disable"] | None = ...,
        security_external_web: str | None = ...,
        security_external_logout: str | None = ...,
        replacemsg_override_group: str | None = ...,
        security_redirect_url: str | None = ...,
        auth_cert: str | None = ...,
        auth_portal_addr: str | None = ...,
        security_exempt_list: str | None = ...,
        security_groups: str | list[str] | list[InterfaceSecuritygroupsItem] | None = ...,
        ike_saml_server: str | None = ...,
        device_identification: Literal["enable", "disable"] | None = ...,
        exclude_signatures: str | list[str] | None = ...,
        device_user_identification: Literal["enable", "disable"] | None = ...,
        lldp_reception: Literal["enable", "disable", "vdom"] | None = ...,
        lldp_transmission: Literal["enable", "disable", "vdom"] | None = ...,
        lldp_network_policy: str | None = ...,
        estimated_upstream_bandwidth: int | None = ...,
        estimated_downstream_bandwidth: int | None = ...,
        measured_upstream_bandwidth: int | None = ...,
        measured_downstream_bandwidth: int | None = ...,
        bandwidth_measure_time: int | None = ...,
        monitor_bandwidth: Literal["enable", "disable"] | None = ...,
        vrrp_virtual_mac: Literal["enable", "disable"] | None = ...,
        vrrp: str | list[str] | list[InterfaceVrrpItem] | None = ...,
        phy_setting: InterfacePhysettingDict | None = ...,
        role: Literal["lan", "wan", "dmz", "undefined"] | None = ...,
        snmp_index: int | None = ...,
        secondary_IP: Literal["enable", "disable"] | None = ...,
        secondaryip: str | list[str] | list[InterfaceSecondaryipItem] | None = ...,
        preserve_session_route: Literal["enable", "disable"] | None = ...,
        auto_auth_extension_device: Literal["enable", "disable"] | None = ...,
        ap_discover: Literal["enable", "disable"] | None = ...,
        fortilink_neighbor_detect: Literal["lldp", "fortilink"] | None = ...,
        ip_managed_by_fortiipam: Literal["inherit-global", "enable", "disable"] | None = ...,
        managed_subnetwork_size: Literal["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216"] | None = ...,
        fortilink_split_interface: Literal["enable", "disable"] | None = ...,
        internal: int | None = ...,
        fortilink_backup_link: int | None = ...,
        switch_controller_access_vlan: Literal["enable", "disable"] | None = ...,
        switch_controller_traffic_policy: str | None = ...,
        switch_controller_rspan_mode: Literal["disable", "enable"] | None = ...,
        switch_controller_netflow_collect: Literal["disable", "enable"] | None = ...,
        switch_controller_mgmt_vlan: int | None = ...,
        switch_controller_igmp_snooping: Literal["enable", "disable"] | None = ...,
        switch_controller_igmp_snooping_proxy: Literal["enable", "disable"] | None = ...,
        switch_controller_igmp_snooping_fast_leave: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping_verify_mac: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping_option82: Literal["enable", "disable"] | None = ...,
        dhcp_snooping_server_list: str | list[str] | list[InterfaceDhcpsnoopingserverlistItem] | None = ...,
        switch_controller_arp_inspection: Literal["enable", "disable", "monitor"] | None = ...,
        switch_controller_learning_limit: int | None = ...,
        switch_controller_nac: str | None = ...,
        switch_controller_dynamic: str | None = ...,
        switch_controller_feature: Literal["none", "default-vlan", "quarantine", "rspan", "voice", "video", "nac", "nac-segment"] | None = ...,
        switch_controller_iot_scanning: Literal["enable", "disable"] | None = ...,
        switch_controller_offload: Literal["enable", "disable"] | None = ...,
        switch_controller_offload_ip: str | None = ...,
        switch_controller_offload_gw: Literal["enable", "disable"] | None = ...,
        swc_vlan: int | None = ...,
        swc_first_create: int | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[InterfaceTaggingItem] | None = ...,
        eap_supplicant: Literal["enable", "disable"] | None = ...,
        eap_method: Literal["tls", "peap"] | None = ...,
        eap_identity: str | None = ...,
        eap_password: str | None = ...,
        eap_ca_cert: str | None = ...,
        eap_user_cert: str | None = ...,
        default_purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        ipv6: InterfaceIpv6Dict | None = ...,
        physical: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InterfacePayload | None = ...,
        name: str | None = ...,
        vrf: int | None = ...,
        cli_conn_status: int | None = ...,
        fortilink: Literal["enable", "disable"] | None = ...,
        switch_controller_source_ip: Literal["outbound", "fixed"] | None = ...,
        mode: Literal["static", "dhcp", "pppoe"] | None = ...,
        client_options: str | list[str] | list[InterfaceClientoptionsItem] | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
        dhcp_relay_interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        dhcp_relay_interface: str | None = ...,
        dhcp_relay_vrf_select: int | None = ...,
        dhcp_broadcast_flag: Literal["disable", "enable"] | None = ...,
        dhcp_relay_service: Literal["disable", "enable"] | None = ...,
        dhcp_relay_ip: str | list[str] | None = ...,
        dhcp_relay_source_ip: str | None = ...,
        dhcp_relay_circuit_id: str | None = ...,
        dhcp_relay_link_selection: str | None = ...,
        dhcp_relay_request_all_server: Literal["disable", "enable"] | None = ...,
        dhcp_relay_allow_no_end_option: Literal["disable", "enable"] | None = ...,
        dhcp_relay_type: Literal["regular", "ipsec"] | None = ...,
        dhcp_smart_relay: Literal["disable", "enable"] | None = ...,
        dhcp_relay_agent_option: Literal["enable", "disable"] | None = ...,
        dhcp_classless_route_addition: Literal["enable", "disable"] | None = ...,
        management_ip: str | None = ...,
        ip: str | None = ...,
        allowaccess: str | list[str] | None = ...,
        gwdetect: Literal["enable", "disable"] | None = ...,
        ping_serv_status: int | None = ...,
        detectserver: str | None = ...,
        detectprotocol: str | list[str] | None = ...,
        ha_priority: int | None = ...,
        fail_detect: Literal["enable", "disable"] | None = ...,
        fail_detect_option: str | list[str] | None = ...,
        fail_alert_method: Literal["link-failed-signal", "link-down"] | None = ...,
        fail_action_on_extender: Literal["soft-restart", "hard-restart", "reboot"] | None = ...,
        fail_alert_interfaces: str | list[str] | list[InterfaceFailalertinterfacesItem] | None = ...,
        dhcp_client_identifier: str | None = ...,
        dhcp_renew_time: int | None = ...,
        ipunnumbered: str | None = ...,
        username: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        detected_peer_mtu: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        defaultgw: Literal["enable", "disable"] | None = ...,
        dns_server_override: Literal["enable", "disable"] | None = ...,
        dns_server_protocol: str | list[str] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        pptp_client: Literal["enable", "disable"] | None = ...,
        pptp_user: str | None = ...,
        pptp_password: str | None = ...,
        pptp_server_ip: str | None = ...,
        pptp_auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        pptp_timeout: int | None = ...,
        arpforward: Literal["enable", "disable"] | None = ...,
        ndiscforward: Literal["enable", "disable"] | None = ...,
        broadcast_forward: Literal["enable", "disable"] | None = ...,
        bfd: Literal["global", "enable", "disable"] | None = ...,
        bfd_desired_min_tx: int | None = ...,
        bfd_detect_mult: int | None = ...,
        bfd_required_min_rx: int | None = ...,
        l2forward: Literal["enable", "disable"] | None = ...,
        icmp_send_redirect: Literal["enable", "disable"] | None = ...,
        icmp_accept_redirect: Literal["enable", "disable"] | None = ...,
        reachable_time: int | None = ...,
        vlanforward: Literal["enable", "disable"] | None = ...,
        stpforward: Literal["enable", "disable"] | None = ...,
        stpforward_mode: Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"] | None = ...,
        ips_sniffer_mode: Literal["enable", "disable"] | None = ...,
        ident_accept: Literal["enable", "disable"] | None = ...,
        ipmac: Literal["enable", "disable"] | None = ...,
        subst: Literal["enable", "disable"] | None = ...,
        macaddr: str | None = ...,
        virtual_mac: str | None = ...,
        substitute_dst_mac: str | None = ...,
        speed: Literal["auto", "10full", "10half", "100full", "100half", "100auto", "1000full", "1000auto"] | None = ...,
        status: Literal["up", "down"] | None = ...,
        netbios_forward: Literal["disable", "enable"] | None = ...,
        wins_ip: str | None = ...,
        type: Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "vdom-link", "loopback", "switch", "vap-switch", "wl-mesh", "fext-wan", "vxlan", "geneve", "switch-vlan", "emac-vlan", "lan-extension"] | None = ...,
        dedicated_to: Literal["none", "management"] | None = ...,
        trust_ip_1: str | None = ...,
        trust_ip_2: str | None = ...,
        trust_ip_3: str | None = ...,
        trust_ip6_1: str | None = ...,
        trust_ip6_2: str | None = ...,
        trust_ip6_3: str | None = ...,
        ring_rx: int | None = ...,
        ring_tx: int | None = ...,
        wccp: Literal["enable", "disable"] | None = ...,
        netflow_sampler: Literal["disable", "tx", "rx", "both"] | None = ...,
        netflow_sample_rate: int | None = ...,
        netflow_sampler_id: int | None = ...,
        sflow_sampler: Literal["enable", "disable"] | None = ...,
        drop_fragment: Literal["enable", "disable"] | None = ...,
        src_check: Literal["enable", "disable"] | None = ...,
        sample_rate: int | None = ...,
        polling_interval: int | None = ...,
        sample_direction: Literal["tx", "rx", "both"] | None = ...,
        explicit_web_proxy: Literal["enable", "disable"] | None = ...,
        explicit_ftp_proxy: Literal["enable", "disable"] | None = ...,
        proxy_captive_portal: Literal["enable", "disable"] | None = ...,
        tcp_mss: int | None = ...,
        inbandwidth: int | None = ...,
        outbandwidth: int | None = ...,
        egress_shaping_profile: str | None = ...,
        ingress_shaping_profile: str | None = ...,
        spillover_threshold: int | None = ...,
        ingress_spillover_threshold: int | None = ...,
        weight: int | None = ...,
        interface: str | None = ...,
        external: Literal["enable", "disable"] | None = ...,
        mtu_override: Literal["enable", "disable"] | None = ...,
        mtu: int | None = ...,
        vlan_protocol: Literal["8021q", "8021ad"] | None = ...,
        vlanid: int | None = ...,
        forward_domain: int | None = ...,
        remote_ip: str | None = ...,
        member: str | list[str] | list[InterfaceMemberItem] | None = ...,
        lacp_mode: Literal["static", "passive", "active"] | None = ...,
        lacp_ha_secondary: Literal["enable", "disable"] | None = ...,
        system_id_type: Literal["auto", "user"] | None = ...,
        system_id: str | None = ...,
        lacp_speed: Literal["slow", "fast"] | None = ...,
        min_links: int | None = ...,
        min_links_down: Literal["operational", "administrative"] | None = ...,
        algorithm: Literal["L2", "L3", "L4", "NPU-GRE", "Source-MAC"] | None = ...,
        link_up_delay: int | None = ...,
        aggregate_type: Literal["physical", "vxlan"] | None = ...,
        priority_override: Literal["enable", "disable"] | None = ...,
        aggregate: str | None = ...,
        redundant_interface: str | None = ...,
        devindex: int | None = ...,
        vindex: int | None = ...,
        switch: str | None = ...,
        description: str | None = ...,
        alias: str | None = ...,
        security_mode: Literal["none", "captive-portal", "802.1X"] | None = ...,
        security_mac_auth_bypass: Literal["mac-auth-only", "enable", "disable"] | None = ...,
        security_ip_auth_bypass: Literal["enable", "disable"] | None = ...,
        security_external_web: str | None = ...,
        security_external_logout: str | None = ...,
        replacemsg_override_group: str | None = ...,
        security_redirect_url: str | None = ...,
        auth_cert: str | None = ...,
        auth_portal_addr: str | None = ...,
        security_exempt_list: str | None = ...,
        security_groups: str | list[str] | list[InterfaceSecuritygroupsItem] | None = ...,
        ike_saml_server: str | None = ...,
        device_identification: Literal["enable", "disable"] | None = ...,
        exclude_signatures: str | list[str] | None = ...,
        device_user_identification: Literal["enable", "disable"] | None = ...,
        lldp_reception: Literal["enable", "disable", "vdom"] | None = ...,
        lldp_transmission: Literal["enable", "disable", "vdom"] | None = ...,
        lldp_network_policy: str | None = ...,
        estimated_upstream_bandwidth: int | None = ...,
        estimated_downstream_bandwidth: int | None = ...,
        measured_upstream_bandwidth: int | None = ...,
        measured_downstream_bandwidth: int | None = ...,
        bandwidth_measure_time: int | None = ...,
        monitor_bandwidth: Literal["enable", "disable"] | None = ...,
        vrrp_virtual_mac: Literal["enable", "disable"] | None = ...,
        vrrp: str | list[str] | list[InterfaceVrrpItem] | None = ...,
        phy_setting: InterfacePhysettingDict | None = ...,
        role: Literal["lan", "wan", "dmz", "undefined"] | None = ...,
        snmp_index: int | None = ...,
        secondary_IP: Literal["enable", "disable"] | None = ...,
        secondaryip: str | list[str] | list[InterfaceSecondaryipItem] | None = ...,
        preserve_session_route: Literal["enable", "disable"] | None = ...,
        auto_auth_extension_device: Literal["enable", "disable"] | None = ...,
        ap_discover: Literal["enable", "disable"] | None = ...,
        fortilink_neighbor_detect: Literal["lldp", "fortilink"] | None = ...,
        ip_managed_by_fortiipam: Literal["inherit-global", "enable", "disable"] | None = ...,
        managed_subnetwork_size: Literal["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216"] | None = ...,
        fortilink_split_interface: Literal["enable", "disable"] | None = ...,
        internal: int | None = ...,
        fortilink_backup_link: int | None = ...,
        switch_controller_access_vlan: Literal["enable", "disable"] | None = ...,
        switch_controller_traffic_policy: str | None = ...,
        switch_controller_rspan_mode: Literal["disable", "enable"] | None = ...,
        switch_controller_netflow_collect: Literal["disable", "enable"] | None = ...,
        switch_controller_mgmt_vlan: int | None = ...,
        switch_controller_igmp_snooping: Literal["enable", "disable"] | None = ...,
        switch_controller_igmp_snooping_proxy: Literal["enable", "disable"] | None = ...,
        switch_controller_igmp_snooping_fast_leave: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping_verify_mac: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping_option82: Literal["enable", "disable"] | None = ...,
        dhcp_snooping_server_list: str | list[str] | list[InterfaceDhcpsnoopingserverlistItem] | None = ...,
        switch_controller_arp_inspection: Literal["enable", "disable", "monitor"] | None = ...,
        switch_controller_learning_limit: int | None = ...,
        switch_controller_nac: str | None = ...,
        switch_controller_dynamic: str | None = ...,
        switch_controller_feature: Literal["none", "default-vlan", "quarantine", "rspan", "voice", "video", "nac", "nac-segment"] | None = ...,
        switch_controller_iot_scanning: Literal["enable", "disable"] | None = ...,
        switch_controller_offload: Literal["enable", "disable"] | None = ...,
        switch_controller_offload_ip: str | None = ...,
        switch_controller_offload_gw: Literal["enable", "disable"] | None = ...,
        swc_vlan: int | None = ...,
        swc_first_create: int | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[InterfaceTaggingItem] | None = ...,
        eap_supplicant: Literal["enable", "disable"] | None = ...,
        eap_method: Literal["tls", "peap"] | None = ...,
        eap_identity: str | None = ...,
        eap_password: str | None = ...,
        eap_ca_cert: str | None = ...,
        eap_user_cert: str | None = ...,
        default_purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        ipv6: InterfaceIpv6Dict | None = ...,
        physical: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

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
        payload_dict: InterfacePayload | None = ...,
        name: str | None = ...,
        vrf: int | None = ...,
        cli_conn_status: int | None = ...,
        fortilink: Literal["enable", "disable"] | None = ...,
        switch_controller_source_ip: Literal["outbound", "fixed"] | None = ...,
        mode: Literal["static", "dhcp", "pppoe"] | None = ...,
        client_options: str | list[str] | list[InterfaceClientoptionsItem] | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
        dhcp_relay_interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        dhcp_relay_interface: str | None = ...,
        dhcp_relay_vrf_select: int | None = ...,
        dhcp_broadcast_flag: Literal["disable", "enable"] | None = ...,
        dhcp_relay_service: Literal["disable", "enable"] | None = ...,
        dhcp_relay_ip: str | list[str] | None = ...,
        dhcp_relay_source_ip: str | None = ...,
        dhcp_relay_circuit_id: str | None = ...,
        dhcp_relay_link_selection: str | None = ...,
        dhcp_relay_request_all_server: Literal["disable", "enable"] | None = ...,
        dhcp_relay_allow_no_end_option: Literal["disable", "enable"] | None = ...,
        dhcp_relay_type: Literal["regular", "ipsec"] | None = ...,
        dhcp_smart_relay: Literal["disable", "enable"] | None = ...,
        dhcp_relay_agent_option: Literal["enable", "disable"] | None = ...,
        dhcp_classless_route_addition: Literal["enable", "disable"] | None = ...,
        management_ip: str | None = ...,
        ip: str | None = ...,
        allowaccess: Literal["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "radius-acct", "probe-response", "fabric", "ftm", "speed-test", "scim"] | list[str] | None = ...,
        gwdetect: Literal["enable", "disable"] | None = ...,
        ping_serv_status: int | None = ...,
        detectserver: str | None = ...,
        detectprotocol: Literal["ping", "tcp-echo", "udp-echo"] | list[str] | None = ...,
        ha_priority: int | None = ...,
        fail_detect: Literal["enable", "disable"] | None = ...,
        fail_detect_option: Literal["detectserver", "link-down"] | list[str] | None = ...,
        fail_alert_method: Literal["link-failed-signal", "link-down"] | None = ...,
        fail_action_on_extender: Literal["soft-restart", "hard-restart", "reboot"] | None = ...,
        fail_alert_interfaces: str | list[str] | list[InterfaceFailalertinterfacesItem] | None = ...,
        dhcp_client_identifier: str | None = ...,
        dhcp_renew_time: int | None = ...,
        ipunnumbered: str | None = ...,
        username: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        detected_peer_mtu: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        defaultgw: Literal["enable", "disable"] | None = ...,
        dns_server_override: Literal["enable", "disable"] | None = ...,
        dns_server_protocol: Literal["cleartext", "dot", "doh"] | list[str] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        pptp_client: Literal["enable", "disable"] | None = ...,
        pptp_user: str | None = ...,
        pptp_password: str | None = ...,
        pptp_server_ip: str | None = ...,
        pptp_auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        pptp_timeout: int | None = ...,
        arpforward: Literal["enable", "disable"] | None = ...,
        ndiscforward: Literal["enable", "disable"] | None = ...,
        broadcast_forward: Literal["enable", "disable"] | None = ...,
        bfd: Literal["global", "enable", "disable"] | None = ...,
        bfd_desired_min_tx: int | None = ...,
        bfd_detect_mult: int | None = ...,
        bfd_required_min_rx: int | None = ...,
        l2forward: Literal["enable", "disable"] | None = ...,
        icmp_send_redirect: Literal["enable", "disable"] | None = ...,
        icmp_accept_redirect: Literal["enable", "disable"] | None = ...,
        reachable_time: int | None = ...,
        vlanforward: Literal["enable", "disable"] | None = ...,
        stpforward: Literal["enable", "disable"] | None = ...,
        stpforward_mode: Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"] | None = ...,
        ips_sniffer_mode: Literal["enable", "disable"] | None = ...,
        ident_accept: Literal["enable", "disable"] | None = ...,
        ipmac: Literal["enable", "disable"] | None = ...,
        subst: Literal["enable", "disable"] | None = ...,
        macaddr: str | None = ...,
        virtual_mac: str | None = ...,
        substitute_dst_mac: str | None = ...,
        speed: Literal["auto", "10full", "10half", "100full", "100half", "100auto", "1000full", "1000auto"] | None = ...,
        status: Literal["up", "down"] | None = ...,
        netbios_forward: Literal["disable", "enable"] | None = ...,
        wins_ip: str | None = ...,
        type: Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "vdom-link", "loopback", "switch", "vap-switch", "wl-mesh", "fext-wan", "vxlan", "geneve", "switch-vlan", "emac-vlan", "lan-extension"] | None = ...,
        dedicated_to: Literal["none", "management"] | None = ...,
        trust_ip_1: str | None = ...,
        trust_ip_2: str | None = ...,
        trust_ip_3: str | None = ...,
        trust_ip6_1: str | None = ...,
        trust_ip6_2: str | None = ...,
        trust_ip6_3: str | None = ...,
        ring_rx: int | None = ...,
        ring_tx: int | None = ...,
        wccp: Literal["enable", "disable"] | None = ...,
        netflow_sampler: Literal["disable", "tx", "rx", "both"] | None = ...,
        netflow_sample_rate: int | None = ...,
        netflow_sampler_id: int | None = ...,
        sflow_sampler: Literal["enable", "disable"] | None = ...,
        drop_fragment: Literal["enable", "disable"] | None = ...,
        src_check: Literal["enable", "disable"] | None = ...,
        sample_rate: int | None = ...,
        polling_interval: int | None = ...,
        sample_direction: Literal["tx", "rx", "both"] | None = ...,
        explicit_web_proxy: Literal["enable", "disable"] | None = ...,
        explicit_ftp_proxy: Literal["enable", "disable"] | None = ...,
        proxy_captive_portal: Literal["enable", "disable"] | None = ...,
        tcp_mss: int | None = ...,
        inbandwidth: int | None = ...,
        outbandwidth: int | None = ...,
        egress_shaping_profile: str | None = ...,
        ingress_shaping_profile: str | None = ...,
        spillover_threshold: int | None = ...,
        ingress_spillover_threshold: int | None = ...,
        weight: int | None = ...,
        interface: str | None = ...,
        external: Literal["enable", "disable"] | None = ...,
        mtu_override: Literal["enable", "disable"] | None = ...,
        mtu: int | None = ...,
        vlan_protocol: Literal["8021q", "8021ad"] | None = ...,
        vlanid: int | None = ...,
        forward_domain: int | None = ...,
        remote_ip: str | None = ...,
        member: str | list[str] | list[InterfaceMemberItem] | None = ...,
        lacp_mode: Literal["static", "passive", "active"] | None = ...,
        lacp_ha_secondary: Literal["enable", "disable"] | None = ...,
        system_id_type: Literal["auto", "user"] | None = ...,
        system_id: str | None = ...,
        lacp_speed: Literal["slow", "fast"] | None = ...,
        min_links: int | None = ...,
        min_links_down: Literal["operational", "administrative"] | None = ...,
        algorithm: Literal["L2", "L3", "L4", "NPU-GRE", "Source-MAC"] | None = ...,
        link_up_delay: int | None = ...,
        aggregate_type: Literal["physical", "vxlan"] | None = ...,
        priority_override: Literal["enable", "disable"] | None = ...,
        aggregate: str | None = ...,
        redundant_interface: str | None = ...,
        devindex: int | None = ...,
        vindex: int | None = ...,
        switch: str | None = ...,
        description: str | None = ...,
        alias: str | None = ...,
        security_mode: Literal["none", "captive-portal", "802.1X"] | None = ...,
        security_mac_auth_bypass: Literal["mac-auth-only", "enable", "disable"] | None = ...,
        security_ip_auth_bypass: Literal["enable", "disable"] | None = ...,
        security_external_web: str | None = ...,
        security_external_logout: str | None = ...,
        replacemsg_override_group: str | None = ...,
        security_redirect_url: str | None = ...,
        auth_cert: str | None = ...,
        auth_portal_addr: str | None = ...,
        security_exempt_list: str | None = ...,
        security_groups: str | list[str] | list[InterfaceSecuritygroupsItem] | None = ...,
        ike_saml_server: str | None = ...,
        device_identification: Literal["enable", "disable"] | None = ...,
        exclude_signatures: Literal["iot", "ot"] | list[str] | None = ...,
        device_user_identification: Literal["enable", "disable"] | None = ...,
        lldp_reception: Literal["enable", "disable", "vdom"] | None = ...,
        lldp_transmission: Literal["enable", "disable", "vdom"] | None = ...,
        lldp_network_policy: str | None = ...,
        estimated_upstream_bandwidth: int | None = ...,
        estimated_downstream_bandwidth: int | None = ...,
        measured_upstream_bandwidth: int | None = ...,
        measured_downstream_bandwidth: int | None = ...,
        bandwidth_measure_time: int | None = ...,
        monitor_bandwidth: Literal["enable", "disable"] | None = ...,
        vrrp_virtual_mac: Literal["enable", "disable"] | None = ...,
        vrrp: str | list[str] | list[InterfaceVrrpItem] | None = ...,
        phy_setting: InterfacePhysettingDict | None = ...,
        role: Literal["lan", "wan", "dmz", "undefined"] | None = ...,
        snmp_index: int | None = ...,
        secondary_IP: Literal["enable", "disable"] | None = ...,
        secondaryip: str | list[str] | list[InterfaceSecondaryipItem] | None = ...,
        preserve_session_route: Literal["enable", "disable"] | None = ...,
        auto_auth_extension_device: Literal["enable", "disable"] | None = ...,
        ap_discover: Literal["enable", "disable"] | None = ...,
        fortilink_neighbor_detect: Literal["lldp", "fortilink"] | None = ...,
        ip_managed_by_fortiipam: Literal["inherit-global", "enable", "disable"] | None = ...,
        managed_subnetwork_size: Literal["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216"] | None = ...,
        fortilink_split_interface: Literal["enable", "disable"] | None = ...,
        internal: int | None = ...,
        fortilink_backup_link: int | None = ...,
        switch_controller_access_vlan: Literal["enable", "disable"] | None = ...,
        switch_controller_traffic_policy: str | None = ...,
        switch_controller_rspan_mode: Literal["disable", "enable"] | None = ...,
        switch_controller_netflow_collect: Literal["disable", "enable"] | None = ...,
        switch_controller_mgmt_vlan: int | None = ...,
        switch_controller_igmp_snooping: Literal["enable", "disable"] | None = ...,
        switch_controller_igmp_snooping_proxy: Literal["enable", "disable"] | None = ...,
        switch_controller_igmp_snooping_fast_leave: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping_verify_mac: Literal["enable", "disable"] | None = ...,
        switch_controller_dhcp_snooping_option82: Literal["enable", "disable"] | None = ...,
        dhcp_snooping_server_list: str | list[str] | list[InterfaceDhcpsnoopingserverlistItem] | None = ...,
        switch_controller_arp_inspection: Literal["enable", "disable", "monitor"] | None = ...,
        switch_controller_learning_limit: int | None = ...,
        switch_controller_nac: str | None = ...,
        switch_controller_dynamic: str | None = ...,
        switch_controller_feature: Literal["none", "default-vlan", "quarantine", "rspan", "voice", "video", "nac", "nac-segment"] | None = ...,
        switch_controller_iot_scanning: Literal["enable", "disable"] | None = ...,
        switch_controller_offload: Literal["enable", "disable"] | None = ...,
        switch_controller_offload_ip: str | None = ...,
        switch_controller_offload_gw: Literal["enable", "disable"] | None = ...,
        swc_vlan: int | None = ...,
        swc_first_create: int | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[InterfaceTaggingItem] | None = ...,
        eap_supplicant: Literal["enable", "disable"] | None = ...,
        eap_method: Literal["tls", "peap"] | None = ...,
        eap_identity: str | None = ...,
        eap_password: str | None = ...,
        eap_ca_cert: str | None = ...,
        eap_user_cert: str | None = ...,
        default_purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        ipv6: InterfaceIpv6Dict | None = ...,
        physical: str | None = ...,
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
    "Interface",
    "InterfacePayload",
    "InterfaceResponse",
    "InterfaceObject",
]