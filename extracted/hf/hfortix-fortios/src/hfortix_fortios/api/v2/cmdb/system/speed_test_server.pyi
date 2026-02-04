""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/speed_test_server
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

class SpeedTestServerHostItem(TypedDict, total=False):
    """Nested item for host field."""
    id: int
    ip: str
    port: int
    user: str
    password: str
    longitude: str
    latitude: str
    distance: int


class SpeedTestServerPayload(TypedDict, total=False):
    """Payload type for SpeedTestServer operations."""
    name: str
    timestamp: int
    host: str | list[str] | list[SpeedTestServerHostItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SpeedTestServerResponse(TypedDict, total=False):
    """Response type for SpeedTestServer - use with .dict property for typed dict access."""
    name: str
    timestamp: int
    host: list[SpeedTestServerHostItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SpeedTestServerHostItemObject(FortiObject[SpeedTestServerHostItem]):
    """Typed object for host table items with attribute access."""
    id: int
    ip: str
    port: int
    user: str
    password: str
    longitude: str
    latitude: str
    distance: int


class SpeedTestServerObject(FortiObject):
    """Typed FortiObject for SpeedTestServer with field access."""
    name: str
    timestamp: int
    host: FortiObjectList[SpeedTestServerHostItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class SpeedTestServer:
    """
    
    Endpoint: system/speed_test_server
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
    ) -> SpeedTestServerObject: ...
    
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
    ) -> FortiObjectList[SpeedTestServerObject]: ...
    
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
        payload_dict: SpeedTestServerPayload | None = ...,
        name: str | None = ...,
        timestamp: int | None = ...,
        host: str | list[str] | list[SpeedTestServerHostItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SpeedTestServerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SpeedTestServerPayload | None = ...,
        name: str | None = ...,
        timestamp: int | None = ...,
        host: str | list[str] | list[SpeedTestServerHostItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SpeedTestServerObject: ...

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
        payload_dict: SpeedTestServerPayload | None = ...,
        name: str | None = ...,
        timestamp: int | None = ...,
        host: str | list[str] | list[SpeedTestServerHostItem] | None = ...,
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
    "SpeedTestServer",
    "SpeedTestServerPayload",
    "SpeedTestServerResponse",
    "SpeedTestServerObject",
]