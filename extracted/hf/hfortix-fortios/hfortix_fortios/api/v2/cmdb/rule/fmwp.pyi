""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: rule/fmwp
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

class FmwpMetadataItem(TypedDict, total=False):
    """Nested item for metadata field."""
    id: int
    metaid: int
    valueid: int


class FmwpPayload(TypedDict, total=False):
    """Payload type for Fmwp operations."""
    name: str
    status: Literal["disable", "enable"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    action: Literal["pass", "block"]
    group: str
    severity: str
    location: str | list[str]
    os: str
    application: str
    service: str
    rule_id: int
    rev: int
    date: int
    metadata: str | list[str] | list[FmwpMetadataItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FmwpResponse(TypedDict, total=False):
    """Response type for Fmwp - use with .dict property for typed dict access."""
    name: str
    status: Literal["disable", "enable"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    action: Literal["pass", "block"]
    group: str
    severity: str
    location: str | list[str]
    os: str
    application: str
    service: str
    rule_id: int
    rev: int
    date: int
    metadata: list[FmwpMetadataItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FmwpMetadataItemObject(FortiObject[FmwpMetadataItem]):
    """Typed object for metadata table items with attribute access."""
    id: int
    metaid: int
    valueid: int


class FmwpObject(FortiObject):
    """Typed FortiObject for Fmwp with field access."""
    name: str
    status: Literal["disable", "enable"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    action: Literal["pass", "block"]
    group: str
    severity: str
    location: str | list[str]
    os: str
    application: str
    service: str
    rule_id: int
    rev: int
    date: int
    metadata: FortiObjectList[FmwpMetadataItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Fmwp:
    """
    
    Endpoint: rule/fmwp
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
    ) -> FmwpObject: ...
    
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
    ) -> FortiObjectList[FmwpObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...




    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FmwpPayload | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        log: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        action: Literal["pass", "block"] | None = ...,
        group: str | None = ...,
        severity: str | None = ...,
        location: str | list[str] | None = ...,
        os: str | None = ...,
        application: str | None = ...,
        service: str | None = ...,
        rule_id: int | None = ...,
        rev: int | None = ...,
        date: int | None = ...,
        metadata: str | list[str] | list[FmwpMetadataItem] | None = ...,
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
    "Fmwp",
    "FmwpPayload",
    "FmwpResponse",
    "FmwpObject",
]