""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/snmp_community
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

class SnmpCommunityHostsItem(TypedDict, total=False):
    """Nested item for hosts field."""
    id: int
    ip: str


class SnmpCommunityPayload(TypedDict, total=False):
    """Payload type for SnmpCommunity operations."""
    id: int
    name: str
    status: Literal["disable", "enable"]
    hosts: str | list[str] | list[SnmpCommunityHostsItem]
    query_v1_status: Literal["disable", "enable"]
    query_v1_port: int
    query_v2c_status: Literal["disable", "enable"]
    query_v2c_port: int
    trap_v1_status: Literal["disable", "enable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["disable", "enable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: str | list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SnmpCommunityResponse(TypedDict, total=False):
    """Response type for SnmpCommunity - use with .dict property for typed dict access."""
    id: int
    name: str
    status: Literal["disable", "enable"]
    hosts: list[SnmpCommunityHostsItem]
    query_v1_status: Literal["disable", "enable"]
    query_v1_port: int
    query_v2c_status: Literal["disable", "enable"]
    query_v2c_port: int
    trap_v1_status: Literal["disable", "enable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["disable", "enable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SnmpCommunityHostsItemObject(FortiObject[SnmpCommunityHostsItem]):
    """Typed object for hosts table items with attribute access."""
    id: int
    ip: str


class SnmpCommunityObject(FortiObject):
    """Typed FortiObject for SnmpCommunity with field access."""
    id: int
    name: str
    status: Literal["disable", "enable"]
    hosts: FortiObjectList[SnmpCommunityHostsItemObject]
    query_v1_status: Literal["disable", "enable"]
    query_v1_port: int
    query_v2c_status: Literal["disable", "enable"]
    query_v2c_port: int
    trap_v1_status: Literal["disable", "enable"]
    trap_v1_lport: int
    trap_v1_rport: int
    trap_v2c_status: Literal["disable", "enable"]
    trap_v2c_lport: int
    trap_v2c_rport: int
    events: str


# ================================================================
# Main Endpoint Class
# ================================================================

class SnmpCommunity:
    """
    
    Endpoint: switch_controller/snmp_community
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SnmpCommunityObject: ...
    
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
    ) -> FortiObjectList[SnmpCommunityObject]: ...
    
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
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[SnmpCommunityHostsItem] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SnmpCommunityObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[SnmpCommunityHostsItem] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SnmpCommunityObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[SnmpCommunityHostsItem] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
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
    "SnmpCommunity",
    "SnmpCommunityPayload",
    "SnmpCommunityResponse",
    "SnmpCommunityObject",
]