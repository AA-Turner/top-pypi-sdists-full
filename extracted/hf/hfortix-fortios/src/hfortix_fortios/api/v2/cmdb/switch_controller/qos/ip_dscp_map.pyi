""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/qos/ip_dscp_map
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

class IpDscpMapMapItem(TypedDict, total=False):
    """Nested item for map field."""
    name: str
    cos_queue: int
    diffserv: Literal["CS0", "CS1", "AF11", "AF12", "AF13", "CS2", "AF21", "AF22", "AF23", "CS3", "AF31", "AF32", "AF33", "CS4", "AF41", "AF42", "AF43", "CS5", "EF", "CS6", "CS7"]
    ip_precedence: Literal["network-control", "internetwork-control", "critic-ecp", "flashoverride", "flash", "immediate", "priority", "routine"]
    value: str


class IpDscpMapPayload(TypedDict, total=False):
    """Payload type for IpDscpMap operations."""
    name: str
    description: str
    map: str | list[str] | list[IpDscpMapMapItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IpDscpMapResponse(TypedDict, total=False):
    """Response type for IpDscpMap - use with .dict property for typed dict access."""
    name: str
    description: str
    map: list[IpDscpMapMapItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IpDscpMapMapItemObject(FortiObject[IpDscpMapMapItem]):
    """Typed object for map table items with attribute access."""
    name: str
    cos_queue: int
    diffserv: Literal["CS0", "CS1", "AF11", "AF12", "AF13", "CS2", "AF21", "AF22", "AF23", "CS3", "AF31", "AF32", "AF33", "CS4", "AF41", "AF42", "AF43", "CS5", "EF", "CS6", "CS7"]
    ip_precedence: Literal["network-control", "internetwork-control", "critic-ecp", "flashoverride", "flash", "immediate", "priority", "routine"]
    value: str


class IpDscpMapObject(FortiObject):
    """Typed FortiObject for IpDscpMap with field access."""
    name: str
    description: str
    map: FortiObjectList[IpDscpMapMapItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class IpDscpMap:
    """
    
    Endpoint: switch_controller/qos/ip_dscp_map
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
    ) -> IpDscpMapObject: ...
    
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
    ) -> FortiObjectList[IpDscpMapObject]: ...
    
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
        payload_dict: IpDscpMapPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        map: str | list[str] | list[IpDscpMapMapItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IpDscpMapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IpDscpMapPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        map: str | list[str] | list[IpDscpMapMapItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IpDscpMapObject: ...

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
        payload_dict: IpDscpMapPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        map: str | list[str] | list[IpDscpMapMapItem] | None = ...,
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
    "IpDscpMap",
    "IpDscpMapPayload",
    "IpDscpMapResponse",
    "IpDscpMapObject",
]