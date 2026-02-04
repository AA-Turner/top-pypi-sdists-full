""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/saml
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

class SamlPayload(TypedDict, total=False):
    """Payload type for Saml operations."""
    name: str
    cert: str
    entity_id: str
    single_sign_on_url: str
    single_logout_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    idp_cert: str
    scim_client: str
    scim_user_attr_type: Literal["user-name", "display-name", "external-id", "email"]
    scim_group_attr_type: Literal["display-name", "external-id"]
    user_name: str
    group_name: str
    digest_method: Literal["sha1", "sha256"]
    require_signed_resp_and_asrt: Literal["enable", "disable"]
    limit_relaystate: Literal["enable", "disable"]
    clock_tolerance: int
    adfs_claim: Literal["enable", "disable"]
    user_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
    group_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
    reauth: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SamlResponse(TypedDict, total=False):
    """Response type for Saml - use with .dict property for typed dict access."""
    name: str
    cert: str
    entity_id: str
    single_sign_on_url: str
    single_logout_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    idp_cert: str
    scim_client: str
    scim_user_attr_type: Literal["user-name", "display-name", "external-id", "email"]
    scim_group_attr_type: Literal["display-name", "external-id"]
    user_name: str
    group_name: str
    digest_method: Literal["sha1", "sha256"]
    require_signed_resp_and_asrt: Literal["enable", "disable"]
    limit_relaystate: Literal["enable", "disable"]
    clock_tolerance: int
    adfs_claim: Literal["enable", "disable"]
    user_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
    group_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
    reauth: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SamlObject(FortiObject):
    """Typed FortiObject for Saml with field access."""
    name: str
    cert: str
    entity_id: str
    single_sign_on_url: str
    single_logout_url: str
    idp_entity_id: str
    idp_single_sign_on_url: str
    idp_single_logout_url: str
    idp_cert: str
    scim_client: str
    scim_user_attr_type: Literal["user-name", "display-name", "external-id", "email"]
    scim_group_attr_type: Literal["display-name", "external-id"]
    user_name: str
    group_name: str
    digest_method: Literal["sha1", "sha256"]
    require_signed_resp_and_asrt: Literal["enable", "disable"]
    limit_relaystate: Literal["enable", "disable"]
    clock_tolerance: int
    adfs_claim: Literal["enable", "disable"]
    user_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
    group_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
    reauth: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Saml:
    """
    
    Endpoint: user/saml
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
    ) -> SamlObject: ...
    
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
    ) -> FortiObjectList[SamlObject]: ...
    
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
        payload_dict: SamlPayload | None = ...,
        name: str | None = ...,
        cert: str | None = ...,
        entity_id: str | None = ...,
        single_sign_on_url: str | None = ...,
        single_logout_url: str | None = ...,
        idp_entity_id: str | None = ...,
        idp_single_sign_on_url: str | None = ...,
        idp_single_logout_url: str | None = ...,
        idp_cert: str | None = ...,
        scim_client: str | None = ...,
        scim_user_attr_type: Literal["user-name", "display-name", "external-id", "email"] | None = ...,
        scim_group_attr_type: Literal["display-name", "external-id"] | None = ...,
        user_name: str | None = ...,
        group_name: str | None = ...,
        digest_method: Literal["sha1", "sha256"] | None = ...,
        require_signed_resp_and_asrt: Literal["enable", "disable"] | None = ...,
        limit_relaystate: Literal["enable", "disable"] | None = ...,
        clock_tolerance: int | None = ...,
        adfs_claim: Literal["enable", "disable"] | None = ...,
        user_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"] | None = ...,
        group_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"] | None = ...,
        reauth: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SamlObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SamlPayload | None = ...,
        name: str | None = ...,
        cert: str | None = ...,
        entity_id: str | None = ...,
        single_sign_on_url: str | None = ...,
        single_logout_url: str | None = ...,
        idp_entity_id: str | None = ...,
        idp_single_sign_on_url: str | None = ...,
        idp_single_logout_url: str | None = ...,
        idp_cert: str | None = ...,
        scim_client: str | None = ...,
        scim_user_attr_type: Literal["user-name", "display-name", "external-id", "email"] | None = ...,
        scim_group_attr_type: Literal["display-name", "external-id"] | None = ...,
        user_name: str | None = ...,
        group_name: str | None = ...,
        digest_method: Literal["sha1", "sha256"] | None = ...,
        require_signed_resp_and_asrt: Literal["enable", "disable"] | None = ...,
        limit_relaystate: Literal["enable", "disable"] | None = ...,
        clock_tolerance: int | None = ...,
        adfs_claim: Literal["enable", "disable"] | None = ...,
        user_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"] | None = ...,
        group_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"] | None = ...,
        reauth: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SamlObject: ...

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
        payload_dict: SamlPayload | None = ...,
        name: str | None = ...,
        cert: str | None = ...,
        entity_id: str | None = ...,
        single_sign_on_url: str | None = ...,
        single_logout_url: str | None = ...,
        idp_entity_id: str | None = ...,
        idp_single_sign_on_url: str | None = ...,
        idp_single_logout_url: str | None = ...,
        idp_cert: str | None = ...,
        scim_client: str | None = ...,
        scim_user_attr_type: Literal["user-name", "display-name", "external-id", "email"] | None = ...,
        scim_group_attr_type: Literal["display-name", "external-id"] | None = ...,
        user_name: str | None = ...,
        group_name: str | None = ...,
        digest_method: Literal["sha1", "sha256"] | None = ...,
        require_signed_resp_and_asrt: Literal["enable", "disable"] | None = ...,
        limit_relaystate: Literal["enable", "disable"] | None = ...,
        clock_tolerance: int | None = ...,
        adfs_claim: Literal["enable", "disable"] | None = ...,
        user_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"] | None = ...,
        group_claim_type: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"] | None = ...,
        reauth: Literal["enable", "disable"] | None = ...,
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
    "Saml",
    "SamlPayload",
    "SamlResponse",
    "SamlObject",
]