""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_subapp
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

class InternetServiceSubappSubappItem(TypedDict, total=False):
    """Nested item for sub-app field."""
    id: int


class InternetServiceSubappPayload(TypedDict, total=False):
    """Payload type for InternetServiceSubapp operations."""
    id: int
    sub_app: str | list[str] | list[InternetServiceSubappSubappItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InternetServiceSubappResponse(TypedDict, total=False):
    """Response type for InternetServiceSubapp - use with .dict property for typed dict access."""
    id: int
    sub_app: list[InternetServiceSubappSubappItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InternetServiceSubappSubappItemObject(FortiObject[InternetServiceSubappSubappItem]):
    """Typed object for sub-app table items with attribute access."""
    id: int


class InternetServiceSubappObject(FortiObject):
    """Typed FortiObject for InternetServiceSubapp with field access."""
    id: int
    sub_app: FortiObjectList[InternetServiceSubappSubappItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceSubapp:
    """
    
    Endpoint: firewall/internet_service_subapp
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceSubappObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[InternetServiceSubappObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...




    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServiceSubappPayload | None = ...,
        id: int | None = ...,
        sub_app: str | list[str] | list[InternetServiceSubappSubappItem] | None = ...,
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
    "InternetServiceSubapp",
    "InternetServiceSubappPayload",
    "InternetServiceSubappResponse",
    "InternetServiceSubappObject",
]