""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/syslogd3/override_filter
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

class OverrideFilterFreestyleItem(TypedDict, total=False):
    """Nested item for free-style field."""
    id: int
    category: Literal["traffic", "event", "virus", "webfilter", "attack", "spam", "anomaly", "voip", "dlp", "app-ctrl", "waf", "gtp", "dns", "ssh", "ssl", "file-filter", "icap", "virtual-patch", "debug"]
    filter: str
    filter_type: Literal["include", "exclude"]


class OverrideFilterPayload(TypedDict, total=False):
    """Payload type for OverrideFilter operations."""
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    forward_traffic: Literal["enable", "disable"]
    local_traffic: Literal["enable", "disable"]
    multicast_traffic: Literal["enable", "disable"]
    sniffer_traffic: Literal["enable", "disable"]
    ztna_traffic: Literal["enable", "disable"]
    http_transaction: Literal["enable", "disable"]
    anomaly: Literal["enable", "disable"]
    voip: Literal["enable", "disable"]
    gtp: Literal["enable", "disable"]
    forti_switch: Literal["enable", "disable"]
    debug: Literal["enable", "disable"]
    free_style: str | list[str] | list[OverrideFilterFreestyleItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class OverrideFilterResponse(TypedDict, total=False):
    """Response type for OverrideFilter - use with .dict property for typed dict access."""
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    forward_traffic: Literal["enable", "disable"]
    local_traffic: Literal["enable", "disable"]
    multicast_traffic: Literal["enable", "disable"]
    sniffer_traffic: Literal["enable", "disable"]
    ztna_traffic: Literal["enable", "disable"]
    http_transaction: Literal["enable", "disable"]
    anomaly: Literal["enable", "disable"]
    voip: Literal["enable", "disable"]
    gtp: Literal["enable", "disable"]
    forti_switch: Literal["enable", "disable"]
    debug: Literal["enable", "disable"]
    free_style: list[OverrideFilterFreestyleItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class OverrideFilterFreestyleItemObject(FortiObject[OverrideFilterFreestyleItem]):
    """Typed object for free-style table items with attribute access."""
    id: int
    category: Literal["traffic", "event", "virus", "webfilter", "attack", "spam", "anomaly", "voip", "dlp", "app-ctrl", "waf", "gtp", "dns", "ssh", "ssl", "file-filter", "icap", "virtual-patch", "debug"]
    filter: str
    filter_type: Literal["include", "exclude"]


class OverrideFilterObject(FortiObject):
    """Typed FortiObject for OverrideFilter with field access."""
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    forward_traffic: Literal["enable", "disable"]
    local_traffic: Literal["enable", "disable"]
    multicast_traffic: Literal["enable", "disable"]
    sniffer_traffic: Literal["enable", "disable"]
    ztna_traffic: Literal["enable", "disable"]
    http_transaction: Literal["enable", "disable"]
    anomaly: Literal["enable", "disable"]
    voip: Literal["enable", "disable"]
    gtp: Literal["enable", "disable"]
    forti_switch: Literal["enable", "disable"]
    debug: Literal["enable", "disable"]
    free_style: FortiObjectList[OverrideFilterFreestyleItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class OverrideFilter:
    """
    
    Endpoint: log/syslogd3/override_filter
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
    ) -> OverrideFilterObject: ...
    
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
        payload_dict: OverrideFilterPayload | None = ...,
        severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        forward_traffic: Literal["enable", "disable"] | None = ...,
        local_traffic: Literal["enable", "disable"] | None = ...,
        multicast_traffic: Literal["enable", "disable"] | None = ...,
        sniffer_traffic: Literal["enable", "disable"] | None = ...,
        ztna_traffic: Literal["enable", "disable"] | None = ...,
        http_transaction: Literal["enable", "disable"] | None = ...,
        anomaly: Literal["enable", "disable"] | None = ...,
        voip: Literal["enable", "disable"] | None = ...,
        gtp: Literal["enable", "disable"] | None = ...,
        forti_switch: Literal["enable", "disable"] | None = ...,
        debug: Literal["enable", "disable"] | None = ...,
        free_style: str | list[str] | list[OverrideFilterFreestyleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> OverrideFilterObject: ...


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
        payload_dict: OverrideFilterPayload | None = ...,
        severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        forward_traffic: Literal["enable", "disable"] | None = ...,
        local_traffic: Literal["enable", "disable"] | None = ...,
        multicast_traffic: Literal["enable", "disable"] | None = ...,
        sniffer_traffic: Literal["enable", "disable"] | None = ...,
        ztna_traffic: Literal["enable", "disable"] | None = ...,
        http_transaction: Literal["enable", "disable"] | None = ...,
        anomaly: Literal["enable", "disable"] | None = ...,
        voip: Literal["enable", "disable"] | None = ...,
        gtp: Literal["enable", "disable"] | None = ...,
        forti_switch: Literal["enable", "disable"] | None = ...,
        debug: Literal["enable", "disable"] | None = ...,
        free_style: str | list[str] | list[OverrideFilterFreestyleItem] | None = ...,
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
    "OverrideFilter",
    "OverrideFilterPayload",
    "OverrideFilterResponse",
    "OverrideFilterObject",
]