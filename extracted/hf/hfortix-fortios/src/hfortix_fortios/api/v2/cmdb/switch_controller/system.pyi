""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/system
Category: cmdb
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

class SystemPayload(TypedDict, total=False):
    """Payload type for System operations."""
    parallel_process_override: Literal["disable", "enable"]
    parallel_process: int
    data_sync_interval: int
    iot_weight_threshold: int
    iot_scan_interval: int
    iot_holdoff: int
    iot_mac_idle: int
    nac_periodic_interval: int
    dynamic_periodic_interval: int
    tunnel_mode: Literal["compatible", "moderate", "strict"]
    caputp_echo_interval: int
    caputp_max_retransmit: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SystemResponse(TypedDict, total=False):
    """Response type for System - use with .dict property for typed dict access."""
    parallel_process_override: Literal["disable", "enable"]
    parallel_process: int
    data_sync_interval: int
    iot_weight_threshold: int
    iot_scan_interval: int
    iot_holdoff: int
    iot_mac_idle: int
    nac_periodic_interval: int
    dynamic_periodic_interval: int
    tunnel_mode: Literal["compatible", "moderate", "strict"]
    caputp_echo_interval: int
    caputp_max_retransmit: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SystemObject(FortiObject):
    """Typed FortiObject for System with field access."""
    parallel_process_override: Literal["disable", "enable"]
    parallel_process: int
    data_sync_interval: int
    iot_weight_threshold: int
    iot_scan_interval: int
    iot_holdoff: int
    iot_mac_idle: int
    nac_periodic_interval: int
    dynamic_periodic_interval: int
    tunnel_mode: Literal["compatible", "moderate", "strict"]
    caputp_echo_interval: int
    caputp_max_retransmit: int


# ================================================================
# Main Endpoint Class
# ================================================================

class System:
    """
    
    Endpoint: switch_controller/system
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SystemObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SystemPayload | None = ...,
        parallel_process_override: Literal["disable", "enable"] | None = ...,
        parallel_process: int | None = ...,
        data_sync_interval: int | None = ...,
        iot_weight_threshold: int | None = ...,
        iot_scan_interval: int | None = ...,
        iot_holdoff: int | None = ...,
        iot_mac_idle: int | None = ...,
        nac_periodic_interval: int | None = ...,
        dynamic_periodic_interval: int | None = ...,
        tunnel_mode: Literal["compatible", "moderate", "strict"] | None = ...,
        caputp_echo_interval: int | None = ...,
        caputp_max_retransmit: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SystemObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SystemPayload | None = ...,
        parallel_process_override: Literal["disable", "enable"] | None = ...,
        parallel_process: int | None = ...,
        data_sync_interval: int | None = ...,
        iot_weight_threshold: int | None = ...,
        iot_scan_interval: int | None = ...,
        iot_holdoff: int | None = ...,
        iot_mac_idle: int | None = ...,
        nac_periodic_interval: int | None = ...,
        dynamic_periodic_interval: int | None = ...,
        tunnel_mode: Literal["compatible", "moderate", "strict"] | None = ...,
        caputp_echo_interval: int | None = ...,
        caputp_max_retransmit: int | None = ...,
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
    "System",
    "SystemPayload",
    "SystemResponse",
    "SystemObject",
]