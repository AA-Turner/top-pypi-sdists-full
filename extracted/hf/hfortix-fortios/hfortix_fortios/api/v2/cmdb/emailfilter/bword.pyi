""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: emailfilter/bword
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

class BwordEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    status: Literal["enable", "disable"]
    id: int
    pattern: str
    pattern_type: Literal["wildcard", "regexp"]
    action: Literal["spam", "clear"]
    where: Literal["subject", "body", "all"]
    language: Literal["western", "simch", "trach", "japanese", "korean", "french", "thai", "spanish"]
    score: int


class BwordPayload(TypedDict, total=False):
    """Payload type for Bword operations."""
    id: int
    name: str
    comment: str
    entries: str | list[str] | list[BwordEntriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class BwordResponse(TypedDict, total=False):
    """Response type for Bword - use with .dict property for typed dict access."""
    id: int
    name: str
    comment: str
    entries: list[BwordEntriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class BwordEntriesItemObject(FortiObject[BwordEntriesItem]):
    """Typed object for entries table items with attribute access."""
    status: Literal["enable", "disable"]
    id: int
    pattern: str
    pattern_type: Literal["wildcard", "regexp"]
    action: Literal["spam", "clear"]
    where: Literal["subject", "body", "all"]
    language: Literal["western", "simch", "trach", "japanese", "korean", "french", "thai", "spanish"]
    score: int


class BwordObject(FortiObject):
    """Typed FortiObject for Bword with field access."""
    id: int
    name: str
    comment: str
    entries: FortiObjectList[BwordEntriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Bword:
    """
    
    Endpoint: emailfilter/bword
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
    ) -> BwordObject: ...
    
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
    ) -> FortiObjectList[BwordObject]: ...
    
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
        payload_dict: BwordPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[BwordEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BwordObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: BwordPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[BwordEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BwordObject: ...

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
        payload_dict: BwordPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[BwordEntriesItem] | None = ...,
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
    "Bword",
    "BwordPayload",
    "BwordResponse",
    "BwordObject",
]