""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/fsso_polling
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

class FssoPollingPayload(TypedDict, total=False):
    """Payload type for FssoPolling operations."""
    status: Literal["enable", "disable"]
    listening_port: int
    authentication: Literal["enable", "disable"]
    auth_password: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FssoPollingResponse(TypedDict, total=False):
    """Response type for FssoPolling - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    listening_port: int
    authentication: Literal["enable", "disable"]
    auth_password: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FssoPollingObject(FortiObject):
    """Typed FortiObject for FssoPolling with field access."""
    status: Literal["enable", "disable"]
    listening_port: int
    authentication: Literal["enable", "disable"]
    auth_password: str


# ================================================================
# Main Endpoint Class
# ================================================================

class FssoPolling:
    """
    
    Endpoint: system/fsso_polling
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FssoPollingObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FssoPollingPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        listening_port: int | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        auth_password: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FssoPollingObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FssoPollingPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        listening_port: int | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        auth_password: str | None = ...,
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
    "FssoPolling",
    "FssoPollingPayload",
    "FssoPollingResponse",
    "FssoPollingObject",
]