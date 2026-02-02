""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/central_snat_map
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

class CentralSnatMapSrcintfItem(TypedDict, total=False):
    """Nested item for srcintf field."""
    name: str


class CentralSnatMapDstintfItem(TypedDict, total=False):
    """Nested item for dstintf field."""
    name: str


class CentralSnatMapOrigaddrItem(TypedDict, total=False):
    """Nested item for orig-addr field."""
    name: str


class CentralSnatMapOrigaddr6Item(TypedDict, total=False):
    """Nested item for orig-addr6 field."""
    name: str


class CentralSnatMapDstaddrItem(TypedDict, total=False):
    """Nested item for dst-addr field."""
    name: str


class CentralSnatMapDstaddr6Item(TypedDict, total=False):
    """Nested item for dst-addr6 field."""
    name: str


class CentralSnatMapNatippoolItem(TypedDict, total=False):
    """Nested item for nat-ippool field."""
    name: str


class CentralSnatMapNatippool6Item(TypedDict, total=False):
    """Nested item for nat-ippool6 field."""
    name: str


class CentralSnatMapPayload(TypedDict, total=False):
    """Payload type for CentralSnatMap operations."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["ipv4", "ipv6"]
    srcintf: str | list[str] | list[CentralSnatMapSrcintfItem]
    dstintf: str | list[str] | list[CentralSnatMapDstintfItem]
    orig_addr: str | list[str] | list[CentralSnatMapOrigaddrItem]
    orig_addr6: str | list[str] | list[CentralSnatMapOrigaddr6Item]
    dst_addr: str | list[str] | list[CentralSnatMapDstaddrItem]
    dst_addr6: str | list[str] | list[CentralSnatMapDstaddr6Item]
    protocol: int
    orig_port: str
    nat: Literal["disable", "enable"]
    nat46: Literal["enable", "disable"]
    nat64: Literal["enable", "disable"]
    nat_ippool: str | list[str] | list[CentralSnatMapNatippoolItem]
    nat_ippool6: str | list[str] | list[CentralSnatMapNatippool6Item]
    port_preserve: Literal["enable", "disable"]
    port_random: Literal["enable", "disable"]
    nat_port: str
    dst_port: str
    comments: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CentralSnatMapResponse(TypedDict, total=False):
    """Response type for CentralSnatMap - use with .dict property for typed dict access."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["ipv4", "ipv6"]
    srcintf: list[CentralSnatMapSrcintfItem]
    dstintf: list[CentralSnatMapDstintfItem]
    orig_addr: list[CentralSnatMapOrigaddrItem]
    orig_addr6: list[CentralSnatMapOrigaddr6Item]
    dst_addr: list[CentralSnatMapDstaddrItem]
    dst_addr6: list[CentralSnatMapDstaddr6Item]
    protocol: int
    orig_port: str
    nat: Literal["disable", "enable"]
    nat46: Literal["enable", "disable"]
    nat64: Literal["enable", "disable"]
    nat_ippool: list[CentralSnatMapNatippoolItem]
    nat_ippool6: list[CentralSnatMapNatippool6Item]
    port_preserve: Literal["enable", "disable"]
    port_random: Literal["enable", "disable"]
    nat_port: str
    dst_port: str
    comments: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CentralSnatMapSrcintfItemObject(FortiObject[CentralSnatMapSrcintfItem]):
    """Typed object for srcintf table items with attribute access."""
    name: str


class CentralSnatMapDstintfItemObject(FortiObject[CentralSnatMapDstintfItem]):
    """Typed object for dstintf table items with attribute access."""
    name: str


class CentralSnatMapOrigaddrItemObject(FortiObject[CentralSnatMapOrigaddrItem]):
    """Typed object for orig-addr table items with attribute access."""
    name: str


class CentralSnatMapOrigaddr6ItemObject(FortiObject[CentralSnatMapOrigaddr6Item]):
    """Typed object for orig-addr6 table items with attribute access."""
    name: str


class CentralSnatMapDstaddrItemObject(FortiObject[CentralSnatMapDstaddrItem]):
    """Typed object for dst-addr table items with attribute access."""
    name: str


class CentralSnatMapDstaddr6ItemObject(FortiObject[CentralSnatMapDstaddr6Item]):
    """Typed object for dst-addr6 table items with attribute access."""
    name: str


class CentralSnatMapNatippoolItemObject(FortiObject[CentralSnatMapNatippoolItem]):
    """Typed object for nat-ippool table items with attribute access."""
    name: str


class CentralSnatMapNatippool6ItemObject(FortiObject[CentralSnatMapNatippool6Item]):
    """Typed object for nat-ippool6 table items with attribute access."""
    name: str


