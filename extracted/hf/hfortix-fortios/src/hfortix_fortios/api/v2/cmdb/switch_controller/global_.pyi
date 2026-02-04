""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/global_
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

class GlobalDisablediscoveryItem(TypedDict, total=False):
    """Nested item for disable-discovery field."""
    name: str


class GlobalCustomcommandItem(TypedDict, total=False):
    """Nested item for custom-command field."""
    command_entry: str
    command_name: str


class GlobalPayload(TypedDict, total=False):
    """Payload type for Global operations."""
    mac_aging_interval: int
    https_image_push: Literal["enable", "disable"]
    vlan_all_mode: Literal["all", "defined"]
    vlan_optimization: Literal["prune", "configured", "none"]
    vlan_identity: Literal["description", "name"]
    disable_discovery: str | list[str] | list[GlobalDisablediscoveryItem]
    mac_retention_period: int
    default_virtual_switch_vlan: str
    dhcp_server_access_list: Literal["enable", "disable"]
    dhcp_option82_format: Literal["ascii", "legacy"]
    dhcp_option82_circuit_id: str | list[str]
    dhcp_option82_remote_id: str | list[str]
    dhcp_snoop_client_req: Literal["drop-untrusted", "forward-untrusted"]
    dhcp_snoop_client_db_exp: int
    dhcp_snoop_db_per_port_learn_limit: int
    log_mac_limit_violations: Literal["enable", "disable"]
    mac_violation_timer: int
    sn_dns_resolution: Literal["enable", "disable"]
    mac_event_logging: Literal["enable", "disable"]
    bounce_quarantined_link: Literal["disable", "enable"]
    quarantine_mode: Literal["by-vlan", "by-redirect"]
    update_user_device: str | list[str]
    custom_command: str | list[str] | list[GlobalCustomcommandItem]
    fips_enforce: Literal["disable", "enable"]
    firmware_provision_on_authorization: Literal["enable", "disable"]
    switch_on_deauth: Literal["no-op", "factory-reset"]
    firewall_auth_user_hold_period: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GlobalResponse(TypedDict, total=False):
    """Response type for Global - use with .dict property for typed dict access."""
    mac_aging_interval: int
    https_image_push: Literal["enable", "disable"]
    vlan_all_mode: Literal["all", "defined"]
    vlan_optimization: Literal["prune", "configured", "none"]
    vlan_identity: Literal["description", "name"]
    disable_discovery: list[GlobalDisablediscoveryItem]
    mac_retention_period: int
    default_virtual_switch_vlan: str
    dhcp_server_access_list: Literal["enable", "disable"]
    dhcp_option82_format: Literal["ascii", "legacy"]
    dhcp_option82_circuit_id: str
    dhcp_option82_remote_id: str
    dhcp_snoop_client_req: Literal["drop-untrusted", "forward-untrusted"]
    dhcp_snoop_client_db_exp: int
    dhcp_snoop_db_per_port_learn_limit: int
    log_mac_limit_violations: Literal["enable", "disable"]
    mac_violation_timer: int
    sn_dns_resolution: Literal["enable", "disable"]
    mac_event_logging: Literal["enable", "disable"]
    bounce_quarantined_link: Literal["disable", "enable"]
    quarantine_mode: Literal["by-vlan", "by-redirect"]
    update_user_device: str
    custom_command: list[GlobalCustomcommandItem]
    fips_enforce: Literal["disable", "enable"]
    firmware_provision_on_authorization: Literal["enable", "disable"]
    switch_on_deauth: Literal["no-op", "factory-reset"]
    firewall_auth_user_hold_period: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GlobalDisablediscoveryItemObject(FortiObject[GlobalDisablediscoveryItem]):
    """Typed object for disable-discovery table items with attribute access."""
    name: str


class GlobalCustomcommandItemObject(FortiObject[GlobalCustomcommandItem]):
    """Typed object for custom-command table items with attribute access."""
    command_entry: str
    command_name: str


