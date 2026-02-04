""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ipam
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

class IpamPoolsExcludeItem(TypedDict, total=False):
    """Nested item for pools.exclude field."""
    ID: int
    exclude_subnet: str


class IpamRulesDeviceItem(TypedDict, total=False):
    """Nested item for rules.device field."""
    name: str


class IpamRulesInterfaceItem(TypedDict, total=False):
    """Nested item for rules.interface field."""
    name: str


class IpamRulesPoolItem(TypedDict, total=False):
    """Nested item for rules.pool field."""
    name: str


class IpamPoolsItem(TypedDict, total=False):
    """Nested item for pools field."""
    name: str
    description: str
    subnet: str
    exclude: str | list[str] | list[IpamPoolsExcludeItem]


class IpamRulesItem(TypedDict, total=False):
    """Nested item for rules field."""
    name: str
    description: str
    device: str | list[str] | list[IpamRulesDeviceItem]
    interface: str | list[str] | list[IpamRulesInterfaceItem]
    role: Literal["any", "lan", "wan", "dmz", "undefined"]
    pool: str | list[str] | list[IpamRulesPoolItem]
    dhcp: Literal["enable", "disable"]


class IpamPayload(TypedDict, total=False):
    """Payload type for Ipam operations."""
    status: Literal["enable", "disable"]
    server_type: Literal["fabric-root"]
    automatic_conflict_resolution: Literal["disable", "enable"]
    require_subnet_size_match: Literal["disable", "enable"]
    manage_lan_addresses: Literal["disable", "enable"]
    manage_lan_extension_addresses: Literal["disable", "enable"]
    manage_ssid_addresses: Literal["disable", "enable"]
    pools: str | list[str] | list[IpamPoolsItem]
    rules: str | list[str] | list[IpamRulesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IpamResponse(TypedDict, total=False):
    """Response type for Ipam - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    server_type: Literal["fabric-root"]
    automatic_conflict_resolution: Literal["disable", "enable"]
    require_subnet_size_match: Literal["disable", "enable"]
    manage_lan_addresses: Literal["disable", "enable"]
    manage_lan_extension_addresses: Literal["disable", "enable"]
    manage_ssid_addresses: Literal["disable", "enable"]
    pools: list[IpamPoolsItem]
    rules: list[IpamRulesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IpamPoolsExcludeItemObject(FortiObject[IpamPoolsExcludeItem]):
    """Typed object for pools.exclude table items with attribute access."""
    ID: int
    exclude_subnet: str


class IpamRulesDeviceItemObject(FortiObject[IpamRulesDeviceItem]):
    """Typed object for rules.device table items with attribute access."""
    name: str


class IpamRulesInterfaceItemObject(FortiObject[IpamRulesInterfaceItem]):
    """Typed object for rules.interface table items with attribute access."""
    name: str


class IpamRulesPoolItemObject(FortiObject[IpamRulesPoolItem]):
    """Typed object for rules.pool table items with attribute access."""
    name: str


class IpamPoolsItemObject(FortiObject[IpamPoolsItem]):
    """Typed object for pools table items with attribute access."""
    name: str
    description: str
    subnet: str
    exclude: FortiObjectList[IpamPoolsExcludeItemObject]


class IpamRulesItemObject(FortiObject[IpamRulesItem]):
    """Typed object for rules table items with attribute access."""
    name: str
    description: str
    device: FortiObjectList[IpamRulesDeviceItemObject]
    interface: FortiObjectList[IpamRulesInterfaceItemObject]
    role: Literal["any", "lan", "wan", "dmz", "undefined"]
    pool: FortiObjectList[IpamRulesPoolItemObject]
    dhcp: Literal["enable", "disable"]


class IpamObject(FortiObject):
    """Typed FortiObject for Ipam with field access."""
    status: Literal["enable", "disable"]
    server_type: Literal["fabric-root"]
    automatic_conflict_resolution: Literal["disable", "enable"]
    require_subnet_size_match: Literal["disable", "enable"]
    manage_lan_addresses: Literal["disable", "enable"]
    manage_lan_extension_addresses: Literal["disable", "enable"]
    manage_ssid_addresses: Literal["disable", "enable"]
    pools: FortiObjectList[IpamPoolsItemObject]
    rules: FortiObjectList[IpamRulesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ipam:
    """
    
    Endpoint: system/ipam
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
    ) -> IpamObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[IpamPoolsItem] | None = ...,
        rules: str | list[str] | list[IpamRulesItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IpamObject: ...


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
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[IpamPoolsItem] | None = ...,
        rules: str | list[str] | list[IpamRulesItem] | None = ...,
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
    "Ipam",
    "IpamPayload",
    "IpamResponse",
    "IpamObject",
]