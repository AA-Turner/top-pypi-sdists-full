""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/eventfilter
Category: cmdb
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

class EventfilterPayload(TypedDict, total=False):
    """Payload type for Eventfilter operations."""
    event: Literal["enable", "disable"]
    system: Literal["enable", "disable"]
    vpn: Literal["enable", "disable"]
    user: Literal["enable", "disable"]
    router: Literal["enable", "disable"]
    wireless_activity: Literal["enable", "disable"]
    wan_opt: Literal["enable", "disable"]
    endpoint: Literal["enable", "disable"]
    ha: Literal["enable", "disable"]
    security_rating: Literal["enable", "disable"]
    fortiextender: Literal["enable", "disable"]
    connector: Literal["enable", "disable"]
    sdwan: Literal["enable", "disable"]
    cifs: Literal["enable", "disable"]
    switch_controller: Literal["enable", "disable"]
    rest_api: Literal["enable", "disable"]
    web_svc: Literal["enable", "disable"]
    webproxy: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class EventfilterResponse(TypedDict, total=False):
    """Response type for Eventfilter - use with .dict property for typed dict access."""
    event: Literal["enable", "disable"]
    system: Literal["enable", "disable"]
    vpn: Literal["enable", "disable"]
    user: Literal["enable", "disable"]
    router: Literal["enable", "disable"]
    wireless_activity: Literal["enable", "disable"]
    wan_opt: Literal["enable", "disable"]
    endpoint: Literal["enable", "disable"]
    ha: Literal["enable", "disable"]
    security_rating: Literal["enable", "disable"]
    fortiextender: Literal["enable", "disable"]
    connector: Literal["enable", "disable"]
    sdwan: Literal["enable", "disable"]
    cifs: Literal["enable", "disable"]
    switch_controller: Literal["enable", "disable"]
    rest_api: Literal["enable", "disable"]
    web_svc: Literal["enable", "disable"]
    webproxy: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class EventfilterObject(FortiObject):
    """Typed FortiObject for Eventfilter with field access."""
    event: Literal["enable", "disable"]
    system: Literal["enable", "disable"]
    vpn: Literal["enable", "disable"]
    user: Literal["enable", "disable"]
    router: Literal["enable", "disable"]
    wireless_activity: Literal["enable", "disable"]
    wan_opt: Literal["enable", "disable"]
    endpoint: Literal["enable", "disable"]
    ha: Literal["enable", "disable"]
    security_rating: Literal["enable", "disable"]
    fortiextender: Literal["enable", "disable"]
    connector: Literal["enable", "disable"]
    sdwan: Literal["enable", "disable"]
    cifs: Literal["enable", "disable"]
    switch_controller: Literal["enable", "disable"]
    rest_api: Literal["enable", "disable"]
    web_svc: Literal["enable", "disable"]
    webproxy: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Eventfilter:
    """
    
    Endpoint: log/eventfilter
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> EventfilterObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> EventfilterObject: ...


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
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
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
    "Eventfilter",
    "EventfilterPayload",
    "EventfilterResponse",
    "EventfilterObject",
]