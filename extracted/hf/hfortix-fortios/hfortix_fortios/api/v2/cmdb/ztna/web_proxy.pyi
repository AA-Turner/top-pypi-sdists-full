""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ztna/web_proxy
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

class WebProxyApigatewayQuicDict(TypedDict, total=False):
    """Nested object type for api-gateway.quic field."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class WebProxyApigatewayRealserversItem(TypedDict, total=False):
    """Nested item for api-gateway.realservers field."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    verify_cert: Literal["enable", "disable"]


class WebProxyApigatewaySslciphersuitesItem(TypedDict, total=False):
    """Nested item for api-gateway.ssl-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class WebProxyApigateway6QuicDict(TypedDict, total=False):
    """Nested object type for api-gateway6.quic field."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class WebProxyApigateway6RealserversItem(TypedDict, total=False):
    """Nested item for api-gateway6.realservers field."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    verify_cert: Literal["enable", "disable"]


class WebProxyApigateway6SslciphersuitesItem(TypedDict, total=False):
    """Nested item for api-gateway6.ssl-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class WebProxyApigatewayItem(TypedDict, total=False):
    """Nested item for api-gateway field."""
    id: int
    url_map: str
    service: Literal["http", "https"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: WebProxyApigatewayQuicDict
    realservers: str | list[str] | list[WebProxyApigatewayRealserversItem]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: str | list[str] | list[WebProxyApigatewaySslciphersuitesItem]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]


class WebProxyApigateway6Item(TypedDict, total=False):
    """Nested item for api-gateway6 field."""
    id: int
    url_map: str
    service: Literal["http", "https"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: WebProxyApigateway6QuicDict
    realservers: str | list[str] | list[WebProxyApigateway6RealserversItem]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: str | list[str] | list[WebProxyApigateway6SslciphersuitesItem]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]


class WebProxyPayload(TypedDict, total=False):
    """Payload type for WebProxy operations."""
    name: str
    vip: str
    host: str
    decrypted_traffic_mirror: str
    log_blocked_traffic: Literal["disable", "enable"]
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    vip6: str
    svr_pool_multiplex: Literal["enable", "disable"]
    svr_pool_ttl: int
    svr_pool_server_max_request: int
    svr_pool_server_max_concurrent_request: int
    api_gateway: str | list[str] | list[WebProxyApigatewayItem]
    api_gateway6: str | list[str] | list[WebProxyApigateway6Item]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class WebProxyResponse(TypedDict, total=False):
    """Response type for WebProxy - use with .dict property for typed dict access."""
    name: str
    vip: str
    host: str
    decrypted_traffic_mirror: str
    log_blocked_traffic: Literal["disable", "enable"]
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    vip6: str
    svr_pool_multiplex: Literal["enable", "disable"]
    svr_pool_ttl: int
    svr_pool_server_max_request: int
    svr_pool_server_max_concurrent_request: int
    api_gateway: list[WebProxyApigatewayItem]
    api_gateway6: list[WebProxyApigateway6Item]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class WebProxyApigatewayRealserversItemObject(FortiObject[WebProxyApigatewayRealserversItem]):
    """Typed object for api-gateway.realservers table items with attribute access."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    verify_cert: Literal["enable", "disable"]


class WebProxyApigatewaySslciphersuitesItemObject(FortiObject[WebProxyApigatewaySslciphersuitesItem]):
    """Typed object for api-gateway.ssl-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class WebProxyApigateway6RealserversItemObject(FortiObject[WebProxyApigateway6RealserversItem]):
    """Typed object for api-gateway6.realservers table items with attribute access."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    port: int
    status: Literal["active", "standby", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    verify_cert: Literal["enable", "disable"]


class WebProxyApigateway6SslciphersuitesItemObject(FortiObject[WebProxyApigateway6SslciphersuitesItem]):
    """Typed object for api-gateway6.ssl-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class WebProxyApigatewayItemObject(FortiObject[WebProxyApigatewayItem]):
    """Typed object for api-gateway table items with attribute access."""
    id: int
    url_map: str
    service: Literal["http", "https"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: WebProxyApigatewayQuicObject
    realservers: FortiObjectList[WebProxyApigatewayRealserversItemObject]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: FortiObjectList[WebProxyApigatewaySslciphersuitesItemObject]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]


class WebProxyApigateway6ItemObject(FortiObject[WebProxyApigateway6Item]):
    """Typed object for api-gateway6 table items with attribute access."""
    id: int
    url_map: str
    service: Literal["http", "https"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: WebProxyApigateway6QuicObject
    realservers: FortiObjectList[WebProxyApigateway6RealserversItemObject]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: FortiObjectList[WebProxyApigateway6SslciphersuitesItemObject]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]


class WebProxyApigatewayQuicObject(FortiObject):
    """Nested object for api-gateway.quic field with attribute access."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class WebProxyApigateway6QuicObject(FortiObject):
    """Nested object for api-gateway6.quic field with attribute access."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class WebProxyObject(FortiObject):
    """Typed FortiObject for WebProxy with field access."""
    name: str
    vip: str
    host: str
    decrypted_traffic_mirror: str
    log_blocked_traffic: Literal["disable", "enable"]
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    vip6: str
    svr_pool_multiplex: Literal["enable", "disable"]
    svr_pool_ttl: int
    svr_pool_server_max_request: int
    svr_pool_server_max_concurrent_request: int
    api_gateway: FortiObjectList[WebProxyApigatewayItemObject]
    api_gateway6: FortiObjectList[WebProxyApigateway6ItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class WebProxy:
    """
    
    Endpoint: ztna/web_proxy
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
    ) -> WebProxyObject: ...
    
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
    ) -> FortiObjectList[WebProxyObject]: ...
    
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
        payload_dict: WebProxyPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        svr_pool_multiplex: Literal["enable", "disable"] | None = ...,
        svr_pool_ttl: int | None = ...,
        svr_pool_server_max_request: int | None = ...,
        svr_pool_server_max_concurrent_request: int | None = ...,
        api_gateway: str | list[str] | list[WebProxyApigatewayItem] | None = ...,
        api_gateway6: str | list[str] | list[WebProxyApigateway6Item] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WebProxyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: WebProxyPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        svr_pool_multiplex: Literal["enable", "disable"] | None = ...,
        svr_pool_ttl: int | None = ...,
        svr_pool_server_max_request: int | None = ...,
        svr_pool_server_max_concurrent_request: int | None = ...,
        api_gateway: str | list[str] | list[WebProxyApigatewayItem] | None = ...,
        api_gateway6: str | list[str] | list[WebProxyApigateway6Item] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WebProxyObject: ...

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
        payload_dict: WebProxyPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        svr_pool_multiplex: Literal["enable", "disable"] | None = ...,
        svr_pool_ttl: int | None = ...,
        svr_pool_server_max_request: int | None = ...,
        svr_pool_server_max_concurrent_request: int | None = ...,
        api_gateway: str | list[str] | list[WebProxyApigatewayItem] | None = ...,
        api_gateway6: str | list[str] | list[WebProxyApigateway6Item] | None = ...,
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
    "WebProxy",
    "WebProxyPayload",
    "WebProxyResponse",
    "WebProxyObject",
]