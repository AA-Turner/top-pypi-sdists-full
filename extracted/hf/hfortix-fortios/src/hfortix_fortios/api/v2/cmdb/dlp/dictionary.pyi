""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: dlp/dictionary
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

class DictionaryEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    id: int
    type: str
    pattern: str
    ignore_case: Literal["enable", "disable"]
    repeat: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    comment: str


class DictionaryPayload(TypedDict, total=False):
    """Payload type for Dictionary operations."""
    uuid: str
    name: str
    match_type: Literal["match-all", "match-any"]
    match_around: Literal["enable", "disable"]
    comment: str
    entries: str | list[str] | list[DictionaryEntriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DictionaryResponse(TypedDict, total=False):
    """Response type for Dictionary - use with .dict property for typed dict access."""
    uuid: str
    name: str
    match_type: Literal["match-all", "match-any"]
    match_around: Literal["enable", "disable"]
    comment: str
    entries: list[DictionaryEntriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DictionaryEntriesItemObject(FortiObject[DictionaryEntriesItem]):
    """Typed object for entries table items with attribute access."""
    id: int
    type: str
    pattern: str
    ignore_case: Literal["enable", "disable"]
    repeat: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    comment: str


class DictionaryObject(FortiObject):
    """Typed FortiObject for Dictionary with field access."""
    uuid: str
    name: str
    match_type: Literal["match-all", "match-any"]
    match_around: Literal["enable", "disable"]
    comment: str
    entries: FortiObjectList[DictionaryEntriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Dictionary:
    """
    
    Endpoint: dlp/dictionary
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
    ) -> DictionaryObject: ...
    
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
    ) -> FortiObjectList[DictionaryObject]: ...
    
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
        payload_dict: DictionaryPayload | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        match_type: Literal["match-all", "match-any"] | None = ...,
        match_around: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[DictionaryEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DictionaryObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DictionaryPayload | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        match_type: Literal["match-all", "match-any"] | None = ...,
        match_around: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[DictionaryEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DictionaryObject: ...

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
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
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
        payload_dict: DictionaryPayload | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        match_type: Literal["match-all", "match-any"] | None = ...,
        match_around: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[DictionaryEntriesItem] | None = ...,
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
    "Dictionary",
    "DictionaryPayload",
    "DictionaryResponse",
    "DictionaryObject",
]