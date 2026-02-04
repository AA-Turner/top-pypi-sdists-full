""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: endpoint_control/ems/status
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

class StatusPayload(TypedDict, total=False):
    """Payload type for Status operations."""
    ems_id: int
    scope: Literal["vdom", "global"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class StatusResponse(TypedDict, total=False):
    """Response type for Status - use with .dict property for typed dict access."""
    ems_id: int
    ems_name: str
    ems_serial: str
    ems_tenant_id: str
    ems_status_id: int
    ems_status: str
    ems_is_connected: bool
    ems_is_verified: bool
    api_status: list[str]
    ws_status: str
    mgmt_ip: str
    mgmt_port: int


class StatusObject(FortiObject[StatusResponse]):
    """Typed FortiObject for Status with field access."""
    ems_id: int
    ems_name: str
    ems_serial: str
    ems_tenant_id: str
    ems_status_id: int
    ems_status: str
    ems_is_connected: bool
    ems_is_verified: bool
    api_status: list[str]
    ws_status: str
    mgmt_ip: str
    mgmt_port: int



# ================================================================
# Main Endpoint Class
# ================================================================

class Status:
    """
    
    Endpoint: endpoint_control/ems/status
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
        ems_id: int | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[StatusObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StatusPayload | None = ...,
        ems_id: int | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StatusObject: ...




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
        payload_dict: StatusPayload | None = ...,
        ems_id: int | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
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
    "Status",
    "StatusResponse",
    "StatusObject",
]