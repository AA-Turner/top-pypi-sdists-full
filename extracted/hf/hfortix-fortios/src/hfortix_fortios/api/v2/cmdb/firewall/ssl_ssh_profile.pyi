""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/ssl_ssh_profile
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

class SslSshProfileSslDict(TypedDict, total=False):
    """Nested object type for ssl field."""
    inspect_all: Literal["disable", "certificate-inspection", "deep-inspection"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]
    cert_probe_failure: Literal["allow", "block"]
    encrypted_client_hello: Literal["allow", "block"]
    min_allowed_ssl_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class SslSshProfileHttpsDict(TypedDict, total=False):
    """Nested object type for https field."""
    ports: int | list[int]
    status: Literal["disable", "certificate-inspection", "deep-inspection"]
    quic: Literal["inspect", "bypass", "block"]
    udp_not_quic: Literal["allow", "block"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]
    cert_probe_failure: Literal["allow", "block"]
    encrypted_client_hello: Literal["allow", "block"]
    min_allowed_ssl_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class SslSshProfileFtpsDict(TypedDict, total=False):
    """Nested object type for ftps field."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]
    min_allowed_ssl_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class SslSshProfileImapsDict(TypedDict, total=False):
    """Nested object type for imaps field."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfilePop3sDict(TypedDict, total=False):
    """Nested object type for pop3s field."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfileSmtpsDict(TypedDict, total=False):
    """Nested object type for smtps field."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfileSshDict(TypedDict, total=False):
    """Nested object type for ssh field."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    inspect_all: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    unsupported_version: Literal["bypass", "block"]
    ssh_tun_policy_check: Literal["disable", "enable"]
    ssh_algorithm: Literal["compatible", "high-encryption"]


class SslSshProfileDotDict(TypedDict, total=False):
    """Nested object type for dot field."""
    status: Literal["disable", "deep-inspection"]
    quic: Literal["inspect", "bypass", "block"]
    udp_not_quic: Literal["allow", "block"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfileSslexemptItem(TypedDict, total=False):
    """Nested item for ssl-exempt field."""
    id: int
    type: Literal["fortiguard-category", "address", "address6", "wildcard-fqdn", "regex"]
    fortiguard_category: int
    address: str
    address6: str
    wildcard_fqdn: str
    regex: str


class SslSshProfileEchoutersniItem(TypedDict, total=False):
    """Nested item for ech-outer-sni field."""
    name: str
    sni: str


class SslSshProfileServercertItem(TypedDict, total=False):
    """Nested item for server-cert field."""
    name: str


class SslSshProfileSslserverItem(TypedDict, total=False):
    """Nested item for ssl-server field."""
    id: int
    ip: str
    https_client_certificate: Literal["bypass", "inspect", "block"]
    smtps_client_certificate: Literal["bypass", "inspect", "block"]
    pop3s_client_certificate: Literal["bypass", "inspect", "block"]
    imaps_client_certificate: Literal["bypass", "inspect", "block"]
    ftps_client_certificate: Literal["bypass", "inspect", "block"]
    ssl_other_client_certificate: Literal["bypass", "inspect", "block"]


class SslSshProfilePayload(TypedDict, total=False):
    """Payload type for SslSshProfile operations."""
    name: str
    comment: str
    ssl: SslSshProfileSslDict
    https: SslSshProfileHttpsDict
    ftps: SslSshProfileFtpsDict
    imaps: SslSshProfileImapsDict
    pop3s: SslSshProfilePop3sDict
    smtps: SslSshProfileSmtpsDict
    ssh: SslSshProfileSshDict
    dot: SslSshProfileDotDict
    allowlist: Literal["enable", "disable"]
    block_blocklisted_certificates: Literal["disable", "enable"]
    ssl_exempt: str | list[str] | list[SslSshProfileSslexemptItem]
    ech_outer_sni: str | list[str] | list[SslSshProfileEchoutersniItem]
    server_cert_mode: Literal["re-sign", "replace"]
    use_ssl_server: Literal["disable", "enable"]
    caname: str
    untrusted_caname: str
    server_cert: str | list[str] | list[SslSshProfileServercertItem]
    ssl_server: str | list[str] | list[SslSshProfileSslserverItem]
    ssl_exemption_ip_rating: Literal["enable", "disable"]
    ssl_exemption_log: Literal["disable", "enable"]
    ssl_anomaly_log: Literal["disable", "enable"]
    ssl_negotiation_log: Literal["disable", "enable"]
    ssl_server_cert_log: Literal["disable", "enable"]
    ssl_handshake_log: Literal["disable", "enable"]
    rpc_over_https: Literal["enable", "disable"]
    mapi_over_https: Literal["enable", "disable"]
    supported_alpn: Literal["http1-1", "http2", "all", "none"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SslSshProfileResponse(TypedDict, total=False):
    """Response type for SslSshProfile - use with .dict property for typed dict access."""
    name: str
    comment: str
    ssl: SslSshProfileSslDict
    https: SslSshProfileHttpsDict
    ftps: SslSshProfileFtpsDict
    imaps: SslSshProfileImapsDict
    pop3s: SslSshProfilePop3sDict
    smtps: SslSshProfileSmtpsDict
    ssh: SslSshProfileSshDict
    dot: SslSshProfileDotDict
    allowlist: Literal["enable", "disable"]
    block_blocklisted_certificates: Literal["disable", "enable"]
    ssl_exempt: list[SslSshProfileSslexemptItem]
    ech_outer_sni: list[SslSshProfileEchoutersniItem]
    server_cert_mode: Literal["re-sign", "replace"]
    use_ssl_server: Literal["disable", "enable"]
    caname: str
    untrusted_caname: str
    server_cert: list[SslSshProfileServercertItem]
    ssl_server: list[SslSshProfileSslserverItem]
    ssl_exemption_ip_rating: Literal["enable", "disable"]
    ssl_exemption_log: Literal["disable", "enable"]
    ssl_anomaly_log: Literal["disable", "enable"]
    ssl_negotiation_log: Literal["disable", "enable"]
    ssl_server_cert_log: Literal["disable", "enable"]
    ssl_handshake_log: Literal["disable", "enable"]
    rpc_over_https: Literal["enable", "disable"]
    mapi_over_https: Literal["enable", "disable"]
    supported_alpn: Literal["http1-1", "http2", "all", "none"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SslSshProfileSslexemptItemObject(FortiObject[SslSshProfileSslexemptItem]):
    """Typed object for ssl-exempt table items with attribute access."""
    id: int
    type: Literal["fortiguard-category", "address", "address6", "wildcard-fqdn", "regex"]
    fortiguard_category: int
    address: str
    address6: str
    wildcard_fqdn: str
    regex: str


class SslSshProfileEchoutersniItemObject(FortiObject[SslSshProfileEchoutersniItem]):
    """Typed object for ech-outer-sni table items with attribute access."""
    name: str
    sni: str


class SslSshProfileServercertItemObject(FortiObject[SslSshProfileServercertItem]):
    """Typed object for server-cert table items with attribute access."""
    name: str


class SslSshProfileSslserverItemObject(FortiObject[SslSshProfileSslserverItem]):
    """Typed object for ssl-server table items with attribute access."""
    id: int
    ip: str
    https_client_certificate: Literal["bypass", "inspect", "block"]
    smtps_client_certificate: Literal["bypass", "inspect", "block"]
    pop3s_client_certificate: Literal["bypass", "inspect", "block"]
    imaps_client_certificate: Literal["bypass", "inspect", "block"]
    ftps_client_certificate: Literal["bypass", "inspect", "block"]
    ssl_other_client_certificate: Literal["bypass", "inspect", "block"]


class SslSshProfileSslObject(FortiObject):
    """Nested object for ssl field with attribute access."""
    inspect_all: Literal["disable", "certificate-inspection", "deep-inspection"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]
    cert_probe_failure: Literal["allow", "block"]
    encrypted_client_hello: Literal["allow", "block"]
    min_allowed_ssl_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class SslSshProfileHttpsObject(FortiObject):
    """Nested object for https field with attribute access."""
    ports: int | list[int]
    status: Literal["disable", "certificate-inspection", "deep-inspection"]
    quic: Literal["inspect", "bypass", "block"]
    udp_not_quic: Literal["allow", "block"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]
    cert_probe_failure: Literal["allow", "block"]
    encrypted_client_hello: Literal["allow", "block"]
    min_allowed_ssl_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class SslSshProfileFtpsObject(FortiObject):
    """Nested object for ftps field with attribute access."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]
    min_allowed_ssl_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]


