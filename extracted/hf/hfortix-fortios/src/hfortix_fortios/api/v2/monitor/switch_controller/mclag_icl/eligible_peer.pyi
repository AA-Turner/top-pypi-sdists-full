""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/mclag_icl/eligible_peer
Category: monitor
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

class EligiblePeerPayload(TypedDict, total=False):
    """Payload type for EligiblePeer operations."""
    fortilink: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class EligiblePeerResponse(TypedDict, total=False):
    """Response type for EligiblePeer - use with .dict property for typed dict access."""
    status: str
    candidate1: str
    candidate2: str


class EligiblePeerObject(FortiObject[EligiblePeerResponse]):
    """Typed FortiObject for EligiblePeer with field access."""
    status: str
    candidate1: str
    candidate2: str



# ================================================================
# Main Endpoint Class
# ================================================================

class EligiblePeer:
    """
    
    Endpoint: switch_controller/mclag_icl/eligible_peer
    Category: monitor
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
        fortilink: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[EligiblePeerObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: EligiblePeerPayload | None = ...,
        fortilink: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> EligiblePeerObject: ...




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
        payload_dict: EligiblePeerPayload | None = ...,
        fortilink: str | None = ...,
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
    "EligiblePeer",
    "EligiblePeerResponse",
    "EligiblePeerObject",
]