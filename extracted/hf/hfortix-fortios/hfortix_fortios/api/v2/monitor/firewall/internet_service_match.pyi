""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_match
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

class InternetServiceMatchPayload(TypedDict, total=False):
    """Payload type for InternetServiceMatch operations."""
    ip: str
    is_ipv6: bool
    ipv4_mask: str
    ipv6_prefix: int


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class InternetServiceMatchResponse(TypedDict, total=False):
    """Response type for InternetServiceMatch - use with .dict property for typed dict access."""
    id: str
    name: str
    num_matched_services: str
    owner: str
    reputation: str


class InternetServiceMatchObject(FortiObject[InternetServiceMatchResponse]):
    """Typed FortiObject for InternetServiceMatch with field access."""
    id: str
    name: str
    num_matched_services: str
    owner: str
    reputation: str



# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceMatch:
    """
    
    Endpoint: firewall/internet_service_match
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
        ip: str,
        is_ipv6: bool | None = ...,
        ipv4_mask: str | None = ...,
        ipv6_prefix: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[InternetServiceMatchObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceMatchPayload | None = ...,
        ip: str | None = ...,
        is_ipv6: bool | None = ...,
        ipv4_mask: str | None = ...,
        ipv6_prefix: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceMatchObject: ...


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
        payload_dict: InternetServiceMatchPayload | None = ...,
        ip: str | None = ...,
        is_ipv6: bool | None = ...,
        ipv4_mask: str | None = ...,
        ipv6_prefix: int | None = ...,
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
    "InternetServiceMatch",
    "InternetServiceMatchResponse",
    "InternetServiceMatchObject",
]