""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: security_rating/report
Category: service
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class ReportPayload(TypedDict, total=False):
    """Payload type for Report operations."""
    scope: Literal["global", "vdom"]
    standalone: str
    type: Literal["psirt", "insight"]
    checks: str
    show_hidden: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class ReportResponse(TypedDict, total=False):
    """Response type for Report - use with .dict property for typed dict access."""
    check: str
    title: str
    description: str
    severity: str
    customMetadata: str
    summary: list[str]


class ReportObject(FortiObject[ReportResponse]):
    """Typed FortiObject for Report with field access."""
    check: str
    title: str
    description: str
    severity: str
    customMetadata: str
    summary: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class Report:
    """
    
    Endpoint: security_rating/report
    Category: service
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        scope: Literal["global", "vdom"] | None = ...,
        standalone: str | None = ...,
        type: Literal["psirt", "insight"],
        checks: str | None = ...,
        show_hidden: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[ReportObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ReportPayload | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        standalone: str | None = ...,
        type: Literal["psirt", "insight"] | None = ...,
        checks: str | None = ...,
        show_hidden: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ReportObject: ...


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
        payload_dict: ReportPayload | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        standalone: str | None = ...,
        type: Literal["psirt", "insight"] | None = ...,
        checks: str | None = ...,
        show_hidden: str | None = ...,
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
    "Report",
    "ReportResponse",
    "ReportObject",
]