""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/available_certificates
Category: monitor
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

class AvailableCertificatesPayload(TypedDict, total=False):
    """Payload type for AvailableCertificates operations."""
    scope: Literal["vdom", "global"]
    with_remote: bool
    with_ca: bool
    with_crl: bool
    mkey: str
    find_all_references: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class AvailableCertificatesResponse(TypedDict, total=False):
    """Response type for AvailableCertificates - use with .dict property for typed dict access."""
    name: str
    status: str
    source: str
    comments: str
    range: str
    exists: bool
    is_ssl_server_cert: bool
    is_ssl_client_cert: bool
    is_proxy_ssl_cert: bool
    is_general_allowable_cert: bool
    is_default_local: bool
    is_built_in: bool
    is_wifi_cert: bool
    is_deep_inspection_cert: bool
    trusted: bool
    has_valid_cert_key: bool
    saml_sig_algo_supported: bool
    revoked_serials: list[str]
    key_type: str
    key_size: int
    cert_protocol: str
    is_local_ca_cert: bool
    type: str
    lastupdate: int
    nextupdate: int
    lastupdate_raw: str
    nextupdate_raw: str
    valid_from: int
    valid_to: int
    valid_from_raw: str
    valid_to_raw: str
    signature_algorithm: str
    subject: str
    subject_raw: str
    issuer: str
    issuer_raw: str
    fingerprint: str
    version: int
    is_ca: bool
    serial_number: str
    q_path: str
    q_name: str
    q_ref: int
    q_static: bool
    q_type: int
    ext: list[str]
    acme_status: str


class AvailableCertificatesObject(FortiObject[AvailableCertificatesResponse]):
    """Typed FortiObject for AvailableCertificates with field access."""
    name: str
    status: str
    source: str
    comments: str
    range: str
    exists: bool
    is_ssl_server_cert: bool
    is_ssl_client_cert: bool
    is_proxy_ssl_cert: bool
    is_general_allowable_cert: bool
    is_default_local: bool
    is_built_in: bool
    is_wifi_cert: bool
    is_deep_inspection_cert: bool
    trusted: bool
    has_valid_cert_key: bool
    saml_sig_algo_supported: bool
    revoked_serials: list[str]
    key_type: str
    key_size: int
    cert_protocol: str
    is_local_ca_cert: bool
    type: str
    lastupdate: int
    nextupdate: int
    lastupdate_raw: str
    nextupdate_raw: str
    valid_from: int
    valid_to: int
    valid_from_raw: str
    valid_to_raw: str
    signature_algorithm: str
    subject: str
    subject_raw: str
    issuer: str
    issuer_raw: str
    fingerprint: str
    version: int
    is_ca: bool
    serial_number: str
    q_path: str
    q_name: str
    q_ref: int
    q_static: bool
    q_type: int
    ext: list[str]
    acme_status: str



# ================================================================
# Main Endpoint Class
# ================================================================

class AvailableCertificates:
    """
    
    Endpoint: system/available_certificates
    Category: monitor
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        scope: Literal["vdom", "global"] | None = ...,
        with_remote: bool | None = ...,
        with_ca: bool | None = ...,
        with_crl: bool | None = ...,
        mkey: str | None = ...,
        find_all_references: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[AvailableCertificatesObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AvailableCertificatesPayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        with_remote: bool | None = ...,
        with_ca: bool | None = ...,
        with_crl: bool | None = ...,
        mkey: str | None = ...,
        find_all_references: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AvailableCertificatesObject: ...




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
        payload_dict: AvailableCertificatesPayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        with_remote: bool | None = ...,
        with_ca: bool | None = ...,
        with_crl: bool | None = ...,
        mkey: str | None = ...,
        find_all_references: bool | None = ...,
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
    "AvailableCertificates",
    "AvailableCertificatesResponse",
    "AvailableCertificatesObject",
]