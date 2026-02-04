""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wifi/vlan_probe
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

class VlanProbePayload(TypedDict, total=False):
    """Payload type for VlanProbe operations."""
    ap_interface: int
    wtp: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class VlanProbeResponse(TypedDict, total=False):
    """Response type for VlanProbe - use with .dict property for typed dict access."""
    results: list[str]
    probe_results_exist: bool
    probe_in_progress: bool


class VlanProbeObject(FortiObject[VlanProbeResponse]):
    """Typed FortiObject for VlanProbe with field access."""
    results: list[str]
    probe_results_exist: bool
    probe_in_progress: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class VlanProbe:
    """
    
    Endpoint: wifi/vlan_probe
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
        ap_interface: int,
        wtp: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[VlanProbeObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VlanProbePayload | None = ...,
        ap_interface: int | None = ...,
        wtp: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VlanProbeObject: ...




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
        payload_dict: VlanProbePayload | None = ...,
        ap_interface: int | None = ...,
        wtp: str | None = ...,
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
    "VlanProbe",
    "VlanProbeResponse",
    "VlanProbeObject",
]