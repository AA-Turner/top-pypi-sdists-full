""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/device_upgrade
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

class DeviceUpgradeKnownhamembersItem(TypedDict, total=False):
    """Nested item for known-ha-members field."""
    serial: str


class DeviceUpgradePayload(TypedDict, total=False):
    """Payload type for DeviceUpgrade operations."""
    vdom: str
    status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"]
    ha_reboot_controller: str
    next_path_index: int
    known_ha_members: str | list[str] | list[DeviceUpgradeKnownhamembersItem]
    initial_version: str
    starter_admin: str
    serial: str
    timing: Literal["immediate", "scheduled"]
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"]
    allow_download: Literal["enable", "disable"]
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DeviceUpgradeResponse(TypedDict, total=False):
    """Response type for DeviceUpgrade - use with .dict property for typed dict access."""
    vdom: str
    status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"]
    ha_reboot_controller: str
    next_path_index: int
    known_ha_members: list[DeviceUpgradeKnownhamembersItem]
    initial_version: str
    starter_admin: str
    serial: str
    timing: Literal["immediate", "scheduled"]
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"]
    allow_download: Literal["enable", "disable"]
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DeviceUpgradeKnownhamembersItemObject(FortiObject[DeviceUpgradeKnownhamembersItem]):
    """Typed object for known-ha-members table items with attribute access."""
    serial: str


class DeviceUpgradeObject(FortiObject):
    """Typed FortiObject for DeviceUpgrade with field access."""
    status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"]
    ha_reboot_controller: str
    next_path_index: int
    known_ha_members: FortiObjectList[DeviceUpgradeKnownhamembersItemObject]
    initial_version: str
    starter_admin: str
    timing: Literal["immediate", "scheduled"]
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"]
    allow_download: Literal["enable", "disable"]
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]


# ================================================================
# Main Endpoint Class
# ================================================================

class DeviceUpgrade:
    """
    
    Endpoint: system/device_upgrade
    Category: cmdb
    MKey: serial
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
        serial: str,
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
    ) -> DeviceUpgradeObject: ...
    
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[DeviceUpgradeObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: DeviceUpgradePayload | None = ...,
        status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"] | None = ...,
        ha_reboot_controller: str | None = ...,
        next_path_index: int | None = ...,
        known_ha_members: str | list[str] | list[DeviceUpgradeKnownhamembersItem] | None = ...,
        initial_version: str | None = ...,
        starter_admin: str | None = ...,
        serial: str | None = ...,
        timing: Literal["immediate", "scheduled"] | None = ...,
        maximum_minutes: int | None = ...,
        time: str | None = ...,
        setup_time: str | None = ...,
        upgrade_path: str | None = ...,
        device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"] | None = ...,
        allow_download: Literal["enable", "disable"] | None = ...,
        failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DeviceUpgradeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DeviceUpgradePayload | None = ...,
        status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"] | None = ...,
        ha_reboot_controller: str | None = ...,
        next_path_index: int | None = ...,
        known_ha_members: str | list[str] | list[DeviceUpgradeKnownhamembersItem] | None = ...,
        initial_version: str | None = ...,
        starter_admin: str | None = ...,
        serial: str | None = ...,
        timing: Literal["immediate", "scheduled"] | None = ...,
        maximum_minutes: int | None = ...,
        time: str | None = ...,
        setup_time: str | None = ...,
        upgrade_path: str | None = ...,
        device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"] | None = ...,
        allow_download: Literal["enable", "disable"] | None = ...,
        failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DeviceUpgradeObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        serial: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        serial: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DeviceUpgradePayload | None = ...,
        status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"] | None = ...,
        ha_reboot_controller: str | None = ...,
        next_path_index: int | None = ...,
        known_ha_members: str | list[str] | list[DeviceUpgradeKnownhamembersItem] | None = ...,
        initial_version: str | None = ...,
        starter_admin: str | None = ...,
        serial: str | None = ...,
        timing: Literal["immediate", "scheduled"] | None = ...,
        maximum_minutes: int | None = ...,
        time: str | None = ...,
        setup_time: str | None = ...,
        upgrade_path: str | None = ...,
        device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"] | None = ...,
        allow_download: Literal["enable", "disable"] | None = ...,
        failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"] | None = ...,
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
    "DeviceUpgrade",
    "DeviceUpgradePayload",
    "DeviceUpgradeResponse",
    "DeviceUpgradeObject",
]