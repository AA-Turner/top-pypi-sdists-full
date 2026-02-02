""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/fabric_time_in_sync
Category: service
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

class FabricTimeInSyncPayload(TypedDict, total=False):
    """Payload type for FabricTimeInSync operations."""
    utc: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class FabricTimeInSyncResponse(TypedDict, total=False):
    """Response type for FabricTimeInSync - use with .dict property for typed dict access."""
    synchronized: bool


class FabricTimeInSyncObject(FortiObject[FabricTimeInSyncResponse]):
    """Typed FortiObject for FabricTimeInSync with field access."""
    synchronized: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class FabricTimeInSync:
    """
    
    Endpoint: system/fabric_time_in_sync
    Category: service
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        utc: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[FabricTimeInSyncObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FabricTimeInSyncPayload | None = ...,
        utc: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FabricTimeInSyncObject: ...


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
        payload_dict: FabricTimeInSyncPayload | None = ...,
        utc: str | None = ...,
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
    "FabricTimeInSync",
    "FabricTimeInSyncResponse",
    "FabricTimeInSyncObject",
]