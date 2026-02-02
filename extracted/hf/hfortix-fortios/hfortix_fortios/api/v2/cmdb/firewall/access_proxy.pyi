""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/access_proxy
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

class AccessProxyApigatewayQuicDict(TypedDict, total=False):
    """Nested object type for api-gateway.quic field."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class AccessProxyApigatewayRealserversItem(TypedDict, total=False):
    """Nested item for api-gateway.realservers field."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    domain: str
    port: int
    mappedport: str
    status: Literal["active", "standby", "disable"]
    type: Literal["tcp-forwarding", "ssh"]
    external_auth: Literal["enable", "disable"]
    tunnel_encryption: Literal["enable", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    ssh_client_cert: str
    ssh_host_key_validation: Literal["disable", "enable"]
    ssh_host_key: str | list[str]
    verify_cert: Literal["enable", "disable"]


class AccessProxyApigatewayApplicationItem(TypedDict, total=False):
    """Nested item for api-gateway.application field."""
    name: str


class AccessProxyApigatewaySslciphersuitesItem(TypedDict, total=False):
    """Nested item for api-gateway.ssl-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class AccessProxyApigateway6QuicDict(TypedDict, total=False):
    """Nested object type for api-gateway6.quic field."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class AccessProxyApigateway6RealserversItem(TypedDict, total=False):
    """Nested item for api-gateway6.realservers field."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    domain: str
    port: int
    mappedport: str
    status: Literal["active", "standby", "disable"]
    type: Literal["tcp-forwarding", "ssh"]
    external_auth: Literal["enable", "disable"]
    tunnel_encryption: Literal["enable", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    ssh_client_cert: str
    ssh_host_key_validation: Literal["disable", "enable"]
    ssh_host_key: str | list[str]
    verify_cert: Literal["enable", "disable"]


class AccessProxyApigateway6ApplicationItem(TypedDict, total=False):
    """Nested item for api-gateway6.application field."""
    name: str


class AccessProxyApigateway6SslciphersuitesItem(TypedDict, total=False):
    """Nested item for api-gateway6.ssl-cipher-suites field."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class AccessProxyApigatewayItem(TypedDict, total=False):
    """Nested item for api-gateway field."""
    id: int
    url_map: str
    service: Literal["http", "https", "tcp-forwarding", "samlsp", "web-portal", "saas"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    virtual_host: str
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: AccessProxyApigatewayQuicDict
    realservers: str | list[str] | list[AccessProxyApigatewayRealserversItem]
    application: str | list[str] | list[AccessProxyApigatewayApplicationItem]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    saml_server: str
    saml_redirect: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: str | list[str] | list[AccessProxyApigatewaySslciphersuitesItem]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]
    ssl_vpn_web_portal: str


class AccessProxyApigateway6Item(TypedDict, total=False):
    """Nested item for api-gateway6 field."""
    id: int
    url_map: str
    service: Literal["http", "https", "tcp-forwarding", "samlsp", "web-portal", "saas"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    virtual_host: str
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: AccessProxyApigateway6QuicDict
    realservers: str | list[str] | list[AccessProxyApigateway6RealserversItem]
    application: str | list[str] | list[AccessProxyApigateway6ApplicationItem]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    saml_server: str
    saml_redirect: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: str | list[str] | list[AccessProxyApigateway6SslciphersuitesItem]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]
    ssl_vpn_web_portal: str


class AccessProxyPayload(TypedDict, total=False):
    """Payload type for AccessProxy operations."""
    name: str
    vip: str
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    log_blocked_traffic: Literal["enable", "disable"]
    add_vhost_domain_to_dnsdb: Literal["enable", "disable"]
    svr_pool_multiplex: Literal["enable", "disable"]
    svr_pool_ttl: int
    svr_pool_server_max_request: int
    svr_pool_server_max_concurrent_request: int
    decrypted_traffic_mirror: str
    api_gateway: str | list[str] | list[AccessProxyApigatewayItem]
    api_gateway6: str | list[str] | list[AccessProxyApigateway6Item]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AccessProxyResponse(TypedDict, total=False):
    """Response type for AccessProxy - use with .dict property for typed dict access."""
    name: str
    vip: str
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    log_blocked_traffic: Literal["enable", "disable"]
    add_vhost_domain_to_dnsdb: Literal["enable", "disable"]
    svr_pool_multiplex: Literal["enable", "disable"]
    svr_pool_ttl: int
    svr_pool_server_max_request: int
    svr_pool_server_max_concurrent_request: int
    decrypted_traffic_mirror: str
    api_gateway: list[AccessProxyApigatewayItem]
    api_gateway6: list[AccessProxyApigateway6Item]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AccessProxyApigatewayRealserversItemObject(FortiObject[AccessProxyApigatewayRealserversItem]):
    """Typed object for api-gateway.realservers table items with attribute access."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    domain: str
    port: int
    mappedport: str
    status: Literal["active", "standby", "disable"]
    type: Literal["tcp-forwarding", "ssh"]
    external_auth: Literal["enable", "disable"]
    tunnel_encryption: Literal["enable", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    ssh_client_cert: str
    ssh_host_key_validation: Literal["disable", "enable"]
    ssh_host_key: str | list[str]
    verify_cert: Literal["enable", "disable"]


class AccessProxyApigatewayApplicationItemObject(FortiObject[AccessProxyApigatewayApplicationItem]):
    """Typed object for api-gateway.application table items with attribute access."""
    name: str


class AccessProxyApigatewaySslciphersuitesItemObject(FortiObject[AccessProxyApigatewaySslciphersuitesItem]):
    """Typed object for api-gateway.ssl-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class AccessProxyApigateway6RealserversItemObject(FortiObject[AccessProxyApigateway6RealserversItem]):
    """Typed object for api-gateway6.realservers table items with attribute access."""
    id: int
    addr_type: Literal["ip", "fqdn"]
    address: str
    ip: str
    domain: str
    port: int
    mappedport: str
    status: Literal["active", "standby", "disable"]
    type: Literal["tcp-forwarding", "ssh"]
    external_auth: Literal["enable", "disable"]
    tunnel_encryption: Literal["enable", "disable"]
    weight: int
    http_host: str
    health_check: Literal["disable", "enable"]
    health_check_proto: Literal["ping", "http", "tcp-connect"]
    holddown_interval: Literal["enable", "disable"]
    translate_host: Literal["enable", "disable"]
    ssh_client_cert: str
    ssh_host_key_validation: Literal["disable", "enable"]
    ssh_host_key: str | list[str]
    verify_cert: Literal["enable", "disable"]


class AccessProxyApigateway6ApplicationItemObject(FortiObject[AccessProxyApigateway6ApplicationItem]):
    """Typed object for api-gateway6.application table items with attribute access."""
    name: str


class AccessProxyApigateway6SslciphersuitesItemObject(FortiObject[AccessProxyApigateway6SslciphersuitesItem]):
    """Typed object for api-gateway6.ssl-cipher-suites table items with attribute access."""
    priority: int
    cipher: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"]
    versions: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class AccessProxyApigatewayItemObject(FortiObject[AccessProxyApigatewayItem]):
    """Typed object for api-gateway table items with attribute access."""
    id: int
    url_map: str
    service: Literal["http", "https", "tcp-forwarding", "samlsp", "web-portal", "saas"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    virtual_host: str
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: AccessProxyApigatewayQuicObject
    realservers: FortiObjectList[AccessProxyApigatewayRealserversItemObject]
    application: FortiObjectList[AccessProxyApigatewayApplicationItemObject]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    saml_server: str
    saml_redirect: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: FortiObjectList[AccessProxyApigatewaySslciphersuitesItemObject]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]
    ssl_vpn_web_portal: str


class AccessProxyApigateway6ItemObject(FortiObject[AccessProxyApigateway6Item]):
    """Typed object for api-gateway6 table items with attribute access."""
    id: int
    url_map: str
    service: Literal["http", "https", "tcp-forwarding", "samlsp", "web-portal", "saas"]
    ldb_method: Literal["static", "round-robin", "weighted", "first-alive", "http-host"]
    virtual_host: str
    url_map_type: Literal["sub-string", "wildcard", "regex"]
    h2_support: Literal["enable", "disable"]
    h3_support: Literal["enable", "disable"]
    quic: AccessProxyApigateway6QuicObject
    realservers: FortiObjectList[AccessProxyApigateway6RealserversItemObject]
    application: FortiObjectList[AccessProxyApigateway6ApplicationItemObject]
    persistence: Literal["none", "http-cookie"]
    http_cookie_domain_from_host: Literal["disable", "enable"]
    http_cookie_domain: str
    http_cookie_path: str
    http_cookie_generation: int
    http_cookie_age: int
    http_cookie_share: Literal["disable", "same-ip"]
    https_cookie_secure: Literal["disable", "enable"]
    saml_server: str
    saml_redirect: Literal["disable", "enable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048", "3072", "4096"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_cipher_suites: FortiObjectList[AccessProxyApigateway6SslciphersuitesItemObject]
    ssl_min_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_renegotiation: Literal["enable", "disable"]
    ssl_vpn_web_portal: str


class AccessProxyApigatewayQuicObject(FortiObject):
    """Nested object for api-gateway.quic field with attribute access."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class AccessProxyApigateway6QuicObject(FortiObject):
    """Nested object for api-gateway6.quic field with attribute access."""
    max_idle_timeout: int
    max_udp_payload_size: int
    active_connection_id_limit: int
    ack_delay_exponent: int
    max_ack_delay: int
    max_datagram_frame_size: int
    active_migration: Literal["enable", "disable"]
    grease_quic_bit: Literal["enable", "disable"]


class AccessProxyObject(FortiObject):
    """Typed FortiObject for AccessProxy with field access."""
    name: str
    vip: str
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    log_blocked_traffic: Literal["enable", "disable"]
    add_vhost_domain_to_dnsdb: Literal["enable", "disable"]
    svr_pool_multiplex: Literal["enable", "disable"]
    svr_pool_ttl: int
    svr_pool_server_max_request: int
    svr_pool_server_max_concurrent_request: int
    decrypted_traffic_mirror: str
    api_gateway: FortiObjectList[AccessProxyApigatewayItemObject]
    api_gateway6: FortiObjectList[AccessProxyApigateway6ItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class AccessProxy:
    """
    
    Endpoint: firewall/access_proxy
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
    ) -> AccessProxyObject: ...
    
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
    ) -> FortiObjectList[AccessProxyObject]: ...
    
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
        payload_dict: AccessProxyPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        log_blocked_traffic: Literal["enable", "disable"] | None = ...,
        add_vhost_domain_to_dnsdb: Literal["enable", "disable"] | None = ...,
        svr_pool_multiplex: Literal["enable", "disable"] | None = ...,
        svr_pool_ttl: int | None = ...,
        svr_pool_server_max_request: int | None = ...,
        svr_pool_server_max_concurrent_request: int | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        api_gateway: str | list[str] | list[AccessProxyApigatewayItem] | None = ...,
        api_gateway6: str | list[str] | list[AccessProxyApigateway6Item] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessProxyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AccessProxyPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        log_blocked_traffic: Literal["enable", "disable"] | None = ...,
        add_vhost_domain_to_dnsdb: Literal["enable", "disable"] | None = ...,
        svr_pool_multiplex: Literal["enable", "disable"] | None = ...,
        svr_pool_ttl: int | None = ...,
        svr_pool_server_max_request: int | None = ...,
        svr_pool_server_max_concurrent_request: int | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        api_gateway: str | list[str] | list[AccessProxyApigatewayItem] | None = ...,
        api_gateway6: str | list[str] | list[AccessProxyApigateway6Item] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessProxyObject: ...

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
        payload_dict: AccessProxyPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        log_blocked_traffic: Literal["enable", "disable"] | None = ...,
        add_vhost_domain_to_dnsdb: Literal["enable", "disable"] | None = ...,
        svr_pool_multiplex: Literal["enable", "disable"] | None = ...,
        svr_pool_ttl: int | None = ...,
        svr_pool_server_max_request: int | None = ...,
        svr_pool_server_max_concurrent_request: int | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        api_gateway: str | list[str] | list[AccessProxyApigatewayItem] | None = ...,
        api_gateway6: str | list[str] | list[AccessProxyApigateway6Item] | None = ...,
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
    "AccessProxy",
    "AccessProxyPayload",
    "AccessProxyResponse",
    "AccessProxyObject",
]