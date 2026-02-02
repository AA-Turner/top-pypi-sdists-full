""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ips/global_
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

class GlobalTlsactiveprobeDict(TypedDict, total=False):
    """Nested object type for tls-active-probe field."""
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vdom: str
    source_ip: str
    source_ip6: str


class GlobalPayload(TypedDict, total=False):
    """Payload type for Global operations."""
    fail_open: Literal["enable", "disable"]
    database: Literal["regular", "extended"]
    traffic_submit: Literal["enable", "disable"]
    anomaly_mode: Literal["periodical", "continuous"]
    session_limit_mode: Literal["accurate", "heuristic"]
    socket_size: int
    engine_count: int
    sync_session_ttl: Literal["enable", "disable"]
    deep_app_insp_timeout: int
    deep_app_insp_db_limit: int
    exclude_signatures: Literal["none", "ot"]
    packet_log_queue_depth: int
    ngfw_max_scan_range: int
    av_mem_limit: int
    machine_learning_detection: Literal["enable", "disable"]
    tls_active_probe: GlobalTlsactiveprobeDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GlobalResponse(TypedDict, total=False):
    """Response type for Global - use with .dict property for typed dict access."""
    fail_open: Literal["enable", "disable"]
    database: Literal["regular", "extended"]
    traffic_submit: Literal["enable", "disable"]
    anomaly_mode: Literal["periodical", "continuous"]
    session_limit_mode: Literal["accurate", "heuristic"]
    socket_size: int
    engine_count: int
    sync_session_ttl: Literal["enable", "disable"]
    deep_app_insp_timeout: int
    deep_app_insp_db_limit: int
    exclude_signatures: Literal["none", "ot"]
    packet_log_queue_depth: int
    ngfw_max_scan_range: int
    av_mem_limit: int
    machine_learning_detection: Literal["enable", "disable"]
    tls_active_probe: GlobalTlsactiveprobeDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GlobalTlsactiveprobeObject(FortiObject):
    """Nested object for tls-active-probe field with attribute access."""
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vdom: str
    source_ip: str
    source_ip6: str


class GlobalObject(FortiObject):
    """Typed FortiObject for Global with field access."""
    fail_open: Literal["enable", "disable"]
    database: Literal["regular", "extended"]
    traffic_submit: Literal["enable", "disable"]
    anomaly_mode: Literal["periodical", "continuous"]
    session_limit_mode: Literal["accurate", "heuristic"]
    socket_size: int
    engine_count: int
    sync_session_ttl: Literal["enable", "disable"]
    deep_app_insp_timeout: int
    deep_app_insp_db_limit: int
    exclude_signatures: Literal["none", "ot"]
    packet_log_queue_depth: int
    ngfw_max_scan_range: int
    av_mem_limit: int
    machine_learning_detection: Literal["enable", "disable"]
    tls_active_probe: GlobalTlsactiveprobeObject


# ================================================================
# Main Endpoint Class
# ================================================================

class Global:
    """
    
    Endpoint: ips/global_
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
    ) -> GlobalObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GlobalPayload | None = ...,
        fail_open: Literal["enable", "disable"] | None = ...,
        database: Literal["regular", "extended"] | None = ...,
        traffic_submit: Literal["enable", "disable"] | None = ...,
        anomaly_mode: Literal["periodical", "continuous"] | None = ...,
        session_limit_mode: Literal["accurate", "heuristic"] | None = ...,
        socket_size: int | None = ...,
        engine_count: int | None = ...,
        sync_session_ttl: Literal["enable", "disable"] | None = ...,
        deep_app_insp_timeout: int | None = ...,
        deep_app_insp_db_limit: int | None = ...,
        exclude_signatures: Literal["none", "ot"] | None = ...,
        packet_log_queue_depth: int | None = ...,
        ngfw_max_scan_range: int | None = ...,
        av_mem_limit: int | None = ...,
        machine_learning_detection: Literal["enable", "disable"] | None = ...,
        tls_active_probe: GlobalTlsactiveprobeDict | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GlobalObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: GlobalPayload | None = ...,
        fail_open: Literal["enable", "disable"] | None = ...,
        database: Literal["regular", "extended"] | None = ...,
        traffic_submit: Literal["enable", "disable"] | None = ...,
        anomaly_mode: Literal["periodical", "continuous"] | None = ...,
        session_limit_mode: Literal["accurate", "heuristic"] | None = ...,
        socket_size: int | None = ...,
        engine_count: int | None = ...,
        sync_session_ttl: Literal["enable", "disable"] | None = ...,
        deep_app_insp_timeout: int | None = ...,
        deep_app_insp_db_limit: int | None = ...,
        exclude_signatures: Literal["none", "ot"] | None = ...,
        packet_log_queue_depth: int | None = ...,
        ngfw_max_scan_range: int | None = ...,
        av_mem_limit: int | None = ...,
        machine_learning_detection: Literal["enable", "disable"] | None = ...,
        tls_active_probe: GlobalTlsactiveprobeDict | None = ...,
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
    "Global",
    "GlobalPayload",
    "GlobalResponse",
    "GlobalObject",
]