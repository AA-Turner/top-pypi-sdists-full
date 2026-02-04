""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/resource/usage
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

class UsagePayload(TypedDict, total=False):
    """Payload type for Usage operations."""
    scope: Literal["vdom", "global"]
    resource: Literal["cpu", "mem", "disk", "session", "session6", "setuprate", "setuprate6", "disk_lograte", "faz_lograte", "forticloud_lograte", "gtp_tunnel", "gtp_tunnel_setup_rate"]
    interval: Literal["1-min", "10-min", "30-min", "1-hour", "12-hour", "24-hour"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class UsageResponse(TypedDict, total=False):
    """Response type for Usage - use with .dict property for typed dict access."""
    cpu: list[str]
    disk: list[str]
    disk_lograte: list[str]
    faz_cloud_lograte: list[str]
    faz_lograte: list[str]
    forticloud_lograte: list[str]
    gtp_tunnel: list[str]
    gtp_tunnel_setup_rate: list[str]
    mem: list[str]
    session: list[str]
    session6: list[str]
    setuprate: list[str]
    setuprate6: list[str]
    npu_session: list[str]
    npu_session6: list[str]
    nturbo_session: list[str]
    nturbo_session6: list[str]
    hw_session: list[str]
    hw_session6: list[str]
    hw_setuprate: list[str]
    hw_setuprate6: list[str]
    hw_ps_log_rate: list[str]
    hw_pm_log_rate: list[str]


class UsageObject(FortiObject[UsageResponse]):
    """Typed FortiObject for Usage with field access."""
    cpu: list[str]
    disk: list[str]
    disk_lograte: list[str]
    faz_cloud_lograte: list[str]
    faz_lograte: list[str]
    forticloud_lograte: list[str]
    gtp_tunnel: list[str]
    gtp_tunnel_setup_rate: list[str]
    mem: list[str]
    session: list[str]
    session6: list[str]
    setuprate: list[str]
    setuprate6: list[str]
    npu_session: list[str]
    npu_session6: list[str]
    nturbo_session: list[str]
    nturbo_session6: list[str]
    hw_session: list[str]
    hw_session6: list[str]
    hw_setuprate: list[str]
    hw_setuprate6: list[str]
    hw_ps_log_rate: list[str]
    hw_pm_log_rate: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class Usage:
    """
    
    Endpoint: system/resource/usage
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
        scope: Literal["vdom", "global"] | None = ...,
        resource: Literal["cpu", "mem", "disk", "session", "session6", "setuprate", "setuprate6", "disk_lograte", "faz_lograte", "forticloud_lograte", "gtp_tunnel", "gtp_tunnel_setup_rate"] | None = ...,
        interval: Literal["1-min", "10-min", "30-min", "1-hour", "12-hour", "24-hour"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[UsageObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UsagePayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        resource: Literal["cpu", "mem", "disk", "session", "session6", "setuprate", "setuprate6", "disk_lograte", "faz_lograte", "forticloud_lograte", "gtp_tunnel", "gtp_tunnel_setup_rate"] | None = ...,
        interval: Literal["1-min", "10-min", "30-min", "1-hour", "12-hour", "24-hour"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UsageObject: ...




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
        payload_dict: UsagePayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        resource: Literal["cpu", "mem", "disk", "session", "session6", "setuprate", "setuprate6", "disk_lograte", "faz_lograte", "forticloud_lograte", "gtp_tunnel", "gtp_tunnel_setup_rate"] | None = ...,
        interval: Literal["1-min", "10-min", "30-min", "1-hour", "12-hour", "24-hour"] | None = ...,
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
    "Usage",
    "UsageResponse",
    "UsageObject",
]