""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ipsec_aggregate
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

class IpsecAggregateMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    tunnel_name: str


class IpsecAggregatePayload(TypedDict, total=False):
    """Payload type for IpsecAggregate operations."""
    name: str
    member: str | list[str] | list[IpsecAggregateMemberItem]
    algorithm: Literal["L3", "L4", "round-robin", "redundant", "weighted-round-robin"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IpsecAggregateResponse(TypedDict, total=False):
    """Response type for IpsecAggregate - use with .dict property for typed dict access."""
    name: str
    member: list[IpsecAggregateMemberItem]
    algorithm: Literal["L3", "L4", "round-robin", "redundant", "weighted-round-robin"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IpsecAggregateMemberItemObject(FortiObject[IpsecAggregateMemberItem]):
    """Typed object for member table items with attribute access."""
    tunnel_name: str


class IpsecAggregateObject(FortiObject):
    """Typed FortiObject for IpsecAggregate with field access."""
    name: str
    member: FortiObjectList[IpsecAggregateMemberItemObject]
    algorithm: Literal["L3", "L4", "round-robin", "redundant", "weighted-round-robin"]


# ================================================================
# Main Endpoint Class
# ================================================================

class IpsecAggregate:
    """
    
    Endpoint: system/ipsec_aggregate
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
    ) -> IpsecAggregateObject: ...
    
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
    ) -> FortiObjectList[IpsecAggregateObject]: ...
    
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
        payload_dict: IpsecAggregatePayload | None = ...,
        name: str | None = ...,
        member: str | list[str] | list[IpsecAggregateMemberItem] | None = ...,
        algorithm: Literal["L3", "L4", "round-robin", "redundant", "weighted-round-robin"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IpsecAggregateObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IpsecAggregatePayload | None = ...,
        name: str | None = ...,
        member: str | list[str] | list[IpsecAggregateMemberItem] | None = ...,
        algorithm: Literal["L3", "L4", "round-robin", "redundant", "weighted-round-robin"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IpsecAggregateObject: ...

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
        payload_dict: IpsecAggregatePayload | None = ...,
        name: str | None = ...,
        member: str | list[str] | list[IpsecAggregateMemberItem] | None = ...,
        algorithm: Literal["L3", "L4", "round-robin", "redundant", "weighted-round-robin"] | None = ...,
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
    "IpsecAggregate",
    "IpsecAggregatePayload",
    "IpsecAggregateResponse",
    "IpsecAggregateObject",
]