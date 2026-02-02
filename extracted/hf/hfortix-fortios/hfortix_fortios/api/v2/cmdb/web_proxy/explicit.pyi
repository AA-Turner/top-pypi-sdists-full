""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: web_proxy/explicit
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

class ExplicitPacpolicySrcaddrItem(TypedDict, total=False):
    """Nested item for pac-policy.srcaddr field."""
    name: str


class ExplicitPacpolicySrcaddr6Item(TypedDict, total=False):
    """Nested item for pac-policy.srcaddr6 field."""
    name: str


class ExplicitPacpolicyDstaddrItem(TypedDict, total=False):
    """Nested item for pac-policy.dstaddr field."""
    name: str


class ExplicitSecurewebproxycertItem(TypedDict, total=False):
    """Nested item for secure-web-proxy-cert field."""
    name: str


class ExplicitPacpolicyItem(TypedDict, total=False):
    """Nested item for pac-policy field."""
    policyid: int
    status: Literal["enable", "disable"]
    srcaddr: str | list[str] | list[ExplicitPacpolicySrcaddrItem]
    srcaddr6: str | list[str] | list[ExplicitPacpolicySrcaddr6Item]
    dstaddr: str | list[str] | list[ExplicitPacpolicyDstaddrItem]
    pac_file_name: str
    pac_file_data: str
    comments: str


