""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/automation_trigger
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class AutomationTriggerVdomItem(TypedDict, total=False):
    """Nested item for vdom field."""
    name: str


class AutomationTriggerLogidItem(TypedDict, total=False):
    """Nested item for logid field."""
    id: int


class AutomationTriggerFieldsItem(TypedDict, total=False):
    """Nested item for fields field."""
    id: int
    name: str
    value: str


class AutomationTriggerPayload(TypedDict, total=False):
    """Payload type for AutomationTrigger operations."""
    name: str
    description: str
    trigger_type: Literal["event-based", "scheduled"]
    event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"]
    vdom: str | list[str] | list[AutomationTriggerVdomItem]
    license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"]
    report_type: Literal["posture", "coverage", "optimization", "any"]
    stitch_name: str
    logid: str | list[str] | list[AutomationTriggerLogidItem]
    trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"]
    trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    trigger_day: int
    trigger_hour: int
    trigger_minute: int
    trigger_datetime: str
    fields: str | list[str] | list[AutomationTriggerFieldsItem]
    faz_event_name: str
    faz_event_severity: str
    faz_event_tags: str
    serial: str
    fabric_event_name: str
    fabric_event_severity: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AutomationTriggerResponse(TypedDict, total=False):
    """Response type for AutomationTrigger - use with .dict property for typed dict access."""
    name: str
    description: str
    trigger_type: Literal["event-based", "scheduled"]
    event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"]
    vdom: list[AutomationTriggerVdomItem]
    license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"]
    report_type: Literal["posture", "coverage", "optimization", "any"]
    stitch_name: str
    logid: list[AutomationTriggerLogidItem]
    trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"]
    trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    trigger_day: int
    trigger_hour: int
    trigger_minute: int
    trigger_datetime: str
    fields: list[AutomationTriggerFieldsItem]
    faz_event_name: str
    faz_event_severity: str
    faz_event_tags: str
    serial: str
    fabric_event_name: str
    fabric_event_severity: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AutomationTriggerVdomItemObject(FortiObject[AutomationTriggerVdomItem]):
    """Typed object for vdom table items with attribute access."""
    name: str


class AutomationTriggerLogidItemObject(FortiObject[AutomationTriggerLogidItem]):
    """Typed object for logid table items with attribute access."""
    id: int


class AutomationTriggerFieldsItemObject(FortiObject[AutomationTriggerFieldsItem]):
    """Typed object for fields table items with attribute access."""
    id: int
    name: str
    value: str


class AutomationTriggerObject(FortiObject):
    """Typed FortiObject for AutomationTrigger with field access."""
    name: str
    description: str
    trigger_type: Literal["event-based", "scheduled"]
    event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"]
    license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"]
    report_type: Literal["posture", "coverage", "optimization", "any"]
    stitch_name: str
    logid: FortiObjectList[AutomationTriggerLogidItemObject]
    trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"]
    trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    trigger_day: int
    trigger_hour: int
    trigger_minute: int
    trigger_datetime: str
    fields: FortiObjectList[AutomationTriggerFieldsItemObject]
    faz_event_name: str
    faz_event_severity: str
    faz_event_tags: str
    fabric_event_name: str
    fabric_event_severity: str


# ================================================================
# Main Endpoint Class
# ================================================================

class AutomationTrigger:
    """
    
    Endpoint: system/automation_trigger
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
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
    ) -> AutomationTriggerObject: ...
    
    @overload
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
    ) -> FortiObjectList[AutomationTriggerObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[AutomationTriggerLogidItem] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[AutomationTriggerFieldsItem] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutomationTriggerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[AutomationTriggerLogidItem] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[AutomationTriggerFieldsItem] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutomationTriggerObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[AutomationTriggerLogidItem] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[AutomationTriggerFieldsItem] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
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
    "AutomationTrigger",
    "AutomationTriggerPayload",
    "AutomationTriggerResponse",
    "AutomationTriggerObject",
]