class SslSshProfileImapsObject(FortiObject):
    """Nested object for imaps field with attribute access."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfilePop3sObject(FortiObject):
    """Nested object for pop3s field with attribute access."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfileSmtpsObject(FortiObject):
    """Nested object for smtps field with attribute access."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfileSshObject(FortiObject):
    """Nested object for ssh field with attribute access."""
    ports: int | list[int]
    status: Literal["disable", "deep-inspection"]
    inspect_all: Literal["disable", "deep-inspection"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    unsupported_version: Literal["bypass", "block"]
    ssh_tun_policy_check: Literal["disable", "enable"]
    ssh_algorithm: Literal["compatible", "high-encryption"]


class SslSshProfileDotObject(FortiObject):
    """Nested object for dot field with attribute access."""
    status: Literal["disable", "deep-inspection"]
    quic: Literal["inspect", "bypass", "block"]
    udp_not_quic: Literal["allow", "block"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    client_certificate: Literal["bypass", "inspect", "block"]
    unsupported_ssl_version: Literal["allow", "block"]
    unsupported_ssl_cipher: Literal["allow", "block"]
    unsupported_ssl_negotiation: Literal["allow", "block"]
    expired_server_cert: Literal["allow", "block", "ignore"]
    revoked_server_cert: Literal["allow", "block", "ignore"]
    untrusted_server_cert: Literal["allow", "block", "ignore"]
    cert_validation_timeout: Literal["allow", "block", "ignore"]
    cert_validation_failure: Literal["allow", "block", "ignore"]
    sni_server_cert_check: Literal["enable", "strict", "disable"]


class SslSshProfileObject(FortiObject):
    """Typed FortiObject for SslSshProfile with field access."""
    name: str
    comment: str
    ssl: SslSshProfileSslObject
    https: SslSshProfileHttpsObject
    ftps: SslSshProfileFtpsObject
    imaps: SslSshProfileImapsObject
    pop3s: SslSshProfilePop3sObject
    smtps: SslSshProfileSmtpsObject
    ssh: SslSshProfileSshObject
    dot: SslSshProfileDotObject
    allowlist: Literal["enable", "disable"]
    block_blocklisted_certificates: Literal["disable", "enable"]
    ssl_exempt: FortiObjectList[SslSshProfileSslexemptItemObject]
    ech_outer_sni: FortiObjectList[SslSshProfileEchoutersniItemObject]
    server_cert_mode: Literal["re-sign", "replace"]
    use_ssl_server: Literal["disable", "enable"]
    caname: str
    untrusted_caname: str
    server_cert: FortiObjectList[SslSshProfileServercertItemObject]
    ssl_server: FortiObjectList[SslSshProfileSslserverItemObject]
    ssl_exemption_ip_rating: Literal["enable", "disable"]
    ssl_exemption_log: Literal["disable", "enable"]
    ssl_anomaly_log: Literal["disable", "enable"]
    ssl_negotiation_log: Literal["disable", "enable"]
    ssl_server_cert_log: Literal["disable", "enable"]
    ssl_handshake_log: Literal["disable", "enable"]
    rpc_over_https: Literal["enable", "disable"]
    mapi_over_https: Literal["enable", "disable"]
    supported_alpn: Literal["http1-1", "http2", "all", "none"]


# ================================================================
# Main Endpoint Class
# ================================================================

class SslSshProfile:
    """
    
    Endpoint: firewall/ssl_ssh_profile
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
    ) -> SslSshProfileObject: ...
    
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
    ) -> FortiObjectList[SslSshProfileObject]: ...
    
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
        payload_dict: SslSshProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        ssl: SslSshProfileSslDict | None = ...,
        https: SslSshProfileHttpsDict | None = ...,
        ftps: SslSshProfileFtpsDict | None = ...,
        imaps: SslSshProfileImapsDict | None = ...,
        pop3s: SslSshProfilePop3sDict | None = ...,
        smtps: SslSshProfileSmtpsDict | None = ...,
        ssh: SslSshProfileSshDict | None = ...,
        dot: SslSshProfileDotDict | None = ...,
        allowlist: Literal["enable", "disable"] | None = ...,
        block_blocklisted_certificates: Literal["disable", "enable"] | None = ...,
        ssl_exempt: str | list[str] | list[SslSshProfileSslexemptItem] | None = ...,
        ech_outer_sni: str | list[str] | list[SslSshProfileEchoutersniItem] | None = ...,
        server_cert_mode: Literal["re-sign", "replace"] | None = ...,
        use_ssl_server: Literal["disable", "enable"] | None = ...,
        caname: str | None = ...,
        untrusted_caname: str | None = ...,
        server_cert: str | list[str] | list[SslSshProfileServercertItem] | None = ...,
        ssl_server: str | list[str] | list[SslSshProfileSslserverItem] | None = ...,
        ssl_exemption_ip_rating: Literal["enable", "disable"] | None = ...,
        ssl_exemption_log: Literal["disable", "enable"] | None = ...,
        ssl_anomaly_log: Literal["disable", "enable"] | None = ...,
        ssl_negotiation_log: Literal["disable", "enable"] | None = ...,
        ssl_server_cert_log: Literal["disable", "enable"] | None = ...,
        ssl_handshake_log: Literal["disable", "enable"] | None = ...,
        rpc_over_https: Literal["enable", "disable"] | None = ...,
        mapi_over_https: Literal["enable", "disable"] | None = ...,
        supported_alpn: Literal["http1-1", "http2", "all", "none"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SslSshProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SslSshProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        ssl: SslSshProfileSslDict | None = ...,
        https: SslSshProfileHttpsDict | None = ...,
        ftps: SslSshProfileFtpsDict | None = ...,
        imaps: SslSshProfileImapsDict | None = ...,
        pop3s: SslSshProfilePop3sDict | None = ...,
        smtps: SslSshProfileSmtpsDict | None = ...,
        ssh: SslSshProfileSshDict | None = ...,
        dot: SslSshProfileDotDict | None = ...,
        allowlist: Literal["enable", "disable"] | None = ...,
        block_blocklisted_certificates: Literal["disable", "enable"] | None = ...,
        ssl_exempt: str | list[str] | list[SslSshProfileSslexemptItem] | None = ...,
        ech_outer_sni: str | list[str] | list[SslSshProfileEchoutersniItem] | None = ...,
        server_cert_mode: Literal["re-sign", "replace"] | None = ...,
        use_ssl_server: Literal["disable", "enable"] | None = ...,
        caname: str | None = ...,
        untrusted_caname: str | None = ...,
        server_cert: str | list[str] | list[SslSshProfileServercertItem] | None = ...,
        ssl_server: str | list[str] | list[SslSshProfileSslserverItem] | None = ...,
        ssl_exemption_ip_rating: Literal["enable", "disable"] | None = ...,
        ssl_exemption_log: Literal["disable", "enable"] | None = ...,
        ssl_anomaly_log: Literal["disable", "enable"] | None = ...,
        ssl_negotiation_log: Literal["disable", "enable"] | None = ...,
        ssl_server_cert_log: Literal["disable", "enable"] | None = ...,
        ssl_handshake_log: Literal["disable", "enable"] | None = ...,
        rpc_over_https: Literal["enable", "disable"] | None = ...,
        mapi_over_https: Literal["enable", "disable"] | None = ...,
        supported_alpn: Literal["http1-1", "http2", "all", "none"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SslSshProfileObject: ...

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
        payload_dict: SslSshProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        ssl: SslSshProfileSslDict | None = ...,
        https: SslSshProfileHttpsDict | None = ...,
        ftps: SslSshProfileFtpsDict | None = ...,
        imaps: SslSshProfileImapsDict | None = ...,
        pop3s: SslSshProfilePop3sDict | None = ...,
        smtps: SslSshProfileSmtpsDict | None = ...,
        ssh: SslSshProfileSshDict | None = ...,
        dot: SslSshProfileDotDict | None = ...,
        allowlist: Literal["enable", "disable"] | None = ...,
        block_blocklisted_certificates: Literal["disable", "enable"] | None = ...,
        ssl_exempt: str | list[str] | list[SslSshProfileSslexemptItem] | None = ...,
        ech_outer_sni: str | list[str] | list[SslSshProfileEchoutersniItem] | None = ...,
        server_cert_mode: Literal["re-sign", "replace"] | None = ...,
        use_ssl_server: Literal["disable", "enable"] | None = ...,
        caname: str | None = ...,
        untrusted_caname: str | None = ...,
        server_cert: str | list[str] | list[SslSshProfileServercertItem] | None = ...,
        ssl_server: str | list[str] | list[SslSshProfileSslserverItem] | None = ...,
        ssl_exemption_ip_rating: Literal["enable", "disable"] | None = ...,
        ssl_exemption_log: Literal["disable", "enable"] | None = ...,
        ssl_anomaly_log: Literal["disable", "enable"] | None = ...,
        ssl_negotiation_log: Literal["disable", "enable"] | None = ...,
        ssl_server_cert_log: Literal["disable", "enable"] | None = ...,
        ssl_handshake_log: Literal["disable", "enable"] | None = ...,
        rpc_over_https: Literal["enable", "disable"] | None = ...,
        mapi_over_https: Literal["enable", "disable"] | None = ...,
        supported_alpn: Literal["http1-1", "http2", "all", "none"] | None = ...,
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
    "SslSshProfile",
    "SslSshProfilePayload",
    "SslSshProfileResponse",
    "SslSshProfileObject",
]