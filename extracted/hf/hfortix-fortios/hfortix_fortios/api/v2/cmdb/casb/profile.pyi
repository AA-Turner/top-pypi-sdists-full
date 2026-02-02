""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: casb/profile
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

class ProfileSaasapplicationSafesearchcontrolItem(TypedDict, total=False):
    """Nested item for saas-application.safe-search-control field."""
    name: str


class ProfileSaasapplicationTenantcontroltenantsItem(TypedDict, total=False):
    """Nested item for saas-application.tenant-control-tenants field."""
    name: str


class ProfileSaasapplicationAdvancedtenantcontrolItem(TypedDict, total=False):
    """Nested item for saas-application.advanced-tenant-control field."""
    name: str
    attribute: str | list[str]


class ProfileSaasapplicationDomaincontroldomainsItem(TypedDict, total=False):
    """Nested item for saas-application.domain-control-domains field."""
    name: str


class ProfileSaasapplicationAccessruleItem(TypedDict, total=False):
    """Nested item for saas-application.access-rule field."""
    name: str
    action: Literal["monitor", "bypass", "block"]
    bypass: Literal["av", "dlp", "web-filter", "file-filter", "video-filter"]
    attribute_filter: str | list[str]


class ProfileSaasapplicationCustomcontrolItem(TypedDict, total=False):
    """Nested item for saas-application.custom-control field."""
    name: str
    option: str | list[str]
    attribute_filter: str | list[str]


class ProfileSaasapplicationItem(TypedDict, total=False):
    """Nested item for saas-application field."""
    name: str
    status: Literal["enable", "disable"]
    safe_search: Literal["enable", "disable"]
    safe_search_control: str | list[str] | list[ProfileSaasapplicationSafesearchcontrolItem]
    tenant_control: Literal["enable", "disable"]
    tenant_control_tenants: str | list[str] | list[ProfileSaasapplicationTenantcontroltenantsItem]
    advanced_tenant_control: str | list[str] | list[ProfileSaasapplicationAdvancedtenantcontrolItem]
    domain_control: Literal["enable", "disable"]
    domain_control_domains: str | list[str] | list[ProfileSaasapplicationDomaincontroldomainsItem]
    log: Literal["enable", "disable"]
    access_rule: str | list[str] | list[ProfileSaasapplicationAccessruleItem]
    custom_control: str | list[str] | list[ProfileSaasapplicationCustomcontrolItem]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    comment: str
    saas_application: str | list[str] | list[ProfileSaasapplicationItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    comment: str
    saas_application: list[ProfileSaasapplicationItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileSaasapplicationSafesearchcontrolItemObject(FortiObject[ProfileSaasapplicationSafesearchcontrolItem]):
    """Typed object for saas-application.safe-search-control table items with attribute access."""
    name: str


class ProfileSaasapplicationTenantcontroltenantsItemObject(FortiObject[ProfileSaasapplicationTenantcontroltenantsItem]):
    """Typed object for saas-application.tenant-control-tenants table items with attribute access."""
    name: str


class ProfileSaasapplicationAdvancedtenantcontrolItemObject(FortiObject[ProfileSaasapplicationAdvancedtenantcontrolItem]):
    """Typed object for saas-application.advanced-tenant-control table items with attribute access."""
    name: str
    attribute: str | list[str]


class ProfileSaasapplicationDomaincontroldomainsItemObject(FortiObject[ProfileSaasapplicationDomaincontroldomainsItem]):
    """Typed object for saas-application.domain-control-domains table items with attribute access."""
    name: str


class ProfileSaasapplicationAccessruleItemObject(FortiObject[ProfileSaasapplicationAccessruleItem]):
    """Typed object for saas-application.access-rule table items with attribute access."""
    name: str
    action: Literal["monitor", "bypass", "block"]
    bypass: Literal["av", "dlp", "web-filter", "file-filter", "video-filter"]
    attribute_filter: str | list[str]


class ProfileSaasapplicationCustomcontrolItemObject(FortiObject[ProfileSaasapplicationCustomcontrolItem]):
    """Typed object for saas-application.custom-control table items with attribute access."""
    name: str
    option: str | list[str]
    attribute_filter: str | list[str]


class ProfileSaasapplicationItemObject(FortiObject[ProfileSaasapplicationItem]):
    """Typed object for saas-application table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    safe_search: Literal["enable", "disable"]
    safe_search_control: FortiObjectList[ProfileSaasapplicationSafesearchcontrolItemObject]
    tenant_control: Literal["enable", "disable"]
    tenant_control_tenants: FortiObjectList[ProfileSaasapplicationTenantcontroltenantsItemObject]
    advanced_tenant_control: FortiObjectList[ProfileSaasapplicationAdvancedtenantcontrolItemObject]
    domain_control: Literal["enable", "disable"]
    domain_control_domains: FortiObjectList[ProfileSaasapplicationDomaincontroldomainsItemObject]
    log: Literal["enable", "disable"]
    access_rule: FortiObjectList[ProfileSaasapplicationAccessruleItemObject]
    custom_control: FortiObjectList[ProfileSaasapplicationCustomcontrolItemObject]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    comment: str
    saas_application: FortiObjectList[ProfileSaasapplicationItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: casb/profile
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
    ) -> ProfileObject: ...
    
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
    ) -> FortiObjectList[ProfileObject]: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        saas_application: str | list[str] | list[ProfileSaasapplicationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        saas_application: str | list[str] | list[ProfileSaasapplicationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        saas_application: str | list[str] | list[ProfileSaasapplicationItem] | None = ...,
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
    "Profile",
    "ProfilePayload",
    "ProfileResponse",
    "ProfileObject",
]