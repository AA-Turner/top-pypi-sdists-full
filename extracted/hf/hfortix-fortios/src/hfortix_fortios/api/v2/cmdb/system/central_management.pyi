""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/central_management
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

class CentralManagementServerlistItem(TypedDict, total=False):
    """Nested item for server-list field."""
    id: int
    server_type: Literal["update", "rating", "vpatch-query", "iot-collect"]
    addr_type: Literal["ipv4", "ipv6", "fqdn"]
    server_address: str
    server_address6: str
    fqdn: str


class CentralManagementPayload(TypedDict, total=False):
    """Payload type for CentralManagement operations."""
    mode: Literal["normal", "backup"]
    type: Literal["fortimanager", "fortiguard", "none"]
    fortigate_cloud_sso_default_profile: str
    schedule_config_restore: Literal["enable", "disable"]
    schedule_script_restore: Literal["enable", "disable"]
    allow_push_configuration: Literal["enable", "disable"]
    allow_push_firmware: Literal["enable", "disable"]
    allow_remote_firmware_upgrade: Literal["enable", "disable"]
    allow_monitor: Literal["enable", "disable"]
    serial_number: str
    fmg: str
    fmg_source_ip: str
    fmg_source_ip6: str
    local_cert: str
    ca_cert: str
    vdom: str
    server_list: str | list[str] | list[CentralManagementServerlistItem]
    fmg_update_port: Literal["8890", "443"]
    fmg_update_http_header: Literal["enable", "disable"]
    include_default_servers: Literal["enable", "disable"]
    enc_algorithm: Literal["default", "high", "low"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CentralManagementResponse(TypedDict, total=False):
    """Response type for CentralManagement - use with .dict property for typed dict access."""
    mode: Literal["normal", "backup"]
    type: Literal["fortimanager", "fortiguard", "none"]
    fortigate_cloud_sso_default_profile: str
    schedule_config_restore: Literal["enable", "disable"]
    schedule_script_restore: Literal["enable", "disable"]
    allow_push_configuration: Literal["enable", "disable"]
    allow_push_firmware: Literal["enable", "disable"]
    allow_remote_firmware_upgrade: Literal["enable", "disable"]
    allow_monitor: Literal["enable", "disable"]
    serial_number: str
    fmg: str
    fmg_source_ip: str
    fmg_source_ip6: str
    local_cert: str
    ca_cert: str
    vdom: str
    server_list: list[CentralManagementServerlistItem]
    fmg_update_port: Literal["8890", "443"]
    fmg_update_http_header: Literal["enable", "disable"]
    include_default_servers: Literal["enable", "disable"]
    enc_algorithm: Literal["default", "high", "low"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CentralManagementServerlistItemObject(FortiObject[CentralManagementServerlistItem]):
    """Typed object for server-list table items with attribute access."""
    id: int
    server_type: Literal["update", "rating", "vpatch-query", "iot-collect"]
    addr_type: Literal["ipv4", "ipv6", "fqdn"]
    server_address: str
    server_address6: str
    fqdn: str


class CentralManagementObject(FortiObject):
    """Typed FortiObject for CentralManagement with field access."""
    mode: Literal["normal", "backup"]
    type: Literal["fortimanager", "fortiguard", "none"]
    fortigate_cloud_sso_default_profile: str
    schedule_config_restore: Literal["enable", "disable"]
    schedule_script_restore: Literal["enable", "disable"]
    allow_push_configuration: Literal["enable", "disable"]
    allow_push_firmware: Literal["enable", "disable"]
    allow_remote_firmware_upgrade: Literal["enable", "disable"]
    allow_monitor: Literal["enable", "disable"]
    serial_number: str
    fmg: str
    fmg_source_ip: str
    fmg_source_ip6: str
    local_cert: str
    ca_cert: str
    server_list: FortiObjectList[CentralManagementServerlistItemObject]
    fmg_update_port: Literal["8890", "443"]
    fmg_update_http_header: Literal["enable", "disable"]
    include_default_servers: Literal["enable", "disable"]
    enc_algorithm: Literal["default", "high", "low"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class CentralManagement:
    """
    
    Endpoint: system/central_management
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
    ) -> CentralManagementObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CentralManagementPayload | None = ...,
        mode: Literal["normal", "backup"] | None = ...,
        type: Literal["fortimanager", "fortiguard", "none"] | None = ...,
        fortigate_cloud_sso_default_profile: str | None = ...,
        schedule_config_restore: Literal["enable", "disable"] | None = ...,
        schedule_script_restore: Literal["enable", "disable"] | None = ...,
        allow_push_configuration: Literal["enable", "disable"] | None = ...,
        allow_push_firmware: Literal["enable", "disable"] | None = ...,
        allow_remote_firmware_upgrade: Literal["enable", "disable"] | None = ...,
        allow_monitor: Literal["enable", "disable"] | None = ...,
        serial_number: str | None = ...,
        fmg: str | None = ...,
        fmg_source_ip: str | None = ...,
        fmg_source_ip6: str | None = ...,
        local_cert: str | None = ...,
        ca_cert: str | None = ...,
        server_list: str | list[str] | list[CentralManagementServerlistItem] | None = ...,
        fmg_update_port: Literal["8890", "443"] | None = ...,
        fmg_update_http_header: Literal["enable", "disable"] | None = ...,
        include_default_servers: Literal["enable", "disable"] | None = ...,
        enc_algorithm: Literal["default", "high", "low"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CentralManagementObject: ...


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
        payload_dict: CentralManagementPayload | None = ...,
        mode: Literal["normal", "backup"] | None = ...,
        type: Literal["fortimanager", "fortiguard", "none"] | None = ...,
        fortigate_cloud_sso_default_profile: str | None = ...,
        schedule_config_restore: Literal["enable", "disable"] | None = ...,
        schedule_script_restore: Literal["enable", "disable"] | None = ...,
        allow_push_configuration: Literal["enable", "disable"] | None = ...,
        allow_push_firmware: Literal["enable", "disable"] | None = ...,
        allow_remote_firmware_upgrade: Literal["enable", "disable"] | None = ...,
        allow_monitor: Literal["enable", "disable"] | None = ...,
        serial_number: str | None = ...,
        fmg: str | None = ...,
        fmg_source_ip: str | None = ...,
        fmg_source_ip6: str | None = ...,
        local_cert: str | None = ...,
        ca_cert: str | None = ...,
        server_list: str | list[str] | list[CentralManagementServerlistItem] | None = ...,
        fmg_update_port: Literal["8890", "443"] | None = ...,
        fmg_update_http_header: Literal["enable", "disable"] | None = ...,
        include_default_servers: Literal["enable", "disable"] | None = ...,
        enc_algorithm: Literal["default", "high", "low"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
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
    "CentralManagement",
    "CentralManagementPayload",
    "CentralManagementResponse",
    "CentralManagementObject",
]