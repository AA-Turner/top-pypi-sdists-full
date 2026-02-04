""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/bfd6
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

class Bfd6NeighborItem(TypedDict, total=False):
    """Nested item for neighbor field."""
    ip6_address: str
    interface: str


class Bfd6MultihoptemplateItem(TypedDict, total=False):
    """Nested item for multihop-template field."""
    id: int
    src: str
    dst: str
    bfd_desired_min_tx: int
    bfd_required_min_rx: int
    bfd_detect_mult: int
    auth_mode: Literal["none", "md5"]
    md5_key: str


class Bfd6Payload(TypedDict, total=False):
    """Payload type for Bfd6 operations."""
    neighbor: str | list[str] | list[Bfd6NeighborItem]
    multihop_template: str | list[str] | list[Bfd6MultihoptemplateItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Bfd6Response(TypedDict, total=False):
    """Response type for Bfd6 - use with .dict property for typed dict access."""
    neighbor: list[Bfd6NeighborItem]
    multihop_template: list[Bfd6MultihoptemplateItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Bfd6NeighborItemObject(FortiObject[Bfd6NeighborItem]):
    """Typed object for neighbor table items with attribute access."""
    ip6_address: str
    interface: str


class Bfd6MultihoptemplateItemObject(FortiObject[Bfd6MultihoptemplateItem]):
    """Typed object for multihop-template table items with attribute access."""
    id: int
    src: str
    dst: str
    bfd_desired_min_tx: int
    bfd_required_min_rx: int
    bfd_detect_mult: int
    auth_mode: Literal["none", "md5"]
    md5_key: str


class Bfd6Object(FortiObject):
    """Typed FortiObject for Bfd6 with field access."""
    neighbor: FortiObjectList[Bfd6NeighborItemObject]
    multihop_template: FortiObjectList[Bfd6MultihoptemplateItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Bfd6:
    """
    
    Endpoint: router/bfd6
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
    ) -> Bfd6Object: ...
    
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
        payload_dict: Bfd6Payload | None = ...,
        neighbor: str | list[str] | list[Bfd6NeighborItem] | None = ...,
        multihop_template: str | list[str] | list[Bfd6MultihoptemplateItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Bfd6Object: ...


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
        payload_dict: Bfd6Payload | None = ...,
        neighbor: str | list[str] | list[Bfd6NeighborItem] | None = ...,
        multihop_template: str | list[str] | list[Bfd6MultihoptemplateItem] | None = ...,
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
    "Bfd6",
    "Bfd6Payload",
    "Bfd6Response",
    "Bfd6Object",
]