""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/local
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

class LocalPayload(TypedDict, total=False):
    """Payload type for Local operations."""
    name: str
    id: int
    status: Literal["enable", "disable"]
    type: Literal["password", "radius", "tacacs+", "ldap", "saml"]
    passwd: str
    ldap_server: str
    radius_server: str
    tacacs_plus_server: str
    saml_server: str
    two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    fortitoken: str
    email_to: str
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    sms_phone: str
    passwd_policy: str
    passwd_time: str
    authtimeout: int
    workstation: str
    auth_concurrent_override: Literal["enable", "disable"]
    auth_concurrent_value: int
    ppk_secret: str
    ppk_identity: str
    qkd_profile: str
    username_sensitivity: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LocalResponse(TypedDict, total=False):
    """Response type for Local - use with .dict property for typed dict access."""
    name: str
    id: int
    status: Literal["enable", "disable"]
    type: Literal["password", "radius", "tacacs+", "ldap", "saml"]
    passwd: str
    ldap_server: str
    radius_server: str
    tacacs_plus_server: str
    saml_server: str
    two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    fortitoken: str
    email_to: str
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    sms_phone: str
    passwd_policy: str
    passwd_time: str
    authtimeout: int
    workstation: str
    auth_concurrent_override: Literal["enable", "disable"]
    auth_concurrent_value: int
    ppk_secret: str
    ppk_identity: str
    qkd_profile: str
    username_sensitivity: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LocalObject(FortiObject):
    """Typed FortiObject for Local with field access."""
    name: str
    id: int
    status: Literal["enable", "disable"]
    type: Literal["password", "radius", "tacacs+", "ldap", "saml"]
    passwd: str
    ldap_server: str
    radius_server: str
    tacacs_plus_server: str
    saml_server: str
    two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    fortitoken: str
    email_to: str
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    sms_phone: str
    passwd_policy: str
    passwd_time: str
    authtimeout: int
    workstation: str
    auth_concurrent_override: Literal["enable", "disable"]
    auth_concurrent_value: int
    ppk_secret: str
    ppk_identity: str
    qkd_profile: str
    username_sensitivity: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Local:
    """
    
    Endpoint: user/local
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
    ) -> LocalObject: ...
    
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
    ) -> FortiObjectList[LocalObject]: ...
    
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
        payload_dict: LocalPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["password", "radius", "tacacs+", "ldap", "saml"] | None = ...,
        passwd: str | None = ...,
        ldap_server: str | None = ...,
        radius_server: str | None = ...,
        tacacs_plus_server: str | None = ...,
        saml_server: str | None = ...,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        fortitoken: str | None = ...,
        email_to: str | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        sms_phone: str | None = ...,
        passwd_policy: str | None = ...,
        passwd_time: str | None = ...,
        authtimeout: int | None = ...,
        workstation: str | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        ppk_secret: str | None = ...,
        ppk_identity: str | None = ...,
        qkd_profile: str | None = ...,
        username_sensitivity: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LocalPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["password", "radius", "tacacs+", "ldap", "saml"] | None = ...,
        passwd: str | None = ...,
        ldap_server: str | None = ...,
        radius_server: str | None = ...,
        tacacs_plus_server: str | None = ...,
        saml_server: str | None = ...,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        fortitoken: str | None = ...,
        email_to: str | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        sms_phone: str | None = ...,
        passwd_policy: str | None = ...,
        passwd_time: str | None = ...,
        authtimeout: int | None = ...,
        workstation: str | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        ppk_secret: str | None = ...,
        ppk_identity: str | None = ...,
        qkd_profile: str | None = ...,
        username_sensitivity: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalObject: ...

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
        payload_dict: LocalPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["password", "radius", "tacacs+", "ldap", "saml"] | None = ...,
        passwd: str | None = ...,
        ldap_server: str | None = ...,
        radius_server: str | None = ...,
        tacacs_plus_server: str | None = ...,
        saml_server: str | None = ...,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        fortitoken: str | None = ...,
        email_to: str | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        sms_phone: str | None = ...,
        passwd_policy: str | None = ...,
        passwd_time: str | None = ...,
        authtimeout: int | None = ...,
        workstation: str | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        ppk_secret: str | None = ...,
        ppk_identity: str | None = ...,
        qkd_profile: str | None = ...,
        username_sensitivity: Literal["disable", "enable"] | None = ...,
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
    "Local",
    "LocalPayload",
    "LocalResponse",
    "LocalObject",
]