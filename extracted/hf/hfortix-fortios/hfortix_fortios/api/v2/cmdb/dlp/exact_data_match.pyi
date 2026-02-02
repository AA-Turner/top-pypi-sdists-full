""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: dlp/exact_data_match
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

class ExactDataMatchColumnsItem(TypedDict, total=False):
    """Nested item for columns field."""
    index: int
    type: str
    optional: Literal["enable", "disable"]


class ExactDataMatchPayload(TypedDict, total=False):
    """Payload type for ExactDataMatch operations."""
    name: str
    optional: int
    data: str
    columns: str | list[str] | list[ExactDataMatchColumnsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExactDataMatchResponse(TypedDict, total=False):
    """Response type for ExactDataMatch - use with .dict property for typed dict access."""
    name: str
    optional: int
    data: str
    columns: list[ExactDataMatchColumnsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExactDataMatchColumnsItemObject(FortiObject[ExactDataMatchColumnsItem]):
    """Typed object for columns table items with attribute access."""
    index: int
    type: str
    optional: Literal["enable", "disable"]


class ExactDataMatchObject(FortiObject):
    """Typed FortiObject for ExactDataMatch with field access."""
    name: str
    optional: int
    data: str
    columns: FortiObjectList[ExactDataMatchColumnsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ExactDataMatch:
    """
    
    Endpoint: dlp/exact_data_match
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
    ) -> ExactDataMatchObject: ...
    
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
    ) -> FortiObjectList[ExactDataMatchObject]: ...
    
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
        payload_dict: ExactDataMatchPayload | None = ...,
        name: str | None = ...,
        optional: int | None = ...,
        data: str | None = ...,
        columns: str | list[str] | list[ExactDataMatchColumnsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExactDataMatchObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExactDataMatchPayload | None = ...,
        name: str | None = ...,
        optional: int | None = ...,
        data: str | None = ...,
        columns: str | list[str] | list[ExactDataMatchColumnsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExactDataMatchObject: ...

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
        payload_dict: ExactDataMatchPayload | None = ...,
        name: str | None = ...,
        optional: int | None = ...,
        data: str | None = ...,
        columns: str | list[str] | list[ExactDataMatchColumnsItem] | None = ...,
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
    "ExactDataMatch",
    "ExactDataMatchPayload",
    "ExactDataMatchResponse",
    "ExactDataMatchObject",
]