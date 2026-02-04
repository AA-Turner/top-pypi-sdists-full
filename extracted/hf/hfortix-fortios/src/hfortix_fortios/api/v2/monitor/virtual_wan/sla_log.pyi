""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: virtual_wan/sla_log
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

class SlaLogPayload(TypedDict, total=False):
    """Payload type for SlaLog operations."""
    sla: list[str]
    interface: str
    since: int
    seconds: int
    latest: bool
    min_sample_interval: int
    sampling_interval: int
    skip_vpn_child: bool
    include_sla_targets_met: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class SlaLogResponse(TypedDict, total=False):
    """Response type for SlaLog - use with .dict property for typed dict access."""
    name: str
    interface: str
    logs: list[str]
    child_intfs: str


class SlaLogObject(FortiObject[SlaLogResponse]):
    """Typed FortiObject for SlaLog with field access."""
    name: str
    interface: str
    logs: list[str]
    child_intfs: str



# ================================================================
# Main Endpoint Class
# ================================================================

class SlaLog:
    """
    
    Endpoint: virtual_wan/sla_log
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
        sla: list[str] | None = ...,
        interface: str | None = ...,
        since: int | None = ...,
        seconds: int | None = ...,
        latest: bool | None = ...,
        min_sample_interval: int | None = ...,
        sampling_interval: int | None = ...,
        skip_vpn_child: bool | None = ...,
        include_sla_targets_met: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[SlaLogObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SlaLogPayload | None = ...,
        sla: list[str] | None = ...,
        interface: str | None = ...,
        since: int | None = ...,
        seconds: int | None = ...,
        latest: bool | None = ...,
        min_sample_interval: int | None = ...,
        sampling_interval: int | None = ...,
        skip_vpn_child: bool | None = ...,
        include_sla_targets_met: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SlaLogObject: ...




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
        payload_dict: SlaLogPayload | None = ...,
        sla: list[str] | None = ...,
        interface: str | None = ...,
        since: int | None = ...,
        seconds: int | None = ...,
        latest: bool | None = ...,
        min_sample_interval: int | None = ...,
        sampling_interval: int | None = ...,
        skip_vpn_child: bool | None = ...,
        include_sla_targets_met: bool | None = ...,
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
    "SlaLog",
    "SlaLogResponse",
    "SlaLogObject",
]