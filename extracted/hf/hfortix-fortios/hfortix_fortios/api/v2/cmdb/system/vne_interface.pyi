""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vne_interface
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class VneInterfacePayload(TypedDict, total=False):
    """Payload type for VneInterface operations."""
    name: str
    interface: str
    ssl_certificate: str
    bmr_hostname: str
    auto_asic_offload: Literal["enable", "disable"]
    ipv4_address: str
    br: str
    update_url: str
    mode: Literal["map-e", "fixed-ip", "ds-lite"]
    http_username: str
    http_password: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VneInterfaceResponse(TypedDict, total=False):
    """Response type for VneInterface - use with .dict property for typed dict access."""
    name: str
    interface: str
    ssl_certificate: str
    bmr_hostname: str
    auto_asic_offload: Literal["enable", "disable"]
    ipv4_address: str
    br: str
    update_url: str
    mode: Literal["map-e", "fixed-ip", "ds-lite"]
    http_username: str
    http_password: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VneInterfaceObject(FortiObject):
    """Typed FortiObject for VneInterface with field access."""
    name: str
    interface: str
    ssl_certificate: str
    bmr_hostname: str
    auto_asic_offload: Literal["enable", "disable"]
    ipv4_address: str
    br: str
    update_url: str
    mode: Literal["map-e", "fixed-ip", "ds-lite"]
    http_username: str
    http_password: str


# ================================================================
# Main Endpoint Class
# ================================================================

class VneInterface:
    """
    
    Endpoint: system/vne_interface
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
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
    ) -> VneInterfaceObject: ...
    
    @overload
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
    ) -> FortiObjectList[VneInterfaceObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: VneInterfacePayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ssl_certificate: str | None = ...,
        bmr_hostname: str | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        ipv4_address: str | None = ...,
        br: str | None = ...,
        update_url: str | None = ...,
        mode: Literal["map-e", "fixed-ip", "ds-lite"] | None = ...,
        http_username: str | None = ...,
        http_password: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VneInterfaceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VneInterfacePayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ssl_certificate: str | None = ...,
        bmr_hostname: str | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        ipv4_address: str | None = ...,
        br: str | None = ...,
        update_url: str | None = ...,
        mode: Literal["map-e", "fixed-ip", "ds-lite"] | None = ...,
        http_username: str | None = ...,
        http_password: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VneInterfaceObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
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
        payload_dict: VneInterfacePayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ssl_certificate: str | None = ...,
        bmr_hostname: str | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        ipv4_address: str | None = ...,
        br: str | None = ...,
        update_url: str | None = ...,
        mode: Literal["map-e", "fixed-ip", "ds-lite"] | None = ...,
        http_username: str | None = ...,
        http_password: str | None = ...,
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
    "VneInterface",
    "VneInterfacePayload",
    "VneInterfaceResponse",
    "VneInterfaceObject",
]