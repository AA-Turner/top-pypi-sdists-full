""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/sdwan
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

class SdwanHealthcheckMembersItem(TypedDict, total=False):
    """Nested item for health-check.members field."""
    seq_num: int


class SdwanHealthcheckSlaItem(TypedDict, total=False):
    """Nested item for health-check.sla field."""
    id: int
    link_cost_factor: Literal["latency", "jitter", "packet-loss", "custom-profile-1", "mos", "remote"]
    latency_threshold: int
    jitter_threshold: int
    packetloss_threshold: int
    mos_threshold: str
    custom_profile_threshold: int
    priority_in_sla: int
    priority_out_sla: int


class SdwanServiceInputdeviceItem(TypedDict, total=False):
    """Nested item for service.input-device field."""
    name: str


class SdwanServiceInputzoneItem(TypedDict, total=False):
    """Nested item for service.input-zone field."""
    name: str


class SdwanServiceDstItem(TypedDict, total=False):
    """Nested item for service.dst field."""
    name: str


class SdwanServiceSrcItem(TypedDict, total=False):
    """Nested item for service.src field."""
    name: str


class SdwanServiceDst6Item(TypedDict, total=False):
    """Nested item for service.dst6 field."""
    name: str


class SdwanServiceSrc6Item(TypedDict, total=False):
    """Nested item for service.src6 field."""
    name: str


class SdwanServiceUsersItem(TypedDict, total=False):
    """Nested item for service.users field."""
    name: str


class SdwanServiceGroupsItem(TypedDict, total=False):
    """Nested item for service.groups field."""
    name: str


class SdwanServiceInternetservicecustomItem(TypedDict, total=False):
    """Nested item for service.internet-service-custom field."""
    name: str


class SdwanServiceInternetservicecustomgroupItem(TypedDict, total=False):
    """Nested item for service.internet-service-custom-group field."""
    name: str


class SdwanServiceInternetservicefortiguardItem(TypedDict, total=False):
    """Nested item for service.internet-service-fortiguard field."""
    name: str


class SdwanServiceInternetservicenameItem(TypedDict, total=False):
    """Nested item for service.internet-service-name field."""
    name: str


class SdwanServiceInternetservicegroupItem(TypedDict, total=False):
    """Nested item for service.internet-service-group field."""
    name: str


class SdwanServiceInternetserviceappctrlItem(TypedDict, total=False):
    """Nested item for service.internet-service-app-ctrl field."""
    id: int


class SdwanServiceInternetserviceappctrlgroupItem(TypedDict, total=False):
    """Nested item for service.internet-service-app-ctrl-group field."""
    name: str


class SdwanServiceInternetserviceappctrlcategoryItem(TypedDict, total=False):
    """Nested item for service.internet-service-app-ctrl-category field."""
    id: int


class SdwanServiceHealthcheckItem(TypedDict, total=False):
    """Nested item for service.health-check field."""
    name: str


class SdwanServiceSlaItem(TypedDict, total=False):
    """Nested item for service.sla field."""
    health_check: str
    id: int


class SdwanServicePrioritymembersItem(TypedDict, total=False):
    """Nested item for service.priority-members field."""
    seq_num: int


class SdwanServicePriorityzoneItem(TypedDict, total=False):
    """Nested item for service.priority-zone field."""
    name: str


class SdwanNeighborMemberItem(TypedDict, total=False):
    """Nested item for neighbor.member field."""
    seq_num: int


class SdwanDuplicationServiceidItem(TypedDict, total=False):
    """Nested item for duplication.service-id field."""
    id: int


class SdwanDuplicationSrcaddrItem(TypedDict, total=False):
    """Nested item for duplication.srcaddr field."""
    name: str


class SdwanDuplicationDstaddrItem(TypedDict, total=False):
    """Nested item for duplication.dstaddr field."""
    name: str


class SdwanDuplicationSrcaddr6Item(TypedDict, total=False):
    """Nested item for duplication.srcaddr6 field."""
    name: str


class SdwanDuplicationDstaddr6Item(TypedDict, total=False):
    """Nested item for duplication.dstaddr6 field."""
    name: str


