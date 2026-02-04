""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/replacemsg/alertmail
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

class AlertmailPayload(TypedDict, total=False):
    """Payload type for Alertmail operations."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AlertmailResponse(TypedDict, total=False):
    """Response type for Alertmail - use with .dict property for typed dict access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AlertmailObject(FortiObject):
    """Typed FortiObject for Alertmail with field access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Alertmail:
    """
    
    Endpoint: system/replacemsg/alertmail
    Category: cmdb
    MKey: msg-type
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
        msg_type: str,
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
    ) -> AlertmailObject: ...
    
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
    ) -> FortiObjectList[AlertmailObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...




    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        msg_type: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_msg_type: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        msg_type: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AlertmailPayload | None = ...,
        msg_type: str | None = ...,
        buffer: str | None = ...,
        header: Literal["none", "http", "8bit"] | None = ...,
        format: Literal["none", "text", "html"] | None = ...,
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
    "Alertmail",
    "AlertmailPayload",
    "AlertmailResponse",
    "AlertmailObject",
]