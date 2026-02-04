""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/lw_profile
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

class LwProfilePayload(TypedDict, total=False):
    """Payload type for LwProfile operations."""
    name: str
    comment: str
    lw_protocol: Literal["basics-station", "packet-forwarder"]
    cups_server: str
    cups_server_port: int
    cups_api_key: str
    tc_server: str
    tc_server_port: int
    tc_api_key: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LwProfileResponse(TypedDict, total=False):
    """Response type for LwProfile - use with .dict property for typed dict access."""
    name: str
    comment: str
    lw_protocol: Literal["basics-station", "packet-forwarder"]
    cups_server: str
    cups_server_port: int
    cups_api_key: str
    tc_server: str
    tc_server_port: int
    tc_api_key: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LwProfileObject(FortiObject):
    """Typed FortiObject for LwProfile with field access."""
    name: str
    comment: str
    lw_protocol: Literal["basics-station", "packet-forwarder"]
    cups_server: str
    cups_server_port: int
    cups_api_key: str
    tc_server: str
    tc_server_port: int
    tc_api_key: str


# ================================================================
# Main Endpoint Class
# ================================================================

class LwProfile:
    """
    
    Endpoint: wireless_controller/lw_profile
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
    ) -> LwProfileObject: ...
    
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
    ) -> FortiObjectList[LwProfileObject]: ...
    
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
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LwProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LwProfileObject: ...

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
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
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
    "LwProfile",
    "LwProfilePayload",
    "LwProfileResponse",
    "LwProfileObject",
]