""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: certificate/local
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
    password: str
    comments: str
    private_key: str
    certificate: str
    csr: str
    state: str
    scep_url: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    auto_regenerate_days: int
    auto_regenerate_days_warning: int
    scep_password: str
    ca_identifier: str
    name_encoding: Literal["printable", "utf8"]
    source_ip: str
    ike_localid: str
    ike_localid_type: Literal["asn1dn", "fqdn"]
    enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"]
    private_key_retain: Literal["enable", "disable"]
    cmp_server: str
    cmp_path: str
    cmp_server_cert: str
    cmp_regeneration_method: Literal["keyupate", "renewal"]
    acme_ca_url: str
    acme_domain: str
    acme_email: str
    acme_eab_key_id: str
    acme_eab_key_hmac: str
    acme_rsa_key_size: int
    acme_renew_window: int
    est_server: str
    est_ca_id: str
    est_http_username: str
    est_http_password: str
    est_client_cert: str
    est_server_cert: str
    est_srp_username: str
    est_srp_password: str
    est_regeneration_method: Literal["create-new-key", "use-existing-key"]
    details: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LocalResponse(TypedDict, total=False):
    """Response type for Local - use with .dict property for typed dict access."""
    name: str
    password: str
    comments: str
    private_key: str
    certificate: str
    csr: str
    state: str
    scep_url: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    auto_regenerate_days: int
    auto_regenerate_days_warning: int
    scep_password: str
    ca_identifier: str
    name_encoding: Literal["printable", "utf8"]
    source_ip: str
    ike_localid: str
    ike_localid_type: Literal["asn1dn", "fqdn"]
    enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"]
    private_key_retain: Literal["enable", "disable"]
    cmp_server: str
    cmp_path: str
    cmp_server_cert: str
    cmp_regeneration_method: Literal["keyupate", "renewal"]
    acme_ca_url: str
    acme_domain: str
    acme_email: str
    acme_eab_key_id: str
    acme_eab_key_hmac: str
    acme_rsa_key_size: int
    acme_renew_window: int
    est_server: str
    est_ca_id: str
    est_http_username: str
    est_http_password: str
    est_client_cert: str
    est_server_cert: str
    est_srp_username: str
    est_srp_password: str
    est_regeneration_method: Literal["create-new-key", "use-existing-key"]
    details: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LocalObject(FortiObject):
    """Typed FortiObject for Local with field access."""
    name: str
    password: str
    comments: str
    private_key: str
    certificate: str
    csr: str
    state: str
    scep_url: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    auto_regenerate_days: int
    auto_regenerate_days_warning: int
    scep_password: str
    ca_identifier: str
    name_encoding: Literal["printable", "utf8"]
    source_ip: str
    ike_localid: str
    ike_localid_type: Literal["asn1dn", "fqdn"]
    enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"]
    private_key_retain: Literal["enable", "disable"]
    cmp_server: str
    cmp_path: str
    cmp_server_cert: str
    cmp_regeneration_method: Literal["keyupate", "renewal"]
    acme_ca_url: str
    acme_domain: str
    acme_email: str
    acme_eab_key_id: str
    acme_eab_key_hmac: str
    acme_rsa_key_size: int
    acme_renew_window: int
    est_server: str
    est_ca_id: str
    est_http_username: str
    est_http_password: str
    est_client_cert: str
    est_server_cert: str
    est_srp_username: str
    est_srp_password: str
    est_regeneration_method: Literal["create-new-key", "use-existing-key"]
    details: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Local:
    """
    
    Endpoint: certificate/local
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[LocalObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LocalPayload | None = ...,
        name: str | None = ...,
        password: str | None = ...,
        comments: str | None = ...,
        private_key: str | None = ...,
        certificate: str | None = ...,
        csr: str | None = ...,
        state: str | None = ...,
        scep_url: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        auto_regenerate_days: int | None = ...,
        auto_regenerate_days_warning: int | None = ...,
        scep_password: str | None = ...,
        ca_identifier: str | None = ...,
        name_encoding: Literal["printable", "utf8"] | None = ...,
        source_ip: str | None = ...,
        ike_localid: str | None = ...,
        ike_localid_type: Literal["asn1dn", "fqdn"] | None = ...,
        enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"] | None = ...,
        private_key_retain: Literal["enable", "disable"] | None = ...,
        cmp_server: str | None = ...,
        cmp_path: str | None = ...,
        cmp_server_cert: str | None = ...,
        cmp_regeneration_method: Literal["keyupate", "renewal"] | None = ...,
        acme_ca_url: str | None = ...,
        acme_domain: str | None = ...,
        acme_email: str | None = ...,
        acme_eab_key_id: str | None = ...,
        acme_eab_key_hmac: str | None = ...,
        acme_rsa_key_size: int | None = ...,
        acme_renew_window: int | None = ...,
        est_server: str | None = ...,
        est_ca_id: str | None = ...,
        est_http_username: str | None = ...,
        est_http_password: str | None = ...,
        est_client_cert: str | None = ...,
        est_server_cert: str | None = ...,
        est_srp_username: str | None = ...,
        est_srp_password: str | None = ...,
        est_regeneration_method: Literal["create-new-key", "use-existing-key"] | None = ...,
        details: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: LocalPayload | None = ...,
        name: str | None = ...,
        password: str | None = ...,
        comments: str | None = ...,
        private_key: str | None = ...,
        certificate: str | None = ...,
        csr: str | None = ...,
        state: str | None = ...,
        scep_url: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        auto_regenerate_days: int | None = ...,
        auto_regenerate_days_warning: int | None = ...,
        scep_password: str | None = ...,
        ca_identifier: str | None = ...,
        name_encoding: Literal["printable", "utf8"] | None = ...,
        source_ip: str | None = ...,
        ike_localid: str | None = ...,
        ike_localid_type: Literal["asn1dn", "fqdn"] | None = ...,
        enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"] | None = ...,
        private_key_retain: Literal["enable", "disable"] | None = ...,
        cmp_server: str | None = ...,
        cmp_path: str | None = ...,
        cmp_server_cert: str | None = ...,
        cmp_regeneration_method: Literal["keyupate", "renewal"] | None = ...,
        acme_ca_url: str | None = ...,
        acme_domain: str | None = ...,
        acme_email: str | None = ...,
        acme_eab_key_id: str | None = ...,
        acme_eab_key_hmac: str | None = ...,
        acme_rsa_key_size: int | None = ...,
        acme_renew_window: int | None = ...,
        est_server: str | None = ...,
        est_ca_id: str | None = ...,
        est_http_username: str | None = ...,
        est_http_password: str | None = ...,
        est_client_cert: str | None = ...,
        est_server_cert: str | None = ...,
        est_srp_username: str | None = ...,
        est_srp_password: str | None = ...,
        est_regeneration_method: Literal["create-new-key", "use-existing-key"] | None = ...,
        details: str | None = ...,
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