class CentralSnatMapObject(FortiObject):
    """Typed FortiObject for CentralSnatMap with field access."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["ipv4", "ipv6"]
    srcintf: FortiObjectList[CentralSnatMapSrcintfItemObject]
    dstintf: FortiObjectList[CentralSnatMapDstintfItemObject]
    orig_addr: FortiObjectList[CentralSnatMapOrigaddrItemObject]
    orig_addr6: FortiObjectList[CentralSnatMapOrigaddr6ItemObject]
    dst_addr: FortiObjectList[CentralSnatMapDstaddrItemObject]
    dst_addr6: FortiObjectList[CentralSnatMapDstaddr6ItemObject]
    protocol: int
    orig_port: str
    nat: Literal["disable", "enable"]
    nat46: Literal["enable", "disable"]
    nat64: Literal["enable", "disable"]
    nat_ippool: FortiObjectList[CentralSnatMapNatippoolItemObject]
    nat_ippool6: FortiObjectList[CentralSnatMapNatippool6ItemObject]
    port_preserve: Literal["enable", "disable"]
    port_random: Literal["enable", "disable"]
    nat_port: str
    dst_port: str
    comments: str


# ================================================================
# Main Endpoint Class
# ================================================================

class CentralSnatMap:
    """
    
    Endpoint: firewall/central_snat_map
    Category: cmdb
    MKey: policyid
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
        policyid: int,
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
    ) -> CentralSnatMapObject: ...
    
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
    ) -> FortiObjectList[CentralSnatMapObject]: ...
    
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
        payload_dict: CentralSnatMapPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["ipv4", "ipv6"] | None = ...,
        srcintf: str | list[str] | list[CentralSnatMapSrcintfItem] | None = ...,
        dstintf: str | list[str] | list[CentralSnatMapDstintfItem] | None = ...,
        orig_addr: str | list[str] | list[CentralSnatMapOrigaddrItem] | None = ...,
        orig_addr6: str | list[str] | list[CentralSnatMapOrigaddr6Item] | None = ...,
        dst_addr: str | list[str] | list[CentralSnatMapDstaddrItem] | None = ...,
        dst_addr6: str | list[str] | list[CentralSnatMapDstaddr6Item] | None = ...,
        protocol: int | None = ...,
        orig_port: str | None = ...,
        nat: Literal["disable", "enable"] | None = ...,
        nat46: Literal["enable", "disable"] | None = ...,
        nat64: Literal["enable", "disable"] | None = ...,
        nat_ippool: str | list[str] | list[CentralSnatMapNatippoolItem] | None = ...,
        nat_ippool6: str | list[str] | list[CentralSnatMapNatippool6Item] | None = ...,
        port_preserve: Literal["enable", "disable"] | None = ...,
        port_random: Literal["enable", "disable"] | None = ...,
        nat_port: str | None = ...,
        dst_port: str | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CentralSnatMapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CentralSnatMapPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["ipv4", "ipv6"] | None = ...,
        srcintf: str | list[str] | list[CentralSnatMapSrcintfItem] | None = ...,
        dstintf: str | list[str] | list[CentralSnatMapDstintfItem] | None = ...,
        orig_addr: str | list[str] | list[CentralSnatMapOrigaddrItem] | None = ...,
        orig_addr6: str | list[str] | list[CentralSnatMapOrigaddr6Item] | None = ...,
        dst_addr: str | list[str] | list[CentralSnatMapDstaddrItem] | None = ...,
        dst_addr6: str | list[str] | list[CentralSnatMapDstaddr6Item] | None = ...,
        protocol: int | None = ...,
        orig_port: str | None = ...,
        nat: Literal["disable", "enable"] | None = ...,
        nat46: Literal["enable", "disable"] | None = ...,
        nat64: Literal["enable", "disable"] | None = ...,
        nat_ippool: str | list[str] | list[CentralSnatMapNatippoolItem] | None = ...,
        nat_ippool6: str | list[str] | list[CentralSnatMapNatippool6Item] | None = ...,
        port_preserve: Literal["enable", "disable"] | None = ...,
        port_random: Literal["enable", "disable"] | None = ...,
        nat_port: str | None = ...,
        dst_port: str | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CentralSnatMapObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        policyid: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        policyid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: CentralSnatMapPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["ipv4", "ipv6"] | None = ...,
        srcintf: str | list[str] | list[CentralSnatMapSrcintfItem] | None = ...,
        dstintf: str | list[str] | list[CentralSnatMapDstintfItem] | None = ...,
        orig_addr: str | list[str] | list[CentralSnatMapOrigaddrItem] | None = ...,
        orig_addr6: str | list[str] | list[CentralSnatMapOrigaddr6Item] | None = ...,
        dst_addr: str | list[str] | list[CentralSnatMapDstaddrItem] | None = ...,
        dst_addr6: str | list[str] | list[CentralSnatMapDstaddr6Item] | None = ...,
        protocol: int | None = ...,
        orig_port: str | None = ...,
        nat: Literal["disable", "enable"] | None = ...,
        nat46: Literal["enable", "disable"] | None = ...,
        nat64: Literal["enable", "disable"] | None = ...,
        nat_ippool: str | list[str] | list[CentralSnatMapNatippoolItem] | None = ...,
        nat_ippool6: str | list[str] | list[CentralSnatMapNatippool6Item] | None = ...,
        port_preserve: Literal["enable", "disable"] | None = ...,
        port_random: Literal["enable", "disable"] | None = ...,
        nat_port: str | None = ...,
        dst_port: str | None = ...,
        comments: str | None = ...,
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
    "CentralSnatMap",
    "CentralSnatMapPayload",
    "CentralSnatMapResponse",
    "CentralSnatMapObject",
]