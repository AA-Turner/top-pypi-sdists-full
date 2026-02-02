""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/qkd
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

class QkdCertificateItem(TypedDict, total=False):
    """Nested item for certificate field."""
    name: str


class QkdPayload(TypedDict, total=False):
    """Payload type for Qkd operations."""
    name: str
    server: str
    port: int
    id: str
    peer: str
    certificate: str | list[str] | list[QkdCertificateItem]
    comment: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class QkdResponse(TypedDict, total=False):
    """Response type for Qkd - use with .dict property for typed dict access."""
    name: str
    server: str
    port: int
    id: str
    peer: str
    certificate: list[QkdCertificateItem]
    comment: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class QkdCertificateItemObject(FortiObject[QkdCertificateItem]):
    """Typed object for certificate table items with attribute access."""
    name: str


class QkdObject(FortiObject):
    """Typed FortiObject for Qkd with field access."""
    name: str
    server: str
    port: int
    id: str
    peer: str
    certificate: FortiObjectList[QkdCertificateItemObject]
    comment: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Qkd:
    """
    
    Endpoint: vpn/qkd
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
    ) -> QkdObject: ...
    
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
    ) -> FortiObjectList[QkdObject]: ...
    
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
        payload_dict: QkdPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        port: int | None = ...,
        id: str | None = ...,
        peer: str | None = ...,
        certificate: str | list[str] | list[QkdCertificateItem] | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QkdObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: QkdPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        port: int | None = ...,
        id: str | None = ...,
        peer: str | None = ...,
        certificate: str | list[str] | list[QkdCertificateItem] | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QkdObject: ...

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
        payload_dict: QkdPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        port: int | None = ...,
        id: str | None = ...,
        peer: str | None = ...,
        certificate: str | list[str] | list[QkdCertificateItem] | None = ...,
        comment: str | None = ...,
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
    "Qkd",
    "QkdPayload",
    "QkdResponse",
    "QkdObject",
]