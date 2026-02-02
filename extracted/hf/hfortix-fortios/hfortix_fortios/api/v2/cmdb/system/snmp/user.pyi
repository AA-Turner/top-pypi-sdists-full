""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/snmp/user
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

class UserVdomsItem(TypedDict, total=False):
    """Nested item for vdoms field."""
    name: str


class UserPayload(TypedDict, total=False):
    """Payload type for User operations."""
    name: str
    status: Literal["enable", "disable"]
    trap_status: Literal["enable", "disable"]
    trap_lport: int
    trap_rport: int
    queries: Literal["enable", "disable"]
    query_port: int
    notify_hosts: str | list[str]
    notify_hosts6: str | list[str]
    source_ip: str
    source_ipv6: str
    ha_direct: Literal["enable", "disable"]
    events: str | list[str]
    mib_view: str
    vdoms: str | list[str] | list[UserVdomsItem]
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
    auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"]
    auth_pwd: str
    priv_proto: Literal["aes", "des", "aes256", "aes256cisco"]
    priv_pwd: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UserResponse(TypedDict, total=False):
    """Response type for User - use with .dict property for typed dict access."""
    name: str
    status: Literal["enable", "disable"]
    trap_status: Literal["enable", "disable"]
    trap_lport: int
    trap_rport: int
    queries: Literal["enable", "disable"]
    query_port: int
    notify_hosts: str | list[str]
    notify_hosts6: str | list[str]
    source_ip: str
    source_ipv6: str
    ha_direct: Literal["enable", "disable"]
    events: str
    mib_view: str
    vdoms: list[UserVdomsItem]
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
    auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"]
    auth_pwd: str
    priv_proto: Literal["aes", "des", "aes256", "aes256cisco"]
    priv_pwd: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UserVdomsItemObject(FortiObject[UserVdomsItem]):
    """Typed object for vdoms table items with attribute access."""
    name: str


class UserObject(FortiObject):
    """Typed FortiObject for User with field access."""
    name: str
    status: Literal["enable", "disable"]
    trap_status: Literal["enable", "disable"]
    trap_lport: int
    trap_rport: int
    queries: Literal["enable", "disable"]
    query_port: int
    notify_hosts: str | list[str]
    notify_hosts6: str | list[str]
    source_ip: str
    source_ipv6: str
    ha_direct: Literal["enable", "disable"]
    events: str
    mib_view: str
    vdoms: FortiObjectList[UserVdomsItemObject]
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
    auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"]
    auth_pwd: str
    priv_proto: Literal["aes", "des", "aes256", "aes256cisco"]
    priv_pwd: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class User:
    """
    
    Endpoint: system/snmp/user
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UserObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[UserObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: UserPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trap_status: Literal["enable", "disable"] | None = ...,
        trap_lport: int | None = ...,
        trap_rport: int | None = ...,
        queries: Literal["enable", "disable"] | None = ...,
        query_port: int | None = ...,
        notify_hosts: str | list[str] | None = ...,
        notify_hosts6: str | list[str] | None = ...,
        source_ip: str | None = ...,
        source_ipv6: str | None = ...,
        ha_direct: Literal["enable", "disable"] | None = ...,
        events: str | list[str] | None = ...,
        mib_view: str | None = ...,
        vdoms: str | list[str] | list[UserVdomsItem] | None = ...,
        security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"] | None = ...,
        auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"] | None = ...,
        auth_pwd: str | None = ...,
        priv_proto: Literal["aes", "des", "aes256", "aes256cisco"] | None = ...,
        priv_pwd: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UserObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UserPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trap_status: Literal["enable", "disable"] | None = ...,
        trap_lport: int | None = ...,
        trap_rport: int | None = ...,
        queries: Literal["enable", "disable"] | None = ...,
        query_port: int | None = ...,
        notify_hosts: str | list[str] | None = ...,
        notify_hosts6: str | list[str] | None = ...,
        source_ip: str | None = ...,
        source_ipv6: str | None = ...,
        ha_direct: Literal["enable", "disable"] | None = ...,
        events: str | list[str] | None = ...,
        mib_view: str | None = ...,
        vdoms: str | list[str] | list[UserVdomsItem] | None = ...,
        security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"] | None = ...,
        auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"] | None = ...,
        auth_pwd: str | None = ...,
        priv_proto: Literal["aes", "des", "aes256", "aes256cisco"] | None = ...,
        priv_pwd: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UserObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: UserPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trap_status: Literal["enable", "disable"] | None = ...,
        trap_lport: int | None = ...,
        trap_rport: int | None = ...,
        queries: Literal["enable", "disable"] | None = ...,
        query_port: int | None = ...,
        notify_hosts: str | list[str] | None = ...,
        notify_hosts6: str | list[str] | None = ...,
        source_ip: str | None = ...,
        source_ipv6: str | None = ...,
        ha_direct: Literal["enable", "disable"] | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "vpn-tun-up", "vpn-tun-down", "ha-switch", "ha-hb-failure", "ips-signature", "ips-anomaly", "av-virus", "av-oversize", "av-pattern", "av-fragmented", "fm-if-change", "fm-conf-change", "bgp-established", "bgp-backward-transition", "ha-member-up", "ha-member-down", "ent-conf-change", "av-conserve", "av-bypass", "av-oversize-passed", "av-oversize-blocked", "ips-pkg-update", "ips-fail-open", "faz-disconnect", "faz", "wc-ap-up", "wc-ap-down", "fswctl-session-up", "fswctl-session-down", "load-balance-real-server-down", "device-new", "per-cpu-high", "dhcp", "pool-usage", "ippool", "interface", "ospf-nbr-state-change", "ospf-virtnbr-state-change", "bfd"] | list[str] | None = ...,
        mib_view: str | None = ...,
        vdoms: str | list[str] | list[UserVdomsItem] | None = ...,
        security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"] | None = ...,
        auth_proto: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"] | None = ...,
        auth_pwd: str | None = ...,
        priv_proto: Literal["aes", "des", "aes256", "aes256cisco"] | None = ...,
        priv_pwd: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
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
    "User",
    "UserPayload",
    "UserResponse",
    "UserObject",
]