""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/stp_settings
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

class StpSettingsPayload(TypedDict, total=False):
    """Payload type for StpSettings operations."""
    name: str
    revision: int
    hello_time: int
    forward_time: int
    max_age: int
    max_hops: int
    pending_timer: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StpSettingsResponse(TypedDict, total=False):
    """Response type for StpSettings - use with .dict property for typed dict access."""
    name: str
    revision: int
    hello_time: int
    forward_time: int
    max_age: int
    max_hops: int
    pending_timer: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StpSettingsObject(FortiObject):
    """Typed FortiObject for StpSettings with field access."""
    name: str
    hello_time: int
    forward_time: int
    max_age: int
    max_hops: int
    pending_timer: int


# ================================================================
# Main Endpoint Class
# ================================================================

class StpSettings:
    """
    
    Endpoint: switch_controller/stp_settings
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
    ) -> StpSettingsObject: ...
    
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
        payload_dict: StpSettingsPayload | None = ...,
        name: str | None = ...,
        revision: int | None = ...,
        hello_time: int | None = ...,
        forward_time: int | None = ...,
        max_age: int | None = ...,
        max_hops: int | None = ...,
        pending_timer: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StpSettingsObject: ...


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
        payload_dict: StpSettingsPayload | None = ...,
        name: str | None = ...,
        revision: int | None = ...,
        hello_time: int | None = ...,
        forward_time: int | None = ...,
        max_age: int | None = ...,
        max_hops: int | None = ...,
        pending_timer: int | None = ...,
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
    "StpSettings",
    "StpSettingsPayload",
    "StpSettingsResponse",
    "StpSettingsObject",
]