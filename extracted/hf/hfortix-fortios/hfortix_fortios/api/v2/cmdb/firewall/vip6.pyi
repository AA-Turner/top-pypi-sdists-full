""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/vip6
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

class Vip6RealserversMonitorItem(TypedDict, total=False):
    """Nested item for realservers.monitor field."""
    name: str


class Vip6SrcfilterItem(TypedDict, total=False):
    """Nested item for src-filter field."""
    range: str


class Vip6QuicDict(TypedDict, total=False):
    """Nested object type for quic field."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class Vip6RealserversItem(TypedDict, total=False):
    """Nested item for realservers field."""
    id: int
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    holddown_interval: int
    healthcheck: Literal["disable", "enable", "vip"]
    http_host: str
    translate_host: Literal["enable", "disable"]
    max_connections: int
    monitor: str | list[str] | list[Vip6RealserversMonitorItem]
    client_ip: str
    verify_cert: Literal["enable", "disable"]


class Vip6SslcertificateItem(TypedDict, total=False):
    """Nested item for ssl-certificate field."""
    name: str


class Vip6SslciphersuitesItem(TypedDict, total=False):
    """Nested item for ssl-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class Vip6SslserverciphersuitesItem(TypedDict, total=False):
    """Nested item for ssl-server-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class Vip6MonitorItem(TypedDict, total=False):
    """Nested item for monitor field."""
    name: str


class Vip6Payload(TypedDict, total=False):
    """Payload type for Vip6 operations."""
    name: str
    id: int
    uuid: str
    comment: str
    type: Literal["static-nat", "server-load-balance", "access-proxy"]
    src_filter: str | list[str] | list[Vip6SrcfilterItem]
    src_vip_filter: Literal["disable", "enable"]
    extip: str
    mappedip: str
    nat_source_vip: Literal["disable", "enable"]
    ndp_reply: Literal["disable", "enable"]
    portforward: Literal["disable", "enable"]
    protocol: Literal["tcp", "udp", "sctp"]
    extport: str
    mappedport: str
    color: int
    ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"]
    http_redirect: Literal["enable", "disable"]
    persistence: Literal["none", "http-cookie", "ssl-session-id"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: Vip6QuicDict
    nat66: Literal["disable", "enable"]
    nat64: Literal["disable", "enable"]
    add_nat64_route: Literal["disable", "enable"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]
    realservers: str | list[str] | list[Vip6RealserversItem]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    http_multiplex: Literal["enable", "disable"]
    http_ip_header: Literal["enable", "disable"]
    http_ip_header_name: str
    outlook_web_access: Literal["disable", "enable"]
    weblogic_server: Literal["disable", "enable"]
    websphere_server: Literal["disable", "enable"]
    ssl_mode: Literal["half", "full"]
    ssl_certificate: str | list[str] | list[Vip6SslcertificateItem]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low", "custom"]
    ssl_cipher_suites: str | list[str] | list[Vip6SslciphersuitesItem]
    ssl_server_renegotiation: Literal["enable", "disable"]
    ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"]
    ssl_server_cipher_suites: str | list[str] | list[Vip6SslserverciphersuitesItem]
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
    monitor: str | list[str] | list[Vip6MonitorItem]
    max_embryonic_connections: int
    embedded_ipv4_address: Literal["disable", "enable"]
    ipv4_mappedip: str
    ipv4_mappedport: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Vip6Response(TypedDict, total=False):
    """Response type for Vip6 - use with .dict property for typed dict access."""
    name: str
    id: int
    uuid: str
    comment: str
    type: Literal["static-nat", "server-load-balance", "access-proxy"]
    src_filter: list[Vip6SrcfilterItem]
    src_vip_filter: Literal["disable", "enable"]
    extip: str
    mappedip: str
    nat_source_vip: Literal["disable", "enable"]
    ndp_reply: Literal["disable", "enable"]
    portforward: Literal["disable", "enable"]
    protocol: Literal["tcp", "udp", "sctp"]
    extport: str
    mappedport: str
    color: int
    ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"]
    http_redirect: Literal["enable", "disable"]
    persistence: Literal["none", "http-cookie", "ssl-session-id"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: Vip6QuicDict
    nat66: Literal["disable", "enable"]
    nat64: Literal["disable", "enable"]
    add_nat64_route: Literal["disable", "enable"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]
    realservers: list[Vip6RealserversItem]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    http_multiplex: Literal["enable", "disable"]
    http_ip_header: Literal["enable", "disable"]
    http_ip_header_name: str
    outlook_web_access: Literal["disable", "enable"]
    weblogic_server: Literal["disable", "enable"]
    websphere_server: Literal["disable", "enable"]
    ssl_mode: Literal["half", "full"]
    ssl_certificate: list[Vip6SslcertificateItem]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low", "custom"]
    ssl_cipher_suites: list[Vip6SslciphersuitesItem]
    ssl_server_renegotiation: Literal["enable", "disable"]
    ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"]
    ssl_server_cipher_suites: list[Vip6SslserverciphersuitesItem]
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
    monitor: list[Vip6MonitorItem]
    max_embryonic_connections: int
    embedded_ipv4_address: Literal["disable", "enable"]
    ipv4_mappedip: str
    ipv4_mappedport: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Vip6RealserversMonitorItemObject(FortiObject[Vip6RealserversMonitorItem]):
    """Typed object for realservers.monitor table items with attribute access."""
    name: str


class Vip6SrcfilterItemObject(FortiObject[Vip6SrcfilterItem]):
    """Typed object for src-filter table items with attribute access."""
    range: str


class Vip6RealserversItemObject(FortiObject[Vip6RealserversItem]):
    """Typed object for realservers table items with attribute access."""
    id: int
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    holddown_interval: int
    healthcheck: Literal["disable", "enable", "vip"]
    http_host: str
    translate_host: Literal["enable", "disable"]
    max_connections: int
    monitor: FortiObjectList[Vip6RealserversMonitorItemObject]
    client_ip: str
    verify_cert: Literal["enable", "disable"]


class Vip6SslcertificateItemObject(FortiObject[Vip6SslcertificateItem]):
    """Typed object for ssl-certificate table items with attribute access."""
    name: str


class Vip6SslciphersuitesItemObject(FortiObject[Vip6SslciphersuitesItem]):
    """Typed object for ssl-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class Vip6SslserverciphersuitesItemObject(FortiObject[Vip6SslserverciphersuitesItem]):
    """Typed object for ssl-server-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class Vip6MonitorItemObject(FortiObject[Vip6MonitorItem]):
    """Typed object for monitor table items with attribute access."""
    name: str


class Vip6QuicObject(FortiObject):
    """Nested object for quic field with attribute access."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class Vip6Object(FortiObject):
    """Typed FortiObject for Vip6 with field access."""
    name: str
    id: int
    uuid: str
    comment: str
    type: Literal["static-nat", "server-load-balance", "access-proxy"]
    src_filter: FortiObjectList[Vip6SrcfilterItemObject]
    src_vip_filter: Literal["disable", "enable"]
    extip: str
    mappedip: str
    nat_source_vip: Literal["disable", "enable"]
    ndp_reply: Literal["disable", "enable"]
    portforward: Literal["disable", "enable"]
    protocol: Literal["tcp", "udp", "sctp"]
    extport: str
    mappedport: str
    color: int
    ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"]
    http_redirect: Literal["enable", "disable"]
    persistence: Literal["none", "http-cookie", "ssl-session-id"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: Vip6QuicObject
    nat66: Literal["disable", "enable"]
    nat64: Literal["disable", "enable"]
    add_nat64_route: Literal["disable", "enable"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]
    realservers: FortiObjectList[Vip6RealserversItemObject]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    http_multiplex: Literal["enable", "disable"]
    http_ip_header: Literal["enable", "disable"]
    http_ip_header_name: str
    outlook_web_access: Literal["disable", "enable"]
    weblogic_server: Literal["disable", "enable"]
    websphere_server: Literal["disable", "enable"]
    ssl_mode: Literal["half", "full"]
    ssl_certificate: FortiObjectList[Vip6SslcertificateItemObject]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low", "custom"]
    ssl_cipher_suites: FortiObjectList[Vip6SslciphersuitesItemObject]
    ssl_server_renegotiation: Literal["enable", "disable"]
    ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"]
    ssl_server_cipher_suites: FortiObjectList[Vip6SslserverciphersuitesItemObject]
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
    monitor: FortiObjectList[Vip6MonitorItemObject]
    max_embryonic_connections: int
    embedded_ipv4_address: Literal["disable", "enable"]
    ipv4_mappedip: str
    ipv4_mappedport: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Vip6:
    """
    
    Endpoint: firewall/vip6
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
    ) -> Vip6Object: ...
    
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
    ) -> FortiObjectList[Vip6Object]: ...
    
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
        payload_dict: Vip6Payload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        comment: str | None = ...,
        type: Literal["static-nat", "server-load-balance", "access-proxy"] | None = ...,
        src_filter: str | list[str] | list[Vip6SrcfilterItem] | None = ...,
        src_vip_filter: Literal["disable", "enable"] | None = ...,
        extip: str | None = ...,
        mappedip: str | None = ...,
        nat_source_vip: Literal["disable", "enable"] | None = ...,
        ndp_reply: Literal["disable", "enable"] | None = ...,
        portforward: Literal["disable", "enable"] | None = ...,
        protocol: Literal["tcp", "udp", "sctp"] | None = ...,
        extport: str | None = ...,
        mappedport: str | None = ...,
        color: int | None = ...,
        ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"] | None = ...,
        server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"] | None = ...,
        http_redirect: Literal["enable", "disable"] | None = ...,
        persistence: Literal["none", "http-cookie", "ssl-session-id"] | None = ...,
        h2_support: Literal["enable", "disable"] | None = ...,
        h3_support: Literal["enable", "disable"] | None = ...,
        quic: Vip6QuicDict | None = ...,
        nat66: Literal["disable", "enable"] | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        realservers: str | list[str] | list[Vip6RealserversItem] | None = ...,
        http_cookie_domain_from_host: Literal["disable", "enable"] | None = ...,
        http_cookie_domain: str | None = ...,
        http_cookie_path: str | None = ...,
        http_cookie_generation: int | None = ...,
        http_cookie_age: int | None = ...,
        http_cookie_share: Literal["disable", "same-ip"] | None = ...,
        https_cookie_secure: Literal["disable", "enable"] | None = ...,
        http_multiplex: Literal["enable", "disable"] | None = ...,
        http_ip_header: Literal["enable", "disable"] | None = ...,
        http_ip_header_name: str | None = ...,
        outlook_web_access: Literal["disable", "enable"] | None = ...,
        weblogic_server: Literal["disable", "enable"] | None = ...,
        websphere_server: Literal["disable", "enable"] | None = ...,
        ssl_mode: Literal["half", "full"] | None = ...,
        ssl_certificate: str | list[str] | list[Vip6SslcertificateItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low", "custom"] | None = ...,
        ssl_cipher_suites: str | list[str] | list[Vip6SslciphersuitesItem] | None = ...,
        ssl_server_renegotiation: Literal["enable", "disable"] | None = ...,
        ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"] | None = ...,
        ssl_server_cipher_suites: str | list[str] | list[Vip6SslserverciphersuitesItem] | None = ...,
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
        monitor: str | list[str] | list[Vip6MonitorItem] | None = ...,
        max_embryonic_connections: int | None = ...,
        embedded_ipv4_address: Literal["disable", "enable"] | None = ...,
        ipv4_mappedip: str | None = ...,
        ipv4_mappedport: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Vip6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Vip6Payload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        comment: str | None = ...,
        type: Literal["static-nat", "server-load-balance", "access-proxy"] | None = ...,
        src_filter: str | list[str] | list[Vip6SrcfilterItem] | None = ...,
        src_vip_filter: Literal["disable", "enable"] | None = ...,
        extip: str | None = ...,
        mappedip: str | None = ...,
        nat_source_vip: Literal["disable", "enable"] | None = ...,
        ndp_reply: Literal["disable", "enable"] | None = ...,
        portforward: Literal["disable", "enable"] | None = ...,
        protocol: Literal["tcp", "udp", "sctp"] | None = ...,
        extport: str | None = ...,
        mappedport: str | None = ...,
        color: int | None = ...,
        ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"] | None = ...,
        server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"] | None = ...,
        http_redirect: Literal["enable", "disable"] | None = ...,
        persistence: Literal["none", "http-cookie", "ssl-session-id"] | None = ...,
        h2_support: Literal["enable", "disable"] | None = ...,
        h3_support: Literal["enable", "disable"] | None = ...,
        quic: Vip6QuicDict | None = ...,
        nat66: Literal["disable", "enable"] | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        realservers: str | list[str] | list[Vip6RealserversItem] | None = ...,
        http_cookie_domain_from_host: Literal["disable", "enable"] | None = ...,
        http_cookie_domain: str | None = ...,
        http_cookie_path: str | None = ...,
        http_cookie_generation: int | None = ...,
        http_cookie_age: int | None = ...,
        http_cookie_share: Literal["disable", "same-ip"] | None = ...,
        https_cookie_secure: Literal["disable", "enable"] | None = ...,
        http_multiplex: Literal["enable", "disable"] | None = ...,
        http_ip_header: Literal["enable", "disable"] | None = ...,
        http_ip_header_name: str | None = ...,
        outlook_web_access: Literal["disable", "enable"] | None = ...,
        weblogic_server: Literal["disable", "enable"] | None = ...,
        websphere_server: Literal["disable", "enable"] | None = ...,
        ssl_mode: Literal["half", "full"] | None = ...,
        ssl_certificate: str | list[str] | list[Vip6SslcertificateItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low", "custom"] | None = ...,
        ssl_cipher_suites: str | list[str] | list[Vip6SslciphersuitesItem] | None = ...,
        ssl_server_renegotiation: Literal["enable", "disable"] | None = ...,
        ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"] | None = ...,
        ssl_server_cipher_suites: str | list[str] | list[Vip6SslserverciphersuitesItem] | None = ...,
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
        monitor: str | list[str] | list[Vip6MonitorItem] | None = ...,
        max_embryonic_connections: int | None = ...,
        embedded_ipv4_address: Literal["disable", "enable"] | None = ...,
        ipv4_mappedip: str | None = ...,
        ipv4_mappedport: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Vip6Object: ...

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
        payload_dict: Vip6Payload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        comment: str | None = ...,
        type: Literal["static-nat", "server-load-balance", "access-proxy"] | None = ...,
        src_filter: str | list[str] | list[Vip6SrcfilterItem] | None = ...,
        src_vip_filter: Literal["disable", "enable"] | None = ...,
        extip: str | None = ...,
        mappedip: str | None = ...,
        nat_source_vip: Literal["disable", "enable"] | None = ...,
        ndp_reply: Literal["disable", "enable"] | None = ...,
        portforward: Literal["disable", "enable"] | None = ...,
        protocol: Literal["tcp", "udp", "sctp"] | None = ...,
        extport: str | None = ...,
        mappedport: str | None = ...,
        color: int | None = ...,
        ldb_method: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"] | None = ...,
        server_type: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"] | None = ...,
        http_redirect: Literal["enable", "disable"] | None = ...,
        persistence: Literal["none", "http-cookie", "ssl-session-id"] | None = ...,
        h2_support: Literal["enable", "disable"] | None = ...,
        h3_support: Literal["enable", "disable"] | None = ...,
        quic: Vip6QuicDict | None = ...,
        nat66: Literal["disable", "enable"] | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        realservers: str | list[str] | list[Vip6RealserversItem] | None = ...,
        http_cookie_domain_from_host: Literal["disable", "enable"] | None = ...,
        http_cookie_domain: str | None = ...,
        http_cookie_path: str | None = ...,
        http_cookie_generation: int | None = ...,
        http_cookie_age: int | None = ...,
        http_cookie_share: Literal["disable", "same-ip"] | None = ...,
        https_cookie_secure: Literal["disable", "enable"] | None = ...,
        http_multiplex: Literal["enable", "disable"] | None = ...,
        http_ip_header: Literal["enable", "disable"] | None = ...,
        http_ip_header_name: str | None = ...,
        outlook_web_access: Literal["disable", "enable"] | None = ...,
        weblogic_server: Literal["disable", "enable"] | None = ...,
        websphere_server: Literal["disable", "enable"] | None = ...,
        ssl_mode: Literal["half", "full"] | None = ...,
        ssl_certificate: str | list[str] | list[Vip6SslcertificateItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low", "custom"] | None = ...,
        ssl_cipher_suites: str | list[str] | list[Vip6SslciphersuitesItem] | None = ...,
        ssl_server_renegotiation: Literal["enable", "disable"] | None = ...,
        ssl_server_algorithm: Literal["high", "medium", "low", "custom", "client"] | None = ...,
        ssl_server_cipher_suites: str | list[str] | list[Vip6SslserverciphersuitesItem] | None = ...,
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
        monitor: str | list[str] | list[Vip6MonitorItem] | None = ...,
        max_embryonic_connections: int | None = ...,
        embedded_ipv4_address: Literal["disable", "enable"] | None = ...,
        ipv4_mappedip: str | None = ...,
        ipv4_mappedport: str | None = ...,
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
    "Vip6",
    "Vip6Payload",
    "Vip6Response",
    "Vip6Object",
]