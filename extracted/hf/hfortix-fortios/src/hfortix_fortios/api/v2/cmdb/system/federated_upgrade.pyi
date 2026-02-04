""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/federated_upgrade
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

class FederatedUpgradeKnownhamembersItem(TypedDict, total=False):
    """Nested item for known-ha-members field."""
    serial: str


class FederatedUpgradeNodelistItem(TypedDict, total=False):
    """Nested item for node-list field."""
    serial: str
    timing: Literal["immediate", "scheduled"]
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"]
    allow_download: Literal["enable", "disable"]
    coordinating_fortigate: str
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]


class FederatedUpgradePayload(TypedDict, total=False):
    """Payload type for FederatedUpgrade operations."""
    status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"]
    source: Literal["user", "auto-firmware-upgrade", "forced-upgrade"]
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]
    failure_device: str
    upgrade_id: int
    next_path_index: int
    ignore_signing_errors: Literal["enable", "disable"]
    ha_reboot_controller: str
    known_ha_members: str | list[str] | list[FederatedUpgradeKnownhamembersItem]
    initial_version: str
    starter_admin: str
    node_list: str | list[str] | list[FederatedUpgradeNodelistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FederatedUpgradeResponse(TypedDict, total=False):
    """Response type for FederatedUpgrade - use with .dict property for typed dict access."""
    status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"]
    source: Literal["user", "auto-firmware-upgrade", "forced-upgrade"]
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]
    failure_device: str
    upgrade_id: int
    next_path_index: int
    ignore_signing_errors: Literal["enable", "disable"]
    ha_reboot_controller: str
    known_ha_members: list[FederatedUpgradeKnownhamembersItem]
    initial_version: str
    starter_admin: str
    node_list: list[FederatedUpgradeNodelistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FederatedUpgradeKnownhamembersItemObject(FortiObject[FederatedUpgradeKnownhamembersItem]):
    """Typed object for known-ha-members table items with attribute access."""
    serial: str


class FederatedUpgradeNodelistItemObject(FortiObject[FederatedUpgradeNodelistItem]):
    """Typed object for node-list table items with attribute access."""
    serial: str
    timing: Literal["immediate", "scheduled"]
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: Literal["fortigate", "fortiswitch", "fortiap", "fortiextender"]
    allow_download: Literal["enable", "disable"]
    coordinating_fortigate: str
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]


class FederatedUpgradeObject(FortiObject):
    """Typed FortiObject for FederatedUpgrade with field access."""
    status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"]
    source: Literal["user", "auto-firmware-upgrade", "forced-upgrade"]
    failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"]
    failure_device: str
    upgrade_id: int
    next_path_index: int
    ignore_signing_errors: Literal["enable", "disable"]
    ha_reboot_controller: str
    known_ha_members: FortiObjectList[FederatedUpgradeKnownhamembersItemObject]
    initial_version: str
    starter_admin: str
    node_list: FortiObjectList[FederatedUpgradeNodelistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class FederatedUpgrade:
    """
    
    Endpoint: system/federated_upgrade
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
    ) -> FederatedUpgradeObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FederatedUpgradePayload | None = ...,
        status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"] | None = ...,
        source: Literal["user", "auto-firmware-upgrade", "forced-upgrade"] | None = ...,
        failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"] | None = ...,
        failure_device: str | None = ...,
        upgrade_id: int | None = ...,
        next_path_index: int | None = ...,
        ignore_signing_errors: Literal["enable", "disable"] | None = ...,
        ha_reboot_controller: str | None = ...,
        known_ha_members: str | list[str] | list[FederatedUpgradeKnownhamembersItem] | None = ...,
        initial_version: str | None = ...,
        starter_admin: str | None = ...,
        node_list: str | list[str] | list[FederatedUpgradeNodelistItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FederatedUpgradeObject: ...


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
        payload_dict: FederatedUpgradePayload | None = ...,
        status: Literal["disabled", "initialized", "downloading", "device-disconnected", "ready", "coordinating", "staging", "final-check", "upgrade-devices", "cancelled", "confirmed", "done", "failed"] | None = ...,
        source: Literal["user", "auto-firmware-upgrade", "forced-upgrade"] | None = ...,
        failure_reason: Literal["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"] | None = ...,
        failure_device: str | None = ...,
        upgrade_id: int | None = ...,
        next_path_index: int | None = ...,
        ignore_signing_errors: Literal["enable", "disable"] | None = ...,
        ha_reboot_controller: str | None = ...,
        known_ha_members: str | list[str] | list[FederatedUpgradeKnownhamembersItem] | None = ...,
        initial_version: str | None = ...,
        starter_admin: str | None = ...,
        node_list: str | list[str] | list[FederatedUpgradeNodelistItem] | None = ...,
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
    "FederatedUpgrade",
    "FederatedUpgradePayload",
    "FederatedUpgradeResponse",
    "FederatedUpgradeObject",
]