""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/managed_switch
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

class ManagedSwitchPortsAllowedvlansItem(TypedDict, total=False):
    """Nested item for ports.allowed-vlans field."""
    vlan_name: str


class ManagedSwitchPortsUntaggedvlansItem(TypedDict, total=False):
    """Nested item for ports.untagged-vlans field."""
    vlan_name: str


class ManagedSwitchPortsAclgroupItem(TypedDict, total=False):
    """Nested item for ports.acl-group field."""
    name: str


class ManagedSwitchPortsFortiswitchaclsItem(TypedDict, total=False):
    """Nested item for ports.fortiswitch-acls field."""
    id: int


class ManagedSwitchPortsDhcpsnoopoption82overrideItem(TypedDict, total=False):
    """Nested item for ports.dhcp-snoop-option82-override field."""
    vlan_name: str
    circuit_id: str
    remote_id: str


class ManagedSwitchPortsInterfacetagsItem(TypedDict, total=False):
    """Nested item for ports.interface-tags field."""
    tag_name: str


class ManagedSwitchPortsMembersItem(TypedDict, total=False):
    """Nested item for ports.members field."""
    member_name: str


class ManagedSwitchIpsourceguardBindingentryItem(TypedDict, total=False):
    """Nested item for ip-source-guard.binding-entry field."""
    entry_name: str
    ip: str
    mac: str


class ManagedSwitchSnmpcommunityHostsItem(TypedDict, total=False):
    """Nested item for snmp-community.hosts field."""
    id: int
    ip: str


class ManagedSwitchMirrorSrcingressItem(TypedDict, total=False):
    """Nested item for mirror.src-ingress field."""
    name: str


class ManagedSwitchMirrorSrcegressItem(TypedDict, total=False):
    """Nested item for mirror.src-egress field."""
    name: str


class ManagedSwitchSystemdhcpserverIprangeItem(TypedDict, total=False):
    """Nested item for system-dhcp-server.ip-range field."""
    id: int
    start_ip: str
    end_ip: str


class ManagedSwitchSystemdhcpserverOptionsItem(TypedDict, total=False):
    """Nested item for system-dhcp-server.options field."""
    id: int
    code: int
    type: Literal["hex", "string", "ip", "fqdn"]
    value: str
    ip: str | list[str]


class ManagedSwitchIgmpsnoopingVlansItem(TypedDict, total=False):
    """Nested item for igmp-snooping.vlans field."""
    vlan_name: str
    proxy: Literal["disable", "enable", "global"]
    querier: Literal["disable", "enable"]
    querier_addr: str
    version: int


class ManagedSwitchRouteoffloadrouterItem(TypedDict, total=False):
    """Nested item for route-offload-router field."""
    vlan_name: str
    router_ip: str


class ManagedSwitchVlanItem(TypedDict, total=False):
    """Nested item for vlan field."""
    vlan_name: str
    assignment_priority: int


class ManagedSwitchPortsItem(TypedDict, total=False):
    """Nested item for ports field."""
    port_name: str
    port_owner: str
    switch_id: str
    speed: Literal["10half", "10full", "100half", "100full", "1000full", "10000full", "auto", "1000auto", "1000full-fiber", "40000full", "auto-module", "100FX-half", "100FX-full", "100000full", "2500auto", "2500full", "25000full", "50000full", "10000cr", "10000sr", "100000sr4", "100000cr4", "40000sr4", "40000cr4", "40000auto", "25000cr", "25000sr", "50000cr", "50000sr", "5000auto", "sgmii-auto"]
    status: Literal["up", "down"]
    poe_status: Literal["enable", "disable"]
    ip_source_guard: Literal["disable", "enable"]
    ptp_status: Literal["disable", "enable"]
    ptp_policy: str
    aggregator_mode: Literal["bandwidth", "count"]
    flapguard: Literal["enable", "disable"]
    flap_rate: int
    flap_duration: int
    flap_timeout: int
    rpvst_port: Literal["disabled", "enabled"]
    poe_pre_standard_detection: Literal["enable", "disable"]
    port_number: int
    port_prefix_type: int
    fortilink_port: int
    poe_capable: int
    pd_capable: int
    stacking_port: int
    p2p_port: int
    mclag_icl_port: int
    authenticated_port: int
    restricted_auth_port: int
    encrypted_port: int
    fiber_port: int
    media_type: str
    poe_standard: str
    poe_max_power: str
    poe_mode_bt_cabable: int
    poe_port_mode: Literal["ieee802-3af", "ieee802-3at", "ieee802-3bt"]
    poe_port_priority: Literal["critical-priority", "high-priority", "low-priority", "medium-priority"]
    poe_port_power: Literal["normal", "perpetual", "perpetual-fast"]
    flags: int
    isl_local_trunk_name: str
    isl_peer_port_name: str
    isl_peer_device_name: str
    isl_peer_device_sn: str
    fgt_peer_port_name: str
    fgt_peer_device_name: str
    vlan: str
    allowed_vlans_all: Literal["enable", "disable"]
    allowed_vlans: str | list[str] | list[ManagedSwitchPortsAllowedvlansItem]
    untagged_vlans: str | list[str] | list[ManagedSwitchPortsUntaggedvlansItem]
    type: Literal["physical", "trunk"]
    access_mode: Literal["dynamic", "nac", "static"]
    matched_dpp_policy: str
    matched_dpp_intf_tags: str
    acl_group: str | list[str] | list[ManagedSwitchPortsAclgroupItem]
    fortiswitch_acls: str | list[str] | list[ManagedSwitchPortsFortiswitchaclsItem]
    dhcp_snooping: Literal["untrusted", "trusted"]
    dhcp_snoop_option82_trust: Literal["enable", "disable"]
    dhcp_snoop_option82_override: str | list[str] | list[ManagedSwitchPortsDhcpsnoopoption82overrideItem]
    arp_inspection_trust: Literal["untrusted", "trusted"]
    igmp_snooping_flood_reports: Literal["enable", "disable"]
    mcast_snooping_flood_traffic: Literal["enable", "disable"]
    stp_state: Literal["enabled", "disabled"]
    stp_root_guard: Literal["enabled", "disabled"]
    stp_bpdu_guard: Literal["enabled", "disabled"]
    stp_bpdu_guard_timeout: int
    edge_port: Literal["enable", "disable"]
    discard_mode: Literal["none", "all-untagged", "all-tagged"]
    packet_sampler: Literal["enabled", "disabled"]
    packet_sample_rate: int
    sflow_counter_interval: int
    sample_direction: Literal["tx", "rx", "both"]
    fec_capable: int
    fec_state: Literal["disabled", "cl74", "cl91", "detect-by-module"]
    flow_control: Literal["disable", "tx", "rx", "both"]
    pause_meter: int
    pause_meter_resume: Literal["75%", "50%", "25%"]
    loop_guard: Literal["enabled", "disabled"]
    loop_guard_timeout: int
    port_policy: str
    qos_policy: str
    storm_control_policy: str
    port_security_policy: str
    export_to_pool: str
    interface_tags: str | list[str] | list[ManagedSwitchPortsInterfacetagsItem]
    learning_limit: int
    sticky_mac: Literal["enable", "disable"]
    lldp_status: Literal["disable", "rx-only", "tx-only", "tx-rx"]
    lldp_profile: str
    export_to: str
    mac_addr: str
    allow_arp_monitor: Literal["disable", "enable"]
    qnq: str
    log_mac_event: Literal["disable", "enable"]
    port_selection_criteria: Literal["src-mac", "dst-mac", "src-dst-mac", "src-ip", "dst-ip", "src-dst-ip"]
    description: str
    lacp_speed: Literal["slow", "fast"]
    mode: Literal["static", "lacp-passive", "lacp-active"]
    bundle: Literal["enable", "disable"]
    member_withdrawal_behavior: Literal["forward", "block"]
    mclag: Literal["enable", "disable"]
    min_bundle: int
    max_bundle: int
    members: str | list[str] | list[ManagedSwitchPortsMembersItem]
    fallback_port: str


