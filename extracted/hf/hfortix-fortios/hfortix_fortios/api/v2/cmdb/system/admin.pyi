""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/admin
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

class AdminVdomItem(TypedDict, total=False):
    """Nested item for vdom field."""
    name: str


class AdminGuestusergroupsItem(TypedDict, total=False):
    """Nested item for guest-usergroups field."""
    name: str


class AdminPayload(TypedDict, total=False):
    """Payload type for Admin operations."""
    name: str
    vdom: str | list[str] | list[AdminVdomItem]
    remote_auth: Literal["enable", "disable"]
    remote_group: str
    wildcard: Literal["enable", "disable"]
    password: str
    peer_auth: Literal["enable", "disable"]
    peer_group: str
    trusthost1: str
    trusthost2: str
    trusthost3: str
    trusthost4: str
    trusthost5: str
    trusthost6: str
    trusthost7: str
    trusthost8: str
    trusthost9: str
    trusthost10: str
    ip6_trusthost1: str
    ip6_trusthost2: str
    ip6_trusthost3: str
    ip6_trusthost4: str
    ip6_trusthost5: str
    ip6_trusthost6: str
    ip6_trusthost7: str
    ip6_trusthost8: str
    ip6_trusthost9: str
    ip6_trusthost10: str
    accprofile: str
    allow_remove_admin_session: Literal["enable", "disable"]
    comments: str
    ssh_public_key1: str
    ssh_public_key2: str
    ssh_public_key3: str
    ssh_certificate: str
    schedule: str
    accprofile_override: Literal["enable", "disable"]
    vdom_override: Literal["enable", "disable"]
    password_expire: str
    force_password_change: Literal["enable", "disable"]
    two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    fortitoken: str
    email_to: str
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    sms_phone: str
    guest_auth: Literal["disable", "enable"]
    guest_usergroups: str | list[str] | list[AdminGuestusergroupsItem]
    guest_lang: str
    status: str
    list: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AdminResponse(TypedDict, total=False):
    """Response type for Admin - use with .dict property for typed dict access."""
    name: str
    vdom: list[AdminVdomItem]
    remote_auth: Literal["enable", "disable"]
    remote_group: str
    wildcard: Literal["enable", "disable"]
    password: str
    peer_auth: Literal["enable", "disable"]
    peer_group: str
    trusthost1: str
    trusthost2: str
    trusthost3: str
    trusthost4: str
    trusthost5: str
    trusthost6: str
    trusthost7: str
    trusthost8: str
    trusthost9: str
    trusthost10: str
    ip6_trusthost1: str
    ip6_trusthost2: str
    ip6_trusthost3: str
    ip6_trusthost4: str
    ip6_trusthost5: str
    ip6_trusthost6: str
    ip6_trusthost7: str
    ip6_trusthost8: str
    ip6_trusthost9: str
    ip6_trusthost10: str
    accprofile: str
    allow_remove_admin_session: Literal["enable", "disable"]
    comments: str
    ssh_public_key1: str
    ssh_public_key2: str
    ssh_public_key3: str
    ssh_certificate: str
    schedule: str
    accprofile_override: Literal["enable", "disable"]
    vdom_override: Literal["enable", "disable"]
    password_expire: str
    force_password_change: Literal["enable", "disable"]
    two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    fortitoken: str
    email_to: str
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    sms_phone: str
    guest_auth: Literal["disable", "enable"]
    guest_usergroups: list[AdminGuestusergroupsItem]
    guest_lang: str
    status: str
    list: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AdminVdomItemObject(FortiObject[AdminVdomItem]):
    """Typed object for vdom table items with attribute access."""
    name: str


class AdminGuestusergroupsItemObject(FortiObject[AdminGuestusergroupsItem]):
    """Typed object for guest-usergroups table items with attribute access."""
    name: str


