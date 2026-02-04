""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/policy
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

class PolicySrcintfItem(TypedDict, total=False):
    """Nested item for srcintf field."""
    name: str


class PolicyDstintfItem(TypedDict, total=False):
    """Nested item for dstintf field."""
    name: str


class PolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class PolicyDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class PolicySrcaddr6Item(TypedDict, total=False):
    """Nested item for srcaddr6 field."""
    name: str


class PolicyDstaddr6Item(TypedDict, total=False):
    """Nested item for dstaddr6 field."""
    name: str


class PolicyZtnaemstagItem(TypedDict, total=False):
    """Nested item for ztna-ems-tag field."""
    name: str


class PolicyZtnaemstagsecondaryItem(TypedDict, total=False):
    """Nested item for ztna-ems-tag-secondary field."""
    name: str


class PolicyZtnageotagItem(TypedDict, total=False):
    """Nested item for ztna-geo-tag field."""
    name: str


class PolicyInternetservicenameItem(TypedDict, total=False):
    """Nested item for internet-service-name field."""
    name: str


class PolicyInternetservicegroupItem(TypedDict, total=False):
    """Nested item for internet-service-group field."""
    name: str


class PolicyInternetservicecustomItem(TypedDict, total=False):
    """Nested item for internet-service-custom field."""
    name: str


class PolicyNetworkservicedynamicItem(TypedDict, total=False):
    """Nested item for network-service-dynamic field."""
    name: str


class PolicyInternetservicecustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service-custom-group field."""
    name: str


class PolicyInternetservicesrcnameItem(TypedDict, total=False):
    """Nested item for internet-service-src-name field."""
    name: str


class PolicyInternetservicesrcgroupItem(TypedDict, total=False):
    """Nested item for internet-service-src-group field."""
    name: str


class PolicyInternetservicesrccustomItem(TypedDict, total=False):
    """Nested item for internet-service-src-custom field."""
    name: str


class PolicyNetworkservicesrcdynamicItem(TypedDict, total=False):
    """Nested item for network-service-src-dynamic field."""
    name: str


class PolicyInternetservicesrccustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service-src-custom-group field."""
    name: str


class PolicySrcvendormacItem(TypedDict, total=False):
    """Nested item for src-vendor-mac field."""
    id: int


class PolicyInternetservice6nameItem(TypedDict, total=False):
    """Nested item for internet-service6-name field."""
    name: str


class PolicyInternetservice6groupItem(TypedDict, total=False):
    """Nested item for internet-service6-group field."""
    name: str


class PolicyInternetservice6customItem(TypedDict, total=False):
    """Nested item for internet-service6-custom field."""
    name: str


class PolicyInternetservice6customgroupItem(TypedDict, total=False):
    """Nested item for internet-service6-custom-group field."""
    name: str


class PolicyInternetservice6srcnameItem(TypedDict, total=False):
    """Nested item for internet-service6-src-name field."""
    name: str


class PolicyInternetservice6srcgroupItem(TypedDict, total=False):
    """Nested item for internet-service6-src-group field."""
    name: str


class PolicyInternetservice6srccustomItem(TypedDict, total=False):
    """Nested item for internet-service6-src-custom field."""
    name: str


