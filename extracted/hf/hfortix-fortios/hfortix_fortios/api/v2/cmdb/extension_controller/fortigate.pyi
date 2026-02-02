""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: extension_controller/fortigate
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

class FortigatePayload(TypedDict, total=False):
    """Payload type for Fortigate operations."""
    name: str
    id: str
    authorized: Literal["discovered", "disable", "enable"]
    hostname: str
    description: str
    vdom: int
    device_id: int
    profile: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FortigateResponse(TypedDict, total=False):
    """Response type for Fortigate - use with .dict property for typed dict access."""
    name: str
    id: str
    authorized: Literal["discovered", "disable", "enable"]
    hostname: str
    description: str
    vdom: int
    device_id: int
    profile: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FortigateObject(FortiObject):
    """Typed FortiObject for Fortigate with field access."""
    name: str
    id: str
    authorized: Literal["discovered", "disable", "enable"]
    hostname: str
    description: str
    device_id: int
    profile: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Fortigate:
    """
    
    Endpoint: extension_controller/fortigate
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
    ) -> FortigateObject: ...
    
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
    ) -> FortiObjectList[FortigateObject]: ...
    
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
        payload_dict: FortigatePayload | None = ...,
        name: str | None = ...,
        id: str | None = ...,
        authorized: Literal["discovered", "disable", "enable"] | None = ...,
        hostname: str | None = ...,
        description: str | None = ...,
        device_id: int | None = ...,
        profile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortigateObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FortigatePayload | None = ...,
        name: str | None = ...,
        id: str | None = ...,
        authorized: Literal["discovered", "disable", "enable"] | None = ...,
        hostname: str | None = ...,
        description: str | None = ...,
        device_id: int | None = ...,
        profile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortigateObject: ...

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
        payload_dict: FortigatePayload | None = ...,
        name: str | None = ...,
        id: str | None = ...,
        authorized: Literal["discovered", "disable", "enable"] | None = ...,
        hostname: str | None = ...,
        description: str | None = ...,
        device_id: int | None = ...,
        profile: str | None = ...,
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
    "Fortigate",
    "FortigatePayload",
    "FortigateResponse",
    "FortigateObject",
]