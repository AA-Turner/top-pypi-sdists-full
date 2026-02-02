""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: webfilter/ftgd_local_cat
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

class FtgdLocalCatPayload(TypedDict, total=False):
    """Payload type for FtgdLocalCat operations."""
    status: Literal["enable", "disable"]
    id: int
    desc: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FtgdLocalCatResponse(TypedDict, total=False):
    """Response type for FtgdLocalCat - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    id: int
    desc: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FtgdLocalCatObject(FortiObject):
    """Typed FortiObject for FtgdLocalCat with field access."""
    status: Literal["enable", "disable"]
    id: int
    desc: str


# ================================================================
# Main Endpoint Class
# ================================================================

class FtgdLocalCat:
    """
    
    Endpoint: webfilter/ftgd_local_cat
    Category: cmdb
    MKey: desc
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
        desc: str,
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
    ) -> FtgdLocalCatObject: ...
    
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
    ) -> FortiObjectList[FtgdLocalCatObject]: ...
    
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
        payload_dict: FtgdLocalCatPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        id: int | None = ...,
        desc: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FtgdLocalCatObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FtgdLocalCatPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        id: int | None = ...,
        desc: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FtgdLocalCatObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        desc: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        desc: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FtgdLocalCatPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        id: int | None = ...,
        desc: str | None = ...,
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
    "FtgdLocalCat",
    "FtgdLocalCatPayload",
    "FtgdLocalCatResponse",
    "FtgdLocalCatObject",
]