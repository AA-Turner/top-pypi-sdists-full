""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wifi/station_capability
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

class StationCapabilityPayload(TypedDict, total=False):
    """Payload type for StationCapability operations."""
    mac_address: str
    min_age: int
    max_age: int


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class StationCapabilityResponse(TypedDict, total=False):
    """Response type for StationCapability - use with .dict property for typed dict access."""
    mac_address: str
    vfid: int
    band_capability: list[str]
    wtp: list[str]


class StationCapabilityObject(FortiObject[StationCapabilityResponse]):
    """Typed FortiObject for StationCapability with field access."""
    mac_address: str
    vfid: int
    band_capability: list[str]
    wtp: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class StationCapability:
    """
    
    Endpoint: wifi/station_capability
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
        mac_address: str | None = ...,
        min_age: int | None = ...,
        max_age: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[StationCapabilityObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StationCapabilityPayload | None = ...,
        mac_address: str | None = ...,
        min_age: int | None = ...,
        max_age: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StationCapabilityObject: ...




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
        payload_dict: StationCapabilityPayload | None = ...,
        mac_address: str | None = ...,
        min_age: int | None = ...,
        max_age: int | None = ...,
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
    "StationCapability",
    "StationCapabilityResponse",
    "StationCapabilityObject",
]