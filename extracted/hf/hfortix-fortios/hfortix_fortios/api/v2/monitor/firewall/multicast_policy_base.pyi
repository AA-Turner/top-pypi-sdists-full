""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/multicast_policy
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

class MulticastPolicyPayload(TypedDict, total=False):
    """Payload type for MulticastPolicy operations."""
    policyid: int


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class MulticastPolicyResponse(TypedDict, total=False):
    """Response type for MulticastPolicy - use with .dict property for typed dict access."""
    policyid: int
    active_sessions: int
    bytes: int
    packets: int
    last_used: int
    first_used: int
    hit_count: int
    uuid: str
    uuid_type: str
    session_count: int
    session_first_used: int
    session_last_used: int
    oversize: bool
    x1_week_ipv4: str


class MulticastPolicyObject(FortiObject[MulticastPolicyResponse]):
    """Typed FortiObject for MulticastPolicy with field access."""
    policyid: int
    active_sessions: int
    bytes: int
    packets: int
    last_used: int
    first_used: int
    hit_count: int
    uuid: str
    uuid_type: str
    session_count: int
    session_first_used: int
    session_last_used: int
    oversize: bool
    x1_week_ipv4: str



# ================================================================
# Main Endpoint Class
# ================================================================

class MulticastPolicy:
    """
    
    Endpoint: firewall/multicast_policy
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
        policyid: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[MulticastPolicyObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MulticastPolicyPayload | None = ...,
        policyid: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastPolicyObject: ...


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
        payload_dict: MulticastPolicyPayload | None = ...,
        policyid: int | None = ...,
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
    "MulticastPolicy",
    "MulticastPolicyResponse",
    "MulticastPolicyObject",
]