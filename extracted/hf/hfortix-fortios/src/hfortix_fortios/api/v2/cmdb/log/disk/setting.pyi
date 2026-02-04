""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/disk/setting
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

class SettingPayload(TypedDict, total=False):
    """Payload type for Setting operations."""
    status: Literal["enable", "disable"]
    ips_archive: Literal["enable", "disable"]
    max_log_file_size: int
    max_policy_packet_capture_size: int
    roll_schedule: Literal["daily", "weekly"]
    roll_day: str | list[str]
    roll_time: str
    diskfull: Literal["overwrite", "nolog"]
    log_quota: int
    dlp_archive_quota: int
    report_quota: int
    maximum_log_age: int
    upload: Literal["enable", "disable"]
    upload_destination: Literal["ftp-server"]
    uploadip: str
    uploadport: int
    source_ip: str
    uploaduser: str
    uploadpass: str
    uploaddir: str
    uploadtype: str | list[str]
    uploadsched: Literal["disable", "enable"]
    uploadtime: str
    upload_delete_files: Literal["enable", "disable"]
    upload_ssl_conn: Literal["default", "high", "low", "disable"]
    full_first_warning_threshold: int
    full_second_warning_threshold: int
    full_final_warning_threshold: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    ips_archive: Literal["enable", "disable"]
    max_log_file_size: int
    max_policy_packet_capture_size: int
    roll_schedule: Literal["daily", "weekly"]
    roll_day: str
    roll_time: str
    diskfull: Literal["overwrite", "nolog"]
    log_quota: int
    dlp_archive_quota: int
    report_quota: int
    maximum_log_age: int
    upload: Literal["enable", "disable"]
    upload_destination: Literal["ftp-server"]
    uploadip: str
    uploadport: int
    source_ip: str
    uploaduser: str
    uploadpass: str
    uploaddir: str
    uploadtype: str
    uploadsched: Literal["disable", "enable"]
    uploadtime: str
    upload_delete_files: Literal["enable", "disable"]
    upload_ssl_conn: Literal["default", "high", "low", "disable"]
    full_first_warning_threshold: int
    full_second_warning_threshold: int
    full_final_warning_threshold: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    status: Literal["enable", "disable"]
    ips_archive: Literal["enable", "disable"]
    max_log_file_size: int
    max_policy_packet_capture_size: int
    roll_schedule: Literal["daily", "weekly"]
    roll_day: str
    roll_time: str
    diskfull: Literal["overwrite", "nolog"]
    log_quota: int
    dlp_archive_quota: int
    report_quota: int
    maximum_log_age: int
    upload: Literal["enable", "disable"]
    upload_destination: Literal["ftp-server"]
    uploadip: str
    uploadport: int
    source_ip: str
    uploaduser: str
    uploadpass: str
    uploaddir: str
    uploadtype: str
    uploadsched: Literal["disable", "enable"]
    uploadtime: str
    upload_delete_files: Literal["enable", "disable"]
    upload_ssl_conn: Literal["default", "high", "low", "disable"]
    full_first_warning_threshold: int
    full_second_warning_threshold: int
    full_final_warning_threshold: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: log/disk/setting
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
    ) -> SettingObject: ...
    
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
        payload_dict: SettingPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        ips_archive: Literal["enable", "disable"] | None = ...,
        max_log_file_size: int | None = ...,
        max_policy_packet_capture_size: int | None = ...,
        roll_schedule: Literal["daily", "weekly"] | None = ...,
        roll_day: str | list[str] | None = ...,
        roll_time: str | None = ...,
        diskfull: Literal["overwrite", "nolog"] | None = ...,
        log_quota: int | None = ...,
        dlp_archive_quota: int | None = ...,
        report_quota: int | None = ...,
        maximum_log_age: int | None = ...,
        upload: Literal["enable", "disable"] | None = ...,
        upload_destination: Literal["ftp-server"] | None = ...,
        uploadip: str | None = ...,
        uploadport: int | None = ...,
        source_ip: str | None = ...,
        uploaduser: str | None = ...,
        uploadpass: str | None = ...,
        uploaddir: str | None = ...,
        uploadtype: str | list[str] | None = ...,
        uploadsched: Literal["disable", "enable"] | None = ...,
        uploadtime: str | None = ...,
        upload_delete_files: Literal["enable", "disable"] | None = ...,
        upload_ssl_conn: Literal["default", "high", "low", "disable"] | None = ...,
        full_first_warning_threshold: int | None = ...,
        full_second_warning_threshold: int | None = ...,
        full_final_warning_threshold: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingObject: ...


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
        payload_dict: SettingPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        ips_archive: Literal["enable", "disable"] | None = ...,
        max_log_file_size: int | None = ...,
        max_policy_packet_capture_size: int | None = ...,
        roll_schedule: Literal["daily", "weekly"] | None = ...,
        roll_day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | list[str] | None = ...,
        roll_time: str | None = ...,
        diskfull: Literal["overwrite", "nolog"] | None = ...,
        log_quota: int | None = ...,
        dlp_archive_quota: int | None = ...,
        report_quota: int | None = ...,
        maximum_log_age: int | None = ...,
        upload: Literal["enable", "disable"] | None = ...,
        upload_destination: Literal["ftp-server"] | None = ...,
        uploadip: str | None = ...,
        uploadport: int | None = ...,
        source_ip: str | None = ...,
        uploaduser: str | None = ...,
        uploadpass: str | None = ...,
        uploaddir: str | None = ...,
        uploadtype: Literal["traffic", "event", "virus", "webfilter", "IPS", "emailfilter", "dlp-archive", "anomaly", "voip", "dlp", "app-ctrl", "waf", "gtp", "dns", "ssh", "ssl", "file-filter", "icap", "virtual-patch", "debug"] | list[str] | None = ...,
        uploadsched: Literal["disable", "enable"] | None = ...,
        uploadtime: str | None = ...,
        upload_delete_files: Literal["enable", "disable"] | None = ...,
        upload_ssl_conn: Literal["default", "high", "low", "disable"] | None = ...,
        full_first_warning_threshold: int | None = ...,
        full_second_warning_threshold: int | None = ...,
        full_final_warning_threshold: int | None = ...,
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
    "Setting",
    "SettingPayload",
    "SettingResponse",
    "SettingObject",
]