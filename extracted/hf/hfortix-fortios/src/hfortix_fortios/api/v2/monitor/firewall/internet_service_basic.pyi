""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_basic
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

class InternetServiceBasicPayload(TypedDict, total=False):
    """Payload type for InternetServiceBasic operations."""
    ipv6_only: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class InternetServiceBasicResponse(TypedDict, total=False):
    """Response type for InternetServiceBasic - use with .dict property for typed dict access."""
    id: int
    q_origin_key: int
    name: str
    direction: str
    database: str
    ip_range_number: int
    ip6_range_number: int
    ip_number: int
    icon_id: int


class InternetServiceBasicObject(FortiObject[InternetServiceBasicResponse]):
    """Typed FortiObject for InternetServiceBasic with field access."""
    id: int
    q_origin_key: int
    name: str
    direction: str
    database: str
    ip_range_number: int
    ip6_range_number: int
    ip_number: int
    icon_id: int



# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceBasic:
    """
    
    Endpoint: firewall/internet_service_basic
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
        ipv6_only: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[InternetServiceBasicObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceBasicPayload | None = ...,
        ipv6_only: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceBasicObject: ...




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
        payload_dict: InternetServiceBasicPayload | None = ...,
        ipv6_only: bool | None = ...,
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
    "InternetServiceBasic",
    "InternetServiceBasicResponse",
    "InternetServiceBasicObject",
]