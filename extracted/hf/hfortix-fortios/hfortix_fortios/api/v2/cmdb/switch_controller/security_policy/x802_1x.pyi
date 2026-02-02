""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/security_policy/x802_1x
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

class X8021xUsergroupItem(TypedDict, total=False):
    """Nested item for user-group field."""
    name: str


class X8021xPayload(TypedDict, total=False):
    """Payload type for X8021x operations."""
    name: str
    security_mode: Literal["802.1X", "802.1X-mac-based"]
    user_group: str | list[str] | list[X8021xUsergroupItem]
    mac_auth_bypass: Literal["disable", "enable"]
    auth_order: Literal["dot1x-mab", "mab-dot1x", "mab"]
    auth_priority: Literal["legacy", "dot1x-mab", "mab-dot1x"]
    open_auth: Literal["disable", "enable"]
    eap_passthru: Literal["disable", "enable"]
    eap_auto_untagged_vlans: Literal["disable", "enable"]
    guest_vlan: Literal["disable", "enable"]
    guest_vlan_id: str
    guest_auth_delay: int
    auth_fail_vlan: Literal["disable", "enable"]
    auth_fail_vlan_id: str
    framevid_apply: Literal["disable", "enable"]
    radius_timeout_overwrite: Literal["disable", "enable"]
    policy_type: Literal["802.1X"]
    authserver_timeout_period: int
    authserver_timeout_vlan: Literal["disable", "enable"]
    authserver_timeout_vlanid: str
    authserver_timeout_tagged: Literal["disable", "lldp-voice", "static"]
    authserver_timeout_tagged_vlanid: str
    dacl: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class X8021xResponse(TypedDict, total=False):
    """Response type for X8021x - use with .dict property for typed dict access."""
    name: str
    security_mode: Literal["802.1X", "802.1X-mac-based"]
    user_group: list[X8021xUsergroupItem]
    mac_auth_bypass: Literal["disable", "enable"]
    auth_order: Literal["dot1x-mab", "mab-dot1x", "mab"]
    auth_priority: Literal["legacy", "dot1x-mab", "mab-dot1x"]
    open_auth: Literal["disable", "enable"]
    eap_passthru: Literal["disable", "enable"]
    eap_auto_untagged_vlans: Literal["disable", "enable"]
    guest_vlan: Literal["disable", "enable"]
    guest_vlan_id: str
    guest_auth_delay: int
    auth_fail_vlan: Literal["disable", "enable"]
    auth_fail_vlan_id: str
    framevid_apply: Literal["disable", "enable"]
    radius_timeout_overwrite: Literal["disable", "enable"]
    policy_type: Literal["802.1X"]
    authserver_timeout_period: int
    authserver_timeout_vlan: Literal["disable", "enable"]
    authserver_timeout_vlanid: str
    authserver_timeout_tagged: Literal["disable", "lldp-voice", "static"]
    authserver_timeout_tagged_vlanid: str
    dacl: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class X8021xUsergroupItemObject(FortiObject[X8021xUsergroupItem]):
    """Typed object for user-group table items with attribute access."""
    name: str


