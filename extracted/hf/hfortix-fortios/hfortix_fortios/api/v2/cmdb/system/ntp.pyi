""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ntp
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

class NtpNtpserverItem(TypedDict, total=False):
    """Nested item for ntpserver field."""
    id: int
    server: str
    ntpv3: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    key_type: Literal["MD5", "SHA1", "SHA256"]
    key: str
    key_id: int
    ip_type: Literal["IPv6", "IPv4", "Both"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class NtpInterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    interface_name: str


class NtpPayload(TypedDict, total=False):
    """Payload type for Ntp operations."""
    ntpsync: Literal["enable", "disable"]
    type: Literal["fortiguard", "custom"]
    syncinterval: int
    ntpserver: str | list[str] | list[NtpNtpserverItem]
    source_ip: str
    source_ip6: str
    server_mode: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    key_type: Literal["MD5", "SHA1", "SHA256"]
    key: str
    key_id: int
    interface: str | list[str] | list[NtpInterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class NtpResponse(TypedDict, total=False):
    """Response type for Ntp - use with .dict property for typed dict access."""
    ntpsync: Literal["enable", "disable"]
    type: Literal["fortiguard", "custom"]
    syncinterval: int
    ntpserver: list[NtpNtpserverItem]
    source_ip: str
    source_ip6: str
    server_mode: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    key_type: Literal["MD5", "SHA1", "SHA256"]
    key: str
    key_id: int
    interface: list[NtpInterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class NtpNtpserverItemObject(FortiObject[NtpNtpserverItem]):
    """Typed object for ntpserver table items with attribute access."""
    id: int
    server: str
    ntpv3: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    key_type: Literal["MD5", "SHA1", "SHA256"]
    key: str
    key_id: int
    ip_type: Literal["IPv6", "IPv4", "Both"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class NtpInterfaceItemObject(FortiObject[NtpInterfaceItem]):
    """Typed object for interface table items with attribute access."""
    interface_name: str


class NtpObject(FortiObject):
    """Typed FortiObject for Ntp with field access."""
    ntpsync: Literal["enable", "disable"]
    type: Literal["fortiguard", "custom"]
    syncinterval: int
    ntpserver: FortiObjectList[NtpNtpserverItemObject]
    source_ip: str
    source_ip6: str
    server_mode: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    key_type: Literal["MD5", "SHA1", "SHA256"]
    key: str
    key_id: int
    interface: FortiObjectList[NtpInterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ntp:
    """
    
    Endpoint: system/ntp
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NtpObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: NtpPayload | None = ...,
        ntpsync: Literal["enable", "disable"] | None = ...,
        type: Literal["fortiguard", "custom"] | None = ...,
        syncinterval: int | None = ...,
        ntpserver: str | list[str] | list[NtpNtpserverItem] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        key_type: Literal["MD5", "SHA1", "SHA256"] | None = ...,
        key: str | None = ...,
        key_id: int | None = ...,
        interface: str | list[str] | list[NtpInterfaceItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NtpObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: NtpPayload | None = ...,
        ntpsync: Literal["enable", "disable"] | None = ...,
        type: Literal["fortiguard", "custom"] | None = ...,
        syncinterval: int | None = ...,
        ntpserver: str | list[str] | list[NtpNtpserverItem] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        key_type: Literal["MD5", "SHA1", "SHA256"] | None = ...,
        key: str | None = ...,
        key_id: int | None = ...,
        interface: str | list[str] | list[NtpInterfaceItem] | None = ...,
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
    "Ntp",
    "NtpPayload",
    "NtpResponse",
    "NtpObject",
]