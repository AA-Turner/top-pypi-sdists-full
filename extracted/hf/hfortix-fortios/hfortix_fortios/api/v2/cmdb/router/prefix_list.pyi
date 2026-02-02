""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/prefix_list
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

class PrefixListRuleItem(TypedDict, total=False):
    """Nested item for rule field."""
    id: int
    action: Literal["permit", "deny"]
    prefix: str
    ge: int
    le: int


class PrefixListPayload(TypedDict, total=False):
    """Payload type for PrefixList operations."""
    name: str
    comments: str
    rule: str | list[str] | list[PrefixListRuleItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PrefixListResponse(TypedDict, total=False):
    """Response type for PrefixList - use with .dict property for typed dict access."""
    name: str
    comments: str
    rule: list[PrefixListRuleItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PrefixListRuleItemObject(FortiObject[PrefixListRuleItem]):
    """Typed object for rule table items with attribute access."""
    id: int
    action: Literal["permit", "deny"]
    prefix: str
    ge: int
    le: int


class PrefixListObject(FortiObject):
    """Typed FortiObject for PrefixList with field access."""
    name: str
    comments: str
    rule: FortiObjectList[PrefixListRuleItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class PrefixList:
    """
    
    Endpoint: router/prefix_list
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
    ) -> PrefixListObject: ...
    
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
    ) -> FortiObjectList[PrefixListObject]: ...
    
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
        payload_dict: PrefixListPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[PrefixListRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PrefixListObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PrefixListPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[PrefixListRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PrefixListObject: ...

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
        payload_dict: PrefixListPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[PrefixListRuleItem] | None = ...,
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
    "PrefixList",
    "PrefixListPayload",
    "PrefixListResponse",
    "PrefixListObject",
]