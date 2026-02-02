""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/snmp
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

class SnmpCommunityHostsItem(TypedDict, total=False):
    """Nested item for community.hosts field."""
    id: int
    ip: str


class SnmpCommunityHosts6Item(TypedDict, total=False):
    """Nested item for community.hosts6 field."""
    id: int
    ipv6: str


class SnmpCommunityItem(TypedDict, total=False):
    """Nested item for community field."""
    id: int
    name: str
    status: Literal["enable", "disable"]
    query_v1_status: Literal["enable", "disable"]
    query_v2c_status: Literal["enable", "disable"]
    trap_v1_status: Literal["enable", "disable"]
    trap_v2c_status: Literal["enable", "disable"]
    hosts: str | list[str] | list[SnmpCommunityHostsItem]
    hosts6: str | list[str] | list[SnmpCommunityHosts6Item]


class SnmpUserItem(TypedDict, total=False):
    """Nested item for user field."""
    name: str
    status: Literal["enable", "disable"]
    queries: Literal["enable", "disable"]
    trap_status: Literal["enable", "disable"]
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
    auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"]
    auth_pwd: str
    priv_proto: Literal["aes", "des", "aes256", "aes256cisco"]
    priv_pwd: str
    notify_hosts: str | list[str]
    notify_hosts6: str | list[str]


class SnmpPayload(TypedDict, total=False):
    """Payload type for Snmp operations."""
    engine_id: str
    contact_info: str
    trap_high_cpu_threshold: int
    trap_high_mem_threshold: int
    community: str | list[str] | list[SnmpCommunityItem]
    user: str | list[str] | list[SnmpUserItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SnmpResponse(TypedDict, total=False):
    """Response type for Snmp - use with .dict property for typed dict access."""
    engine_id: str
    contact_info: str
    trap_high_cpu_threshold: int
    trap_high_mem_threshold: int
    community: list[SnmpCommunityItem]
    user: list[SnmpUserItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SnmpCommunityHostsItemObject(FortiObject[SnmpCommunityHostsItem]):
    """Typed object for community.hosts table items with attribute access."""
    id: int
    ip: str


class SnmpCommunityHosts6ItemObject(FortiObject[SnmpCommunityHosts6Item]):
    """Typed object for community.hosts6 table items with attribute access."""
    id: int
    ipv6: str


class SnmpCommunityItemObject(FortiObject[SnmpCommunityItem]):
    """Typed object for community table items with attribute access."""
    id: int
    name: str
    status: Literal["enable", "disable"]
    query_v1_status: Literal["enable", "disable"]
    query_v2c_status: Literal["enable", "disable"]
    trap_v1_status: Literal["enable", "disable"]
    trap_v2c_status: Literal["enable", "disable"]
    hosts: FortiObjectList[SnmpCommunityHostsItemObject]
    hosts6: FortiObjectList[SnmpCommunityHosts6ItemObject]


class SnmpUserItemObject(FortiObject[SnmpUserItem]):
    """Typed object for user table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    queries: Literal["enable", "disable"]
    trap_status: Literal["enable", "disable"]
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
    auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"]
    auth_pwd: str
    priv_proto: Literal["aes", "des", "aes256", "aes256cisco"]
    priv_pwd: str
    notify_hosts: str | list[str]
    notify_hosts6: str | list[str]


class SnmpObject(FortiObject):
    """Typed FortiObject for Snmp with field access."""
    engine_id: str
    contact_info: str
    trap_high_cpu_threshold: int
    trap_high_mem_threshold: int
    community: FortiObjectList[SnmpCommunityItemObject]
    user: FortiObjectList[SnmpUserItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Snmp:
    """
    
    Endpoint: wireless_controller/snmp
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
    ) -> SnmpObject: ...
    
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
        payload_dict: SnmpPayload | None = ...,
        engine_id: str | None = ...,
        contact_info: str | None = ...,
        trap_high_cpu_threshold: int | None = ...,
        trap_high_mem_threshold: int | None = ...,
        community: str | list[str] | list[SnmpCommunityItem] | None = ...,
        user: str | list[str] | list[SnmpUserItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SnmpObject: ...


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
        payload_dict: SnmpPayload | None = ...,
        engine_id: str | None = ...,
        contact_info: str | None = ...,
        trap_high_cpu_threshold: int | None = ...,
        trap_high_mem_threshold: int | None = ...,
        community: str | list[str] | list[SnmpCommunityItem] | None = ...,
        user: str | list[str] | list[SnmpUserItem] | None = ...,
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
    "Snmp",
    "SnmpPayload",
    "SnmpResponse",
    "SnmpObject",
]