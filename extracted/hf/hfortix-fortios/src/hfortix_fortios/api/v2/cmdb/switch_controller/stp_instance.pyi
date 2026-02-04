""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/stp_instance
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

class StpInstanceVlanrangeItem(TypedDict, total=False):
    """Nested item for vlan-range field."""
    vlan_name: str


class StpInstancePayload(TypedDict, total=False):
    """Payload type for StpInstance operations."""
    id: str
    vlan_range: str | list[str] | list[StpInstanceVlanrangeItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StpInstanceResponse(TypedDict, total=False):
    """Response type for StpInstance - use with .dict property for typed dict access."""
    id: str
    vlan_range: list[StpInstanceVlanrangeItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StpInstanceVlanrangeItemObject(FortiObject[StpInstanceVlanrangeItem]):
    """Typed object for vlan-range table items with attribute access."""
    vlan_name: str


class StpInstanceObject(FortiObject):
    """Typed FortiObject for StpInstance with field access."""
    id: str
    vlan_range: FortiObjectList[StpInstanceVlanrangeItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class StpInstance:
    """
    
    Endpoint: switch_controller/stp_instance
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
        id: str,
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
    ) -> StpInstanceObject: ...
    
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
    ) -> FortiObjectList[StpInstanceObject]: ...
    
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
        payload_dict: StpInstancePayload | None = ...,
        id: str | None = ...,
        vlan_range: str | list[str] | list[StpInstanceVlanrangeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StpInstanceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StpInstancePayload | None = ...,
        id: str | None = ...,
        vlan_range: str | list[str] | list[StpInstanceVlanrangeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StpInstanceObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: StpInstancePayload | None = ...,
        id: str | None = ...,
        vlan_range: str | list[str] | list[StpInstanceVlanrangeItem] | None = ...,
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
    "StpInstance",
    "StpInstancePayload",
    "StpInstanceResponse",
    "StpInstanceObject",
]