""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/check_addrgrp_exclude_mac_member
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

class CheckAddrgrpExcludeMacMemberPayload(TypedDict, total=False):
    """Payload type for CheckAddrgrpExcludeMacMember operations."""
    mkey: str
    ip_version: Literal["ipv4", "ipv6"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class CheckAddrgrpExcludeMacMemberResponse(TypedDict, total=False):
    """Response type for CheckAddrgrpExcludeMacMember - use with .dict property for typed dict access."""
    exclude_mac_member: bool


class CheckAddrgrpExcludeMacMemberObject(FortiObject[CheckAddrgrpExcludeMacMemberResponse]):
    """Typed FortiObject for CheckAddrgrpExcludeMacMember with field access."""
    exclude_mac_member: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class CheckAddrgrpExcludeMacMember:
    """
    
    Endpoint: firewall/check_addrgrp_exclude_mac_member
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
        mkey: str,
        ip_version: Literal["ipv4", "ipv6"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[CheckAddrgrpExcludeMacMemberObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CheckAddrgrpExcludeMacMemberPayload | None = ...,
        mkey: str | None = ...,
        ip_version: Literal["ipv4", "ipv6"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CheckAddrgrpExcludeMacMemberObject: ...




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
        payload_dict: CheckAddrgrpExcludeMacMemberPayload | None = ...,
        mkey: str | None = ...,
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
    "CheckAddrgrpExcludeMacMember",
    "CheckAddrgrpExcludeMacMemberResponse",
    "CheckAddrgrpExcludeMacMemberObject",
]