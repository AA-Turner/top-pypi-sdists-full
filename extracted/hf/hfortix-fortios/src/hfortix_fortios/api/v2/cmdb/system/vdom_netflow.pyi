""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vdom_netflow
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

class VdomNetflowCollectorsItem(TypedDict, total=False):
    """Nested item for collectors field."""
    id: int
    collector_ip: str
    collector_port: int
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class VdomNetflowPayload(TypedDict, total=False):
    """Payload type for VdomNetflow operations."""
    vdom_netflow: Literal["enable", "disable"]
    collectors: str | list[str] | list[VdomNetflowCollectorsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VdomNetflowResponse(TypedDict, total=False):
    """Response type for VdomNetflow - use with .dict property for typed dict access."""
    vdom_netflow: Literal["enable", "disable"]
    collectors: list[VdomNetflowCollectorsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VdomNetflowCollectorsItemObject(FortiObject[VdomNetflowCollectorsItem]):
    """Typed object for collectors table items with attribute access."""
    id: int
    collector_ip: str
    collector_port: int
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class VdomNetflowObject(FortiObject):
    """Typed FortiObject for VdomNetflow with field access."""
    vdom_netflow: Literal["enable", "disable"]
    collectors: FortiObjectList[VdomNetflowCollectorsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class VdomNetflow:
    """
    
    Endpoint: system/vdom_netflow
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomNetflowObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VdomNetflowPayload | None = ...,
        vdom_netflow: Literal["enable", "disable"] | None = ...,
        collectors: str | list[str] | list[VdomNetflowCollectorsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomNetflowObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
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
        payload_dict: VdomNetflowPayload | None = ...,
        vdom_netflow: Literal["enable", "disable"] | None = ...,
        collectors: str | list[str] | list[VdomNetflowCollectorsItem] | None = ...,
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
    "VdomNetflow",
    "VdomNetflowPayload",
    "VdomNetflowResponse",
    "VdomNetflowObject",
]