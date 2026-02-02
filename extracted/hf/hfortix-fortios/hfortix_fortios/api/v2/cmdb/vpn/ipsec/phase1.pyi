""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/ipsec/phase1
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

class Phase1CertificateItem(TypedDict, total=False):
    """Nested item for certificate field."""
    name: str


class Phase1InternaldomainlistItem(TypedDict, total=False):
    """Nested item for internal-domain-list field."""
    domain_name: str


class Phase1DnssuffixsearchItem(TypedDict, total=False):
    """Nested item for dns-suffix-search field."""
    dns_suffix: str


class Phase1Ipv4excluderangeItem(TypedDict, total=False):
    """Nested item for ipv4-exclude-range field."""
    id: int
    start_ip: str
    end_ip: str


class Phase1Ipv6excluderangeItem(TypedDict, total=False):
    """Nested item for ipv6-exclude-range field."""
    id: int
    start_ip: str
    end_ip: str


class Phase1BackupgatewayItem(TypedDict, total=False):
    """Nested item for backup-gateway field."""
    address: str


class Phase1RemotegwztnatagsItem(TypedDict, total=False):
    """Nested item for remote-gw-ztna-tags field."""
    name: str


class Phase1Payload(TypedDict, total=False):
    """Payload type for Phase1 operations."""
    name: str
    type: Literal["static", "dynamic", "ddns"]
    interface: str
    ike_version: Literal["1", "2"]
    remote_gw: str
    local_gw: str
    remotegw_ddns: str
    keylife: int
    certificate: str | list[str] | list[Phase1CertificateItem]
    authmethod: Literal["psk", "signature"]
    authmethod_remote: Literal["psk", "signature"]
    mode: Literal["aggressive", "main"]
    peertype: Literal["any", "one", "dialup", "peer", "peergrp"]
    peerid: str
    usrgrp: str
    peer: str
    peergrp: str
    mode_cfg: Literal["disable", "enable"]
    mode_cfg_allow_client_selector: Literal["disable", "enable"]
    assign_ip: Literal["disable", "enable"]
    assign_ip_from: Literal["range", "usrgrp", "dhcp", "name"]
    ipv4_start_ip: str
    ipv4_end_ip: str
    ipv4_netmask: str
    dhcp_ra_giaddr: str
    dhcp6_ra_linkaddr: str
    dns_mode: Literal["manual", "auto"]
    ipv4_dns_server1: str
    ipv4_dns_server2: str
    ipv4_dns_server3: str
    internal_domain_list: str | list[str] | list[Phase1InternaldomainlistItem]
    dns_suffix_search: str | list[str] | list[Phase1DnssuffixsearchItem]
    ipv4_wins_server1: str
    ipv4_wins_server2: str
    ipv4_exclude_range: str | list[str] | list[Phase1Ipv4excluderangeItem]
    ipv4_split_include: str
    split_include_service: str
    ipv4_name: str
    ipv6_start_ip: str
    ipv6_end_ip: str
    ipv6_prefix: int
    ipv6_dns_server1: str
    ipv6_dns_server2: str
    ipv6_dns_server3: str
    ipv6_exclude_range: str | list[str] | list[Phase1Ipv6excluderangeItem]
    ipv6_split_include: str
    ipv6_name: str
    ip_delay_interval: int
    unity_support: Literal["disable", "enable"]
    domain: str
    banner: str
    include_local_lan: Literal["disable", "enable"]
    ipv4_split_exclude: str
    ipv6_split_exclude: str
    save_password: Literal["disable", "enable"]
    client_auto_negotiate: Literal["disable", "enable"]
    client_keep_alive: Literal["disable", "enable"]
    backup_gateway: str | list[str] | list[Phase1BackupgatewayItem]
    proposal: str | list[str]
    add_route: Literal["disable", "enable"]
    add_gw_route: Literal["enable", "disable"]
    psksecret: str
    psksecret_remote: str
    keepalive: int
    distance: int
    priority: int
    localid: str
    localid_type: Literal["auto", "fqdn", "user-fqdn", "keyid", "address", "asn1dn"]
    auto_negotiate: Literal["enable", "disable"]
    negotiate_timeout: int
    fragmentation: Literal["enable", "disable"]
    dpd: Literal["disable", "on-idle", "on-demand"]
    dpd_retrycount: int
    dpd_retryinterval: str
    comments: str
    npu_offload: Literal["enable", "disable"]
    send_cert_chain: Literal["enable", "disable"]
    dhgrp: str | list[str]
    addke1: str | list[str]
    addke2: str | list[str]
    addke3: str | list[str]
    addke4: str | list[str]
    addke5: str | list[str]
    addke6: str | list[str]
    addke7: str | list[str]
    suite_b: Literal["disable", "suite-b-gcm-128", "suite-b-gcm-256"]
    eap: Literal["enable", "disable"]
    eap_identity: Literal["use-id-payload", "send-request"]
    eap_exclude_peergrp: str
    eap_cert_auth: Literal["enable", "disable"]
    acct_verify: Literal["enable", "disable"]
    ppk: Literal["disable", "allow", "require"]
    ppk_secret: str
    ppk_identity: str
    wizard_type: Literal["custom", "dialup-forticlient", "dialup-ios", "dialup-android", "dialup-windows", "dialup-cisco", "static-fortigate", "dialup-fortigate", "static-cisco", "dialup-cisco-fw", "simplified-static-fortigate", "hub-fortigate-auto-discovery", "spoke-fortigate-auto-discovery", "fabric-overlay-orchestrator"]
    xauthtype: Literal["disable", "client", "pap", "chap", "auto"]
    reauth: Literal["disable", "enable"]
    authusr: str
    authpasswd: str
    group_authentication: Literal["enable", "disable"]
    group_authentication_secret: str
    authusrgrp: str
    mesh_selector_type: Literal["disable", "subnet", "host"]
    idle_timeout: Literal["enable", "disable"]
    shared_idle_timeout: Literal["enable", "disable"]
    idle_timeoutinterval: int
    ha_sync_esp_seqno: Literal["enable", "disable"]
    fgsp_sync: Literal["enable", "disable"]
    inbound_dscp_copy: Literal["enable", "disable"]
    nattraversal: Literal["enable", "disable", "forced"]
    esn: Literal["require", "allow", "disable"]
    fragmentation_mtu: int
    childless_ike: Literal["enable", "disable"]
    azure_ad_autoconnect: Literal["enable", "disable"]
    client_resume: Literal["enable", "disable"]
    client_resume_interval: int
    rekey: Literal["enable", "disable"]
    digital_signature_auth: Literal["enable", "disable"]
    signature_hash_alg: str | list[str]
    rsa_signature_format: Literal["pkcs1", "pss"]
    rsa_signature_hash_override: Literal["enable", "disable"]
    enforce_unique_id: Literal["disable", "keep-new", "keep-old"]
    cert_id_validation: Literal["enable", "disable"]
    fec_egress: Literal["enable", "disable"]
    fec_send_timeout: int
    fec_base: int
    fec_codec: Literal["rs", "xor"]
    fec_redundant: int
    fec_ingress: Literal["enable", "disable"]
    fec_receive_timeout: int
    fec_health_check: str
    fec_mapping_profile: str
    network_overlay: Literal["disable", "enable"]
    network_id: int
    dev_id_notification: Literal["disable", "enable"]
    dev_id: str
    loopback_asymroute: Literal["enable", "disable"]
    link_cost: int
    kms: str
    exchange_fgt_device_id: Literal["enable", "disable"]
    ipv6_auto_linklocal: Literal["enable", "disable"]
    ems_sn_check: Literal["enable", "disable"]
    cert_trust_store: Literal["local", "ems"]
    qkd: Literal["disable", "allow", "require"]
    qkd_hybrid: Literal["disable", "allow", "require"]
    qkd_profile: str
    transport: Literal["udp", "auto", "tcp"]
    fortinet_esp: Literal["enable", "disable"]
    auto_transport_threshold: int
    remote_gw_match: Literal["any", "ipmask", "iprange", "geography", "ztna"]
    remote_gw_subnet: str
    remote_gw_start_ip: str
    remote_gw_end_ip: str
    remote_gw_country: str
    remote_gw_ztna_tags: str | list[str] | list[Phase1RemotegwztnatagsItem]
    remote_gw6_match: Literal["any", "ipprefix", "iprange", "geography"]
    remote_gw6_subnet: str
    remote_gw6_start_ip: str
    remote_gw6_end_ip: str
    remote_gw6_country: str
    cert_peer_username_validation: Literal["none", "othername", "rfc822name", "cn"]
    cert_peer_username_strip: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Phase1Response(TypedDict, total=False):
    """Response type for Phase1 - use with .dict property for typed dict access."""
    name: str
    type: Literal["static", "dynamic", "ddns"]
    interface: str
    ike_version: Literal["1", "2"]
    remote_gw: str
    local_gw: str
    remotegw_ddns: str
    keylife: int
    certificate: list[Phase1CertificateItem]
    authmethod: Literal["psk", "signature"]
    authmethod_remote: Literal["psk", "signature"]
    mode: Literal["aggressive", "main"]
    peertype: Literal["any", "one", "dialup", "peer", "peergrp"]
    peerid: str
    usrgrp: str
    peer: str
    peergrp: str
    mode_cfg: Literal["disable", "enable"]
    mode_cfg_allow_client_selector: Literal["disable", "enable"]
    assign_ip: Literal["disable", "enable"]
    assign_ip_from: Literal["range", "usrgrp", "dhcp", "name"]
    ipv4_start_ip: str
    ipv4_end_ip: str
    ipv4_netmask: str
    dhcp_ra_giaddr: str
    dhcp6_ra_linkaddr: str
    dns_mode: Literal["manual", "auto"]
    ipv4_dns_server1: str
    ipv4_dns_server2: str
    ipv4_dns_server3: str
    internal_domain_list: list[Phase1InternaldomainlistItem]
    dns_suffix_search: list[Phase1DnssuffixsearchItem]
    ipv4_wins_server1: str
    ipv4_wins_server2: str
    ipv4_exclude_range: list[Phase1Ipv4excluderangeItem]
    ipv4_split_include: str
    split_include_service: str
    ipv4_name: str
    ipv6_start_ip: str
    ipv6_end_ip: str
    ipv6_prefix: int
    ipv6_dns_server1: str
    ipv6_dns_server2: str
    ipv6_dns_server3: str
    ipv6_exclude_range: list[Phase1Ipv6excluderangeItem]
    ipv6_split_include: str
    ipv6_name: str
    ip_delay_interval: int
    unity_support: Literal["disable", "enable"]
    domain: str
    banner: str
    include_local_lan: Literal["disable", "enable"]
    ipv4_split_exclude: str
    ipv6_split_exclude: str
    save_password: Literal["disable", "enable"]
    client_auto_negotiate: Literal["disable", "enable"]
    client_keep_alive: Literal["disable", "enable"]
    backup_gateway: list[Phase1BackupgatewayItem]
    proposal: str
    add_route: Literal["disable", "enable"]
    add_gw_route: Literal["enable", "disable"]
    psksecret: str
    psksecret_remote: str
    keepalive: int
    distance: int
    priority: int
    localid: str
    localid_type: Literal["auto", "fqdn", "user-fqdn", "keyid", "address", "asn1dn"]
    auto_negotiate: Literal["enable", "disable"]
    negotiate_timeout: int
    fragmentation: Literal["enable", "disable"]
    dpd: Literal["disable", "on-idle", "on-demand"]
    dpd_retrycount: int
    dpd_retryinterval: str
    comments: str
    npu_offload: Literal["enable", "disable"]
    send_cert_chain: Literal["enable", "disable"]
    dhgrp: str
    addke1: str
    addke2: str
    addke3: str
    addke4: str
    addke5: str
    addke6: str
    addke7: str
    suite_b: Literal["disable", "suite-b-gcm-128", "suite-b-gcm-256"]
    eap: Literal["enable", "disable"]
    eap_identity: Literal["use-id-payload", "send-request"]
    eap_exclude_peergrp: str
    eap_cert_auth: Literal["enable", "disable"]
    acct_verify: Literal["enable", "disable"]
    ppk: Literal["disable", "allow", "require"]
    ppk_secret: str
    ppk_identity: str
    wizard_type: Literal["custom", "dialup-forticlient", "dialup-ios", "dialup-android", "dialup-windows", "dialup-cisco", "static-fortigate", "dialup-fortigate", "static-cisco", "dialup-cisco-fw", "simplified-static-fortigate", "hub-fortigate-auto-discovery", "spoke-fortigate-auto-discovery", "fabric-overlay-orchestrator"]
    xauthtype: Literal["disable", "client", "pap", "chap", "auto"]
    reauth: Literal["disable", "enable"]
    authusr: str
    authpasswd: str
    group_authentication: Literal["enable", "disable"]
    group_authentication_secret: str
    authusrgrp: str
    mesh_selector_type: Literal["disable", "subnet", "host"]
    idle_timeout: Literal["enable", "disable"]
    shared_idle_timeout: Literal["enable", "disable"]
    idle_timeoutinterval: int
    ha_sync_esp_seqno: Literal["enable", "disable"]
    fgsp_sync: Literal["enable", "disable"]
    inbound_dscp_copy: Literal["enable", "disable"]
    nattraversal: Literal["enable", "disable", "forced"]
    esn: Literal["require", "allow", "disable"]
    fragmentation_mtu: int
    childless_ike: Literal["enable", "disable"]
    azure_ad_autoconnect: Literal["enable", "disable"]
    client_resume: Literal["enable", "disable"]
    client_resume_interval: int
    rekey: Literal["enable", "disable"]
    digital_signature_auth: Literal["enable", "disable"]
    signature_hash_alg: str
    rsa_signature_format: Literal["pkcs1", "pss"]
    rsa_signature_hash_override: Literal["enable", "disable"]
    enforce_unique_id: Literal["disable", "keep-new", "keep-old"]
    cert_id_validation: Literal["enable", "disable"]
    fec_egress: Literal["enable", "disable"]
    fec_send_timeout: int
    fec_base: int
    fec_codec: Literal["rs", "xor"]
    fec_redundant: int
    fec_ingress: Literal["enable", "disable"]
    fec_receive_timeout: int
    fec_health_check: str
    fec_mapping_profile: str
    network_overlay: Literal["disable", "enable"]
    network_id: int
    dev_id_notification: Literal["disable", "enable"]
    dev_id: str
    loopback_asymroute: Literal["enable", "disable"]
    link_cost: int
    kms: str
    exchange_fgt_device_id: Literal["enable", "disable"]
    ipv6_auto_linklocal: Literal["enable", "disable"]
    ems_sn_check: Literal["enable", "disable"]
    cert_trust_store: Literal["local", "ems"]
    qkd: Literal["disable", "allow", "require"]
    qkd_hybrid: Literal["disable", "allow", "require"]
    qkd_profile: str
    transport: Literal["udp", "auto", "tcp"]
    fortinet_esp: Literal["enable", "disable"]
    auto_transport_threshold: int
    remote_gw_match: Literal["any", "ipmask", "iprange", "geography", "ztna"]
    remote_gw_subnet: str
    remote_gw_start_ip: str
    remote_gw_end_ip: str
    remote_gw_country: str
    remote_gw_ztna_tags: list[Phase1RemotegwztnatagsItem]
    remote_gw6_match: Literal["any", "ipprefix", "iprange", "geography"]
    remote_gw6_subnet: str
    remote_gw6_start_ip: str
    remote_gw6_end_ip: str
    remote_gw6_country: str
    cert_peer_username_validation: Literal["none", "othername", "rfc822name", "cn"]
    cert_peer_username_strip: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Phase1CertificateItemObject(FortiObject[Phase1CertificateItem]):
    """Typed object for certificate table items with attribute access."""
    name: str


