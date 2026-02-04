""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/setting
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

class SettingCustomlogfieldsItem(TypedDict, total=False):
    """Nested item for custom-log-fields field."""
    field_id: str


class SettingPayload(TypedDict, total=False):
    """Payload type for Setting operations."""
    resolve_ip: Literal["enable", "disable"]
    resolve_port: Literal["enable", "disable"]
    log_user_in_upper: Literal["enable", "disable"]
    fwpolicy_implicit_log: Literal["enable", "disable"]
    fwpolicy6_implicit_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    local_in_allow: Literal["enable", "disable"]
    local_in_deny_unicast: Literal["enable", "disable"]
    local_in_deny_broadcast: Literal["enable", "disable"]
    local_in_policy_log: Literal["enable", "disable"]
    local_out: Literal["enable", "disable"]
    local_out_ioc_detection: Literal["enable", "disable"]
    daemon_log: Literal["enable", "disable"]
    neighbor_event: Literal["enable", "disable"]
    brief_traffic_format: Literal["enable", "disable"]
    user_anonymize: Literal["enable", "disable"]
    expolicy_implicit_log: Literal["enable", "disable"]
    log_policy_comment: Literal["enable", "disable"]
    faz_override: Literal["enable", "disable"]
    syslog_override: Literal["enable", "disable"]
    rest_api_set: Literal["enable", "disable"]
    rest_api_get: Literal["enable", "disable"]
    rest_api_performance: Literal["enable", "disable"]
    long_live_session_stat: Literal["enable", "disable"]
    extended_utm_log: Literal["enable", "disable"]
    zone_name: Literal["enable", "disable"]
    web_svc_perf: Literal["enable", "disable"]
    custom_log_fields: str | list[str] | list[SettingCustomlogfieldsItem]
    anonymization_hash: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    resolve_ip: Literal["enable", "disable"]
    resolve_port: Literal["enable", "disable"]
    log_user_in_upper: Literal["enable", "disable"]
    fwpolicy_implicit_log: Literal["enable", "disable"]
    fwpolicy6_implicit_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    local_in_allow: Literal["enable", "disable"]
    local_in_deny_unicast: Literal["enable", "disable"]
    local_in_deny_broadcast: Literal["enable", "disable"]
    local_in_policy_log: Literal["enable", "disable"]
    local_out: Literal["enable", "disable"]
    local_out_ioc_detection: Literal["enable", "disable"]
    daemon_log: Literal["enable", "disable"]
    neighbor_event: Literal["enable", "disable"]
    brief_traffic_format: Literal["enable", "disable"]
    user_anonymize: Literal["enable", "disable"]
    expolicy_implicit_log: Literal["enable", "disable"]
    log_policy_comment: Literal["enable", "disable"]
    faz_override: Literal["enable", "disable"]
    syslog_override: Literal["enable", "disable"]
    rest_api_set: Literal["enable", "disable"]
    rest_api_get: Literal["enable", "disable"]
    rest_api_performance: Literal["enable", "disable"]
    long_live_session_stat: Literal["enable", "disable"]
    extended_utm_log: Literal["enable", "disable"]
    zone_name: Literal["enable", "disable"]
    web_svc_perf: Literal["enable", "disable"]
    custom_log_fields: list[SettingCustomlogfieldsItem]
    anonymization_hash: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingCustomlogfieldsItemObject(FortiObject[SettingCustomlogfieldsItem]):
    """Typed object for custom-log-fields table items with attribute access."""
    field_id: str


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    resolve_ip: Literal["enable", "disable"]
    resolve_port: Literal["enable", "disable"]
    log_user_in_upper: Literal["enable", "disable"]
    fwpolicy_implicit_log: Literal["enable", "disable"]
    fwpolicy6_implicit_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    local_in_allow: Literal["enable", "disable"]
    local_in_deny_unicast: Literal["enable", "disable"]
    local_in_deny_broadcast: Literal["enable", "disable"]
    local_in_policy_log: Literal["enable", "disable"]
    local_out: Literal["enable", "disable"]
    local_out_ioc_detection: Literal["enable", "disable"]
    daemon_log: Literal["enable", "disable"]
    neighbor_event: Literal["enable", "disable"]
    brief_traffic_format: Literal["enable", "disable"]
    user_anonymize: Literal["enable", "disable"]
    expolicy_implicit_log: Literal["enable", "disable"]
    log_policy_comment: Literal["enable", "disable"]
    faz_override: Literal["enable", "disable"]
    syslog_override: Literal["enable", "disable"]
    rest_api_set: Literal["enable", "disable"]
    rest_api_get: Literal["enable", "disable"]
    rest_api_performance: Literal["enable", "disable"]
    long_live_session_stat: Literal["enable", "disable"]
    extended_utm_log: Literal["enable", "disable"]
    zone_name: Literal["enable", "disable"]
    web_svc_perf: Literal["enable", "disable"]
    custom_log_fields: FortiObjectList[SettingCustomlogfieldsItemObject]
    anonymization_hash: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: log/setting
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
        resolve_ip: Literal["enable", "disable"] | None = ...,
        resolve_port: Literal["enable", "disable"] | None = ...,
        log_user_in_upper: Literal["enable", "disable"] | None = ...,
        fwpolicy_implicit_log: Literal["enable", "disable"] | None = ...,
        fwpolicy6_implicit_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        local_in_allow: Literal["enable", "disable"] | None = ...,
        local_in_deny_unicast: Literal["enable", "disable"] | None = ...,
        local_in_deny_broadcast: Literal["enable", "disable"] | None = ...,
        local_in_policy_log: Literal["enable", "disable"] | None = ...,
        local_out: Literal["enable", "disable"] | None = ...,
        local_out_ioc_detection: Literal["enable", "disable"] | None = ...,
        daemon_log: Literal["enable", "disable"] | None = ...,
        neighbor_event: Literal["enable", "disable"] | None = ...,
        brief_traffic_format: Literal["enable", "disable"] | None = ...,
        user_anonymize: Literal["enable", "disable"] | None = ...,
        expolicy_implicit_log: Literal["enable", "disable"] | None = ...,
        log_policy_comment: Literal["enable", "disable"] | None = ...,
        faz_override: Literal["enable", "disable"] | None = ...,
        syslog_override: Literal["enable", "disable"] | None = ...,
        rest_api_set: Literal["enable", "disable"] | None = ...,
        rest_api_get: Literal["enable", "disable"] | None = ...,
        rest_api_performance: Literal["enable", "disable"] | None = ...,
        long_live_session_stat: Literal["enable", "disable"] | None = ...,
        extended_utm_log: Literal["enable", "disable"] | None = ...,
        zone_name: Literal["enable", "disable"] | None = ...,
        web_svc_perf: Literal["enable", "disable"] | None = ...,
        custom_log_fields: str | list[str] | list[SettingCustomlogfieldsItem] | None = ...,
        anonymization_hash: str | None = ...,
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
        resolve_ip: Literal["enable", "disable"] | None = ...,
        resolve_port: Literal["enable", "disable"] | None = ...,
        log_user_in_upper: Literal["enable", "disable"] | None = ...,
        fwpolicy_implicit_log: Literal["enable", "disable"] | None = ...,
        fwpolicy6_implicit_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        local_in_allow: Literal["enable", "disable"] | None = ...,
        local_in_deny_unicast: Literal["enable", "disable"] | None = ...,
        local_in_deny_broadcast: Literal["enable", "disable"] | None = ...,
        local_in_policy_log: Literal["enable", "disable"] | None = ...,
        local_out: Literal["enable", "disable"] | None = ...,
        local_out_ioc_detection: Literal["enable", "disable"] | None = ...,
        daemon_log: Literal["enable", "disable"] | None = ...,
        neighbor_event: Literal["enable", "disable"] | None = ...,
        brief_traffic_format: Literal["enable", "disable"] | None = ...,
        user_anonymize: Literal["enable", "disable"] | None = ...,
        expolicy_implicit_log: Literal["enable", "disable"] | None = ...,
        log_policy_comment: Literal["enable", "disable"] | None = ...,
        faz_override: Literal["enable", "disable"] | None = ...,
        syslog_override: Literal["enable", "disable"] | None = ...,
        rest_api_set: Literal["enable", "disable"] | None = ...,
        rest_api_get: Literal["enable", "disable"] | None = ...,
        rest_api_performance: Literal["enable", "disable"] | None = ...,
        long_live_session_stat: Literal["enable", "disable"] | None = ...,
        extended_utm_log: Literal["enable", "disable"] | None = ...,
        zone_name: Literal["enable", "disable"] | None = ...,
        web_svc_perf: Literal["enable", "disable"] | None = ...,
        custom_log_fields: str | list[str] | list[SettingCustomlogfieldsItem] | None = ...,
        anonymization_hash: str | None = ...,
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