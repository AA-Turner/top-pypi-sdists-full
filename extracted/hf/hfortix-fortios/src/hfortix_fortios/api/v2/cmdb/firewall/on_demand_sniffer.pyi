""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/on_demand_sniffer
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

class OnDemandSnifferHostsItem(TypedDict, total=False):
    """Nested item for hosts field."""
    host: str


class OnDemandSnifferPortsItem(TypedDict, total=False):
    """Nested item for ports field."""
    port: int


class OnDemandSnifferProtocolsItem(TypedDict, total=False):
    """Nested item for protocols field."""
    protocol: int


class OnDemandSnifferPayload(TypedDict, total=False):
    """Payload type for OnDemandSniffer operations."""
    name: str
    interface: str
    max_packet_count: int
    hosts: str | list[str] | list[OnDemandSnifferHostsItem]
    ports: str | list[str] | list[OnDemandSnifferPortsItem]
    protocols: str | list[str] | list[OnDemandSnifferProtocolsItem]
    non_ip_packet: Literal["enable", "disable"]
    advanced_filter: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class OnDemandSnifferResponse(TypedDict, total=False):
    """Response type for OnDemandSniffer - use with .dict property for typed dict access."""
    name: str
    interface: str
    max_packet_count: int
    hosts: list[OnDemandSnifferHostsItem]
    ports: list[OnDemandSnifferPortsItem]
    protocols: list[OnDemandSnifferProtocolsItem]
    non_ip_packet: Literal["enable", "disable"]
    advanced_filter: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class OnDemandSnifferHostsItemObject(FortiObject[OnDemandSnifferHostsItem]):
    """Typed object for hosts table items with attribute access."""
    host: str


class OnDemandSnifferPortsItemObject(FortiObject[OnDemandSnifferPortsItem]):
    """Typed object for ports table items with attribute access."""
    port: int


class OnDemandSnifferProtocolsItemObject(FortiObject[OnDemandSnifferProtocolsItem]):
    """Typed object for protocols table items with attribute access."""
    protocol: int


class OnDemandSnifferObject(FortiObject):
    """Typed FortiObject for OnDemandSniffer with field access."""
    name: str
    interface: str
    max_packet_count: int
    hosts: FortiObjectList[OnDemandSnifferHostsItemObject]
    ports: FortiObjectList[OnDemandSnifferPortsItemObject]
    protocols: FortiObjectList[OnDemandSnifferProtocolsItemObject]
    non_ip_packet: Literal["enable", "disable"]
    advanced_filter: str


# ================================================================
# Main Endpoint Class
# ================================================================

class OnDemandSniffer:
    """
    
    Endpoint: firewall/on_demand_sniffer
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
    ) -> OnDemandSnifferObject: ...
    
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
    ) -> FortiObjectList[OnDemandSnifferObject]: ...
    
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
        payload_dict: OnDemandSnifferPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        max_packet_count: int | None = ...,
        hosts: str | list[str] | list[OnDemandSnifferHostsItem] | None = ...,
        ports: str | list[str] | list[OnDemandSnifferPortsItem] | None = ...,
        protocols: str | list[str] | list[OnDemandSnifferProtocolsItem] | None = ...,
        non_ip_packet: Literal["enable", "disable"] | None = ...,
        advanced_filter: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> OnDemandSnifferObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: OnDemandSnifferPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        max_packet_count: int | None = ...,
        hosts: str | list[str] | list[OnDemandSnifferHostsItem] | None = ...,
        ports: str | list[str] | list[OnDemandSnifferPortsItem] | None = ...,
        protocols: str | list[str] | list[OnDemandSnifferProtocolsItem] | None = ...,
        non_ip_packet: Literal["enable", "disable"] | None = ...,
        advanced_filter: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> OnDemandSnifferObject: ...

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
        payload_dict: OnDemandSnifferPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        max_packet_count: int | None = ...,
        hosts: str | list[str] | list[OnDemandSnifferHostsItem] | None = ...,
        ports: str | list[str] | list[OnDemandSnifferPortsItem] | None = ...,
        protocols: str | list[str] | list[OnDemandSnifferProtocolsItem] | None = ...,
        non_ip_packet: Literal["enable", "disable"] | None = ...,
        advanced_filter: str | None = ...,
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
    "OnDemandSniffer",
    "OnDemandSnifferPayload",
    "OnDemandSnifferResponse",
    "OnDemandSnifferObject",
]