class GlobalObject(FortiObject):
    """Typed FortiObject for Global with field access."""
    mac_aging_interval: int
    https_image_push: Literal["enable", "disable"]
    vlan_all_mode: Literal["all", "defined"]
    vlan_optimization: Literal["prune", "configured", "none"]
    vlan_identity: Literal["description", "name"]
    disable_discovery: FortiObjectList[GlobalDisablediscoveryItemObject]
    mac_retention_period: int
    default_virtual_switch_vlan: str
    dhcp_server_access_list: Literal["enable", "disable"]
    dhcp_option82_format: Literal["ascii", "legacy"]
    dhcp_option82_circuit_id: str
    dhcp_option82_remote_id: str
    dhcp_snoop_client_req: Literal["drop-untrusted", "forward-untrusted"]
    dhcp_snoop_client_db_exp: int
    dhcp_snoop_db_per_port_learn_limit: int
    log_mac_limit_violations: Literal["enable", "disable"]
    mac_violation_timer: int
    sn_dns_resolution: Literal["enable", "disable"]
    mac_event_logging: Literal["enable", "disable"]
    bounce_quarantined_link: Literal["disable", "enable"]
    quarantine_mode: Literal["by-vlan", "by-redirect"]
    update_user_device: str
    custom_command: FortiObjectList[GlobalCustomcommandItemObject]
    fips_enforce: Literal["disable", "enable"]
    firmware_provision_on_authorization: Literal["enable", "disable"]
    switch_on_deauth: Literal["no-op", "factory-reset"]
    firewall_auth_user_hold_period: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Global:
    """
    
    Endpoint: switch_controller/global_
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
    ) -> GlobalObject: ...
    
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
        payload_dict: GlobalPayload | None = ...,
        mac_aging_interval: int | None = ...,
        https_image_push: Literal["enable", "disable"] | None = ...,
        vlan_all_mode: Literal["all", "defined"] | None = ...,
        vlan_optimization: Literal["prune", "configured", "none"] | None = ...,
        vlan_identity: Literal["description", "name"] | None = ...,
        disable_discovery: str | list[str] | list[GlobalDisablediscoveryItem] | None = ...,
        mac_retention_period: int | None = ...,
        default_virtual_switch_vlan: str | None = ...,
        dhcp_server_access_list: Literal["enable", "disable"] | None = ...,
        dhcp_option82_format: Literal["ascii", "legacy"] | None = ...,
        dhcp_option82_circuit_id: str | list[str] | None = ...,
        dhcp_option82_remote_id: str | list[str] | None = ...,
        dhcp_snoop_client_req: Literal["drop-untrusted", "forward-untrusted"] | None = ...,
        dhcp_snoop_client_db_exp: int | None = ...,
        dhcp_snoop_db_per_port_learn_limit: int | None = ...,
        log_mac_limit_violations: Literal["enable", "disable"] | None = ...,
        mac_violation_timer: int | None = ...,
        sn_dns_resolution: Literal["enable", "disable"] | None = ...,
        mac_event_logging: Literal["enable", "disable"] | None = ...,
        bounce_quarantined_link: Literal["disable", "enable"] | None = ...,
        quarantine_mode: Literal["by-vlan", "by-redirect"] | None = ...,
        update_user_device: str | list[str] | None = ...,
        custom_command: str | list[str] | list[GlobalCustomcommandItem] | None = ...,
        fips_enforce: Literal["disable", "enable"] | None = ...,
        firmware_provision_on_authorization: Literal["enable", "disable"] | None = ...,
        switch_on_deauth: Literal["no-op", "factory-reset"] | None = ...,
        firewall_auth_user_hold_period: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GlobalObject: ...


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
        payload_dict: GlobalPayload | None = ...,
        mac_aging_interval: int | None = ...,
        https_image_push: Literal["enable", "disable"] | None = ...,
        vlan_all_mode: Literal["all", "defined"] | None = ...,
        vlan_optimization: Literal["prune", "configured", "none"] | None = ...,
        vlan_identity: Literal["description", "name"] | None = ...,
        disable_discovery: str | list[str] | list[GlobalDisablediscoveryItem] | None = ...,
        mac_retention_period: int | None = ...,
        default_virtual_switch_vlan: str | None = ...,
        dhcp_server_access_list: Literal["enable", "disable"] | None = ...,
        dhcp_option82_format: Literal["ascii", "legacy"] | None = ...,
        dhcp_option82_circuit_id: Literal["intfname", "vlan", "hostname", "mode", "description"] | list[str] | None = ...,
        dhcp_option82_remote_id: Literal["mac", "hostname", "ip"] | list[str] | None = ...,
        dhcp_snoop_client_req: Literal["drop-untrusted", "forward-untrusted"] | None = ...,
        dhcp_snoop_client_db_exp: int | None = ...,
        dhcp_snoop_db_per_port_learn_limit: int | None = ...,
        log_mac_limit_violations: Literal["enable", "disable"] | None = ...,
        mac_violation_timer: int | None = ...,
        sn_dns_resolution: Literal["enable", "disable"] | None = ...,
        mac_event_logging: Literal["enable", "disable"] | None = ...,
        bounce_quarantined_link: Literal["disable", "enable"] | None = ...,
        quarantine_mode: Literal["by-vlan", "by-redirect"] | None = ...,
        update_user_device: Literal["mac-cache", "lldp", "dhcp-snooping", "l2-db", "l3-db"] | list[str] | None = ...,
        custom_command: str | list[str] | list[GlobalCustomcommandItem] | None = ...,
        fips_enforce: Literal["disable", "enable"] | None = ...,
        firmware_provision_on_authorization: Literal["enable", "disable"] | None = ...,
        switch_on_deauth: Literal["no-op", "factory-reset"] | None = ...,
        firewall_auth_user_hold_period: int | None = ...,
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
    "Global",
    "GlobalPayload",
    "GlobalResponse",
    "GlobalObject",
]