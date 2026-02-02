""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ptp
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

class PtpServerinterfaceItem(TypedDict, total=False):
    """Nested item for server-interface field."""
    id: int
    server_interface_name: str
    delay_mechanism: Literal["E2E", "P2P"]


class PtpPayload(TypedDict, total=False):
    """Payload type for Ptp operations."""
    status: Literal["enable", "disable"]
    mode: Literal["multicast", "hybrid"]
    delay_mechanism: Literal["E2E", "P2P"]
    request_interval: int
    interface: str
    server_mode: Literal["enable", "disable"]
    server_interface: str | list[str] | list[PtpServerinterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PtpResponse(TypedDict, total=False):
    """Response type for Ptp - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    mode: Literal["multicast", "hybrid"]
    delay_mechanism: Literal["E2E", "P2P"]
    request_interval: int
    interface: str
    server_mode: Literal["enable", "disable"]
    server_interface: list[PtpServerinterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PtpServerinterfaceItemObject(FortiObject[PtpServerinterfaceItem]):
    """Typed object for server-interface table items with attribute access."""
    id: int
    server_interface_name: str
    delay_mechanism: Literal["E2E", "P2P"]


class PtpObject(FortiObject):
    """Typed FortiObject for Ptp with field access."""
    status: Literal["enable", "disable"]
    mode: Literal["multicast", "hybrid"]
    delay_mechanism: Literal["E2E", "P2P"]
    request_interval: int
    interface: str
    server_mode: Literal["enable", "disable"]
    server_interface: FortiObjectList[PtpServerinterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ptp:
    """
    
    Endpoint: system/ptp
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
    ) -> PtpObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[PtpServerinterfaceItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PtpObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[PtpServerinterfaceItem] | None = ...,
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
    "Ptp",
    "PtpPayload",
    "PtpResponse",
    "PtpObject",
]