class X8021xObject(FortiObject):
    """Typed FortiObject for X8021x with field access."""
    name: str
    security_mode: Literal["802.1X", "802.1X-mac-based"]
    user_group: FortiObjectList[X8021xUsergroupItemObject]
    mac_auth_bypass: Literal["disable", "enable"]
    auth_order: Literal["dot1x-mab", "mab-dot1x", "mab"]
    auth_priority: Literal["legacy", "dot1x-mab", "mab-dot1x"]
    open_auth: Literal["disable", "enable"]
    eap_passthru: Literal["disable", "enable"]
    eap_auto_untagged_vlans: Literal["disable", "enable"]
    guest_vlan: Literal["disable", "enable"]
    guest_vlan_id: str
    guest_auth_delay: int
    auth_fail_vlan: Literal["disable", "enable"]
    auth_fail_vlan_id: str
    framevid_apply: Literal["disable", "enable"]
    radius_timeout_overwrite: Literal["disable", "enable"]
    policy_type: Literal["802.1X"]
    authserver_timeout_period: int
    authserver_timeout_vlan: Literal["disable", "enable"]
    authserver_timeout_vlanid: str
    authserver_timeout_tagged: Literal["disable", "lldp-voice", "static"]
    authserver_timeout_tagged_vlanid: str
    dacl: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class X8021x:
    """
    
    Endpoint: switch_controller/security_policy/x802_1x
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> X8021xObject: ...
    
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
    ) -> FortiObjectList[X8021xObject]: ...
    
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
        payload_dict: X8021xPayload | None = ...,
        name: str | None = ...,
        security_mode: Literal["802.1X", "802.1X-mac-based"] | None = ...,
        user_group: str | list[str] | list[X8021xUsergroupItem] | None = ...,
        mac_auth_bypass: Literal["disable", "enable"] | None = ...,
        auth_order: Literal["dot1x-mab", "mab-dot1x", "mab"] | None = ...,
        auth_priority: Literal["legacy", "dot1x-mab", "mab-dot1x"] | None = ...,
        open_auth: Literal["disable", "enable"] | None = ...,
        eap_passthru: Literal["disable", "enable"] | None = ...,
        eap_auto_untagged_vlans: Literal["disable", "enable"] | None = ...,
        guest_vlan: Literal["disable", "enable"] | None = ...,
        guest_vlan_id: str | None = ...,
        guest_auth_delay: int | None = ...,
        auth_fail_vlan: Literal["disable", "enable"] | None = ...,
        auth_fail_vlan_id: str | None = ...,
        framevid_apply: Literal["disable", "enable"] | None = ...,
        radius_timeout_overwrite: Literal["disable", "enable"] | None = ...,
        policy_type: Literal["802.1X"] | None = ...,
        authserver_timeout_period: int | None = ...,
        authserver_timeout_vlan: Literal["disable", "enable"] | None = ...,
        authserver_timeout_vlanid: str | None = ...,
        authserver_timeout_tagged: Literal["disable", "lldp-voice", "static"] | None = ...,
        authserver_timeout_tagged_vlanid: str | None = ...,
        dacl: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> X8021xObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: X8021xPayload | None = ...,
        name: str | None = ...,
        security_mode: Literal["802.1X", "802.1X-mac-based"] | None = ...,
        user_group: str | list[str] | list[X8021xUsergroupItem] | None = ...,
        mac_auth_bypass: Literal["disable", "enable"] | None = ...,
        auth_order: Literal["dot1x-mab", "mab-dot1x", "mab"] | None = ...,
        auth_priority: Literal["legacy", "dot1x-mab", "mab-dot1x"] | None = ...,
        open_auth: Literal["disable", "enable"] | None = ...,
        eap_passthru: Literal["disable", "enable"] | None = ...,
        eap_auto_untagged_vlans: Literal["disable", "enable"] | None = ...,
        guest_vlan: Literal["disable", "enable"] | None = ...,
        guest_vlan_id: str | None = ...,
        guest_auth_delay: int | None = ...,
        auth_fail_vlan: Literal["disable", "enable"] | None = ...,
        auth_fail_vlan_id: str | None = ...,
        framevid_apply: Literal["disable", "enable"] | None = ...,
        radius_timeout_overwrite: Literal["disable", "enable"] | None = ...,
        policy_type: Literal["802.1X"] | None = ...,
        authserver_timeout_period: int | None = ...,
        authserver_timeout_vlan: Literal["disable", "enable"] | None = ...,
        authserver_timeout_vlanid: str | None = ...,
        authserver_timeout_tagged: Literal["disable", "lldp-voice", "static"] | None = ...,
        authserver_timeout_tagged_vlanid: str | None = ...,
        dacl: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> X8021xObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
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
        payload_dict: X8021xPayload | None = ...,
        name: str | None = ...,
        security_mode: Literal["802.1X", "802.1X-mac-based"] | None = ...,
        user_group: str | list[str] | list[X8021xUsergroupItem] | None = ...,
        mac_auth_bypass: Literal["disable", "enable"] | None = ...,
        auth_order: Literal["dot1x-mab", "mab-dot1x", "mab"] | None = ...,
        auth_priority: Literal["legacy", "dot1x-mab", "mab-dot1x"] | None = ...,
        open_auth: Literal["disable", "enable"] | None = ...,
        eap_passthru: Literal["disable", "enable"] | None = ...,
        eap_auto_untagged_vlans: Literal["disable", "enable"] | None = ...,
        guest_vlan: Literal["disable", "enable"] | None = ...,
        guest_vlan_id: str | None = ...,
        guest_auth_delay: int | None = ...,
        auth_fail_vlan: Literal["disable", "enable"] | None = ...,
        auth_fail_vlan_id: str | None = ...,
        framevid_apply: Literal["disable", "enable"] | None = ...,
        radius_timeout_overwrite: Literal["disable", "enable"] | None = ...,
        policy_type: Literal["802.1X"] | None = ...,
        authserver_timeout_period: int | None = ...,
        authserver_timeout_vlan: Literal["disable", "enable"] | None = ...,
        authserver_timeout_vlanid: str | None = ...,
        authserver_timeout_tagged: Literal["disable", "lldp-voice", "static"] | None = ...,
        authserver_timeout_tagged_vlanid: str | None = ...,
        dacl: Literal["disable", "enable"] | None = ...,
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
    "X8021x",
    "X8021xPayload",
    "X8021xResponse",
    "X8021xObject",
]