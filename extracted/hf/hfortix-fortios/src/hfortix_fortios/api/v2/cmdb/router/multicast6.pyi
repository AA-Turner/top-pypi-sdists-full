""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/multicast6
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

class Multicast6PimsmglobalRpaddressItem(TypedDict, total=False):
    """Nested item for pim-sm-global.rp-address field."""
    id: int
    ip6_address: str


class Multicast6InterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    name: str
    hello_interval: int
    hello_holdtime: int


class Multicast6PimsmglobalDict(TypedDict, total=False):
    """Nested object type for pim-sm-global field."""
    register_rate_limit: int
    pim_use_sdwan: Literal["enable", "disable"]
    rp_address: str | list[str] | list[Multicast6PimsmglobalRpaddressItem]


class Multicast6Payload(TypedDict, total=False):
    """Payload type for Multicast6 operations."""
    multicast_routing: Literal["enable", "disable"]
    multicast_pmtu: Literal["enable", "disable"]
    interface: str | list[str] | list[Multicast6InterfaceItem]
    pim_sm_global: Multicast6PimsmglobalDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Multicast6Response(TypedDict, total=False):
    """Response type for Multicast6 - use with .dict property for typed dict access."""
    multicast_routing: Literal["enable", "disable"]
    multicast_pmtu: Literal["enable", "disable"]
    interface: list[Multicast6InterfaceItem]
    pim_sm_global: Multicast6PimsmglobalDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Multicast6InterfaceItemObject(FortiObject[Multicast6InterfaceItem]):
    """Typed object for interface table items with attribute access."""
    name: str
    hello_interval: int
    hello_holdtime: int


class Multicast6PimsmglobalRpaddressItemObject(FortiObject[Multicast6PimsmglobalRpaddressItem]):
    """Typed object for pim-sm-global.rp-address table items with attribute access."""
    id: int
    ip6_address: str


class Multicast6PimsmglobalObject(FortiObject):
    """Nested object for pim-sm-global field with attribute access."""
    register_rate_limit: int
    pim_use_sdwan: Literal["enable", "disable"]
    rp_address: str | list[str]


class Multicast6Object(FortiObject):
    """Typed FortiObject for Multicast6 with field access."""
    multicast_routing: Literal["enable", "disable"]
    multicast_pmtu: Literal["enable", "disable"]
    interface: FortiObjectList[Multicast6InterfaceItemObject]
    pim_sm_global: Multicast6PimsmglobalObject


# ================================================================
# Main Endpoint Class
# ================================================================

class Multicast6:
    """
    
    Endpoint: router/multicast6
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
    ) -> Multicast6Object: ...
    
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
        payload_dict: Multicast6Payload | None = ...,
        multicast_routing: Literal["enable", "disable"] | None = ...,
        multicast_pmtu: Literal["enable", "disable"] | None = ...,
        interface: str | list[str] | list[Multicast6InterfaceItem] | None = ...,
        pim_sm_global: Multicast6PimsmglobalDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Multicast6Object: ...


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
        payload_dict: Multicast6Payload | None = ...,
        multicast_routing: Literal["enable", "disable"] | None = ...,
        multicast_pmtu: Literal["enable", "disable"] | None = ...,
        interface: str | list[str] | list[Multicast6InterfaceItem] | None = ...,
        pim_sm_global: Multicast6PimsmglobalDict | None = ...,
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
    "Multicast6",
    "Multicast6Payload",
    "Multicast6Response",
    "Multicast6Object",
]