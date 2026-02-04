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
# Response Types (TypedDict for dict-style access)
# ================================================================

class PolicyResponse(TypedDict, total=False):
    """Response type for Policy - use with .dict property for typed dict access."""
    policyid: list[str]
    ip_version: Literal["ipv4", "ipv6"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PolicyObject(FortiObject):
    """Typed FortiObject for Policy with field access."""
    policyid: list[str]
    ip_version: Literal["ipv4", "ipv6"]


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
    ) -> PolicyObject: ...
    


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
    "PolicyPayload",
    "PolicyResponse",
    "PolicyObject",
]