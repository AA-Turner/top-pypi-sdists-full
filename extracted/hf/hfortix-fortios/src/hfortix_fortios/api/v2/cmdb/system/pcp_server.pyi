""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/pcp_server
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

class PcpServerPoolsClientsubnetItem(TypedDict, total=False):
    """Nested item for pools.client-subnet field."""
    subnet: str


class PcpServerPoolsThirdpartysubnetItem(TypedDict, total=False):
    """Nested item for pools.third-party-subnet field."""
    subnet: str


class PcpServerPoolsIntlintfItem(TypedDict, total=False):
    """Nested item for pools.intl-intf field."""
    interface_name: str


class PcpServerPoolsItem(TypedDict, total=False):
    """Nested item for pools field."""
    name: str
    description: str
    id: int
    client_subnet: str | list[str] | list[PcpServerPoolsClientsubnetItem]
    ext_intf: str
    arp_reply: Literal["disable", "enable"]
    extip: str
    extport: str
    minimal_lifetime: int
    maximal_lifetime: int
    client_mapping_limit: int
    mapping_filter_limit: int
    allow_opcode: Literal["map", "peer", "announce"]
    third_party: Literal["allow", "disallow"]
    third_party_subnet: str | list[str] | list[PcpServerPoolsThirdpartysubnetItem]
    multicast_announcement: Literal["enable", "disable"]
    announcement_count: int
    intl_intf: str | list[str] | list[PcpServerPoolsIntlintfItem]
    recycle_delay: int


class PcpServerPayload(TypedDict, total=False):
    """Payload type for PcpServer operations."""
    status: Literal["enable", "disable"]
    pools: str | list[str] | list[PcpServerPoolsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PcpServerResponse(TypedDict, total=False):
    """Response type for PcpServer - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    pools: list[PcpServerPoolsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PcpServerPoolsClientsubnetItemObject(FortiObject[PcpServerPoolsClientsubnetItem]):
    """Typed object for pools.client-subnet table items with attribute access."""
    subnet: str


class PcpServerPoolsThirdpartysubnetItemObject(FortiObject[PcpServerPoolsThirdpartysubnetItem]):
    """Typed object for pools.third-party-subnet table items with attribute access."""
    subnet: str


class PcpServerPoolsIntlintfItemObject(FortiObject[PcpServerPoolsIntlintfItem]):
    """Typed object for pools.intl-intf table items with attribute access."""
    interface_name: str


class PcpServerPoolsItemObject(FortiObject[PcpServerPoolsItem]):
    """Typed object for pools table items with attribute access."""
    name: str
    description: str
    id: int
    client_subnet: FortiObjectList[PcpServerPoolsClientsubnetItemObject]
    ext_intf: str
    arp_reply: Literal["disable", "enable"]
    extip: str
    extport: str
    minimal_lifetime: int
    maximal_lifetime: int
    client_mapping_limit: int
    mapping_filter_limit: int
    allow_opcode: Literal["map", "peer", "announce"]
    third_party: Literal["allow", "disallow"]
    third_party_subnet: FortiObjectList[PcpServerPoolsThirdpartysubnetItemObject]
    multicast_announcement: Literal["enable", "disable"]
    announcement_count: int
    intl_intf: FortiObjectList[PcpServerPoolsIntlintfItemObject]
    recycle_delay: int


class PcpServerObject(FortiObject):
    """Typed FortiObject for PcpServer with field access."""
    status: Literal["enable", "disable"]
    pools: FortiObjectList[PcpServerPoolsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class PcpServer:
    """
    
    Endpoint: system/pcp_server
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
    ) -> PcpServerObject: ...
    
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
        payload_dict: PcpServerPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        pools: str | list[str] | list[PcpServerPoolsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PcpServerObject: ...


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
        payload_dict: PcpServerPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        pools: str | list[str] | list[PcpServerPoolsItem] | None = ...,
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
    "PcpServer",
    "PcpServerPayload",
    "PcpServerResponse",
    "PcpServerObject",
]