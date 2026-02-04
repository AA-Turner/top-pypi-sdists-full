""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/access_proxy_ssh_client_cert
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

class AccessProxySshClientCertCertextensionItem(TypedDict, total=False):
    """Nested item for cert-extension field."""
    name: str
    critical: Literal["no", "yes"]
    type: Literal["fixed", "user"]
    data: str


class AccessProxySshClientCertPayload(TypedDict, total=False):
    """Payload type for AccessProxySshClientCert operations."""
    name: str
    source_address: Literal["enable", "disable"]
    permit_x11_forwarding: Literal["enable", "disable"]
    permit_agent_forwarding: Literal["enable", "disable"]
    permit_port_forwarding: Literal["enable", "disable"]
    permit_pty: Literal["enable", "disable"]
    permit_user_rc: Literal["enable", "disable"]
    cert_extension: str | list[str] | list[AccessProxySshClientCertCertextensionItem]
    auth_ca: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AccessProxySshClientCertResponse(TypedDict, total=False):
    """Response type for AccessProxySshClientCert - use with .dict property for typed dict access."""
    name: str
    source_address: Literal["enable", "disable"]
    permit_x11_forwarding: Literal["enable", "disable"]
    permit_agent_forwarding: Literal["enable", "disable"]
    permit_port_forwarding: Literal["enable", "disable"]
    permit_pty: Literal["enable", "disable"]
    permit_user_rc: Literal["enable", "disable"]
    cert_extension: list[AccessProxySshClientCertCertextensionItem]
    auth_ca: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AccessProxySshClientCertCertextensionItemObject(FortiObject[AccessProxySshClientCertCertextensionItem]):
    """Typed object for cert-extension table items with attribute access."""
    name: str
    critical: Literal["no", "yes"]
    type: Literal["fixed", "user"]
    data: str


class AccessProxySshClientCertObject(FortiObject):
    """Typed FortiObject for AccessProxySshClientCert with field access."""
    name: str
    source_address: Literal["enable", "disable"]
    permit_x11_forwarding: Literal["enable", "disable"]
    permit_agent_forwarding: Literal["enable", "disable"]
    permit_port_forwarding: Literal["enable", "disable"]
    permit_pty: Literal["enable", "disable"]
    permit_user_rc: Literal["enable", "disable"]
    cert_extension: FortiObjectList[AccessProxySshClientCertCertextensionItemObject]
    auth_ca: str


# ================================================================
# Main Endpoint Class
# ================================================================

class AccessProxySshClientCert:
    """
    
    Endpoint: firewall/access_proxy_ssh_client_cert
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
    ) -> AccessProxySshClientCertObject: ...
    
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
    ) -> FortiObjectList[AccessProxySshClientCertObject]: ...
    
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
        payload_dict: AccessProxySshClientCertPayload | None = ...,
        name: str | None = ...,
        source_address: Literal["enable", "disable"] | None = ...,
        permit_x11_forwarding: Literal["enable", "disable"] | None = ...,
        permit_agent_forwarding: Literal["enable", "disable"] | None = ...,
        permit_port_forwarding: Literal["enable", "disable"] | None = ...,
        permit_pty: Literal["enable", "disable"] | None = ...,
        permit_user_rc: Literal["enable", "disable"] | None = ...,
        cert_extension: str | list[str] | list[AccessProxySshClientCertCertextensionItem] | None = ...,
        auth_ca: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessProxySshClientCertObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AccessProxySshClientCertPayload | None = ...,
        name: str | None = ...,
        source_address: Literal["enable", "disable"] | None = ...,
        permit_x11_forwarding: Literal["enable", "disable"] | None = ...,
        permit_agent_forwarding: Literal["enable", "disable"] | None = ...,
        permit_port_forwarding: Literal["enable", "disable"] | None = ...,
        permit_pty: Literal["enable", "disable"] | None = ...,
        permit_user_rc: Literal["enable", "disable"] | None = ...,
        cert_extension: str | list[str] | list[AccessProxySshClientCertCertextensionItem] | None = ...,
        auth_ca: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessProxySshClientCertObject: ...

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
        payload_dict: AccessProxySshClientCertPayload | None = ...,
        name: str | None = ...,
        source_address: Literal["enable", "disable"] | None = ...,
        permit_x11_forwarding: Literal["enable", "disable"] | None = ...,
        permit_agent_forwarding: Literal["enable", "disable"] | None = ...,
        permit_port_forwarding: Literal["enable", "disable"] | None = ...,
        permit_pty: Literal["enable", "disable"] | None = ...,
        permit_user_rc: Literal["enable", "disable"] | None = ...,
        cert_extension: str | list[str] | list[AccessProxySshClientCertCertextensionItem] | None = ...,
        auth_ca: str | None = ...,
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
    "AccessProxySshClientCert",
    "AccessProxySshClientCertPayload",
    "AccessProxySshClientCertResponse",
    "AccessProxySshClientCertObject",
]