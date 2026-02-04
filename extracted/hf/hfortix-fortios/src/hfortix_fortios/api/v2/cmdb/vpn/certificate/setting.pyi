""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/certificate/setting
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

class SettingCrlverificationDict(TypedDict, total=False):
    """Nested object type for crl-verification field."""
    expiry: Literal["ignore", "revoke"]
    leaf_crl_absence: Literal["ignore", "revoke"]
    chain_crl_absence: Literal["ignore", "revoke"]


class SettingPayload(TypedDict, total=False):
    """Payload type for Setting operations."""
    ocsp_status: Literal["enable", "mandatory", "disable"]
    ocsp_option: Literal["certificate", "server"]
    proxy: str
    proxy_port: int
    proxy_username: str
    proxy_password: str
    source_ip: str
    ocsp_default_server: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    check_ca_cert: Literal["enable", "disable"]
    check_ca_chain: Literal["enable", "disable"]
    subject_match: Literal["substring", "value"]
    subject_set: Literal["subset", "superset"]
    cn_match: Literal["substring", "value"]
    cn_allow_multi: Literal["disable", "enable"]
    crl_verification: SettingCrlverificationDict
    strict_ocsp_check: Literal["enable", "disable"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    cmp_save_extra_certs: Literal["enable", "disable"]
    cmp_key_usage_checking: Literal["enable", "disable"]
    cert_expire_warning: int
    certname_rsa1024: str
    certname_rsa2048: str
    certname_rsa4096: str
    certname_dsa1024: str
    certname_dsa2048: str
    certname_ecdsa256: str
    certname_ecdsa384: str
    certname_ecdsa521: str
    certname_ed25519: str
    certname_ed448: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    ocsp_status: Literal["enable", "mandatory", "disable"]
    ocsp_option: Literal["certificate", "server"]
    proxy: str
    proxy_port: int
    proxy_username: str
    proxy_password: str
    source_ip: str
    ocsp_default_server: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    check_ca_cert: Literal["enable", "disable"]
    check_ca_chain: Literal["enable", "disable"]
    subject_match: Literal["substring", "value"]
    subject_set: Literal["subset", "superset"]
    cn_match: Literal["substring", "value"]
    cn_allow_multi: Literal["disable", "enable"]
    crl_verification: SettingCrlverificationDict
    strict_ocsp_check: Literal["enable", "disable"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    cmp_save_extra_certs: Literal["enable", "disable"]
    cmp_key_usage_checking: Literal["enable", "disable"]
    cert_expire_warning: int
    certname_rsa1024: str
    certname_rsa2048: str
    certname_rsa4096: str
    certname_dsa1024: str
    certname_dsa2048: str
    certname_ecdsa256: str
    certname_ecdsa384: str
    certname_ecdsa521: str
    certname_ed25519: str
    certname_ed448: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingCrlverificationObject(FortiObject):
    """Nested object for crl-verification field with attribute access."""
    expiry: Literal["ignore", "revoke"]
    leaf_crl_absence: Literal["ignore", "revoke"]
    chain_crl_absence: Literal["ignore", "revoke"]


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    ocsp_status: Literal["enable", "mandatory", "disable"]
    ocsp_option: Literal["certificate", "server"]
    proxy: str
    proxy_port: int
    proxy_username: str
    proxy_password: str
    source_ip: str
    ocsp_default_server: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    check_ca_cert: Literal["enable", "disable"]
    check_ca_chain: Literal["enable", "disable"]
    subject_match: Literal["substring", "value"]
    subject_set: Literal["subset", "superset"]
    cn_match: Literal["substring", "value"]
    cn_allow_multi: Literal["disable", "enable"]
    crl_verification: SettingCrlverificationObject
    strict_ocsp_check: Literal["enable", "disable"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    cmp_save_extra_certs: Literal["enable", "disable"]
    cmp_key_usage_checking: Literal["enable", "disable"]
    cert_expire_warning: int
    certname_rsa1024: str
    certname_rsa2048: str
    certname_rsa4096: str
    certname_dsa1024: str
    certname_dsa2048: str
    certname_ecdsa256: str
    certname_ecdsa384: str
    certname_ecdsa521: str
    certname_ed25519: str
    certname_ed448: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: vpn/certificate/setting
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
        ocsp_status: Literal["enable", "mandatory", "disable"] | None = ...,
        ocsp_option: Literal["certificate", "server"] | None = ...,
        proxy: str | None = ...,
        proxy_port: int | None = ...,
        proxy_username: str | None = ...,
        proxy_password: str | None = ...,
        source_ip: str | None = ...,
        ocsp_default_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        check_ca_cert: Literal["enable", "disable"] | None = ...,
        check_ca_chain: Literal["enable", "disable"] | None = ...,
        subject_match: Literal["substring", "value"] | None = ...,
        subject_set: Literal["subset", "superset"] | None = ...,
        cn_match: Literal["substring", "value"] | None = ...,
        cn_allow_multi: Literal["disable", "enable"] | None = ...,
        crl_verification: SettingCrlverificationDict | None = ...,
        strict_ocsp_check: Literal["enable", "disable"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        cmp_save_extra_certs: Literal["enable", "disable"] | None = ...,
        cmp_key_usage_checking: Literal["enable", "disable"] | None = ...,
        cert_expire_warning: int | None = ...,
        certname_rsa1024: str | None = ...,
        certname_rsa2048: str | None = ...,
        certname_rsa4096: str | None = ...,
        certname_dsa1024: str | None = ...,
        certname_dsa2048: str | None = ...,
        certname_ecdsa256: str | None = ...,
        certname_ecdsa384: str | None = ...,
        certname_ecdsa521: str | None = ...,
        certname_ed25519: str | None = ...,
        certname_ed448: str | None = ...,
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
        ocsp_status: Literal["enable", "mandatory", "disable"] | None = ...,
        ocsp_option: Literal["certificate", "server"] | None = ...,
        proxy: str | None = ...,
        proxy_port: int | None = ...,
        proxy_username: str | None = ...,
        proxy_password: str | None = ...,
        source_ip: str | None = ...,
        ocsp_default_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        check_ca_cert: Literal["enable", "disable"] | None = ...,
        check_ca_chain: Literal["enable", "disable"] | None = ...,
        subject_match: Literal["substring", "value"] | None = ...,
        subject_set: Literal["subset", "superset"] | None = ...,
        cn_match: Literal["substring", "value"] | None = ...,
        cn_allow_multi: Literal["disable", "enable"] | None = ...,
        crl_verification: SettingCrlverificationDict | None = ...,
        strict_ocsp_check: Literal["enable", "disable"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        cmp_save_extra_certs: Literal["enable", "disable"] | None = ...,
        cmp_key_usage_checking: Literal["enable", "disable"] | None = ...,
        cert_expire_warning: int | None = ...,
        certname_rsa1024: str | None = ...,
        certname_rsa2048: str | None = ...,
        certname_rsa4096: str | None = ...,
        certname_dsa1024: str | None = ...,
        certname_dsa2048: str | None = ...,
        certname_ecdsa256: str | None = ...,
        certname_ecdsa384: str | None = ...,
        certname_ecdsa521: str | None = ...,
        certname_ed25519: str | None = ...,
        certname_ed448: str | None = ...,
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