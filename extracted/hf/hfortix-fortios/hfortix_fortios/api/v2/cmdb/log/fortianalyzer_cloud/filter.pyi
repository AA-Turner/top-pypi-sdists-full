""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/fortianalyzer_cloud/filter
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

class FilterFreestyleItem(TypedDict, total=False):
    """Nested item for free-style field."""
    id: int
    category: Literal["traffic", "event", "virus", "webfilter", "attack", "spam", "anomaly", "voip", "dlp", "app-ctrl", "waf", "gtp", "dns", "ssh", "ssl", "file-filter", "icap", "virtual-patch", "debug"]
    filter: str
    filter_type: Literal["include", "exclude"]


class FilterPayload(TypedDict, total=False):
    """Payload type for Filter operations."""
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    forward_traffic: Literal["enable", "disable"]
    local_traffic: Literal["enable", "disable"]
    multicast_traffic: Literal["enable", "disable"]
    sniffer_traffic: Literal["enable", "disable"]
    ztna_traffic: Literal["enable", "disable"]
    http_transaction: Literal["enable", "disable"]
    anomaly: Literal["enable", "disable"]
    voip: Literal["enable", "disable"]
    dlp_archive: Literal["enable", "disable"]
    gtp: Literal["enable", "disable"]
    forti_switch: Literal["enable", "disable"]
    free_style: str | list[str] | list[FilterFreestyleItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FilterResponse(TypedDict, total=False):
    """Response type for Filter - use with .dict property for typed dict access."""
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    forward_traffic: Literal["enable", "disable"]
    local_traffic: Literal["enable", "disable"]
    multicast_traffic: Literal["enable", "disable"]
    sniffer_traffic: Literal["enable", "disable"]
    ztna_traffic: Literal["enable", "disable"]
    http_transaction: Literal["enable", "disable"]
    anomaly: Literal["enable", "disable"]
    voip: Literal["enable", "disable"]
    dlp_archive: Literal["enable", "disable"]
    gtp: Literal["enable", "disable"]
    forti_switch: Literal["enable", "disable"]
    free_style: list[FilterFreestyleItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FilterFreestyleItemObject(FortiObject[FilterFreestyleItem]):
    """Typed object for free-style table items with attribute access."""
    id: int
    category: Literal["traffic", "event", "virus", "webfilter", "attack", "spam", "anomaly", "voip", "dlp", "app-ctrl", "waf", "gtp", "dns", "ssh", "ssl", "file-filter", "icap", "virtual-patch", "debug"]
    filter: str
    filter_type: Literal["include", "exclude"]


class FilterObject(FortiObject):
    """Typed FortiObject for Filter with field access."""
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    forward_traffic: Literal["enable", "disable"]
    local_traffic: Literal["enable", "disable"]
    multicast_traffic: Literal["enable", "disable"]
    sniffer_traffic: Literal["enable", "disable"]
    ztna_traffic: Literal["enable", "disable"]
    http_transaction: Literal["enable", "disable"]
    anomaly: Literal["enable", "disable"]
    voip: Literal["enable", "disable"]
    dlp_archive: Literal["enable", "disable"]
    gtp: Literal["enable", "disable"]
    forti_switch: Literal["enable", "disable"]
    free_style: FortiObjectList[FilterFreestyleItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Filter:
    """
    
    Endpoint: log/fortianalyzer_cloud/filter
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FilterObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FilterPayload | None = ...,
        severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        forward_traffic: Literal["enable", "disable"] | None = ...,
        local_traffic: Literal["enable", "disable"] | None = ...,
        multicast_traffic: Literal["enable", "disable"] | None = ...,
        sniffer_traffic: Literal["enable", "disable"] | None = ...,
        ztna_traffic: Literal["enable", "disable"] | None = ...,
        http_transaction: Literal["enable", "disable"] | None = ...,
        anomaly: Literal["enable", "disable"] | None = ...,
        voip: Literal["enable", "disable"] | None = ...,
        dlp_archive: Literal["enable", "disable"] | None = ...,
        gtp: Literal["enable", "disable"] | None = ...,
        forti_switch: Literal["enable", "disable"] | None = ...,
        free_style: str | list[str] | list[FilterFreestyleItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FilterObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FilterPayload | None = ...,
        severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        forward_traffic: Literal["enable", "disable"] | None = ...,
        local_traffic: Literal["enable", "disable"] | None = ...,
        multicast_traffic: Literal["enable", "disable"] | None = ...,
        sniffer_traffic: Literal["enable", "disable"] | None = ...,
        ztna_traffic: Literal["enable", "disable"] | None = ...,
        http_transaction: Literal["enable", "disable"] | None = ...,
        anomaly: Literal["enable", "disable"] | None = ...,
        voip: Literal["enable", "disable"] | None = ...,
        dlp_archive: Literal["enable", "disable"] | None = ...,
        gtp: Literal["enable", "disable"] | None = ...,
        forti_switch: Literal["enable", "disable"] | None = ...,
        free_style: str | list[str] | list[FilterFreestyleItem] | None = ...,
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
    "Filter",
    "FilterPayload",
    "FilterResponse",
    "FilterObject",
]