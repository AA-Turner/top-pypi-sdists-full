""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service
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

class InternetServicePayload(TypedDict, total=False):
    """Payload type for InternetService operations."""
    id: int
    name: str
    icon_id: int
    direction: Literal["src", "dst", "both"]
    database: Literal["isdb", "irdb"]
    ip_range_number: int
    extra_ip_range_number: int
    ip_number: int
    ip6_range_number: int
    extra_ip6_range_number: int
    singularity: int
    obsolete: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InternetServiceResponse(TypedDict, total=False):
    """Response type for InternetService - use with .dict property for typed dict access."""
    id: int
    name: str
    icon_id: int
    direction: Literal["src", "dst", "both"]
    database: Literal["isdb", "irdb"]
    ip_range_number: int
    extra_ip_range_number: int
    ip_number: int
    ip6_range_number: int
    extra_ip6_range_number: int
    singularity: int
    obsolete: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InternetServiceObject(FortiObject):
    """Typed FortiObject for InternetService with field access."""
    id: int
    name: str
    icon_id: int
    direction: Literal["src", "dst", "both"]
    database: Literal["isdb", "irdb"]
    ip_range_number: int
    extra_ip_range_number: int
    ip_number: int
    ip6_range_number: int
    extra_ip6_range_number: int
    singularity: int
    obsolete: int


# ================================================================
# Main Endpoint Class
# ================================================================

class InternetService:
    """
    
    Endpoint: firewall/internet_service
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
    ) -> InternetServiceObject: ...
    
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
    ) -> FortiObjectList[InternetServiceObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...




    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
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
    "InternetService",
    "InternetServicePayload",
    "InternetServiceResponse",
    "InternetServiceObject",
]