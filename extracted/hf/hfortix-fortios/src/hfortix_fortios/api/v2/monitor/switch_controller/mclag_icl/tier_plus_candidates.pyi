""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/mclag_icl/tier_plus_candidates
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

class TierPlusCandidatesPayload(TypedDict, total=False):
    """Payload type for TierPlusCandidates operations."""
    fortilink: str
    parent_peer1: str
    parent_peer2: str
    is_tier2: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class TierPlusCandidatesResponse(TypedDict, total=False):
    """Response type for TierPlusCandidates - use with .dict property for typed dict access."""
    status: str
    peer1_candidate: str
    peer2_candidate: str


class TierPlusCandidatesObject(FortiObject[TierPlusCandidatesResponse]):
    """Typed FortiObject for TierPlusCandidates with field access."""
    status: str
    peer1_candidate: str
    peer2_candidate: str



# ================================================================
# Main Endpoint Class
# ================================================================

class TierPlusCandidates:
    """
    
    Endpoint: switch_controller/mclag_icl/tier_plus_candidates
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
        parent_peer1: str,
        parent_peer2: str,
        is_tier2: bool,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[TierPlusCandidatesObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: TierPlusCandidatesPayload | None = ...,
        fortilink: str | None = ...,
        parent_peer1: str | None = ...,
        parent_peer2: str | None = ...,
        is_tier2: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TierPlusCandidatesObject: ...




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
        payload_dict: TierPlusCandidatesPayload | None = ...,
        fortilink: str | None = ...,
        parent_peer1: str | None = ...,
        parent_peer2: str | None = ...,
        is_tier2: bool | None = ...,
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
    "TierPlusCandidates",
    "TierPlusCandidatesResponse",
    "TierPlusCandidatesObject",
]