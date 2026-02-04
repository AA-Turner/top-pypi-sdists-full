""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/vip
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

class VipRealserversMonitorItem(TypedDict, total=False):
    """Nested item for realservers.monitor field."""
    name: str


class VipSrcfilterItem(TypedDict, total=False):
    """Nested item for src-filter field."""
    range: str


class VipServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class VipExtaddrItem(TypedDict, total=False):
    """Nested item for extaddr field."""
    name: str


class VipQuicDict(TypedDict, total=False):
    """Nested object type for quic field."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class VipMappedipItem(TypedDict, total=False):
    """Nested item for mappedip field."""
    range: str


class VipSrcintffilterItem(TypedDict, total=False):
    """Nested item for srcintf-filter field."""
    interface_name: str


class VipRealserversItem(TypedDict, total=False):
    """Nested item for realservers field."""
    id: int
    type: Literal["ip", "address"]
    address: str
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    holddown_interval: int
    healthcheck: Literal["disable", "enable", "vip"]
    http_host: str
    translate_host: Literal["enable", "disable"]
    max_connections: int
    monitor: str | list[str] | list[VipRealserversMonitorItem]
    client_ip: str
    verify_cert: Literal["enable", "disable"]


class VipSslcertificateItem(TypedDict, total=False):
    """Nested item for ssl-certificate field."""
    name: str


class VipSslciphersuitesItem(TypedDict, total=False):
    """Nested item for ssl-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class VipSslserverciphersuitesItem(TypedDict, total=False):
    """Nested item for ssl-server-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class VipMonitorItem(TypedDict, total=False):
    """Nested item for monitor field."""
    name: str


class VipGslbpublicipsItem(TypedDict, total=False):
    """Nested item for gslb-public-ips field."""
    index: int
    ip: str


class VipPayload(TypedDict, total=False):
    """Payload type for Vip operations."""
    name: str
    id: int
    uuid: str
    comment: str
    type: Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"]
    server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"]
    dns_mapping_ttl: int
    ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    src_filter: str | list[str] | list[VipSrcfilterItem]
    src_vip_filter: Literal["disable", "enable"]
    service: str | list[str] | list[VipServiceItem]
    extip: str
    extaddr: str | list[str] | list[VipExtaddrItem]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: VipQuicDict
    nat44: Literal["disable", "enable"]
    nat46: Literal["disable", "enable"]
    add_nat46_route: Literal["disable", "enable"]
    mappedip: str | list[str] | list[VipMappedipItem]
    mapped_addr: str
    extintf: str
    arp_reply: Literal["disable", "enable"]
    http_redirect: Literal["enable", "disable"]
    persistence: Literal["none", "http-cookie", "ssl-session-id"]
    nat_source_vip: Literal["disable", "enable"]
    portforward: Literal["disable", "enable"]
    status: Literal["disable", "enable"]
    protocol: Literal["tcp", "udp", "sctp", "icmp"]
    extport: str
    mappedport: str
    gratuitous_arp_interval: int
    srcintf_filter: str | list[str] | list[VipSrcintffilterItem]
    portmapping_type: Literal["1-to-1", "m-to-n"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]
    realservers: str | list[str] | list[VipRealserversItem]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    http_multiplex: Literal["enable", "disable"]
    http_multiplex_ttl: int
    http_multiplex_max_request: int
    http_multiplex_max_concurrent_request: int
    http_ip_header: Literal["enable", "disable"]
    http_ip_header_name: str
    outlook_web_access: Literal["disable", "enable"]
    weblogic_server: Literal["disable", "enable"]
    websphere_server: Literal["disable", "enable"]
    ssl_mode: Literal["half", "full"]
    ssl_certificate: str | list[str] | list[VipSslcertificateItem]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low", "custom"]
    ssl_cipher_suites: str | list[str] | list[VipSslciphersuitesItem]
    ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"]
    ssl_server_cipher_suites: str | list[str] | list[VipSslserverciphersuitesItem]
    ssl_pfs: Literal["require", "deny", "allow"]
    ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_server_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
    ssl_server_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
    ssl_accept_ffdhe_groups: Literal["enable", "disable"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    ssl_client_fallback: Literal["disable", "enable"]
    ssl_client_renegotiation: Literal["allow", "deny", "secure"]
    ssl_client_session_state_type: Literal["disable", "time", "count", "both"]
    ssl_client_session_state_timeout: int
    ssl_client_session_state_max: int
    ssl_client_rekey_count: int
    ssl_server_renegotiation: Literal["enable", "disable"]
    ssl_server_session_state_type: Literal["disable", "time", "count", "both"]
    ssl_server_session_state_timeout: int
    ssl_server_session_state_max: int
    ssl_http_location_conversion: Literal["enable", "disable"]
    ssl_http_match_host: Literal["enable", "disable"]
    ssl_hpkp: Literal["disable", "enable", "report-only"]
    ssl_hpkp_primary: str
    ssl_hpkp_backup: str
    ssl_hpkp_age: int
    ssl_hpkp_report_uri: str
    ssl_hpkp_include_subdomains: Literal["disable", "enable"]
    ssl_hsts: Literal["disable", "enable"]
    ssl_hsts_age: int
    ssl_hsts_include_subdomains: Literal["disable", "enable"]
    monitor: str | list[str] | list[VipMonitorItem]
    max_embryonic_connections: int
    color: int
    ipv6_mappedip: str
    ipv6_mappedport: str
    one_click_gslb_server: Literal["disable", "enable"]
    gslb_hostname: str
    gslb_domain_name: str
    gslb_public_ips: str | list[str] | list[VipGslbpublicipsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VipResponse(TypedDict, total=False):
    """Response type for Vip - use with .dict property for typed dict access."""
    name: str
    id: int
    uuid: str
    comment: str
    type: Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"]
    server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"]
    dns_mapping_ttl: int
    ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    src_filter: list[VipSrcfilterItem]
    src_vip_filter: Literal["disable", "enable"]
    service: list[VipServiceItem]
    extip: str
    extaddr: list[VipExtaddrItem]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: VipQuicDict
    nat44: Literal["disable", "enable"]
    nat46: Literal["disable", "enable"]
    add_nat46_route: Literal["disable", "enable"]
    mappedip: list[VipMappedipItem]
    mapped_addr: str
    extintf: str
    arp_reply: Literal["disable", "enable"]
    http_redirect: Literal["enable", "disable"]
    persistence: Literal["none", "http-cookie", "ssl-session-id"]
    nat_source_vip: Literal["disable", "enable"]
    portforward: Literal["disable", "enable"]
    status: Literal["disable", "enable"]
    protocol: Literal["tcp", "udp", "sctp", "icmp"]
    extport: str
    mappedport: str
    gratuitous_arp_interval: int
    srcintf_filter: list[VipSrcintffilterItem]
    portmapping_type: Literal["1-to-1", "m-to-n"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]
    realservers: list[VipRealserversItem]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    http_multiplex: Literal["enable", "disable"]
    http_multiplex_ttl: int
    http_multiplex_max_request: int
    http_multiplex_max_concurrent_request: int
    http_ip_header: Literal["enable", "disable"]
    http_ip_header_name: str
    outlook_web_access: Literal["disable", "enable"]
    weblogic_server: Literal["disable", "enable"]
    websphere_server: Literal["disable", "enable"]
    ssl_mode: Literal["half", "full"]
    ssl_certificate: list[VipSslcertificateItem]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low", "custom"]
    ssl_cipher_suites: list[VipSslciphersuitesItem]
    ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"]
    ssl_server_cipher_suites: list[VipSslserverciphersuitesItem]
    ssl_pfs: Literal["require", "deny", "allow"]
    ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_server_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
    ssl_server_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
    ssl_accept_ffdhe_groups: Literal["enable", "disable"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    ssl_client_fallback: Literal["disable", "enable"]
    ssl_client_renegotiation: Literal["allow", "deny", "secure"]
    ssl_client_session_state_type: Literal["disable", "time", "count", "both"]
    ssl_client_session_state_timeout: int
    ssl_client_session_state_max: int
    ssl_client_rekey_count: int
    ssl_server_renegotiation: Literal["enable", "disable"]
    ssl_server_session_state_type: Literal["disable", "time", "count", "both"]
    ssl_server_session_state_timeout: int
    ssl_server_session_state_max: int
    ssl_http_location_conversion: Literal["enable", "disable"]
    ssl_http_match_host: Literal["enable", "disable"]
    ssl_hpkp: Literal["disable", "enable", "report-only"]
    ssl_hpkp_primary: str
    ssl_hpkp_backup: str
    ssl_hpkp_age: int
    ssl_hpkp_report_uri: str
    ssl_hpkp_include_subdomains: Literal["disable", "enable"]
    ssl_hsts: Literal["disable", "enable"]
    ssl_hsts_age: int
    ssl_hsts_include_subdomains: Literal["disable", "enable"]
    monitor: list[VipMonitorItem]
    max_embryonic_connections: int
    color: int
    ipv6_mappedip: str
    ipv6_mappedport: str
    one_click_gslb_server: Literal["disable", "enable"]
    gslb_hostname: str
    gslb_domain_name: str
    gslb_public_ips: list[VipGslbpublicipsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VipRealserversMonitorItemObject(FortiObject[VipRealserversMonitorItem]):
    """Typed object for realservers.monitor table items with attribute access."""
    name: str


class VipSrcfilterItemObject(FortiObject[VipSrcfilterItem]):
    """Typed object for src-filter table items with attribute access."""
    range: str


class VipServiceItemObject(FortiObject[VipServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class VipExtaddrItemObject(FortiObject[VipExtaddrItem]):
    """Typed object for extaddr table items with attribute access."""
    name: str


class VipMappedipItemObject(FortiObject[VipMappedipItem]):
    """Typed object for mappedip table items with attribute access."""
    range: str


class VipSrcintffilterItemObject(FortiObject[VipSrcintffilterItem]):
    """Typed object for srcintf-filter table items with attribute access."""
    interface_name: str


class VipRealserversItemObject(FortiObject[VipRealserversItem]):
    """Typed object for realservers table items with attribute access."""
    id: int
    type: Literal["ip", "address"]
    address: str
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    holddown_interval: int
    healthcheck: Literal["disable", "enable", "vip"]
    http_host: str
    translate_host: Literal["enable", "disable"]
    max_connections: int
    monitor: FortiObjectList[VipRealserversMonitorItemObject]
    client_ip: str
    verify_cert: Literal["enable", "disable"]


class VipSslcertificateItemObject(FortiObject[VipSslcertificateItem]):
    """Typed object for ssl-certificate table items with attribute access."""
    name: str


class VipSslciphersuitesItemObject(FortiObject[VipSslciphersuitesItem]):
    """Typed object for ssl-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class VipSslserverciphersuitesItemObject(FortiObject[VipSslserverciphersuitesItem]):
    """Typed object for ssl-server-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class VipMonitorItemObject(FortiObject[VipMonitorItem]):
    """Typed object for monitor table items with attribute access."""
    name: str


class VipGslbpublicipsItemObject(FortiObject[VipGslbpublicipsItem]):
    """Typed object for gslb-public-ips table items with attribute access."""
    index: int
    ip: str


class VipQuicObject(FortiObject):
    """Nested object for quic field with attribute access."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class VipObject(FortiObject):
    """Typed FortiObject for Vip with field access."""
    name: str
    id: int
    uuid: str
    comment: str
    type: Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"]
    server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"]
    dns_mapping_ttl: int
    ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    src_filter: FortiObjectList[VipSrcfilterItemObject]
    src_vip_filter: Literal["disable", "enable"]
    service: FortiObjectList[VipServiceItemObject]
    extip: str
    extaddr: FortiObjectList[VipExtaddrItemObject]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: VipQuicObject
    nat44: Literal["disable", "enable"]
    nat46: Literal["disable", "enable"]
    add_nat46_route: Literal["disable", "enable"]
    mappedip: FortiObjectList[VipMappedipItemObject]
    mapped_addr: str
    extintf: str
    arp_reply: Literal["disable", "enable"]
    http_redirect: Literal["enable", "disable"]
    persistence: Literal["none", "http-cookie", "ssl-session-id"]
    nat_source_vip: Literal["disable", "enable"]
    portforward: Literal["disable", "enable"]
    status: Literal["disable", "enable"]
    protocol: Literal["tcp", "udp", "sctp", "icmp"]
    extport: str
    mappedport: str
    gratuitous_arp_interval: int
    srcintf_filter: FortiObjectList[VipSrcintffilterItemObject]
    portmapping_type: Literal["1-to-1", "m-to-n"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]
    realservers: FortiObjectList[VipRealserversItemObject]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    http_multiplex: Literal["enable", "disable"]
    http_multiplex_ttl: int
    http_multiplex_max_request: int
    http_multiplex_max_concurrent_request: int
    http_ip_header: Literal["enable", "disable"]
    http_ip_header_name: str
    outlook_web_access: Literal["disable", "enable"]
    weblogic_server: Literal["disable", "enable"]
    websphere_server: Literal["disable", "enable"]
    ssl_mode: Literal["half", "full"]
    ssl_certificate: FortiObjectList[VipSslcertificateItemObject]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low", "custom"]
    ssl_cipher_suites: FortiObjectList[VipSslciphersuitesItemObject]
    ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"]
    ssl_server_cipher_suites: FortiObjectList[VipSslserverciphersuitesItemObject]
    ssl_pfs: Literal["require", "deny", "allow"]
    ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_server_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
    ssl_server_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
    ssl_accept_ffdhe_groups: Literal["enable", "disable"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    ssl_client_fallback: Literal["disable", "enable"]
    ssl_client_renegotiation: Literal["allow", "deny", "secure"]
    ssl_client_session_state_type: Literal["disable", "time", "count", "both"]
    ssl_client_session_state_timeout: int
    ssl_client_session_state_max: int
    ssl_client_rekey_count: int
    ssl_server_renegotiation: Literal["enable", "disable"]
    ssl_server_session_state_type: Literal["disable", "time", "count", "both"]
    ssl_server_session_state_timeout: int
    ssl_server_session_state_max: int
    ssl_http_location_conversion: Literal["enable", "disable"]
    ssl_http_match_host: Literal["enable", "disable"]
    ssl_hpkp: Literal["disable", "enable", "report-only"]
    ssl_hpkp_primary: str
    ssl_hpkp_backup: str
    ssl_hpkp_age: int
    ssl_hpkp_report_uri: str
    ssl_hpkp_include_subdomains: Literal["disable", "enable"]
    ssl_hsts: Literal["disable", "enable"]
    ssl_hsts_age: int
    ssl_hsts_include_subdomains: Literal["disable", "enable"]
    monitor: FortiObjectList[VipMonitorItemObject]
    max_embryonic_connections: int
    color: int
    ipv6_mappedip: str
    ipv6_mappedport: str
    one_click_gslb_server: Literal["disable", "enable"]
    gslb_hostname: str
    gslb_domain_name: str
    gslb_public_ips: FortiObjectList[VipGslbpublicipsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Vip:
    """
    
    Endpoint: firewall/vip
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
    ) -> VipObject: ...
    
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
    ) -> FortiObjectList[VipObject]: ...
    
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
        payload_dict: VipPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        comment: str | None = ...,
        type: Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"] | None = ...,
        server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"] | None = ...,
        dns_mapping_ttl: int | None = ...,
        ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"] | None = ...,
        src_filter: str | list[str] | list[VipSrcfilterItem] | None = ...,
        src_vip_filter: Literal["disable", "enable"] | None = ...,
        service: str | list[str] | list[VipServiceItem] | None = ...,
        extip: str | None = ...,
        extaddr: str | list[str] | list[VipExtaddrItem] | None = ...,
        h2_support: Literal["enable", "disable"] | None = ...,
        h3_support: Literal["enable", "disable"] | None = ...,
        quic: VipQuicDict | None = ...,
        nat44: Literal["disable", "enable"] | None = ...,
        nat46: Literal["disable", "enable"] | None = ...,
        add_nat46_route: Literal["disable", "enable"] | None = ...,
        mappedip: str | list[str] | list[VipMappedipItem] | None = ...,
        mapped_addr: str | None = ...,
        extintf: str | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        http_redirect: Literal["enable", "disable"] | None = ...,
        persistence: Literal["none", "http-cookie", "ssl-session-id"] | None = ...,
        nat_source_vip: Literal["disable", "enable"] | None = ...,
        portforward: Literal["disable", "enable"] | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        protocol: Literal["tcp", "udp", "sctp", "icmp"] | None = ...,
        extport: str | None = ...,
        mappedport: str | None = ...,
        gratuitous_arp_interval: int | None = ...,
        srcintf_filter: str | list[str] | list[VipSrcintffilterItem] | None = ...,
        portmapping_type: Literal["1-to-1", "m-to-n"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        realservers: str | list[str] | list[VipRealserversItem] | None = ...,
        http_cookie_domain_from_host: Literal["disable", "enable"] | None = ...,
        http_cookie_domain: str | None = ...,
        http_cookie_path: str | None = ...,
        http_cookie_generation: int | None = ...,
        http_cookie_age: int | None = ...,
        http_cookie_share: Literal["disable", "same-ip"] | None = ...,
        https_cookie_secure: Literal["disable", "enable"] | None = ...,
        http_multiplex: Literal["enable", "disable"] | None = ...,
        http_multiplex_ttl: int | None = ...,
        http_multiplex_max_request: int | None = ...,
        http_multiplex_max_concurrent_request: int | None = ...,
        http_ip_header: Literal["enable", "disable"] | None = ...,
        http_ip_header_name: str | None = ...,
        outlook_web_access: Literal["disable", "enable"] | None = ...,
        weblogic_server: Literal["disable", "enable"] | None = ...,
        websphere_server: Literal["disable", "enable"] | None = ...,
        ssl_mode: Literal["half", "full"] | None = ...,
        ssl_certificate: str | list[str] | list[VipSslcertificateItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low", "custom"] | None = ...,
        ssl_cipher_suites: str | list[str] | list[VipSslciphersuitesItem] | None = ...,
        ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"] | None = ...,
        ssl_server_cipher_suites: str | list[str] | list[VipSslserverciphersuitesItem] | None = ...,
        ssl_pfs: Literal["require", "deny", "allow"] | None = ...,
        ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        ssl_server_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"] | None = ...,
        ssl_server_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"] | None = ...,
        ssl_accept_ffdhe_groups: Literal["enable", "disable"] | None = ...,
        ssl_send_empty_frags: Literal["enable", "disable"] | None = ...,
        ssl_client_fallback: Literal["disable", "enable"] | None = ...,
        ssl_client_renegotiation: Literal["allow", "deny", "secure"] | None = ...,
        ssl_client_session_state_type: Literal["disable", "time", "count", "both"] | None = ...,
        ssl_client_session_state_timeout: int | None = ...,
        ssl_client_session_state_max: int | None = ...,
        ssl_client_rekey_count: int | None = ...,
        ssl_server_renegotiation: Literal["enable", "disable"] | None = ...,
        ssl_server_session_state_type: Literal["disable", "time", "count", "both"] | None = ...,
        ssl_server_session_state_timeout: int | None = ...,
        ssl_server_session_state_max: int | None = ...,
        ssl_http_location_conversion: Literal["enable", "disable"] | None = ...,
        ssl_http_match_host: Literal["enable", "disable"] | None = ...,
        ssl_hpkp: Literal["disable", "enable", "report-only"] | None = ...,
        ssl_hpkp_primary: str | None = ...,
        ssl_hpkp_backup: str | None = ...,
        ssl_hpkp_age: int | None = ...,
        ssl_hpkp_report_uri: str | None = ...,
        ssl_hpkp_include_subdomains: Literal["disable", "enable"] | None = ...,
        ssl_hsts: Literal["disable", "enable"] | None = ...,
        ssl_hsts_age: int | None = ...,
        ssl_hsts_include_subdomains: Literal["disable", "enable"] | None = ...,
        monitor: str | list[str] | list[VipMonitorItem] | None = ...,
        max_embryonic_connections: int | None = ...,
        color: int | None = ...,
        ipv6_mappedip: str | None = ...,
        ipv6_mappedport: str | None = ...,
        one_click_gslb_server: Literal["disable", "enable"] | None = ...,
        gslb_hostname: str | None = ...,
        gslb_domain_name: str | None = ...,
        gslb_public_ips: str | list[str] | list[VipGslbpublicipsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VipObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VipPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        comment: str | None = ...,
        type: Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"] | None = ...,
        server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"] | None = ...,
        dns_mapping_ttl: int | None = ...,
        ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"] | None = ...,
        src_filter: str | list[str] | list[VipSrcfilterItem] | None = ...,
        src_vip_filter: Literal["disable", "enable"] | None = ...,
        service: str | list[str] | list[VipServiceItem] | None = ...,
        extip: str | None = ...,
        extaddr: str | list[str] | list[VipExtaddrItem] | None = ...,
        h2_support: Literal["enable", "disable"] | None = ...,
        h3_support: Literal["enable", "disable"] | None = ...,
        quic: VipQuicDict | None = ...,
        nat44: Literal["disable", "enable"] | None = ...,
        nat46: Literal["disable", "enable"] | None = ...,
        add_nat46_route: Literal["disable", "enable"] | None = ...,
        mappedip: str | list[str] | list[VipMappedipItem] | None = ...,
        mapped_addr: str | None = ...,
        extintf: str | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        http_redirect: Literal["enable", "disable"] | None = ...,
        persistence: Literal["none", "http-cookie", "ssl-session-id"] | None = ...,
        nat_source_vip: Literal["disable", "enable"] | None = ...,
        portforward: Literal["disable", "enable"] | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        protocol: Literal["tcp", "udp", "sctp", "icmp"] | None = ...,
        extport: str | None = ...,
        mappedport: str | None = ...,
        gratuitous_arp_interval: int | None = ...,
        srcintf_filter: str | list[str] | list[VipSrcintffilterItem] | None = ...,
        portmapping_type: Literal["1-to-1", "m-to-n"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        realservers: str | list[str] | list[VipRealserversItem] | None = ...,
        http_cookie_domain_from_host: Literal["disable", "enable"] | None = ...,
        http_cookie_domain: str | None = ...,
        http_cookie_path: str | None = ...,
        http_cookie_generation: int | None = ...,
        http_cookie_age: int | None = ...,
        http_cookie_share: Literal["disable", "same-ip"] | None = ...,
        https_cookie_secure: Literal["disable", "enable"] | None = ...,
        http_multiplex: Literal["enable", "disable"] | None = ...,
        http_multiplex_ttl: int | None = ...,
        http_multiplex_max_request: int | None = ...,
        http_multiplex_max_concurrent_request: int | None = ...,
        http_ip_header: Literal["enable", "disable"] | None = ...,
        http_ip_header_name: str | None = ...,
        outlook_web_access: Literal["disable", "enable"] | None = ...,
        weblogic_server: Literal["disable", "enable"] | None = ...,
        websphere_server: Literal["disable", "enable"] | None = ...,
        ssl_mode: Literal["half", "full"] | None = ...,
        ssl_certificate: str | list[str] | list[VipSslcertificateItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low", "custom"] | None = ...,
        ssl_cipher_suites: str | list[str] | list[VipSslciphersuitesItem] | None = ...,
        ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"] | None = ...,
        ssl_server_cipher_suites: str | list[str] | list[VipSslserverciphersuitesItem] | None = ...,
        ssl_pfs: Literal["require", "deny", "allow"] | None = ...,
        ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        ssl_server_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"] | None = ...,
        ssl_server_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"] | None = ...,
        ssl_accept_ffdhe_groups: Literal["enable", "disable"] | None = ...,
        ssl_send_empty_frags: Literal["enable", "disable"] | None = ...,
        ssl_client_fallback: Literal["disable", "enable"] | None = ...,
        ssl_client_renegotiation: Literal["allow", "deny", "secure"] | None = ...,
        ssl_client_session_state_type: Literal["disable", "time", "count", "both"] | None = ...,
        ssl_client_session_state_timeout: int | None = ...,
        ssl_client_session_state_max: int | None = ...,
        ssl_client_rekey_count: int | None = ...,
        ssl_server_renegotiation: Literal["enable", "disable"] | None = ...,
        ssl_server_session_state_type: Literal["disable", "time", "count", "both"] | None = ...,
        ssl_server_session_state_timeout: int | None = ...,
        ssl_server_session_state_max: int | None = ...,
        ssl_http_location_conversion: Literal["enable", "disable"] | None = ...,
        ssl_http_match_host: Literal["enable", "disable"] | None = ...,
        ssl_hpkp: Literal["disable", "enable", "report-only"] | None = ...,
        ssl_hpkp_primary: str | None = ...,
        ssl_hpkp_backup: str | None = ...,
        ssl_hpkp_age: int | None = ...,
        ssl_hpkp_report_uri: str | None = ...,
        ssl_hpkp_include_subdomains: Literal["disable", "enable"] | None = ...,
        ssl_hsts: Literal["disable", "enable"] | None = ...,
        ssl_hsts_age: int | None = ...,
        ssl_hsts_include_subdomains: Literal["disable", "enable"] | None = ...,
        monitor: str | list[str] | list[VipMonitorItem] | None = ...,
        max_embryonic_connections: int | None = ...,
        color: int | None = ...,
        ipv6_mappedip: str | None = ...,
        ipv6_mappedport: str | None = ...,
        one_click_gslb_server: Literal["disable", "enable"] | None = ...,
        gslb_hostname: str | None = ...,
        gslb_domain_name: str | None = ...,
        gslb_public_ips: str | list[str] | list[VipGslbpublicipsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VipObject: ...

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
        payload_dict: VipPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        comment: str | None = ...,
        type: Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"] | None = ...,
        server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"] | None = ...,
        dns_mapping_ttl: int | None = ...,
        ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"] | None = ...,
        src_filter: str | list[str] | list[VipSrcfilterItem] | None = ...,
        src_vip_filter: Literal["disable", "enable"] | None = ...,
        service: str | list[str] | list[VipServiceItem] | None = ...,
        extip: str | None = ...,
        extaddr: str | list[str] | list[VipExtaddrItem] | None = ...,
        h2_support: Literal["enable", "disable"] | None = ...,
        h3_support: Literal["enable", "disable"] | None = ...,
        quic: VipQuicDict | None = ...,
        nat44: Literal["disable", "enable"] | None = ...,
        nat46: Literal["disable", "enable"] | None = ...,
        add_nat46_route: Literal["disable", "enable"] | None = ...,
        mappedip: str | list[str] | list[VipMappedipItem] | None = ...,
        mapped_addr: str | None = ...,
        extintf: str | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        http_redirect: Literal["enable", "disable"] | None = ...,
        persistence: Literal["none", "http-cookie", "ssl-session-id"] | None = ...,
        nat_source_vip: Literal["disable", "enable"] | None = ...,
        portforward: Literal["disable", "enable"] | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        protocol: Literal["tcp", "udp", "sctp", "icmp"] | None = ...,
        extport: str | None = ...,
        mappedport: str | None = ...,
        gratuitous_arp_interval: int | None = ...,
        srcintf_filter: str | list[str] | list[VipSrcintffilterItem] | None = ...,
        portmapping_type: Literal["1-to-1", "m-to-n"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        realservers: str | list[str] | list[VipRealserversItem] | None = ...,
        http_cookie_domain_from_host: Literal["disable", "enable"] | None = ...,
        http_cookie_domain: str | None = ...,
        http_cookie_path: str | None = ...,
        http_cookie_generation: int | None = ...,
        http_cookie_age: int | None = ...,
        http_cookie_share: Literal["disable", "same-ip"] | None = ...,
        https_cookie_secure: Literal["disable", "enable"] | None = ...,
        http_multiplex: Literal["enable", "disable"] | None = ...,
        http_multiplex_ttl: int | None = ...,
        http_multiplex_max_request: int | None = ...,
        http_multiplex_max_concurrent_request: int | None = ...,
        http_ip_header: Literal["enable", "disable"] | None = ...,
        http_ip_header_name: str | None = ...,
        outlook_web_access: Literal["disable", "enable"] | None = ...,
        weblogic_server: Literal["disable", "enable"] | None = ...,
        websphere_server: Literal["disable", "enable"] | None = ...,
        ssl_mode: Literal["half", "full"] | None = ...,
        ssl_certificate: str | list[str] | list[VipSslcertificateItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low", "custom"] | None = ...,
        ssl_cipher_suites: str | list[str] | list[VipSslciphersuitesItem] | None = ...,
        ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"] | None = ...,
        ssl_server_cipher_suites: str | list[str] | list[VipSslserverciphersuitesItem] | None = ...,
        ssl_pfs: Literal["require", "deny", "allow"] | None = ...,
        ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        ssl_server_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"] | None = ...,
        ssl_server_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"] | None = ...,
        ssl_accept_ffdhe_groups: Literal["enable", "disable"] | None = ...,
        ssl_send_empty_frags: Literal["enable", "disable"] | None = ...,
        ssl_client_fallback: Literal["disable", "enable"] | None = ...,
        ssl_client_renegotiation: Literal["allow", "deny", "secure"] | None = ...,
        ssl_client_session_state_type: Literal["disable", "time", "count", "both"] | None = ...,
        ssl_client_session_state_timeout: int | None = ...,
        ssl_client_session_state_max: int | None = ...,
        ssl_client_rekey_count: int | None = ...,
        ssl_server_renegotiation: Literal["enable", "disable"] | None = ...,
        ssl_server_session_state_type: Literal["disable", "time", "count", "both"] | None = ...,
        ssl_server_session_state_timeout: int | None = ...,
        ssl_server_session_state_max: int | None = ...,
        ssl_http_location_conversion: Literal["enable", "disable"] | None = ...,
        ssl_http_match_host: Literal["enable", "disable"] | None = ...,
        ssl_hpkp: Literal["disable", "enable", "report-only"] | None = ...,
        ssl_hpkp_primary: str | None = ...,
        ssl_hpkp_backup: str | None = ...,
        ssl_hpkp_age: int | None = ...,
        ssl_hpkp_report_uri: str | None = ...,
        ssl_hpkp_include_subdomains: Literal["disable", "enable"] | None = ...,
        ssl_hsts: Literal["disable", "enable"] | None = ...,
        ssl_hsts_age: int | None = ...,
        ssl_hsts_include_subdomains: Literal["disable", "enable"] | None = ...,
        monitor: str | list[str] | list[VipMonitorItem] | None = ...,
        max_embryonic_connections: int | None = ...,
        color: int | None = ...,
        ipv6_mappedip: str | None = ...,
        ipv6_mappedport: str | None = ...,
        one_click_gslb_server: Literal["disable", "enable"] | None = ...,
        gslb_hostname: str | None = ...,
        gslb_domain_name: str | None = ...,
        gslb_public_ips: str | list[str] | list[VipGslbpublicipsItem] | None = ...,
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
    "Vip",
    "VipPayload",
    "VipResponse",
    "VipObject",
]