""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/interface/speed_test_status
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

class SpeedTestStatusPayload(TypedDict, total=False):
    """Payload type for SpeedTestStatus operations."""
    id: int


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class SpeedTestStatusResponse(TypedDict, total=False):
    """Response type for SpeedTestStatus - use with .dict property for typed dict access."""
    progress: int
    measured_upstream_bandwidth: int
    measured_downstream_bandwidth: int
    measure_time: int
    error_code: int


class SpeedTestStatusObject(FortiObject[SpeedTestStatusResponse]):
    """Typed FortiObject for SpeedTestStatus with field access."""
    progress: int
    measured_upstream_bandwidth: int
    measured_downstream_bandwidth: int
    measure_time: int
    error_code: int



# ================================================================
# Main Endpoint Class
# ================================================================

class SpeedTestStatus:
    """
    
    Endpoint: system/interface/speed_test_status
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
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[SpeedTestStatusObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SpeedTestStatusPayload | None = ...,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SpeedTestStatusObject: ...


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
        payload_dict: SpeedTestStatusPayload | None = ...,
        id: int | None = ...,
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
    "SpeedTestStatus",
    "SpeedTestStatusResponse",
    "SpeedTestStatusObject",
]