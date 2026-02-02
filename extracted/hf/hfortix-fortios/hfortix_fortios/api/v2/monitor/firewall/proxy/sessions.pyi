""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/proxy/sessions
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

class SessionsPayload(TypedDict, total=False):
    """Payload type for Sessions operations."""
    ip_version: Literal["ipv4", "ipv6", "ipboth"]
    count: int
    summary: bool
    srcaddr: str
    dstaddr: str
    srcaddr6: str
    dstaddr6: str
    srcport: str
    dstport: str
    srcintf: str
    dstintf: str
    policyid: str
    proxy_policyid: str
    protocol: str
    application: str
    country: str
    seconds: str
    since: str
    owner: str
    username: str
    src_uuid: str
    dst_uuid: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class SessionsResponse(TypedDict, total=False):
    """Response type for Sessions - use with .dict property for typed dict access."""
    summary: str
    details: list[str]


class SessionsObject(FortiObject[SessionsResponse]):
    """Typed FortiObject for Sessions with field access."""
    summary: str
    details: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class Sessions:
    """
    
    Endpoint: firewall/proxy/sessions
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
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = ...,
        count: int,
        summary: bool | None = ...,
        srcaddr: str | None = ...,
        dstaddr: str | None = ...,
        srcaddr6: str | None = ...,
        dstaddr6: str | None = ...,
        srcport: str | None = ...,
        dstport: str | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        policyid: str | None = ...,
        proxy_policyid: str | None = ...,
        protocol: str | None = ...,
        application: str | None = ...,
        country: str | None = ...,
        seconds: str | None = ...,
        since: str | None = ...,
        owner: str | None = ...,
        username: str | None = ...,
        src_uuid: str | None = ...,
        dst_uuid: str | None = ...,
        filter: str | list[str] | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[SessionsObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SessionsPayload | None = ...,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = ...,
        count: int | None = ...,
        summary: bool | None = ...,
        srcaddr: str | None = ...,
        dstaddr: str | None = ...,
        srcaddr6: str | None = ...,
        dstaddr6: str | None = ...,
        srcport: str | None = ...,
        dstport: str | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        policyid: str | None = ...,
        proxy_policyid: str | None = ...,
        protocol: str | None = ...,
        application: str | None = ...,
        country: str | None = ...,
        seconds: str | None = ...,
        since: str | None = ...,
        owner: str | None = ...,
        username: str | None = ...,
        src_uuid: str | None = ...,
        dst_uuid: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SessionsObject: ...


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
        payload_dict: SessionsPayload | None = ...,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = ...,
        count: int | None = ...,
        summary: bool | None = ...,
        srcaddr: str | None = ...,
        dstaddr: str | None = ...,
        srcaddr6: str | None = ...,
        dstaddr6: str | None = ...,
        srcport: str | None = ...,
        dstport: str | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        policyid: str | None = ...,
        proxy_policyid: str | None = ...,
        protocol: str | None = ...,
        application: str | None = ...,
        country: str | None = ...,
        seconds: str | None = ...,
        since: str | None = ...,
        owner: str | None = ...,
        username: str | None = ...,
        src_uuid: str | None = ...,
        dst_uuid: str | None = ...,
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
    "Sessions",
    "SessionsResponse",
    "SessionsObject",
]