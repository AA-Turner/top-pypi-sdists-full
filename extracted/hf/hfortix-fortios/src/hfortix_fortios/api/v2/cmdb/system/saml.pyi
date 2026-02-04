""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/saml
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

class SamlServiceprovidersAssertionattributesItem(TypedDict, total=False):
    """Nested item for service-providers.assertion-attributes field."""
    name: str
    type: Literal["username", "email", "profile-name"]


class SamlServiceprovidersItem(TypedDict, total=False):
    """Nested item for service-providers field."""
    name: str
    prefix: str
    sp_binding_protocol: Literal["post", "redirect"]
    sp_cert: str
    sp_entity_id: str
    sp_single_sign_on_url: str
    sp_single_logout_url: str
    sp_portal_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    assertion_attributes: str | list[str] | list[SamlServiceprovidersAssertionattributesItem]


class SamlPayload(TypedDict, total=False):
    """Payload type for Saml operations."""
    status: Literal["enable", "disable"]
    role: Literal["identity-provider", "service-provider"]
    default_login_page: Literal["normal", "sso"]
    default_profile: str
    cert: str
    binding_protocol: Literal["post", "redirect"]
    portal_url: str
    entity_id: str
    single_sign_on_url: str
    single_logout_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    idp_cert: str
    server_address: str
    require_signed_resp_and_asrt: Literal["enable", "disable"]
    tolerance: int
    life: int
    service_providers: str | list[str] | list[SamlServiceprovidersItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SamlResponse(TypedDict, total=False):
    """Response type for Saml - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    role: Literal["identity-provider", "service-provider"]
    default_login_page: Literal["normal", "sso"]
    default_profile: str
    cert: str
    binding_protocol: Literal["post", "redirect"]
    portal_url: str
    entity_id: str
    single_sign_on_url: str
    single_logout_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    idp_cert: str
    server_address: str
    require_signed_resp_and_asrt: Literal["enable", "disable"]
    tolerance: int
    life: int
    service_providers: list[SamlServiceprovidersItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SamlServiceprovidersAssertionattributesItemObject(FortiObject[SamlServiceprovidersAssertionattributesItem]):
    """Typed object for service-providers.assertion-attributes table items with attribute access."""
    name: str
    type: Literal["username", "email", "profile-name"]


class SamlServiceprovidersItemObject(FortiObject[SamlServiceprovidersItem]):
    """Typed object for service-providers table items with attribute access."""
    name: str
    prefix: str
    sp_binding_protocol: Literal["post", "redirect"]
    sp_cert: str
    sp_entity_id: str
    sp_single_sign_on_url: str
    sp_single_logout_url: str
    sp_portal_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    assertion_attributes: FortiObjectList[SamlServiceprovidersAssertionattributesItemObject]


class SamlObject(FortiObject):
    """Typed FortiObject for Saml with field access."""
    status: Literal["enable", "disable"]
    role: Literal["identity-provider", "service-provider"]
    default_login_page: Literal["normal", "sso"]
    default_profile: str
    cert: str
    binding_protocol: Literal["post", "redirect"]
    portal_url: str
    entity_id: str
    single_sign_on_url: str
    single_logout_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    idp_cert: str
    server_address: str
    require_signed_resp_and_asrt: Literal["enable", "disable"]
    tolerance: int
    life: int
    service_providers: FortiObjectList[SamlServiceprovidersItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Saml:
    """
    
    Endpoint: system/saml
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
    ) -> SamlObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SamlPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        role: Literal["identity-provider", "service-provider"] | None = ...,
        default_login_page: Literal["normal", "sso"] | None = ...,
        default_profile: str | None = ...,
        cert: str | None = ...,
        binding_protocol: Literal["post", "redirect"] | None = ...,
        portal_url: str | None = ...,
        entity_id: str | None = ...,
        single_sign_on_url: str | None = ...,
        single_logout_url: str | None = ...,
        idp_entity_id: str | None = ...,
        idp_single_sign_on_url: str | None = ...,
        idp_single_logout_url: str | None = ...,
        idp_cert: str | None = ...,
        server_address: str | None = ...,
        require_signed_resp_and_asrt: Literal["enable", "disable"] | None = ...,
        tolerance: int | None = ...,
        life: int | None = ...,
        service_providers: str | list[str] | list[SamlServiceprovidersItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SamlObject: ...


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
        payload_dict: SamlPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        role: Literal["identity-provider", "service-provider"] | None = ...,
        default_login_page: Literal["normal", "sso"] | None = ...,
        default_profile: str | None = ...,
        cert: str | None = ...,
        binding_protocol: Literal["post", "redirect"] | None = ...,
        portal_url: str | None = ...,
        entity_id: str | None = ...,
        single_sign_on_url: str | None = ...,
        single_logout_url: str | None = ...,
        idp_entity_id: str | None = ...,
        idp_single_sign_on_url: str | None = ...,
        idp_single_logout_url: str | None = ...,
        idp_cert: str | None = ...,
        server_address: str | None = ...,
        require_signed_resp_and_asrt: Literal["enable", "disable"] | None = ...,
        tolerance: int | None = ...,
        life: int | None = ...,
        service_providers: str | list[str] | list[SamlServiceprovidersItem] | None = ...,
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
    "Saml",
    "SamlPayload",
    "SamlResponse",
    "SamlObject",
]