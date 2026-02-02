""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn_certificate/csr/generate
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

class GeneratePayload(TypedDict, total=False):
    """Payload type for Generate operations."""
    certname: str
    subject: str
    keytype: Literal["rsa", "ec"]
    keysize: Literal["1024", "1536", "2048", "4096"]
    curvename: Literal["secp256r1", "secp384r1", "secp521r1"]
    orgunits: list[str]
    org: str
    city: str
    state: str
    countrycode: str
    email: str
    subject_alt_name: str
    password: str
    scep_url: str
    scep_password: str
    scope: Literal["vdom", "global"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GenerateResponse(TypedDict, total=False):
    """Response type for Generate - use with .dict property for typed dict access."""
    certname: str
    subject: str
    keytype: Literal["rsa", "ec"]
    keysize: Literal["1024", "1536", "2048", "4096"]
    curvename: Literal["secp256r1", "secp384r1", "secp521r1"]
    orgunits: list[str]
    org: str
    city: str
    state: str
    countrycode: str
    email: str
    subject_alt_name: str
    password: str
    scep_url: str
    scep_password: str
    scope: Literal["vdom", "global"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GenerateObject(FortiObject):
    """Typed FortiObject for Generate with field access."""
    certname: str
    subject: str
    keytype: Literal["rsa", "ec"]
    keysize: Literal["1024", "1536", "2048", "4096"]
    curvename: Literal["secp256r1", "secp384r1", "secp521r1"]
    orgunits: list[str]
    org: str
    city: str
    state: str
    countrycode: str
    email: str
    subject_alt_name: str
    password: str
    scep_url: str
    scep_password: str
    scope: Literal["vdom", "global"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Generate:
    """
    
    Endpoint: vpn_certificate/csr/generate
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
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GenerateObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: GeneratePayload | None = ...,
        certname: str | None = ...,
        subject: str | None = ...,
        keytype: Literal["rsa", "ec"] | None = ...,
        keysize: Literal["1024", "1536", "2048", "4096"] | None = ...,
        curvename: Literal["secp256r1", "secp384r1", "secp521r1"] | None = ...,
        orgunits: list[str] | None = ...,
        org: str | None = ...,
        city: str | None = ...,
        state: str | None = ...,
        countrycode: str | None = ...,
        email: str | None = ...,
        subject_alt_name: str | None = ...,
        password: str | None = ...,
        scep_url: str | None = ...,
        scep_password: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GenerateObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GeneratePayload | None = ...,
        certname: str | None = ...,
        subject: str | None = ...,
        keytype: Literal["rsa", "ec"] | None = ...,
        keysize: Literal["1024", "1536", "2048", "4096"] | None = ...,
        curvename: Literal["secp256r1", "secp384r1", "secp521r1"] | None = ...,
        orgunits: list[str] | None = ...,
        org: str | None = ...,
        city: str | None = ...,
        state: str | None = ...,
        countrycode: str | None = ...,
        email: str | None = ...,
        subject_alt_name: str | None = ...,
        password: str | None = ...,
        scep_url: str | None = ...,
        scep_password: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GenerateObject: ...


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
        payload_dict: GeneratePayload | None = ...,
        certname: str | None = ...,
        subject: str | None = ...,
        keytype: Literal["rsa", "ec"] | None = ...,
        keysize: Literal["1024", "1536", "2048", "4096"] | None = ...,
        curvename: Literal["secp256r1", "secp384r1", "secp521r1"] | None = ...,
        orgunits: list[str] | None = ...,
        org: str | None = ...,
        city: str | None = ...,
        state: str | None = ...,
        countrycode: str | None = ...,
        email: str | None = ...,
        subject_alt_name: str | None = ...,
        password: str | None = ...,
        scep_url: str | None = ...,
        scep_password: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
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
    "Generate",
    "GeneratePayload",
    "GenerateResponse",
    "GenerateObject",
]