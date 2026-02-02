""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/virtual_wire_pair
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

class VirtualWirePairMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    interface_name: str


class VirtualWirePairPayload(TypedDict, total=False):
    """Payload type for VirtualWirePair operations."""
    name: str
    member: str | list[str] | list[VirtualWirePairMemberItem]
    wildcard_vlan: Literal["enable", "disable"]
    vlan_filter: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VirtualWirePairResponse(TypedDict, total=False):
    """Response type for VirtualWirePair - use with .dict property for typed dict access."""
    name: str
    member: list[VirtualWirePairMemberItem]
    wildcard_vlan: Literal["enable", "disable"]
    vlan_filter: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VirtualWirePairMemberItemObject(FortiObject[VirtualWirePairMemberItem]):
    """Typed object for member table items with attribute access."""
    interface_name: str


class VirtualWirePairObject(FortiObject):
    """Typed FortiObject for VirtualWirePair with field access."""
    name: str
    member: FortiObjectList[VirtualWirePairMemberItemObject]
    wildcard_vlan: Literal["enable", "disable"]
    vlan_filter: str


# ================================================================
# Main Endpoint Class
# ================================================================

class VirtualWirePair:
    """
    
    Endpoint: system/virtual_wire_pair
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VirtualWirePairObject: ...
    
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
    ) -> FortiObjectList[VirtualWirePairObject]: ...
    
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
        payload_dict: VirtualWirePairPayload | None = ...,
        name: str | None = ...,
        member: str | list[str] | list[VirtualWirePairMemberItem] | None = ...,
        wildcard_vlan: Literal["enable", "disable"] | None = ...,
        vlan_filter: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VirtualWirePairObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VirtualWirePairPayload | None = ...,
        name: str | None = ...,
        member: str | list[str] | list[VirtualWirePairMemberItem] | None = ...,
        wildcard_vlan: Literal["enable", "disable"] | None = ...,
        vlan_filter: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VirtualWirePairObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
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
        payload_dict: VirtualWirePairPayload | None = ...,
        name: str | None = ...,
        member: str | list[str] | list[VirtualWirePairMemberItem] | None = ...,
        wildcard_vlan: Literal["enable", "disable"] | None = ...,
        vlan_filter: str | None = ...,
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
    "VirtualWirePair",
    "VirtualWirePairPayload",
    "VirtualWirePairResponse",
    "VirtualWirePairObject",
]