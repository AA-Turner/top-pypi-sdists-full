""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vm_information
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
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class VmInformationResponse(TypedDict, total=False):
    """Response type for VmInformation - use with .dict property for typed dict access."""
    cpu_used: int
    cpu_max: int
    mem_used: int
    mem_max: int
    is_payg: bool
    nva_payg_billing_status: str
    type: str
    valid: bool
    status: str
    license_model: int
    license_platform_name: str
    license_source: str
    expires: int
    validation_overdue_since: int
    closed_network: bool
    is_autoscale_master: bool
    autoscale_set_size: int
    autoscale_enabled: bool
    autoscale_peers: list[str]


class VmInformationObject(FortiObject[VmInformationResponse]):
    """Typed FortiObject for VmInformation with field access."""
    cpu_used: int
    cpu_max: int
    mem_used: int
    mem_max: int
    is_payg: bool
    nva_payg_billing_status: str
    type: str
    valid: bool
    status: str
    license_model: int
    license_platform_name: str
    license_source: str
    expires: int
    validation_overdue_since: int
    closed_network: bool
    is_autoscale_master: bool
    autoscale_set_size: int
    autoscale_enabled: bool
    autoscale_peers: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class VmInformation:
    """
    
    Endpoint: system/vm_information
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
    ) -> FortiObjectList[VmInformationObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...


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
        payload_dict: dict[str, Any] | None = ...,
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
    "VmInformation",
    "VmInformationResponse",
    "VmInformationObject",
]