""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/ldap
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

class LdapPayload(TypedDict, total=False):
    """Payload type for Ldap operations."""
    name: str
    server: str
    secondary_server: str
    tertiary_server: str
    status_ttl: int
    server_identity_check: Literal["enable", "disable"]
    source_ip: str
    source_ip_interface: str
    source_port: int
    cnid: str
    dn: str
    type: Literal["simple", "anonymous", "regular"]
    two_factor: Literal["disable", "fortitoken-cloud"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    two_factor_filter: str
    username: str
    password: str
    group_member_check: Literal["user-attr", "group-object", "posix-group-object"]
    group_search_base: str
    group_object_filter: str
    group_filter: str
    secure: Literal["disable", "starttls", "ldaps"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    ca_cert: str
    port: int
    password_expiry_warning: Literal["enable", "disable"]
    password_renewal: Literal["enable", "disable"]
    member_attr: str
    account_key_processing: Literal["same", "strip"]
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]
    account_key_filter: str
    search_type: str | list[str]
    client_cert_auth: Literal["enable", "disable"]
    client_cert: str
    obtain_user_info: Literal["enable", "disable"]
    user_info_exchange_server: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    antiphish: Literal["enable", "disable"]
    password_attr: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LdapResponse(TypedDict, total=False):
    """Response type for Ldap - use with .dict property for typed dict access."""
    name: str
    server: str
    secondary_server: str
    tertiary_server: str
    status_ttl: int
    server_identity_check: Literal["enable", "disable"]
    source_ip: str
    source_ip_interface: str
    source_port: int
    cnid: str
    dn: str
    type: Literal["simple", "anonymous", "regular"]
    two_factor: Literal["disable", "fortitoken-cloud"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    two_factor_filter: str
    username: str
    password: str
    group_member_check: Literal["user-attr", "group-object", "posix-group-object"]
    group_search_base: str
    group_object_filter: str
    group_filter: str
    secure: Literal["disable", "starttls", "ldaps"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    ca_cert: str
    port: int
    password_expiry_warning: Literal["enable", "disable"]
    password_renewal: Literal["enable", "disable"]
    member_attr: str
    account_key_processing: Literal["same", "strip"]
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]
    account_key_filter: str
    search_type: str
    client_cert_auth: Literal["enable", "disable"]
    client_cert: str
    obtain_user_info: Literal["enable", "disable"]
    user_info_exchange_server: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    antiphish: Literal["enable", "disable"]
    password_attr: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LdapObject(FortiObject):
    """Typed FortiObject for Ldap with field access."""
    name: str
    server: str
    secondary_server: str
    tertiary_server: str
    status_ttl: int
    server_identity_check: Literal["enable", "disable"]
    source_ip: str
    source_ip_interface: str
    source_port: int
    cnid: str
    dn: str
    type: Literal["simple", "anonymous", "regular"]
    two_factor: Literal["disable", "fortitoken-cloud"]
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    two_factor_notification: Literal["email", "sms"]
    two_factor_filter: str
    username: str
    password: str
    group_member_check: Literal["user-attr", "group-object", "posix-group-object"]
    group_search_base: str
    group_object_filter: str
    group_filter: str
    secure: Literal["disable", "starttls", "ldaps"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    ca_cert: str
    port: int
    password_expiry_warning: Literal["enable", "disable"]
    password_renewal: Literal["enable", "disable"]
    member_attr: str
    account_key_processing: Literal["same", "strip"]
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]
    account_key_filter: str
    search_type: str
    client_cert_auth: Literal["enable", "disable"]
    client_cert: str
    obtain_user_info: Literal["enable", "disable"]
    user_info_exchange_server: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    antiphish: Literal["enable", "disable"]
    password_attr: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Ldap:
    """
    
    Endpoint: user/ldap
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
    ) -> LdapObject: ...
    
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
    ) -> FortiObjectList[LdapObject]: ...
    
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
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: str | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LdapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: str | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LdapObject: ...

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
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
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
    "Ldap",
    "LdapPayload",
    "LdapResponse",
    "LdapObject",
]