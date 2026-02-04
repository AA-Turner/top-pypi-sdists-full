""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/ap_status
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

class ApStatusPayload(TypedDict, total=False):
    """Payload type for ApStatus operations."""
    id: int
    bssid: str
    ssid: str
    status: Literal["rogue", "accepted", "suppressed"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ApStatusResponse(TypedDict, total=False):
    """Response type for ApStatus - use with .dict property for typed dict access."""
    id: int
    bssid: str
    ssid: str
    status: Literal["rogue", "accepted", "suppressed"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ApStatusObject(FortiObject):
    """Typed FortiObject for ApStatus with field access."""
    id: int
    bssid: str
    ssid: str
    status: Literal["rogue", "accepted", "suppressed"]


# ================================================================
# Main Endpoint Class
# ================================================================

class ApStatus:
    """
    
    Endpoint: wireless_controller/ap_status
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ApStatusObject: ...
    
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
    ) -> FortiObjectList[ApStatusObject]: ...
    
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
        payload_dict: ApStatusPayload | None = ...,
        id: int | None = ...,
        bssid: str | None = ...,
        ssid: str | None = ...,
        status: Literal["rogue", "accepted", "suppressed"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ApStatusObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ApStatusPayload | None = ...,
        id: int | None = ...,
        bssid: str | None = ...,
        ssid: str | None = ...,
        status: Literal["rogue", "accepted", "suppressed"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ApStatusObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ApStatusPayload | None = ...,
        id: int | None = ...,
        bssid: str | None = ...,
        ssid: str | None = ...,
        status: Literal["rogue", "accepted", "suppressed"] | None = ...,
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
    "ApStatus",
    "ApStatusPayload",
    "ApStatusResponse",
    "ApStatusObject",
]