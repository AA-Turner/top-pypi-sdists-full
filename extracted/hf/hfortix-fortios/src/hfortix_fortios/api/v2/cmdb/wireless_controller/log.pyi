""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/log
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

class LogPayload(TypedDict, total=False):
    """Payload type for Log operations."""
    status: Literal["enable", "disable"]
    addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LogResponse(TypedDict, total=False):
    """Response type for Log - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LogObject(FortiObject):
    """Typed FortiObject for Log with field access."""
    status: Literal["enable", "disable"]
    addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Log:
    """
    
    Endpoint: wireless_controller/log
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
    ) -> LogObject: ...
    
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
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LogObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


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
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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
    "Log",
    "LogPayload",
    "LogResponse",
    "LogObject",
]