""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: certificate/crl
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

class CrlPayload(TypedDict, total=False):
    """Payload type for Crl operations."""
    name: str
    crl: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    update_vdom: str
    ldap_server: str
    ldap_username: str
    ldap_password: str
    http_url: str
    scep_url: str
    scep_cert: str
    update_interval: int
    source_ip: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CrlResponse(TypedDict, total=False):
    """Response type for Crl - use with .dict property for typed dict access."""
    name: str
    crl: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    update_vdom: str
    ldap_server: str
    ldap_username: str
    ldap_password: str
    http_url: str
    scep_url: str
    scep_cert: str
    update_interval: int
    source_ip: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CrlObject(FortiObject):
    """Typed FortiObject for Crl with field access."""
    name: str
    crl: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    update_vdom: str
    ldap_server: str
    ldap_username: str
    ldap_password: str
    http_url: str
    scep_url: str
    scep_cert: str
    update_interval: int
    source_ip: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Crl:
    """
    
    Endpoint: certificate/crl
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
    ) -> CrlObject: ...
    
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
    ) -> FortiObjectList[CrlObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CrlObject: ...


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
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
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
    "Crl",
    "CrlPayload",
    "CrlResponse",
    "CrlObject",
]