class SdwanDuplicationSrcintfItem(TypedDict, total=False):
    """Nested item for duplication.srcintf field."""
    name: str


class SdwanDuplicationDstintfItem(TypedDict, total=False):
    """Nested item for duplication.dstintf field."""
    name: str


class SdwanDuplicationServiceItem(TypedDict, total=False):
    """Nested item for duplication.service field."""
    name: str


class SdwanFailalertinterfacesItem(TypedDict, total=False):
    """Nested item for fail-alert-interfaces field."""
    name: str


class SdwanZoneItem(TypedDict, total=False):
    """Nested item for zone field."""
    name: str
    advpn_select: Literal["enable", "disable"]
    advpn_health_check: str
    service_sla_tie_break: Literal["cfg-order", "fib-best-match", "priority", "input-device"]
    minimum_sla_meet_members: int


class SdwanMembersItem(TypedDict, total=False):
    """Nested item for members field."""
    seq_num: int
    interface: str
    zone: str
    gateway: str
    preferred_source: str
    source: str
    gateway6: str
    source6: str
    cost: int
    weight: int
    priority: int
    priority6: int
    priority_in_sla: int
    priority_out_sla: int
    spillover_threshold: int
    ingress_spillover_threshold: int
    volume_ratio: int
    status: Literal["disable", "enable"]
    transport_group: int
    comment: str


class SdwanHealthcheckItem(TypedDict, total=False):
    """Nested item for health-check field."""
    name: str
    fortiguard: Literal["disable", "enable"]
    fortiguard_name: str
    probe_packets: Literal["disable", "enable"]
    addr_mode: Literal["ipv4", "ipv6"]
    system_dns: Literal["disable", "enable"]
    server: str | list[str]
    detect_mode: Literal["active", "passive", "prefer-passive", "remote", "agent-based"]
    protocol: Literal["ping", "tcp-echo", "udp-echo", "http", "https", "twamp", "dns", "tcp-connect", "ftp"]
    port: int
    quality_measured_method: Literal["half-open", "half-close"]
    security_mode: Literal["none", "authentication"]
    user: str
    password: str
    packet_size: int
    ha_priority: int
    ftp_mode: Literal["passive", "port"]
    ftp_file: str
    http_get: str
    http_agent: str
    http_match: str
    dns_request_domain: str
    dns_match_ip: str
    interval: int
    probe_timeout: int
    agent_probe_timeout: int
    remote_probe_timeout: int
    failtime: int
    recoverytime: int
    probe_count: int
    diffservcode: str
    update_cascade_interface: Literal["enable", "disable"]
    update_static_route: Literal["enable", "disable"]
    update_bgp_route: Literal["enable", "disable"]
    embed_measured_health: Literal["enable", "disable"]
    sla_id_redistribute: int
    sla_fail_log_period: int
    sla_pass_log_period: int
    threshold_warning_packetloss: int
    threshold_alert_packetloss: int
    threshold_warning_latency: int
    threshold_alert_latency: int
    threshold_warning_jitter: int
    threshold_alert_jitter: int
    vrf: int
    source: str
    source6: str
    members: str | list[str] | list[SdwanHealthcheckMembersItem]
    mos_codec: Literal["g711", "g722", "g729"]
    class_id: int
    packet_loss_weight: int
    latency_weight: int
    jitter_weight: int
    bandwidth_weight: int
    sla: str | list[str] | list[SdwanHealthcheckSlaItem]


class SdwanServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    id: int
    name: str
    addr_mode: Literal["ipv4", "ipv6"]
    load_balance: Literal["enable", "disable"]
    input_device: str | list[str] | list[SdwanServiceInputdeviceItem]
    input_device_negate: Literal["enable", "disable"]
    input_zone: str | list[str] | list[SdwanServiceInputzoneItem]
    mode: Literal["auto", "manual", "priority", "sla"]
    zone_mode: Literal["enable", "disable"]
    minimum_sla_meet_members: int
    hash_mode: Literal["round-robin", "source-ip-based", "source-dest-ip-based", "inbandwidth", "outbandwidth", "bibandwidth"]
    shortcut_priority: Literal["enable", "disable", "auto"]
    role: Literal["standalone", "primary", "secondary"]
    standalone_action: Literal["enable", "disable"]
    quality_link: int
    tos: str
    tos_mask: str
    protocol: int
    start_port: int
    end_port: int
    start_src_port: int
    end_src_port: int
    dst: str | list[str] | list[SdwanServiceDstItem]
    dst_negate: Literal["enable", "disable"]
    src: str | list[str] | list[SdwanServiceSrcItem]
    dst6: str | list[str] | list[SdwanServiceDst6Item]
    src6: str | list[str] | list[SdwanServiceSrc6Item]
    src_negate: Literal["enable", "disable"]
    users: str | list[str] | list[SdwanServiceUsersItem]
    groups: str | list[str] | list[SdwanServiceGroupsItem]
    internet_service: Literal["enable", "disable"]
    internet_service_custom: str | list[str] | list[SdwanServiceInternetservicecustomItem]
    internet_service_custom_group: str | list[str] | list[SdwanServiceInternetservicecustomgroupItem]
    internet_service_fortiguard: str | list[str] | list[SdwanServiceInternetservicefortiguardItem]
    internet_service_name: str | list[str] | list[SdwanServiceInternetservicenameItem]
    internet_service_group: str | list[str] | list[SdwanServiceInternetservicegroupItem]
    internet_service_app_ctrl: str | list[str] | list[SdwanServiceInternetserviceappctrlItem]
    internet_service_app_ctrl_group: str | list[str] | list[SdwanServiceInternetserviceappctrlgroupItem]
    internet_service_app_ctrl_category: str | list[str] | list[SdwanServiceInternetserviceappctrlcategoryItem]
    health_check: str | list[str] | list[SdwanServiceHealthcheckItem]
    link_cost_factor: Literal["latency", "jitter", "packet-loss", "inbandwidth", "outbandwidth", "bibandwidth", "custom-profile-1"]
    packet_loss_weight: int
    latency_weight: int
    jitter_weight: int
    bandwidth_weight: int
    link_cost_threshold: int
    hold_down_time: int
    sla_stickiness: Literal["enable", "disable"]
    dscp_forward: Literal["enable", "disable"]
    dscp_reverse: Literal["enable", "disable"]
    dscp_forward_tag: str
    dscp_reverse_tag: str
    sla: str | list[str] | list[SdwanServiceSlaItem]
    priority_members: str | list[str] | list[SdwanServicePrioritymembersItem]
    priority_zone: str | list[str] | list[SdwanServicePriorityzoneItem]
    status: Literal["enable", "disable"]
    gateway: Literal["enable", "disable"]
    default: Literal["enable", "disable"]
    sla_compare_method: Literal["order", "number"]
    fib_best_match_force: Literal["disable", "enable"]
    tie_break: Literal["zone", "cfg-order", "fib-best-match", "priority", "input-device"]
    use_shortcut_sla: Literal["enable", "disable"]
    passive_measurement: Literal["enable", "disable"]
    agent_exclusive: Literal["enable", "disable"]
    shortcut: Literal["enable", "disable"]
    comment: str


class SdwanNeighborItem(TypedDict, total=False):
    """Nested item for neighbor field."""
    ip: str
    member: str | list[str] | list[SdwanNeighborMemberItem]
    service_id: int
    minimum_sla_meet_members: int
    mode: Literal["sla", "speedtest"]
    role: Literal["standalone", "primary", "secondary"]
    route_metric: Literal["preferable", "priority"]
    health_check: str
    sla_id: int


class SdwanDuplicationItem(TypedDict, total=False):
    """Nested item for duplication field."""
    id: int
    service_id: str | list[str] | list[SdwanDuplicationServiceidItem]
    srcaddr: str | list[str] | list[SdwanDuplicationSrcaddrItem]
    dstaddr: str | list[str] | list[SdwanDuplicationDstaddrItem]
    srcaddr6: str | list[str] | list[SdwanDuplicationSrcaddr6Item]
    dstaddr6: str | list[str] | list[SdwanDuplicationDstaddr6Item]
    srcintf: str | list[str] | list[SdwanDuplicationSrcintfItem]
    dstintf: str | list[str] | list[SdwanDuplicationDstintfItem]
    service: str | list[str] | list[SdwanDuplicationServiceItem]
    packet_duplication: Literal["disable", "force", "on-demand"]
    sla_match_service: Literal["enable", "disable"]
    packet_de_duplication: Literal["enable", "disable"]


