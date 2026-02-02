""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: dlp/data_type
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

class DataTypePayload(TypedDict, total=False):
    """Payload type for DataType operations."""
    name: str
    pattern: str
    verify: str
    verify2: str
    match_around: str
    look_back: int
    look_ahead: int
    match_back: int
    match_ahead: int
    transform: str
    verify_transformed_pattern: Literal["enable", "disable"]
    comment: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DataTypeResponse(TypedDict, total=False):
    """Response type for DataType - use with .dict property for typed dict access."""
    name: str
    pattern: str
    verify: str
    verify2: str
    match_around: str
    look_back: int
    look_ahead: int
    match_back: int
    match_ahead: int
    transform: str
    verify_transformed_pattern: Literal["enable", "disable"]
    comment: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DataTypeObject(FortiObject):
    """Typed FortiObject for DataType with field access."""
    name: str
    pattern: str
    verify: str
    verify2: str
    match_around: str
    look_back: int
    look_ahead: int
    match_back: int
    match_ahead: int
    transform: str
    verify_transformed_pattern: Literal["enable", "disable"]
    comment: str


# ================================================================
# Main Endpoint Class
# ================================================================

class DataType:
    """
    
    Endpoint: dlp/data_type
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
    ) -> DataTypeObject: ...
    
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
    ) -> FortiObjectList[DataTypeObject]: ...
    
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
        payload_dict: DataTypePayload | None = ...,
        name: str | None = ...,
        pattern: str | None = ...,
        verify: str | None = ...,
        verify2: str | None = ...,
        match_around: str | None = ...,
        look_back: int | None = ...,
        look_ahead: int | None = ...,
        match_back: int | None = ...,
        match_ahead: int | None = ...,
        transform: str | None = ...,
        verify_transformed_pattern: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DataTypeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DataTypePayload | None = ...,
        name: str | None = ...,
        pattern: str | None = ...,
        verify: str | None = ...,
        verify2: str | None = ...,
        match_around: str | None = ...,
        look_back: int | None = ...,
        look_ahead: int | None = ...,
        match_back: int | None = ...,
        match_ahead: int | None = ...,
        transform: str | None = ...,
        verify_transformed_pattern: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DataTypeObject: ...

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
        payload_dict: DataTypePayload | None = ...,
        name: str | None = ...,
        pattern: str | None = ...,
        verify: str | None = ...,
        verify2: str | None = ...,
        match_around: str | None = ...,
        look_back: int | None = ...,
        look_ahead: int | None = ...,
        match_back: int | None = ...,
        match_ahead: int | None = ...,
        transform: str | None = ...,
        verify_transformed_pattern: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
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
    "DataType",
    "DataTypePayload",
    "DataTypeResponse",
    "DataTypeObject",
]