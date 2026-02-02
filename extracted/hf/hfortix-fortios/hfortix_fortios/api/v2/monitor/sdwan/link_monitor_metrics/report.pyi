""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: sdwan/link_monitor_metrics/report
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

class ReportPayload(TypedDict, total=False):
    """Payload type for Report operations."""
    agent_ip: str
    application_name: str
    application_id: int
    latency: str
    jitter: str
    packet_loss: str
    ntt: str
    srt: str
    application_error: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ReportResponse(TypedDict, total=False):
    """Response type for Report - use with .dict property for typed dict access."""
    agent_ip: str
    application_name: str
    application_id: int
    latency: str
    jitter: str
    packet_loss: str
    ntt: str
    srt: str
    application_error: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ReportObject(FortiObject):
    """Typed FortiObject for Report with field access."""
    agent_ip: str
    application_name: str
    application_id: int
    latency: str
    jitter: str
    packet_loss: str
    ntt: str
    srt: str
    application_error: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Report:
    """
    
    Endpoint: sdwan/link_monitor_metrics/report
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
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ReportObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: ReportPayload | None = ...,
        agent_ip: str | None = ...,
        application_name: str | None = ...,
        application_id: int | None = ...,
        latency: str | None = ...,
        jitter: str | None = ...,
        packet_loss: str | None = ...,
        ntt: str | None = ...,
        srt: str | None = ...,
        application_error: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ReportObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ReportPayload | None = ...,
        agent_ip: str | None = ...,
        application_name: str | None = ...,
        application_id: int | None = ...,
        latency: str | None = ...,
        jitter: str | None = ...,
        packet_loss: str | None = ...,
        ntt: str | None = ...,
        srt: str | None = ...,
        application_error: str | None = ...,
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
        agent_ip: str | None = ...,
        application_name: str | None = ...,
        application_id: int | None = ...,
        latency: str | None = ...,
        jitter: str | None = ...,
        packet_loss: str | None = ...,
        ntt: str | None = ...,
        srt: str | None = ...,
        application_error: str | None = ...,
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
    "ReportPayload",
    "ReportResponse",
    "ReportObject",
]