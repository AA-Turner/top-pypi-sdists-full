""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/fortianalyzer2/override_setting
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

class OverrideSettingSerialItem(TypedDict, total=False):
    """Nested item for serial field."""
    name: str


class OverrideSettingPayload(TypedDict, total=False):
    """Payload type for OverrideSetting operations."""
    use_management_vdom: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    ips_archive: Literal["enable", "disable"]
    server: str
    alt_server: str
    fallback_to_primary: Literal["enable", "disable"]
    certificate_verification: Literal["enable", "disable"]
    serial: str | list[str] | list[OverrideSettingSerialItem]
    server_cert_ca: str
    preshared_key: str
    access_config: Literal["enable", "disable"]
    hmac_algorithm: Literal["sha256"]
    enc_algorithm: Literal["high-medium", "high", "low"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    conn_timeout: int
    monitor_keepalive_period: int
    monitor_failure_retry_period: int
    certificate: str
    source_ip: str
    upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"]
    upload_interval: Literal["daily", "weekly", "monthly"]
    upload_day: str
    upload_time: str
    reliable: Literal["enable", "disable"]
    priority: Literal["default", "low"]
    max_log_rate: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class OverrideSettingResponse(TypedDict, total=False):
    """Response type for OverrideSetting - use with .dict property for typed dict access."""
    use_management_vdom: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    ips_archive: Literal["enable", "disable"]
    server: str
    alt_server: str
    fallback_to_primary: Literal["enable", "disable"]
    certificate_verification: Literal["enable", "disable"]
    serial: list[OverrideSettingSerialItem]
    server_cert_ca: str
    preshared_key: str
    access_config: Literal["enable", "disable"]
    hmac_algorithm: Literal["sha256"]
    enc_algorithm: Literal["high-medium", "high", "low"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    conn_timeout: int
    monitor_keepalive_period: int
    monitor_failure_retry_period: int
    certificate: str
    source_ip: str
    upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"]
    upload_interval: Literal["daily", "weekly", "monthly"]
    upload_day: str
    upload_time: str
    reliable: Literal["enable", "disable"]
    priority: Literal["default", "low"]
    max_log_rate: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class OverrideSettingSerialItemObject(FortiObject[OverrideSettingSerialItem]):
    """Typed object for serial table items with attribute access."""
    name: str


class OverrideSettingObject(FortiObject):
    """Typed FortiObject for OverrideSetting with field access."""
    use_management_vdom: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    ips_archive: Literal["enable", "disable"]
    server: str
    alt_server: str
    fallback_to_primary: Literal["enable", "disable"]
    certificate_verification: Literal["enable", "disable"]
    server_cert_ca: str
    preshared_key: str
    access_config: Literal["enable", "disable"]
    hmac_algorithm: Literal["sha256"]
    enc_algorithm: Literal["high-medium", "high", "low"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    conn_timeout: int
    monitor_keepalive_period: int
    monitor_failure_retry_period: int
    certificate: str
    source_ip: str
    upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"]
    upload_interval: Literal["daily", "weekly", "monthly"]
    upload_day: str
    upload_time: str
    reliable: Literal["enable", "disable"]
    priority: Literal["default", "low"]
    max_log_rate: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class OverrideSetting:
    """
    
    Endpoint: log/fortianalyzer2/override_setting
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
    ) -> OverrideSettingObject: ...
    
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
        payload_dict: OverrideSettingPayload | None = ...,
        use_management_vdom: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        ips_archive: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        alt_server: str | None = ...,
        fallback_to_primary: Literal["enable", "disable"] | None = ...,
        certificate_verification: Literal["enable", "disable"] | None = ...,
        serial: str | list[str] | list[OverrideSettingSerialItem] | None = ...,
        server_cert_ca: str | None = ...,
        preshared_key: str | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        hmac_algorithm: Literal["sha256"] | None = ...,
        enc_algorithm: Literal["high-medium", "high", "low"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        conn_timeout: int | None = ...,
        monitor_keepalive_period: int | None = ...,
        monitor_failure_retry_period: int | None = ...,
        certificate: str | None = ...,
        source_ip: str | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        reliable: Literal["enable", "disable"] | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> OverrideSettingObject: ...


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
        payload_dict: OverrideSettingPayload | None = ...,
        use_management_vdom: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        ips_archive: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        alt_server: str | None = ...,
        fallback_to_primary: Literal["enable", "disable"] | None = ...,
        certificate_verification: Literal["enable", "disable"] | None = ...,
        serial: str | list[str] | list[OverrideSettingSerialItem] | None = ...,
        server_cert_ca: str | None = ...,
        preshared_key: str | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        hmac_algorithm: Literal["sha256"] | None = ...,
        enc_algorithm: Literal["high-medium", "high", "low"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        conn_timeout: int | None = ...,
        monitor_keepalive_period: int | None = ...,
        monitor_failure_retry_period: int | None = ...,
        certificate: str | None = ...,
        source_ip: str | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        reliable: Literal["enable", "disable"] | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
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
    "OverrideSetting",
    "OverrideSettingPayload",
    "OverrideSettingResponse",
    "OverrideSettingObject",
]