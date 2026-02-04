""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wifi/rogue_ap
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

class RogueApPayload(TypedDict, total=False):
    """Payload type for RogueAp operations."""
    managed_ssid_only: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class RogueApResponse(TypedDict, total=False):
    """Response type for RogueAp - use with .dict property for typed dict access."""
    status: str
    is_managed: str
    is_dead: bool
    is_wired: bool
    is_fake: bool
    capinfo: str
    ssid: str
    band: str
    mac: str
    manufacturer: str
    security_mode: str
    encryption: str
    signal_strength_noise: str
    signal_strength: int
    noise: int
    channel: int
    rate: int
    first_seen: str
    first_seen_utc: int
    last_seen: str
    last_seen_utc: int
    sta_mac: str
    wtp_count: int
    detected_by_wtp: list[str]
    onwire: bool


class RogueApObject(FortiObject[RogueApResponse]):
    """Typed FortiObject for RogueAp with field access."""
    status: str
    is_managed: str
    is_dead: bool
    is_wired: bool
    is_fake: bool
    capinfo: str
    ssid: str
    band: str
    mac: str
    manufacturer: str
    security_mode: str
    encryption: str
    signal_strength_noise: str
    signal_strength: int
    noise: int
    channel: int
    rate: int
    first_seen: str
    first_seen_utc: int
    last_seen: str
    last_seen_utc: int
    sta_mac: str
    wtp_count: int
    detected_by_wtp: list[str]
    onwire: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class RogueAp:
    """
    
    Endpoint: wifi/rogue_ap
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
        managed_ssid_only: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[RogueApObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RogueApPayload | None = ...,
        managed_ssid_only: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RogueApObject: ...




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
        payload_dict: RogueApPayload | None = ...,
        managed_ssid_only: bool | None = ...,
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
    "RogueAp",
    "RogueApResponse",
    "RogueApObject",
]