class ManagedSwitchIpsourceguardItem(TypedDict, total=False):
    """Nested item for ip-source-guard field."""
    port: str
    description: str
    binding_entry: str | list[str] | list[ManagedSwitchIpsourceguardBindingentryItem]


class ManagedSwitchStpsettingsDict(TypedDict, total=False):
    """Nested object type for stp-settings field."""
    local_override: Literal["enable", "disable"]
    name: str
    revision: int
    hello_time: int
    forward_time: int
    max_age: int
    max_hops: int
    pending_timer: int


class ManagedSwitchStpinstanceItem(TypedDict, total=False):
    """Nested item for stp-instance field."""
    id: str
    priority: Literal["0", "4096", "8192", "12288", "16384", "20480", "24576", "28672", "32768", "36864", "40960", "45056", "49152", "53248", "57344", "61440"]


class ManagedSwitchSnmpsysinfoDict(TypedDict, total=False):
    """Nested object type for snmp-sysinfo field."""
    status: Literal["disable", "enable"]
    engine_id: str
    description: str
    contact_info: str
    location: str


class ManagedSwitchSnmptrapthresholdDict(TypedDict, total=False):
    """Nested object type for snmp-trap-threshold field."""
    trap_high_cpu_threshold: int
    trap_low_memory_threshold: int
    trap_log_full_threshold: int


