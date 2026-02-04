""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/usb_log
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

class UsbLogResponse(TypedDict, total=False):
    """Response type for UsbLog - use with .dict property for typed dict access."""
    usb_attached: bool
    max_usb_filename_length: str
    auto_install_image: bool
    auto_install_conf: bool
    disk_size: str
    avail_space: str
    model: str
    progress: str
    same_vdom: bool
    is_copying: bool
    log_size: str
    log_file_no: str


class UsbLogObject(FortiObject[UsbLogResponse]):
    """Typed FortiObject for UsbLog with field access."""
    usb_attached: bool
    max_usb_filename_length: str
    auto_install_image: bool
    auto_install_conf: bool
    disk_size: str
    avail_space: str
    model: str
    progress: str
    same_vdom: bool
    is_copying: bool
    log_size: str
    log_file_no: str



# ================================================================
# Main Endpoint Class
# ================================================================

class UsbLog:
    """
    
    Endpoint: system/usb_log
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
    ) -> FortiObjectList[UsbLogObject]: ...
    


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
    "UsbLog",
    "UsbLogResponse",
    "UsbLogObject",
]