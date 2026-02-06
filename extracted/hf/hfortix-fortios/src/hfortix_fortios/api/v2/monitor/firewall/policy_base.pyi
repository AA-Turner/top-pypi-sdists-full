""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/policy
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

class PolicyPayload(TypedDict, total=False):
    """Payload type for Policy operations."""
    policyid: list[str]
    ip_version: Literal["ipv4", "ipv6"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class PolicyResponse(TypedDict, total=False):
    """Response type for Policy - use with .dict property for typed dict access."""
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
    software_bytes: int
    software_packets: int
    asic_bytes: int
    asic_packets: int
    nturbo_bytes: int
    nturbo_packets: int
    cgn_bytes: int
    cgn_packets: int
    cgn_last_used: int
    cgn_first_used: int
    cgn_hit_count: int
    oversize: bool
    x1_week_ipv4: str
    x1_week_ipv6: str


class PolicyObject(FortiObject[PolicyResponse]):
    """Typed FortiObject for Policy with field access."""
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
    software_bytes: int
    software_packets: int
    asic_bytes: int
    asic_packets: int
    nturbo_bytes: int
    nturbo_packets: int
    cgn_bytes: int
    cgn_packets: int
    cgn_last_used: int
    cgn_first_used: int
    cgn_hit_count: int
    oversize: bool
    x1_week_ipv4: str
    x1_week_ipv6: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Policy:
    """
    
    Endpoint: firewall/policy
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
        policyid: list[str] | None = ...,
        ip_version: Literal["ipv4", "ipv6"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[PolicyObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PolicyPayload | None = ...,
        policyid: list[str] | None = ...,
        ip_version: Literal["ipv4", "ipv6"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PolicyObject: ...




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
        payload_dict: PolicyPayload | None = ...,
        policyid: list[str] | None = ...,
        ip_version: Literal["ipv4", "ipv6"] | None = ...,
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
    "Policy",
    "PolicyResponse",
    "PolicyObject",
]