class ManagedSwitchSnmpcommunityItem(TypedDict, total=False):
    """Nested item for snmp-community field."""
    id: int
    name: str
    status: Literal["disable", "enable"]
    hosts: str | list[str] | list[ManagedSwitchSnmpcommunityHostsItem]
    query_v1_status: Literal["disable", "enable"]
    query_v1_port: int
    query_v2c_status: Literal["disable", "enable"]
    query_v2c_port: int
    trap_v1_status: Literal["disable", "enable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["disable", "enable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"]


class ManagedSwitchSnmpuserItem(TypedDict, total=False):
    """Nested item for snmp-user field."""
    name: str
    queries: Literal["disable", "enable"]
    query_port: int
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
    auth_proto: Literal["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
    auth_pwd: str
    priv_proto: Literal["aes128", "aes192", "aes192c", "aes256", "aes256c", "des"]
    priv_pwd: str


class ManagedSwitchSwitchlogDict(TypedDict, total=False):
    """Nested object type for switch-log field."""
    local_override: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


class ManagedSwitchRemotelogItem(TypedDict, total=False):
    """Nested item for remote-log field."""
    name: str
    status: Literal["enable", "disable"]
    server: str
    port: int
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    csv: Literal["enable", "disable"]
    facility: Literal["kernel", "user", "mail", "daemon", "auth", "syslog", "lpr", "news", "uucp", "cron", "authpriv", "ftp", "ntp", "audit", "alert", "clock", "local0", "local1", "local2", "local3", "local4", "local5", "local6", "local7"]


class ManagedSwitchStormcontrolDict(TypedDict, total=False):
    """Nested object type for storm-control field."""
    local_override: Literal["enable", "disable"]
    rate: int
    burst_size_level: int
    unknown_unicast: Literal["enable", "disable"]
    unknown_multicast: Literal["enable", "disable"]
    broadcast: Literal["enable", "disable"]


class ManagedSwitchMirrorItem(TypedDict, total=False):
    """Nested item for mirror field."""
    name: str
    status: Literal["active", "inactive"]
    switching_packet: Literal["enable", "disable"]
    dst: str
    src_ingress: str | list[str] | list[ManagedSwitchMirrorSrcingressItem]
    src_egress: str | list[str] | list[ManagedSwitchMirrorSrcegressItem]


class ManagedSwitchStaticmacItem(TypedDict, total=False):
    """Nested item for static-mac field."""
    id: int
    type: Literal["static", "sticky"]
    vlan: str
    mac: str
    interface: str
    description: str


class ManagedSwitchCustomcommandItem(TypedDict, total=False):
    """Nested item for custom-command field."""
    command_entry: str
    command_name: str


class ManagedSwitchDhcpsnoopingstaticclientItem(TypedDict, total=False):
    """Nested item for dhcp-snooping-static-client field."""
    name: str
    vlan: str
    ip: str
    mac: str
    port: str


class ManagedSwitchIgmpsnoopingDict(TypedDict, total=False):
    """Nested object type for igmp-snooping field."""
    local_override: Literal["enable", "disable"]
    aging_time: int
    flood_unknown_multicast: Literal["enable", "disable"]
    vlans: str | list[str] | list[ManagedSwitchIgmpsnoopingVlansItem]


class ManagedSwitchX8021xsettingsDict(TypedDict, total=False):
    """Nested object type for 802-1X-settings field."""
    local_override: Literal["enable", "disable"]
    link_down_auth: Literal["set-unauth", "no-action"]
    reauth_period: int
    max_reauth_attempt: int
    tx_period: int
    mab_reauth: Literal["disable", "enable"]
    mac_username_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_password_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_calling_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_called_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_case: Literal["lowercase", "uppercase"]


class ManagedSwitchRoutervrfItem(TypedDict, total=False):
    """Nested item for router-vrf field."""
    name: str
    switch_id: str
    vrfid: int


class ManagedSwitchSysteminterfaceItem(TypedDict, total=False):
    """Nested item for system-interface field."""
    name: str
    switch_id: str
    mode: Literal["static", "dhcp"]
    ip: str
    status: Literal["disable", "enable"]
    allowaccess: Literal["ping", "https", "http", "ssh", "snmp", "telnet", "radius-acct"]
    vlan: str
    type: Literal["vlan", "physical"]
    interface: str
    vrf: str


class ManagedSwitchRouterstaticItem(TypedDict, total=False):
    """Nested item for router-static field."""
    id: int
    switch_id: str
    blackhole: Literal["disable", "enable"]
    comment: str
    device: str
    distance: int
    dst: str
    dynamic_gateway: Literal["disable", "enable"]
    gateway: str
    status: Literal["disable", "enable"]
    vrf: str


class ManagedSwitchSystemdhcpserverItem(TypedDict, total=False):
    """Nested item for system-dhcp-server field."""
    id: int
    switch_id: str
    status: Literal["disable", "enable"]
    lease_time: int
    dns_service: Literal["local", "default", "specify"]
    dns_server1: str
    dns_server2: str
    dns_server3: str
    ntp_service: Literal["local", "default", "specify"]
    ntp_server1: str
    ntp_server2: str
    ntp_server3: str
    default_gateway: str
    netmask: str
    interface: str
    ip_range: str | list[str] | list[ManagedSwitchSystemdhcpserverIprangeItem]
    options: str | list[str] | list[ManagedSwitchSystemdhcpserverOptionsItem]


class ManagedSwitchPayload(TypedDict, total=False):
    """Payload type for ManagedSwitch operations."""
    switch_id: str
    sn: str
    description: str
    switch_profile: str
    access_profile: str
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    fsw_wan1_peer: str
    fsw_wan1_admin: Literal["discovered", "disable", "enable"]
    poe_pre_standard_detection: Literal["enable", "disable"]
    dhcp_server_access_list: Literal["global", "enable", "disable"]
    poe_detection_type: int
    max_poe_budget: int
    directly_connected: int
    version: int
    max_allowed_trunk_members: int
    pre_provisioned: int
    l3_discovered: int
    mgmt_mode: int
    tunnel_discovered: int
    tdr_supported: str
    dynamic_capability: str
    switch_device_tag: str
    switch_dhcp_opt43_key: str
    mclag_igmp_snooping_aware: Literal["enable", "disable"]
    dynamically_discovered: int
    ptp_status: Literal["disable", "enable"]
    ptp_profile: str
    radius_nas_ip_override: Literal["disable", "enable"]
    radius_nas_ip: str
    route_offload: Literal["disable", "enable"]
    route_offload_mclag: Literal["disable", "enable"]
    route_offload_router: str | list[str] | list[ManagedSwitchRouteoffloadrouterItem]
    vlan: str | list[str] | list[ManagedSwitchVlanItem]
    type: Literal["virtual", "physical"]
    owner_vdom: str
    flow_identity: str
    staged_image_version: str
    delayed_restart_trigger: int
    firmware_provision: Literal["enable", "disable"]
    firmware_provision_version: str
    firmware_provision_latest: Literal["disable", "once"]
    ports: str | list[str] | list[ManagedSwitchPortsItem]
    ip_source_guard: str | list[str] | list[ManagedSwitchIpsourceguardItem]
    stp_settings: ManagedSwitchStpsettingsDict
    stp_instance: str | list[str] | list[ManagedSwitchStpinstanceItem]
    override_snmp_sysinfo: Literal["disable", "enable"]
    snmp_sysinfo: ManagedSwitchSnmpsysinfoDict
    override_snmp_trap_threshold: Literal["enable", "disable"]
    snmp_trap_threshold: ManagedSwitchSnmptrapthresholdDict
    override_snmp_community: Literal["enable", "disable"]
    snmp_community: str | list[str] | list[ManagedSwitchSnmpcommunityItem]
    override_snmp_user: Literal["enable", "disable"]
    snmp_user: str | list[str] | list[ManagedSwitchSnmpuserItem]
    qos_drop_policy: Literal["taildrop", "random-early-detection"]
    qos_red_probability: int
    switch_log: ManagedSwitchSwitchlogDict
    remote_log: str | list[str] | list[ManagedSwitchRemotelogItem]
    storm_control: ManagedSwitchStormcontrolDict
    mirror: str | list[str] | list[ManagedSwitchMirrorItem]
    static_mac: str | list[str] | list[ManagedSwitchStaticmacItem]
    custom_command: str | list[str] | list[ManagedSwitchCustomcommandItem]
    dhcp_snooping_static_client: str | list[str] | list[ManagedSwitchDhcpsnoopingstaticclientItem]
    igmp_snooping: ManagedSwitchIgmpsnoopingDict
    x802_1X_settings: ManagedSwitchX8021xsettingsDict
    router_vrf: str | list[str] | list[ManagedSwitchRoutervrfItem]
    system_interface: str | list[str] | list[ManagedSwitchSysteminterfaceItem]
    router_static: str | list[str] | list[ManagedSwitchRouterstaticItem]
    system_dhcp_server: str | list[str] | list[ManagedSwitchSystemdhcpserverItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ManagedSwitchResponse(TypedDict, total=False):
    """Response type for ManagedSwitch - use with .dict property for typed dict access."""
    switch_id: str
    sn: str
    description: str
    switch_profile: str
    access_profile: str
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    fsw_wan1_peer: str
    fsw_wan1_admin: Literal["discovered", "disable", "enable"]
    poe_pre_standard_detection: Literal["enable", "disable"]
    dhcp_server_access_list: Literal["global", "enable", "disable"]
    poe_detection_type: int
    max_poe_budget: int
    directly_connected: int
    version: int
    max_allowed_trunk_members: int
    pre_provisioned: int
    l3_discovered: int
    mgmt_mode: int
    tunnel_discovered: int
    tdr_supported: str
    dynamic_capability: str
    switch_device_tag: str
    switch_dhcp_opt43_key: str
    mclag_igmp_snooping_aware: Literal["enable", "disable"]
    dynamically_discovered: int
    ptp_status: Literal["disable", "enable"]
    ptp_profile: str
    radius_nas_ip_override: Literal["disable", "enable"]
    radius_nas_ip: str
    route_offload: Literal["disable", "enable"]
    route_offload_mclag: Literal["disable", "enable"]
    route_offload_router: list[ManagedSwitchRouteoffloadrouterItem]
    vlan: list[ManagedSwitchVlanItem]
    type: Literal["virtual", "physical"]
    owner_vdom: str
    flow_identity: str
    staged_image_version: str
    delayed_restart_trigger: int
    firmware_provision: Literal["enable", "disable"]
    firmware_provision_version: str
    firmware_provision_latest: Literal["disable", "once"]
    ports: list[ManagedSwitchPortsItem]
    ip_source_guard: list[ManagedSwitchIpsourceguardItem]
    stp_settings: ManagedSwitchStpsettingsDict
    stp_instance: list[ManagedSwitchStpinstanceItem]
    override_snmp_sysinfo: Literal["disable", "enable"]
    snmp_sysinfo: ManagedSwitchSnmpsysinfoDict
    override_snmp_trap_threshold: Literal["enable", "disable"]
    snmp_trap_threshold: ManagedSwitchSnmptrapthresholdDict
    override_snmp_community: Literal["enable", "disable"]
    snmp_community: list[ManagedSwitchSnmpcommunityItem]
    override_snmp_user: Literal["enable", "disable"]
    snmp_user: list[ManagedSwitchSnmpuserItem]
    qos_drop_policy: Literal["taildrop", "random-early-detection"]
    qos_red_probability: int
    switch_log: ManagedSwitchSwitchlogDict
    remote_log: list[ManagedSwitchRemotelogItem]
    storm_control: ManagedSwitchStormcontrolDict
    mirror: list[ManagedSwitchMirrorItem]
    static_mac: list[ManagedSwitchStaticmacItem]
    custom_command: list[ManagedSwitchCustomcommandItem]
    dhcp_snooping_static_client: list[ManagedSwitchDhcpsnoopingstaticclientItem]
    igmp_snooping: ManagedSwitchIgmpsnoopingDict
    x802_1X_settings: ManagedSwitchX8021xsettingsDict
    router_vrf: list[ManagedSwitchRoutervrfItem]
    system_interface: list[ManagedSwitchSysteminterfaceItem]
    router_static: list[ManagedSwitchRouterstaticItem]
    system_dhcp_server: list[ManagedSwitchSystemdhcpserverItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ManagedSwitchPortsAllowedvlansItemObject(FortiObject[ManagedSwitchPortsAllowedvlansItem]):
    """Typed object for ports.allowed-vlans table items with attribute access."""
    vlan_name: str


class ManagedSwitchPortsUntaggedvlansItemObject(FortiObject[ManagedSwitchPortsUntaggedvlansItem]):
    """Typed object for ports.untagged-vlans table items with attribute access."""
    vlan_name: str


class ManagedSwitchPortsAclgroupItemObject(FortiObject[ManagedSwitchPortsAclgroupItem]):
    """Typed object for ports.acl-group table items with attribute access."""
    name: str


class ManagedSwitchPortsFortiswitchaclsItemObject(FortiObject[ManagedSwitchPortsFortiswitchaclsItem]):
    """Typed object for ports.fortiswitch-acls table items with attribute access."""
    id: int


class ManagedSwitchPortsDhcpsnoopoption82overrideItemObject(FortiObject[ManagedSwitchPortsDhcpsnoopoption82overrideItem]):
    """Typed object for ports.dhcp-snoop-option82-override table items with attribute access."""
    vlan_name: str
    circuit_id: str
    remote_id: str


class ManagedSwitchPortsInterfacetagsItemObject(FortiObject[ManagedSwitchPortsInterfacetagsItem]):
    """Typed object for ports.interface-tags table items with attribute access."""
    tag_name: str


class ManagedSwitchPortsMembersItemObject(FortiObject[ManagedSwitchPortsMembersItem]):
    """Typed object for ports.members table items with attribute access."""
    member_name: str


class ManagedSwitchIpsourceguardBindingentryItemObject(FortiObject[ManagedSwitchIpsourceguardBindingentryItem]):
    """Typed object for ip-source-guard.binding-entry table items with attribute access."""
    entry_name: str
    ip: str
    mac: str


class ManagedSwitchSnmpcommunityHostsItemObject(FortiObject[ManagedSwitchSnmpcommunityHostsItem]):
    """Typed object for snmp-community.hosts table items with attribute access."""
    id: int
    ip: str


class ManagedSwitchMirrorSrcingressItemObject(FortiObject[ManagedSwitchMirrorSrcingressItem]):
    """Typed object for mirror.src-ingress table items with attribute access."""
    name: str


class ManagedSwitchMirrorSrcegressItemObject(FortiObject[ManagedSwitchMirrorSrcegressItem]):
    """Typed object for mirror.src-egress table items with attribute access."""
    name: str


class ManagedSwitchSystemdhcpserverIprangeItemObject(FortiObject[ManagedSwitchSystemdhcpserverIprangeItem]):
    """Typed object for system-dhcp-server.ip-range table items with attribute access."""
    id: int
    start_ip: str
    end_ip: str


class ManagedSwitchSystemdhcpserverOptionsItemObject(FortiObject[ManagedSwitchSystemdhcpserverOptionsItem]):
    """Typed object for system-dhcp-server.options table items with attribute access."""
    id: int
    code: int
    type: Literal["hex", "string", "ip", "fqdn"]
    value: str
    ip: str | list[str]


class ManagedSwitchRouteoffloadrouterItemObject(FortiObject[ManagedSwitchRouteoffloadrouterItem]):
    """Typed object for route-offload-router table items with attribute access."""
    vlan_name: str
    router_ip: str


class ManagedSwitchVlanItemObject(FortiObject[ManagedSwitchVlanItem]):
    """Typed object for vlan table items with attribute access."""
    vlan_name: str
    assignment_priority: int


class ManagedSwitchPortsItemObject(FortiObject[ManagedSwitchPortsItem]):
    """Typed object for ports table items with attribute access."""
    port_name: str
    port_owner: str
    switch_id: str
    speed: Literal["10half", "10full", "100half", "100full", "1000full", "10000full", "auto", "1000auto", "1000full-fiber", "40000full", "auto-module", "100FX-half", "100FX-full", "100000full", "2500auto", "2500full", "25000full", "50000full", "10000cr", "10000sr", "100000sr4", "100000cr4", "40000sr4", "40000cr4", "40000auto", "25000cr", "25000sr", "50000cr", "50000sr", "5000auto", "sgmii-auto"]
    status: Literal["up", "down"]
    poe_status: Literal["enable", "disable"]
    ip_source_guard: Literal["disable", "enable"]
    ptp_status: Literal["disable", "enable"]
    ptp_policy: str
    aggregator_mode: Literal["bandwidth", "count"]
    flapguard: Literal["enable", "disable"]
    flap_rate: int
    flap_duration: int
    flap_timeout: int
    rpvst_port: Literal["disabled", "enabled"]
    poe_pre_standard_detection: Literal["enable", "disable"]
    port_number: int
    port_prefix_type: int
    fortilink_port: int
    poe_capable: int
    pd_capable: int
    stacking_port: int
    p2p_port: int
    mclag_icl_port: int
    authenticated_port: int
    restricted_auth_port: int
    encrypted_port: int
    fiber_port: int
    media_type: str
    poe_standard: str
    poe_max_power: str
    poe_mode_bt_cabable: int
    poe_port_mode: Literal["ieee802-3af", "ieee802-3at", "ieee802-3bt"]
    poe_port_priority: Literal["critical-priority", "high-priority", "low-priority", "medium-priority"]
    poe_port_power: Literal["normal", "perpetual", "perpetual-fast"]
    flags: int
    isl_local_trunk_name: str
    isl_peer_port_name: str
    isl_peer_device_name: str
    isl_peer_device_sn: str
    fgt_peer_port_name: str
    fgt_peer_device_name: str
    vlan: str
    allowed_vlans_all: Literal["enable", "disable"]
    allowed_vlans: FortiObjectList[ManagedSwitchPortsAllowedvlansItemObject]
    untagged_vlans: FortiObjectList[ManagedSwitchPortsUntaggedvlansItemObject]
    type: Literal["physical", "trunk"]
    access_mode: Literal["dynamic", "nac", "static"]
    matched_dpp_policy: str
    matched_dpp_intf_tags: str
    acl_group: FortiObjectList[ManagedSwitchPortsAclgroupItemObject]
    fortiswitch_acls: FortiObjectList[ManagedSwitchPortsFortiswitchaclsItemObject]
    dhcp_snooping: Literal["untrusted", "trusted"]
    dhcp_snoop_option82_trust: Literal["enable", "disable"]
    dhcp_snoop_option82_override: FortiObjectList[ManagedSwitchPortsDhcpsnoopoption82overrideItemObject]
    arp_inspection_trust: Literal["untrusted", "trusted"]
    igmp_snooping_flood_reports: Literal["enable", "disable"]
    mcast_snooping_flood_traffic: Literal["enable", "disable"]
    stp_state: Literal["enabled", "disabled"]
    stp_root_guard: Literal["enabled", "disabled"]
    stp_bpdu_guard: Literal["enabled", "disabled"]
    stp_bpdu_guard_timeout: int
    edge_port: Literal["enable", "disable"]
    discard_mode: Literal["none", "all-untagged", "all-tagged"]
    packet_sampler: Literal["enabled", "disabled"]
    packet_sample_rate: int
    sflow_counter_interval: int
    sample_direction: Literal["tx", "rx", "both"]
    fec_capable: int
    fec_state: Literal["disabled", "cl74", "cl91", "detect-by-module"]
    flow_control: Literal["disable", "tx", "rx", "both"]
    pause_meter: int
    pause_meter_resume: Literal["75%", "50%", "25%"]
    loop_guard: Literal["enabled", "disabled"]
    loop_guard_timeout: int
    port_policy: str
    qos_policy: str
    storm_control_policy: str
    port_security_policy: str
    export_to_pool: str
    interface_tags: FortiObjectList[ManagedSwitchPortsInterfacetagsItemObject]
    learning_limit: int
    sticky_mac: Literal["enable", "disable"]
    lldp_status: Literal["disable", "rx-only", "tx-only", "tx-rx"]
    lldp_profile: str
    export_to: str
    mac_addr: str
    allow_arp_monitor: Literal["disable", "enable"]
    qnq: str
    log_mac_event: Literal["disable", "enable"]
    port_selection_criteria: Literal["src-mac", "dst-mac", "src-dst-mac", "src-ip", "dst-ip", "src-dst-ip"]
    description: str
    lacp_speed: Literal["slow", "fast"]
    mode: Literal["static", "lacp-passive", "lacp-active"]
    bundle: Literal["enable", "disable"]
    member_withdrawal_behavior: Literal["forward", "block"]
    mclag: Literal["enable", "disable"]
    min_bundle: int
    max_bundle: int
    members: FortiObjectList[ManagedSwitchPortsMembersItemObject]
    fallback_port: str


class ManagedSwitchIpsourceguardItemObject(FortiObject[ManagedSwitchIpsourceguardItem]):
    """Typed object for ip-source-guard table items with attribute access."""
    port: str
    description: str
    binding_entry: FortiObjectList[ManagedSwitchIpsourceguardBindingentryItemObject]


class ManagedSwitchStpinstanceItemObject(FortiObject[ManagedSwitchStpinstanceItem]):
    """Typed object for stp-instance table items with attribute access."""
    id: str
    priority: Literal["0", "4096", "8192", "12288", "16384", "20480", "24576", "28672", "32768", "36864", "40960", "45056", "49152", "53248", "57344", "61440"]


class ManagedSwitchSnmpcommunityItemObject(FortiObject[ManagedSwitchSnmpcommunityItem]):
    """Typed object for snmp-community table items with attribute access."""
    id: int
    name: str
    status: Literal["disable", "enable"]
    hosts: FortiObjectList[ManagedSwitchSnmpcommunityHostsItemObject]
    query_v1_status: Literal["disable", "enable"]
    query_v1_port: int
    query_v2c_status: Literal["disable", "enable"]
    query_v2c_port: int
    trap_v1_status: Literal["disable", "enable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["disable", "enable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"]


class ManagedSwitchSnmpuserItemObject(FortiObject[ManagedSwitchSnmpuserItem]):
    """Typed object for snmp-user table items with attribute access."""
    name: str
    queries: Literal["disable", "enable"]
    query_port: int
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
    auth_proto: Literal["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
    auth_pwd: str
    priv_proto: Literal["aes128", "aes192", "aes192c", "aes256", "aes256c", "des"]
    priv_pwd: str


class ManagedSwitchRemotelogItemObject(FortiObject[ManagedSwitchRemotelogItem]):
    """Typed object for remote-log table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    server: str
    port: int
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    csv: Literal["enable", "disable"]
    facility: Literal["kernel", "user", "mail", "daemon", "auth", "syslog", "lpr", "news", "uucp", "cron", "authpriv", "ftp", "ntp", "audit", "alert", "clock", "local0", "local1", "local2", "local3", "local4", "local5", "local6", "local7"]


class ManagedSwitchMirrorItemObject(FortiObject[ManagedSwitchMirrorItem]):
    """Typed object for mirror table items with attribute access."""
    name: str
    status: Literal["active", "inactive"]
    switching_packet: Literal["enable", "disable"]
    dst: str
    src_ingress: FortiObjectList[ManagedSwitchMirrorSrcingressItemObject]
    src_egress: FortiObjectList[ManagedSwitchMirrorSrcegressItemObject]


class ManagedSwitchStaticmacItemObject(FortiObject[ManagedSwitchStaticmacItem]):
    """Typed object for static-mac table items with attribute access."""
    id: int
    type: Literal["static", "sticky"]
    vlan: str
    mac: str
    interface: str
    description: str


class ManagedSwitchCustomcommandItemObject(FortiObject[ManagedSwitchCustomcommandItem]):
    """Typed object for custom-command table items with attribute access."""
    command_entry: str
    command_name: str


class ManagedSwitchDhcpsnoopingstaticclientItemObject(FortiObject[ManagedSwitchDhcpsnoopingstaticclientItem]):
    """Typed object for dhcp-snooping-static-client table items with attribute access."""
    name: str
    vlan: str
    ip: str
    mac: str
    port: str


class ManagedSwitchRoutervrfItemObject(FortiObject[ManagedSwitchRoutervrfItem]):
    """Typed object for router-vrf table items with attribute access."""
    name: str
    switch_id: str
    vrfid: int


class ManagedSwitchSysteminterfaceItemObject(FortiObject[ManagedSwitchSysteminterfaceItem]):
    """Typed object for system-interface table items with attribute access."""
    name: str
    switch_id: str
    mode: Literal["static", "dhcp"]
    ip: str
    status: Literal["disable", "enable"]
    allowaccess: Literal["ping", "https", "http", "ssh", "snmp", "telnet", "radius-acct"]
    vlan: str
    type: Literal["vlan", "physical"]
    interface: str
    vrf: str


class ManagedSwitchRouterstaticItemObject(FortiObject[ManagedSwitchRouterstaticItem]):
    """Typed object for router-static table items with attribute access."""
    id: int
    switch_id: str
    blackhole: Literal["disable", "enable"]
    comment: str
    device: str
    distance: int
    dst: str
    dynamic_gateway: Literal["disable", "enable"]
    gateway: str
    status: Literal["disable", "enable"]
    vrf: str


class ManagedSwitchSystemdhcpserverItemObject(FortiObject[ManagedSwitchSystemdhcpserverItem]):
    """Typed object for system-dhcp-server table items with attribute access."""
    id: int
    switch_id: str
    status: Literal["disable", "enable"]
    lease_time: int
    dns_service: Literal["local", "default", "specify"]
    dns_server1: str
    dns_server2: str
    dns_server3: str
    ntp_service: Literal["local", "default", "specify"]
    ntp_server1: str
    ntp_server2: str
    ntp_server3: str
    default_gateway: str
    netmask: str
    interface: str
    ip_range: FortiObjectList[ManagedSwitchSystemdhcpserverIprangeItemObject]
    options: FortiObjectList[ManagedSwitchSystemdhcpserverOptionsItemObject]


class ManagedSwitchIgmpsnoopingVlansItemObject(FortiObject[ManagedSwitchIgmpsnoopingVlansItem]):
    """Typed object for igmp-snooping.vlans table items with attribute access."""
    vlan_name: str
    proxy: Literal["disable", "enable", "global"]
    querier: Literal["disable", "enable"]
    querier_addr: str
    version: int


class ManagedSwitchStpsettingsObject(FortiObject):
    """Nested object for stp-settings field with attribute access."""
    local_override: Literal["enable", "disable"]
    name: str
    revision: int
    hello_time: int
    forward_time: int
    max_age: int
    max_hops: int
    pending_timer: int


class ManagedSwitchSnmpsysinfoObject(FortiObject):
    """Nested object for snmp-sysinfo field with attribute access."""
    status: Literal["disable", "enable"]
    engine_id: str
    description: str
    contact_info: str
    location: str


class ManagedSwitchSnmptrapthresholdObject(FortiObject):
    """Nested object for snmp-trap-threshold field with attribute access."""
    trap_high_cpu_threshold: int
    trap_low_memory_threshold: int
    trap_log_full_threshold: int


class ManagedSwitchSwitchlogObject(FortiObject):
    """Nested object for switch-log field with attribute access."""
    local_override: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


class ManagedSwitchStormcontrolObject(FortiObject):
    """Nested object for storm-control field with attribute access."""
    local_override: Literal["enable", "disable"]
    rate: int
    burst_size_level: int
    unknown_unicast: Literal["enable", "disable"]
    unknown_multicast: Literal["enable", "disable"]
    broadcast: Literal["enable", "disable"]


class ManagedSwitchIgmpsnoopingObject(FortiObject):
    """Nested object for igmp-snooping field with attribute access."""
    local_override: Literal["enable", "disable"]
    aging_time: int
    flood_unknown_multicast: Literal["enable", "disable"]
    vlans: str | list[str]


class ManagedSwitchX8021xsettingsObject(FortiObject):
    """Nested object for 802-1X-settings field with attribute access."""
    local_override: Literal["enable", "disable"]
    link_down_auth: Literal["set-unauth", "no-action"]
    reauth_period: int
    max_reauth_attempt: int
    tx_period: int
    mab_reauth: Literal["disable", "enable"]
    mac_username_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_password_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_calling_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_called_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_case: Literal["lowercase", "uppercase"]


class ManagedSwitchObject(FortiObject):
    """Typed FortiObject for ManagedSwitch with field access."""
    switch_id: str
    sn: str
    description: str
    switch_profile: str
    access_profile: str
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    fsw_wan1_peer: str
    fsw_wan1_admin: Literal["discovered", "disable", "enable"]
    poe_pre_standard_detection: Literal["enable", "disable"]
    dhcp_server_access_list: Literal["global", "enable", "disable"]
    poe_detection_type: int
    max_poe_budget: int
    directly_connected: int
    max_allowed_trunk_members: int
    pre_provisioned: int
    l3_discovered: int
    mgmt_mode: int
    tunnel_discovered: int
    tdr_supported: str
    dynamic_capability: str
    switch_device_tag: str
    switch_dhcp_opt43_key: str
    mclag_igmp_snooping_aware: Literal["enable", "disable"]
    dynamically_discovered: int
    ptp_status: Literal["disable", "enable"]
    ptp_profile: str
    radius_nas_ip_override: Literal["disable", "enable"]
    radius_nas_ip: str
    route_offload: Literal["disable", "enable"]
    route_offload_mclag: Literal["disable", "enable"]
    route_offload_router: FortiObjectList[ManagedSwitchRouteoffloadrouterItemObject]
    vlan: FortiObjectList[ManagedSwitchVlanItemObject]
    type: Literal["virtual", "physical"]
    owner_vdom: str
    flow_identity: str
    staged_image_version: str
    delayed_restart_trigger: int
    firmware_provision: Literal["enable", "disable"]
    firmware_provision_version: str
    firmware_provision_latest: Literal["disable", "once"]
    ports: FortiObjectList[ManagedSwitchPortsItemObject]
    ip_source_guard: FortiObjectList[ManagedSwitchIpsourceguardItemObject]
    stp_settings: ManagedSwitchStpsettingsObject
    stp_instance: FortiObjectList[ManagedSwitchStpinstanceItemObject]
    override_snmp_sysinfo: Literal["disable", "enable"]
    snmp_sysinfo: ManagedSwitchSnmpsysinfoObject
    override_snmp_trap_threshold: Literal["enable", "disable"]
    snmp_trap_threshold: ManagedSwitchSnmptrapthresholdObject
    override_snmp_community: Literal["enable", "disable"]
    snmp_community: FortiObjectList[ManagedSwitchSnmpcommunityItemObject]
    override_snmp_user: Literal["enable", "disable"]
    snmp_user: FortiObjectList[ManagedSwitchSnmpuserItemObject]
    qos_drop_policy: Literal["taildrop", "random-early-detection"]
    qos_red_probability: int
    switch_log: ManagedSwitchSwitchlogObject
    remote_log: FortiObjectList[ManagedSwitchRemotelogItemObject]
    storm_control: ManagedSwitchStormcontrolObject
    mirror: FortiObjectList[ManagedSwitchMirrorItemObject]
    static_mac: FortiObjectList[ManagedSwitchStaticmacItemObject]
    custom_command: FortiObjectList[ManagedSwitchCustomcommandItemObject]
    dhcp_snooping_static_client: FortiObjectList[ManagedSwitchDhcpsnoopingstaticclientItemObject]
    igmp_snooping: ManagedSwitchIgmpsnoopingObject
    x802_1X_settings: ManagedSwitchX8021xsettingsObject
    router_vrf: FortiObjectList[ManagedSwitchRoutervrfItemObject]
    system_interface: FortiObjectList[ManagedSwitchSysteminterfaceItemObject]
    router_static: FortiObjectList[ManagedSwitchRouterstaticItemObject]
    system_dhcp_server: FortiObjectList[ManagedSwitchSystemdhcpserverItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ManagedSwitch:
    """
    
    Endpoint: switch_controller/managed_switch
    Category: cmdb
    MKey: switch-id
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
        switch_id: str,
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
    ) -> ManagedSwitchObject: ...
    
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
    ) -> FortiObjectList[ManagedSwitchObject]: ...
    
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
        payload_dict: ManagedSwitchPayload | None = ...,
        switch_id: str | None = ...,
        sn: str | None = ...,
        description: str | None = ...,
        switch_profile: str | None = ...,
        access_profile: str | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        fsw_wan1_peer: str | None = ...,
        fsw_wan1_admin: Literal["discovered", "disable", "enable"] | None = ...,
        poe_pre_standard_detection: Literal["enable", "disable"] | None = ...,
        dhcp_server_access_list: Literal["global", "enable", "disable"] | None = ...,
        poe_detection_type: int | None = ...,
        max_poe_budget: int | None = ...,
        directly_connected: int | None = ...,
        version: int | None = ...,
        max_allowed_trunk_members: int | None = ...,
        pre_provisioned: int | None = ...,
        l3_discovered: int | None = ...,
        mgmt_mode: int | None = ...,
        tunnel_discovered: int | None = ...,
        tdr_supported: str | None = ...,
        dynamic_capability: str | None = ...,
        switch_device_tag: str | None = ...,
        switch_dhcp_opt43_key: str | None = ...,
        mclag_igmp_snooping_aware: Literal["enable", "disable"] | None = ...,
        dynamically_discovered: int | None = ...,
        ptp_status: Literal["disable", "enable"] | None = ...,
        ptp_profile: str | None = ...,
        radius_nas_ip_override: Literal["disable", "enable"] | None = ...,
        radius_nas_ip: str | None = ...,
        route_offload: Literal["disable", "enable"] | None = ...,
        route_offload_mclag: Literal["disable", "enable"] | None = ...,
        route_offload_router: str | list[str] | list[ManagedSwitchRouteoffloadrouterItem] | None = ...,
        vlan: str | list[str] | list[ManagedSwitchVlanItem] | None = ...,
        type: Literal["virtual", "physical"] | None = ...,
        owner_vdom: str | None = ...,
        flow_identity: str | None = ...,
        staged_image_version: str | None = ...,
        delayed_restart_trigger: int | None = ...,
        firmware_provision: Literal["enable", "disable"] | None = ...,
        firmware_provision_version: str | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        ports: str | list[str] | list[ManagedSwitchPortsItem] | None = ...,
        ip_source_guard: str | list[str] | list[ManagedSwitchIpsourceguardItem] | None = ...,
        stp_settings: ManagedSwitchStpsettingsDict | None = ...,
        stp_instance: str | list[str] | list[ManagedSwitchStpinstanceItem] | None = ...,
        override_snmp_sysinfo: Literal["disable", "enable"] | None = ...,
        snmp_sysinfo: ManagedSwitchSnmpsysinfoDict | None = ...,
        override_snmp_trap_threshold: Literal["enable", "disable"] | None = ...,
        snmp_trap_threshold: ManagedSwitchSnmptrapthresholdDict | None = ...,
        override_snmp_community: Literal["enable", "disable"] | None = ...,
        snmp_community: str | list[str] | list[ManagedSwitchSnmpcommunityItem] | None = ...,
        override_snmp_user: Literal["enable", "disable"] | None = ...,
        snmp_user: str | list[str] | list[ManagedSwitchSnmpuserItem] | None = ...,
        qos_drop_policy: Literal["taildrop", "random-early-detection"] | None = ...,
        qos_red_probability: int | None = ...,
        switch_log: ManagedSwitchSwitchlogDict | None = ...,
        remote_log: str | list[str] | list[ManagedSwitchRemotelogItem] | None = ...,
        storm_control: ManagedSwitchStormcontrolDict | None = ...,
        mirror: str | list[str] | list[ManagedSwitchMirrorItem] | None = ...,
        static_mac: str | list[str] | list[ManagedSwitchStaticmacItem] | None = ...,
        custom_command: str | list[str] | list[ManagedSwitchCustomcommandItem] | None = ...,
        dhcp_snooping_static_client: str | list[str] | list[ManagedSwitchDhcpsnoopingstaticclientItem] | None = ...,
        igmp_snooping: ManagedSwitchIgmpsnoopingDict | None = ...,
        x802_1X_settings: ManagedSwitchX8021xsettingsDict | None = ...,
        router_vrf: str | list[str] | list[ManagedSwitchRoutervrfItem] | None = ...,
        system_interface: str | list[str] | list[ManagedSwitchSysteminterfaceItem] | None = ...,
        router_static: str | list[str] | list[ManagedSwitchRouterstaticItem] | None = ...,
        system_dhcp_server: str | list[str] | list[ManagedSwitchSystemdhcpserverItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ManagedSwitchObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ManagedSwitchPayload | None = ...,
        switch_id: str | None = ...,
        sn: str | None = ...,
        description: str | None = ...,
        switch_profile: str | None = ...,
        access_profile: str | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        fsw_wan1_peer: str | None = ...,
        fsw_wan1_admin: Literal["discovered", "disable", "enable"] | None = ...,
        poe_pre_standard_detection: Literal["enable", "disable"] | None = ...,
        dhcp_server_access_list: Literal["global", "enable", "disable"] | None = ...,
        poe_detection_type: int | None = ...,
        max_poe_budget: int | None = ...,
        directly_connected: int | None = ...,
        version: int | None = ...,
        max_allowed_trunk_members: int | None = ...,
        pre_provisioned: int | None = ...,
        l3_discovered: int | None = ...,
        mgmt_mode: int | None = ...,
        tunnel_discovered: int | None = ...,
        tdr_supported: str | None = ...,
        dynamic_capability: str | None = ...,
        switch_device_tag: str | None = ...,
        switch_dhcp_opt43_key: str | None = ...,
        mclag_igmp_snooping_aware: Literal["enable", "disable"] | None = ...,
        dynamically_discovered: int | None = ...,
        ptp_status: Literal["disable", "enable"] | None = ...,
        ptp_profile: str | None = ...,
        radius_nas_ip_override: Literal["disable", "enable"] | None = ...,
        radius_nas_ip: str | None = ...,
        route_offload: Literal["disable", "enable"] | None = ...,
        route_offload_mclag: Literal["disable", "enable"] | None = ...,
        route_offload_router: str | list[str] | list[ManagedSwitchRouteoffloadrouterItem] | None = ...,
        vlan: str | list[str] | list[ManagedSwitchVlanItem] | None = ...,
        type: Literal["virtual", "physical"] | None = ...,
        owner_vdom: str | None = ...,
        flow_identity: str | None = ...,
        staged_image_version: str | None = ...,
        delayed_restart_trigger: int | None = ...,
        firmware_provision: Literal["enable", "disable"] | None = ...,
        firmware_provision_version: str | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        ports: str | list[str] | list[ManagedSwitchPortsItem] | None = ...,
        ip_source_guard: str | list[str] | list[ManagedSwitchIpsourceguardItem] | None = ...,
        stp_settings: ManagedSwitchStpsettingsDict | None = ...,
        stp_instance: str | list[str] | list[ManagedSwitchStpinstanceItem] | None = ...,
        override_snmp_sysinfo: Literal["disable", "enable"] | None = ...,
        snmp_sysinfo: ManagedSwitchSnmpsysinfoDict | None = ...,
        override_snmp_trap_threshold: Literal["enable", "disable"] | None = ...,
        snmp_trap_threshold: ManagedSwitchSnmptrapthresholdDict | None = ...,
        override_snmp_community: Literal["enable", "disable"] | None = ...,
        snmp_community: str | list[str] | list[ManagedSwitchSnmpcommunityItem] | None = ...,
        override_snmp_user: Literal["enable", "disable"] | None = ...,
        snmp_user: str | list[str] | list[ManagedSwitchSnmpuserItem] | None = ...,
        qos_drop_policy: Literal["taildrop", "random-early-detection"] | None = ...,
        qos_red_probability: int | None = ...,
        switch_log: ManagedSwitchSwitchlogDict | None = ...,
        remote_log: str | list[str] | list[ManagedSwitchRemotelogItem] | None = ...,
        storm_control: ManagedSwitchStormcontrolDict | None = ...,
        mirror: str | list[str] | list[ManagedSwitchMirrorItem] | None = ...,
        static_mac: str | list[str] | list[ManagedSwitchStaticmacItem] | None = ...,
        custom_command: str | list[str] | list[ManagedSwitchCustomcommandItem] | None = ...,
        dhcp_snooping_static_client: str | list[str] | list[ManagedSwitchDhcpsnoopingstaticclientItem] | None = ...,
        igmp_snooping: ManagedSwitchIgmpsnoopingDict | None = ...,
        x802_1X_settings: ManagedSwitchX8021xsettingsDict | None = ...,
        router_vrf: str | list[str] | list[ManagedSwitchRoutervrfItem] | None = ...,
        system_interface: str | list[str] | list[ManagedSwitchSysteminterfaceItem] | None = ...,
        router_static: str | list[str] | list[ManagedSwitchRouterstaticItem] | None = ...,
        system_dhcp_server: str | list[str] | list[ManagedSwitchSystemdhcpserverItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ManagedSwitchObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        switch_id: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        switch_id: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_switch_id: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        switch_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ManagedSwitchPayload | None = ...,
        switch_id: str | None = ...,
        sn: str | None = ...,
        description: str | None = ...,
        switch_profile: str | None = ...,
        access_profile: str | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        fsw_wan1_peer: str | None = ...,
        fsw_wan1_admin: Literal["discovered", "disable", "enable"] | None = ...,
        poe_pre_standard_detection: Literal["enable", "disable"] | None = ...,
        dhcp_server_access_list: Literal["global", "enable", "disable"] | None = ...,
        poe_detection_type: int | None = ...,
        max_poe_budget: int | None = ...,
        directly_connected: int | None = ...,
        version: int | None = ...,
        max_allowed_trunk_members: int | None = ...,
        pre_provisioned: int | None = ...,
        l3_discovered: int | None = ...,
        mgmt_mode: int | None = ...,
        tunnel_discovered: int | None = ...,
        tdr_supported: str | None = ...,
        dynamic_capability: str | None = ...,
        switch_device_tag: str | None = ...,
        switch_dhcp_opt43_key: str | None = ...,
        mclag_igmp_snooping_aware: Literal["enable", "disable"] | None = ...,
        dynamically_discovered: int | None = ...,
        ptp_status: Literal["disable", "enable"] | None = ...,
        ptp_profile: str | None = ...,
        radius_nas_ip_override: Literal["disable", "enable"] | None = ...,
        radius_nas_ip: str | None = ...,
        route_offload: Literal["disable", "enable"] | None = ...,
        route_offload_mclag: Literal["disable", "enable"] | None = ...,
        route_offload_router: str | list[str] | list[ManagedSwitchRouteoffloadrouterItem] | None = ...,
        vlan: str | list[str] | list[ManagedSwitchVlanItem] | None = ...,
        type: Literal["virtual", "physical"] | None = ...,
        owner_vdom: str | None = ...,
        flow_identity: str | None = ...,
        staged_image_version: str | None = ...,
        delayed_restart_trigger: int | None = ...,
        firmware_provision: Literal["enable", "disable"] | None = ...,
        firmware_provision_version: str | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        ports: str | list[str] | list[ManagedSwitchPortsItem] | None = ...,
        ip_source_guard: str | list[str] | list[ManagedSwitchIpsourceguardItem] | None = ...,
        stp_settings: ManagedSwitchStpsettingsDict | None = ...,
        stp_instance: str | list[str] | list[ManagedSwitchStpinstanceItem] | None = ...,
        override_snmp_sysinfo: Literal["disable", "enable"] | None = ...,
        snmp_sysinfo: ManagedSwitchSnmpsysinfoDict | None = ...,
        override_snmp_trap_threshold: Literal["enable", "disable"] | None = ...,
        snmp_trap_threshold: ManagedSwitchSnmptrapthresholdDict | None = ...,
        override_snmp_community: Literal["enable", "disable"] | None = ...,
        snmp_community: str | list[str] | list[ManagedSwitchSnmpcommunityItem] | None = ...,
        override_snmp_user: Literal["enable", "disable"] | None = ...,
        snmp_user: str | list[str] | list[ManagedSwitchSnmpuserItem] | None = ...,
        qos_drop_policy: Literal["taildrop", "random-early-detection"] | None = ...,
        qos_red_probability: int | None = ...,
        switch_log: ManagedSwitchSwitchlogDict | None = ...,
        remote_log: str | list[str] | list[ManagedSwitchRemotelogItem] | None = ...,
        storm_control: ManagedSwitchStormcontrolDict | None = ...,
        mirror: str | list[str] | list[ManagedSwitchMirrorItem] | None = ...,
        static_mac: str | list[str] | list[ManagedSwitchStaticmacItem] | None = ...,
        custom_command: str | list[str] | list[ManagedSwitchCustomcommandItem] | None = ...,
        dhcp_snooping_static_client: str | list[str] | list[ManagedSwitchDhcpsnoopingstaticclientItem] | None = ...,
        igmp_snooping: ManagedSwitchIgmpsnoopingDict | None = ...,
        x802_1X_settings: ManagedSwitchX8021xsettingsDict | None = ...,
        router_vrf: str | list[str] | list[ManagedSwitchRoutervrfItem] | None = ...,
        system_interface: str | list[str] | list[ManagedSwitchSysteminterfaceItem] | None = ...,
        router_static: str | list[str] | list[ManagedSwitchRouterstaticItem] | None = ...,
        system_dhcp_server: str | list[str] | list[ManagedSwitchSystemdhcpserverItem] | None = ...,
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
    "ManagedSwitch",
    "ManagedSwitchPayload",
    "ManagedSwitchResponse",
    "ManagedSwitchObject",
]