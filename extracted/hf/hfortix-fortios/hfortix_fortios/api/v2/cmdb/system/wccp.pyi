""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/wccp
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

class WccpPayload(TypedDict, total=False):
    """Payload type for Wccp operations."""
    service_id: str
    router_id: str
    cache_id: str
    group_address: str
    server_list: str | list[str]
    router_list: str | list[str]
    ports_defined: Literal["source", "destination"]
    server_type: Literal["forward", "proxy"]
    ports: str | list[str]
    authentication: Literal["enable", "disable"]
    password: str
    forward_method: Literal["GRE", "L2", "any"]
    cache_engine_method: Literal["GRE", "L2"]
    service_type: Literal["auto", "standard", "dynamic"]
    primary_hash: str | list[str]
    priority: int
    protocol: int
    assignment_weight: int
    assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"]
    return_method: Literal["GRE", "L2", "any"]
    assignment_method: Literal["HASH", "MASK", "any"]
    assignment_srcaddr_mask: str
    assignment_dstaddr_mask: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class WccpResponse(TypedDict, total=False):
    """Response type for Wccp - use with .dict property for typed dict access."""
    service_id: str
    router_id: str
    cache_id: str
    group_address: str
    server_list: str | list[str]
    router_list: str | list[str]
    ports_defined: Literal["source", "destination"]
    server_type: Literal["forward", "proxy"]
    ports: str | list[str]
    authentication: Literal["enable", "disable"]
    password: str
    forward_method: Literal["GRE", "L2", "any"]
    cache_engine_method: Literal["GRE", "L2"]
    service_type: Literal["auto", "standard", "dynamic"]
    primary_hash: str
    priority: int
    protocol: int
    assignment_weight: int
    assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"]
    return_method: Literal["GRE", "L2", "any"]
    assignment_method: Literal["HASH", "MASK", "any"]
    assignment_srcaddr_mask: str
    assignment_dstaddr_mask: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class WccpObject(FortiObject):
    """Typed FortiObject for Wccp with field access."""
    service_id: str
    router_id: str
    cache_id: str
    group_address: str
    server_list: str | list[str]
    router_list: str | list[str]
    ports_defined: Literal["source", "destination"]
    server_type: Literal["forward", "proxy"]
    ports: str | list[str]
    authentication: Literal["enable", "disable"]
    password: str
    forward_method: Literal["GRE", "L2", "any"]
    cache_engine_method: Literal["GRE", "L2"]
    service_type: Literal["auto", "standard", "dynamic"]
    primary_hash: str
    priority: int
    protocol: int
    assignment_weight: int
    assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"]
    return_method: Literal["GRE", "L2", "any"]
    assignment_method: Literal["HASH", "MASK", "any"]
    assignment_srcaddr_mask: str
    assignment_dstaddr_mask: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Wccp:
    """
    
    Endpoint: system/wccp
    Category: cmdb
    MKey: service-id
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
        service_id: str,
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
    ) -> WccpObject: ...
    
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
    ) -> FortiObjectList[WccpObject]: ...
    
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
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: str | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WccpObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: str | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WccpObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        service_id: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
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
    "Wccp",
    "WccpPayload",
    "WccpResponse",
    "WccpObject",
]