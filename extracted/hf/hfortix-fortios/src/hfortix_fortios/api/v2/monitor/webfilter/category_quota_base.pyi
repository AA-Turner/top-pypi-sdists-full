""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: webfilter/category_quota
Category: monitor
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

class CategoryQuotaPayload(TypedDict, total=False):
    """Payload type for CategoryQuota operations."""
    profile: str
    user: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class CategoryQuotaResponse(TypedDict, total=False):
    """Response type for CategoryQuota - use with .dict property for typed dict access."""
    id: int
    category: str
    time: int
    remaining_time: int
    traffic: int
    remaining_traffic: int


class CategoryQuotaObject(FortiObject[CategoryQuotaResponse]):
    """Typed FortiObject for CategoryQuota with field access."""
    id: int
    category: str
    time: int
    remaining_time: int
    traffic: int
    remaining_traffic: int



# ================================================================
# Main Endpoint Class
# ================================================================

class CategoryQuota:
    """
    
    Endpoint: webfilter/category_quota
    Category: monitor
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
        profile: str | None = ...,
        user: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[CategoryQuotaObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CategoryQuotaPayload | None = ...,
        profile: str | None = ...,
        user: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CategoryQuotaObject: ...




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
        payload_dict: CategoryQuotaPayload | None = ...,
        profile: str | None = ...,
        user: str | None = ...,
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
    "CategoryQuota",
    "CategoryQuotaResponse",
    "CategoryQuotaObject",
]