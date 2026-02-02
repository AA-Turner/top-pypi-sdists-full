""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/affinity_interrupt
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

class AffinityInterruptPayload(TypedDict, total=False):
    """Payload type for AffinityInterrupt operations."""
    id: int
    interrupt: str
    affinity_cpumask: str
    default_affinity_cpumask: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AffinityInterruptResponse(TypedDict, total=False):
    """Response type for AffinityInterrupt - use with .dict property for typed dict access."""
    id: int
    interrupt: str
    affinity_cpumask: str
    default_affinity_cpumask: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AffinityInterruptObject(FortiObject):
    """Typed FortiObject for AffinityInterrupt with field access."""
    id: int
    interrupt: str
    affinity_cpumask: str
    default_affinity_cpumask: str


# ================================================================
# Main Endpoint Class
# ================================================================

class AffinityInterrupt:
    """
    
    Endpoint: system/affinity_interrupt
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> AffinityInterruptObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[AffinityInterruptObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: AffinityInterruptPayload | None = ...,
        id: int | None = ...,
        interrupt: str | None = ...,
        affinity_cpumask: str | None = ...,
        default_affinity_cpumask: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AffinityInterruptObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AffinityInterruptPayload | None = ...,
        id: int | None = ...,
        interrupt: str | None = ...,
        affinity_cpumask: str | None = ...,
        default_affinity_cpumask: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AffinityInterruptObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AffinityInterruptPayload | None = ...,
        id: int | None = ...,
        interrupt: str | None = ...,
        affinity_cpumask: str | None = ...,
        default_affinity_cpumask: str | None = ...,
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
    "AffinityInterrupt",
    "AffinityInterruptPayload",
    "AffinityInterruptResponse",
    "AffinityInterruptObject",
]