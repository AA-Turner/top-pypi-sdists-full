""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: authentication/scheme
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

class SchemeUserdatabaseItem(TypedDict, total=False):
    """Nested item for user-database field."""
    name: str


class SchemePayload(TypedDict, total=False):
    """Payload type for Scheme operations."""
    name: str
    method: str | list[str]
    negotiate_ntlm: Literal["enable", "disable"]
    kerberos_keytab: str
    domain_controller: str
    saml_server: str
    saml_timeout: int
    fsso_agent_for_ntlm: str
    require_tfa: Literal["enable", "disable"]
    fsso_guest: Literal["enable", "disable"]
    user_cert: Literal["enable", "disable"]
    cert_http_header: Literal["enable", "disable"]
    user_database: str | list[str] | list[SchemeUserdatabaseItem]
    ssh_ca: str
    external_idp: str
    group_attr_type: Literal["display-name", "external-id"]
    digest_algo: str | list[str]
    digest_rfc2069: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SchemeResponse(TypedDict, total=False):
    """Response type for Scheme - use with .dict property for typed dict access."""
    name: str
    method: str
    negotiate_ntlm: Literal["enable", "disable"]
    kerberos_keytab: str
    domain_controller: str
    saml_server: str
    saml_timeout: int
    fsso_agent_for_ntlm: str
    require_tfa: Literal["enable", "disable"]
    fsso_guest: Literal["enable", "disable"]
    user_cert: Literal["enable", "disable"]
    cert_http_header: Literal["enable", "disable"]
    user_database: list[SchemeUserdatabaseItem]
    ssh_ca: str
    external_idp: str
    group_attr_type: Literal["display-name", "external-id"]
    digest_algo: str
    digest_rfc2069: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SchemeUserdatabaseItemObject(FortiObject[SchemeUserdatabaseItem]):
    """Typed object for user-database table items with attribute access."""
    name: str


class SchemeObject(FortiObject):
    """Typed FortiObject for Scheme with field access."""
    name: str
    method: str
    negotiate_ntlm: Literal["enable", "disable"]
    kerberos_keytab: str
    domain_controller: str
    saml_server: str
    saml_timeout: int
    fsso_agent_for_ntlm: str
    require_tfa: Literal["enable", "disable"]
    fsso_guest: Literal["enable", "disable"]
    user_cert: Literal["enable", "disable"]
    cert_http_header: Literal["enable", "disable"]
    user_database: FortiObjectList[SchemeUserdatabaseItemObject]
    ssh_ca: str
    external_idp: str
    group_attr_type: Literal["display-name", "external-id"]
    digest_algo: str
    digest_rfc2069: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Scheme:
    """
    
    Endpoint: authentication/scheme
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
    ) -> SchemeObject: ...
    
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
    ) -> FortiObjectList[SchemeObject]: ...
    
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
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: str | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[SchemeUserdatabaseItem] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: str | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SchemeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: str | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[SchemeUserdatabaseItem] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: str | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SchemeObject: ...

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
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[SchemeUserdatabaseItem] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
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
    "Scheme",
    "SchemePayload",
    "SchemeResponse",
    "SchemeObject",
]