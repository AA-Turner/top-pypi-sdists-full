""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/proxy_policy
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

class ProxyPolicyAccessproxyItem(TypedDict, total=False):
    """Nested item for access-proxy field."""
    name: str


class ProxyPolicyAccessproxy6Item(TypedDict, total=False):
    """Nested item for access-proxy6 field."""
    name: str


class ProxyPolicyZtnaproxyItem(TypedDict, total=False):
    """Nested item for ztna-proxy field."""
    name: str


class ProxyPolicySrcintfItem(TypedDict, total=False):
    """Nested item for srcintf field."""
    name: str


class ProxyPolicyDstintfItem(TypedDict, total=False):
    """Nested item for dstintf field."""
    name: str


class ProxyPolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class ProxyPolicyPoolnameItem(TypedDict, total=False):
    """Nested item for poolname field."""
    name: str


class ProxyPolicyPoolname6Item(TypedDict, total=False):
    """Nested item for poolname6 field."""
    name: str


class ProxyPolicyDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class ProxyPolicyZtnaemstagItem(TypedDict, total=False):
    """Nested item for ztna-ems-tag field."""
    name: str


class ProxyPolicyUrlriskItem(TypedDict, total=False):
    """Nested item for url-risk field."""
    name: str


class ProxyPolicyInternetservicenameItem(TypedDict, total=False):
    """Nested item for internet-service-name field."""
    name: str


class ProxyPolicyInternetservicegroupItem(TypedDict, total=False):
    """Nested item for internet-service-group field."""
    name: str


class ProxyPolicyInternetservicecustomItem(TypedDict, total=False):
    """Nested item for internet-service-custom field."""
    name: str


class ProxyPolicyInternetservicecustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service-custom-group field."""
    name: str


class ProxyPolicyInternetservicefortiguardItem(TypedDict, total=False):
    """Nested item for internet-service-fortiguard field."""
    name: str


class ProxyPolicyInternetservice6nameItem(TypedDict, total=False):
    """Nested item for internet-service6-name field."""
    name: str


class ProxyPolicyInternetservice6groupItem(TypedDict, total=False):
    """Nested item for internet-service6-group field."""
    name: str


class ProxyPolicyInternetservice6customItem(TypedDict, total=False):
    """Nested item for internet-service6-custom field."""
    name: str


class ProxyPolicyInternetservice6customgroupItem(TypedDict, total=False):
    """Nested item for internet-service6-custom-group field."""
    name: str


class ProxyPolicyInternetservice6fortiguardItem(TypedDict, total=False):
    """Nested item for internet-service6-fortiguard field."""
    name: str


class ProxyPolicyServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class ProxyPolicySrcaddr6Item(TypedDict, total=False):
    """Nested item for srcaddr6 field."""
    name: str


class ProxyPolicyDstaddr6Item(TypedDict, total=False):
    """Nested item for dstaddr6 field."""
    name: str


class ProxyPolicyGroupsItem(TypedDict, total=False):
    """Nested item for groups field."""
    name: str


class ProxyPolicyUsersItem(TypedDict, total=False):
    """Nested item for users field."""
    name: str


class ProxyPolicyPayload(TypedDict, total=False):
    """Payload type for ProxyPolicy operations."""
    uuid: str
    policyid: int
    name: str
    proxy: Literal["explicit-web", "transparent-web", "ftp", "ssh", "ssh-tunnel", "access-proxy", "ztna-proxy", "wanopt"]
    access_proxy: str | list[str] | list[ProxyPolicyAccessproxyItem]
    access_proxy6: str | list[str] | list[ProxyPolicyAccessproxy6Item]
    ztna_proxy: str | list[str] | list[ProxyPolicyZtnaproxyItem]
    srcintf: str | list[str] | list[ProxyPolicySrcintfItem]
    dstintf: str | list[str] | list[ProxyPolicyDstintfItem]
    srcaddr: str | list[str] | list[ProxyPolicySrcaddrItem]
    poolname: str | list[str] | list[ProxyPolicyPoolnameItem]
    poolname6: str | list[str] | list[ProxyPolicyPoolname6Item]
    dstaddr: str | list[str] | list[ProxyPolicyDstaddrItem]
    ztna_ems_tag: str | list[str] | list[ProxyPolicyZtnaemstagItem]
    ztna_tags_match_logic: Literal["or", "and"]
    device_ownership: Literal["enable", "disable"]
    url_risk: str | list[str] | list[ProxyPolicyUrlriskItem]
    internet_service: Literal["enable", "disable"]
    internet_service_negate: Literal["enable", "disable"]
    internet_service_name: str | list[str] | list[ProxyPolicyInternetservicenameItem]
    internet_service_group: str | list[str] | list[ProxyPolicyInternetservicegroupItem]
    internet_service_custom: str | list[str] | list[ProxyPolicyInternetservicecustomItem]
    internet_service_custom_group: str | list[str] | list[ProxyPolicyInternetservicecustomgroupItem]
    internet_service_fortiguard: str | list[str] | list[ProxyPolicyInternetservicefortiguardItem]
    internet_service6: Literal["enable", "disable"]
    internet_service6_negate: Literal["enable", "disable"]
    internet_service6_name: str | list[str] | list[ProxyPolicyInternetservice6nameItem]
    internet_service6_group: str | list[str] | list[ProxyPolicyInternetservice6groupItem]
    internet_service6_custom: str | list[str] | list[ProxyPolicyInternetservice6customItem]
    internet_service6_custom_group: str | list[str] | list[ProxyPolicyInternetservice6customgroupItem]
    internet_service6_fortiguard: str | list[str] | list[ProxyPolicyInternetservice6fortiguardItem]
    service: str | list[str] | list[ProxyPolicyServiceItem]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr_negate: Literal["enable", "disable"]
    ztna_ems_tag_negate: Literal["enable", "disable"]
    service_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny", "redirect", "isolate"]
    status: Literal["enable", "disable"]
    schedule: str
    logtraffic: Literal["all", "utm", "disable"]
    session_ttl: int
    srcaddr6: str | list[str] | list[ProxyPolicySrcaddr6Item]
    dstaddr6: str | list[str] | list[ProxyPolicyDstaddr6Item]
    groups: str | list[str] | list[ProxyPolicyGroupsItem]
    users: str | list[str] | list[ProxyPolicyUsersItem]
    http_tunnel_auth: Literal["enable", "disable"]
    ssh_policy_redirect: Literal["enable", "disable"]
    webproxy_forward_server: str
    isolator_server: str
    webproxy_profile: str
    transparent: Literal["enable", "disable"]
    webcache: Literal["enable", "disable"]
    webcache_https: Literal["disable", "enable"]
    disclaimer: Literal["disable", "domain", "policy", "user"]
    utm_status: Literal["enable", "disable"]
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
    ips_voip_filter: str
    sctp_filter_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str
    replacemsg_override_group: str
    logtraffic_start: Literal["enable", "disable"]
    log_http_transaction: Literal["enable", "disable"]
    comments: str
    block_notification: Literal["enable", "disable"]
    redirect_url: str
    https_sub_category: Literal["enable", "disable"]
    decrypted_traffic_mirror: str
    detect_https_in_http_request: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProxyPolicyResponse(TypedDict, total=False):
    """Response type for ProxyPolicy - use with .dict property for typed dict access."""
    uuid: str
    policyid: int
    name: str
    proxy: Literal["explicit-web", "transparent-web", "ftp", "ssh", "ssh-tunnel", "access-proxy", "ztna-proxy", "wanopt"]
    access_proxy: list[ProxyPolicyAccessproxyItem]
    access_proxy6: list[ProxyPolicyAccessproxy6Item]
    ztna_proxy: list[ProxyPolicyZtnaproxyItem]
    srcintf: list[ProxyPolicySrcintfItem]
    dstintf: list[ProxyPolicyDstintfItem]
    srcaddr: list[ProxyPolicySrcaddrItem]
    poolname: list[ProxyPolicyPoolnameItem]
    poolname6: list[ProxyPolicyPoolname6Item]
    dstaddr: list[ProxyPolicyDstaddrItem]
    ztna_ems_tag: list[ProxyPolicyZtnaemstagItem]
    ztna_tags_match_logic: Literal["or", "and"]
    device_ownership: Literal["enable", "disable"]
    url_risk: list[ProxyPolicyUrlriskItem]
    internet_service: Literal["enable", "disable"]
    internet_service_negate: Literal["enable", "disable"]
    internet_service_name: list[ProxyPolicyInternetservicenameItem]
    internet_service_group: list[ProxyPolicyInternetservicegroupItem]
    internet_service_custom: list[ProxyPolicyInternetservicecustomItem]
    internet_service_custom_group: list[ProxyPolicyInternetservicecustomgroupItem]
    internet_service_fortiguard: list[ProxyPolicyInternetservicefortiguardItem]
    internet_service6: Literal["enable", "disable"]
    internet_service6_negate: Literal["enable", "disable"]
    internet_service6_name: list[ProxyPolicyInternetservice6nameItem]
    internet_service6_group: list[ProxyPolicyInternetservice6groupItem]
    internet_service6_custom: list[ProxyPolicyInternetservice6customItem]
    internet_service6_custom_group: list[ProxyPolicyInternetservice6customgroupItem]
    internet_service6_fortiguard: list[ProxyPolicyInternetservice6fortiguardItem]
    service: list[ProxyPolicyServiceItem]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr_negate: Literal["enable", "disable"]
    ztna_ems_tag_negate: Literal["enable", "disable"]
    service_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny", "redirect", "isolate"]
    status: Literal["enable", "disable"]
    schedule: str
    logtraffic: Literal["all", "utm", "disable"]
    session_ttl: int
    srcaddr6: list[ProxyPolicySrcaddr6Item]
    dstaddr6: list[ProxyPolicyDstaddr6Item]
    groups: list[ProxyPolicyGroupsItem]
    users: list[ProxyPolicyUsersItem]
    http_tunnel_auth: Literal["enable", "disable"]
    ssh_policy_redirect: Literal["enable", "disable"]
    webproxy_forward_server: str
    isolator_server: str
    webproxy_profile: str
    transparent: Literal["enable", "disable"]
    webcache: Literal["enable", "disable"]
    webcache_https: Literal["disable", "enable"]
    disclaimer: Literal["disable", "domain", "policy", "user"]
    utm_status: Literal["enable", "disable"]
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
    ips_voip_filter: str
    sctp_filter_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str
    replacemsg_override_group: str
    logtraffic_start: Literal["enable", "disable"]
    log_http_transaction: Literal["enable", "disable"]
    comments: str
    block_notification: Literal["enable", "disable"]
    redirect_url: str
    https_sub_category: Literal["enable", "disable"]
    decrypted_traffic_mirror: str
    detect_https_in_http_request: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProxyPolicyAccessproxyItemObject(FortiObject[ProxyPolicyAccessproxyItem]):
    """Typed object for access-proxy table items with attribute access."""
    name: str


class ProxyPolicyAccessproxy6ItemObject(FortiObject[ProxyPolicyAccessproxy6Item]):
    """Typed object for access-proxy6 table items with attribute access."""
    name: str


class ProxyPolicyZtnaproxyItemObject(FortiObject[ProxyPolicyZtnaproxyItem]):
    """Typed object for ztna-proxy table items with attribute access."""
    name: str


class ProxyPolicySrcintfItemObject(FortiObject[ProxyPolicySrcintfItem]):
    """Typed object for srcintf table items with attribute access."""
    name: str


class ProxyPolicyDstintfItemObject(FortiObject[ProxyPolicyDstintfItem]):
    """Typed object for dstintf table items with attribute access."""
    name: str


class ProxyPolicySrcaddrItemObject(FortiObject[ProxyPolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class ProxyPolicyPoolnameItemObject(FortiObject[ProxyPolicyPoolnameItem]):
    """Typed object for poolname table items with attribute access."""
    name: str


class ProxyPolicyPoolname6ItemObject(FortiObject[ProxyPolicyPoolname6Item]):
    """Typed object for poolname6 table items with attribute access."""
    name: str


class ProxyPolicyDstaddrItemObject(FortiObject[ProxyPolicyDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class ProxyPolicyZtnaemstagItemObject(FortiObject[ProxyPolicyZtnaemstagItem]):
    """Typed object for ztna-ems-tag table items with attribute access."""
    name: str


class ProxyPolicyUrlriskItemObject(FortiObject[ProxyPolicyUrlriskItem]):
    """Typed object for url-risk table items with attribute access."""
    name: str


class ProxyPolicyInternetservicenameItemObject(FortiObject[ProxyPolicyInternetservicenameItem]):
    """Typed object for internet-service-name table items with attribute access."""
    name: str


class ProxyPolicyInternetservicegroupItemObject(FortiObject[ProxyPolicyInternetservicegroupItem]):
    """Typed object for internet-service-group table items with attribute access."""
    name: str


class ProxyPolicyInternetservicecustomItemObject(FortiObject[ProxyPolicyInternetservicecustomItem]):
    """Typed object for internet-service-custom table items with attribute access."""
    name: str


class ProxyPolicyInternetservicecustomgroupItemObject(FortiObject[ProxyPolicyInternetservicecustomgroupItem]):
    """Typed object for internet-service-custom-group table items with attribute access."""
    name: str


class ProxyPolicyInternetservicefortiguardItemObject(FortiObject[ProxyPolicyInternetservicefortiguardItem]):
    """Typed object for internet-service-fortiguard table items with attribute access."""
    name: str


class ProxyPolicyInternetservice6nameItemObject(FortiObject[ProxyPolicyInternetservice6nameItem]):
    """Typed object for internet-service6-name table items with attribute access."""
    name: str


class ProxyPolicyInternetservice6groupItemObject(FortiObject[ProxyPolicyInternetservice6groupItem]):
    """Typed object for internet-service6-group table items with attribute access."""
    name: str


class ProxyPolicyInternetservice6customItemObject(FortiObject[ProxyPolicyInternetservice6customItem]):
    """Typed object for internet-service6-custom table items with attribute access."""
    name: str


class ProxyPolicyInternetservice6customgroupItemObject(FortiObject[ProxyPolicyInternetservice6customgroupItem]):
    """Typed object for internet-service6-custom-group table items with attribute access."""
    name: str


class ProxyPolicyInternetservice6fortiguardItemObject(FortiObject[ProxyPolicyInternetservice6fortiguardItem]):
    """Typed object for internet-service6-fortiguard table items with attribute access."""
    name: str


class ProxyPolicyServiceItemObject(FortiObject[ProxyPolicyServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class ProxyPolicySrcaddr6ItemObject(FortiObject[ProxyPolicySrcaddr6Item]):
    """Typed object for srcaddr6 table items with attribute access."""
    name: str


class ProxyPolicyDstaddr6ItemObject(FortiObject[ProxyPolicyDstaddr6Item]):
    """Typed object for dstaddr6 table items with attribute access."""
    name: str


class ProxyPolicyGroupsItemObject(FortiObject[ProxyPolicyGroupsItem]):
    """Typed object for groups table items with attribute access."""
    name: str


class ProxyPolicyUsersItemObject(FortiObject[ProxyPolicyUsersItem]):
    """Typed object for users table items with attribute access."""
    name: str


class ProxyPolicyObject(FortiObject):
    """Typed FortiObject for ProxyPolicy with field access."""
    uuid: str
    policyid: int
    name: str
    proxy: Literal["explicit-web", "transparent-web", "ftp", "ssh", "ssh-tunnel", "access-proxy", "ztna-proxy", "wanopt"]
    access_proxy: FortiObjectList[ProxyPolicyAccessproxyItemObject]
    access_proxy6: FortiObjectList[ProxyPolicyAccessproxy6ItemObject]
    ztna_proxy: FortiObjectList[ProxyPolicyZtnaproxyItemObject]
    srcintf: FortiObjectList[ProxyPolicySrcintfItemObject]
    dstintf: FortiObjectList[ProxyPolicyDstintfItemObject]
    srcaddr: FortiObjectList[ProxyPolicySrcaddrItemObject]
    poolname: FortiObjectList[ProxyPolicyPoolnameItemObject]
    poolname6: FortiObjectList[ProxyPolicyPoolname6ItemObject]
    dstaddr: FortiObjectList[ProxyPolicyDstaddrItemObject]
    ztna_ems_tag: FortiObjectList[ProxyPolicyZtnaemstagItemObject]
    ztna_tags_match_logic: Literal["or", "and"]
    device_ownership: Literal["enable", "disable"]
    url_risk: FortiObjectList[ProxyPolicyUrlriskItemObject]
    internet_service: Literal["enable", "disable"]
    internet_service_negate: Literal["enable", "disable"]
    internet_service_name: FortiObjectList[ProxyPolicyInternetservicenameItemObject]
    internet_service_group: FortiObjectList[ProxyPolicyInternetservicegroupItemObject]
    internet_service_custom: FortiObjectList[ProxyPolicyInternetservicecustomItemObject]
    internet_service_custom_group: FortiObjectList[ProxyPolicyInternetservicecustomgroupItemObject]
    internet_service_fortiguard: FortiObjectList[ProxyPolicyInternetservicefortiguardItemObject]
    internet_service6: Literal["enable", "disable"]
    internet_service6_negate: Literal["enable", "disable"]
    internet_service6_name: FortiObjectList[ProxyPolicyInternetservice6nameItemObject]
    internet_service6_group: FortiObjectList[ProxyPolicyInternetservice6groupItemObject]
    internet_service6_custom: FortiObjectList[ProxyPolicyInternetservice6customItemObject]
    internet_service6_custom_group: FortiObjectList[ProxyPolicyInternetservice6customgroupItemObject]
    internet_service6_fortiguard: FortiObjectList[ProxyPolicyInternetservice6fortiguardItemObject]
    service: FortiObjectList[ProxyPolicyServiceItemObject]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr_negate: Literal["enable", "disable"]
    ztna_ems_tag_negate: Literal["enable", "disable"]
    service_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny", "redirect", "isolate"]
    status: Literal["enable", "disable"]
    schedule: str
    logtraffic: Literal["all", "utm", "disable"]
    session_ttl: int
    srcaddr6: FortiObjectList[ProxyPolicySrcaddr6ItemObject]
    dstaddr6: FortiObjectList[ProxyPolicyDstaddr6ItemObject]
    groups: FortiObjectList[ProxyPolicyGroupsItemObject]
    users: FortiObjectList[ProxyPolicyUsersItemObject]
    http_tunnel_auth: Literal["enable", "disable"]
    ssh_policy_redirect: Literal["enable", "disable"]
    webproxy_forward_server: str
    isolator_server: str
    webproxy_profile: str
    transparent: Literal["enable", "disable"]
    webcache: Literal["enable", "disable"]
    webcache_https: Literal["disable", "enable"]
    disclaimer: Literal["disable", "domain", "policy", "user"]
    utm_status: Literal["enable", "disable"]
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
    ips_voip_filter: str
    sctp_filter_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str
    replacemsg_override_group: str
    logtraffic_start: Literal["enable", "disable"]
    log_http_transaction: Literal["enable", "disable"]
    comments: str
    block_notification: Literal["enable", "disable"]
    redirect_url: str
    https_sub_category: Literal["enable", "disable"]
    decrypted_traffic_mirror: str
    detect_https_in_http_request: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class ProxyPolicy:
    """
    
    Endpoint: firewall/proxy_policy
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
    ) -> ProxyPolicyObject: ...
    
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
    ) -> FortiObjectList[ProxyPolicyObject]: ...
    
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
        payload_dict: ProxyPolicyPayload | None = ...,
        uuid: str | None = ...,
        policyid: int | None = ...,
        name: str | None = ...,
        proxy: Literal["explicit-web", "transparent-web", "ftp", "ssh", "ssh-tunnel", "access-proxy", "ztna-proxy", "wanopt"] | None = ...,
        access_proxy: str | list[str] | list[ProxyPolicyAccessproxyItem] | None = ...,
        access_proxy6: str | list[str] | list[ProxyPolicyAccessproxy6Item] | None = ...,
        ztna_proxy: str | list[str] | list[ProxyPolicyZtnaproxyItem] | None = ...,
        srcintf: str | list[str] | list[ProxyPolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[ProxyPolicyDstintfItem] | None = ...,
        srcaddr: str | list[str] | list[ProxyPolicySrcaddrItem] | None = ...,
        poolname: str | list[str] | list[ProxyPolicyPoolnameItem] | None = ...,
        poolname6: str | list[str] | list[ProxyPolicyPoolname6Item] | None = ...,
        dstaddr: str | list[str] | list[ProxyPolicyDstaddrItem] | None = ...,
        ztna_ems_tag: str | list[str] | list[ProxyPolicyZtnaemstagItem] | None = ...,
        ztna_tags_match_logic: Literal["or", "and"] | None = ...,
        device_ownership: Literal["enable", "disable"] | None = ...,
        url_risk: str | list[str] | list[ProxyPolicyUrlriskItem] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[ProxyPolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[ProxyPolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[ProxyPolicyInternetservicecustomItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[ProxyPolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[ProxyPolicyInternetservicefortiguardItem] | None = ...,
        internet_service6: Literal["enable", "disable"] | None = ...,
        internet_service6_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_name: str | list[str] | list[ProxyPolicyInternetservice6nameItem] | None = ...,
        internet_service6_group: str | list[str] | list[ProxyPolicyInternetservice6groupItem] | None = ...,
        internet_service6_custom: str | list[str] | list[ProxyPolicyInternetservice6customItem] | None = ...,
        internet_service6_custom_group: str | list[str] | list[ProxyPolicyInternetservice6customgroupItem] | None = ...,
        internet_service6_fortiguard: str | list[str] | list[ProxyPolicyInternetservice6fortiguardItem] | None = ...,
        service: str | list[str] | list[ProxyPolicyServiceItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        ztna_ems_tag_negate: Literal["enable", "disable"] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny", "redirect", "isolate"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        session_ttl: int | None = ...,
        srcaddr6: str | list[str] | list[ProxyPolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[ProxyPolicyDstaddr6Item] | None = ...,
        groups: str | list[str] | list[ProxyPolicyGroupsItem] | None = ...,
        users: str | list[str] | list[ProxyPolicyUsersItem] | None = ...,
        http_tunnel_auth: Literal["enable", "disable"] | None = ...,
        ssh_policy_redirect: Literal["enable", "disable"] | None = ...,
        webproxy_forward_server: str | None = ...,
        isolator_server: str | None = ...,
        webproxy_profile: str | None = ...,
        transparent: Literal["enable", "disable"] | None = ...,
        webcache: Literal["enable", "disable"] | None = ...,
        webcache_https: Literal["disable", "enable"] | None = ...,
        disclaimer: Literal["disable", "domain", "policy", "user"] | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
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
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        replacemsg_override_group: str | None = ...,
        logtraffic_start: Literal["enable", "disable"] | None = ...,
        log_http_transaction: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        block_notification: Literal["enable", "disable"] | None = ...,
        redirect_url: str | None = ...,
        https_sub_category: Literal["enable", "disable"] | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        detect_https_in_http_request: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProxyPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProxyPolicyPayload | None = ...,
        uuid: str | None = ...,
        policyid: int | None = ...,
        name: str | None = ...,
        proxy: Literal["explicit-web", "transparent-web", "ftp", "ssh", "ssh-tunnel", "access-proxy", "ztna-proxy", "wanopt"] | None = ...,
        access_proxy: str | list[str] | list[ProxyPolicyAccessproxyItem] | None = ...,
        access_proxy6: str | list[str] | list[ProxyPolicyAccessproxy6Item] | None = ...,
        ztna_proxy: str | list[str] | list[ProxyPolicyZtnaproxyItem] | None = ...,
        srcintf: str | list[str] | list[ProxyPolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[ProxyPolicyDstintfItem] | None = ...,
        srcaddr: str | list[str] | list[ProxyPolicySrcaddrItem] | None = ...,
        poolname: str | list[str] | list[ProxyPolicyPoolnameItem] | None = ...,
        poolname6: str | list[str] | list[ProxyPolicyPoolname6Item] | None = ...,
        dstaddr: str | list[str] | list[ProxyPolicyDstaddrItem] | None = ...,
        ztna_ems_tag: str | list[str] | list[ProxyPolicyZtnaemstagItem] | None = ...,
        ztna_tags_match_logic: Literal["or", "and"] | None = ...,
        device_ownership: Literal["enable", "disable"] | None = ...,
        url_risk: str | list[str] | list[ProxyPolicyUrlriskItem] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[ProxyPolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[ProxyPolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[ProxyPolicyInternetservicecustomItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[ProxyPolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[ProxyPolicyInternetservicefortiguardItem] | None = ...,
        internet_service6: Literal["enable", "disable"] | None = ...,
        internet_service6_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_name: str | list[str] | list[ProxyPolicyInternetservice6nameItem] | None = ...,
        internet_service6_group: str | list[str] | list[ProxyPolicyInternetservice6groupItem] | None = ...,
        internet_service6_custom: str | list[str] | list[ProxyPolicyInternetservice6customItem] | None = ...,
        internet_service6_custom_group: str | list[str] | list[ProxyPolicyInternetservice6customgroupItem] | None = ...,
        internet_service6_fortiguard: str | list[str] | list[ProxyPolicyInternetservice6fortiguardItem] | None = ...,
        service: str | list[str] | list[ProxyPolicyServiceItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        ztna_ems_tag_negate: Literal["enable", "disable"] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny", "redirect", "isolate"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        session_ttl: int | None = ...,
        srcaddr6: str | list[str] | list[ProxyPolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[ProxyPolicyDstaddr6Item] | None = ...,
        groups: str | list[str] | list[ProxyPolicyGroupsItem] | None = ...,
        users: str | list[str] | list[ProxyPolicyUsersItem] | None = ...,
        http_tunnel_auth: Literal["enable", "disable"] | None = ...,
        ssh_policy_redirect: Literal["enable", "disable"] | None = ...,
        webproxy_forward_server: str | None = ...,
        isolator_server: str | None = ...,
        webproxy_profile: str | None = ...,
        transparent: Literal["enable", "disable"] | None = ...,
        webcache: Literal["enable", "disable"] | None = ...,
        webcache_https: Literal["disable", "enable"] | None = ...,
        disclaimer: Literal["disable", "domain", "policy", "user"] | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
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
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        replacemsg_override_group: str | None = ...,
        logtraffic_start: Literal["enable", "disable"] | None = ...,
        log_http_transaction: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        block_notification: Literal["enable", "disable"] | None = ...,
        redirect_url: str | None = ...,
        https_sub_category: Literal["enable", "disable"] | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        detect_https_in_http_request: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProxyPolicyObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        policyid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ProxyPolicyPayload | None = ...,
        uuid: str | None = ...,
        policyid: int | None = ...,
        name: str | None = ...,
        proxy: Literal["explicit-web", "transparent-web", "ftp", "ssh", "ssh-tunnel", "access-proxy", "ztna-proxy", "wanopt"] | None = ...,
        access_proxy: str | list[str] | list[ProxyPolicyAccessproxyItem] | None = ...,
        access_proxy6: str | list[str] | list[ProxyPolicyAccessproxy6Item] | None = ...,
        ztna_proxy: str | list[str] | list[ProxyPolicyZtnaproxyItem] | None = ...,
        srcintf: str | list[str] | list[ProxyPolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[ProxyPolicyDstintfItem] | None = ...,
        srcaddr: str | list[str] | list[ProxyPolicySrcaddrItem] | None = ...,
        poolname: str | list[str] | list[ProxyPolicyPoolnameItem] | None = ...,
        poolname6: str | list[str] | list[ProxyPolicyPoolname6Item] | None = ...,
        dstaddr: str | list[str] | list[ProxyPolicyDstaddrItem] | None = ...,
        ztna_ems_tag: str | list[str] | list[ProxyPolicyZtnaemstagItem] | None = ...,
        ztna_tags_match_logic: Literal["or", "and"] | None = ...,
        device_ownership: Literal["enable", "disable"] | None = ...,
        url_risk: str | list[str] | list[ProxyPolicyUrlriskItem] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[ProxyPolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[ProxyPolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[ProxyPolicyInternetservicecustomItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[ProxyPolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[ProxyPolicyInternetservicefortiguardItem] | None = ...,
        internet_service6: Literal["enable", "disable"] | None = ...,
        internet_service6_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_name: str | list[str] | list[ProxyPolicyInternetservice6nameItem] | None = ...,
        internet_service6_group: str | list[str] | list[ProxyPolicyInternetservice6groupItem] | None = ...,
        internet_service6_custom: str | list[str] | list[ProxyPolicyInternetservice6customItem] | None = ...,
        internet_service6_custom_group: str | list[str] | list[ProxyPolicyInternetservice6customgroupItem] | None = ...,
        internet_service6_fortiguard: str | list[str] | list[ProxyPolicyInternetservice6fortiguardItem] | None = ...,
        service: str | list[str] | list[ProxyPolicyServiceItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        ztna_ems_tag_negate: Literal["enable", "disable"] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny", "redirect", "isolate"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        session_ttl: int | None = ...,
        srcaddr6: str | list[str] | list[ProxyPolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[ProxyPolicyDstaddr6Item] | None = ...,
        groups: str | list[str] | list[ProxyPolicyGroupsItem] | None = ...,
        users: str | list[str] | list[ProxyPolicyUsersItem] | None = ...,
        http_tunnel_auth: Literal["enable", "disable"] | None = ...,
        ssh_policy_redirect: Literal["enable", "disable"] | None = ...,
        webproxy_forward_server: str | None = ...,
        isolator_server: str | None = ...,
        webproxy_profile: str | None = ...,
        transparent: Literal["enable", "disable"] | None = ...,
        webcache: Literal["enable", "disable"] | None = ...,
        webcache_https: Literal["disable", "enable"] | None = ...,
        disclaimer: Literal["disable", "domain", "policy", "user"] | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
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
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        replacemsg_override_group: str | None = ...,
        logtraffic_start: Literal["enable", "disable"] | None = ...,
        log_http_transaction: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        block_notification: Literal["enable", "disable"] | None = ...,
        redirect_url: str | None = ...,
        https_sub_category: Literal["enable", "disable"] | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        detect_https_in_http_request: Literal["enable", "disable"] | None = ...,
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
    "ProxyPolicy",
    "ProxyPolicyPayload",
    "ProxyPolicyResponse",
    "ProxyPolicyObject",
]