class SdwanPayload(TypedDict, total=False):
    """Payload type for Sdwan operations."""
    status: Literal["disable", "enable"]
    load_balance_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based", "measured-volume-based"]
    speedtest_bypass_routing: Literal["disable", "enable"]
    duplication_max_num: int
    duplication_max_discrepancy: int
    neighbor_hold_down: Literal["enable", "disable"]
    neighbor_hold_down_time: int
    app_perf_log_period: int
    neighbor_hold_boot_time: int
    fail_detect: Literal["enable", "disable"]
    fail_alert_interfaces: str | list[str] | list[SdwanFailalertinterfacesItem]
    zone: str | list[str] | list[SdwanZoneItem]
    members: str | list[str] | list[SdwanMembersItem]
    health_check: str | list[str] | list[SdwanHealthcheckItem]
    service: str | list[str] | list[SdwanServiceItem]
    neighbor: str | list[str] | list[SdwanNeighborItem]
    duplication: str | list[str] | list[SdwanDuplicationItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SdwanResponse(TypedDict, total=False):
    """Response type for Sdwan - use with .dict property for typed dict access."""
    status: Literal["disable", "enable"]
    load_balance_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based", "measured-volume-based"]
    speedtest_bypass_routing: Literal["disable", "enable"]
    duplication_max_num: int
    duplication_max_discrepancy: int
    neighbor_hold_down: Literal["enable", "disable"]
    neighbor_hold_down_time: int
    app_perf_log_period: int
    neighbor_hold_boot_time: int
    fail_detect: Literal["enable", "disable"]
    fail_alert_interfaces: list[SdwanFailalertinterfacesItem]
    zone: list[SdwanZoneItem]
    members: list[SdwanMembersItem]
    health_check: list[SdwanHealthcheckItem]
    service: list[SdwanServiceItem]
    neighbor: list[SdwanNeighborItem]
    duplication: list[SdwanDuplicationItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SdwanHealthcheckMembersItemObject(FortiObject[SdwanHealthcheckMembersItem]):
    """Typed object for health-check.members table items with attribute access."""
    seq_num: int


class SdwanHealthcheckSlaItemObject(FortiObject[SdwanHealthcheckSlaItem]):
    """Typed object for health-check.sla table items with attribute access."""
    id: int
    link_cost_factor: Literal["latency", "jitter", "packet-loss", "custom-profile-1", "mos", "remote"]
    latency_threshold: int
    jitter_threshold: int
    packetloss_threshold: int
    mos_threshold: str
    custom_profile_threshold: int
    priority_in_sla: int
    priority_out_sla: int


class SdwanServiceInputdeviceItemObject(FortiObject[SdwanServiceInputdeviceItem]):
    """Typed object for service.input-device table items with attribute access."""
    name: str


class SdwanServiceInputzoneItemObject(FortiObject[SdwanServiceInputzoneItem]):
    """Typed object for service.input-zone table items with attribute access."""
    name: str


class SdwanServiceDstItemObject(FortiObject[SdwanServiceDstItem]):
    """Typed object for service.dst table items with attribute access."""
    name: str


class SdwanServiceSrcItemObject(FortiObject[SdwanServiceSrcItem]):
    """Typed object for service.src table items with attribute access."""
    name: str


class SdwanServiceDst6ItemObject(FortiObject[SdwanServiceDst6Item]):
    """Typed object for service.dst6 table items with attribute access."""
    name: str


class SdwanServiceSrc6ItemObject(FortiObject[SdwanServiceSrc6Item]):
    """Typed object for service.src6 table items with attribute access."""
    name: str


class SdwanServiceUsersItemObject(FortiObject[SdwanServiceUsersItem]):
    """Typed object for service.users table items with attribute access."""
    name: str


class SdwanServiceGroupsItemObject(FortiObject[SdwanServiceGroupsItem]):
    """Typed object for service.groups table items with attribute access."""
    name: str


class SdwanServiceInternetservicecustomItemObject(FortiObject[SdwanServiceInternetservicecustomItem]):
    """Typed object for service.internet-service-custom table items with attribute access."""
    name: str


class SdwanServiceInternetservicecustomgroupItemObject(FortiObject[SdwanServiceInternetservicecustomgroupItem]):
    """Typed object for service.internet-service-custom-group table items with attribute access."""
    name: str


class SdwanServiceInternetservicefortiguardItemObject(FortiObject[SdwanServiceInternetservicefortiguardItem]):
    """Typed object for service.internet-service-fortiguard table items with attribute access."""
    name: str


class SdwanServiceInternetservicenameItemObject(FortiObject[SdwanServiceInternetservicenameItem]):
    """Typed object for service.internet-service-name table items with attribute access."""
    name: str


class SdwanServiceInternetservicegroupItemObject(FortiObject[SdwanServiceInternetservicegroupItem]):
    """Typed object for service.internet-service-group table items with attribute access."""
    name: str


class SdwanServiceInternetserviceappctrlItemObject(FortiObject[SdwanServiceInternetserviceappctrlItem]):
    """Typed object for service.internet-service-app-ctrl table items with attribute access."""
    id: int


class SdwanServiceInternetserviceappctrlgroupItemObject(FortiObject[SdwanServiceInternetserviceappctrlgroupItem]):
    """Typed object for service.internet-service-app-ctrl-group table items with attribute access."""
    name: str


class SdwanServiceInternetserviceappctrlcategoryItemObject(FortiObject[SdwanServiceInternetserviceappctrlcategoryItem]):
    """Typed object for service.internet-service-app-ctrl-category table items with attribute access."""
    id: int


class SdwanServiceHealthcheckItemObject(FortiObject[SdwanServiceHealthcheckItem]):
    """Typed object for service.health-check table items with attribute access."""
    name: str


class SdwanServiceSlaItemObject(FortiObject[SdwanServiceSlaItem]):
    """Typed object for service.sla table items with attribute access."""
    health_check: str
    id: int


class SdwanServicePrioritymembersItemObject(FortiObject[SdwanServicePrioritymembersItem]):
    """Typed object for service.priority-members table items with attribute access."""
    seq_num: int


class SdwanServicePriorityzoneItemObject(FortiObject[SdwanServicePriorityzoneItem]):
    """Typed object for service.priority-zone table items with attribute access."""
    name: str


class SdwanNeighborMemberItemObject(FortiObject[SdwanNeighborMemberItem]):
    """Typed object for neighbor.member table items with attribute access."""
    seq_num: int


class SdwanDuplicationServiceidItemObject(FortiObject[SdwanDuplicationServiceidItem]):
    """Typed object for duplication.service-id table items with attribute access."""
    id: int


class SdwanDuplicationSrcaddrItemObject(FortiObject[SdwanDuplicationSrcaddrItem]):
    """Typed object for duplication.srcaddr table items with attribute access."""
    name: str


class SdwanDuplicationDstaddrItemObject(FortiObject[SdwanDuplicationDstaddrItem]):
    """Typed object for duplication.dstaddr table items with attribute access."""
    name: str


class SdwanDuplicationSrcaddr6ItemObject(FortiObject[SdwanDuplicationSrcaddr6Item]):
    """Typed object for duplication.srcaddr6 table items with attribute access."""
    name: str


class SdwanDuplicationDstaddr6ItemObject(FortiObject[SdwanDuplicationDstaddr6Item]):
    """Typed object for duplication.dstaddr6 table items with attribute access."""
    name: str


class SdwanDuplicationSrcintfItemObject(FortiObject[SdwanDuplicationSrcintfItem]):
    """Typed object for duplication.srcintf table items with attribute access."""
    name: str


class SdwanDuplicationDstintfItemObject(FortiObject[SdwanDuplicationDstintfItem]):
    """Typed object for duplication.dstintf table items with attribute access."""
    name: str


class SdwanDuplicationServiceItemObject(FortiObject[SdwanDuplicationServiceItem]):
    """Typed object for duplication.service table items with attribute access."""
    name: str


class SdwanFailalertinterfacesItemObject(FortiObject[SdwanFailalertinterfacesItem]):
    """Typed object for fail-alert-interfaces table items with attribute access."""
    name: str


class SdwanZoneItemObject(FortiObject[SdwanZoneItem]):
    """Typed object for zone table items with attribute access."""
    name: str
    advpn_select: Literal["enable", "disable"]
    advpn_health_check: str
    service_sla_tie_break: Literal["cfg-order", "fib-best-match", "priority", "input-device"]
    minimum_sla_meet_members: int


class SdwanMembersItemObject(FortiObject[SdwanMembersItem]):
    """Typed object for members table items with attribute access."""
    seq_num: int
    interface: str
    zone: str
    gateway: str
    preferred_source: str
    source: str
    gateway6: str
    source6: str
    cost: int
    weight: int
    priority: int
    priority6: int
    priority_in_sla: int
    priority_out_sla: int
    spillover_threshold: int
    ingress_spillover_threshold: int
    volume_ratio: int
    status: Literal["disable", "enable"]
    transport_group: int
    comment: str


class SdwanHealthcheckItemObject(FortiObject[SdwanHealthcheckItem]):
    """Typed object for health-check table items with attribute access."""
    name: str
    fortiguard: Literal["disable", "enable"]
    fortiguard_name: str
    probe_packets: Literal["disable", "enable"]
    addr_mode: Literal["ipv4", "ipv6"]
    system_dns: Literal["disable", "enable"]
    server: str | list[str]
    detect_mode: Literal["active", "passive", "prefer-passive", "remote", "agent-based"]
    protocol: Literal["ping", "tcp-echo", "udp-echo", "http", "https", "twamp", "dns", "tcp-connect", "ftp"]
    port: int
    quality_measured_method: Literal["half-open", "half-close"]
    security_mode: Literal["none", "authentication"]
    user: str
    password: str
    packet_size: int
    ha_priority: int
    ftp_mode: Literal["passive", "port"]
    ftp_file: str
    http_get: str
    http_agent: str
    http_match: str
    dns_request_domain: str
    dns_match_ip: str
    interval: int
    probe_timeout: int
    agent_probe_timeout: int
    remote_probe_timeout: int
    failtime: int
    recoverytime: int
    probe_count: int
    diffservcode: str
    update_cascade_interface: Literal["enable", "disable"]
    update_static_route: Literal["enable", "disable"]
    update_bgp_route: Literal["enable", "disable"]
    embed_measured_health: Literal["enable", "disable"]
    sla_id_redistribute: int
    sla_fail_log_period: int
    sla_pass_log_period: int
    threshold_warning_packetloss: int
    threshold_alert_packetloss: int
    threshold_warning_latency: int
    threshold_alert_latency: int
    threshold_warning_jitter: int
    threshold_alert_jitter: int
    vrf: int
    source: str
    source6: str
    members: FortiObjectList[SdwanHealthcheckMembersItemObject]
    mos_codec: Literal["g711", "g722", "g729"]
    class_id: int
    packet_loss_weight: int
    latency_weight: int
    jitter_weight: int
    bandwidth_weight: int
    sla: FortiObjectList[SdwanHealthcheckSlaItemObject]


class SdwanServiceItemObject(FortiObject[SdwanServiceItem]):
    """Typed object for service table items with attribute access."""
    id: int
    name: str
    addr_mode: Literal["ipv4", "ipv6"]
    load_balance: Literal["enable", "disable"]
    input_device: FortiObjectList[SdwanServiceInputdeviceItemObject]
    input_device_negate: Literal["enable", "disable"]
    input_zone: FortiObjectList[SdwanServiceInputzoneItemObject]
    mode: Literal["auto", "manual", "priority", "sla"]
    zone_mode: Literal["enable", "disable"]
    minimum_sla_meet_members: int
    hash_mode: Literal["round-robin", "source-ip-based", "source-dest-ip-based", "inbandwidth", "outbandwidth", "bibandwidth"]
    shortcut_priority: Literal["enable", "disable", "auto"]
    role: Literal["standalone", "primary", "secondary"]
    standalone_action: Literal["enable", "disable"]
    quality_link: int
    tos: str
    tos_mask: str
    protocol: int
    start_port: int
    end_port: int
    start_src_port: int
    end_src_port: int
    dst: FortiObjectList[SdwanServiceDstItemObject]
    dst_negate: Literal["enable", "disable"]
    src: FortiObjectList[SdwanServiceSrcItemObject]
    dst6: FortiObjectList[SdwanServiceDst6ItemObject]
    src6: FortiObjectList[SdwanServiceSrc6ItemObject]
    src_negate: Literal["enable", "disable"]
    users: FortiObjectList[SdwanServiceUsersItemObject]
    groups: FortiObjectList[SdwanServiceGroupsItemObject]
    internet_service: Literal["enable", "disable"]
    internet_service_custom: FortiObjectList[SdwanServiceInternetservicecustomItemObject]
    internet_service_custom_group: FortiObjectList[SdwanServiceInternetservicecustomgroupItemObject]
    internet_service_fortiguard: FortiObjectList[SdwanServiceInternetservicefortiguardItemObject]
    internet_service_name: FortiObjectList[SdwanServiceInternetservicenameItemObject]
    internet_service_group: FortiObjectList[SdwanServiceInternetservicegroupItemObject]
    internet_service_app_ctrl: FortiObjectList[SdwanServiceInternetserviceappctrlItemObject]
    internet_service_app_ctrl_group: FortiObjectList[SdwanServiceInternetserviceappctrlgroupItemObject]
    internet_service_app_ctrl_category: FortiObjectList[SdwanServiceInternetserviceappctrlcategoryItemObject]
    health_check: FortiObjectList[SdwanServiceHealthcheckItemObject]
    link_cost_factor: Literal["latency", "jitter", "packet-loss", "inbandwidth", "outbandwidth", "bibandwidth", "custom-profile-1"]
    packet_loss_weight: int
    latency_weight: int
    jitter_weight: int
    bandwidth_weight: int
    link_cost_threshold: int
    hold_down_time: int
    sla_stickiness: Literal["enable", "disable"]
    dscp_forward: Literal["enable", "disable"]
    dscp_reverse: Literal["enable", "disable"]
    dscp_forward_tag: str
    dscp_reverse_tag: str
    sla: FortiObjectList[SdwanServiceSlaItemObject]
    priority_members: FortiObjectList[SdwanServicePrioritymembersItemObject]
    priority_zone: FortiObjectList[SdwanServicePriorityzoneItemObject]
    status: Literal["enable", "disable"]
    gateway: Literal["enable", "disable"]
    default: Literal["enable", "disable"]
    sla_compare_method: Literal["order", "number"]
    fib_best_match_force: Literal["disable", "enable"]
    tie_break: Literal["zone", "cfg-order", "fib-best-match", "priority", "input-device"]
    use_shortcut_sla: Literal["enable", "disable"]
    passive_measurement: Literal["enable", "disable"]
    agent_exclusive: Literal["enable", "disable"]
    shortcut: Literal["enable", "disable"]
    comment: str


class SdwanNeighborItemObject(FortiObject[SdwanNeighborItem]):
    """Typed object for neighbor table items with attribute access."""
    ip: str
    member: FortiObjectList[SdwanNeighborMemberItemObject]
    service_id: int
    minimum_sla_meet_members: int
    mode: Literal["sla", "speedtest"]
    role: Literal["standalone", "primary", "secondary"]
    route_metric: Literal["preferable", "priority"]
    health_check: str
    sla_id: int


class SdwanDuplicationItemObject(FortiObject[SdwanDuplicationItem]):
    """Typed object for duplication table items with attribute access."""
    id: int
    service_id: FortiObjectList[SdwanDuplicationServiceidItemObject]
    srcaddr: FortiObjectList[SdwanDuplicationSrcaddrItemObject]
    dstaddr: FortiObjectList[SdwanDuplicationDstaddrItemObject]
    srcaddr6: FortiObjectList[SdwanDuplicationSrcaddr6ItemObject]
    dstaddr6: FortiObjectList[SdwanDuplicationDstaddr6ItemObject]
    srcintf: FortiObjectList[SdwanDuplicationSrcintfItemObject]
    dstintf: FortiObjectList[SdwanDuplicationDstintfItemObject]
    service: FortiObjectList[SdwanDuplicationServiceItemObject]
    packet_duplication: Literal["disable", "force", "on-demand"]
    sla_match_service: Literal["enable", "disable"]
    packet_de_duplication: Literal["enable", "disable"]


class SdwanObject(FortiObject):
    """Typed FortiObject for Sdwan with field access."""
    status: Literal["disable", "enable"]
    load_balance_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based", "measured-volume-based"]
    speedtest_bypass_routing: Literal["disable", "enable"]
    duplication_max_num: int
    duplication_max_discrepancy: int
    neighbor_hold_down: Literal["enable", "disable"]
    neighbor_hold_down_time: int
    app_perf_log_period: int
    neighbor_hold_boot_time: int
    fail_detect: Literal["enable", "disable"]
    fail_alert_interfaces: FortiObjectList[SdwanFailalertinterfacesItemObject]
    zone: FortiObjectList[SdwanZoneItemObject]
    members: FortiObjectList[SdwanMembersItemObject]
    health_check: FortiObjectList[SdwanHealthcheckItemObject]
    service: FortiObjectList[SdwanServiceItemObject]
    neighbor: FortiObjectList[SdwanNeighborItemObject]
    duplication: FortiObjectList[SdwanDuplicationItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Sdwan:
    """
    
    Endpoint: system/sdwan
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
    ) -> SdwanObject: ...
    
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
        payload_dict: SdwanPayload | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        load_balance_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based", "measured-volume-based"] | None = ...,
        speedtest_bypass_routing: Literal["disable", "enable"] | None = ...,
        duplication_max_num: int | None = ...,
        duplication_max_discrepancy: int | None = ...,
        neighbor_hold_down: Literal["enable", "disable"] | None = ...,
        neighbor_hold_down_time: int | None = ...,
        app_perf_log_period: int | None = ...,
        neighbor_hold_boot_time: int | None = ...,
        fail_detect: Literal["enable", "disable"] | None = ...,
        fail_alert_interfaces: str | list[str] | list[SdwanFailalertinterfacesItem] | None = ...,
        zone: str | list[str] | list[SdwanZoneItem] | None = ...,
        members: str | list[str] | list[SdwanMembersItem] | None = ...,
        health_check: str | list[str] | list[SdwanHealthcheckItem] | None = ...,
        service: str | list[str] | list[SdwanServiceItem] | None = ...,
        neighbor: str | list[str] | list[SdwanNeighborItem] | None = ...,
        duplication: str | list[str] | list[SdwanDuplicationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SdwanObject: ...


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
        payload_dict: SdwanPayload | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        load_balance_mode: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based", "measured-volume-based"] | None = ...,
        speedtest_bypass_routing: Literal["disable", "enable"] | None = ...,
        duplication_max_num: int | None = ...,
        duplication_max_discrepancy: int | None = ...,
        neighbor_hold_down: Literal["enable", "disable"] | None = ...,
        neighbor_hold_down_time: int | None = ...,
        app_perf_log_period: int | None = ...,
        neighbor_hold_boot_time: int | None = ...,
        fail_detect: Literal["enable", "disable"] | None = ...,
        fail_alert_interfaces: str | list[str] | list[SdwanFailalertinterfacesItem] | None = ...,
        zone: str | list[str] | list[SdwanZoneItem] | None = ...,
        members: str | list[str] | list[SdwanMembersItem] | None = ...,
        health_check: str | list[str] | list[SdwanHealthcheckItem] | None = ...,
        service: str | list[str] | list[SdwanServiceItem] | None = ...,
        neighbor: str | list[str] | list[SdwanNeighborItem] | None = ...,
        duplication: str | list[str] | list[SdwanDuplicationItem] | None = ...,
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
    "Sdwan",
    "SdwanPayload",
    "SdwanResponse",
    "SdwanObject",
]