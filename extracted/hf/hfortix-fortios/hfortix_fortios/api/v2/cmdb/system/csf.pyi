""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/csf
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

class CsfFabricconnectorVdomItem(TypedDict, total=False):
    """Nested item for fabric-connector.vdom field."""
    name: str


class CsfTrustedlistItem(TypedDict, total=False):
    """Nested item for trusted-list field."""
    name: str
    authorization_type: Literal["serial", "certificate"]
    serial: str
    certificate: str
    action: Literal["accept", "deny"]
    ha_members: str | list[str]
    downstream_authorization: Literal["enable", "disable"]
    index: int


class CsfFabricconnectorItem(TypedDict, total=False):
    """Nested item for fabric-connector field."""
    serial: str
    accprofile: str
    configuration_write_access: Literal["enable", "disable"]
    vdom: str | list[str] | list[CsfFabricconnectorVdomItem]


class CsfPayload(TypedDict, total=False):
    """Payload type for Csf operations."""
    status: Literal["enable", "disable"]
    uid: str
    upstream: str
    source_ip: str
    upstream_interface_select_method: Literal["auto", "sdwan", "specify"]
    upstream_interface: str
    upstream_port: int
    group_name: str
    group_password: str
    accept_auth_by_cert: Literal["disable", "enable"]
    log_unification: Literal["disable", "enable"]
    authorization_request_type: Literal["serial", "certificate"]
    certificate: str
    fabric_workers: int
    downstream_access: Literal["enable", "disable"]
    legacy_authentication: Literal["disable", "enable"]
    downstream_accprofile: str
    configuration_sync: Literal["default", "local"]
    fabric_object_unification: Literal["default", "local"]
    saml_configuration_sync: Literal["default", "local"]
    trusted_list: str | list[str] | list[CsfTrustedlistItem]
    fabric_connector: str | list[str] | list[CsfFabricconnectorItem]
    forticloud_account_enforcement: Literal["enable", "disable"]
    file_mgmt: Literal["enable", "disable"]
    file_quota: int
    file_quota_warning: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CsfResponse(TypedDict, total=False):
    """Response type for Csf - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    uid: str
    upstream: str
    source_ip: str
    upstream_interface_select_method: Literal["auto", "sdwan", "specify"]
    upstream_interface: str
    upstream_port: int
    group_name: str
    group_password: str
    accept_auth_by_cert: Literal["disable", "enable"]
    log_unification: Literal["disable", "enable"]
    authorization_request_type: Literal["serial", "certificate"]
    certificate: str
    fabric_workers: int
    downstream_access: Literal["enable", "disable"]
    legacy_authentication: Literal["disable", "enable"]
    downstream_accprofile: str
    configuration_sync: Literal["default", "local"]
    fabric_object_unification: Literal["default", "local"]
    saml_configuration_sync: Literal["default", "local"]
    trusted_list: list[CsfTrustedlistItem]
    fabric_connector: list[CsfFabricconnectorItem]
    forticloud_account_enforcement: Literal["enable", "disable"]
    file_mgmt: Literal["enable", "disable"]
    file_quota: int
    file_quota_warning: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CsfFabricconnectorVdomItemObject(FortiObject[CsfFabricconnectorVdomItem]):
    """Typed object for fabric-connector.vdom table items with attribute access."""
    name: str


class CsfTrustedlistItemObject(FortiObject[CsfTrustedlistItem]):
    """Typed object for trusted-list table items with attribute access."""
    name: str
    authorization_type: Literal["serial", "certificate"]
    serial: str
    certificate: str
    action: Literal["accept", "deny"]
    ha_members: str | list[str]
    downstream_authorization: Literal["enable", "disable"]
    index: int


class CsfFabricconnectorItemObject(FortiObject[CsfFabricconnectorItem]):
    """Typed object for fabric-connector table items with attribute access."""
    serial: str
    accprofile: str
    configuration_write_access: Literal["enable", "disable"]
    vdom: FortiObjectList[CsfFabricconnectorVdomItemObject]


class CsfObject(FortiObject):
    """Typed FortiObject for Csf with field access."""
    status: Literal["enable", "disable"]
    uid: str
    upstream: str
    source_ip: str
    upstream_interface_select_method: Literal["auto", "sdwan", "specify"]
    upstream_interface: str
    upstream_port: int
    group_name: str
    group_password: str
    accept_auth_by_cert: Literal["disable", "enable"]
    log_unification: Literal["disable", "enable"]
    authorization_request_type: Literal["serial", "certificate"]
    certificate: str
    fabric_workers: int
    downstream_access: Literal["enable", "disable"]
    legacy_authentication: Literal["disable", "enable"]
    downstream_accprofile: str
    configuration_sync: Literal["default", "local"]
    fabric_object_unification: Literal["default", "local"]
    saml_configuration_sync: Literal["default", "local"]
    trusted_list: FortiObjectList[CsfTrustedlistItemObject]
    fabric_connector: FortiObjectList[CsfFabricconnectorItemObject]
    forticloud_account_enforcement: Literal["enable", "disable"]
    file_mgmt: Literal["enable", "disable"]
    file_quota: int
    file_quota_warning: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Csf:
    """
    
    Endpoint: system/csf
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
    ) -> CsfObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CsfPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        uid: str | None = ...,
        upstream: str | None = ...,
        source_ip: str | None = ...,
        upstream_interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        upstream_interface: str | None = ...,
        upstream_port: int | None = ...,
        group_name: str | None = ...,
        group_password: str | None = ...,
        accept_auth_by_cert: Literal["disable", "enable"] | None = ...,
        log_unification: Literal["disable", "enable"] | None = ...,
        authorization_request_type: Literal["serial", "certificate"] | None = ...,
        certificate: str | None = ...,
        fabric_workers: int | None = ...,
        downstream_access: Literal["enable", "disable"] | None = ...,
        legacy_authentication: Literal["disable", "enable"] | None = ...,
        downstream_accprofile: str | None = ...,
        configuration_sync: Literal["default", "local"] | None = ...,
        fabric_object_unification: Literal["default", "local"] | None = ...,
        saml_configuration_sync: Literal["default", "local"] | None = ...,
        trusted_list: str | list[str] | list[CsfTrustedlistItem] | None = ...,
        fabric_connector: str | list[str] | list[CsfFabricconnectorItem] | None = ...,
        forticloud_account_enforcement: Literal["enable", "disable"] | None = ...,
        file_mgmt: Literal["enable", "disable"] | None = ...,
        file_quota: int | None = ...,
        file_quota_warning: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CsfObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: CsfPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        uid: str | None = ...,
        upstream: str | None = ...,
        source_ip: str | None = ...,
        upstream_interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        upstream_interface: str | None = ...,
        upstream_port: int | None = ...,
        group_name: str | None = ...,
        group_password: str | None = ...,
        accept_auth_by_cert: Literal["disable", "enable"] | None = ...,
        log_unification: Literal["disable", "enable"] | None = ...,
        authorization_request_type: Literal["serial", "certificate"] | None = ...,
        certificate: str | None = ...,
        fabric_workers: int | None = ...,
        downstream_access: Literal["enable", "disable"] | None = ...,
        legacy_authentication: Literal["disable", "enable"] | None = ...,
        downstream_accprofile: str | None = ...,
        configuration_sync: Literal["default", "local"] | None = ...,
        fabric_object_unification: Literal["default", "local"] | None = ...,
        saml_configuration_sync: Literal["default", "local"] | None = ...,
        trusted_list: str | list[str] | list[CsfTrustedlistItem] | None = ...,
        fabric_connector: str | list[str] | list[CsfFabricconnectorItem] | None = ...,
        forticloud_account_enforcement: Literal["enable", "disable"] | None = ...,
        file_mgmt: Literal["enable", "disable"] | None = ...,
        file_quota: int | None = ...,
        file_quota_warning: int | None = ...,
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
    "Csf",
    "CsfPayload",
    "CsfResponse",
    "CsfObject",
]