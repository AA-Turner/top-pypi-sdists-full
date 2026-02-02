""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ips/view_map
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

class ViewMapPayload(TypedDict, total=False):
    """Payload type for ViewMap operations."""
    id: int
    vdom_id: int
    policy_id: int
    id_policy_id: int
    which: Literal["firewall", "interface", "interface6", "sniffer", "sniffer6", "explicit"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ViewMapResponse(TypedDict, total=False):
    """Response type for ViewMap - use with .dict property for typed dict access."""
    id: int
    vdom_id: int
    policy_id: int
    id_policy_id: int
    which: Literal["firewall", "interface", "interface6", "sniffer", "sniffer6", "explicit"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ViewMapObject(FortiObject):
    """Typed FortiObject for ViewMap with field access."""
    id: int
    vdom_id: int
    policy_id: int
    id_policy_id: int
    which: Literal["firewall", "interface", "interface6", "sniffer", "sniffer6", "explicit"]


# ================================================================
# Main Endpoint Class
# ================================================================

class ViewMap:
    """
    
    Endpoint: ips/view_map
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
    ) -> ViewMapObject: ...
    
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
    ) -> FortiObjectList[ViewMapObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...




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
        payload_dict: ViewMapPayload | None = ...,
        id: int | None = ...,
        vdom_id: int | None = ...,
        policy_id: int | None = ...,
        id_policy_id: int | None = ...,
        which: Literal["firewall", "interface", "interface6", "sniffer", "sniffer6", "explicit"] | None = ...,
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
    "ViewMap",
    "ViewMapPayload",
    "ViewMapResponse",
    "ViewMapObject",
]