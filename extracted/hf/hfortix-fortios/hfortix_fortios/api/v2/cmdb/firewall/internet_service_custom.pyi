""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_custom
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

class InternetServiceCustomEntryPortrangeItem(TypedDict, total=False):
    """Nested item for entry.port-range field."""
    id: int
    start_port: int
    end_port: int


class InternetServiceCustomEntryDstItem(TypedDict, total=False):
    """Nested item for entry.dst field."""
    name: str


class InternetServiceCustomEntryDst6Item(TypedDict, total=False):
    """Nested item for entry.dst6 field."""
    name: str


class InternetServiceCustomEntryItem(TypedDict, total=False):
    """Nested item for entry field."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: str | list[str] | list[InternetServiceCustomEntryPortrangeItem]
    dst: str | list[str] | list[InternetServiceCustomEntryDstItem]
    dst6: str | list[str] | list[InternetServiceCustomEntryDst6Item]


class InternetServiceCustomPayload(TypedDict, total=False):
    """Payload type for InternetServiceCustom operations."""
    name: str
    reputation: int
    comment: str
    entry: str | list[str] | list[InternetServiceCustomEntryItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InternetServiceCustomResponse(TypedDict, total=False):
    """Response type for InternetServiceCustom - use with .dict property for typed dict access."""
    name: str
    reputation: int
    comment: str
    entry: list[InternetServiceCustomEntryItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InternetServiceCustomEntryPortrangeItemObject(FortiObject[InternetServiceCustomEntryPortrangeItem]):
    """Typed object for entry.port-range table items with attribute access."""
    id: int
    start_port: int
    end_port: int


class InternetServiceCustomEntryDstItemObject(FortiObject[InternetServiceCustomEntryDstItem]):
    """Typed object for entry.dst table items with attribute access."""
    name: str


class InternetServiceCustomEntryDst6ItemObject(FortiObject[InternetServiceCustomEntryDst6Item]):
    """Typed object for entry.dst6 table items with attribute access."""
    name: str


class InternetServiceCustomEntryItemObject(FortiObject[InternetServiceCustomEntryItem]):
    """Typed object for entry table items with attribute access."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: FortiObjectList[InternetServiceCustomEntryPortrangeItemObject]
    dst: FortiObjectList[InternetServiceCustomEntryDstItemObject]
    dst6: FortiObjectList[InternetServiceCustomEntryDst6ItemObject]


class InternetServiceCustomObject(FortiObject):
    """Typed FortiObject for InternetServiceCustom with field access."""
    name: str
    reputation: int
    comment: str
    entry: FortiObjectList[InternetServiceCustomEntryItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceCustom:
    """
    
    Endpoint: firewall/internet_service_custom
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
    ) -> InternetServiceCustomObject: ...
    
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
    ) -> FortiObjectList[InternetServiceCustomObject]: ...
    
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
        payload_dict: InternetServiceCustomPayload | None = ...,
        name: str | None = ...,
        reputation: int | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceCustomEntryItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceCustomObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceCustomPayload | None = ...,
        name: str | None = ...,
        reputation: int | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceCustomEntryItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceCustomObject: ...

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
        payload_dict: InternetServiceCustomPayload | None = ...,
        name: str | None = ...,
        reputation: int | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceCustomEntryItem] | None = ...,
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
    "InternetServiceCustom",
    "InternetServiceCustomPayload",
    "InternetServiceCustomResponse",
    "InternetServiceCustomObject",
]