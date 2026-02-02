""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: emailfilter/block_allow_list
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

class BlockAllowListEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    status: Literal["enable", "disable"]
    id: int
    type: Literal["ip", "email-to", "email-from", "subject"]
    action: Literal["reject", "spam", "clear"]
    addr_type: Literal["ipv4", "ipv6"]
    ip4_subnet: str
    ip6_subnet: str
    pattern_type: Literal["wildcard", "regexp"]
    pattern: str


class BlockAllowListPayload(TypedDict, total=False):
    """Payload type for BlockAllowList operations."""
    id: int
    name: str
    comment: str
    entries: str | list[str] | list[BlockAllowListEntriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class BlockAllowListResponse(TypedDict, total=False):
    """Response type for BlockAllowList - use with .dict property for typed dict access."""
    id: int
    name: str
    comment: str
    entries: list[BlockAllowListEntriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class BlockAllowListEntriesItemObject(FortiObject[BlockAllowListEntriesItem]):
    """Typed object for entries table items with attribute access."""
    status: Literal["enable", "disable"]
    id: int
    type: Literal["ip", "email-to", "email-from", "subject"]
    action: Literal["reject", "spam", "clear"]
    addr_type: Literal["ipv4", "ipv6"]
    ip4_subnet: str
    ip6_subnet: str
    pattern_type: Literal["wildcard", "regexp"]
    pattern: str


class BlockAllowListObject(FortiObject):
    """Typed FortiObject for BlockAllowList with field access."""
    id: int
    name: str
    comment: str
    entries: FortiObjectList[BlockAllowListEntriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class BlockAllowList:
    """
    
    Endpoint: emailfilter/block_allow_list
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
    ) -> BlockAllowListObject: ...
    
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
    ) -> FortiObjectList[BlockAllowListObject]: ...
    
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
        payload_dict: BlockAllowListPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[BlockAllowListEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BlockAllowListObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: BlockAllowListPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[BlockAllowListEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BlockAllowListObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

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
        payload_dict: BlockAllowListPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[BlockAllowListEntriesItem] | None = ...,
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
    "BlockAllowList",
    "BlockAllowListPayload",
    "BlockAllowListResponse",
    "BlockAllowListObject",
]