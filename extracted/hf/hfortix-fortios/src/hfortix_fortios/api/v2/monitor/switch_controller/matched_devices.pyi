""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/matched_devices
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

class MatchedDevicesPayload(TypedDict, total=False):
    """Payload type for MatchedDevices operations."""
    mkey: str
    include_dynamic: bool
    mac: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class MatchedDevicesResponse(TypedDict, total=False):
    """Response type for MatchedDevices - use with .dict property for typed dict access."""
    mac: str
    last_known_switch: str
    last_known_port: str
    matched_nac_policy: str
    matched_dynamic_port_policy: str
    mac_policy: str
    matched_policy: str
    is_dynamic: bool
    is_nac: bool


class MatchedDevicesObject(FortiObject[MatchedDevicesResponse]):
    """Typed FortiObject for MatchedDevices with field access."""
    mac: str
    last_known_switch: str
    last_known_port: str
    matched_nac_policy: str
    matched_dynamic_port_policy: str
    mac_policy: str
    matched_policy: str
    is_dynamic: bool
    is_nac: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class MatchedDevices:
    """
    
    Endpoint: switch_controller/matched_devices
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
        mkey: str | None = ...,
        include_dynamic: bool | None = ...,
        mac: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[MatchedDevicesObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MatchedDevicesPayload | None = ...,
        mkey: str | None = ...,
        include_dynamic: bool | None = ...,
        mac: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MatchedDevicesObject: ...




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
        payload_dict: MatchedDevicesPayload | None = ...,
        mkey: str | None = ...,
        include_dynamic: bool | None = ...,
        mac: str | None = ...,
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
    "MatchedDevices",
    "MatchedDevicesResponse",
    "MatchedDevicesObject",
]