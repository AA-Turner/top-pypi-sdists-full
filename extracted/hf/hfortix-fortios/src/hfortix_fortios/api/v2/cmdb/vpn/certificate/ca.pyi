""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/certificate/ca
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

class CaPayload(TypedDict, total=False):
    """Payload type for Ca operations."""
    name: str
    ca: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    ssl_inspection_trusted: Literal["enable", "disable"]
    scep_url: str
    est_url: str
    auto_update_days: int
    auto_update_days_warning: int
    source_ip: str
    ca_identifier: str
    obsolete: Literal["disable", "enable"]
    fabric_ca: Literal["disable", "enable"]
    details: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CaResponse(TypedDict, total=False):
    """Response type for Ca - use with .dict property for typed dict access."""
    name: str
    ca: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    ssl_inspection_trusted: Literal["enable", "disable"]
    scep_url: str
    est_url: str
    auto_update_days: int
    auto_update_days_warning: int
    source_ip: str
    ca_identifier: str
    obsolete: Literal["disable", "enable"]
    fabric_ca: Literal["disable", "enable"]
    details: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CaObject(FortiObject):
    """Typed FortiObject for Ca with field access."""
    name: str
    ca: str
    range: Literal["global", "vdom"]
    source: Literal["factory", "user", "bundle"]
    ssl_inspection_trusted: Literal["enable", "disable"]
    scep_url: str
    est_url: str
    auto_update_days: int
    auto_update_days_warning: int
    source_ip: str
    ca_identifier: str
    obsolete: Literal["disable", "enable"]
    fabric_ca: Literal["disable", "enable"]
    details: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Ca:
    """
    
    Endpoint: vpn/certificate/ca
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
    ) -> CaObject: ...
    
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
    ) -> FortiObjectList[CaObject]: ...
    
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
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CaObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CaObject: ...


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
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
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
    "Ca",
    "CaPayload",
    "CaResponse",
    "CaObject",
]