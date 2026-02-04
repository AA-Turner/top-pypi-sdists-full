""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/setting
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

class SettingAuthportsItem(TypedDict, total=False):
    """Nested item for auth-ports field."""
    id: int
    type: Literal["http", "https", "ftp", "telnet"]
    port: int


class SettingCorsallowedoriginsItem(TypedDict, total=False):
    """Nested item for cors-allowed-origins field."""
    name: str


class SettingPayload(TypedDict, total=False):
    """Payload type for Setting operations."""
    auth_type: str | list[str]
    auth_cert: str
    auth_ca_cert: str
    auth_secure_http: Literal["enable", "disable"]
    auth_http_basic: Literal["enable", "disable"]
    auth_ssl_allow_renegotiation: Literal["enable", "disable"]
    auth_src_mac: Literal["enable", "disable"]
    auth_on_demand: Literal["always", "implicitly"]
    auth_timeout: int
    auth_timeout_type: Literal["idle-timeout", "hard-timeout", "new-session"]
    auth_portal_timeout: int
    radius_ses_timeout_act: Literal["hard-timeout", "ignore-timeout"]
    auth_blackout_time: int
    auth_invalid_max: int
    auth_lockout_threshold: int
    auth_lockout_duration: int
    per_policy_disclaimer: Literal["enable", "disable"]
    auth_ports: str | list[str] | list[SettingAuthportsItem]
    auth_ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    auth_ssl_max_proto_version: Literal["sslv3", "tlsv1", "tlsv1-1", "tlsv1-2", "tlsv1-3"]
    auth_ssl_sigalgs: Literal["no-rsa-pss", "all"]
    default_user_password_policy: str
    cors: Literal["disable", "enable"]
    cors_allowed_origins: str | list[str] | list[SettingCorsallowedoriginsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    auth_type: str
    auth_cert: str
    auth_ca_cert: str
    auth_secure_http: Literal["enable", "disable"]
    auth_http_basic: Literal["enable", "disable"]
    auth_ssl_allow_renegotiation: Literal["enable", "disable"]
    auth_src_mac: Literal["enable", "disable"]
    auth_on_demand: Literal["always", "implicitly"]
    auth_timeout: int
    auth_timeout_type: Literal["idle-timeout", "hard-timeout", "new-session"]
    auth_portal_timeout: int
    radius_ses_timeout_act: Literal["hard-timeout", "ignore-timeout"]
    auth_blackout_time: int
    auth_invalid_max: int
    auth_lockout_threshold: int
    auth_lockout_duration: int
    per_policy_disclaimer: Literal["enable", "disable"]
    auth_ports: list[SettingAuthportsItem]
    auth_ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    auth_ssl_max_proto_version: Literal["sslv3", "tlsv1", "tlsv1-1", "tlsv1-2", "tlsv1-3"]
    auth_ssl_sigalgs: Literal["no-rsa-pss", "all"]
    default_user_password_policy: str
    cors: Literal["disable", "enable"]
    cors_allowed_origins: list[SettingCorsallowedoriginsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingAuthportsItemObject(FortiObject[SettingAuthportsItem]):
    """Typed object for auth-ports table items with attribute access."""
    id: int
    type: Literal["http", "https", "ftp", "telnet"]
    port: int


class SettingCorsallowedoriginsItemObject(FortiObject[SettingCorsallowedoriginsItem]):
    """Typed object for cors-allowed-origins table items with attribute access."""
    name: str


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    auth_type: str
    auth_cert: str
    auth_ca_cert: str
    auth_secure_http: Literal["enable", "disable"]
    auth_http_basic: Literal["enable", "disable"]
    auth_ssl_allow_renegotiation: Literal["enable", "disable"]
    auth_src_mac: Literal["enable", "disable"]
    auth_on_demand: Literal["always", "implicitly"]
    auth_timeout: int
    auth_timeout_type: Literal["idle-timeout", "hard-timeout", "new-session"]
    auth_portal_timeout: int
    radius_ses_timeout_act: Literal["hard-timeout", "ignore-timeout"]
    auth_blackout_time: int
    auth_invalid_max: int
    auth_lockout_threshold: int
    auth_lockout_duration: int
    per_policy_disclaimer: Literal["enable", "disable"]
    auth_ports: FortiObjectList[SettingAuthportsItemObject]
    auth_ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    auth_ssl_max_proto_version: Literal["sslv3", "tlsv1", "tlsv1-1", "tlsv1-2", "tlsv1-3"]
    auth_ssl_sigalgs: Literal["no-rsa-pss", "all"]
    default_user_password_policy: str
    cors: Literal["disable", "enable"]
    cors_allowed_origins: FortiObjectList[SettingCorsallowedoriginsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: user/setting
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
        auth_type: str | list[str] | None = ...,
        auth_cert: str | None = ...,
        auth_ca_cert: str | None = ...,
        auth_secure_http: Literal["enable", "disable"] | None = ...,
        auth_http_basic: Literal["enable", "disable"] | None = ...,
        auth_ssl_allow_renegotiation: Literal["enable", "disable"] | None = ...,
        auth_src_mac: Literal["enable", "disable"] | None = ...,
        auth_on_demand: Literal["always", "implicitly"] | None = ...,
        auth_timeout: int | None = ...,
        auth_timeout_type: Literal["idle-timeout", "hard-timeout", "new-session"] | None = ...,
        auth_portal_timeout: int | None = ...,
        radius_ses_timeout_act: Literal["hard-timeout", "ignore-timeout"] | None = ...,
        auth_blackout_time: int | None = ...,
        auth_invalid_max: int | None = ...,
        auth_lockout_threshold: int | None = ...,
        auth_lockout_duration: int | None = ...,
        per_policy_disclaimer: Literal["enable", "disable"] | None = ...,
        auth_ports: str | list[str] | list[SettingAuthportsItem] | None = ...,
        auth_ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auth_ssl_max_proto_version: Literal["sslv3", "tlsv1", "tlsv1-1", "tlsv1-2", "tlsv1-3"] | None = ...,
        auth_ssl_sigalgs: Literal["no-rsa-pss", "all"] | None = ...,
        default_user_password_policy: str | None = ...,
        cors: Literal["disable", "enable"] | None = ...,
        cors_allowed_origins: str | list[str] | list[SettingCorsallowedoriginsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingObject: ...


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
        payload_dict: SettingPayload | None = ...,
        auth_type: Literal["http", "https", "ftp", "telnet"] | list[str] | None = ...,
        auth_cert: str | None = ...,
        auth_ca_cert: str | None = ...,
        auth_secure_http: Literal["enable", "disable"] | None = ...,
        auth_http_basic: Literal["enable", "disable"] | None = ...,
        auth_ssl_allow_renegotiation: Literal["enable", "disable"] | None = ...,
        auth_src_mac: Literal["enable", "disable"] | None = ...,
        auth_on_demand: Literal["always", "implicitly"] | None = ...,
        auth_timeout: int | None = ...,
        auth_timeout_type: Literal["idle-timeout", "hard-timeout", "new-session"] | None = ...,
        auth_portal_timeout: int | None = ...,
        radius_ses_timeout_act: Literal["hard-timeout", "ignore-timeout"] | None = ...,
        auth_blackout_time: int | None = ...,
        auth_invalid_max: int | None = ...,
        auth_lockout_threshold: int | None = ...,
        auth_lockout_duration: int | None = ...,
        per_policy_disclaimer: Literal["enable", "disable"] | None = ...,
        auth_ports: str | list[str] | list[SettingAuthportsItem] | None = ...,
        auth_ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auth_ssl_max_proto_version: Literal["sslv3", "tlsv1", "tlsv1-1", "tlsv1-2", "tlsv1-3"] | None = ...,
        auth_ssl_sigalgs: Literal["no-rsa-pss", "all"] | None = ...,
        default_user_password_policy: str | None = ...,
        cors: Literal["disable", "enable"] | None = ...,
        cors_allowed_origins: str | list[str] | list[SettingCorsallowedoriginsItem] | None = ...,
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