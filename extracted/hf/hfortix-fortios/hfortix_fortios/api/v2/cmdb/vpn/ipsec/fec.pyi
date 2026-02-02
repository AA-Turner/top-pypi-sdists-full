""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/ipsec/fec
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

class FecMappingsItem(TypedDict, total=False):
    """Nested item for mappings field."""
    seqno: int
    base: int
    redundant: int
    packet_loss_threshold: int
    latency_threshold: int
    bandwidth_up_threshold: int
    bandwidth_down_threshold: int
    bandwidth_bi_threshold: int


class FecPayload(TypedDict, total=False):
    """Payload type for Fec operations."""
    name: str
    mappings: str | list[str] | list[FecMappingsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FecResponse(TypedDict, total=False):
    """Response type for Fec - use with .dict property for typed dict access."""
    name: str
    mappings: list[FecMappingsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FecMappingsItemObject(FortiObject[FecMappingsItem]):
    """Typed object for mappings table items with attribute access."""
    seqno: int
    base: int
    redundant: int
    packet_loss_threshold: int
    latency_threshold: int
    bandwidth_up_threshold: int
    bandwidth_down_threshold: int
    bandwidth_bi_threshold: int


class FecObject(FortiObject):
    """Typed FortiObject for Fec with field access."""
    name: str
    mappings: FortiObjectList[FecMappingsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Fec:
    """
    
    Endpoint: vpn/ipsec/fec
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
    ) -> FecObject: ...
    
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
    ) -> FortiObjectList[FecObject]: ...
    
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
        payload_dict: FecPayload | None = ...,
        name: str | None = ...,
        mappings: str | list[str] | list[FecMappingsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FecObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FecPayload | None = ...,
        name: str | None = ...,
        mappings: str | list[str] | list[FecMappingsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FecObject: ...

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
        payload_dict: FecPayload | None = ...,
        name: str | None = ...,
        mappings: str | list[str] | list[FecMappingsItem] | None = ...,
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
    "Fec",
    "FecPayload",
    "FecResponse",
    "FecObject",
]