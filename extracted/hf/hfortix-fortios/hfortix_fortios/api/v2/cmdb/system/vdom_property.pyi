""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vdom_property
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

class VdomPropertyPayload(TypedDict, total=False):
    """Payload type for VdomProperty operations."""
    name: str
    description: str
    snmp_index: int
    session: str | list[str]
    ipsec_phase1: str | list[str]
    ipsec_phase2: str | list[str]
    ipsec_phase1_interface: str | list[str]
    ipsec_phase2_interface: str | list[str]
    dialup_tunnel: str | list[str]
    firewall_policy: str | list[str]
    firewall_address: str | list[str]
    firewall_addrgrp: str | list[str]
    custom_service: str | list[str]
    service_group: str | list[str]
    onetime_schedule: str | list[str]
    recurring_schedule: str | list[str]
    user: str | list[str]
    user_group: str | list[str]
    sslvpn: str | list[str]
    proxy: str | list[str]
    log_disk_quota: str | list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VdomPropertyResponse(TypedDict, total=False):
    """Response type for VdomProperty - use with .dict property for typed dict access."""
    name: str
    description: str
    snmp_index: int
    session: str | list[str]
    ipsec_phase1: str | list[str]
    ipsec_phase2: str | list[str]
    ipsec_phase1_interface: str | list[str]
    ipsec_phase2_interface: str | list[str]
    dialup_tunnel: str | list[str]
    firewall_policy: str | list[str]
    firewall_address: str | list[str]
    firewall_addrgrp: str | list[str]
    custom_service: str | list[str]
    service_group: str | list[str]
    onetime_schedule: str | list[str]
    recurring_schedule: str | list[str]
    user: str | list[str]
    user_group: str | list[str]
    sslvpn: str | list[str]
    proxy: str | list[str]
    log_disk_quota: str | list[str]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VdomPropertyObject(FortiObject):
    """Typed FortiObject for VdomProperty with field access."""
    name: str
    description: str
    snmp_index: int
    session: str | list[str]
    ipsec_phase1: str | list[str]
    ipsec_phase2: str | list[str]
    ipsec_phase1_interface: str | list[str]
    ipsec_phase2_interface: str | list[str]
    dialup_tunnel: str | list[str]
    firewall_policy: str | list[str]
    firewall_address: str | list[str]
    firewall_addrgrp: str | list[str]
    custom_service: str | list[str]
    service_group: str | list[str]
    onetime_schedule: str | list[str]
    recurring_schedule: str | list[str]
    user: str | list[str]
    user_group: str | list[str]
    sslvpn: str | list[str]
    proxy: str | list[str]
    log_disk_quota: str | list[str]


# ================================================================
# Main Endpoint Class
# ================================================================

class VdomProperty:
    """
    
    Endpoint: system/vdom_property
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
    ) -> VdomPropertyObject: ...
    
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
    ) -> FortiObjectList[VdomPropertyObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomPropertyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomPropertyObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
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
    "VdomProperty",
    "VdomPropertyPayload",
    "VdomPropertyResponse",
    "VdomPropertyObject",
]