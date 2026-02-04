""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/collected_email
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

class CollectedEmailPayload(TypedDict, total=False):
    """Payload type for CollectedEmail operations."""
    ipv6: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class CollectedEmailResponse(TypedDict, total=False):
    """Response type for CollectedEmail - use with .dict property for typed dict access."""
    collected_email: str
    duration_secs: int
    ipaddr: str
    expiry_secs: int
    traffic_vol_bytes: int
    mac: str


class CollectedEmailObject(FortiObject[CollectedEmailResponse]):
    """Typed FortiObject for CollectedEmail with field access."""
    collected_email: str
    duration_secs: int
    ipaddr: str
    expiry_secs: int
    traffic_vol_bytes: int
    mac: str



# ================================================================
# Main Endpoint Class
# ================================================================

class CollectedEmail:
    """
    
    Endpoint: user/collected_email
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
        ipv6: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[CollectedEmailObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CollectedEmailPayload | None = ...,
        ipv6: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CollectedEmailObject: ...




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
        payload_dict: CollectedEmailPayload | None = ...,
        ipv6: bool | None = ...,
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
    "CollectedEmail",
    "CollectedEmailResponse",
    "CollectedEmailObject",
]