class ExplicitPayload(TypedDict, total=False):
    """Payload type for Explicit operations."""
    status: Literal["enable", "disable"]
    secure_web_proxy: Literal["disable", "enable", "secure"]
    ftp_over_http: Literal["enable", "disable"]
    socks: Literal["enable", "disable"]
    http_incoming_port: str
    http_connection_mode: Literal["static", "multiplex", "serverpool"]
    https_incoming_port: str
    secure_web_proxy_cert: str | list[str] | list[ExplicitSecurewebproxycertItem]
    client_cert: Literal["disable", "enable"]
    user_agent_detect: Literal["disable", "enable"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ftp_incoming_port: str
    socks_incoming_port: str
    incoming_ip: str
    outgoing_ip: str | list[str]
    interface_select_method: Literal["sdwan", "specify"]
    interface: str
    vrf_select: int
    ipv6_status: Literal["enable", "disable"]
    incoming_ip6: str
    outgoing_ip6: str | list[str]
    strict_guest: Literal["enable", "disable"]
    pref_dns_result: Literal["ipv4", "ipv6", "ipv4-strict", "ipv6-strict"]
    unknown_http_version: Literal["reject", "best-effort"]
    realm: str
    sec_default_action: Literal["accept", "deny"]
    https_replacement_message: Literal["enable", "disable"]
    message_upon_server_error: Literal["enable", "disable"]
    pac_file_server_status: Literal["enable", "disable"]
    pac_file_url: str
    pac_file_server_port: str
    pac_file_through_https: Literal["enable", "disable"]
    pac_file_name: str
    pac_file_data: str
    pac_policy: str | list[str] | list[ExplicitPacpolicyItem]
    ssl_algorithm: Literal["high", "medium", "low"]
    trace_auth_no_rsp: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExplicitResponse(TypedDict, total=False):
    """Response type for Explicit - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    secure_web_proxy: Literal["disable", "enable", "secure"]
    ftp_over_http: Literal["enable", "disable"]
    socks: Literal["enable", "disable"]
    http_incoming_port: str
    http_connection_mode: Literal["static", "multiplex", "serverpool"]
    https_incoming_port: str
    secure_web_proxy_cert: list[ExplicitSecurewebproxycertItem]
    client_cert: Literal["disable", "enable"]
    user_agent_detect: Literal["disable", "enable"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ftp_incoming_port: str
    socks_incoming_port: str
    incoming_ip: str
    outgoing_ip: str | list[str]
    interface_select_method: Literal["sdwan", "specify"]
    interface: str
    vrf_select: int
    ipv6_status: Literal["enable", "disable"]
    incoming_ip6: str
    outgoing_ip6: str | list[str]
    strict_guest: Literal["enable", "disable"]
    pref_dns_result: Literal["ipv4", "ipv6", "ipv4-strict", "ipv6-strict"]
    unknown_http_version: Literal["reject", "best-effort"]
    realm: str
    sec_default_action: Literal["accept", "deny"]
    https_replacement_message: Literal["enable", "disable"]
    message_upon_server_error: Literal["enable", "disable"]
    pac_file_server_status: Literal["enable", "disable"]
    pac_file_url: str
    pac_file_server_port: str
    pac_file_through_https: Literal["enable", "disable"]
    pac_file_name: str
    pac_file_data: str
    pac_policy: list[ExplicitPacpolicyItem]
    ssl_algorithm: Literal["high", "medium", "low"]
    trace_auth_no_rsp: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExplicitPacpolicySrcaddrItemObject(FortiObject[ExplicitPacpolicySrcaddrItem]):
    """Typed object for pac-policy.srcaddr table items with attribute access."""
    name: str


class ExplicitPacpolicySrcaddr6ItemObject(FortiObject[ExplicitPacpolicySrcaddr6Item]):
    """Typed object for pac-policy.srcaddr6 table items with attribute access."""
    name: str


class ExplicitPacpolicyDstaddrItemObject(FortiObject[ExplicitPacpolicyDstaddrItem]):
    """Typed object for pac-policy.dstaddr table items with attribute access."""
    name: str


class ExplicitSecurewebproxycertItemObject(FortiObject[ExplicitSecurewebproxycertItem]):
    """Typed object for secure-web-proxy-cert table items with attribute access."""
    name: str


class ExplicitPacpolicyItemObject(FortiObject[ExplicitPacpolicyItem]):
    """Typed object for pac-policy table items with attribute access."""
    policyid: int
    status: Literal["enable", "disable"]
    srcaddr: FortiObjectList[ExplicitPacpolicySrcaddrItemObject]
    srcaddr6: FortiObjectList[ExplicitPacpolicySrcaddr6ItemObject]
    dstaddr: FortiObjectList[ExplicitPacpolicyDstaddrItemObject]
    pac_file_name: str
    pac_file_data: str
    comments: str


class ExplicitObject(FortiObject):
    """Typed FortiObject for Explicit with field access."""
    status: Literal["enable", "disable"]
    secure_web_proxy: Literal["disable", "enable", "secure"]
    ftp_over_http: Literal["enable", "disable"]
    socks: Literal["enable", "disable"]
    http_incoming_port: str
    http_connection_mode: Literal["static", "multiplex", "serverpool"]
    https_incoming_port: str
    secure_web_proxy_cert: FortiObjectList[ExplicitSecurewebproxycertItemObject]
    client_cert: Literal["disable", "enable"]
    user_agent_detect: Literal["disable", "enable"]
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ftp_incoming_port: str
    socks_incoming_port: str
    incoming_ip: str
    outgoing_ip: str | list[str]
    interface_select_method: Literal["sdwan", "specify"]
    interface: str
    vrf_select: int
    ipv6_status: Literal["enable", "disable"]
    incoming_ip6: str
    outgoing_ip6: str | list[str]
    strict_guest: Literal["enable", "disable"]
    pref_dns_result: Literal["ipv4", "ipv6", "ipv4-strict", "ipv6-strict"]
    unknown_http_version: Literal["reject", "best-effort"]
    realm: str
    sec_default_action: Literal["accept", "deny"]
    https_replacement_message: Literal["enable", "disable"]
    message_upon_server_error: Literal["enable", "disable"]
    pac_file_server_status: Literal["enable", "disable"]
    pac_file_url: str
    pac_file_server_port: str
    pac_file_through_https: Literal["enable", "disable"]
    pac_file_name: str
    pac_file_data: str
    pac_policy: FortiObjectList[ExplicitPacpolicyItemObject]
    ssl_algorithm: Literal["high", "medium", "low"]
    trace_auth_no_rsp: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Explicit:
    """
    
    Endpoint: web_proxy/explicit
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
    ) -> ExplicitObject: ...
    
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
        payload_dict: ExplicitPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        secure_web_proxy: Literal["disable", "enable", "secure"] | None = ...,
        ftp_over_http: Literal["enable", "disable"] | None = ...,
        socks: Literal["enable", "disable"] | None = ...,
        http_incoming_port: str | None = ...,
        http_connection_mode: Literal["static", "multiplex", "serverpool"] | None = ...,
        https_incoming_port: str | None = ...,
        secure_web_proxy_cert: str | list[str] | list[ExplicitSecurewebproxycertItem] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048"] | None = ...,
        ftp_incoming_port: str | None = ...,
        socks_incoming_port: str | None = ...,
        incoming_ip: str | None = ...,
        outgoing_ip: str | list[str] | None = ...,
        interface_select_method: Literal["sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        ipv6_status: Literal["enable", "disable"] | None = ...,
        incoming_ip6: str | None = ...,
        outgoing_ip6: str | list[str] | None = ...,
        strict_guest: Literal["enable", "disable"] | None = ...,
        pref_dns_result: Literal["ipv4", "ipv6", "ipv4-strict", "ipv6-strict"] | None = ...,
        unknown_http_version: Literal["reject", "best-effort"] | None = ...,
        realm: str | None = ...,
        sec_default_action: Literal["accept", "deny"] | None = ...,
        https_replacement_message: Literal["enable", "disable"] | None = ...,
        message_upon_server_error: Literal["enable", "disable"] | None = ...,
        pac_file_server_status: Literal["enable", "disable"] | None = ...,
        pac_file_url: str | None = ...,
        pac_file_server_port: str | None = ...,
        pac_file_through_https: Literal["enable", "disable"] | None = ...,
        pac_file_name: str | None = ...,
        pac_file_data: str | None = ...,
        pac_policy: str | list[str] | list[ExplicitPacpolicyItem] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low"] | None = ...,
        trace_auth_no_rsp: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExplicitObject: ...


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
        payload_dict: ExplicitPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        secure_web_proxy: Literal["disable", "enable", "secure"] | None = ...,
        ftp_over_http: Literal["enable", "disable"] | None = ...,
        socks: Literal["enable", "disable"] | None = ...,
        http_incoming_port: str | None = ...,
        http_connection_mode: Literal["static", "multiplex", "serverpool"] | None = ...,
        https_incoming_port: str | None = ...,
        secure_web_proxy_cert: str | list[str] | list[ExplicitSecurewebproxycertItem] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048"] | None = ...,
        ftp_incoming_port: str | None = ...,
        socks_incoming_port: str | None = ...,
        incoming_ip: str | None = ...,
        outgoing_ip: str | list[str] | None = ...,
        interface_select_method: Literal["sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        ipv6_status: Literal["enable", "disable"] | None = ...,
        incoming_ip6: str | None = ...,
        outgoing_ip6: str | list[str] | None = ...,
        strict_guest: Literal["enable", "disable"] | None = ...,
        pref_dns_result: Literal["ipv4", "ipv6", "ipv4-strict", "ipv6-strict"] | None = ...,
        unknown_http_version: Literal["reject", "best-effort"] | None = ...,
        realm: str | None = ...,
        sec_default_action: Literal["accept", "deny"] | None = ...,
        https_replacement_message: Literal["enable", "disable"] | None = ...,
        message_upon_server_error: Literal["enable", "disable"] | None = ...,
        pac_file_server_status: Literal["enable", "disable"] | None = ...,
        pac_file_url: str | None = ...,
        pac_file_server_port: str | None = ...,
        pac_file_through_https: Literal["enable", "disable"] | None = ...,
        pac_file_name: str | None = ...,
        pac_file_data: str | None = ...,
        pac_policy: str | list[str] | list[ExplicitPacpolicyItem] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low"] | None = ...,
        trace_auth_no_rsp: Literal["enable", "disable"] | None = ...,
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
    "Explicit",
    "ExplicitPayload",
    "ExplicitResponse",
    "ExplicitObject",
]