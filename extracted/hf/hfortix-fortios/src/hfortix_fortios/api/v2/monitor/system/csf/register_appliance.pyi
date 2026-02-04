""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/csf/register_appliance
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

class RegisterAppliancePayload(TypedDict, total=False):
    """Payload type for RegisterAppliance operations."""
    type: str
    mgmt_ip: str
    mgmt_port: int
    mgmt_url_parameters: list[str]
    serial: str
    hostname: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RegisterApplianceResponse(TypedDict, total=False):
    """Response type for RegisterAppliance - use with .dict property for typed dict access."""
    type: str
    mgmt_ip: str
    mgmt_port: int
    mgmt_url_parameters: list[str]
    serial: str
    hostname: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RegisterApplianceObject(FortiObject):
    """Typed FortiObject for RegisterAppliance with field access."""
    type: str
    mgmt_ip: str
    mgmt_port: int
    mgmt_url_parameters: list[str]
    hostname: str


# ================================================================
# Main Endpoint Class
# ================================================================

class RegisterAppliance:
    """
    
    Endpoint: system/csf/register_appliance
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
    ) -> RegisterApplianceObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: RegisterAppliancePayload | None = ...,
        type: str | None = ...,
        mgmt_ip: str | None = ...,
        mgmt_port: int | None = ...,
        mgmt_url_parameters: list[str] | None = ...,
        serial: str | None = ...,
        hostname: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RegisterApplianceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RegisterAppliancePayload | None = ...,
        type: str | None = ...,
        mgmt_ip: str | None = ...,
        mgmt_port: int | None = ...,
        mgmt_url_parameters: list[str] | None = ...,
        serial: str | None = ...,
        hostname: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RegisterApplianceObject: ...




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
        payload_dict: RegisterAppliancePayload | None = ...,
        type: str | None = ...,
        mgmt_ip: str | None = ...,
        mgmt_port: int | None = ...,
        mgmt_url_parameters: list[str] | None = ...,
        serial: str | None = ...,
        hostname: str | None = ...,
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
    "RegisterAppliance",
    "RegisterAppliancePayload",
    "RegisterApplianceResponse",
    "RegisterApplianceObject",
]