""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/anqp_venue_url
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

class AnqpVenueUrlValuelistItem(TypedDict, total=False):
    """Nested item for value-list field."""
    index: int
    number: int
    value: str


class AnqpVenueUrlPayload(TypedDict, total=False):
    """Payload type for AnqpVenueUrl operations."""
    name: str
    value_list: str | list[str] | list[AnqpVenueUrlValuelistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AnqpVenueUrlResponse(TypedDict, total=False):
    """Response type for AnqpVenueUrl - use with .dict property for typed dict access."""
    name: str
    value_list: list[AnqpVenueUrlValuelistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AnqpVenueUrlValuelistItemObject(FortiObject[AnqpVenueUrlValuelistItem]):
    """Typed object for value-list table items with attribute access."""
    index: int
    number: int
    value: str


class AnqpVenueUrlObject(FortiObject):
    """Typed FortiObject for AnqpVenueUrl with field access."""
    name: str
    value_list: FortiObjectList[AnqpVenueUrlValuelistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class AnqpVenueUrl:
    """
    
    Endpoint: wireless_controller/hotspot20/anqp_venue_url
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
    ) -> AnqpVenueUrlObject: ...
    
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
    ) -> FortiObjectList[AnqpVenueUrlObject]: ...
    
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
        payload_dict: AnqpVenueUrlPayload | None = ...,
        name: str | None = ...,
        value_list: str | list[str] | list[AnqpVenueUrlValuelistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpVenueUrlObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AnqpVenueUrlPayload | None = ...,
        name: str | None = ...,
        value_list: str | list[str] | list[AnqpVenueUrlValuelistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpVenueUrlObject: ...

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
        payload_dict: AnqpVenueUrlPayload | None = ...,
        name: str | None = ...,
        value_list: str | list[str] | list[AnqpVenueUrlValuelistItem] | None = ...,
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
    "AnqpVenueUrl",
    "AnqpVenueUrlPayload",
    "AnqpVenueUrlResponse",
    "AnqpVenueUrlObject",
]