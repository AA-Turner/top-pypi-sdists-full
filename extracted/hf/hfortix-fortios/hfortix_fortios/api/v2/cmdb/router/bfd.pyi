""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/bfd
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

class BfdNeighborItem(TypedDict, total=False):
    """Nested item for neighbor field."""
    ip: str
    interface: str


class BfdMultihoptemplateItem(TypedDict, total=False):
    """Nested item for multihop-template field."""
    id: int
    src: str
    dst: str
    bfd_desired_min_tx: int
    bfd_required_min_rx: int
    bfd_detect_mult: int
    auth_mode: Literal["none", "md5"]
    md5_key: str


class BfdPayload(TypedDict, total=False):
    """Payload type for Bfd operations."""
    neighbor: str | list[str] | list[BfdNeighborItem]
    multihop_template: str | list[str] | list[BfdMultihoptemplateItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class BfdResponse(TypedDict, total=False):
    """Response type for Bfd - use with .dict property for typed dict access."""
    neighbor: list[BfdNeighborItem]
    multihop_template: list[BfdMultihoptemplateItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class BfdNeighborItemObject(FortiObject[BfdNeighborItem]):
    """Typed object for neighbor table items with attribute access."""
    ip: str
    interface: str


class BfdMultihoptemplateItemObject(FortiObject[BfdMultihoptemplateItem]):
    """Typed object for multihop-template table items with attribute access."""
    id: int
    src: str
    dst: str
    bfd_desired_min_tx: int
    bfd_required_min_rx: int
    bfd_detect_mult: int
    auth_mode: Literal["none", "md5"]
    md5_key: str


class BfdObject(FortiObject):
    """Typed FortiObject for Bfd with field access."""
    neighbor: FortiObjectList[BfdNeighborItemObject]
    multihop_template: FortiObjectList[BfdMultihoptemplateItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Bfd:
    """
    
    Endpoint: router/bfd
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
    ) -> BfdObject: ...
    
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
        payload_dict: BfdPayload | None = ...,
        neighbor: str | list[str] | list[BfdNeighborItem] | None = ...,
        multihop_template: str | list[str] | list[BfdMultihoptemplateItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BfdObject: ...


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
        payload_dict: BfdPayload | None = ...,
        neighbor: str | list[str] | list[BfdNeighborItem] | None = ...,
        multihop_template: str | list[str] | list[BfdMultihoptemplateItem] | None = ...,
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
    "Bfd",
    "BfdPayload",
    "BfdResponse",
    "BfdObject",
]