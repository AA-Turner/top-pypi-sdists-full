""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/anqp_roaming_consortium
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

class AnqpRoamingConsortiumOilistItem(TypedDict, total=False):
    """Nested item for oi-list field."""
    index: int
    oi: str
    comment: str


class AnqpRoamingConsortiumPayload(TypedDict, total=False):
    """Payload type for AnqpRoamingConsortium operations."""
    name: str
    oi_list: str | list[str] | list[AnqpRoamingConsortiumOilistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AnqpRoamingConsortiumResponse(TypedDict, total=False):
    """Response type for AnqpRoamingConsortium - use with .dict property for typed dict access."""
    name: str
    oi_list: list[AnqpRoamingConsortiumOilistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AnqpRoamingConsortiumOilistItemObject(FortiObject[AnqpRoamingConsortiumOilistItem]):
    """Typed object for oi-list table items with attribute access."""
    index: int
    oi: str
    comment: str


class AnqpRoamingConsortiumObject(FortiObject):
    """Typed FortiObject for AnqpRoamingConsortium with field access."""
    name: str
    oi_list: FortiObjectList[AnqpRoamingConsortiumOilistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class AnqpRoamingConsortium:
    """
    
    Endpoint: wireless_controller/hotspot20/anqp_roaming_consortium
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
    ) -> AnqpRoamingConsortiumObject: ...
    
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
    ) -> FortiObjectList[AnqpRoamingConsortiumObject]: ...
    
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
        payload_dict: AnqpRoamingConsortiumPayload | None = ...,
        name: str | None = ...,
        oi_list: str | list[str] | list[AnqpRoamingConsortiumOilistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpRoamingConsortiumObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AnqpRoamingConsortiumPayload | None = ...,
        name: str | None = ...,
        oi_list: str | list[str] | list[AnqpRoamingConsortiumOilistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpRoamingConsortiumObject: ...

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
        payload_dict: AnqpRoamingConsortiumPayload | None = ...,
        name: str | None = ...,
        oi_list: str | list[str] | list[AnqpRoamingConsortiumOilistItem] | None = ...,
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
    "AnqpRoamingConsortium",
    "AnqpRoamingConsortiumPayload",
    "AnqpRoamingConsortiumResponse",
    "AnqpRoamingConsortiumObject",
]