class Phase1InternaldomainlistItemObject(FortiObject[Phase1InternaldomainlistItem]):
    """Typed object for internal-domain-list table items with attribute access."""
    domain_name: str


class Phase1DnssuffixsearchItemObject(FortiObject[Phase1DnssuffixsearchItem]):
    """Typed object for dns-suffix-search table items with attribute access."""
    dns_suffix: str


class Phase1Ipv4excluderangeItemObject(FortiObject[Phase1Ipv4excluderangeItem]):
    """Typed object for ipv4-exclude-range table items with attribute access."""
    id: int
    start_ip: str
    end_ip: str


class Phase1Ipv6excluderangeItemObject(FortiObject[Phase1Ipv6excluderangeItem]):
    """Typed object for ipv6-exclude-range table items with attribute access."""
    id: int
    start_ip: str
    end_ip: str


class Phase1BackupgatewayItemObject(FortiObject[Phase1BackupgatewayItem]):
    """Typed object for backup-gateway table items with attribute access."""
    address: str


class Phase1RemotegwztnatagsItemObject(FortiObject[Phase1RemotegwztnatagsItem]):
    """Typed object for remote-gw-ztna-tags table items with attribute access."""
    name: str


class Phase1Object(FortiObject):
    """Typed FortiObject for Phase1 with field access."""
    name: str
    type: Literal["static", "dynamic", "ddns"]
    interface: str
    ike_version: Literal["1", "2"]
    remote_gw: str
    local_gw: str
    remotegw_ddns: str
    keylife: int
    certificate: FortiObjectList[Phase1CertificateItemObject]
    authmethod: Literal["psk", "signature"]
    authmethod_remote: Literal["psk", "signature"]
    mode: Literal["aggressive", "main"]
    peertype: Literal["any", "one", "dialup", "peer", "peergrp"]
    peerid: str
    usrgrp: str
    peer: str
    peergrp: str
    mode_cfg: Literal["disable", "enable"]
    mode_cfg_allow_client_selector: Literal["disable", "enable"]
    assign_ip: Literal["disable", "enable"]
    assign_ip_from: Literal["range", "usrgrp", "dhcp", "name"]
    ipv4_start_ip: str
    ipv4_end_ip: str
    ipv4_netmask: str
    dhcp_ra_giaddr: str
    dhcp6_ra_linkaddr: str
    dns_mode: Literal["manual", "auto"]
    ipv4_dns_server1: str
    ipv4_dns_server2: str
    ipv4_dns_server3: str
    internal_domain_list: FortiObjectList[Phase1InternaldomainlistItemObject]
    dns_suffix_search: FortiObjectList[Phase1DnssuffixsearchItemObject]
    ipv4_wins_server1: str
    ipv4_wins_server2: str
    ipv4_exclude_range: FortiObjectList[Phase1Ipv4excluderangeItemObject]
    ipv4_split_include: str
    split_include_service: str
    ipv4_name: str
    ipv6_start_ip: str
    ipv6_end_ip: str
    ipv6_prefix: int
    ipv6_dns_server1: str
    ipv6_dns_server2: str
    ipv6_dns_server3: str
    ipv6_exclude_range: FortiObjectList[Phase1Ipv6excluderangeItemObject]
    ipv6_split_include: str
    ipv6_name: str
    ip_delay_interval: int
    unity_support: Literal["disable", "enable"]
    domain: str
    banner: str
    include_local_lan: Literal["disable", "enable"]
    ipv4_split_exclude: str
    ipv6_split_exclude: str
    save_password: Literal["disable", "enable"]
    client_auto_negotiate: Literal["disable", "enable"]
    client_keep_alive: Literal["disable", "enable"]
    backup_gateway: FortiObjectList[Phase1BackupgatewayItemObject]
    proposal: str
    add_route: Literal["disable", "enable"]
    add_gw_route: Literal["enable", "disable"]
    psksecret: str
    psksecret_remote: str
    keepalive: int
    distance: int
    priority: int
    localid: str
    localid_type: Literal["auto", "fqdn", "user-fqdn", "keyid", "address", "asn1dn"]
    auto_negotiate: Literal["enable", "disable"]
    negotiate_timeout: int
    fragmentation: Literal["enable", "disable"]
    dpd: Literal["disable", "on-idle", "on-demand"]
    dpd_retrycount: int
    dpd_retryinterval: str
    comments: str
    npu_offload: Literal["enable", "disable"]
    send_cert_chain: Literal["enable", "disable"]
    dhgrp: str
    addke1: str
    addke2: str
    addke3: str
    addke4: str
    addke5: str
    addke6: str
    addke7: str
    suite_b: Literal["disable", "suite-b-gcm-128", "suite-b-gcm-256"]
    eap: Literal["enable", "disable"]
    eap_identity: Literal["use-id-payload", "send-request"]
    eap_exclude_peergrp: str
    eap_cert_auth: Literal["enable", "disable"]
    acct_verify: Literal["enable", "disable"]
    ppk: Literal["disable", "allow", "require"]
    ppk_secret: str
    ppk_identity: str
    wizard_type: Literal["custom", "dialup-forticlient", "dialup-ios", "dialup-android", "dialup-windows", "dialup-cisco", "static-fortigate", "dialup-fortigate", "static-cisco", "dialup-cisco-fw", "simplified-static-fortigate", "hub-fortigate-auto-discovery", "spoke-fortigate-auto-discovery", "fabric-overlay-orchestrator"]
    xauthtype: Literal["disable", "client", "pap", "chap", "auto"]
    reauth: Literal["disable", "enable"]
    authusr: str
    authpasswd: str
    group_authentication: Literal["enable", "disable"]
    group_authentication_secret: str
    authusrgrp: str
    mesh_selector_type: Literal["disable", "subnet", "host"]
    idle_timeout: Literal["enable", "disable"]
    shared_idle_timeout: Literal["enable", "disable"]
    idle_timeoutinterval: int
    ha_sync_esp_seqno: Literal["enable", "disable"]
    fgsp_sync: Literal["enable", "disable"]
    inbound_dscp_copy: Literal["enable", "disable"]
    nattraversal: Literal["enable", "disable", "forced"]
    esn: Literal["require", "allow", "disable"]
    fragmentation_mtu: int
    childless_ike: Literal["enable", "disable"]
    azure_ad_autoconnect: Literal["enable", "disable"]
    client_resume: Literal["enable", "disable"]
    client_resume_interval: int
    rekey: Literal["enable", "disable"]
    digital_signature_auth: Literal["enable", "disable"]
    signature_hash_alg: str
    rsa_signature_format: Literal["pkcs1", "pss"]
    rsa_signature_hash_override: Literal["enable", "disable"]
    enforce_unique_id: Literal["disable", "keep-new", "keep-old"]
    cert_id_validation: Literal["enable", "disable"]
    fec_egress: Literal["enable", "disable"]
    fec_send_timeout: int
    fec_base: int
    fec_codec: Literal["rs", "xor"]
    fec_redundant: int
    fec_ingress: Literal["enable", "disable"]
    fec_receive_timeout: int
    fec_health_check: str
    fec_mapping_profile: str
    network_overlay: Literal["disable", "enable"]
    network_id: int
    dev_id_notification: Literal["disable", "enable"]
    dev_id: str
    loopback_asymroute: Literal["enable", "disable"]
    link_cost: int
    kms: str
    exchange_fgt_device_id: Literal["enable", "disable"]
    ipv6_auto_linklocal: Literal["enable", "disable"]
    ems_sn_check: Literal["enable", "disable"]
    cert_trust_store: Literal["local", "ems"]
    qkd: Literal["disable", "allow", "require"]
    qkd_hybrid: Literal["disable", "allow", "require"]
    qkd_profile: str
    transport: Literal["udp", "auto", "tcp"]
    fortinet_esp: Literal["enable", "disable"]
    auto_transport_threshold: int
    remote_gw_match: Literal["any", "ipmask", "iprange", "geography", "ztna"]
    remote_gw_subnet: str
    remote_gw_start_ip: str
    remote_gw_end_ip: str
    remote_gw_country: str
    remote_gw_ztna_tags: FortiObjectList[Phase1RemotegwztnatagsItemObject]
    remote_gw6_match: Literal["any", "ipprefix", "iprange", "geography"]
    remote_gw6_subnet: str
    remote_gw6_start_ip: str
    remote_gw6_end_ip: str
    remote_gw6_country: str
    cert_peer_username_validation: Literal["none", "othername", "rfc822name", "cn"]
    cert_peer_username_strip: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Phase1:
    """
    
    Endpoint: vpn/ipsec/phase1
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
    ) -> Phase1Object: ...
    
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
    ) -> FortiObjectList[Phase1Object]: ...
    
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
        payload_dict: Phase1Payload | None = ...,
        name: str | None = ...,
        type: Literal["static", "dynamic", "ddns"] | None = ...,
        interface: str | None = ...,
        ike_version: Literal["1", "2"] | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        remotegw_ddns: str | None = ...,
        keylife: int | None = ...,
        certificate: str | list[str] | list[Phase1CertificateItem] | None = ...,
        authmethod: Literal["psk", "signature"] | None = ...,
        authmethod_remote: Literal["psk", "signature"] | None = ...,
        mode: Literal["aggressive", "main"] | None = ...,
        peertype: Literal["any", "one", "dialup", "peer", "peergrp"] | None = ...,
        peerid: str | None = ...,
        usrgrp: str | None = ...,
        peer: str | None = ...,
        peergrp: str | None = ...,
        mode_cfg: Literal["disable", "enable"] | None = ...,
        mode_cfg_allow_client_selector: Literal["disable", "enable"] | None = ...,
        assign_ip: Literal["disable", "enable"] | None = ...,
        assign_ip_from: Literal["range", "usrgrp", "dhcp", "name"] | None = ...,
        ipv4_start_ip: str | None = ...,
        ipv4_end_ip: str | None = ...,
        ipv4_netmask: str | None = ...,
        dhcp_ra_giaddr: str | None = ...,
        dhcp6_ra_linkaddr: str | None = ...,
        dns_mode: Literal["manual", "auto"] | None = ...,
        ipv4_dns_server1: str | None = ...,
        ipv4_dns_server2: str | None = ...,
        ipv4_dns_server3: str | None = ...,
        internal_domain_list: str | list[str] | list[Phase1InternaldomainlistItem] | None = ...,
        dns_suffix_search: str | list[str] | list[Phase1DnssuffixsearchItem] | None = ...,
        ipv4_wins_server1: str | None = ...,
        ipv4_wins_server2: str | None = ...,
        ipv4_exclude_range: str | list[str] | list[Phase1Ipv4excluderangeItem] | None = ...,
        ipv4_split_include: str | None = ...,
        split_include_service: str | None = ...,
        ipv4_name: str | None = ...,
        ipv6_start_ip: str | None = ...,
        ipv6_end_ip: str | None = ...,
        ipv6_prefix: int | None = ...,
        ipv6_dns_server1: str | None = ...,
        ipv6_dns_server2: str | None = ...,
        ipv6_dns_server3: str | None = ...,
        ipv6_exclude_range: str | list[str] | list[Phase1Ipv6excluderangeItem] | None = ...,
        ipv6_split_include: str | None = ...,
        ipv6_name: str | None = ...,
        ip_delay_interval: int | None = ...,
        unity_support: Literal["disable", "enable"] | None = ...,
        domain: str | None = ...,
        banner: str | None = ...,
        include_local_lan: Literal["disable", "enable"] | None = ...,
        ipv4_split_exclude: str | None = ...,
        ipv6_split_exclude: str | None = ...,
        save_password: Literal["disable", "enable"] | None = ...,
        client_auto_negotiate: Literal["disable", "enable"] | None = ...,
        client_keep_alive: Literal["disable", "enable"] | None = ...,
        backup_gateway: str | list[str] | list[Phase1BackupgatewayItem] | None = ...,
        proposal: str | list[str] | None = ...,
        add_route: Literal["disable", "enable"] | None = ...,
        add_gw_route: Literal["enable", "disable"] | None = ...,
        psksecret: str | None = ...,
        psksecret_remote: str | None = ...,
        keepalive: int | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
        localid: str | None = ...,
        localid_type: Literal["auto", "fqdn", "user-fqdn", "keyid", "address", "asn1dn"] | None = ...,
        auto_negotiate: Literal["enable", "disable"] | None = ...,
        negotiate_timeout: int | None = ...,
        fragmentation: Literal["enable", "disable"] | None = ...,
        dpd: Literal["disable", "on-idle", "on-demand"] | None = ...,
        dpd_retrycount: int | None = ...,
        dpd_retryinterval: str | None = ...,
        comments: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        send_cert_chain: Literal["enable", "disable"] | None = ...,
        dhgrp: str | list[str] | None = ...,
        addke1: str | list[str] | None = ...,
        addke2: str | list[str] | None = ...,
        addke3: str | list[str] | None = ...,
        addke4: str | list[str] | None = ...,
        addke5: str | list[str] | None = ...,
        addke6: str | list[str] | None = ...,
        addke7: str | list[str] | None = ...,
        suite_b: Literal["disable", "suite-b-gcm-128", "suite-b-gcm-256"] | None = ...,
        eap: Literal["enable", "disable"] | None = ...,
        eap_identity: Literal["use-id-payload", "send-request"] | None = ...,
        eap_exclude_peergrp: str | None = ...,
        eap_cert_auth: Literal["enable", "disable"] | None = ...,
        acct_verify: Literal["enable", "disable"] | None = ...,
        ppk: Literal["disable", "allow", "require"] | None = ...,
        ppk_secret: str | None = ...,
        ppk_identity: str | None = ...,
        wizard_type: Literal["custom", "dialup-forticlient", "dialup-ios", "dialup-android", "dialup-windows", "dialup-cisco", "static-fortigate", "dialup-fortigate", "static-cisco", "dialup-cisco-fw", "simplified-static-fortigate", "hub-fortigate-auto-discovery", "spoke-fortigate-auto-discovery", "fabric-overlay-orchestrator"] | None = ...,
        xauthtype: Literal["disable", "client", "pap", "chap", "auto"] | None = ...,
        reauth: Literal["disable", "enable"] | None = ...,
        authusr: str | None = ...,
        authpasswd: str | None = ...,
        group_authentication: Literal["enable", "disable"] | None = ...,
        group_authentication_secret: str | None = ...,
        authusrgrp: str | None = ...,
        mesh_selector_type: Literal["disable", "subnet", "host"] | None = ...,
        idle_timeout: Literal["enable", "disable"] | None = ...,
        shared_idle_timeout: Literal["enable", "disable"] | None = ...,
        idle_timeoutinterval: int | None = ...,
        ha_sync_esp_seqno: Literal["enable", "disable"] | None = ...,
        fgsp_sync: Literal["enable", "disable"] | None = ...,
        inbound_dscp_copy: Literal["enable", "disable"] | None = ...,
        nattraversal: Literal["enable", "disable", "forced"] | None = ...,
        esn: Literal["require", "allow", "disable"] | None = ...,
        fragmentation_mtu: int | None = ...,
        childless_ike: Literal["enable", "disable"] | None = ...,
        azure_ad_autoconnect: Literal["enable", "disable"] | None = ...,
        client_resume: Literal["enable", "disable"] | None = ...,
        client_resume_interval: int | None = ...,
        rekey: Literal["enable", "disable"] | None = ...,
        digital_signature_auth: Literal["enable", "disable"] | None = ...,
        signature_hash_alg: str | list[str] | None = ...,
        rsa_signature_format: Literal["pkcs1", "pss"] | None = ...,
        rsa_signature_hash_override: Literal["enable", "disable"] | None = ...,
        enforce_unique_id: Literal["disable", "keep-new", "keep-old"] | None = ...,
        cert_id_validation: Literal["enable", "disable"] | None = ...,
        fec_egress: Literal["enable", "disable"] | None = ...,
        fec_send_timeout: int | None = ...,
        fec_base: int | None = ...,
        fec_codec: Literal["rs", "xor"] | None = ...,
        fec_redundant: int | None = ...,
        fec_ingress: Literal["enable", "disable"] | None = ...,
        fec_receive_timeout: int | None = ...,
        fec_health_check: str | None = ...,
        fec_mapping_profile: str | None = ...,
        network_overlay: Literal["disable", "enable"] | None = ...,
        network_id: int | None = ...,
        dev_id_notification: Literal["disable", "enable"] | None = ...,
        dev_id: str | None = ...,
        loopback_asymroute: Literal["enable", "disable"] | None = ...,
        link_cost: int | None = ...,
        kms: str | None = ...,
        exchange_fgt_device_id: Literal["enable", "disable"] | None = ...,
        ipv6_auto_linklocal: Literal["enable", "disable"] | None = ...,
        ems_sn_check: Literal["enable", "disable"] | None = ...,
        cert_trust_store: Literal["local", "ems"] | None = ...,
        qkd: Literal["disable", "allow", "require"] | None = ...,
        qkd_hybrid: Literal["disable", "allow", "require"] | None = ...,
        qkd_profile: str | None = ...,
        transport: Literal["udp", "auto", "tcp"] | None = ...,
        fortinet_esp: Literal["enable", "disable"] | None = ...,
        auto_transport_threshold: int | None = ...,
        remote_gw_match: Literal["any", "ipmask", "iprange", "geography", "ztna"] | None = ...,
        remote_gw_subnet: str | None = ...,
        remote_gw_start_ip: str | None = ...,
        remote_gw_end_ip: str | None = ...,
        remote_gw_country: str | None = ...,
        remote_gw_ztna_tags: str | list[str] | list[Phase1RemotegwztnatagsItem] | None = ...,
        remote_gw6_match: Literal["any", "ipprefix", "iprange", "geography"] | None = ...,
        remote_gw6_subnet: str | None = ...,
        remote_gw6_start_ip: str | None = ...,
        remote_gw6_end_ip: str | None = ...,
        remote_gw6_country: str | None = ...,
        cert_peer_username_validation: Literal["none", "othername", "rfc822name", "cn"] | None = ...,
        cert_peer_username_strip: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Phase1Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Phase1Payload | None = ...,
        name: str | None = ...,
        type: Literal["static", "dynamic", "ddns"] | None = ...,
        interface: str | None = ...,
        ike_version: Literal["1", "2"] | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        remotegw_ddns: str | None = ...,
        keylife: int | None = ...,
        certificate: str | list[str] | list[Phase1CertificateItem] | None = ...,
        authmethod: Literal["psk", "signature"] | None = ...,
        authmethod_remote: Literal["psk", "signature"] | None = ...,
        mode: Literal["aggressive", "main"] | None = ...,
        peertype: Literal["any", "one", "dialup", "peer", "peergrp"] | None = ...,
        peerid: str | None = ...,
        usrgrp: str | None = ...,
        peer: str | None = ...,
        peergrp: str | None = ...,
        mode_cfg: Literal["disable", "enable"] | None = ...,
        mode_cfg_allow_client_selector: Literal["disable", "enable"] | None = ...,
        assign_ip: Literal["disable", "enable"] | None = ...,
        assign_ip_from: Literal["range", "usrgrp", "dhcp", "name"] | None = ...,
        ipv4_start_ip: str | None = ...,
        ipv4_end_ip: str | None = ...,
        ipv4_netmask: str | None = ...,
        dhcp_ra_giaddr: str | None = ...,
        dhcp6_ra_linkaddr: str | None = ...,
        dns_mode: Literal["manual", "auto"] | None = ...,
        ipv4_dns_server1: str | None = ...,
        ipv4_dns_server2: str | None = ...,
        ipv4_dns_server3: str | None = ...,
        internal_domain_list: str | list[str] | list[Phase1InternaldomainlistItem] | None = ...,
        dns_suffix_search: str | list[str] | list[Phase1DnssuffixsearchItem] | None = ...,
        ipv4_wins_server1: str | None = ...,
        ipv4_wins_server2: str | None = ...,
        ipv4_exclude_range: str | list[str] | list[Phase1Ipv4excluderangeItem] | None = ...,
        ipv4_split_include: str | None = ...,
        split_include_service: str | None = ...,
        ipv4_name: str | None = ...,
        ipv6_start_ip: str | None = ...,
        ipv6_end_ip: str | None = ...,
        ipv6_prefix: int | None = ...,
        ipv6_dns_server1: str | None = ...,
        ipv6_dns_server2: str | None = ...,
        ipv6_dns_server3: str | None = ...,
        ipv6_exclude_range: str | list[str] | list[Phase1Ipv6excluderangeItem] | None = ...,
        ipv6_split_include: str | None = ...,
        ipv6_name: str | None = ...,
        ip_delay_interval: int | None = ...,
        unity_support: Literal["disable", "enable"] | None = ...,
        domain: str | None = ...,
        banner: str | None = ...,
        include_local_lan: Literal["disable", "enable"] | None = ...,
        ipv4_split_exclude: str | None = ...,
        ipv6_split_exclude: str | None = ...,
        save_password: Literal["disable", "enable"] | None = ...,
        client_auto_negotiate: Literal["disable", "enable"] | None = ...,
        client_keep_alive: Literal["disable", "enable"] | None = ...,
        backup_gateway: str | list[str] | list[Phase1BackupgatewayItem] | None = ...,
        proposal: str | list[str] | None = ...,
        add_route: Literal["disable", "enable"] | None = ...,
        add_gw_route: Literal["enable", "disable"] | None = ...,
        psksecret: str | None = ...,
        psksecret_remote: str | None = ...,
        keepalive: int | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
        localid: str | None = ...,
        localid_type: Literal["auto", "fqdn", "user-fqdn", "keyid", "address", "asn1dn"] | None = ...,
        auto_negotiate: Literal["enable", "disable"] | None = ...,
        negotiate_timeout: int | None = ...,
        fragmentation: Literal["enable", "disable"] | None = ...,
        dpd: Literal["disable", "on-idle", "on-demand"] | None = ...,
        dpd_retrycount: int | None = ...,
        dpd_retryinterval: str | None = ...,
        comments: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        send_cert_chain: Literal["enable", "disable"] | None = ...,
        dhgrp: str | list[str] | None = ...,
        addke1: str | list[str] | None = ...,
        addke2: str | list[str] | None = ...,
        addke3: str | list[str] | None = ...,
        addke4: str | list[str] | None = ...,
        addke5: str | list[str] | None = ...,
        addke6: str | list[str] | None = ...,
        addke7: str | list[str] | None = ...,
        suite_b: Literal["disable", "suite-b-gcm-128", "suite-b-gcm-256"] | None = ...,
        eap: Literal["enable", "disable"] | None = ...,
        eap_identity: Literal["use-id-payload", "send-request"] | None = ...,
        eap_exclude_peergrp: str | None = ...,
        eap_cert_auth: Literal["enable", "disable"] | None = ...,
        acct_verify: Literal["enable", "disable"] | None = ...,
        ppk: Literal["disable", "allow", "require"] | None = ...,
        ppk_secret: str | None = ...,
        ppk_identity: str | None = ...,
        wizard_type: Literal["custom", "dialup-forticlient", "dialup-ios", "dialup-android", "dialup-windows", "dialup-cisco", "static-fortigate", "dialup-fortigate", "static-cisco", "dialup-cisco-fw", "simplified-static-fortigate", "hub-fortigate-auto-discovery", "spoke-fortigate-auto-discovery", "fabric-overlay-orchestrator"] | None = ...,
        xauthtype: Literal["disable", "client", "pap", "chap", "auto"] | None = ...,
        reauth: Literal["disable", "enable"] | None = ...,
        authusr: str | None = ...,
        authpasswd: str | None = ...,
        group_authentication: Literal["enable", "disable"] | None = ...,
        group_authentication_secret: str | None = ...,
        authusrgrp: str | None = ...,
        mesh_selector_type: Literal["disable", "subnet", "host"] | None = ...,
        idle_timeout: Literal["enable", "disable"] | None = ...,
        shared_idle_timeout: Literal["enable", "disable"] | None = ...,
        idle_timeoutinterval: int | None = ...,
        ha_sync_esp_seqno: Literal["enable", "disable"] | None = ...,
        fgsp_sync: Literal["enable", "disable"] | None = ...,
        inbound_dscp_copy: Literal["enable", "disable"] | None = ...,
        nattraversal: Literal["enable", "disable", "forced"] | None = ...,
        esn: Literal["require", "allow", "disable"] | None = ...,
        fragmentation_mtu: int | None = ...,
        childless_ike: Literal["enable", "disable"] | None = ...,
        azure_ad_autoconnect: Literal["enable", "disable"] | None = ...,
        client_resume: Literal["enable", "disable"] | None = ...,
        client_resume_interval: int | None = ...,
        rekey: Literal["enable", "disable"] | None = ...,
        digital_signature_auth: Literal["enable", "disable"] | None = ...,
        signature_hash_alg: str | list[str] | None = ...,
        rsa_signature_format: Literal["pkcs1", "pss"] | None = ...,
        rsa_signature_hash_override: Literal["enable", "disable"] | None = ...,
        enforce_unique_id: Literal["disable", "keep-new", "keep-old"] | None = ...,
        cert_id_validation: Literal["enable", "disable"] | None = ...,
        fec_egress: Literal["enable", "disable"] | None = ...,
        fec_send_timeout: int | None = ...,
        fec_base: int | None = ...,
        fec_codec: Literal["rs", "xor"] | None = ...,
        fec_redundant: int | None = ...,
        fec_ingress: Literal["enable", "disable"] | None = ...,
        fec_receive_timeout: int | None = ...,
        fec_health_check: str | None = ...,
        fec_mapping_profile: str | None = ...,
        network_overlay: Literal["disable", "enable"] | None = ...,
        network_id: int | None = ...,
        dev_id_notification: Literal["disable", "enable"] | None = ...,
        dev_id: str | None = ...,
        loopback_asymroute: Literal["enable", "disable"] | None = ...,
        link_cost: int | None = ...,
        kms: str | None = ...,
        exchange_fgt_device_id: Literal["enable", "disable"] | None = ...,
        ipv6_auto_linklocal: Literal["enable", "disable"] | None = ...,
        ems_sn_check: Literal["enable", "disable"] | None = ...,
        cert_trust_store: Literal["local", "ems"] | None = ...,
        qkd: Literal["disable", "allow", "require"] | None = ...,
        qkd_hybrid: Literal["disable", "allow", "require"] | None = ...,
        qkd_profile: str | None = ...,
        transport: Literal["udp", "auto", "tcp"] | None = ...,
        fortinet_esp: Literal["enable", "disable"] | None = ...,
        auto_transport_threshold: int | None = ...,
        remote_gw_match: Literal["any", "ipmask", "iprange", "geography", "ztna"] | None = ...,
        remote_gw_subnet: str | None = ...,
        remote_gw_start_ip: str | None = ...,
        remote_gw_end_ip: str | None = ...,
        remote_gw_country: str | None = ...,
        remote_gw_ztna_tags: str | list[str] | list[Phase1RemotegwztnatagsItem] | None = ...,
        remote_gw6_match: Literal["any", "ipprefix", "iprange", "geography"] | None = ...,
        remote_gw6_subnet: str | None = ...,
        remote_gw6_start_ip: str | None = ...,
        remote_gw6_end_ip: str | None = ...,
        remote_gw6_country: str | None = ...,
        cert_peer_username_validation: Literal["none", "othername", "rfc822name", "cn"] | None = ...,
        cert_peer_username_strip: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Phase1Object: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: Phase1Payload | None = ...,
        name: str | None = ...,
        type: Literal["static", "dynamic", "ddns"] | None = ...,
        interface: str | None = ...,
        ike_version: Literal["1", "2"] | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        remotegw_ddns: str | None = ...,
        keylife: int | None = ...,
        certificate: str | list[str] | list[Phase1CertificateItem] | None = ...,
        authmethod: Literal["psk", "signature"] | None = ...,
        authmethod_remote: Literal["psk", "signature"] | None = ...,
        mode: Literal["aggressive", "main"] | None = ...,
        peertype: Literal["any", "one", "dialup", "peer", "peergrp"] | None = ...,
        peerid: str | None = ...,
        usrgrp: str | None = ...,
        peer: str | None = ...,
        peergrp: str | None = ...,
        mode_cfg: Literal["disable", "enable"] | None = ...,
        mode_cfg_allow_client_selector: Literal["disable", "enable"] | None = ...,
        assign_ip: Literal["disable", "enable"] | None = ...,
        assign_ip_from: Literal["range", "usrgrp", "dhcp", "name"] | None = ...,
        ipv4_start_ip: str | None = ...,
        ipv4_end_ip: str | None = ...,
        ipv4_netmask: str | None = ...,
        dhcp_ra_giaddr: str | None = ...,
        dhcp6_ra_linkaddr: str | None = ...,
        dns_mode: Literal["manual", "auto"] | None = ...,
        ipv4_dns_server1: str | None = ...,
        ipv4_dns_server2: str | None = ...,
        ipv4_dns_server3: str | None = ...,
        internal_domain_list: str | list[str] | list[Phase1InternaldomainlistItem] | None = ...,
        dns_suffix_search: str | list[str] | list[Phase1DnssuffixsearchItem] | None = ...,
        ipv4_wins_server1: str | None = ...,
        ipv4_wins_server2: str | None = ...,
        ipv4_exclude_range: str | list[str] | list[Phase1Ipv4excluderangeItem] | None = ...,
        ipv4_split_include: str | None = ...,
        split_include_service: str | None = ...,
        ipv4_name: str | None = ...,
        ipv6_start_ip: str | None = ...,
        ipv6_end_ip: str | None = ...,
        ipv6_prefix: int | None = ...,
        ipv6_dns_server1: str | None = ...,
        ipv6_dns_server2: str | None = ...,
        ipv6_dns_server3: str | None = ...,
        ipv6_exclude_range: str | list[str] | list[Phase1Ipv6excluderangeItem] | None = ...,
        ipv6_split_include: str | None = ...,
        ipv6_name: str | None = ...,
        ip_delay_interval: int | None = ...,
        unity_support: Literal["disable", "enable"] | None = ...,
        domain: str | None = ...,
        banner: str | None = ...,
        include_local_lan: Literal["disable", "enable"] | None = ...,
        ipv4_split_exclude: str | None = ...,
        ipv6_split_exclude: str | None = ...,
        save_password: Literal["disable", "enable"] | None = ...,
        client_auto_negotiate: Literal["disable", "enable"] | None = ...,
        client_keep_alive: Literal["disable", "enable"] | None = ...,
        backup_gateway: str | list[str] | list[Phase1BackupgatewayItem] | None = ...,
        proposal: Literal["des-md5", "des-sha1", "des-sha256", "des-sha384", "des-sha512", "3des-md5", "3des-sha1", "3des-sha256", "3des-sha384", "3des-sha512", "aes128-md5", "aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes128gcm-prfsha1", "aes128gcm-prfsha256", "aes128gcm-prfsha384", "aes128gcm-prfsha512", "aes192-md5", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-md5", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes256gcm-prfsha1", "aes256gcm-prfsha256", "aes256gcm-prfsha384", "aes256gcm-prfsha512", "chacha20poly1305-prfsha1", "chacha20poly1305-prfsha256", "chacha20poly1305-prfsha384", "chacha20poly1305-prfsha512", "aria128-md5", "aria128-sha1", "aria128-sha256", "aria128-sha384", "aria128-sha512", "aria192-md5", "aria192-sha1", "aria192-sha256", "aria192-sha384", "aria192-sha512", "aria256-md5", "aria256-sha1", "aria256-sha256", "aria256-sha384", "aria256-sha512", "seed-md5", "seed-sha1", "seed-sha256", "seed-sha384", "seed-sha512"] | list[str] | None = ...,
        add_route: Literal["disable", "enable"] | None = ...,
        add_gw_route: Literal["enable", "disable"] | None = ...,
        psksecret: str | None = ...,
        psksecret_remote: str | None = ...,
        keepalive: int | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
        localid: str | None = ...,
        localid_type: Literal["auto", "fqdn", "user-fqdn", "keyid", "address", "asn1dn"] | None = ...,
        auto_negotiate: Literal["enable", "disable"] | None = ...,
        negotiate_timeout: int | None = ...,
        fragmentation: Literal["enable", "disable"] | None = ...,
        dpd: Literal["disable", "on-idle", "on-demand"] | None = ...,
        dpd_retrycount: int | None = ...,
        dpd_retryinterval: str | None = ...,
        comments: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        send_cert_chain: Literal["enable", "disable"] | None = ...,
        dhgrp: Literal["1", "2", "5", "14", "15", "16", "17", "18", "19", "20", "21", "27", "28", "29", "30", "31", "32"] | list[str] | None = ...,
        addke1: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke2: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke3: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke4: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke5: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke6: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke7: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        suite_b: Literal["disable", "suite-b-gcm-128", "suite-b-gcm-256"] | None = ...,
        eap: Literal["enable", "disable"] | None = ...,
        eap_identity: Literal["use-id-payload", "send-request"] | None = ...,
        eap_exclude_peergrp: str | None = ...,
        eap_cert_auth: Literal["enable", "disable"] | None = ...,
        acct_verify: Literal["enable", "disable"] | None = ...,
        ppk: Literal["disable", "allow", "require"] | None = ...,
        ppk_secret: str | None = ...,
        ppk_identity: str | None = ...,
        wizard_type: Literal["custom", "dialup-forticlient", "dialup-ios", "dialup-android", "dialup-windows", "dialup-cisco", "static-fortigate", "dialup-fortigate", "static-cisco", "dialup-cisco-fw", "simplified-static-fortigate", "hub-fortigate-auto-discovery", "spoke-fortigate-auto-discovery", "fabric-overlay-orchestrator"] | None = ...,
        xauthtype: Literal["disable", "client", "pap", "chap", "auto"] | None = ...,
        reauth: Literal["disable", "enable"] | None = ...,
        authusr: str | None = ...,
        authpasswd: str | None = ...,
        group_authentication: Literal["enable", "disable"] | None = ...,
        group_authentication_secret: str | None = ...,
        authusrgrp: str | None = ...,
        mesh_selector_type: Literal["disable", "subnet", "host"] | None = ...,
        idle_timeout: Literal["enable", "disable"] | None = ...,
        shared_idle_timeout: Literal["enable", "disable"] | None = ...,
        idle_timeoutinterval: int | None = ...,
        ha_sync_esp_seqno: Literal["enable", "disable"] | None = ...,
        fgsp_sync: Literal["enable", "disable"] | None = ...,
        inbound_dscp_copy: Literal["enable", "disable"] | None = ...,
        nattraversal: Literal["enable", "disable", "forced"] | None = ...,
        esn: Literal["require", "allow", "disable"] | None = ...,
        fragmentation_mtu: int | None = ...,
        childless_ike: Literal["enable", "disable"] | None = ...,
        azure_ad_autoconnect: Literal["enable", "disable"] | None = ...,
        client_resume: Literal["enable", "disable"] | None = ...,
        client_resume_interval: int | None = ...,
        rekey: Literal["enable", "disable"] | None = ...,
        digital_signature_auth: Literal["enable", "disable"] | None = ...,
        signature_hash_alg: Literal["sha1", "sha2-256", "sha2-384", "sha2-512"] | list[str] | None = ...,
        rsa_signature_format: Literal["pkcs1", "pss"] | None = ...,
        rsa_signature_hash_override: Literal["enable", "disable"] | None = ...,
        enforce_unique_id: Literal["disable", "keep-new", "keep-old"] | None = ...,
        cert_id_validation: Literal["enable", "disable"] | None = ...,
        fec_egress: Literal["enable", "disable"] | None = ...,
        fec_send_timeout: int | None = ...,
        fec_base: int | None = ...,
        fec_codec: Literal["rs", "xor"] | None = ...,
        fec_redundant: int | None = ...,
        fec_ingress: Literal["enable", "disable"] | None = ...,
        fec_receive_timeout: int | None = ...,
        fec_health_check: str | None = ...,
        fec_mapping_profile: str | None = ...,
        network_overlay: Literal["disable", "enable"] | None = ...,
        network_id: int | None = ...,
        dev_id_notification: Literal["disable", "enable"] | None = ...,
        dev_id: str | None = ...,
        loopback_asymroute: Literal["enable", "disable"] | None = ...,
        link_cost: int | None = ...,
        kms: str | None = ...,
        exchange_fgt_device_id: Literal["enable", "disable"] | None = ...,
        ipv6_auto_linklocal: Literal["enable", "disable"] | None = ...,
        ems_sn_check: Literal["enable", "disable"] | None = ...,
        cert_trust_store: Literal["local", "ems"] | None = ...,
        qkd: Literal["disable", "allow", "require"] | None = ...,
        qkd_hybrid: Literal["disable", "allow", "require"] | None = ...,
        qkd_profile: str | None = ...,
        transport: Literal["udp", "auto", "tcp"] | None = ...,
        fortinet_esp: Literal["enable", "disable"] | None = ...,
        auto_transport_threshold: int | None = ...,
        remote_gw_match: Literal["any", "ipmask", "iprange", "geography", "ztna"] | None = ...,
        remote_gw_subnet: str | None = ...,
        remote_gw_start_ip: str | None = ...,
        remote_gw_end_ip: str | None = ...,
        remote_gw_country: str | None = ...,
        remote_gw_ztna_tags: str | list[str] | list[Phase1RemotegwztnatagsItem] | None = ...,
        remote_gw6_match: Literal["any", "ipprefix", "iprange", "geography"] | None = ...,
        remote_gw6_subnet: str | None = ...,
        remote_gw6_start_ip: str | None = ...,
        remote_gw6_end_ip: str | None = ...,
        remote_gw6_country: str | None = ...,
        cert_peer_username_validation: Literal["none", "othername", "rfc822name", "cn"] | None = ...,
        cert_peer_username_strip: Literal["disable", "enable"] | None = ...,
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
    "Phase1",
    "Phase1Payload",
    "Phase1Response",
    "Phase1Object",
]