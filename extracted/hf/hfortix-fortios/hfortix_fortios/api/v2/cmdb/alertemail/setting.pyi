""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: alertemail/setting
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
    username: str
    mailto1: str
    mailto2: str
    mailto3: str
    filter_mode: Literal["category", "threshold"]
    email_interval: int
    IPS_logs: Literal["enable", "disable"]
    firewall_authentication_failure_logs: Literal["enable", "disable"]
    HA_logs: Literal["enable", "disable"]
    IPsec_errors_logs: Literal["enable", "disable"]
    FDS_update_logs: Literal["enable", "disable"]
    PPP_errors_logs: Literal["enable", "disable"]
    sslvpn_authentication_errors_logs: Literal["enable", "disable"]
    antivirus_logs: Literal["enable", "disable"]
    webfilter_logs: Literal["enable", "disable"]
    configuration_changes_logs: Literal["enable", "disable"]
    violation_traffic_logs: Literal["enable", "disable"]
    admin_login_logs: Literal["enable", "disable"]
    FDS_license_expiring_warning: Literal["enable", "disable"]
    log_disk_usage_warning: Literal["enable", "disable"]
    fortiguard_log_quota_warning: Literal["enable", "disable"]
    amc_interface_bypass_mode: Literal["enable", "disable"]
    FIPS_CC_errors: Literal["enable", "disable"]
    FSSO_disconnect_logs: Literal["enable", "disable"]
    ssh_logs: Literal["enable", "disable"]
    local_disk_usage: int
    emergency_interval: int
    alert_interval: int
    critical_interval: int
    error_interval: int
    warning_interval: int
    notification_interval: int
    information_interval: int
    debug_interval: int
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    username: str
    mailto1: str
    mailto2: str
    mailto3: str
    filter_mode: Literal["category", "threshold"]
    email_interval: int
    IPS_logs: Literal["enable", "disable"]
    firewall_authentication_failure_logs: Literal["enable", "disable"]
    HA_logs: Literal["enable", "disable"]
    IPsec_errors_logs: Literal["enable", "disable"]
    FDS_update_logs: Literal["enable", "disable"]
    PPP_errors_logs: Literal["enable", "disable"]
    sslvpn_authentication_errors_logs: Literal["enable", "disable"]
    antivirus_logs: Literal["enable", "disable"]
    webfilter_logs: Literal["enable", "disable"]
    configuration_changes_logs: Literal["enable", "disable"]
    violation_traffic_logs: Literal["enable", "disable"]
    admin_login_logs: Literal["enable", "disable"]
    FDS_license_expiring_warning: Literal["enable", "disable"]
    log_disk_usage_warning: Literal["enable", "disable"]
    fortiguard_log_quota_warning: Literal["enable", "disable"]
    amc_interface_bypass_mode: Literal["enable", "disable"]
    FIPS_CC_errors: Literal["enable", "disable"]
    FSSO_disconnect_logs: Literal["enable", "disable"]
    ssh_logs: Literal["enable", "disable"]
    local_disk_usage: int
    emergency_interval: int
    alert_interval: int
    critical_interval: int
    error_interval: int
    warning_interval: int
    notification_interval: int
    information_interval: int
    debug_interval: int
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    username: str
    mailto1: str
    mailto2: str
    mailto3: str
    filter_mode: Literal["category", "threshold"]
    email_interval: int
    IPS_logs: Literal["enable", "disable"]
    firewall_authentication_failure_logs: Literal["enable", "disable"]
    HA_logs: Literal["enable", "disable"]
    IPsec_errors_logs: Literal["enable", "disable"]
    FDS_update_logs: Literal["enable", "disable"]
    PPP_errors_logs: Literal["enable", "disable"]
    sslvpn_authentication_errors_logs: Literal["enable", "disable"]
    antivirus_logs: Literal["enable", "disable"]
    webfilter_logs: Literal["enable", "disable"]
    configuration_changes_logs: Literal["enable", "disable"]
    violation_traffic_logs: Literal["enable", "disable"]
    admin_login_logs: Literal["enable", "disable"]
    FDS_license_expiring_warning: Literal["enable", "disable"]
    log_disk_usage_warning: Literal["enable", "disable"]
    fortiguard_log_quota_warning: Literal["enable", "disable"]
    amc_interface_bypass_mode: Literal["enable", "disable"]
    FIPS_CC_errors: Literal["enable", "disable"]
    FSSO_disconnect_logs: Literal["enable", "disable"]
    ssh_logs: Literal["enable", "disable"]
    local_disk_usage: int
    emergency_interval: int
    alert_interval: int
    critical_interval: int
    error_interval: int
    warning_interval: int
    notification_interval: int
    information_interval: int
    debug_interval: int
    severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: alertemail/setting
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
        username: str | None = ...,
        mailto1: str | None = ...,
        mailto2: str | None = ...,
        mailto3: str | None = ...,
        filter_mode: Literal["category", "threshold"] | None = ...,
        email_interval: int | None = ...,
        IPS_logs: Literal["enable", "disable"] | None = ...,
        firewall_authentication_failure_logs: Literal["enable", "disable"] | None = ...,
        HA_logs: Literal["enable", "disable"] | None = ...,
        IPsec_errors_logs: Literal["enable", "disable"] | None = ...,
        FDS_update_logs: Literal["enable", "disable"] | None = ...,
        PPP_errors_logs: Literal["enable", "disable"] | None = ...,
        sslvpn_authentication_errors_logs: Literal["enable", "disable"] | None = ...,
        antivirus_logs: Literal["enable", "disable"] | None = ...,
        webfilter_logs: Literal["enable", "disable"] | None = ...,
        configuration_changes_logs: Literal["enable", "disable"] | None = ...,
        violation_traffic_logs: Literal["enable", "disable"] | None = ...,
        admin_login_logs: Literal["enable", "disable"] | None = ...,
        FDS_license_expiring_warning: Literal["enable", "disable"] | None = ...,
        log_disk_usage_warning: Literal["enable", "disable"] | None = ...,
        fortiguard_log_quota_warning: Literal["enable", "disable"] | None = ...,
        amc_interface_bypass_mode: Literal["enable", "disable"] | None = ...,
        FIPS_CC_errors: Literal["enable", "disable"] | None = ...,
        FSSO_disconnect_logs: Literal["enable", "disable"] | None = ...,
        ssh_logs: Literal["enable", "disable"] | None = ...,
        local_disk_usage: int | None = ...,
        emergency_interval: int | None = ...,
        alert_interval: int | None = ...,
        critical_interval: int | None = ...,
        error_interval: int | None = ...,
        warning_interval: int | None = ...,
        notification_interval: int | None = ...,
        information_interval: int | None = ...,
        debug_interval: int | None = ...,
        severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingObject: ...


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
        username: str | None = ...,
        mailto1: str | None = ...,
        mailto2: str | None = ...,
        mailto3: str | None = ...,
        filter_mode: Literal["category", "threshold"] | None = ...,
        email_interval: int | None = ...,
        IPS_logs: Literal["enable", "disable"] | None = ...,
        firewall_authentication_failure_logs: Literal["enable", "disable"] | None = ...,
        HA_logs: Literal["enable", "disable"] | None = ...,
        IPsec_errors_logs: Literal["enable", "disable"] | None = ...,
        FDS_update_logs: Literal["enable", "disable"] | None = ...,
        PPP_errors_logs: Literal["enable", "disable"] | None = ...,
        sslvpn_authentication_errors_logs: Literal["enable", "disable"] | None = ...,
        antivirus_logs: Literal["enable", "disable"] | None = ...,
        webfilter_logs: Literal["enable", "disable"] | None = ...,
        configuration_changes_logs: Literal["enable", "disable"] | None = ...,
        violation_traffic_logs: Literal["enable", "disable"] | None = ...,
        admin_login_logs: Literal["enable", "disable"] | None = ...,
        FDS_license_expiring_warning: Literal["enable", "disable"] | None = ...,
        log_disk_usage_warning: Literal["enable", "disable"] | None = ...,
        fortiguard_log_quota_warning: Literal["enable", "disable"] | None = ...,
        amc_interface_bypass_mode: Literal["enable", "disable"] | None = ...,
        FIPS_CC_errors: Literal["enable", "disable"] | None = ...,
        FSSO_disconnect_logs: Literal["enable", "disable"] | None = ...,
        ssh_logs: Literal["enable", "disable"] | None = ...,
        local_disk_usage: int | None = ...,
        emergency_interval: int | None = ...,
        alert_interval: int | None = ...,
        critical_interval: int | None = ...,
        error_interval: int | None = ...,
        warning_interval: int | None = ...,
        notification_interval: int | None = ...,
        information_interval: int | None = ...,
        debug_interval: int | None = ...,
        severity: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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