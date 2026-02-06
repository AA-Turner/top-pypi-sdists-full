"""
Child Table Helper Type Stubs for system/pcp-server

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class PoolsDict(TypedDict, total=False):
    """Type definition for pools child table entry."""
    name: str
    description: str | None
    id: int | None
    client_subnet: list[Any]
    ext_intf: str
    arp_reply: str | None
    extip: str
    extport: str
    minimal_lifetime: int | None
    maximal_lifetime: int | None
    client_mapping_limit: int | None
    mapping_filter_limit: int | None
    allow_opcode: str | None
    third_party: str | None
    third_party_subnet: list[Any] | None
    multicast_announcement: str | None
    announcement_count: int | None
    intl_intf: list[Any]
    recycle_delay: int | None


class PoolsObject(FortiObject):
    """Typed FortiObject for pools child table entry with attribute access."""
    name: str
    description: str | None
    id: int | None
    client_subnet: list[Any]
    ext_intf: str
    arp_reply: str | None
    extip: str
    extport: str
    minimal_lifetime: int | None
    maximal_lifetime: int | None
    client_mapping_limit: int | None
    mapping_filter_limit: int | None
    allow_opcode: str | None
    third_party: str | None
    third_party_subnet: list[Any] | None
    multicast_announcement: str | None
    announcement_count: int | None
    intl_intf: list[Any]
    recycle_delay: int | None



class PoolsHelper:
    """Helper class for managing pools child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[PoolsObject] | PoolsObject | None: ...
    
    def set(
        self,
        name: str,
        client_subnet: list[Any],
        ext_intf: str,
        extip: str,
        extport: str,
        intl_intf: list[Any],
        description: str | None = ...,
        id: int | None = ...,
        arp_reply: str | None = ...,
        minimal_lifetime: int | None = ...,
        maximal_lifetime: int | None = ...,
        client_mapping_limit: int | None = ...,
        mapping_filter_limit: int | None = ...,
        allow_opcode: str | None = ...,
        third_party: str | None = ...,
        third_party_subnet: list[Any] | None = ...,
        multicast_announcement: str | None = ...,
        announcement_count: int | None = ...,
        recycle_delay: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

