""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/resource_limits
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

class ResourceLimitsPayload(TypedDict, total=False):
    """Payload type for ResourceLimits operations."""
    session: int
    ipsec_phase1: int
    ipsec_phase2: int
    ipsec_phase1_interface: int
    ipsec_phase2_interface: int
    dialup_tunnel: int
    firewall_policy: int
    firewall_address: int
    firewall_addrgrp: int
    custom_service: int
    service_group: int
    onetime_schedule: int
    recurring_schedule: int
    user: int
    user_group: int
    sslvpn: int
    proxy: int
    log_disk_quota: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ResourceLimitsResponse(TypedDict, total=False):
    """Response type for ResourceLimits - use with .dict property for typed dict access."""
    session: int
    ipsec_phase1: int
    ipsec_phase2: int
    ipsec_phase1_interface: int
    ipsec_phase2_interface: int
    dialup_tunnel: int
    firewall_policy: int
    firewall_address: int
    firewall_addrgrp: int
    custom_service: int
    service_group: int
    onetime_schedule: int
    recurring_schedule: int
    user: int
    user_group: int
    sslvpn: int
    proxy: int
    log_disk_quota: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ResourceLimitsObject(FortiObject):
    """Typed FortiObject for ResourceLimits with field access."""
    session: int
    ipsec_phase1: int
    ipsec_phase2: int
    ipsec_phase1_interface: int
    ipsec_phase2_interface: int
    dialup_tunnel: int
    firewall_policy: int
    firewall_address: int
    firewall_addrgrp: int
    custom_service: int
    service_group: int
    onetime_schedule: int
    recurring_schedule: int
    user: int
    user_group: int
    sslvpn: int
    proxy: int
    log_disk_quota: int


# ================================================================
# Main Endpoint Class
# ================================================================

class ResourceLimits:
    """
    
    Endpoint: system/resource_limits
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
    ) -> ResourceLimitsObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ResourceLimitsPayload | None = ...,
        session: int | None = ...,
        ipsec_phase1: int | None = ...,
        ipsec_phase2: int | None = ...,
        ipsec_phase1_interface: int | None = ...,
        ipsec_phase2_interface: int | None = ...,
        dialup_tunnel: int | None = ...,
        firewall_policy: int | None = ...,
        firewall_address: int | None = ...,
        firewall_addrgrp: int | None = ...,
        custom_service: int | None = ...,
        service_group: int | None = ...,
        onetime_schedule: int | None = ...,
        recurring_schedule: int | None = ...,
        user: int | None = ...,
        user_group: int | None = ...,
        sslvpn: int | None = ...,
        proxy: int | None = ...,
        log_disk_quota: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ResourceLimitsObject: ...


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
        payload_dict: ResourceLimitsPayload | None = ...,
        session: int | None = ...,
        ipsec_phase1: int | None = ...,
        ipsec_phase2: int | None = ...,
        ipsec_phase1_interface: int | None = ...,
        ipsec_phase2_interface: int | None = ...,
        dialup_tunnel: int | None = ...,
        firewall_policy: int | None = ...,
        firewall_address: int | None = ...,
        firewall_addrgrp: int | None = ...,
        custom_service: int | None = ...,
        service_group: int | None = ...,
        onetime_schedule: int | None = ...,
        recurring_schedule: int | None = ...,
        user: int | None = ...,
        user_group: int | None = ...,
        sslvpn: int | None = ...,
        proxy: int | None = ...,
        log_disk_quota: int | None = ...,
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
    "ResourceLimits",
    "ResourceLimitsPayload",
    "ResourceLimitsResponse",
    "ResourceLimitsObject",
]