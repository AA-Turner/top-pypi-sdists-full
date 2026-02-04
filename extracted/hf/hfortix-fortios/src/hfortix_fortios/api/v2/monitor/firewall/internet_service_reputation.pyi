""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_reputation
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

class InternetServiceReputationPayload(TypedDict, total=False):
    """Payload type for InternetServiceReputation operations."""
    ip: str
    is_ipv6: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class InternetServiceReputationResponse(TypedDict, total=False):
    """Response type for InternetServiceReputation - use with .dict property for typed dict access."""
    id: int
    name: str
    reputation: int
    popularity: int
    botnet_id: int
    domain_id: int
    country_id: int
    region_id: int
    city_id: int
    blocklist: list[str]


class InternetServiceReputationObject(FortiObject[InternetServiceReputationResponse]):
    """Typed FortiObject for InternetServiceReputation with field access."""
    id: int
    name: str
    reputation: int
    popularity: int
    botnet_id: int
    domain_id: int
    country_id: int
    region_id: int
    city_id: int
    blocklist: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceReputation:
    """
    
    Endpoint: firewall/internet_service_reputation
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
        ip: str,
        is_ipv6: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[InternetServiceReputationObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceReputationPayload | None = ...,
        ip: str | None = ...,
        is_ipv6: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceReputationObject: ...




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
        payload_dict: InternetServiceReputationPayload | None = ...,
        ip: str | None = ...,
        is_ipv6: bool | None = ...,
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
    "InternetServiceReputation",
    "InternetServiceReputationResponse",
    "InternetServiceReputationObject",
]