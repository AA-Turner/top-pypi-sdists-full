""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: fortiview/realtime_statistics
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

class RealtimeStatisticsPayload(TypedDict, total=False):
    """Payload type for RealtimeStatistics operations."""
    srcaddr: str
    dstaddr: str
    srcaddr6: str
    dstaddr6: str
    srcport: str
    dstport: str
    srcintf: str
    srcintfrole: list[str]
    dstintf: str
    dstintfrole: list[str]
    policyid: str
    security_policyid: str
    protocol: str
    web_category: str
    web_domain: str
    application: str
    country: str
    seconds: str
    since: str
    owner: str
    username: str
    shaper: str
    srcuuid: str
    dstuuid: str
    sessionid: int
    report_by: str
    sort_by: str
    ip_version: Literal["ipv4", "ipv6", "ipboth"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RealtimeStatisticsResponse(TypedDict, total=False):
    """Response type for RealtimeStatistics - use with .dict property for typed dict access."""
    srcaddr: str
    dstaddr: str
    srcaddr6: str
    dstaddr6: str
    srcport: str
    dstport: str
    srcintf: str
    srcintfrole: list[str]
    dstintf: str
    dstintfrole: list[str]
    policyid: str
    security_policyid: str
    protocol: str
    web_category: str
    web_domain: str
    application: str
    country: str
    seconds: str
    since: str
    owner: str
    username: str
    shaper: str
    srcuuid: str
    dstuuid: str
    sessionid: int
    report_by: str
    sort_by: str
    ip_version: Literal["ipv4", "ipv6", "ipboth"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RealtimeStatisticsObject(FortiObject):
    """Typed FortiObject for RealtimeStatistics with field access."""
    srcaddr: str
    dstaddr: str
    srcaddr6: str
    dstaddr6: str
    srcport: str
    dstport: str
    srcintf: str
    srcintfrole: list[str]
    dstintf: str
    dstintfrole: list[str]
    policyid: str
    security_policyid: str
    protocol: str
    web_category: str
    web_domain: str
    application: str
    country: str
    seconds: str
    since: str
    owner: str
    username: str
    shaper: str
    srcuuid: str
    dstuuid: str
    sessionid: int
    report_by: str
    sort_by: str
    ip_version: Literal["ipv4", "ipv6", "ipboth"]


# ================================================================
# Main Endpoint Class
# ================================================================

class RealtimeStatistics:
    """
    
    Endpoint: fortiview/realtime_statistics
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
        srcaddr: str | None = ...,
        dstaddr: str | None = ...,
        srcaddr6: str | None = ...,
        dstaddr6: str | None = ...,
        srcport: str | None = ...,
        dstport: str | None = ...,
        srcintf: str | None = ...,
        srcintfrole: list[str] | None = ...,
        dstintf: str | None = ...,
        dstintfrole: list[str] | None = ...,
        policyid: str | None = ...,
        security_policyid: str | None = ...,
        protocol: str | None = ...,
        web_category: str | None = ...,
        web_domain: str | None = ...,
        application: str | None = ...,
        country: str | None = ...,
        seconds: str | None = ...,
        since: str | None = ...,
        owner: str | None = ...,
        username: str | None = ...,
        shaper: str | None = ...,
        srcuuid: str | None = ...,
        dstuuid: str | None = ...,
        sessionid: int | None = ...,
        report_by: str | None = ...,
        sort_by: str | None = ...,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RealtimeStatisticsObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RealtimeStatisticsPayload | None = ...,
        srcaddr: str | None = ...,
        dstaddr: str | None = ...,
        srcaddr6: str | None = ...,
        dstaddr6: str | None = ...,
        srcport: str | None = ...,
        dstport: str | None = ...,
        srcintf: str | None = ...,
        srcintfrole: list[str] | None = ...,
        dstintf: str | None = ...,
        dstintfrole: list[str] | None = ...,
        policyid: str | None = ...,
        security_policyid: str | None = ...,
        protocol: str | None = ...,
        web_category: str | None = ...,
        web_domain: str | None = ...,
        application: str | None = ...,
        country: str | None = ...,
        seconds: str | None = ...,
        since: str | None = ...,
        owner: str | None = ...,
        username: str | None = ...,
        shaper: str | None = ...,
        srcuuid: str | None = ...,
        dstuuid: str | None = ...,
        sessionid: int | None = ...,
        report_by: str | None = ...,
        sort_by: str | None = ...,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RealtimeStatisticsObject: ...




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
        payload_dict: RealtimeStatisticsPayload | None = ...,
        srcaddr: str | None = ...,
        dstaddr: str | None = ...,
        srcaddr6: str | None = ...,
        dstaddr6: str | None = ...,
        srcport: str | None = ...,
        dstport: str | None = ...,
        srcintf: str | None = ...,
        srcintfrole: list[str] | None = ...,
        dstintf: str | None = ...,
        dstintfrole: list[str] | None = ...,
        policyid: str | None = ...,
        security_policyid: str | None = ...,
        protocol: str | None = ...,
        web_category: str | None = ...,
        web_domain: str | None = ...,
        application: str | None = ...,
        country: str | None = ...,
        seconds: str | None = ...,
        since: str | None = ...,
        owner: str | None = ...,
        username: str | None = ...,
        shaper: str | None = ...,
        srcuuid: str | None = ...,
        dstuuid: str | None = ...,
        sessionid: int | None = ...,
        report_by: str | None = ...,
        sort_by: str | None = ...,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = ...,
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
    "RealtimeStatistics",
    "RealtimeStatisticsPayload",
    "RealtimeStatisticsResponse",
    "RealtimeStatisticsObject",
]