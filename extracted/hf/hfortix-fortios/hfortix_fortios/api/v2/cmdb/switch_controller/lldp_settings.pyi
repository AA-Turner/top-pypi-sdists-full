""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/lldp_settings
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

class LldpSettingsPayload(TypedDict, total=False):
    """Payload type for LldpSettings operations."""
    tx_hold: int
    tx_interval: int
    fast_start_interval: int
    management_interface: Literal["internal", "mgmt"]
    device_detection: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LldpSettingsResponse(TypedDict, total=False):
    """Response type for LldpSettings - use with .dict property for typed dict access."""
    tx_hold: int
    tx_interval: int
    fast_start_interval: int
    management_interface: Literal["internal", "mgmt"]
    device_detection: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LldpSettingsObject(FortiObject):
    """Typed FortiObject for LldpSettings with field access."""
    tx_hold: int
    tx_interval: int
    fast_start_interval: int
    management_interface: Literal["internal", "mgmt"]
    device_detection: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class LldpSettings:
    """
    
    Endpoint: switch_controller/lldp_settings
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LldpSettingsObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LldpSettingsObject: ...


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
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
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
    "LldpSettings",
    "LldpSettingsPayload",
    "LldpSettingsResponse",
    "LldpSettingsObject",
]