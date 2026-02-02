""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: registration/forticloud/register_device
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

class RegisterDevicePayload(TypedDict, total=False):
    """Payload type for RegisterDevice operations."""
    serial: str
    email: str
    password: str
    reseller: str
    reseller_id: int
    country: str
    is_government: bool
    agreement_accepted: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class RegisterDeviceResponse(TypedDict, total=False):
    """Response type for RegisterDevice - use with .dict property for typed dict access."""
    successful_registration_count: int
    failed_registration_count: int
    success: bool
    forticare_agreement: str


class RegisterDeviceObject(FortiObject[RegisterDeviceResponse]):
    """Typed FortiObject for RegisterDevice with field access."""
    successful_registration_count: int
    failed_registration_count: int
    success: bool
    forticare_agreement: str



# ================================================================
# Main Endpoint Class
# ================================================================

class RegisterDevice:
    """
    
    Endpoint: registration/forticloud/register_device
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
    ) -> FortiObjectList[RegisterDeviceObject]: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: RegisterDevicePayload | None = ...,
        serial: str | None = ...,
        email: str | None = ...,
        password: str | None = ...,
        reseller: str | None = ...,
        reseller_id: int | None = ...,
        country: str | None = ...,
        is_government: bool | None = ...,
        agreement_accepted: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RegisterDeviceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RegisterDevicePayload | None = ...,
        serial: str | None = ...,
        email: str | None = ...,
        password: str | None = ...,
        reseller: str | None = ...,
        reseller_id: int | None = ...,
        country: str | None = ...,
        is_government: bool | None = ...,
        agreement_accepted: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RegisterDeviceObject: ...


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
        payload_dict: RegisterDevicePayload | None = ...,
        serial: str | None = ...,
        email: str | None = ...,
        password: str | None = ...,
        reseller: str | None = ...,
        reseller_id: int | None = ...,
        country: str | None = ...,
        is_government: bool | None = ...,
        agreement_accepted: bool | None = ...,
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
    "RegisterDevice",
    "RegisterDeviceResponse",
    "RegisterDeviceObject",
]