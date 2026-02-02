""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/exchange
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

class ExchangeKdcipItem(TypedDict, total=False):
    """Nested item for kdc-ip field."""
    ipv4: str


class ExchangePayload(TypedDict, total=False):
    """Payload type for Exchange operations."""
    name: str
    server_name: str
    domain_name: str
    username: str
    password: str
    ip: str
    connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"]
    validate_server_certificate: Literal["disable", "enable"]
    auth_type: Literal["spnego", "ntlm", "kerberos"]
    auth_level: Literal["connect", "call", "packet", "integrity", "privacy"]
    http_auth_type: Literal["basic", "ntlm"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    auto_discover_kdc: Literal["enable", "disable"]
    kdc_ip: str | list[str] | list[ExchangeKdcipItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExchangeResponse(TypedDict, total=False):
    """Response type for Exchange - use with .dict property for typed dict access."""
    name: str
    server_name: str
    domain_name: str
    username: str
    password: str
    ip: str
    connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"]
    validate_server_certificate: Literal["disable", "enable"]
    auth_type: Literal["spnego", "ntlm", "kerberos"]
    auth_level: Literal["connect", "call", "packet", "integrity", "privacy"]
    http_auth_type: Literal["basic", "ntlm"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    auto_discover_kdc: Literal["enable", "disable"]
    kdc_ip: list[ExchangeKdcipItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExchangeKdcipItemObject(FortiObject[ExchangeKdcipItem]):
    """Typed object for kdc-ip table items with attribute access."""
    ipv4: str


class ExchangeObject(FortiObject):
    """Typed FortiObject for Exchange with field access."""
    name: str
    server_name: str
    domain_name: str
    username: str
    password: str
    ip: str
    connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"]
    validate_server_certificate: Literal["disable", "enable"]
    auth_type: Literal["spnego", "ntlm", "kerberos"]
    auth_level: Literal["connect", "call", "packet", "integrity", "privacy"]
    http_auth_type: Literal["basic", "ntlm"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    auto_discover_kdc: Literal["enable", "disable"]
    kdc_ip: FortiObjectList[ExchangeKdcipItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Exchange:
    """
    
    Endpoint: user/exchange
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
    ) -> ExchangeObject: ...
    
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
    ) -> FortiObjectList[ExchangeObject]: ...
    
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
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[ExchangeKdcipItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExchangeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[ExchangeKdcipItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExchangeObject: ...

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
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[ExchangeKdcipItem] | None = ...,
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
    "Exchange",
    "ExchangePayload",
    "ExchangeResponse",
    "ExchangeObject",
]