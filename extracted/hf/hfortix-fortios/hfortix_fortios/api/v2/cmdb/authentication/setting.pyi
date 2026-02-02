""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: authentication/setting
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

class SettingUsercertcaItem(TypedDict, total=False):
    """Nested item for user-cert-ca field."""
    name: str


class SettingDevrangeItem(TypedDict, total=False):
    """Nested item for dev-range field."""
    name: str


class SettingPayload(TypedDict, total=False):
    """Payload type for Setting operations."""
    active_auth_scheme: str
    sso_auth_scheme: str
    update_time: str
    persistent_cookie: Literal["enable", "disable"]
    ip_auth_cookie: Literal["enable", "disable"]
    cookie_max_age: int
    cookie_refresh_div: int
    captive_portal_type: Literal["fqdn", "ip"]
    captive_portal_ip: str
    captive_portal_ip6: str
    captive_portal: str
    captive_portal6: str
    cert_auth: Literal["enable", "disable"]
    cert_captive_portal: str
    cert_captive_portal_ip: str
    cert_captive_portal_port: int
    captive_portal_port: int
    auth_https: Literal["enable", "disable"]
    captive_portal_ssl_port: int
    user_cert_ca: str | list[str] | list[SettingUsercertcaItem]
    dev_range: str | list[str] | list[SettingDevrangeItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    active_auth_scheme: str
    sso_auth_scheme: str
    update_time: str
    persistent_cookie: Literal["enable", "disable"]
    ip_auth_cookie: Literal["enable", "disable"]
    cookie_max_age: int
    cookie_refresh_div: int
    captive_portal_type: Literal["fqdn", "ip"]
    captive_portal_ip: str
    captive_portal_ip6: str
    captive_portal: str
    captive_portal6: str
    cert_auth: Literal["enable", "disable"]
    cert_captive_portal: str
    cert_captive_portal_ip: str
    cert_captive_portal_port: int
    captive_portal_port: int
    auth_https: Literal["enable", "disable"]
    captive_portal_ssl_port: int
    user_cert_ca: list[SettingUsercertcaItem]
    dev_range: list[SettingDevrangeItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingUsercertcaItemObject(FortiObject[SettingUsercertcaItem]):
    """Typed object for user-cert-ca table items with attribute access."""
    name: str


class SettingDevrangeItemObject(FortiObject[SettingDevrangeItem]):
    """Typed object for dev-range table items with attribute access."""
    name: str


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    active_auth_scheme: str
    sso_auth_scheme: str
    update_time: str
    persistent_cookie: Literal["enable", "disable"]
    ip_auth_cookie: Literal["enable", "disable"]
    cookie_max_age: int
    cookie_refresh_div: int
    captive_portal_type: Literal["fqdn", "ip"]
    captive_portal_ip: str
    captive_portal_ip6: str
    captive_portal: str
    captive_portal6: str
    cert_auth: Literal["enable", "disable"]
    cert_captive_portal: str
    cert_captive_portal_ip: str
    cert_captive_portal_port: int
    captive_portal_port: int
    auth_https: Literal["enable", "disable"]
    captive_portal_ssl_port: int
    user_cert_ca: FortiObjectList[SettingUsercertcaItemObject]
    dev_range: FortiObjectList[SettingDevrangeItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: authentication/setting
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
    ) -> SettingObject: ...
    
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
        payload_dict: SettingPayload | None = ...,
        active_auth_scheme: str | None = ...,
        sso_auth_scheme: str | None = ...,
        update_time: str | None = ...,
        persistent_cookie: Literal["enable", "disable"] | None = ...,
        ip_auth_cookie: Literal["enable", "disable"] | None = ...,
        cookie_max_age: int | None = ...,
        cookie_refresh_div: int | None = ...,
        captive_portal_type: Literal["fqdn", "ip"] | None = ...,
        captive_portal_ip: str | None = ...,
        captive_portal_ip6: str | None = ...,
        captive_portal: str | None = ...,
        captive_portal6: str | None = ...,
        cert_auth: Literal["enable", "disable"] | None = ...,
        cert_captive_portal: str | None = ...,
        cert_captive_portal_ip: str | None = ...,
        cert_captive_portal_port: int | None = ...,
        captive_portal_port: int | None = ...,
        auth_https: Literal["enable", "disable"] | None = ...,
        captive_portal_ssl_port: int | None = ...,
        user_cert_ca: str | list[str] | list[SettingUsercertcaItem] | None = ...,
        dev_range: str | list[str] | list[SettingDevrangeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingObject: ...


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
        payload_dict: SettingPayload | None = ...,
        active_auth_scheme: str | None = ...,
        sso_auth_scheme: str | None = ...,
        update_time: str | None = ...,
        persistent_cookie: Literal["enable", "disable"] | None = ...,
        ip_auth_cookie: Literal["enable", "disable"] | None = ...,
        cookie_max_age: int | None = ...,
        cookie_refresh_div: int | None = ...,
        captive_portal_type: Literal["fqdn", "ip"] | None = ...,
        captive_portal_ip: str | None = ...,
        captive_portal_ip6: str | None = ...,
        captive_portal: str | None = ...,
        captive_portal6: str | None = ...,
        cert_auth: Literal["enable", "disable"] | None = ...,
        cert_captive_portal: str | None = ...,
        cert_captive_portal_ip: str | None = ...,
        cert_captive_portal_port: int | None = ...,
        captive_portal_port: int | None = ...,
        auth_https: Literal["enable", "disable"] | None = ...,
        captive_portal_ssl_port: int | None = ...,
        user_cert_ca: str | list[str] | list[SettingUsercertcaItem] | None = ...,
        dev_range: str | list[str] | list[SettingDevrangeItem] | None = ...,
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
    "Setting",
    "SettingPayload",
    "SettingResponse",
    "SettingObject",
]