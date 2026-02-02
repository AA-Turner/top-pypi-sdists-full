""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/anqp_ip_address_type
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

class AnqpIpAddressTypePayload(TypedDict, total=False):
    """Payload type for AnqpIpAddressType operations."""
    name: str
    ipv6_address_type: Literal["not-available", "available", "not-known"]
    ipv4_address_type: Literal["not-available", "public", "port-restricted", "single-NATed-private", "double-NATed-private", "port-restricted-and-single-NATed", "port-restricted-and-double-NATed", "not-known"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AnqpIpAddressTypeResponse(TypedDict, total=False):
    """Response type for AnqpIpAddressType - use with .dict property for typed dict access."""
    name: str
    ipv6_address_type: Literal["not-available", "available", "not-known"]
    ipv4_address_type: Literal["not-available", "public", "port-restricted", "single-NATed-private", "double-NATed-private", "port-restricted-and-single-NATed", "port-restricted-and-double-NATed", "not-known"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AnqpIpAddressTypeObject(FortiObject):
    """Typed FortiObject for AnqpIpAddressType with field access."""
    name: str
    ipv6_address_type: Literal["not-available", "available", "not-known"]
    ipv4_address_type: Literal["not-available", "public", "port-restricted", "single-NATed-private", "double-NATed-private", "port-restricted-and-single-NATed", "port-restricted-and-double-NATed", "not-known"]


# ================================================================
# Main Endpoint Class
# ================================================================

class AnqpIpAddressType:
    """
    
    Endpoint: wireless_controller/hotspot20/anqp_ip_address_type
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
    ) -> AnqpIpAddressTypeObject: ...
    
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
    ) -> FortiObjectList[AnqpIpAddressTypeObject]: ...
    
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
        payload_dict: AnqpIpAddressTypePayload | None = ...,
        name: str | None = ...,
        ipv6_address_type: Literal["not-available", "available", "not-known"] | None = ...,
        ipv4_address_type: Literal["not-available", "public", "port-restricted", "single-NATed-private", "double-NATed-private", "port-restricted-and-single-NATed", "port-restricted-and-double-NATed", "not-known"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpIpAddressTypeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AnqpIpAddressTypePayload | None = ...,
        name: str | None = ...,
        ipv6_address_type: Literal["not-available", "available", "not-known"] | None = ...,
        ipv4_address_type: Literal["not-available", "public", "port-restricted", "single-NATed-private", "double-NATed-private", "port-restricted-and-single-NATed", "port-restricted-and-double-NATed", "not-known"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpIpAddressTypeObject: ...

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
        payload_dict: AnqpIpAddressTypePayload | None = ...,
        name: str | None = ...,
        ipv6_address_type: Literal["not-available", "available", "not-known"] | None = ...,
        ipv4_address_type: Literal["not-available", "public", "port-restricted", "single-NATed-private", "double-NATed-private", "port-restricted-and-single-NATed", "port-restricted-and-double-NATed", "not-known"] | None = ...,
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
    "AnqpIpAddressType",
    "AnqpIpAddressTypePayload",
    "AnqpIpAddressTypeResponse",
    "AnqpIpAddressTypeObject",
]