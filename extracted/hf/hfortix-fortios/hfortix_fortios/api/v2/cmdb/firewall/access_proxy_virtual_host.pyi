""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/access_proxy_virtual_host
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

class AccessProxyVirtualHostSslcertificateItem(TypedDict, total=False):
    """Nested item for ssl-certificate field."""
    name: str


class AccessProxyVirtualHostPayload(TypedDict, total=False):
    """Payload type for AccessProxyVirtualHost operations."""
    name: str
    ssl_certificate: str | list[str] | list[AccessProxyVirtualHostSslcertificateItem]
    host: str
    host_type: Literal["sub-string", "wildcard"]
    replacemsg_group: str
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AccessProxyVirtualHostResponse(TypedDict, total=False):
    """Response type for AccessProxyVirtualHost - use with .dict property for typed dict access."""
    name: str
    ssl_certificate: list[AccessProxyVirtualHostSslcertificateItem]
    host: str
    host_type: Literal["sub-string", "wildcard"]
    replacemsg_group: str
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AccessProxyVirtualHostSslcertificateItemObject(FortiObject[AccessProxyVirtualHostSslcertificateItem]):
    """Typed object for ssl-certificate table items with attribute access."""
    name: str


class AccessProxyVirtualHostObject(FortiObject):
    """Typed FortiObject for AccessProxyVirtualHost with field access."""
    name: str
    ssl_certificate: FortiObjectList[AccessProxyVirtualHostSslcertificateItemObject]
    host: str
    host_type: Literal["sub-string", "wildcard"]
    replacemsg_group: str
    empty_cert_action: Literal["accept", "block", "accept-unmanageable"]
    user_agent_detect: Literal["disable", "enable"]
    client_cert: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class AccessProxyVirtualHost:
    """
    
    Endpoint: firewall/access_proxy_virtual_host
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
    ) -> AccessProxyVirtualHostObject: ...
    
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
    ) -> FortiObjectList[AccessProxyVirtualHostObject]: ...
    
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
        payload_dict: AccessProxyVirtualHostPayload | None = ...,
        name: str | None = ...,
        ssl_certificate: str | list[str] | list[AccessProxyVirtualHostSslcertificateItem] | None = ...,
        host: str | None = ...,
        host_type: Literal["sub-string", "wildcard"] | None = ...,
        replacemsg_group: str | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessProxyVirtualHostObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AccessProxyVirtualHostPayload | None = ...,
        name: str | None = ...,
        ssl_certificate: str | list[str] | list[AccessProxyVirtualHostSslcertificateItem] | None = ...,
        host: str | None = ...,
        host_type: Literal["sub-string", "wildcard"] | None = ...,
        replacemsg_group: str | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessProxyVirtualHostObject: ...

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
        payload_dict: AccessProxyVirtualHostPayload | None = ...,
        name: str | None = ...,
        ssl_certificate: str | list[str] | list[AccessProxyVirtualHostSslcertificateItem] | None = ...,
        host: str | None = ...,
        host_type: Literal["sub-string", "wildcard"] | None = ...,
        replacemsg_group: str | None = ...,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = ...,
        user_agent_detect: Literal["disable", "enable"] | None = ...,
        client_cert: Literal["disable", "enable"] | None = ...,
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
    "AccessProxyVirtualHost",
    "AccessProxyVirtualHostPayload",
    "AccessProxyVirtualHostResponse",
    "AccessProxyVirtualHostObject",
]