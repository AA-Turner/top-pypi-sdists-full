""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: videofilter/keyword
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

class KeywordWordItem(TypedDict, total=False):
    """Nested item for word field."""
    name: str
    comment: str
    pattern_type: Literal["wildcard", "regex"]
    status: Literal["enable", "disable"]


class KeywordPayload(TypedDict, total=False):
    """Payload type for Keyword operations."""
    id: int
    name: str
    comment: str
    match: Literal["or", "and"]
    word: str | list[str] | list[KeywordWordItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class KeywordResponse(TypedDict, total=False):
    """Response type for Keyword - use with .dict property for typed dict access."""
    id: int
    name: str
    comment: str
    match: Literal["or", "and"]
    word: list[KeywordWordItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class KeywordWordItemObject(FortiObject[KeywordWordItem]):
    """Typed object for word table items with attribute access."""
    name: str
    comment: str
    pattern_type: Literal["wildcard", "regex"]
    status: Literal["enable", "disable"]


class KeywordObject(FortiObject):
    """Typed FortiObject for Keyword with field access."""
    id: int
    name: str
    comment: str
    match: Literal["or", "and"]
    word: FortiObjectList[KeywordWordItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Keyword:
    """
    
    Endpoint: videofilter/keyword
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
    ) -> KeywordObject: ...
    
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
    ) -> FortiObjectList[KeywordObject]: ...
    
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
        payload_dict: KeywordPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        match: Literal["or", "and"] | None = ...,
        word: str | list[str] | list[KeywordWordItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KeywordObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: KeywordPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        match: Literal["or", "and"] | None = ...,
        word: str | list[str] | list[KeywordWordItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KeywordObject: ...

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
        payload_dict: KeywordPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        match: Literal["or", "and"] | None = ...,
        word: str | list[str] | list[KeywordWordItem] | None = ...,
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
    "Keyword",
    "KeywordPayload",
    "KeywordResponse",
    "KeywordObject",
]