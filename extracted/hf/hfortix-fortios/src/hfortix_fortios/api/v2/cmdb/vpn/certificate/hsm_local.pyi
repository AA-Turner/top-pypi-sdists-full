""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/certificate/hsm_local
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

class HsmLocalPayload(TypedDict, total=False):
    """Payload type for HsmLocal operations."""
    name: str
    comments: str
    vendor: Literal["unknown", "gch"]
    api_version: Literal["unknown", "gch-default"]
    certificate: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    gch_url: str
    gch_project: str
    gch_location: str
    gch_keyring: str
    gch_cryptokey: str
    gch_cryptokey_version: str
    gch_cloud_service_name: str
    gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"]
    details: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class HsmLocalResponse(TypedDict, total=False):
    """Response type for HsmLocal - use with .dict property for typed dict access."""
    name: str
    comments: str
    vendor: Literal["unknown", "gch"]
    api_version: Literal["unknown", "gch-default"]
    certificate: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    gch_url: str
    gch_project: str
    gch_location: str
    gch_keyring: str
    gch_cryptokey: str
    gch_cryptokey_version: str
    gch_cloud_service_name: str
    gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"]
    details: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class HsmLocalObject(FortiObject):
    """Typed FortiObject for HsmLocal with field access."""
    name: str
    comments: str
    vendor: Literal["unknown", "gch"]
    api_version: Literal["unknown", "gch-default"]
    certificate: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    gch_url: str
    gch_project: str
    gch_location: str
    gch_keyring: str
    gch_cryptokey: str
    gch_cryptokey_version: str
    gch_cloud_service_name: str
    gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"]
    details: str


# ================================================================
# Main Endpoint Class
# ================================================================

class HsmLocal:
    """
    
    Endpoint: vpn/certificate/hsm_local
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
    ) -> HsmLocalObject: ...
    
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
    ) -> FortiObjectList[HsmLocalObject]: ...
    
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
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HsmLocalObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HsmLocalObject: ...

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
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
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
    "HsmLocal",
    "HsmLocalPayload",
    "HsmLocalResponse",
    "HsmLocalObject",
]