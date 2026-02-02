""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/snmp/community
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

class CommunityHostsItem(TypedDict, total=False):
    """Nested item for hosts field."""
    id: int
    source_ip: str
    ip: str
    ha_direct: Literal["enable", "disable"]
    host_type: Literal["any", "query", "trap"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class CommunityHosts6Item(TypedDict, total=False):
    """Nested item for hosts6 field."""
    id: int
    source_ipv6: str
    ipv6: str
    ha_direct: Literal["enable", "disable"]
    host_type: Literal["any", "query", "trap"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class CommunityVdomsItem(TypedDict, total=False):
    """Nested item for vdoms field."""
    name: str


class CommunityPayload(TypedDict, total=False):
    """Payload type for Community operations."""
    id: int
    name: str
    status: Literal["enable", "disable"]
    hosts: str | list[str] | list[CommunityHostsItem]
    hosts6: str | list[str] | list[CommunityHosts6Item]
    query_v1_status: Literal["enable", "disable"]
    query_v1_port: int
    query_v2c_status: Literal["enable", "disable"]
    query_v2c_port: int
    trap_v1_status: Literal["enable", "disable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["enable", "disable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: str | list[str]
    mib_view: str
    vdoms: str | list[str] | list[CommunityVdomsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CommunityResponse(TypedDict, total=False):
    """Response type for Community - use with .dict property for typed dict access."""
    id: int
    name: str
    status: Literal["enable", "disable"]
    hosts: list[CommunityHostsItem]
    hosts6: list[CommunityHosts6Item]
    query_v1_status: Literal["enable", "disable"]
    query_v1_port: int
    query_v2c_status: Literal["enable", "disable"]
    query_v2c_port: int
    trap_v1_status: Literal["enable", "disable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["enable", "disable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: str
    mib_view: str
    vdoms: list[CommunityVdomsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CommunityHostsItemObject(FortiObject[CommunityHostsItem]):
    """Typed object for hosts table items with attribute access."""
    id: int
    source_ip: str
    ip: str
    ha_direct: Literal["enable", "disable"]
    host_type: Literal["any", "query", "trap"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class CommunityHosts6ItemObject(FortiObject[CommunityHosts6Item]):
    """Typed object for hosts6 table items with attribute access."""
    id: int
    source_ipv6: str
    ipv6: str
    ha_direct: Literal["enable", "disable"]
    host_type: Literal["any", "query", "trap"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class CommunityVdomsItemObject(FortiObject[CommunityVdomsItem]):
    """Typed object for vdoms table items with attribute access."""
    name: str


class CommunityObject(FortiObject):
    """Typed FortiObject for Community with field access."""
    id: int
    name: str
    status: Literal["enable", "disable"]
    hosts: FortiObjectList[CommunityHostsItemObject]
    hosts6: FortiObjectList[CommunityHosts6ItemObject]
    query_v1_status: Literal["enable", "disable"]
    query_v1_port: int
    query_v2c_status: Literal["enable", "disable"]
    query_v2c_port: int
    trap_v1_status: Literal["enable", "disable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["enable", "disable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: str
    mib_view: str
    vdoms: FortiObjectList[CommunityVdomsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Community:
    """
    
    Endpoint: system/snmp/community
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> CommunityObject: ...
    
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
    ) -> FortiObjectList[CommunityObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: CommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        hosts: str | list[str] | list[CommunityHostsItem] | None = ...,
        hosts6: str | list[str] | list[CommunityHosts6Item] | None = ...,
        query_v1_status: Literal["enable", "disable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["enable", "disable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["enable", "disable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["enable", "disable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: str | list[str] | None = ...,
        mib_view: str | None = ...,
        vdoms: str | list[str] | list[CommunityVdomsItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CommunityObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        hosts: str | list[str] | list[CommunityHostsItem] | None = ...,
        hosts6: str | list[str] | list[CommunityHosts6Item] | None = ...,
        query_v1_status: Literal["enable", "disable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["enable", "disable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["enable", "disable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["enable", "disable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: str | list[str] | None = ...,
        mib_view: str | None = ...,
        vdoms: str | list[str] | list[CommunityVdomsItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CommunityObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: CommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        hosts: str | list[str] | list[CommunityHostsItem] | None = ...,
        hosts6: str | list[str] | list[CommunityHosts6Item] | None = ...,
        query_v1_status: Literal["enable", "disable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["enable", "disable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["enable", "disable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["enable", "disable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "vpn-tun-up", "vpn-tun-down", "ha-switch", "ha-hb-failure", "ips-signature", "ips-anomaly", "av-virus", "av-oversize", "av-pattern", "av-fragmented", "fm-if-change", "fm-conf-change", "bgp-established", "bgp-backward-transition", "ha-member-up", "ha-member-down", "ent-conf-change", "av-conserve", "av-bypass", "av-oversize-passed", "av-oversize-blocked", "ips-pkg-update", "ips-fail-open", "faz-disconnect", "faz", "wc-ap-up", "wc-ap-down", "fswctl-session-up", "fswctl-session-down", "load-balance-real-server-down", "device-new", "per-cpu-high", "dhcp", "pool-usage", "ippool", "interface", "ospf-nbr-state-change", "ospf-virtnbr-state-change", "bfd"] | list[str] | None = ...,
        mib_view: str | None = ...,
        vdoms: str | list[str] | list[CommunityVdomsItem] | None = ...,
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
    "Community",
    "CommunityPayload",
    "CommunityResponse",
    "CommunityObject",
]