class AdminObject(FortiObject):
    """Typed FortiObject for Admin with field access."""
    name: str
    remote_auth: Literal["enable", "disable"]
    remote_group: str
    wildcard: Literal["enable", "disable"]
    password: str
    peer_auth: Literal["enable", "disable"]
    peer_group: str
    trusthost1: str
    trusthost2: str
    trusthost3: str
    trusthost4: str
    trusthost5: str
    trusthost6: str
    trusthost7: str
    trusthost8: str
    trusthost9: str
    trusthost10: str
    ip6_trusthost1: str
    ip6_trusthost2: str
    ip6_trusthost3: str
    ip6_trusthost4: str
    ip6_trusthost5: str
    ip6_trusthost6: str
    ip6_trusthost7: str
    ip6_trusthost8: str
    ip6_trusthost9: str
    ip6_trusthost10: str
    accprofile: str
    allow_remove_admin_session: Literal["enable", "disable"]
    comments: str
    ssh_public_key1: str
    ssh_public_key2: str
    ssh_public_key3: str
    ssh_certificate: str
    schedule: str
    accprofile_override: Literal["enable", "disable"]
    vdom_override: Literal["enable", "disable"]
    password_expire: str
    force_password_change: Literal["enable", "disable"]
    two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    fortitoken: str
    email_to: str
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    sms_phone: str
    guest_auth: Literal["disable", "enable"]
    guest_usergroups: FortiObjectList[AdminGuestusergroupsItemObject]
    guest_lang: str
    status: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Admin:
    """
    
    Endpoint: system/admin
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
    ) -> AdminObject: ...
    
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
    ) -> FortiObjectList[AdminObject]: ...
    
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
        payload_dict: AdminPayload | None = ...,
        name: str | None = ...,
        remote_auth: Literal["enable", "disable"] | None = ...,
        remote_group: str | None = ...,
        wildcard: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        peer_auth: Literal["enable", "disable"] | None = ...,
        peer_group: str | None = ...,
        trusthost1: str | None = ...,
        trusthost2: str | None = ...,
        trusthost3: str | None = ...,
        trusthost4: str | None = ...,
        trusthost5: str | None = ...,
        trusthost6: str | None = ...,
        trusthost7: str | None = ...,
        trusthost8: str | None = ...,
        trusthost9: str | None = ...,
        trusthost10: str | None = ...,
        ip6_trusthost1: str | None = ...,
        ip6_trusthost2: str | None = ...,
        ip6_trusthost3: str | None = ...,
        ip6_trusthost4: str | None = ...,
        ip6_trusthost5: str | None = ...,
        ip6_trusthost6: str | None = ...,
        ip6_trusthost7: str | None = ...,
        ip6_trusthost8: str | None = ...,
        ip6_trusthost9: str | None = ...,
        ip6_trusthost10: str | None = ...,
        accprofile: str | None = ...,
        allow_remove_admin_session: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        ssh_public_key1: str | None = ...,
        ssh_public_key2: str | None = ...,
        ssh_public_key3: str | None = ...,
        ssh_certificate: str | None = ...,
        schedule: str | None = ...,
        accprofile_override: Literal["enable", "disable"] | None = ...,
        vdom_override: Literal["enable", "disable"] | None = ...,
        password_expire: str | None = ...,
        force_password_change: Literal["enable", "disable"] | None = ...,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        fortitoken: str | None = ...,
        email_to: str | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        sms_phone: str | None = ...,
        guest_auth: Literal["disable", "enable"] | None = ...,
        guest_usergroups: str | list[str] | list[AdminGuestusergroupsItem] | None = ...,
        guest_lang: str | None = ...,
        status: str | None = ...,
        list: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AdminObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AdminPayload | None = ...,
        name: str | None = ...,
        remote_auth: Literal["enable", "disable"] | None = ...,
        remote_group: str | None = ...,
        wildcard: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        peer_auth: Literal["enable", "disable"] | None = ...,
        peer_group: str | None = ...,
        trusthost1: str | None = ...,
        trusthost2: str | None = ...,
        trusthost3: str | None = ...,
        trusthost4: str | None = ...,
        trusthost5: str | None = ...,
        trusthost6: str | None = ...,
        trusthost7: str | None = ...,
        trusthost8: str | None = ...,
        trusthost9: str | None = ...,
        trusthost10: str | None = ...,
        ip6_trusthost1: str | None = ...,
        ip6_trusthost2: str | None = ...,
        ip6_trusthost3: str | None = ...,
        ip6_trusthost4: str | None = ...,
        ip6_trusthost5: str | None = ...,
        ip6_trusthost6: str | None = ...,
        ip6_trusthost7: str | None = ...,
        ip6_trusthost8: str | None = ...,
        ip6_trusthost9: str | None = ...,
        ip6_trusthost10: str | None = ...,
        accprofile: str | None = ...,
        allow_remove_admin_session: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        ssh_public_key1: str | None = ...,
        ssh_public_key2: str | None = ...,
        ssh_public_key3: str | None = ...,
        ssh_certificate: str | None = ...,
        schedule: str | None = ...,
        accprofile_override: Literal["enable", "disable"] | None = ...,
        vdom_override: Literal["enable", "disable"] | None = ...,
        password_expire: str | None = ...,
        force_password_change: Literal["enable", "disable"] | None = ...,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        fortitoken: str | None = ...,
        email_to: str | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        sms_phone: str | None = ...,
        guest_auth: Literal["disable", "enable"] | None = ...,
        guest_usergroups: str | list[str] | list[AdminGuestusergroupsItem] | None = ...,
        guest_lang: str | None = ...,
        status: str | None = ...,
        list: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AdminObject: ...

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
        payload_dict: AdminPayload | None = ...,
        name: str | None = ...,
        remote_auth: Literal["enable", "disable"] | None = ...,
        remote_group: str | None = ...,
        wildcard: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        peer_auth: Literal["enable", "disable"] | None = ...,
        peer_group: str | None = ...,
        trusthost1: str | None = ...,
        trusthost2: str | None = ...,
        trusthost3: str | None = ...,
        trusthost4: str | None = ...,
        trusthost5: str | None = ...,
        trusthost6: str | None = ...,
        trusthost7: str | None = ...,
        trusthost8: str | None = ...,
        trusthost9: str | None = ...,
        trusthost10: str | None = ...,
        ip6_trusthost1: str | None = ...,
        ip6_trusthost2: str | None = ...,
        ip6_trusthost3: str | None = ...,
        ip6_trusthost4: str | None = ...,
        ip6_trusthost5: str | None = ...,
        ip6_trusthost6: str | None = ...,
        ip6_trusthost7: str | None = ...,
        ip6_trusthost8: str | None = ...,
        ip6_trusthost9: str | None = ...,
        ip6_trusthost10: str | None = ...,
        accprofile: str | None = ...,
        allow_remove_admin_session: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        ssh_public_key1: str | None = ...,
        ssh_public_key2: str | None = ...,
        ssh_public_key3: str | None = ...,
        ssh_certificate: str | None = ...,
        schedule: str | None = ...,
        accprofile_override: Literal["enable", "disable"] | None = ...,
        vdom_override: Literal["enable", "disable"] | None = ...,
        password_expire: str | None = ...,
        force_password_change: Literal["enable", "disable"] | None = ...,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        fortitoken: str | None = ...,
        email_to: str | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        sms_phone: str | None = ...,
        guest_auth: Literal["disable", "enable"] | None = ...,
        guest_usergroups: str | list[str] | list[AdminGuestusergroupsItem] | None = ...,
        guest_lang: str | None = ...,
        status: str | None = ...,
        list: str | None = ...,
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
    "Admin",
    "AdminPayload",
    "AdminResponse",
    "AdminObject",
]