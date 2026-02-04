""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/historic_daily_remote_logs
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

class HistoricDailyRemoteLogsPayload(TypedDict, total=False):
    """Payload type for HistoricDailyRemoteLogs operations."""
    server: Literal["forticloud", "fortianalyzer", "fortianalyzercloud", "nulldevice"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class HistoricDailyRemoteLogsResponse(TypedDict, total=False):
    """Response type for HistoricDailyRemoteLogs - use with .dict property for typed dict access."""
    traffic: str
    event: str
    virus: str
    ips: str
    emailfilter: str
    anomaly: str
    voip: str
    dlp: str
    app_ctrl: str
    webfilter: str
    waf: str
    dns: str
    ssh: str
    ssl: str
    file_filter: str
    icap: str
    sctp_filter: str
    forti_switch: str
    virtual_patch: str
    casb: str
    unknown: str


class HistoricDailyRemoteLogsObject(FortiObject[HistoricDailyRemoteLogsResponse]):
    """Typed FortiObject for HistoricDailyRemoteLogs with field access."""
    traffic: str
    event: str
    virus: str
    ips: str
    emailfilter: str
    anomaly: str
    voip: str
    dlp: str
    app_ctrl: str
    webfilter: str
    waf: str
    dns: str
    ssh: str
    ssl: str
    file_filter: str
    icap: str
    sctp_filter: str
    forti_switch: str
    virtual_patch: str
    casb: str
    unknown: str



# ================================================================
# Main Endpoint Class
# ================================================================

class HistoricDailyRemoteLogs:
    """
    
    Endpoint: log/historic_daily_remote_logs
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
        server: Literal["forticloud", "fortianalyzer", "fortianalyzercloud", "nulldevice"],
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[HistoricDailyRemoteLogsObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: HistoricDailyRemoteLogsPayload | None = ...,
        server: Literal["forticloud", "fortianalyzer", "fortianalyzercloud", "nulldevice"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HistoricDailyRemoteLogsObject: ...




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
        payload_dict: HistoricDailyRemoteLogsPayload | None = ...,
        server: Literal["forticloud", "fortianalyzer", "fortianalyzercloud", "nulldevice"] | None = ...,
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
    "HistoricDailyRemoteLogs",
    "HistoricDailyRemoteLogsResponse",
    "HistoricDailyRemoteLogsObject",
]