class PolicyInternetservice6srccustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service6-src-custom-group field."""
    name: str


class PolicyRtpaddrItem(TypedDict, total=False):
    """Nested item for rtp-addr field."""
    name: str


class PolicyServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class PolicyPcppoolnameItem(TypedDict, total=False):
    """Nested item for pcp-poolname field."""
    name: str


class PolicyPoolnameItem(TypedDict, total=False):
    """Nested item for poolname field."""
    name: str


class PolicyPoolname6Item(TypedDict, total=False):
    """Nested item for poolname6 field."""
    name: str


class PolicyNtlmenabledbrowsersItem(TypedDict, total=False):
    """Nested item for ntlm-enabled-browsers field."""
    user_agent_string: str


class PolicyGroupsItem(TypedDict, total=False):
    """Nested item for groups field."""
    name: str


class PolicyUsersItem(TypedDict, total=False):
    """Nested item for users field."""
    name: str


class PolicyFssogroupsItem(TypedDict, total=False):
    """Nested item for fsso-groups field."""
    name: str


class PolicyCustomlogfieldsItem(TypedDict, total=False):
    """Nested item for custom-log-fields field."""
    field_id: str


class PolicySgtItem(TypedDict, total=False):
    """Nested item for sgt field."""
    id: int


class PolicyInternetservicefortiguardItem(TypedDict, total=False):
    """Nested item for internet-service-fortiguard field."""
    name: str


class PolicyInternetservicesrcfortiguardItem(TypedDict, total=False):
    """Nested item for internet-service-src-fortiguard field."""
    name: str


class PolicyInternetservice6fortiguardItem(TypedDict, total=False):
    """Nested item for internet-service6-fortiguard field."""
    name: str


class PolicyInternetservice6srcfortiguardItem(TypedDict, total=False):
    """Nested item for internet-service6-src-fortiguard field."""
    name: str


class PolicyPayload(TypedDict, total=False):
    """Payload type for Policy operations."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    uuid: str
    srcintf: str | list[str] | list[PolicySrcintfItem]
    dstintf: str | list[str] | list[PolicyDstintfItem]
    action: Literal["accept", "deny", "ipsec"]
    nat64: Literal["enable", "disable"]
    nat46: Literal["enable", "disable"]
    ztna_status: Literal["enable", "disable"]
    ztna_device_ownership: Literal["enable", "disable"]
    srcaddr: str | list[str] | list[PolicySrcaddrItem]
    dstaddr: str | list[str] | list[PolicyDstaddrItem]
    srcaddr6: str | list[str] | list[PolicySrcaddr6Item]
    dstaddr6: str | list[str] | list[PolicyDstaddr6Item]
    ztna_ems_tag: str | list[str] | list[PolicyZtnaemstagItem]
    ztna_ems_tag_secondary: str | list[str] | list[PolicyZtnaemstagsecondaryItem]
    ztna_tags_match_logic: Literal["or", "and"]
    ztna_geo_tag: str | list[str] | list[PolicyZtnageotagItem]
    internet_service: Literal["enable", "disable"]
    internet_service_name: str | list[str] | list[PolicyInternetservicenameItem]
    internet_service_group: str | list[str] | list[PolicyInternetservicegroupItem]
    internet_service_custom: str | list[str] | list[PolicyInternetservicecustomItem]
    network_service_dynamic: str | list[str] | list[PolicyNetworkservicedynamicItem]
    internet_service_custom_group: str | list[str] | list[PolicyInternetservicecustomgroupItem]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: str | list[str] | list[PolicyInternetservicesrcnameItem]
    internet_service_src_group: str | list[str] | list[PolicyInternetservicesrcgroupItem]
    internet_service_src_custom: str | list[str] | list[PolicyInternetservicesrccustomItem]
    network_service_src_dynamic: str | list[str] | list[PolicyNetworkservicesrcdynamicItem]
    internet_service_src_custom_group: str | list[str] | list[PolicyInternetservicesrccustomgroupItem]
    reputation_minimum: int
    reputation_direction: Literal["source", "destination"]
    src_vendor_mac: str | list[str] | list[PolicySrcvendormacItem]
    internet_service6: Literal["enable", "disable"]
    internet_service6_name: str | list[str] | list[PolicyInternetservice6nameItem]
    internet_service6_group: str | list[str] | list[PolicyInternetservice6groupItem]
    internet_service6_custom: str | list[str] | list[PolicyInternetservice6customItem]
    internet_service6_custom_group: str | list[str] | list[PolicyInternetservice6customgroupItem]
    internet_service6_src: Literal["enable", "disable"]
    internet_service6_src_name: str | list[str] | list[PolicyInternetservice6srcnameItem]
    internet_service6_src_group: str | list[str] | list[PolicyInternetservice6srcgroupItem]
    internet_service6_src_custom: str | list[str] | list[PolicyInternetservice6srccustomItem]
    internet_service6_src_custom_group: str | list[str] | list[PolicyInternetservice6srccustomgroupItem]
    reputation_minimum6: int
    reputation_direction6: Literal["source", "destination"]
    rtp_nat: Literal["disable", "enable"]
    rtp_addr: str | list[str] | list[PolicyRtpaddrItem]
    send_deny_packet: Literal["disable", "enable"]
    firewall_session_dirty: Literal["check-all", "check-new"]
    schedule: str
    schedule_timeout: Literal["enable", "disable"]
    policy_expiry: Literal["enable", "disable"]
    policy_expiry_date: str
    policy_expiry_date_utc: str
    service: str | list[str] | list[PolicyServiceItem]
    tos_mask: str
    tos: str
    tos_negate: Literal["enable", "disable"]
    anti_replay: Literal["enable", "disable"]
    tcp_session_without_syn: Literal["all", "data-only", "disable"]
    geoip_anycast: Literal["enable", "disable"]
    geoip_match: Literal["physical-location", "registered-location"]
    dynamic_shaping: Literal["enable", "disable"]
    passive_wan_health_measurement: Literal["enable", "disable"]
    app_monitor: Literal["enable", "disable"]
    utm_status: Literal["enable", "disable"]
    inspection_mode: Literal["proxy", "flow"]
    http_policy_redirect: Literal["enable", "disable", "legacy"]
    ssh_policy_redirect: Literal["enable", "disable"]
    ztna_policy_redirect: Literal["enable", "disable"]
    webproxy_profile: str
    profile_type: Literal["single", "group"]
    profile_group: str
    profile_protocol_options: str
    ssl_ssh_profile: str
    av_profile: str
    webfilter_profile: str
    dnsfilter_profile: str
    emailfilter_profile: str
    dlp_profile: str
    file_filter_profile: str
    ips_sensor: str
    application_list: str
    voip_profile: str
    ips_voip_filter: str
    sctp_filter_profile: str
    diameter_filter_profile: str
    virtual_patch_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str
    logtraffic: Literal["all", "utm", "disable"]
    logtraffic_start: Literal["enable", "disable"]
    log_http_transaction: Literal["enable", "disable"]
    capture_packet: Literal["enable", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    wanopt: Literal["enable", "disable"]
    wanopt_detection: Literal["active", "passive", "off"]
    wanopt_passive_opt: Literal["default", "transparent", "non-transparent"]
    wanopt_profile: str
    wanopt_peer: str
    webcache: Literal["enable", "disable"]
    webcache_https: Literal["disable", "enable"]
    webproxy_forward_server: str
    traffic_shaper: str
    traffic_shaper_reverse: str
    per_ip_shaper: str
    nat: Literal["enable", "disable"]
    pcp_outbound: Literal["enable", "disable"]
    pcp_inbound: Literal["enable", "disable"]
    pcp_poolname: str | list[str] | list[PolicyPcppoolnameItem]
    permit_any_host: Literal["enable", "disable"]
    permit_stun_host: Literal["enable", "disable"]
    fixedport: Literal["enable", "disable"]
    port_preserve: Literal["enable", "disable"]
    port_random: Literal["enable", "disable"]
    ippool: Literal["enable", "disable"]
    poolname: str | list[str] | list[PolicyPoolnameItem]
    poolname6: str | list[str] | list[PolicyPoolname6Item]
    session_ttl: str
    vlan_cos_fwd: int
    vlan_cos_rev: int
    inbound: Literal["enable", "disable"]
    outbound: Literal["enable", "disable"]
    natinbound: Literal["enable", "disable"]
    natoutbound: Literal["enable", "disable"]
    fec: Literal["enable", "disable"]
    wccp: Literal["enable", "disable"]
    ntlm: Literal["enable", "disable"]
    ntlm_guest: Literal["enable", "disable"]
    ntlm_enabled_browsers: str | list[str] | list[PolicyNtlmenabledbrowsersItem]
    fsso_agent_for_ntlm: str
    groups: str | list[str] | list[PolicyGroupsItem]
    users: str | list[str] | list[PolicyUsersItem]
    fsso_groups: str | list[str] | list[PolicyFssogroupsItem]
    auth_path: Literal["enable", "disable"]
    disclaimer: Literal["enable", "disable"]
    email_collect: Literal["enable", "disable"]
    vpntunnel: str
    natip: str
    match_vip: Literal["enable", "disable"]
    match_vip_only: Literal["enable", "disable"]
    diffserv_copy: Literal["enable", "disable"]
    diffserv_forward: Literal["enable", "disable"]
    diffserv_reverse: Literal["enable", "disable"]
    diffservcode_forward: str
    diffservcode_rev: str
    tcp_mss_sender: int
    tcp_mss_receiver: int
    comments: str
    auth_cert: str
    auth_redirect_addr: str
    redirect_url: str
    identity_based_route: str
    block_notification: Literal["enable", "disable"]
    custom_log_fields: str | list[str] | list[PolicyCustomlogfieldsItem]
    replacemsg_override_group: str
    srcaddr_negate: Literal["enable", "disable"]
    srcaddr6_negate: Literal["enable", "disable"]
    dstaddr_negate: Literal["enable", "disable"]
    dstaddr6_negate: Literal["enable", "disable"]
    ztna_ems_tag_negate: Literal["enable", "disable"]
    service_negate: Literal["enable", "disable"]
    internet_service_negate: Literal["enable", "disable"]
    internet_service_src_negate: Literal["enable", "disable"]
    internet_service6_negate: Literal["enable", "disable"]
    internet_service6_src_negate: Literal["enable", "disable"]
    timeout_send_rst: Literal["enable", "disable"]
    captive_portal_exempt: Literal["enable", "disable"]
    decrypted_traffic_mirror: str
    dsri: Literal["enable", "disable"]
    radius_mac_auth_bypass: Literal["enable", "disable"]
    radius_ip_auth_bypass: Literal["enable", "disable"]
    delay_tcp_npu_session: Literal["enable", "disable"]
    vlan_filter: str
    sgt_check: Literal["enable", "disable"]
    sgt: str | list[str] | list[PolicySgtItem]
    internet_service_fortiguard: str | list[str] | list[PolicyInternetservicefortiguardItem]
    internet_service_src_fortiguard: str | list[str] | list[PolicyInternetservicesrcfortiguardItem]
    internet_service6_fortiguard: str | list[str] | list[PolicyInternetservice6fortiguardItem]
    internet_service6_src_fortiguard: str | list[str] | list[PolicyInternetservice6srcfortiguardItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PolicyResponse(TypedDict, total=False):
    """Response type for Policy - use with .dict property for typed dict access."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    uuid: str
    srcintf: list[PolicySrcintfItem]
    dstintf: list[PolicyDstintfItem]
    action: Literal["accept", "deny", "ipsec"]
    nat64: Literal["enable", "disable"]
    nat46: Literal["enable", "disable"]
    ztna_status: Literal["enable", "disable"]
    ztna_device_ownership: Literal["enable", "disable"]
    srcaddr: list[PolicySrcaddrItem]
    dstaddr: list[PolicyDstaddrItem]
    srcaddr6: list[PolicySrcaddr6Item]
    dstaddr6: list[PolicyDstaddr6Item]
    ztna_ems_tag: list[PolicyZtnaemstagItem]
    ztna_ems_tag_secondary: list[PolicyZtnaemstagsecondaryItem]
    ztna_tags_match_logic: Literal["or", "and"]
    ztna_geo_tag: list[PolicyZtnageotagItem]
    internet_service: Literal["enable", "disable"]
    internet_service_name: list[PolicyInternetservicenameItem]
    internet_service_group: list[PolicyInternetservicegroupItem]
    internet_service_custom: list[PolicyInternetservicecustomItem]
    network_service_dynamic: list[PolicyNetworkservicedynamicItem]
    internet_service_custom_group: list[PolicyInternetservicecustomgroupItem]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: list[PolicyInternetservicesrcnameItem]
    internet_service_src_group: list[PolicyInternetservicesrcgroupItem]
    internet_service_src_custom: list[PolicyInternetservicesrccustomItem]
    network_service_src_dynamic: list[PolicyNetworkservicesrcdynamicItem]
    internet_service_src_custom_group: list[PolicyInternetservicesrccustomgroupItem]
    reputation_minimum: int
    reputation_direction: Literal["source", "destination"]
    src_vendor_mac: list[PolicySrcvendormacItem]
    internet_service6: Literal["enable", "disable"]
    internet_service6_name: list[PolicyInternetservice6nameItem]
    internet_service6_group: list[PolicyInternetservice6groupItem]
    internet_service6_custom: list[PolicyInternetservice6customItem]
    internet_service6_custom_group: list[PolicyInternetservice6customgroupItem]
    internet_service6_src: Literal["enable", "disable"]
    internet_service6_src_name: list[PolicyInternetservice6srcnameItem]
    internet_service6_src_group: list[PolicyInternetservice6srcgroupItem]
    internet_service6_src_custom: list[PolicyInternetservice6srccustomItem]
    internet_service6_src_custom_group: list[PolicyInternetservice6srccustomgroupItem]
    reputation_minimum6: int
    reputation_direction6: Literal["source", "destination"]
    rtp_nat: Literal["disable", "enable"]
    rtp_addr: list[PolicyRtpaddrItem]
    send_deny_packet: Literal["disable", "enable"]
    firewall_session_dirty: Literal["check-all", "check-new"]
    schedule: str
    schedule_timeout: Literal["enable", "disable"]
    policy_expiry: Literal["enable", "disable"]
    policy_expiry_date: str
    policy_expiry_date_utc: str
    service: list[PolicyServiceItem]
    tos_mask: str
    tos: str
    tos_negate: Literal["enable", "disable"]
    anti_replay: Literal["enable", "disable"]
    tcp_session_without_syn: Literal["all", "data-only", "disable"]
    geoip_anycast: Literal["enable", "disable"]
    geoip_match: Literal["physical-location", "registered-location"]
    dynamic_shaping: Literal["enable", "disable"]
    passive_wan_health_measurement: Literal["enable", "disable"]
    app_monitor: Literal["enable", "disable"]
    utm_status: Literal["enable", "disable"]
    inspection_mode: Literal["proxy", "flow"]
    http_policy_redirect: Literal["enable", "disable", "legacy"]
    ssh_policy_redirect: Literal["enable", "disable"]
    ztna_policy_redirect: Literal["enable", "disable"]
    webproxy_profile: str
    profile_type: Literal["single", "group"]
    profile_group: str
    profile_protocol_options: str
    ssl_ssh_profile: str
    av_profile: str
    webfilter_profile: str
    dnsfilter_profile: str
    emailfilter_profile: str
    dlp_profile: str
    file_filter_profile: str
    ips_sensor: str
    application_list: str
    voip_profile: str
    ips_voip_filter: str
    sctp_filter_profile: str
    diameter_filter_profile: str
    virtual_patch_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str
    logtraffic: Literal["all", "utm", "disable"]
    logtraffic_start: Literal["enable", "disable"]
    log_http_transaction: Literal["enable", "disable"]
    capture_packet: Literal["enable", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    wanopt: Literal["enable", "disable"]
    wanopt_detection: Literal["active", "passive", "off"]
    wanopt_passive_opt: Literal["default", "transparent", "non-transparent"]
    wanopt_profile: str
    wanopt_peer: str
    webcache: Literal["enable", "disable"]
    webcache_https: Literal["disable", "enable"]
    webproxy_forward_server: str
    traffic_shaper: str
    traffic_shaper_reverse: str
    per_ip_shaper: str
    nat: Literal["enable", "disable"]
    pcp_outbound: Literal["enable", "disable"]
    pcp_inbound: Literal["enable", "disable"]
    pcp_poolname: list[PolicyPcppoolnameItem]
    permit_any_host: Literal["enable", "disable"]
    permit_stun_host: Literal["enable", "disable"]
    fixedport: Literal["enable", "disable"]
    port_preserve: Literal["enable", "disable"]
    port_random: Literal["enable", "disable"]
    ippool: Literal["enable", "disable"]
    poolname: list[PolicyPoolnameItem]
    poolname6: list[PolicyPoolname6Item]
    session_ttl: str
    vlan_cos_fwd: int
    vlan_cos_rev: int
    inbound: Literal["enable", "disable"]
    outbound: Literal["enable", "disable"]
    natinbound: Literal["enable", "disable"]
    natoutbound: Literal["enable", "disable"]
    fec: Literal["enable", "disable"]
    wccp: Literal["enable", "disable"]
    ntlm: Literal["enable", "disable"]
    ntlm_guest: Literal["enable", "disable"]
    ntlm_enabled_browsers: list[PolicyNtlmenabledbrowsersItem]
    fsso_agent_for_ntlm: str
    groups: list[PolicyGroupsItem]
    users: list[PolicyUsersItem]
    fsso_groups: list[PolicyFssogroupsItem]
    auth_path: Literal["enable", "disable"]
    disclaimer: Literal["enable", "disable"]
    email_collect: Literal["enable", "disable"]
    vpntunnel: str
    natip: str
    match_vip: Literal["enable", "disable"]
    match_vip_only: Literal["enable", "disable"]
    diffserv_copy: Literal["enable", "disable"]
    diffserv_forward: Literal["enable", "disable"]
    diffserv_reverse: Literal["enable", "disable"]
    diffservcode_forward: str
    diffservcode_rev: str
    tcp_mss_sender: int
    tcp_mss_receiver: int
    comments: str
    auth_cert: str
    auth_redirect_addr: str
    redirect_url: str
    identity_based_route: str
    block_notification: Literal["enable", "disable"]
    custom_log_fields: list[PolicyCustomlogfieldsItem]
    replacemsg_override_group: str
    srcaddr_negate: Literal["enable", "disable"]
    srcaddr6_negate: Literal["enable", "disable"]
    dstaddr_negate: Literal["enable", "disable"]
    dstaddr6_negate: Literal["enable", "disable"]
    ztna_ems_tag_negate: Literal["enable", "disable"]
    service_negate: Literal["enable", "disable"]
    internet_service_negate: Literal["enable", "disable"]
    internet_service_src_negate: Literal["enable", "disable"]
    internet_service6_negate: Literal["enable", "disable"]
    internet_service6_src_negate: Literal["enable", "disable"]
    timeout_send_rst: Literal["enable", "disable"]
    captive_portal_exempt: Literal["enable", "disable"]
    decrypted_traffic_mirror: str
    dsri: Literal["enable", "disable"]
    radius_mac_auth_bypass: Literal["enable", "disable"]
    radius_ip_auth_bypass: Literal["enable", "disable"]
    delay_tcp_npu_session: Literal["enable", "disable"]
    vlan_filter: str
    sgt_check: Literal["enable", "disable"]
    sgt: list[PolicySgtItem]
    internet_service_fortiguard: list[PolicyInternetservicefortiguardItem]
    internet_service_src_fortiguard: list[PolicyInternetservicesrcfortiguardItem]
    internet_service6_fortiguard: list[PolicyInternetservice6fortiguardItem]
    internet_service6_src_fortiguard: list[PolicyInternetservice6srcfortiguardItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PolicySrcintfItemObject(FortiObject[PolicySrcintfItem]):
    """Typed object for srcintf table items with attribute access."""
    name: str


class PolicyDstintfItemObject(FortiObject[PolicyDstintfItem]):
    """Typed object for dstintf table items with attribute access."""
    name: str


class PolicySrcaddrItemObject(FortiObject[PolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class PolicyDstaddrItemObject(FortiObject[PolicyDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class PolicySrcaddr6ItemObject(FortiObject[PolicySrcaddr6Item]):
    """Typed object for srcaddr6 table items with attribute access."""
    name: str


class PolicyDstaddr6ItemObject(FortiObject[PolicyDstaddr6Item]):
    """Typed object for dstaddr6 table items with attribute access."""
    name: str


class PolicyZtnaemstagItemObject(FortiObject[PolicyZtnaemstagItem]):
    """Typed object for ztna-ems-tag table items with attribute access."""
    name: str


class PolicyZtnaemstagsecondaryItemObject(FortiObject[PolicyZtnaemstagsecondaryItem]):
    """Typed object for ztna-ems-tag-secondary table items with attribute access."""
    name: str


class PolicyZtnageotagItemObject(FortiObject[PolicyZtnageotagItem]):
    """Typed object for ztna-geo-tag table items with attribute access."""
    name: str


class PolicyInternetservicenameItemObject(FortiObject[PolicyInternetservicenameItem]):
    """Typed object for internet-service-name table items with attribute access."""
    name: str


class PolicyInternetservicegroupItemObject(FortiObject[PolicyInternetservicegroupItem]):
    """Typed object for internet-service-group table items with attribute access."""
    name: str


class PolicyInternetservicecustomItemObject(FortiObject[PolicyInternetservicecustomItem]):
    """Typed object for internet-service-custom table items with attribute access."""
    name: str


class PolicyNetworkservicedynamicItemObject(FortiObject[PolicyNetworkservicedynamicItem]):
    """Typed object for network-service-dynamic table items with attribute access."""
    name: str


class PolicyInternetservicecustomgroupItemObject(FortiObject[PolicyInternetservicecustomgroupItem]):
    """Typed object for internet-service-custom-group table items with attribute access."""
    name: str


class PolicyInternetservicesrcnameItemObject(FortiObject[PolicyInternetservicesrcnameItem]):
    """Typed object for internet-service-src-name table items with attribute access."""
    name: str


class PolicyInternetservicesrcgroupItemObject(FortiObject[PolicyInternetservicesrcgroupItem]):
    """Typed object for internet-service-src-group table items with attribute access."""
    name: str


class PolicyInternetservicesrccustomItemObject(FortiObject[PolicyInternetservicesrccustomItem]):
    """Typed object for internet-service-src-custom table items with attribute access."""
    name: str


class PolicyNetworkservicesrcdynamicItemObject(FortiObject[PolicyNetworkservicesrcdynamicItem]):
    """Typed object for network-service-src-dynamic table items with attribute access."""
    name: str


class PolicyInternetservicesrccustomgroupItemObject(FortiObject[PolicyInternetservicesrccustomgroupItem]):
    """Typed object for internet-service-src-custom-group table items with attribute access."""
    name: str


class PolicySrcvendormacItemObject(FortiObject[PolicySrcvendormacItem]):
    """Typed object for src-vendor-mac table items with attribute access."""
    id: int


class PolicyInternetservice6nameItemObject(FortiObject[PolicyInternetservice6nameItem]):
    """Typed object for internet-service6-name table items with attribute access."""
    name: str


class PolicyInternetservice6groupItemObject(FortiObject[PolicyInternetservice6groupItem]):
    """Typed object for internet-service6-group table items with attribute access."""
    name: str


class PolicyInternetservice6customItemObject(FortiObject[PolicyInternetservice6customItem]):
    """Typed object for internet-service6-custom table items with attribute access."""
    name: str


class PolicyInternetservice6customgroupItemObject(FortiObject[PolicyInternetservice6customgroupItem]):
    """Typed object for internet-service6-custom-group table items with attribute access."""
    name: str


class PolicyInternetservice6srcnameItemObject(FortiObject[PolicyInternetservice6srcnameItem]):
    """Typed object for internet-service6-src-name table items with attribute access."""
    name: str


class PolicyInternetservice6srcgroupItemObject(FortiObject[PolicyInternetservice6srcgroupItem]):
    """Typed object for internet-service6-src-group table items with attribute access."""
    name: str


class PolicyInternetservice6srccustomItemObject(FortiObject[PolicyInternetservice6srccustomItem]):
    """Typed object for internet-service6-src-custom table items with attribute access."""
    name: str


class PolicyInternetservice6srccustomgroupItemObject(FortiObject[PolicyInternetservice6srccustomgroupItem]):
    """Typed object for internet-service6-src-custom-group table items with attribute access."""
    name: str


class PolicyRtpaddrItemObject(FortiObject[PolicyRtpaddrItem]):
    """Typed object for rtp-addr table items with attribute access."""
    name: str


class PolicyServiceItemObject(FortiObject[PolicyServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class PolicyPcppoolnameItemObject(FortiObject[PolicyPcppoolnameItem]):
    """Typed object for pcp-poolname table items with attribute access."""
    name: str


class PolicyPoolnameItemObject(FortiObject[PolicyPoolnameItem]):
    """Typed object for poolname table items with attribute access."""
    name: str


class PolicyPoolname6ItemObject(FortiObject[PolicyPoolname6Item]):
    """Typed object for poolname6 table items with attribute access."""
    name: str


class PolicyNtlmenabledbrowsersItemObject(FortiObject[PolicyNtlmenabledbrowsersItem]):
    """Typed object for ntlm-enabled-browsers table items with attribute access."""
    user_agent_string: str


class PolicyGroupsItemObject(FortiObject[PolicyGroupsItem]):
    """Typed object for groups table items with attribute access."""
    name: str


class PolicyUsersItemObject(FortiObject[PolicyUsersItem]):
    """Typed object for users table items with attribute access."""
    name: str


class PolicyFssogroupsItemObject(FortiObject[PolicyFssogroupsItem]):
    """Typed object for fsso-groups table items with attribute access."""
    name: str


class PolicyCustomlogfieldsItemObject(FortiObject[PolicyCustomlogfieldsItem]):
    """Typed object for custom-log-fields table items with attribute access."""
    field_id: str


class PolicySgtItemObject(FortiObject[PolicySgtItem]):
    """Typed object for sgt table items with attribute access."""
    id: int


class PolicyInternetservicefortiguardItemObject(FortiObject[PolicyInternetservicefortiguardItem]):
    """Typed object for internet-service-fortiguard table items with attribute access."""
    name: str


class PolicyInternetservicesrcfortiguardItemObject(FortiObject[PolicyInternetservicesrcfortiguardItem]):
    """Typed object for internet-service-src-fortiguard table items with attribute access."""
    name: str


class PolicyInternetservice6fortiguardItemObject(FortiObject[PolicyInternetservice6fortiguardItem]):
    """Typed object for internet-service6-fortiguard table items with attribute access."""
    name: str


class PolicyInternetservice6srcfortiguardItemObject(FortiObject[PolicyInternetservice6srcfortiguardItem]):
    """Typed object for internet-service6-src-fortiguard table items with attribute access."""
    name: str


class PolicyObject(FortiObject):
    """Typed FortiObject for Policy with field access."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    uuid: str
    srcintf: FortiObjectList[PolicySrcintfItemObject]
    dstintf: FortiObjectList[PolicyDstintfItemObject]
    action: Literal["accept", "deny", "ipsec"]
    nat64: Literal["enable", "disable"]
    nat46: Literal["enable", "disable"]
    ztna_status: Literal["enable", "disable"]
    ztna_device_ownership: Literal["enable", "disable"]
    srcaddr: FortiObjectList[PolicySrcaddrItemObject]
    dstaddr: FortiObjectList[PolicyDstaddrItemObject]
    srcaddr6: FortiObjectList[PolicySrcaddr6ItemObject]
    dstaddr6: FortiObjectList[PolicyDstaddr6ItemObject]
    ztna_ems_tag: FortiObjectList[PolicyZtnaemstagItemObject]
    ztna_ems_tag_secondary: FortiObjectList[PolicyZtnaemstagsecondaryItemObject]
    ztna_tags_match_logic: Literal["or", "and"]
    ztna_geo_tag: FortiObjectList[PolicyZtnageotagItemObject]
    internet_service: Literal["enable", "disable"]
    internet_service_name: FortiObjectList[PolicyInternetservicenameItemObject]
    internet_service_group: FortiObjectList[PolicyInternetservicegroupItemObject]
    internet_service_custom: FortiObjectList[PolicyInternetservicecustomItemObject]
    network_service_dynamic: FortiObjectList[PolicyNetworkservicedynamicItemObject]
    internet_service_custom_group: FortiObjectList[PolicyInternetservicecustomgroupItemObject]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: FortiObjectList[PolicyInternetservicesrcnameItemObject]
    internet_service_src_group: FortiObjectList[PolicyInternetservicesrcgroupItemObject]
    internet_service_src_custom: FortiObjectList[PolicyInternetservicesrccustomItemObject]
    network_service_src_dynamic: FortiObjectList[PolicyNetworkservicesrcdynamicItemObject]
    internet_service_src_custom_group: FortiObjectList[PolicyInternetservicesrccustomgroupItemObject]
    reputation_minimum: int
    reputation_direction: Literal["source", "destination"]
    src_vendor_mac: FortiObjectList[PolicySrcvendormacItemObject]
    internet_service6: Literal["enable", "disable"]
    internet_service6_name: FortiObjectList[PolicyInternetservice6nameItemObject]
    internet_service6_group: FortiObjectList[PolicyInternetservice6groupItemObject]
    internet_service6_custom: FortiObjectList[PolicyInternetservice6customItemObject]
    internet_service6_custom_group: FortiObjectList[PolicyInternetservice6customgroupItemObject]
    internet_service6_src: Literal["enable", "disable"]
    internet_service6_src_name: FortiObjectList[PolicyInternetservice6srcnameItemObject]
    internet_service6_src_group: FortiObjectList[PolicyInternetservice6srcgroupItemObject]
    internet_service6_src_custom: FortiObjectList[PolicyInternetservice6srccustomItemObject]
    internet_service6_src_custom_group: FortiObjectList[PolicyInternetservice6srccustomgroupItemObject]
    reputation_minimum6: int
    reputation_direction6: Literal["source", "destination"]
    rtp_nat: Literal["disable", "enable"]
    rtp_addr: FortiObjectList[PolicyRtpaddrItemObject]
    send_deny_packet: Literal["disable", "enable"]
    firewall_session_dirty: Literal["check-all", "check-new"]
    schedule: str
    schedule_timeout: Literal["enable", "disable"]
    policy_expiry: Literal["enable", "disable"]
    policy_expiry_date: str
    policy_expiry_date_utc: str
    service: FortiObjectList[PolicyServiceItemObject]
    tos_mask: str
    tos: str
    tos_negate: Literal["enable", "disable"]
    anti_replay: Literal["enable", "disable"]
    tcp_session_without_syn: Literal["all", "data-only", "disable"]
    geoip_anycast: Literal["enable", "disable"]
    geoip_match: Literal["physical-location", "registered-location"]
    dynamic_shaping: Literal["enable", "disable"]
    passive_wan_health_measurement: Literal["enable", "disable"]
    app_monitor: Literal["enable", "disable"]
    utm_status: Literal["enable", "disable"]
    inspection_mode: Literal["proxy", "flow"]
    http_policy_redirect: Literal["enable", "disable", "legacy"]
    ssh_policy_redirect: Literal["enable", "disable"]
    ztna_policy_redirect: Literal["enable", "disable"]
    webproxy_profile: str
    profile_type: Literal["single", "group"]
    profile_group: str
    profile_protocol_options: str
    ssl_ssh_profile: str
    av_profile: str
    webfilter_profile: str
    dnsfilter_profile: str
    emailfilter_profile: str
    dlp_profile: str
    file_filter_profile: str
    ips_sensor: str
    application_list: str
    voip_profile: str
    ips_voip_filter: str
    sctp_filter_profile: str
    diameter_filter_profile: str
    virtual_patch_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str
    logtraffic: Literal["all", "utm", "disable"]
    logtraffic_start: Literal["enable", "disable"]
    log_http_transaction: Literal["enable", "disable"]
    capture_packet: Literal["enable", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    wanopt: Literal["enable", "disable"]
    wanopt_detection: Literal["active", "passive", "off"]
    wanopt_passive_opt: Literal["default", "transparent", "non-transparent"]
    wanopt_profile: str
    wanopt_peer: str
    webcache: Literal["enable", "disable"]
    webcache_https: Literal["disable", "enable"]
    webproxy_forward_server: str
    traffic_shaper: str
    traffic_shaper_reverse: str
    per_ip_shaper: str
    nat: Literal["enable", "disable"]
    pcp_outbound: Literal["enable", "disable"]
    pcp_inbound: Literal["enable", "disable"]
    pcp_poolname: FortiObjectList[PolicyPcppoolnameItemObject]
    permit_any_host: Literal["enable", "disable"]
    permit_stun_host: Literal["enable", "disable"]
    fixedport: Literal["enable", "disable"]
    port_preserve: Literal["enable", "disable"]
    port_random: Literal["enable", "disable"]
    ippool: Literal["enable", "disable"]
    poolname: FortiObjectList[PolicyPoolnameItemObject]
    poolname6: FortiObjectList[PolicyPoolname6ItemObject]
    session_ttl: str
    vlan_cos_fwd: int
    vlan_cos_rev: int
    inbound: Literal["enable", "disable"]
    outbound: Literal["enable", "disable"]
    natinbound: Literal["enable", "disable"]
    natoutbound: Literal["enable", "disable"]
    fec: Literal["enable", "disable"]
    wccp: Literal["enable", "disable"]
    ntlm: Literal["enable", "disable"]
    ntlm_guest: Literal["enable", "disable"]
    ntlm_enabled_browsers: FortiObjectList[PolicyNtlmenabledbrowsersItemObject]
    fsso_agent_for_ntlm: str
    groups: FortiObjectList[PolicyGroupsItemObject]
    users: FortiObjectList[PolicyUsersItemObject]
    fsso_groups: FortiObjectList[PolicyFssogroupsItemObject]
    auth_path: Literal["enable", "disable"]
    disclaimer: Literal["enable", "disable"]
    email_collect: Literal["enable", "disable"]
    vpntunnel: str
    natip: str
    match_vip: Literal["enable", "disable"]
    match_vip_only: Literal["enable", "disable"]
    diffserv_copy: Literal["enable", "disable"]
    diffserv_forward: Literal["enable", "disable"]
    diffserv_reverse: Literal["enable", "disable"]
    diffservcode_forward: str
    diffservcode_rev: str
    tcp_mss_sender: int
    tcp_mss_receiver: int
    comments: str
    auth_cert: str
    auth_redirect_addr: str
    redirect_url: str
    identity_based_route: str
    block_notification: Literal["enable", "disable"]
    custom_log_fields: FortiObjectList[PolicyCustomlogfieldsItemObject]
    replacemsg_override_group: str
    srcaddr_negate: Literal["enable", "disable"]
    srcaddr6_negate: Literal["enable", "disable"]
    dstaddr_negate: Literal["enable", "disable"]
    dstaddr6_negate: Literal["enable", "disable"]
    ztna_ems_tag_negate: Literal["enable", "disable"]
    service_negate: Literal["enable", "disable"]
    internet_service_negate: Literal["enable", "disable"]
    internet_service_src_negate: Literal["enable", "disable"]
    internet_service6_negate: Literal["enable", "disable"]
    internet_service6_src_negate: Literal["enable", "disable"]
    timeout_send_rst: Literal["enable", "disable"]
    captive_portal_exempt: Literal["enable", "disable"]
    decrypted_traffic_mirror: str
    dsri: Literal["enable", "disable"]
    radius_mac_auth_bypass: Literal["enable", "disable"]
    radius_ip_auth_bypass: Literal["enable", "disable"]
    delay_tcp_npu_session: Literal["enable", "disable"]
    vlan_filter: str
    sgt_check: Literal["enable", "disable"]
    sgt: FortiObjectList[PolicySgtItemObject]
    internet_service_fortiguard: FortiObjectList[PolicyInternetservicefortiguardItemObject]
    internet_service_src_fortiguard: FortiObjectList[PolicyInternetservicesrcfortiguardItemObject]
    internet_service6_fortiguard: FortiObjectList[PolicyInternetservice6fortiguardItemObject]
    internet_service6_src_fortiguard: FortiObjectList[PolicyInternetservice6srcfortiguardItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Policy:
    """
    
    Endpoint: firewall/policy
    Category: cmdb
    MKey: policyid
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
        policyid: int,
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
    ) -> PolicyObject: ...
    
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
    ) -> FortiObjectList[PolicyObject]: ...
    
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
        payload_dict: PolicyPayload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        srcintf: str | list[str] | list[PolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[PolicyDstintfItem] | None = ...,
        action: Literal["accept", "deny", "ipsec"] | None = ...,
        nat64: Literal["enable", "disable"] | None = ...,
        nat46: Literal["enable", "disable"] | None = ...,
        ztna_status: Literal["enable", "disable"] | None = ...,
        ztna_device_ownership: Literal["enable", "disable"] | None = ...,
        srcaddr: str | list[str] | list[PolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[PolicyDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[PolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[PolicyDstaddr6Item] | None = ...,
        ztna_ems_tag: str | list[str] | list[PolicyZtnaemstagItem] | None = ...,
        ztna_ems_tag_secondary: str | list[str] | list[PolicyZtnaemstagsecondaryItem] | None = ...,
        ztna_tags_match_logic: Literal["or", "and"] | None = ...,
        ztna_geo_tag: str | list[str] | list[PolicyZtnageotagItem] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[PolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[PolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[PolicyInternetservicecustomItem] | None = ...,
        network_service_dynamic: str | list[str] | list[PolicyNetworkservicedynamicItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[PolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[PolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[PolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[PolicyInternetservicesrccustomItem] | None = ...,
        network_service_src_dynamic: str | list[str] | list[PolicyNetworkservicesrcdynamicItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[PolicyInternetservicesrccustomgroupItem] | None = ...,
        reputation_minimum: int | None = ...,
        reputation_direction: Literal["source", "destination"] | None = ...,
        src_vendor_mac: str | list[str] | list[PolicySrcvendormacItem] | None = ...,
        internet_service6: Literal["enable", "disable"] | None = ...,
        internet_service6_name: str | list[str] | list[PolicyInternetservice6nameItem] | None = ...,
        internet_service6_group: str | list[str] | list[PolicyInternetservice6groupItem] | None = ...,
        internet_service6_custom: str | list[str] | list[PolicyInternetservice6customItem] | None = ...,
        internet_service6_custom_group: str | list[str] | list[PolicyInternetservice6customgroupItem] | None = ...,
        internet_service6_src: Literal["enable", "disable"] | None = ...,
        internet_service6_src_name: str | list[str] | list[PolicyInternetservice6srcnameItem] | None = ...,
        internet_service6_src_group: str | list[str] | list[PolicyInternetservice6srcgroupItem] | None = ...,
        internet_service6_src_custom: str | list[str] | list[PolicyInternetservice6srccustomItem] | None = ...,
        internet_service6_src_custom_group: str | list[str] | list[PolicyInternetservice6srccustomgroupItem] | None = ...,
        reputation_minimum6: int | None = ...,
        reputation_direction6: Literal["source", "destination"] | None = ...,
        rtp_nat: Literal["disable", "enable"] | None = ...,
        rtp_addr: str | list[str] | list[PolicyRtpaddrItem] | None = ...,
        send_deny_packet: Literal["disable", "enable"] | None = ...,
        firewall_session_dirty: Literal["check-all", "check-new"] | None = ...,
        schedule: str | None = ...,
        schedule_timeout: Literal["enable", "disable"] | None = ...,
        policy_expiry: Literal["enable", "disable"] | None = ...,
        policy_expiry_date: str | None = ...,
        policy_expiry_date_utc: str | None = ...,
        service: str | list[str] | list[PolicyServiceItem] | None = ...,
        tos_mask: str | None = ...,
        tos: str | None = ...,
        tos_negate: Literal["enable", "disable"] | None = ...,
        anti_replay: Literal["enable", "disable"] | None = ...,
        tcp_session_without_syn: Literal["all", "data-only", "disable"] | None = ...,
        geoip_anycast: Literal["enable", "disable"] | None = ...,
        geoip_match: Literal["physical-location", "registered-location"] | None = ...,
        dynamic_shaping: Literal["enable", "disable"] | None = ...,
        passive_wan_health_measurement: Literal["enable", "disable"] | None = ...,
        app_monitor: Literal["enable", "disable"] | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        inspection_mode: Literal["proxy", "flow"] | None = ...,
        http_policy_redirect: Literal["enable", "disable", "legacy"] | None = ...,
        ssh_policy_redirect: Literal["enable", "disable"] | None = ...,
        ztna_policy_redirect: Literal["enable", "disable"] | None = ...,
        webproxy_profile: str | None = ...,
        profile_type: Literal["single", "group"] | None = ...,
        profile_group: str | None = ...,
        profile_protocol_options: str | None = ...,
        ssl_ssh_profile: str | None = ...,
        av_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        dnsfilter_profile: str | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile: str | None = ...,
        file_filter_profile: str | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        voip_profile: str | None = ...,
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        diameter_filter_profile: str | None = ...,
        virtual_patch_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        logtraffic_start: Literal["enable", "disable"] | None = ...,
        log_http_transaction: Literal["enable", "disable"] | None = ...,
        capture_packet: Literal["enable", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        wanopt: Literal["enable", "disable"] | None = ...,
        wanopt_detection: Literal["active", "passive", "off"] | None = ...,
        wanopt_passive_opt: Literal["default", "transparent", "non-transparent"] | None = ...,
        wanopt_profile: str | None = ...,
        wanopt_peer: str | None = ...,
        webcache: Literal["enable", "disable"] | None = ...,
        webcache_https: Literal["disable", "enable"] | None = ...,
        webproxy_forward_server: str | None = ...,
        traffic_shaper: str | None = ...,
        traffic_shaper_reverse: str | None = ...,
        per_ip_shaper: str | None = ...,
        nat: Literal["enable", "disable"] | None = ...,
        pcp_outbound: Literal["enable", "disable"] | None = ...,
        pcp_inbound: Literal["enable", "disable"] | None = ...,
        pcp_poolname: str | list[str] | list[PolicyPcppoolnameItem] | None = ...,
        permit_any_host: Literal["enable", "disable"] | None = ...,
        permit_stun_host: Literal["enable", "disable"] | None = ...,
        fixedport: Literal["enable", "disable"] | None = ...,
        port_preserve: Literal["enable", "disable"] | None = ...,
        port_random: Literal["enable", "disable"] | None = ...,
        ippool: Literal["enable", "disable"] | None = ...,
        poolname: str | list[str] | list[PolicyPoolnameItem] | None = ...,
        poolname6: str | list[str] | list[PolicyPoolname6Item] | None = ...,
        session_ttl: str | None = ...,
        vlan_cos_fwd: int | None = ...,
        vlan_cos_rev: int | None = ...,
        inbound: Literal["enable", "disable"] | None = ...,
        outbound: Literal["enable", "disable"] | None = ...,
        natinbound: Literal["enable", "disable"] | None = ...,
        natoutbound: Literal["enable", "disable"] | None = ...,
        fec: Literal["enable", "disable"] | None = ...,
        wccp: Literal["enable", "disable"] | None = ...,
        ntlm: Literal["enable", "disable"] | None = ...,
        ntlm_guest: Literal["enable", "disable"] | None = ...,
        ntlm_enabled_browsers: str | list[str] | list[PolicyNtlmenabledbrowsersItem] | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        groups: str | list[str] | list[PolicyGroupsItem] | None = ...,
        users: str | list[str] | list[PolicyUsersItem] | None = ...,
        fsso_groups: str | list[str] | list[PolicyFssogroupsItem] | None = ...,
        auth_path: Literal["enable", "disable"] | None = ...,
        disclaimer: Literal["enable", "disable"] | None = ...,
        email_collect: Literal["enable", "disable"] | None = ...,
        vpntunnel: str | None = ...,
        natip: str | None = ...,
        match_vip: Literal["enable", "disable"] | None = ...,
        match_vip_only: Literal["enable", "disable"] | None = ...,
        diffserv_copy: Literal["enable", "disable"] | None = ...,
        diffserv_forward: Literal["enable", "disable"] | None = ...,
        diffserv_reverse: Literal["enable", "disable"] | None = ...,
        diffservcode_forward: str | None = ...,
        diffservcode_rev: str | None = ...,
        tcp_mss_sender: int | None = ...,
        tcp_mss_receiver: int | None = ...,
        comments: str | None = ...,
        auth_cert: str | None = ...,
        auth_redirect_addr: str | None = ...,
        redirect_url: str | None = ...,
        identity_based_route: str | None = ...,
        block_notification: Literal["enable", "disable"] | None = ...,
        custom_log_fields: str | list[str] | list[PolicyCustomlogfieldsItem] | None = ...,
        replacemsg_override_group: str | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        srcaddr6_negate: Literal["enable", "disable"] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr6_negate: Literal["enable", "disable"] | None = ...,
        ztna_ems_tag_negate: Literal["enable", "disable"] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_src_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_src_negate: Literal["enable", "disable"] | None = ...,
        timeout_send_rst: Literal["enable", "disable"] | None = ...,
        captive_portal_exempt: Literal["enable", "disable"] | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        radius_mac_auth_bypass: Literal["enable", "disable"] | None = ...,
        radius_ip_auth_bypass: Literal["enable", "disable"] | None = ...,
        delay_tcp_npu_session: Literal["enable", "disable"] | None = ...,
        vlan_filter: str | None = ...,
        sgt_check: Literal["enable", "disable"] | None = ...,
        sgt: str | list[str] | list[PolicySgtItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[PolicyInternetservicefortiguardItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[PolicyInternetservicesrcfortiguardItem] | None = ...,
        internet_service6_fortiguard: str | list[str] | list[PolicyInternetservice6fortiguardItem] | None = ...,
        internet_service6_src_fortiguard: str | list[str] | list[PolicyInternetservice6srcfortiguardItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PolicyPayload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        srcintf: str | list[str] | list[PolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[PolicyDstintfItem] | None = ...,
        action: Literal["accept", "deny", "ipsec"] | None = ...,
        nat64: Literal["enable", "disable"] | None = ...,
        nat46: Literal["enable", "disable"] | None = ...,
        ztna_status: Literal["enable", "disable"] | None = ...,
        ztna_device_ownership: Literal["enable", "disable"] | None = ...,
        srcaddr: str | list[str] | list[PolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[PolicyDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[PolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[PolicyDstaddr6Item] | None = ...,
        ztna_ems_tag: str | list[str] | list[PolicyZtnaemstagItem] | None = ...,
        ztna_ems_tag_secondary: str | list[str] | list[PolicyZtnaemstagsecondaryItem] | None = ...,
        ztna_tags_match_logic: Literal["or", "and"] | None = ...,
        ztna_geo_tag: str | list[str] | list[PolicyZtnageotagItem] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[PolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[PolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[PolicyInternetservicecustomItem] | None = ...,
        network_service_dynamic: str | list[str] | list[PolicyNetworkservicedynamicItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[PolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[PolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[PolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[PolicyInternetservicesrccustomItem] | None = ...,
        network_service_src_dynamic: str | list[str] | list[PolicyNetworkservicesrcdynamicItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[PolicyInternetservicesrccustomgroupItem] | None = ...,
        reputation_minimum: int | None = ...,
        reputation_direction: Literal["source", "destination"] | None = ...,
        src_vendor_mac: str | list[str] | list[PolicySrcvendormacItem] | None = ...,
        internet_service6: Literal["enable", "disable"] | None = ...,
        internet_service6_name: str | list[str] | list[PolicyInternetservice6nameItem] | None = ...,
        internet_service6_group: str | list[str] | list[PolicyInternetservice6groupItem] | None = ...,
        internet_service6_custom: str | list[str] | list[PolicyInternetservice6customItem] | None = ...,
        internet_service6_custom_group: str | list[str] | list[PolicyInternetservice6customgroupItem] | None = ...,
        internet_service6_src: Literal["enable", "disable"] | None = ...,
        internet_service6_src_name: str | list[str] | list[PolicyInternetservice6srcnameItem] | None = ...,
        internet_service6_src_group: str | list[str] | list[PolicyInternetservice6srcgroupItem] | None = ...,
        internet_service6_src_custom: str | list[str] | list[PolicyInternetservice6srccustomItem] | None = ...,
        internet_service6_src_custom_group: str | list[str] | list[PolicyInternetservice6srccustomgroupItem] | None = ...,
        reputation_minimum6: int | None = ...,
        reputation_direction6: Literal["source", "destination"] | None = ...,
        rtp_nat: Literal["disable", "enable"] | None = ...,
        rtp_addr: str | list[str] | list[PolicyRtpaddrItem] | None = ...,
        send_deny_packet: Literal["disable", "enable"] | None = ...,
        firewall_session_dirty: Literal["check-all", "check-new"] | None = ...,
        schedule: str | None = ...,
        schedule_timeout: Literal["enable", "disable"] | None = ...,
        policy_expiry: Literal["enable", "disable"] | None = ...,
        policy_expiry_date: str | None = ...,
        policy_expiry_date_utc: str | None = ...,
        service: str | list[str] | list[PolicyServiceItem] | None = ...,
        tos_mask: str | None = ...,
        tos: str | None = ...,
        tos_negate: Literal["enable", "disable"] | None = ...,
        anti_replay: Literal["enable", "disable"] | None = ...,
        tcp_session_without_syn: Literal["all", "data-only", "disable"] | None = ...,
        geoip_anycast: Literal["enable", "disable"] | None = ...,
        geoip_match: Literal["physical-location", "registered-location"] | None = ...,
        dynamic_shaping: Literal["enable", "disable"] | None = ...,
        passive_wan_health_measurement: Literal["enable", "disable"] | None = ...,
        app_monitor: Literal["enable", "disable"] | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        inspection_mode: Literal["proxy", "flow"] | None = ...,
        http_policy_redirect: Literal["enable", "disable", "legacy"] | None = ...,
        ssh_policy_redirect: Literal["enable", "disable"] | None = ...,
        ztna_policy_redirect: Literal["enable", "disable"] | None = ...,
        webproxy_profile: str | None = ...,
        profile_type: Literal["single", "group"] | None = ...,
        profile_group: str | None = ...,
        profile_protocol_options: str | None = ...,
        ssl_ssh_profile: str | None = ...,
        av_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        dnsfilter_profile: str | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile: str | None = ...,
        file_filter_profile: str | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        voip_profile: str | None = ...,
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        diameter_filter_profile: str | None = ...,
        virtual_patch_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        logtraffic_start: Literal["enable", "disable"] | None = ...,
        log_http_transaction: Literal["enable", "disable"] | None = ...,
        capture_packet: Literal["enable", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        wanopt: Literal["enable", "disable"] | None = ...,
        wanopt_detection: Literal["active", "passive", "off"] | None = ...,
        wanopt_passive_opt: Literal["default", "transparent", "non-transparent"] | None = ...,
        wanopt_profile: str | None = ...,
        wanopt_peer: str | None = ...,
        webcache: Literal["enable", "disable"] | None = ...,
        webcache_https: Literal["disable", "enable"] | None = ...,
        webproxy_forward_server: str | None = ...,
        traffic_shaper: str | None = ...,
        traffic_shaper_reverse: str | None = ...,
        per_ip_shaper: str | None = ...,
        nat: Literal["enable", "disable"] | None = ...,
        pcp_outbound: Literal["enable", "disable"] | None = ...,
        pcp_inbound: Literal["enable", "disable"] | None = ...,
        pcp_poolname: str | list[str] | list[PolicyPcppoolnameItem] | None = ...,
        permit_any_host: Literal["enable", "disable"] | None = ...,
        permit_stun_host: Literal["enable", "disable"] | None = ...,
        fixedport: Literal["enable", "disable"] | None = ...,
        port_preserve: Literal["enable", "disable"] | None = ...,
        port_random: Literal["enable", "disable"] | None = ...,
        ippool: Literal["enable", "disable"] | None = ...,
        poolname: str | list[str] | list[PolicyPoolnameItem] | None = ...,
        poolname6: str | list[str] | list[PolicyPoolname6Item] | None = ...,
        session_ttl: str | None = ...,
        vlan_cos_fwd: int | None = ...,
        vlan_cos_rev: int | None = ...,
        inbound: Literal["enable", "disable"] | None = ...,
        outbound: Literal["enable", "disable"] | None = ...,
        natinbound: Literal["enable", "disable"] | None = ...,
        natoutbound: Literal["enable", "disable"] | None = ...,
        fec: Literal["enable", "disable"] | None = ...,
        wccp: Literal["enable", "disable"] | None = ...,
        ntlm: Literal["enable", "disable"] | None = ...,
        ntlm_guest: Literal["enable", "disable"] | None = ...,
        ntlm_enabled_browsers: str | list[str] | list[PolicyNtlmenabledbrowsersItem] | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        groups: str | list[str] | list[PolicyGroupsItem] | None = ...,
        users: str | list[str] | list[PolicyUsersItem] | None = ...,
        fsso_groups: str | list[str] | list[PolicyFssogroupsItem] | None = ...,
        auth_path: Literal["enable", "disable"] | None = ...,
        disclaimer: Literal["enable", "disable"] | None = ...,
        email_collect: Literal["enable", "disable"] | None = ...,
        vpntunnel: str | None = ...,
        natip: str | None = ...,
        match_vip: Literal["enable", "disable"] | None = ...,
        match_vip_only: Literal["enable", "disable"] | None = ...,
        diffserv_copy: Literal["enable", "disable"] | None = ...,
        diffserv_forward: Literal["enable", "disable"] | None = ...,
        diffserv_reverse: Literal["enable", "disable"] | None = ...,
        diffservcode_forward: str | None = ...,
        diffservcode_rev: str | None = ...,
        tcp_mss_sender: int | None = ...,
        tcp_mss_receiver: int | None = ...,
        comments: str | None = ...,
        auth_cert: str | None = ...,
        auth_redirect_addr: str | None = ...,
        redirect_url: str | None = ...,
        identity_based_route: str | None = ...,
        block_notification: Literal["enable", "disable"] | None = ...,
        custom_log_fields: str | list[str] | list[PolicyCustomlogfieldsItem] | None = ...,
        replacemsg_override_group: str | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        srcaddr6_negate: Literal["enable", "disable"] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr6_negate: Literal["enable", "disable"] | None = ...,
        ztna_ems_tag_negate: Literal["enable", "disable"] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_src_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_src_negate: Literal["enable", "disable"] | None = ...,
        timeout_send_rst: Literal["enable", "disable"] | None = ...,
        captive_portal_exempt: Literal["enable", "disable"] | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        radius_mac_auth_bypass: Literal["enable", "disable"] | None = ...,
        radius_ip_auth_bypass: Literal["enable", "disable"] | None = ...,
        delay_tcp_npu_session: Literal["enable", "disable"] | None = ...,
        vlan_filter: str | None = ...,
        sgt_check: Literal["enable", "disable"] | None = ...,
        sgt: str | list[str] | list[PolicySgtItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[PolicyInternetservicefortiguardItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[PolicyInternetservicesrcfortiguardItem] | None = ...,
        internet_service6_fortiguard: str | list[str] | list[PolicyInternetservice6fortiguardItem] | None = ...,
        internet_service6_src_fortiguard: str | list[str] | list[PolicyInternetservice6srcfortiguardItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PolicyObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        policyid: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        policyid: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_policyid: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        policyid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: PolicyPayload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        srcintf: str | list[str] | list[PolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[PolicyDstintfItem] | None = ...,
        action: Literal["accept", "deny", "ipsec"] | None = ...,
        nat64: Literal["enable", "disable"] | None = ...,
        nat46: Literal["enable", "disable"] | None = ...,
        ztna_status: Literal["enable", "disable"] | None = ...,
        ztna_device_ownership: Literal["enable", "disable"] | None = ...,
        srcaddr: str | list[str] | list[PolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[PolicyDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[PolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[PolicyDstaddr6Item] | None = ...,
        ztna_ems_tag: str | list[str] | list[PolicyZtnaemstagItem] | None = ...,
        ztna_ems_tag_secondary: str | list[str] | list[PolicyZtnaemstagsecondaryItem] | None = ...,
        ztna_tags_match_logic: Literal["or", "and"] | None = ...,
        ztna_geo_tag: str | list[str] | list[PolicyZtnageotagItem] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[PolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[PolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[PolicyInternetservicecustomItem] | None = ...,
        network_service_dynamic: str | list[str] | list[PolicyNetworkservicedynamicItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[PolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[PolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[PolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[PolicyInternetservicesrccustomItem] | None = ...,
        network_service_src_dynamic: str | list[str] | list[PolicyNetworkservicesrcdynamicItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[PolicyInternetservicesrccustomgroupItem] | None = ...,
        reputation_minimum: int | None = ...,
        reputation_direction: Literal["source", "destination"] | None = ...,
        src_vendor_mac: str | list[str] | list[PolicySrcvendormacItem] | None = ...,
        internet_service6: Literal["enable", "disable"] | None = ...,
        internet_service6_name: str | list[str] | list[PolicyInternetservice6nameItem] | None = ...,
        internet_service6_group: str | list[str] | list[PolicyInternetservice6groupItem] | None = ...,
        internet_service6_custom: str | list[str] | list[PolicyInternetservice6customItem] | None = ...,
        internet_service6_custom_group: str | list[str] | list[PolicyInternetservice6customgroupItem] | None = ...,
        internet_service6_src: Literal["enable", "disable"] | None = ...,
        internet_service6_src_name: str | list[str] | list[PolicyInternetservice6srcnameItem] | None = ...,
        internet_service6_src_group: str | list[str] | list[PolicyInternetservice6srcgroupItem] | None = ...,
        internet_service6_src_custom: str | list[str] | list[PolicyInternetservice6srccustomItem] | None = ...,
        internet_service6_src_custom_group: str | list[str] | list[PolicyInternetservice6srccustomgroupItem] | None = ...,
        reputation_minimum6: int | None = ...,
        reputation_direction6: Literal["source", "destination"] | None = ...,
        rtp_nat: Literal["disable", "enable"] | None = ...,
        rtp_addr: str | list[str] | list[PolicyRtpaddrItem] | None = ...,
        send_deny_packet: Literal["disable", "enable"] | None = ...,
        firewall_session_dirty: Literal["check-all", "check-new"] | None = ...,
        schedule: str | None = ...,
        schedule_timeout: Literal["enable", "disable"] | None = ...,
        policy_expiry: Literal["enable", "disable"] | None = ...,
        policy_expiry_date: str | None = ...,
        policy_expiry_date_utc: str | None = ...,
        service: str | list[str] | list[PolicyServiceItem] | None = ...,
        tos_mask: str | None = ...,
        tos: str | None = ...,
        tos_negate: Literal["enable", "disable"] | None = ...,
        anti_replay: Literal["enable", "disable"] | None = ...,
        tcp_session_without_syn: Literal["all", "data-only", "disable"] | None = ...,
        geoip_anycast: Literal["enable", "disable"] | None = ...,
        geoip_match: Literal["physical-location", "registered-location"] | None = ...,
        dynamic_shaping: Literal["enable", "disable"] | None = ...,
        passive_wan_health_measurement: Literal["enable", "disable"] | None = ...,
        app_monitor: Literal["enable", "disable"] | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        inspection_mode: Literal["proxy", "flow"] | None = ...,
        http_policy_redirect: Literal["enable", "disable", "legacy"] | None = ...,
        ssh_policy_redirect: Literal["enable", "disable"] | None = ...,
        ztna_policy_redirect: Literal["enable", "disable"] | None = ...,
        webproxy_profile: str | None = ...,
        profile_type: Literal["single", "group"] | None = ...,
        profile_group: str | None = ...,
        profile_protocol_options: str | None = ...,
        ssl_ssh_profile: str | None = ...,
        av_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        dnsfilter_profile: str | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile: str | None = ...,
        file_filter_profile: str | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        voip_profile: str | None = ...,
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        diameter_filter_profile: str | None = ...,
        virtual_patch_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        logtraffic_start: Literal["enable", "disable"] | None = ...,
        log_http_transaction: Literal["enable", "disable"] | None = ...,
        capture_packet: Literal["enable", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        wanopt: Literal["enable", "disable"] | None = ...,
        wanopt_detection: Literal["active", "passive", "off"] | None = ...,
        wanopt_passive_opt: Literal["default", "transparent", "non-transparent"] | None = ...,
        wanopt_profile: str | None = ...,
        wanopt_peer: str | None = ...,
        webcache: Literal["enable", "disable"] | None = ...,
        webcache_https: Literal["disable", "enable"] | None = ...,
        webproxy_forward_server: str | None = ...,
        traffic_shaper: str | None = ...,
        traffic_shaper_reverse: str | None = ...,
        per_ip_shaper: str | None = ...,
        nat: Literal["enable", "disable"] | None = ...,
        pcp_outbound: Literal["enable", "disable"] | None = ...,
        pcp_inbound: Literal["enable", "disable"] | None = ...,
        pcp_poolname: str | list[str] | list[PolicyPcppoolnameItem] | None = ...,
        permit_any_host: Literal["enable", "disable"] | None = ...,
        permit_stun_host: Literal["enable", "disable"] | None = ...,
        fixedport: Literal["enable", "disable"] | None = ...,
        port_preserve: Literal["enable", "disable"] | None = ...,
        port_random: Literal["enable", "disable"] | None = ...,
        ippool: Literal["enable", "disable"] | None = ...,
        poolname: str | list[str] | list[PolicyPoolnameItem] | None = ...,
        poolname6: str | list[str] | list[PolicyPoolname6Item] | None = ...,
        session_ttl: str | None = ...,
        vlan_cos_fwd: int | None = ...,
        vlan_cos_rev: int | None = ...,
        inbound: Literal["enable", "disable"] | None = ...,
        outbound: Literal["enable", "disable"] | None = ...,
        natinbound: Literal["enable", "disable"] | None = ...,
        natoutbound: Literal["enable", "disable"] | None = ...,
        fec: Literal["enable", "disable"] | None = ...,
        wccp: Literal["enable", "disable"] | None = ...,
        ntlm: Literal["enable", "disable"] | None = ...,
        ntlm_guest: Literal["enable", "disable"] | None = ...,
        ntlm_enabled_browsers: str | list[str] | list[PolicyNtlmenabledbrowsersItem] | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        groups: str | list[str] | list[PolicyGroupsItem] | None = ...,
        users: str | list[str] | list[PolicyUsersItem] | None = ...,
        fsso_groups: str | list[str] | list[PolicyFssogroupsItem] | None = ...,
        auth_path: Literal["enable", "disable"] | None = ...,
        disclaimer: Literal["enable", "disable"] | None = ...,
        email_collect: Literal["enable", "disable"] | None = ...,
        vpntunnel: str | None = ...,
        natip: str | None = ...,
        match_vip: Literal["enable", "disable"] | None = ...,
        match_vip_only: Literal["enable", "disable"] | None = ...,
        diffserv_copy: Literal["enable", "disable"] | None = ...,
        diffserv_forward: Literal["enable", "disable"] | None = ...,
        diffserv_reverse: Literal["enable", "disable"] | None = ...,
        diffservcode_forward: str | None = ...,
        diffservcode_rev: str | None = ...,
        tcp_mss_sender: int | None = ...,
        tcp_mss_receiver: int | None = ...,
        comments: str | None = ...,
        auth_cert: str | None = ...,
        auth_redirect_addr: str | None = ...,
        redirect_url: str | None = ...,
        identity_based_route: str | None = ...,
        block_notification: Literal["enable", "disable"] | None = ...,
        custom_log_fields: str | list[str] | list[PolicyCustomlogfieldsItem] | None = ...,
        replacemsg_override_group: str | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        srcaddr6_negate: Literal["enable", "disable"] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr6_negate: Literal["enable", "disable"] | None = ...,
        ztna_ems_tag_negate: Literal["enable", "disable"] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_src_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_src_negate: Literal["enable", "disable"] | None = ...,
        timeout_send_rst: Literal["enable", "disable"] | None = ...,
        captive_portal_exempt: Literal["enable", "disable"] | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        radius_mac_auth_bypass: Literal["enable", "disable"] | None = ...,
        radius_ip_auth_bypass: Literal["enable", "disable"] | None = ...,
        delay_tcp_npu_session: Literal["enable", "disable"] | None = ...,
        vlan_filter: str | None = ...,
        sgt_check: Literal["enable", "disable"] | None = ...,
        sgt: str | list[str] | list[PolicySgtItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[PolicyInternetservicefortiguardItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[PolicyInternetservicesrcfortiguardItem] | None = ...,
        internet_service6_fortiguard: str | list[str] | list[PolicyInternetservice6fortiguardItem] | None = ...,
        internet_service6_src_fortiguard: str | list[str] | list[PolicyInternetservice6srcfortiguardItem] | None = ...,
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
    "Policy",
    "PolicyPayload",
    "PolicyResponse",
    "PolicyObject",
]